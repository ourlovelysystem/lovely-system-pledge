# History 021 — Receipt claim and expiration policy

**Date:** 2026-08-31  
**Status:** Accepted direction  
**Specification:** [0.0.0-alpha.2](../SPECIFICATION.md)  
**Supersedes:** [History 003 — Voice receipts, claimability, and revocation](./2026-08-27-003-voice-receipts-and-claims.md), for claim and expiration policy  
**Related:** [Contribution catalog and deferred deletion function](../CONTRIBUTION_CATALOG.md)

## Context

The earlier receipt record intentionally left claim, retention, and deletion unresolved. Subsequent discussion established a narrower policy for anonymous borrowed electronic valuables: the system must be severe about expiration, while allowing a receipt holder to become known and take responsibility before expiration.

The operator's stated direction included:

> "It can be claimed by its receipt holder if that person creates a durable authenticated user account in Our Lovely System."

and:

> "Before expiration. Aggressive enforcement on borrowed items. This is how Our Lovely System will earn trust."

The operator further required that a claim not disappear into private custody: the claimant becomes known in the act, and the public record tells both the anonymous lending story and the claim story.

## Direction

An anonymous borrowed electronic valuable is claimable only before its expiration. A successful claim requires both the item receipt and a durable authenticated Our Lovely System account.

An unclaimed borrowed item becomes ineligible at expiration and is aggressively removed. Its audio, transcript, and derivatives must be purged. A later claim cannot revive the removed content.

A timely claim moves the item from anonymous borrowed custody to known-account custody. The claim is public: Pledge records who claimed which item and when, without publishing the receipt.

## Decisions

- Receipt possession is required but does not prove that the claimant is the speaker or original lender.
- Pledge makes that limitation visible rather than silently resolving it in the claimant's favor.
- Claiming makes a person known and associates that known account with the claimed item.
- Where the lending record includes a displayable asserted identity, Pledge may show it with the known claimant so the public can see the difference between lending and claiming.
- The initial anonymous borrowing term is not extended by minimum-use targets or delayed deletion processing.
- The standard expiration outcome for an unclaimed item is removal, not dormant retention.
- The existing receipt-claim and removal mechanisms are not implemented by this policy update. The public policy text says so plainly.

## Corrections

The previous public lending page said that a receipt gave the visitor a way to request deletion. That described an unimplemented feature as available behavior. It has been replaced with the accepted policy and an explicit statement that the claim path and removal worker are not yet available controls.

This record does not turn a receipt into proof of personal identity, ownership, authorship, or consent beyond the original borrowing record. It establishes a visible, accountable claim mechanism for when a receipt holder chooses to become known.

## Open questions

- What durable retention and withdrawal rules govern an item after a timely claim?
- What exact account-verification standard is needed before public identity is shown?
- Which original lending attributes are displayable without exposing a lender who remained anonymous?
- What implementation proves that an expired unclaimed item and every derivative were removed?
- How should failed or disputed claims be represented without concealing the attempt?

## Result

Pledge now has an accepted policy: anonymous borrowing is temporary and expires hard; a receipt holder who wishes to preserve an item must do so before expiration by becoming a known, durable participant. The resulting claim is publicly accountable. Implementation remains a later, separately testable slice.

## References

- [Specification 0.0.0-alpha.2](../SPECIFICATION.md)
- [Prior proposed claim record](./2026-08-27-003-voice-receipts-and-claims.md)
- [Contribution catalog requirements](../CONTRIBUTION_CATALOG.md)
