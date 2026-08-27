# History 001 — Bootstrap voice solicitation specification

**Date:** 2026-08-27  
**Status:** Accepted direction  
**Specification:** [0.0.0-alpha.1](../SPECIFICATION.md)  
**Supersedes:** None  
**Related:** [Specification commit](https://github.com/ourlovelysystem/lovely-system-pledge/commit/722aff20f2698cb5de1288ef10d43c948237da2b); [hostile review request](https://github.com/ourlovelysystem/lovely-system-nasty-oracle/issues/1); [Computahhh Event 105](https://github.com/ourlovelysystem/lovely-system-computahhh/blob/main/events/2026-08-27-105.md); [Computahhh Event 106](https://github.com/ourlovelysystem/lovely-system-computahhh/blob/main/events/2026-08-27-106.md)

## Context

Pledge is intended to grow from a public outer edge toward progressively more durable identity, authority, and accountability. The first build was deliberately narrowed to one reusable utility: soliciting a spoken answer to a known textual question and processing the audio without making the contributor wait.

At initial deployment, Pledge has no audio catalogue and therefore no voice with which to challenge a visitor.

## Direction

The operator established the bootstrap sequence:

1. Pledge states in text that it has no voice and asks whether it may borrow the visitor's.
2. An agreeing visitor records an audio contribution that performs the function of asking, “Who are you?”
3. Pledge validates only the recording envelope synchronously. A valid audio file lets the visitor proceed immediately to a “Come Back Soon” page.
4. Transcription and semantic evaluation happen asynchronously.
5. An accepted, unexpired contribution enters the catalogue from which Pledge can present future auditory challenges.
6. If the catalogue later has no eligible voices, Pledge enters a distinct “sulk mode” and asks to borrow a voice again.

The exact phrase is not a rigid password. Semantically suitable variations and humor are allowed. Examples explicitly considered acceptable include “Who are you, dickwad?”, “Who you are?”, “Who you?”, and “Sing me your name.”

## Decisions

- Audio-envelope validation is synchronous; content validation is asynchronous.
- The contributor does not wait for transcription or semantic classification.
- Transcription confidence and semantic match confidence are separate values.
- Acceptance should be based on whether the track adequately performs the known question's function, not exact textual equality.
- Borrowing is time-bound. Minute-scale durations are needed during testing; later policy will likely use days.
- Audio and derived transcriptions must be purged when their authorized retention expires.
- Eligible tracks are ordinarily selected randomly.
- A configurable minimum-use target may temporarily prioritize a track so a contributor is likely to hear their own contribution on return.
- Expiration overrides the minimum-use target. Minimum use never extends consent.
- “Bootstrap mode” means Pledge has never had an eligible voice. “Sulk mode” means it previously had a voice but currently has none.

These decisions are captured in specification version 0.0.0-alpha.1.

## Corrections

An earlier interpretation made the workflow broader and risked implying that Pledge would wait for transcription before admitting the visitor. The operator corrected this: Pledge “validates the envelope only not the contents before allowing the user to pass through.” The specification reflects that correction.

The voice contribution is not merely a spoken identity answer. In the bootstrap context, the visitor lends Pledge a reusable auditory challenge whose function is “Who are you?”

## Open questions

The specification deliberately leaves implementation parameters unresolved, including:

- exact envelope constraints and duration limits;
- the acceptance threshold and the treatment of borderline semantic matches;
- the testing and production retention choices;
- the minimum-use target and selection weighting;
- the mechanism for purge verification;
- abuse handling and catalogue moderation;
- the eventual cloud architecture.

These questions must not be treated as settled requirements without a later history entry or specification revision.

## Result

The repository received the recoverable specification `0.0.0-alpha.1`. A hostile review was requested from the Oracle of Snake Mountain, with explicit invitation to attack consent, retention, asynchronous validation, selection fairness, state transitions, security, and recoverability.

This entry establishes the initial project-history record and demonstrates the convention defined in `history/README.md`.

## References

- [Current specification](../SPECIFICATION.md)
- [Specification commit](https://github.com/ourlovelysystem/lovely-system-pledge/commit/722aff20f2698cb5de1288ef10d43c948237da2b)
- [Oracle hostile review request](https://github.com/ourlovelysystem/lovely-system-nasty-oracle/issues/1)
- [Computahhh Event 105](https://github.com/ourlovelysystem/lovely-system-computahhh/blob/main/events/2026-08-27-105.md)
- [Computahhh Event 106](https://github.com/ourlovelysystem/lovely-system-computahhh/blob/main/events/2026-08-27-106.md)
