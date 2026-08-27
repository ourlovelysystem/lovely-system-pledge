# Pledge backend

This SAM application implements durable public voice-submission intake and
asynchronous transcription and bootstrap evaluation.

## Deploy

```bash
cd backend
sam validate
sam build
sam deploy
```

The committed `samconfig.toml` uses the application-qualified CloudFormation
stack name `lovely-system-pledge` and requires changeset confirmation.

After deployment, copy the `ApiUrl` output into `../config.js`.

## Current routes

- `GET /health`
- `POST /submissions`

The intake route accepts JSON containing `audio_base64`, `media_type`, `duration_ms`, and `borrowing_term`. It writes the audio and canonical JSON record to private, versioned S3 storage, then queues the submission in SQS.

The SQS consumer starts an Amazon Transcribe job. An EventBridge completion
handler records the transcript, average word confidence, provisional semantic
score, inspectable reason, and decision in the canonical submission record.

The semantic evaluator is an explicit bootstrap rule set, not a probability
model. It recognizes direct and common identity-question variants. Catalogue
publication, playback selection, expiration, and purge remain future slices.
