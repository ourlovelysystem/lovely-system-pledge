# History 008 — Capital disposition voting test RFC

**Date:** 2026-08-29
**Status:** Proposed
**Specification:** N/A
**Supersedes:** None
**Related:** [RFC 0001 — Capital Disposition Voting Test](../rfcs/0001-capital-disposition-voting-test.md)

## Context

The operator stated:

> I want to have system features which exist just to prove that voting works. Voting test:
>
> Raise capital. Provide a vote. Return to sender, give it to the CEO as a bonus, give it to the CEO's second favorite charity (CEO is CEO's first favorite charity).

The operator then directed:

> Write it up and post it in the spirit of an RFC.

## Direction

Pledge should explore a bounded feature that tests whether voting governs a valuable consequence. The feature raises capital, gives an eligible constituency a vote among three precommitted dispositions, executes the winning result, and publishes evidence of execution.

## Decisions

- The proposal is recorded as RFC 0001.
- The RFC remains proposed and does not authorize capital collection or implementation.
- The three ballot outcomes are preserved as directed: return to sender, CEO bonus, and the CEO's preidentified second-favorite charity.
- The CEO is identified as the CEO's first-favorite charity.
- Success requires execution and inspectable evidence, not merely a tally.
- Contributor receipts are proposed as evidence of standing for this contributor vote.
- Receipt secrets must not be exposed in the published ballot record.

## Corrections

None.

## Open questions

The RFC preserves unresolved questions concerning the capital amount, contribution units, voting power, quorum, thresholds, ties, return mechanism, charity identity, costs, inspection, exploitation, and independent verification.

## Result

RFC 0001 is prepared as a public proposal for the Capital Disposition Voting Test.

## References

- [RFC 0001 — Capital Disposition Voting Test](../rfcs/0001-capital-disposition-voting-test.md)
- [Pledge Project History convention](./README.md)
