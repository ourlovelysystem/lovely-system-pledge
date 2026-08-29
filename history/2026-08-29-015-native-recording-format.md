# History 015 — Native recording replaces WAV conversion

**Date:** 2026-08-29
**Status:** Corrected
**Specification:** N/A
**Supersedes:** [History 014 — Recording format fixed as WAV PCM](./2026-08-29-014-recording-format-contract.md)
**Related:** [Pledge recording control](../pledge-recording-control.js)

## Context

Pledge briefly converted every browser recording to WAV before playback and upload. The operator asked whether the browser's native MediaRecorder output was suitable without conversion. It was.

The operator then asked:

> So why the fuck are we doing it?

The answer was that WAV conversion had been selected for theoretical consistency without a demonstrated requirement. The operator directed:

> Record in the best available native format. Confirm it can be consumed by AWS transcribe.

## Direction

Pledge records and uploads the best available browser-native format that Amazon Transcribe accepts. It does not convert the recording to WAV.

## Decisions

The control tests browser support in this order:

1. WebM with Opus;
2. MP4 with AAC;
3. Ogg with Opus;
4. WebM without an explicit codec;
5. MP4 without an explicit codec; and
6. Ogg without an explicit codec.

If the browser supports none of these Transcribe-compatible formats, the control refuses to record rather than uploading an arbitrary format.

The actual native MIME type is preserved on the Blob and sent as the upload Content-Type. The visible recording-control version advances to `0.1.3`.

## Corrections

WAV conversion was unnecessary for the present purpose. It added client-side decoding, resampling, encoding, delay, memory use, and a failure surface without making the recording more usable by Amazon Transcribe.

History 014 remains visible as the superseded decision and implementation record.

## Open questions

- The deployed control requires testing in each supported browser family.
- The transcription starter must map the stored MIME type to `webm`, `mp4`, or `ogg` when it starts an Amazon Transcribe job.

## Result

The recording control now preserves a Transcribe-compatible native recording and performs no WAV conversion.

## References

- [Amazon Transcribe input formats](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html)
- [Pledge project history convention](./README.md)
