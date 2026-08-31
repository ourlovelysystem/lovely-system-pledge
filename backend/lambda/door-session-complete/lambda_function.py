"""Persist completed temporary door-session transcripts; never write the catalog."""

import json
import os
import time
import urllib.request
import uuid

import boto3


dynamodb = boto3.client("dynamodb")
transcribe = boto3.client("transcribe")
TABLE_NAME = os.environ["DOOR_SESSIONS_TABLE"]
JOB_PREFIX = "pledge-door-"


def session_id_from_job_name(job_name):
    if not job_name.startswith(JOB_PREFIX):
        raise ValueError("Transcription job does not belong to a door session.")
    session_id = job_name[len(JOB_PREFIX):]
    parsed = uuid.UUID(session_id, version=4)
    if str(parsed) != session_id.lower():
        raise ValueError("Door session identifier is not canonical UUIDv4 text.")
    return session_id.lower()


def transcript_text_from_uri(uri):
    with urllib.request.urlopen(uri, timeout=10) as response:
        document = json.load(response)
    transcripts = document.get("results", {}).get("transcripts", [])
    return (transcripts[0].get("transcript", "") if transcripts else "").strip()


def complete_session(session_id, job_name):
    job = transcribe.get_transcription_job(
        TranscriptionJobName=job_name
    )["TranscriptionJob"]
    status = job["TranscriptionJobStatus"]
    now = int(time.time())
    if status == "COMPLETED":
        uri = job["Transcript"]["TranscriptFileUri"]
        transcript_text = transcript_text_from_uri(uri)
        dynamodb.update_item(
            TableName=TABLE_NAME,
            Key={"session_id": {"S": session_id}},
            UpdateExpression=(
                "SET #status = :complete, transcript_text = :text, "
                "transcribed_at = :now, updated_at = :now"
            ),
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":complete": {"S": "complete"},
                ":text": {"S": transcript_text[:100_000]},
                ":now": {"N": str(now)},
            },
        )
        return {"status": "complete", "transcript_text": transcript_text}

    failure_reason = job.get("FailureReason", "Transcription failed.")
    dynamodb.update_item(
        TableName=TABLE_NAME,
        Key={"session_id": {"S": session_id}},
        UpdateExpression=(
            "SET #status = :failed, transcription_failure_reason = :reason, "
            "updated_at = :now"
        ),
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues={
            ":failed": {"S": "failed"},
            ":reason": {"S": failure_reason[:500]},
            ":now": {"N": str(now)},
        },
    )
    return {"status": "failed", "reason": failure_reason}


def lambda_handler(event, context):
    detail = event.get("detail", {})
    job_name = detail.get("TranscriptionJobName", "")
    event_status = detail.get("TranscriptionJobStatus")
    if event_status not in {"COMPLETED", "FAILED"} or not job_name.startswith(JOB_PREFIX):
        return {"ignored": True}
    session_id = session_id_from_job_name(job_name)
    return complete_session(session_id, job_name)
