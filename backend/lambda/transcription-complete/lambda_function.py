import json
import os
import statistics
import time
import urllib.request
import uuid

import boto3


dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
transcribe = boto3.client("transcribe")

ELECTRONIC_VALUABLES_TABLE = os.environ["ELECTRONIC_VALUABLES_TABLE"]
STATE_TABLE = os.environ["STATE_TABLE"]
TRANSCRIPT_BUCKET = os.environ["TRANSCRIPT_BUCKET"]

JOB_PREFIX = "pledge-"
TRANSCRIPT_PREFIX = "transcripts/"
TRANSCRIPTION_POLICY_VERSION = "amazon-transcribe-v1"
MAX_DATABASE_TRANSCRIPT_BYTES = 100_000


def get_boolean_parameter(parameter_name, default=False):
    response = dynamodb.get_item(
        TableName=STATE_TABLE,
        Key={"parameter_name": {"S": parameter_name}},
        ConsistentRead=True,
    )

    value = response.get("Item", {}).get("parameter_value", {})
    return value.get("BOOL", default)


def receipt_from_job_name(job_name):
    if not job_name.startswith(JOB_PREFIX):
        raise ValueError("Transcription job does not belong to Pledge.")

    receipt_id = job_name[len(JOB_PREFIX):]

    try:
        parsed = uuid.UUID(receipt_id, version=4)
    except ValueError as error:
        raise ValueError(
            "Transcription job does not contain a UUIDv4 receipt."
        ) from error

    if str(parsed) != receipt_id.lower():
        raise ValueError("Receipt identifier is not canonical UUIDv4 text.")

    return receipt_id.lower()


def get_catalog_item(receipt_id):
    response = dynamodb.get_item(
        TableName=ELECTRONIC_VALUABLES_TABLE,
        Key={"electronic_valuable_id": {"S": receipt_id}},
        ConsistentRead=True,
    )

    item = response.get("Item")
    if not item:
        raise ValueError(f"No electronic valuable exists for {receipt_id}.")

    return item


def string_value(item, name):
    return item.get(name, {}).get("S")


def load_transcript_document(receipt_id, transcript_uri):
    if get_boolean_parameter("save_transcript_to_object"):
        response = s3.get_object(
            Bucket=TRANSCRIPT_BUCKET,
            Key=f"{TRANSCRIPT_PREFIX}{receipt_id}.json",
        )
        return json.loads(response["Body"].read())

    with urllib.request.urlopen(transcript_uri, timeout=10) as response:
        return json.loads(response.read())


def extract_metrics(document):
    results = document.get("results", {})
    transcripts = results.get("transcripts", [])
    transcript_text = (
        transcripts[0].get("transcript", "") if transcripts else ""
    ).strip()

    pronunciation_items = [
        item
        for item in results.get("items", [])
        if item.get("type") == "pronunciation"
    ]

    confidences = []
    end_times = []

    for item in pronunciation_items:
        alternatives = item.get("alternatives", [])
        if alternatives and alternatives[0].get("confidence") is not None:
            confidences.append(float(alternatives[0]["confidence"]))

        if item.get("end_time") is not None:
            end_times.append(float(item["end_time"]))

    return {
        "transcript_text": transcript_text,
        "word_count": len(pronunciation_items),
        "confidence_mean": (
            statistics.fmean(confidences) if confidences else None
        ),
        "confidence_min": min(confidences) if confidences else None,
        "duration_seconds": max(end_times) if end_times else 0.0,
    }


def update_failed(receipt_id, job_name, failure_reason):
    now = int(time.time())

    dynamodb.update_item(
        TableName=ELECTRONIC_VALUABLES_TABLE,
        Key={"electronic_valuable_id": {"S": receipt_id}},
        UpdateExpression=(
            "SET #transcription_status = :failed, "
            "#transcription_failure_reason = :reason, "
            "#updated_at = :updated_at"
        ),
        ConditionExpression="#transcription_job_name = :job_name",
        ExpressionAttributeNames={
            "#transcription_status": "transcription_status",
            "#transcription_failure_reason": "transcription_failure_reason",
            "#transcription_job_name": "transcription_job_name",
            "#updated_at": "updated_at",
        },
        ExpressionAttributeValues={
            ":failed": {"S": "failed"},
            ":reason": {"S": (failure_reason or "Unknown failure")[:500]},
            ":job_name": {"S": job_name},
            ":updated_at": {"N": str(now)},
        },
    )


