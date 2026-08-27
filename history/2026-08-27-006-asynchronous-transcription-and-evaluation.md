# History 006 — Asynchronous transcription and provisional evaluation

**Date:** 2026-08-27  
**Status:** Implemented in repository; deployment pending  
**Specification:** [0.0.0-alpha.1](../SPECIFICATION.md)  
**Supersedes:** None  
**Related:** [Durable submission intake](./2026-08-27-005-durable-submission-intake.md)

## Context

Durable intake stores accepted audio and its canonical submission record before
placing a processing message on SQS. The queue previously had no consumer.

## Direction

Processing remains asynchronous. The contributor does not wait for
transcription or semantic evaluation. This slice consumes the existing queue,
records the result in the canonical S3 submission record, and stops before
catalogue publication or playback.

## Decisions

- An SQS-triggered Lambda starts an Amazon Transcribe batch job for each
  accepted submission.
- Transcription jobs use an application-qualified `pledge-` prefix followed by
  the submission UUID.
- Amazon Transcribe writes its complete JSON result into the private,
  versioned submissions bucket.
- Amazon EventBridge delivers `COMPLETED` and `FAILED` Transcribe job-state
  events to a completion Lambda.
- The completion Lambda stores the combined transcript and average confidence
  from pronunciation items in the canonical submission record.
- Failed jobs preserve the failure supplied by the Transcribe event.
- SQS partial-batch failure reporting prevents one failed item from forcing
  successful items in the same batch to be retried.
- A deterministic bootstrap rule set performs the first semantic evaluation.
  It records its evaluator version and an inspectable reason.
- The evaluator recognizes direct identity questions, ordinary rearrangements,
  added language, name requests, and identity requests. Ambiguous identity
  language requires review; unrelated speech is marked unusable.
- The semantic score is a rule output. It is not represented as a calibrated
  probability.
- A `usable` decision in the submission record does not yet publish the track
  into a selectable catalogue.
- The committed SAM configuration names the CloudFormation stack
  `lovely-system-pledge` and requires changeset confirmation.

## Known limitation

The bootstrap evaluator cannot provide general semantic understanding. It is
deliberately small, testable, and visible. The specification's broader
tolerance for nonliteral phrasing will require calibration and may require a
different evaluator after a real test collection exists.

EventBridge delivery is best effort. A later reconciliation process must find
Transcribe jobs or submission records that remain in progress after their
expected completion window.

## Verification

Repository unit tests cover:

- direct identity questions;
- humorous additions;
- name-request variants;
- ambiguous identity language;
- unrelated speech;
- confidence averaging; and
- empty transcript results.

The local execution environment did not include the SAM CLI, so
`sam validate --lint` and deployment remain operator-side verification steps.

## Result

The repository now contains the asynchronous processing consumer and
completion handler. Deployment is intentionally not claimed by this record.

## References

- [Amazon Transcribe EventBridge events](https://docs.aws.amazon.com/transcribe/latest/dg/monitoring-events.html)
- [StartTranscriptionJob API](https://docs.aws.amazon.com/transcribe/latest/APIReference/API_StartTranscriptionJob.html)
- [Durable submission intake](./2026-08-27-005-durable-submission-intake.md)
