# History 005 — Durable submission intake

**Date:** 2026-08-27  
**Status:** Implemented  
**Specification:** [0.0.0-alpha.1](../SPECIFICATION.md)  
**Supersedes:** None  
**Related:** [Bootstrap browser slice](./2026-08-27-004-bootstrap-browser-slice.md)

## Context

The first executable slice recorded audio in the browser but explicitly stopped before durable submission. The next implementation slice connects a valid browser recording to AWS-backed intake without representing transcription or catalogue admission as complete.

## Direction

A public bootstrap contribution should become durable after synchronous envelope checks and should enter an asynchronous processing queue. The contributor should not wait for transcription.

## Decisions

- AWS SAM defines an HTTP API, Lambda intake function, private versioned S3 bucket, SQS processing queue, and dead-letter queue.
- The browser submits audio through the Pledge API rather than uploading directly to S3.
- The intake accepts base64 audio inside a JSON request. This is suitable for the current 30-second, 4 MiB test boundary and avoids exposing an S3 upload capability to the browser.
- The Lambda checks declared media type, size, duration bounds, base64 integrity, and recognizable container signature.
- Client-reported duration is recorded explicitly as client-reported; it is not treated as independently verified.
- Audio and a canonical JSON submission record are written to S3 before processing is queued.
- The canonical record records the known solicitation, requested function, reference text, catalogue, hash, permission interval, and pending processing states.
- A queue failure leaves a durable record marked `enqueue_failed`; it does not erase the accepted audio.
- The borrowing clock provisionally begins at envelope acceptance. This is an implementation choice still open to correction.
- No receipt, claim credential, revocation behavior, transcription, semantic score, catalogue eligibility, selection, or purge capability is claimed by this slice.

## Corrections

The browser prototype previously allowed its local Submit action to display Come Back Soon without durable storage. Submission now requires a configured API and a successful 202 response before displaying that state.

The synchronous validation implemented here does not yet prove that an audio decoder can render the entire recording or that the signal is usable. It validates a stricter envelope than the browser-only prototype but remains short of the complete envelope contract described by the specification.

## Open questions

- Should the borrowing clock begin at envelope acceptance, catalogue acceptance, or first use?
- Is API-carried base64 audio acceptable beyond the first test, or should Pledge later adopt another bounded upload transport?
- Which decoder and signal checks belong in the intake path?
- What retry process will recover records marked `enqueue_failed`?
- What durable non-content audit fields will survive eventual content purge?
- Which worker will perform transcription and semantic validation?
- How will purge execution and verification work?

## Result

The repository now contains a deployable SAM intake backend and a browser client wired to it through `config.js`. A successful submission stores audio plus canonical metadata and queues asynchronous work.

The processing queue intentionally has no consumer yet.

## References

- [Current specification](../SPECIFICATION.md)
- [Bootstrap browser slice](./2026-08-27-004-bootstrap-browser-slice.md)
- [Project-history convention](./README.md)
