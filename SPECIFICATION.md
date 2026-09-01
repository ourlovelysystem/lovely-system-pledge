# Pledge Specification

**Version:** 0.1.0-alpha  
**Date:** 2026-09-01  
**Status:** Current implemented behavior and declared boundaries  
**Project:** `pledge.ourlovelysystem.org`

## 1. Purpose

Pledge is a voice-gated system that speaks with temporarily borrowed voices.

A person may lend a recording that performs an auditory challenge. Pledge transcribes and evaluates that recording asynchronously before admitting it to a time-bounded catalogue of challenge voices. A visitor may then hear a borrowed challenge, make a short spoken response, and receive a private receipt showing what Pledge recorded and transcribed.

Pledge does not claim speaker biometrics, civil identity verification, or present-day authorization of a user account. It records a bounded voice interaction and makes its processing visible to the submitting browser.

## 2. Governing distinctions

Pledge maintains two independent flows. They must not be conflated.

| Flow | Purpose | Current result |
|---|---|---|
| Borrowed electronic valuable | Supply a challenge voice to Pledge | A usable, unexpired recording may be selected and played as a challenge. |
| Door session | Let a visitor hear a challenge and leave a response | A private temporary record is created, transcribed, and displayed to that browser. |

A catalogue voice is evaluated for whether it performs the requested function: asking the listener to identify themselves. A door response is currently transcribed and retained in its private temporary session. It is **not** presently semantically evaluated for admission, identity, or `isNotMute=true`.

## 3. Borrowed challenge voices

### 3.1 Requested function

The initial challenge function is:

> Ask the listener to identify themselves.

The reference phrase is:

> Who are you?

Pledge accepts semantic variation rather than exact repetition. Humor, awkward grammar, or a nonliteral phrasing may still perform the function.

### 3.2 Asynchronous catalogue processing

A submitted candidate recording is transcribed by Amazon Transcribe. Pledge records transcription measures when available and uses Amazon Bedrock Nova Micro to make a separate semantic-function judgment.

The stored measures are distinct:

- **Transcription confidence**: how confidently Transcribe recognized words.
- **Semantic match score**: how well the transcript performs the requested function.
- **Content decision**: `usable`, `review_required`, or `unusable`.

Transcription confidence is not semantic correctness. A poor transcription-confidence result is not automatically a bad challenge voice.

### 3.3 Catalogue eligibility and selection

A challenge is eligible only when it is marked `catalog_eligible`, is in borrowed status, is unexpired, and has usable object metadata.

When a door session begins, Pledge selects an eligible voice. It prioritizes eligible recordings whose `use_count` remains below `minimum_uses`; otherwise it selects randomly from the eligible set.

Challenge playback is acknowledged separately. That acknowledgement increments the selected voice's use count once.

## 4. Door-session experience

### 4.1 One-button interaction

The public door page is `/door.html`.

The intended current interaction is one press of **Step Up**:

1. Pledge creates a private door session and selects a borrowed challenge.
2. Pledge plays that challenge without exposing a browser audio slider.
3. When the challenge ends, Pledge emits an audible rising double tone and begins recording.
4. Pledge records for the session's configured limit, currently 15 seconds.
5. Pledge stops recording and emits an audible falling double tone.
6. Pledge uploads and submits the response automatically.
7. Pledge redirects to the private recording receipt.

There are no manual repeat, record, stop, submit, or response-playback controls in the current door flow.

A browser that denies microphone permission receives an error and may try again.

### 4.2 Private recording receipt

The receipt page is `/recording.html`.

After submission, the browser stores only an opaque temporary session handle in `sessionStorage`: a session identifier and a random browser-session token. It does not store the transcript, audio, or authoritative status.

The receipt retrieves the session through the API using that token. It displays:

- receipt/session identifier;
- challenge identifier;
- current status;
- recorded media type;
- recording limit;
- created, submitted, transcribed, and validity times;
- transcription text when complete; or
- transcription failure reason when applicable.

The receipt is private to that browser session. Its token is not placed in the URL, and there is no public recording-record route.

