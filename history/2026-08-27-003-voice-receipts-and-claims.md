# History 003 — Voice receipts, claimability, and revocation

**Date:** 2026-08-27  
**Status:** Proposed  
**Specification:** [0.0.0-alpha.1](../SPECIFICATION.md); no specification change made  
**Supersedes:** None  
**Related:** [Bootstrap voice solicitation history](./2026-08-27-001-bootstrap-voice-specification.md)

## Context

The operator signaled that Pledge may not be able to provide a reliable user-operated deletion function for submitted voices. The operator can, however, envision issuing a receipt for every submitted voice.

The proposed receipt would contain a `secUUID` capable of making the voice claimable and revocable.

This discussion concerns possible future behavior. It does not establish that deletion, claiming, revocation, receipts, or credential recovery currently exist.

## Direction

One element is genuinely in the operator's direction:

- A submitted voice should be capable of being claimed using its receipt.

The following are suggestions under consideration rather than accepted system behavior:

- provide a receipt for each submitted voice;
- use a `secUUID` as evidence of control;
- allow the holder to revoke future use;
- distinguish a public voice reference from a secret control credential;
- issue a second receipt when a revocation request is processed;
- distinguish cessation of use from physical deletion;
- describe retention and purge behavior precisely.

The operator specifically instructed: “Do not lock these as behaviors or advertise them as this will be false signaling.”

## Decisions

No implementation decisions were made.

Claimability is a design direction the operator has in mind. Its exact authentication rule, lifecycle, user interface, and effect remain undefined.

No public promise should be made from this entry.

## Corrections

The assistant previously phrased several suggestions as if they formed a settled contract, including proposed field separation, revocation consequences, eventual purge behavior, receipt contents, and recommended disclosure language.

That degree of certainty was incorrect. These items are proposals only. They must not be represented in documentation, interface copy, policy, or implementation descriptions as available or promised behavior unless the operator later accepts them and the repository records that acceptance.

## Open questions

- Is `secUUID` itself the control credential, a public reference, or one component of a larger receipt?
- What evidence is sufficient to claim a voice?
- What does claiming permit?
- What exactly does revocation stop?
- Is revocation immediate, asynchronous, or best-effort?
- Does revocation affect only future selection, or also retained audio, transcripts, derivatives, backups, and audit records?
- Is there a separate public `voice_id`?
- Can a lost receipt be recovered?
- What retention or deletion behavior can Pledge truthfully promise?
- Which of these capabilities belong in the first implementation?

## Result

The suggestions are preserved for later consideration without changing the current specification or advertising them as system behavior.

Future contributors and AI agents should treat every item in this entry as unresolved except for the operator's stated interest in making a voice claimable through a receipt.

## References

- [Current specification](../SPECIFICATION.md)
- [Project-history convention](./README.md)
- [Bootstrap voice solicitation history](./2026-08-27-001-bootstrap-voice-specification.md)
