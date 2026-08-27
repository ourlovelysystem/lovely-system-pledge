import base64
import binascii
import hashlib
import json
import os
import time
import uuid
from datetime import datetime, timedelta, timezone

import boto3

s3 = boto3.client("s3")
sqs = boto3.client("sqs")

BUCKET = os.environ["SUBMISSIONS_BUCKET"]
QUEUE_URL = os.environ["PROCESSING_QUEUE_URL"]
MAX_AUDIO_BYTES = int(os.environ.get("MAX_AUDIO_BYTES", "4194304"))
MIN_DURATION_MS = int(os.environ.get("MIN_DURATION_MS", "750"))
MAX_DURATION_MS = int(os.environ.get("MAX_DURATION_MS", "30000"))

ALLOWED_MEDIA_TYPES = {
    "audio/webm": "webm",
    "audio/webm;codecs=opus": "webm",
    "audio/mp4": "m4a",
    "audio/mpeg": "mp3",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
}
TERM_DAYS = {"1-day": 1, "1-week": 7, "1-month": 30, "1-year": 365}


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "content-type": "application/json",
            "cache-control": "no-store",
            "access-control-allow-origin": "*",
        },
        "body": json.dumps(body),
    }


def utc_iso(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def media_signature_matches(media_type, audio):
    if media_type.startswith("audio/webm"):
        return audio.startswith(bytes.fromhex("1a45dfa3"))
    if media_type == "audio/mp4":
        return len(audio) >= 12 and audio[4:8] == b"ftyp"
    if media_type == "audio/mpeg":
        return audio.startswith(b"ID3") or audio[:2] in {
            b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"
        }
    if media_type in {"audio/wav", "audio/x-wav"}:
        return len(audio) >= 12 and audio[:4] == b"RIFF" and audio[8:12] == b"WAVE"
    return False


def parse_submission(event):
    try:
        payload = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc

    media_type = str(payload.get("media_type", "")).lower().strip()
    if media_type not in ALLOWED_MEDIA_TYPES:
        raise ValueError("Unsupported audio media type.")

    try:
        audio = base64.b64decode(payload.get("audio_base64", ""), validate=True)
    except (binascii.Error, ValueError, TypeError) as exc:
        raise ValueError("audio_base64 is not valid base64.") from exc

    if not audio:
        raise ValueError("Audio is required.")
    if len(audio) > MAX_AUDIO_BYTES:
        raise ValueError("Audio exceeds the configured size limit.")
    if not media_signature_matches(media_type, audio):
        raise ValueError("Audio bytes do not match the declared media type.")

    duration_ms = payload.get("duration_ms")
    if not isinstance(duration_ms, int):
        raise ValueError("duration_ms must be an integer.")
    if not MIN_DURATION_MS <= duration_ms <= MAX_DURATION_MS:
        raise ValueError("Audio duration is outside the configured limits.")

    term = payload.get("borrowing_term")
    if term not in TERM_DAYS:
        raise ValueError("Unsupported borrowing term.")

    return payload, audio, media_type, duration_ms, term


def create_submission(event):
    payload, audio, media_type, duration_ms, term = parse_submission(event)
    submission_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(days=TERM_DAYS[term])
    extension = ALLOWED_MEDIA_TYPES[media_type]
    audio_key = f"audio/{submission_id}/source.{extension}"
    record_key = f"submissions/{submission_id}.json"
    digest = hashlib.sha256(audio).hexdigest()

    record = {
        "schema_version": "pledge-submission-0.0.1",
        "submission_id": submission_id,
        "context": "bootstrap",
        "solicitation_text": "Record a voice track that asks the listener: Who are you?",
        "requested_function": "ask the listener who they are",
        "reference_text": "Who are you?",
        "catalogue": "who_are_you",
        "audio_object_reference": audio_key,
        "audio_media_type": media_type,
        "audio_size_bytes": len(audio),
        "audio_duration_ms_reported_by_client": duration_ms,
        "audio_sha256": digest,
        "envelope_accepted_at": utc_iso(created_at),
        "borrowing_starts_at": utc_iso(created_at),
        "expires_at": utc_iso(expires_at),
        "borrowing_term": term,
        "minimum_uses": 0,
        "completed_uses": 0,
        "transcription_status": "pending",
        "catalogue_decision": "pending",
        "processing_status": "enqueue_pending",
        "validation_policy_version": "bootstrap-0.0.1",
        "retention_policy_version": "bootstrap-0.0.1",
        "created_at": utc_iso(created_at),
        "updated_at": utc_iso(created_at),
    }

    s3.put_object(
        Bucket=BUCKET,
        Key=audio_key,
        Body=audio,
        ContentType=media_type,
        Metadata={
            "submission-id": submission_id,
            "expires-at": str(int(expires_at.timestamp())),
            "sha256": digest,
        },
        Tagging=f"state=pending&term={term}",
    )
    s3.put_object(
        Bucket=BUCKET,
        Key=record_key,
        Body=json.dumps(record, indent=2).encode("utf-8"),
        ContentType="application/json",
    )

    try:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({
                "submission_id": submission_id,
                "record_key": record_key,
                "audio_key": audio_key,
            }),
        )
        record["processing_status"] = "queued"
        record["updated_at"] = utc_iso(datetime.now(timezone.utc))
        s3.put_object(
            Bucket=BUCKET,
            Key=record_key,
            Body=json.dumps(record, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception:
        # The canonical record remains inspectable and identifies the enqueue failure.
        record["processing_status"] = "enqueue_failed"
        record["updated_at"] = utc_iso(datetime.now(timezone.utc))
        s3.put_object(
            Bucket=BUCKET,
            Key=record_key,
            Body=json.dumps(record, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
        raise

    return response(202, {
        "submission_id": submission_id,
        "status": "envelope_accepted",
        "processing_status": "queued",
        "expires_at": record["expires_at"],
    })


def lambda_handler(event, _context):
    route = event.get("routeKey", "")
    if route == "GET /health":
        return response(200, {"status": "ok", "server_time": int(time.time())})
    if route == "POST /submissions":
        try:
            return create_submission(event)
        except ValueError as exc:
            return response(400, {"error": str(exc)})
        except Exception:
            return response(500, {"error": "Submission intake failed."})
    return response(404, {"error": "Not found."})