The receipt does not poll. A person may reload or return to it to obtain current server state.

## 5. Door-session processing

### 5.1 Session creation and upload

A new door session has:

- a random UUID session identifier;
- a hashed browser-session token stored server-side;
- a selected challenge identifier and object reference;
- a 15-second recording limit;
- a 12-hour access-validity window; and
- a 24-hour DynamoDB TTL window.

The browser requests a presigned S3 PUT URL for a supported response type: `audio/webm`, `audio/ogg`, or `audio/mp4`. The bucket permits this PUT only from `https://pledge.ourlovelysystem.org` with `Content-Type`.

### 5.2 Submission and transcription

When the S3 object exists, submission starts an Amazon Transcribe job named:

```text
pledge-door-<session UUID>
```

The session moves to `submitted`. Amazon Transcribe completion emits an EventBridge event. The rule `lovely-system-pledge-door-session-transcription-complete` invokes `lovely-system-pledge-door-session-complete`.

On successful completion, that Lambda retrieves the transcript and updates the private session to:

```text
status = complete
transcript_text = <recognized text>
transcribed_at = <epoch seconds>
```

On a transcription failure, it updates the private session to `failed` and preserves the failure reason.

Observed recent tests completed the submit-to-transcript path in approximately 8–9 seconds. That is an observed result, not a service guarantee.

## 6. API boundary

The HTTP API is at `https://api.pledge.ourlovelysystem.org`.

| Method and route | Purpose |
|---|---|
| `POST /door-sessions` | Create a private session and return a selected challenge URL. |
| `POST /door-sessions/{session_id}/challenge-played` | Acknowledge challenge playback and increment use count once. |
| `POST /door-sessions/{session_id}/upload-url` | Return a private presigned response-upload URL. |
| `POST /door-sessions/{session_id}/submit` | Verify upload and start Transcribe. |
| `GET /door-sessions/{session_id}` | Return the authorized browser's session metadata and transcript/failure when available. |

All session-specific routes require the browser-session token in `x-pledge-session-token`. The server stores its hash, not the token itself.

## 7. State model

### 7.1 Door-session states

```text
ready
upload_pending
submitted
complete
failed
```

`complete` means the private temporary response has been transcribed and written to the door-session record. It does not mean the visitor has been authenticated, identified, admitted to a user zone, or granted `isNotMute=true`.

### 7.2 Catalogue state

The catalogue is distinct from door sessions. Challenge candidates record transcription, semantic validation, eligibility, expiration, use counts, and borrowing status. Pledge uses only currently eligible borrowed items as audible challenges.

## 8. Privacy, retention, and borrowing direction

Borrowed voices are not permanent donations. Pledge borrows them under bounded terms.

The system maintains temporary response objects separately from the catalogue. Door-session completion never writes a visitor response to the challenge catalogue.

A receipt is possession evidence for an electronic valuable; it is not proof that a claimant is the speaker or sole interested party. The claimed-item custody and public-accountability process remains a declared direction, not a currently exposed feature.

Expiration must make borrowed catalogue audio ineligible immediately. Aggressive deletion of expired audio, transcript, and derived content is required by Pledge's intended policy, but automated purge/verification is not yet implemented.

## 9. Explicit current limits

Pledge does not yet implement:

- granting `isNotMute=true`;
- semantic evaluation of door responses for authorization;
- speaker biometric or civil identity verification;
- authenticated account integration;
- trustee, agent, or seniority roles;
- receipt-claim endpoint or public claim ledger;
- withdrawal interface;
- automated expiration purge and purge verification;
- production retention/withdrawal rules for claimed material; or
- a public recording browser.

The current door interface is functional but visually provisional. Its one-button interaction and private receipt are the current tested interface, not a final visual design.

## 10. Recovery statement

> Pledge speaks with eligible borrowed voices. A visitor presses Step Up, hears a question, receives an audible recording boundary, and leaves one short response. Pledge submits it, transcribes it asynchronously, and gives the submitting browser a private receipt. A completed receipt proves transcription persistence, not identity, authentication, or admission.
