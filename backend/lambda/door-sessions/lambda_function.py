"""Temporary Pledge door sessions. No borrowed-artifact catalog writes occur here."""

import hashlib
import json
import os
import secrets
import time
import uuid

import boto3


dynamodb = boto3.client("dynamodb")
TABLE_NAME = os.environ["DOOR_SESSIONS_TABLE"]
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
    session_id = event.get("pathParameters", {}).get("session_id")
    token = supplied_token(event)
    if not session_id or not token:
        return response(401, {"error": "A session ID and session token are required."})

    result = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={"session_id": {"S": session_id}},
        ConsistentRead=True,
    )
    item = result.get("Item")
    if not item or not secrets.compare_digest(
        item["browser_session_hash"]["S"], token_hash(token)
    ):
        return response(404, {"error": "Session not found."})

    if int(time.time()) > int(item["valid_until"]["N"]):
        return response(410, {"error": "Session expired."})

    return response(200, {
        "session_id": session_id,
        "status": item["status"]["S"],
        "challenge_id": item["challenge_id"]["S"],
        "recording_seconds": int(item["recording_seconds"]["N"]),
        "valid_until": int(item["valid_until"]["N"]),
    })


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if method == "POST":
        return create_session()
    if method == "GET":
        return get_session(event)
    return response(405, {"error": "Method not allowed."})
