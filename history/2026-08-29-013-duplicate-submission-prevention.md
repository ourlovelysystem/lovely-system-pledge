# History 013 — Duplicate recording submission prevented

**Date:** 2026-08-29
**Status:** Implemented
**Specification:** N/A
**Supersedes:** None
**Related:** [Duplicate-submission fix](https://github.com/ourlovelysystem/lovely-system-pledge/commit/804cd94760d109cbe1e3f80f2f9c92d3f681cd38), [version 0.1.1](https://github.com/ourlovelysystem/lovely-system-pledge/commit/43c1e6d65b9480b5ced5f325dc6240eb382102da)

## Context

Testing of the Pledge recording control showed that the same in-memory audio recording could be submitted more than once. Each accepted request created another electronic valuable even though the user had not made a new recording.

The operator directed:

> Fix the duplication submission problem first otherwise I will forget it.

## Direction

A successful submission must consume the control's permission to submit the current recording. Playback may remain available, but another submission requires another recording.

## Decisions

- After a successful submission, the control disables **Submit** for the submitted recording.
- The user may continue to play the submitted recording.
- Starting and completing a new recording makes that new recording eligible for one submission.
- The recording-control descriptor was advanced from `0.1.0` to `0.1.1` so the deployed behavior is inspectable.

## Corrections

An earlier assistant statement inferred that `pledge.ourlovelysystem.org` lacked an automatic GitHub deployment pipeline. That inference was unsupported and wrong. The site has an automatic GitHub deployment pipeline, and it deployed this fix.

## Open questions

This control-level prevention does not establish request-level idempotency in the API. Whether the intake API should independently reject retried or replayed submissions remains open.

## Result

The fix was committed, deployed through the existing automatic GitHub deployment pipeline, and exposed by the live page as `bootstrap voice · 0.1.1`.

The operator tested the deployed fix and reported:

> Fix tested. Looks good.

## References

- [Commit 804cd94 — Prevent duplicate recording submission](https://github.com/ourlovelysystem/lovely-system-pledge/commit/804cd94760d109cbe1e3f80f2f9c92d3f681cd38)
- [Commit 43c1e6d — Bump recording control to 0.1.1](https://github.com/ourlovelysystem/lovely-system-pledge/commit/43c1e6d65b9480b5ced5f325dc6240eb382102da)
- [Pledge recording control](https://pledge.ourlovelysystem.org/recording-control.html)
