import json
import os
import re
from datetime import datetime, timezone

import boto3


s3 = boto3.client("s3")
transcribe = boto3.client("transcribe")

BUCKET = os.environ["SUBMISSIONS_BUCKET"]
JOB_PREFIX = os.environ.get("TRANSCRIBE_JOB_PREFIX", "pledge-")
LANGUAGE_CODE = os.environ.get("TRANSCRIBE_LANGUAGE_CODE", "en-US")


def utc_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_record(record_key):
    result = s3.get_object(Bucket=BUCKET, Key=record_key)
    return json.loads(result["Body"].read())


def save_record(record_key, record):
    record["updated_at"] = utc_iso()
    s3.put_object(
        Bucket=BUCKET,
        Key=record_key,
        Body=json.dumps(record, indent=2).encode("utf-8"),
        ContentType="application/json",
    )


def media_format(media_type):
    if media_type.startswith("audio/webm"):
        return "webm"
    return {
        "audio/mp4": "mp4",
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "audio/x-wav": "wav",
    }[media_type]


def start_one(message):
    submission_id = message["submission_id"]
    record_key = message["record_key"]
    record = load_record(record_key)
    job_name = f"{JOB_PREFIX}{submission_id}"
    transcript_key = f"transcripts/{submission_id}/aws-transcribe.json"

    if record.get("transcription_status") in {"in_progress", "completed"}:
        return

    # Persist the deterministic job and output names before starting external
    # work so an unusually fast completion event can always resolve them.
    record["transcription_job_name"] = job_name
    record["transcript_object_reference"] = transcript_key
    record["transcription_status"] = "starting"
    record["processing_status"] = "transcription_starting"
    record.pop("processing_error", None)
    save_record(record_key, record)

    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=LANGUAGE_CODE,
            MediaFormat=media_format(record["audio_media_type"]),
            Media={
                "MediaFileUri": (
                    f"s3://{BUCKET}/{record['audio_object_reference']}"
                )
            },
            OutputBucketName=BUCKET,
            OutputKey=transcript_key,
            Settings={"ShowAlternatives": False},
        )
    except Exception as exc:
        error = getattr(exc, "response", {}).get("Error", {})
        if error.get("Code") != "ConflictException":
            record["transcription_status"] = "start_failed"
            record["processing_status"] = "transcription_start_failed"
            record["processing_error"] = error.get("Code", "unknown")
            save_record(record_key, record)
            raise

    record["transcription_status"] = "in_progress"
    record["processing_status"] = "transcription_in_progress"
    record.pop("processing_error", None)
    save_record(record_key, record)


def start_handler(event, _context):
    failures = []
    for item in event.get("Records", []):
        try:
            start_one(json.loads(item["body"]))
        except Exception:
            failures.append({"itemIdentifier": item["messageId"]})
    return {"batchItemFailures": failures}


def average_confidence(transcript_document):
    values = []
    for item in transcript_document.get("results", {}).get("items", []):
        if item.get("type") != "pronunciation":
            continue
        alternatives = item.get("alternatives") or []
        if alternatives and "confidence" in alternatives[0]:
            values.append(float(alternatives[0]["confidence"]))
    if not values:
        return None
    return round(sum(values) / len(values), 4)


def semantic_evaluation(transcript_text):
    """Provisional, inspectable bootstrap evaluator; not a probability model."""
    normalized = re.sub(r"[^a-z0-9' ]+", " ", transcript_text.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    tokens = set(normalized.split())

    exact = normalized in {"who are you", "who you", "who you are"}
    identity_question = "who" in tokens and bool(tokens & {"you", "your"})
    name_request = "name" in tokens and bool(
        tokens & {"your", "say", "tell", "give", "sing"}
    )
    identity_request = "identity" in tokens and bool(
        tokens & {"your", "state", "tell", "give"}
    )

    if exact:
        score = 1.0
        reason = "recognized_direct_identity_question"
    elif identity_question:
        score = 0.9
        reason = "recognized_identity_question_variant"
    elif name_request or identity_request:
        score = 0.82
        reason = "recognized_identity_request_variant"
    elif tokens & {"who", "name", "identity"}:
        score = 0.5
        reason = "identity_language_without_clear_requested_function"
    else:
        score = 0.1
        reason = "requested_function_not_recognized"

    if score >= 0.8:
        decision = "usable"
    elif score >= 0.35:
        decision = "review_required"
    else:
        decision = "unusable"

    return {
        "semantic_match_score": score,
        "catalogue_decision": decision,
        "semantic_evaluation_reason": reason,
        "semantic_evaluator": "bootstrap-rules-0.0.1",
    }


def transcript_text(transcript_document):
    transcripts = transcript_document.get("results", {}).get("transcripts", [])
    if not transcripts:
        return ""
    return str(transcripts[0].get("transcript", "")).strip()


def completion_handler(event, _context):
    detail = event.get("detail", {})
    job_name = detail.get("TranscriptionJobName", "")
    status = detail.get("TranscriptionJobStatus", "")
    if not job_name.startswith(JOB_PREFIX):
        return {"ignored": True}

    submission_id = job_name[len(JOB_PREFIX):]
    record_key = f"submissions/{submission_id}.json"
    record = load_record(record_key)

    if status == "FAILED":
        record["transcription_status"] = "failed"
        record["processing_status"] = "transcription_failed"
        record["processing_error"] = detail.get("FailureReason", "unknown")
        save_record(record_key, record)
        return {"submission_id": submission_id, "status": "failed"}

    if status != "COMPLETED":
        return {"ignored": True}

    transcript_key = record["transcript_object_reference"]
    transcript_document = json.loads(
        s3.get_object(Bucket=BUCKET, Key=transcript_key)["Body"].read()
    )
    text = transcript_text(transcript_document)
    confidence = average_confidence(transcript_document)

    record["transcript"] = text
    record["transcription_confidence"] = confidence
    record["transcription_status"] = "completed"
    record.update(semantic_evaluation(text))
    record["processing_status"] = "evaluation_completed"
    record.pop("processing_error", None)
    save_record(record_key, record)
    return {
        "submission_id": submission_id,
        "status": record["processing_status"],
        "decision": record["catalogue_decision"],
    }
