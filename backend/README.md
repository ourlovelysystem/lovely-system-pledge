# Pledge backend

This SAM application implements durable public voice-submission intake.

## Deploy

```bash
cd backend
sam validate
sam build
sam deploy --guided
```

After deployment, copy the `ApiUrl` output into `../config.js`.

## Current routes

- `GET /health`
- `POST /submissions`

The intake route accepts JSON containing `audio_base64`, `media_type`, `duration_ms`, and `borrowing_term`. It writes the audio and canonical JSON record to private, versioned S3 storage, then queues the submission in SQS.

The queue has no processing consumer yet. Transcription, semantic validation, catalogue admission, expiration, and purge remain future slices.
