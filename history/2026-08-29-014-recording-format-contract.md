# History 014 — Recording format fixed as WAV PCM

**Date:** 2026-08-29
**Status:** Implemented
**Specification:** N/A
**Supersedes:** The recording control's pass-through use of the browser-selected media format
**Related:** [Pledge recording control](../pledge-recording-control.js)

## Context

Work resumed on the path from a borrowed voice recording to transcription and eventual catalogue eligibility. Amazon Transcribe input compatibility was initially discussed as though Pledge needed to accommodate the format of an earlier AIFF test artifact.

The operator corrected the premise:

> We are generating the voice recording so we can choose whatever the fuck we want.

The operator then directed:

> Choose the audio format.

## Direction

Pledge controls the submitted recording format. The selected contract is:

```text
container: WAV
encoding: PCM signed 16-bit
channels: mono
sample rate: 16,000 Hz
content type: audio/wav
```

## Decisions

- The browser may use its native recording format during capture.
- Before playback or submission, the control decodes the captured audio, mixes it to mono, resamples it to 16 kHz, and encodes a PCM WAV file.
- The control submits `Content-Type: audio/wav` rather than forwarding a browser-selected media type.
- The visible recording-control version advances to `0.1.2`.
- While WAV preparation is underway, recording, playback, seeking, and submission controls remain disabled.

## Corrections

The earlier compatibility framing was wrong. Pledge does not need to treat the AIFF system-test artifact as an input constraint. It owns the browser recording path and may establish one deliberate output contract.

## Open questions

- The deployed control still requires browser testing with an actual microphone recording.
- The submission Lambda must be verified to preserve `audio/wav` as the S3 object content type.
- The transcription starter must explicitly use `MediaFormat: wav`.

## Result

The WAV encoder was structurally verified locally. Its output contained:

- `RIFF` and `WAVE` identifiers;
- PCM audio format `1`;
- one channel;
- a 16,000 Hz sample rate;
- 16 bits per sample; and
- a correctly sized data section.

## References

- [Amazon Transcribe input formats](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html)
- [Pledge project history convention](./README.md)
