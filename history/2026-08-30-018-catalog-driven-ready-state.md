# History 018 — Catalog-driven ready state

**Date:** 2026-08-30
**Status:** Accepted direction
**Specification:** N/A
**Supersedes:** None
**Related:** [History 017 — Bedrock functional-match evaluation pending](./2026-08-29-017-bedrock-functional-match-pending.md); [semantic-transition commit](https://github.com/ourlovelysystem/lovely-system-pledge/commit/23fdd9417a0fd58362915ce0498160679537ca30); [ready-page commit](https://github.com/ourlovelysystem/lovely-system-pledge/commit/bf3c65541a643f140e8f89638fb909900784e0a4)

## Context

The transcription-completion Lambda now evaluates completed voice tracks with Bedrock, assigns a final content decision, and sets `catalog_eligible`.

The tested receipt `1c37a153-2f6c-44fc-93f8-bec76e2e01e9` completed with:

- `semantic_match_score = 1.0`;
- `content_decision = usable`; and
- `catalog_eligible = true`.

At that point Pledge had an eligible borrowed voice, but the global `run_mode` parameter still read `voiceless`.

## Direction

The operator directed:

> When the semantic evaluation completed, the catalog gets updates and the eligibility flags get set. That is the right time to set the system ready state should be checked and updated if it is not already ready.

The operator then selected the reciprocal mechanism:

> Using a deletion trigger in the catalog.

And rejected sulk-mode behavior for this implementation:

> Forget sulk. Just set it to voiceless.

## Decisions

1. `ready` is the run-mode value once Pledge has an eligible borrowed voice.
2. Immediately after a successful semantic evaluation sets `catalog_eligible = true`, the completion flow must read `run_mode` and set it to `ready` when it is not already `ready`.
3. A DynamoDB Streams trigger on catalog `REMOVE` events must recheck whether any eligible recording remains.
4. If no eligible recording remains after a catalog deletion, the trigger must set `run_mode` to `voiceless`.
5. The deletion handler must be idempotent because DynamoDB Streams can deliver the same event more than once.
6. This transition does not change borrowing status.

## Corrections

The earlier proposal to derive run mode on every State API request by scanning the catalog was rejected as unnecessary complexity for the current system.

The earlier sulk-mode proposal was rejected for this implementation. The only no-eligible-voice state is `voiceless`.

## Open questions

- Which catalog lifecycle actions physically delete a record: expiration, revocation, withdrawal, purge, or some combination?
- Does a future large catalog require an eligibility index for the deletion handler's remaining-eligible check?
- What selected challenge-track data does the future nonblank `ready` page require?

## Result

The frontend recognizes `run_mode: "ready"` and displays only `Ready.`

The automatic completion-to-`ready` transition and catalog-deletion trigger are accepted direction, not yet implemented.

## References

- [Pledge specification — state derivation](../SPECIFICATION.md)
- [Pledge history convention](./README.md)
