# History 016 — Native audio retained; playback conversion deferred

**Date:** 2026-08-29
**Status:** Accepted direction
**Specification:** N/A
**Supersedes:** None
**Related:** [History 015 — Native recording replaces WAV conversion](./2026-08-29-015-native-recording-format.md)

## Context

After Pledge removed unnecessary WAV conversion, the operator asked how playable the supported native formats would be and required the options to be scored for recording, replay, and transcription.

The evaluated native formats were WebM/Opus, MP4/AAC, and Ogg/Opus.

## Direction

The scores are structured estimates for current major browsers on a 0–100 scale. They are comparative judgments, not measured compatibility rates or calibrated probabilities.

| Native format | Recording | Replay | AWS transcription |
|---|---:|---:|---:|
| **WebM/Opus** | **96** | 93 | **96** |
| **MP4/AAC** | 86 | **99** | 94 |
| **Ogg/Opus** | 76 | 80 | **96** |

The comparison identified:

- WebM/Opus as the strongest native-recording choice;
- MP4/AAC as the strongest cross-browser replay choice; and
- WebM/Opus and Ogg/Opus as narrow transcription leaders, with MP4/AAC still fully suitable.

## Decisions

Pledge will use the simplest implementation now:

1. record the best supported native format;
2. upload the original recording unchanged;
3. transcribe the original asynchronously;
4. replay the original where supported; and
5. perform no audio conversion.

The current preference order remains:

1. WebM/Opus;
2. MP4/AAC;
3. Ogg/Opus;
4. the corresponding containers without an explicit codec declaration.

A possible later optimization is documented and deferred:

    native borrowed recording
    → immediate durable upload and receipt
    → asynchronous MP4/AAC playback derivative

If implemented later, the original recording would remain the borrowed source asset. The playback derivative would inherit the original's expiration, withdrawal, and deletion rules. Transcription would continue to use the original rather than a lossy playback derivative.

## Corrections

No correction to History 015 is required. This entry clarifies the tradeoff between optimal native recording and maximum cross-browser replay, then records the decision not to add conversion now.

## Open questions

- Will observed replay failures justify an MP4/AAC derivative?
- What browser and device evidence would cross the implementation threshold?
- If created, should the derivative use playback/<receipt_id>.m4a or another resource namespace?

## Result

The potential playback optimization is documented and deferred.

No conversion pipeline will be implemented now. The deployed native-format recording path remains the selected implementation.

## References

- [Amazon Transcribe input formats](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html)
- [WebKit WebM/Opus support](https://webkit.org/blog/16574/webkit-features-in-safari-18-4/)
- [MDN audio-codec guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Audio_codecs)
