"""Temporary Pledge door sessions. No borrowed-artifact catalog writes occur here."""

import base64
import hashlib
import json
import os
import secrets
import time
import uuid

import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
transcribe = boto3.client("transcribe")
TABLE_NAME = os.environ["DOOR_SESSIONS_TABLE"]
TEMPORARY_SESSIONS_BUCKET = os.environ["TEMPORARY_SESSIONS_BUCKET"]
SESSION_VALID_SECONDS = int(os.environ.get("SESSION_VALID_SECONDS", "43200"))
SESSION_TTL_SECONDS = int(os.environ.get("SESSION_TTL_SECONDS", "86400"))
CHALLENGE_ID = "who-are-you-v1"
RECORDING_SECONDS = 15


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json",
            "cache-control": "no-store",
        },
        "body": json.dumps(body),
    }


def token_hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def supplied_token(event):
    headers = {key.lower(): value for key, value in event.get("headers", {}).items()}
    return headers.get("x-pledge-session-token")


def request_json(event):
    body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    try:
        value = json.loads(body)
    except json.JSONDecodeError as error:
        raise ValueError("Request body must be JSON.") from error
    if not isinstance(value, dict):
        raise ValueError("Request body must be a JSON object.")
    return value


def authorized_session(event):
    session_id = event.get("pathParameters", {}).get("session_id")
    token = supplied_token(event)
    if not session_id or not token:
        return None, response(401, {"error": "A session ID and session token are required."})
    result = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={"session_id": {"S": session_id}},
        ConsistentRead=True,
    )
    item = result.get("Item")
    if not item or not secrets.compare_digest(
        item["browser_session_hash"]["S"], token_hash(token)
    ):
        return None, response(404, {"error": "Session not found."})
    if int(time.time()) > int(item["valid_until"]["N"]):
        return None, response(410, {"error": "Session expired."})
    return item, None


def create_session():
    now = int(time.time())
    session_id = str(uuid.uuid4())
    token = secrets.token_urlsafe(32)
    valid_until = now + SESSION_VALID_SECONDS
    ttl_until = now + SESSION_TTL_SECONDS
    dynamodb.put_item(
        TableName=TABLE_NAME,
        Item={
            "session_id": {"S": session_id},
            "browser_session_hash": {"S": token_hash(token)},
            "status": {"S": "ready"},
            "challenge_id": {"S": CHALLENGE_ID},
            "recording_seconds": {"N": str(RECORDING_SECONDS)},
            "created_at": {"N": str(now)},
            "updated_at": {"N": str(now)},
            "valid_until": {"N": str(valid_until)},
            "expires_at": {"N": str(ttl_until)},
        },
        ConditionExpression="attribute_not_exists(session_id)",
    )
    return response(201, {
        "session_id": session_id,
        "browser_session_token": token,
        "status": "ready",
        "challenge_id": CHALLENGE_ID,
        "recording_seconds": RECORDING_SECONDS,
        "valid_until": valid_until,
    })


def get_session(event):
    item, error_response = authorized_session(event)
    if error_response:
        return error_response
    session_id = item["session_id"]["S"]

    session = {
        "session_id": session_id,
        "status": item["status"]["S"],
        "challenge_id": item["challenge_id"]["S"],
        "recording_seconds": int(item["recording_seconds"]["N"]),
        "valid_until": int(item["valid_until"]["N"]),
    }
    if "transcript_text" in item:
        session["transcript_text"] = item["transcript_text"]["S"]
    if "transcription_failure_reason" in item:
        session["transcription_failure_reason"] = item["transcription_failure_reason"]["S"]
    return response(200, session)


def create_upload_url(event):
    item, error_response = authorized_session(event)
    if error_response:
        return error_response
    try:
        body = request_json(event)
    except ValueError as error:
        return response(400, {"error": str(error)})

    content_type = body.get("content_type")
    if content_type not in {"audio/webm", "audio/ogg", "audio/mp4"}:
        return response(400, {"error": "Unsupported recording content type."})

    session_id = item["session_id"]["S"]
    object_key = f"temporary-sessions/{session_id}/recording"
    now = int(time.time())
    dynamodb.update_item(
        TableName=TABLE_NAME,
        Key={"session_id": {"S": session_id}},
        UpdateExpression=(
            "SET #status = :status, audio_object_key = :key, "
            "audio_content_type = :content_type, updated_at = :now"
        ),
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues={
            ":status": {"S": "upload_pending"},
            ":key": {"S": object_key},
            ":content_type": {"S": content_type},
            ":now": {"N": str(now)},
        },
    )
    upload_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": TEMPORARY_SESSIONS_BUCKET,
            "Key": object_key,
            "ContentType": content_type,
        },
        ExpiresIn=300,
        HttpMethod="PUT",
    )
    return response(200, {
        "object_key": object_key,
        "content_type": content_type,
        "upload_url": upload_url,
        "upload_url_expires_in_seconds": 300,
    })


def submit_recording(event):
    item, error_response = authorized_session(event)
    if error_response:
        return error_response
    session_id = item["session_id"]["S"]
    object_key = item.get("audio_object_key", {}).get("S")
    content_type = item.get("audio_content_type", {}).get("S")
    if not object_key or not content_type:
        return response(409, {"error": "No recording upload is pending for this session."})
    try:
        s3.head_object(Bucket=TEMPORARY_SESSIONS_BUCKET, Key=object_key)
    except ClientError as error:
        if error.response.get("Error", {}).get("Code") in {"404", "NoSuchKey", "NotFound"}:
            return response(409, {"error": "The recording has not been uploaded."})
        raise

    media_format = {
        "audio/webm": "webm",
        "audio/ogg": "ogg",
        "audio/mp4": "mp4",
    }[content_type]
    job_name = f"pledge-door-{session_id}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode="en-US",
        MediaFormat=media_format,
        Media={"MediaFileUri": f"s3://{TEMPORARY_SESSIONS_BUCKET}/{object_key}"},
    )
    now = int(time.time())
    dynamodb.update_item(
        TableName=TABLE_NAME,
        Key={"session_id": {"S": session_id}},
        UpdateExpression=(
            "SET #status = :status, transcription_job_name = :job_name, "
            "submitted_at = :now, updated_at = :now"
        ),
        ExpressionAttributeNames={"#status": "status"},
        ExpressionAttributeValues={
            ":status": {"S": "submitted"},
            ":job_name": {"S": job_name},
            ":now": {"N": str(now)},
        },
    )
    return response(202, {
        "session_id": session_id,
        "status": "submitted",
        "transcription_job_name": job_name,
    })


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if method == "POST":
        if event.get("pathParameters", {}).get("session_id"):
            if event.get("rawPath", "").endswith("/submit"):
                return submit_recording(event)
            return create_upload_url(event)
        return create_session()
    if method == "GET":
        return get_session(event)
    return response(405, {"error": "Method not allowed."})
