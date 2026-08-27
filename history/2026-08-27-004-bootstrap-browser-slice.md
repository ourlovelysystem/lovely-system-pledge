# History 004 — Bootstrap browser slice

**Date:** 2026-08-27  
**Status:** Implemented  
**Specification:** [0.0.0-alpha.1](../SPECIFICATION.md)  
**Supersedes:** None  
**Related:** [Bootstrap voice solicitation history](./2026-08-27-001-bootstrap-voice-specification.md)

## Context

The repository contained the recoverable bootstrap specification and project history but no executable application. The operator ended an unrelated logging detour and directed: “Pledge.”

## Direction

Begin building from Pledge's outermost layer. Establish the bootstrap presentation and browser recording interaction before claiming that durable storage, asynchronous transcription, catalogue admission, selection, expiration, or purge exist.

## Decisions

- The first implementation is a framework-free static browser slice.
- The landing page presents the no-voice bootstrap question.
- Consent opens the reusable bootstrap solicitation interface.
- The browser requests microphone access only after the visitor elects to record.
- A live audiograph represents microphone input.
- Local envelope checks require a nontrivial audio object and a duration between 0.75 and 30 seconds.
- The visitor may listen to or discard the recording.
- Borrowing-period choices are presented in day-scale units already named in the project direction.
- The interface explicitly states that durable submission is not connected.
- The Come Back Soon state is reached only after a locally valid recording is submitted.

## Corrections

None.

## Open questions

- Which backend contract will receive the audio and metadata?
- Which AWS resources will implement canonical storage, the processing queue, transcription, semantic validation, inventory, expiration, and purge?
- When should the borrowing clock begin?
- What exact signal-quality check belongs in synchronous envelope validation?
- Should the temporary 0.75–30 second bounds remain?
- What should declining the solicitation do beyond leaving Pledge mute?
- Should the day-scale borrowing choices remain visible during the first backend test, or should a test-only control exist elsewhere?
- The current browser slice does not create a receipt or claim credential.

## Result

Pledge now has an executable front-end slice covering bootstrap consent, voice solicitation, recording, a live microphone audiograph, replay, discard, local envelope validation, and Come Back Soon.

No durable or asynchronous capability is represented as complete.

## References

- [Current specification](../SPECIFICATION.md)
- [Project-history convention](./README.md)
- [Bootstrap voice solicitation history](./2026-08-27-001-bootstrap-voice-specification.md)