def update_completed(receipt_id, job_name, job, metrics):
    transcript_text = metrics["transcript_text"]
    transcript_bytes = len(transcript_text.encode("utf-8"))

    if transcript_bytes > MAX_DATABASE_TRANSCRIPT_BYTES:
        raise ValueError(
            f"Transcript is too large for the catalog: "
            f"{transcript_bytes} bytes."
        )

    completed_at = int(
        job.get("CompletionTime", time.time()).timestamp()
        if hasattr(job.get("CompletionTime"), "timestamp")
        else time.time()
    )

    names = {
        "#transcription_status": "transcription_status",
        "#transcription_provider": "transcription_provider",
        "#transcription_language_code": "transcription_language_code",
        "#transcription_completed_at": "transcription_completed_at",
        "#transcription_policy_version": "transcription_policy_version",
        "#recognized_word_count": "recognized_word_count",
        "#recognized_duration_seconds": "recognized_duration_seconds",
        "#transcription_job_name": "transcription_job_name",
        "#transcription_failure_reason": "transcription_failure_reason",
        "#transcript_text": "transcript_text",
        "#updated_at": "updated_at",
    }

    values = {
        ":completed": {"S": "completed"},
        ":provider": {"S": "amazon-transcribe"},
        ":language_code": {
            "S": job.get("LanguageCode", "unknown")
        },
        ":completed_at": {"N": str(completed_at)},
        ":policy_version": {"S": TRANSCRIPTION_POLICY_VERSION},
        ":word_count": {"N": str(metrics["word_count"])},
        ":duration": {
            "N": f'{metrics["duration_seconds"]:.3f}'
        },
        ":job_name": {"S": job_name},
        ":updated_at": {"N": str(int(time.time()))},
    }

    assignments = [
        "#transcription_status = :completed",
        "#transcription_provider = :provider",
        "#transcription_language_code = :language_code",
        "#transcription_completed_at = :completed_at",
        "#transcription_policy_version = :policy_version",
        "#recognized_word_count = :word_count",
        "#recognized_duration_seconds = :duration",
        "#updated_at = :updated_at",
    ]

    removals = ["#transcription_failure_reason"]

    if metrics["confidence_mean"] is not None:
        names["#transcription_confidence_mean"] = (
            "transcription_confidence_mean"
        )
        values[":confidence_mean"] = {
            "N": f'{metrics["confidence_mean"]:.6f}'
        }
        assignments.append(
            "#transcription_confidence_mean = :confidence_mean"
        )

    if metrics["confidence_min"] is not None:
        names["#transcription_confidence_min"] = (
            "transcription_confidence_min"
        )
        values[":confidence_min"] = {
            "N": f'{metrics["confidence_min"]:.6f}'
        }
        assignments.append(
            "#transcription_confidence_min = :confidence_min"
        )

    if get_boolean_parameter("save_transcript_to_database"):
        values[":transcript_text"] = {"S": transcript_text}
        assignments.append("#transcript_text = :transcript_text")
    else:
        removals.append("#transcript_text")

    update_expression = "SET " + ", ".join(assignments)
    if removals:
        update_expression += " REMOVE " + ", ".join(removals)

    dynamodb.update_item(
        TableName=ELECTRONIC_VALUABLES_TABLE,
        Key={"electronic_valuable_id": {"S": receipt_id}},
        UpdateExpression=update_expression,
        ConditionExpression="#transcription_job_name = :job_name",
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
    )


def lambda_handler(event, context):
    detail = event.get("detail", {})
    job_name = detail.get("TranscriptionJobName")
    event_status = detail.get("TranscriptionJobStatus")

    if not job_name or not event_status:
        raise ValueError("Event does not describe a transcription job.")

    receipt_id = receipt_from_job_name(job_name)
    item = get_catalog_item(receipt_id)

    if string_value(item, "transcription_job_name") != job_name:
        raise ValueError("Catalog record does not match the job name.")

    response = transcribe.get_transcription_job(
        TranscriptionJobName=job_name
    )
    job = response["TranscriptionJob"]
    actual_status = job["TranscriptionJobStatus"]

    if event_status != actual_status:
        raise ValueError(
            f"Event status {event_status} does not match "
            f"job status {actual_status}."
        )

    if actual_status == "FAILED":
        update_failed(
            receipt_id,
            job_name,
            job.get("FailureReason"),
        )
        return {
            "ok": True,
            "receipt_id": receipt_id,
            "transcription_status": "failed",
        }

    if actual_status != "COMPLETED":
        raise ValueError(
            f"Unsupported transcription status: {actual_status}."
        )

    transcript_uri = job["Transcript"]["TranscriptFileUri"]
    document = load_transcript_document(receipt_id, transcript_uri)
    metrics = extract_metrics(document)

    update_completed(
        receipt_id,
        job_name,
        job,
        metrics,
    )

    return {
        "ok": True,
        "receipt_id": receipt_id,
        "transcription_status": "completed",
        "word_count": metrics["word_count"],
        "confidence_mean": metrics["confidence_mean"],
        "confidence_min": metrics["confidence_min"],
        "duration_seconds": metrics["duration_seconds"],
        "transcript_saved_to_database": get_boolean_parameter(
            "save_transcript_to_database"
        ),
    }