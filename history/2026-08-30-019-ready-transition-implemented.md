# History 019 — Ready transition implemented

**Date:** 2026-08-30
**Status:** Implemented
**Specification:** N/A
**Supersedes:** None
**Related:** [History 018 — Catalog-driven ready state](./2026-08-30-018-catalog-driven-ready-state.md); [source commit](https://github.com/ourlovelysystem/lovely-system-pledge/commit/c3db61096b34afd9752ec1b681e7004cc502a11a)

## Context

History 018 accepted the rule that a successful usable recording moves Pledge from `voiceless` to `ready`.

## Direction

The accepted direction controls: after the catalog eligibility update, Pledge checks `run_mode` and updates it to `ready` when needed.

## Decisions

- The transition belongs in the transcription-completion Lambda immediately after final `usable` eligibility is written.
- The state write is conditional and idempotent: an already-`ready` state is a no-op.
- Borrowing status is not changed.

## Corrections

The first deployed test failed at the state write because the Lambda role could read but not update `lovely-system-pledge-state`.

The missing permission was added narrowly: `dynamodb:UpdateItem` on that state table only. The test was then rerun.

## Open questions

- Implement the catalog-deletion trigger that moves Pledge from `ready` to `voiceless` when the last eligible recording is deleted.
- Define which lifecycle actions physically delete catalog records.

## Result

Lambda version `3` was deployed. The completed receipt `1c37a153-2f6c-44fc-93f8-bec76e2e01e9` was rerun successfully with no function error.

The resulting state-table record was observed as:

```json
{
  "parameter_name": "run_mode",
  "parameter_value": "ready"
}
```

Pledge is now ready.

## References

- [Pledge history convention](./README.md)
- [Catalog-driven ready state](./2026-08-30-018-catalog-driven-ready-state.md)
