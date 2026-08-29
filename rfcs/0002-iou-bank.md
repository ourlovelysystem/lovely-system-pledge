# RFC 0002 — IOU Bank

**Status:** Proposed  
**Date:** 2026-08-29  
**System:** Our Lovely System — Pledge  
**Authors:** Will Daly; Codex as recorder and drafting assistant  
**Related:** [RFC 0001 — Capital Disposition Voting Test](./0001-capital-disposition-voting-test.md)  
**Supersedes:** Nothing

## Summary

This RFC proposes the **IOU Bank** as a test capital generator for Our Lovely System — Pledge.

A writer creates and submits a written artifact in this form:

> **IOU 5**

The writer chooses the amount and chooses the manner of self-attribution. The template contains a name field specifically marked **optional**.

Submission places the IOU note into a market where other users may inspect it, acknowledge it with a **Yeah, okay** signal, accept responsibility for honoring it, and supply its stated capital. The user who honors a note receives credit for honoring it.

The note's face value is proposed by its writer. Collective human judgment determines which notes receive acknowledgment, which notes are accepted, and which notes are ultimately honored.

## Governing claim

> **An IOU note has the value its writer proposes, the credibility people assign to it, and the capital value someone ultimately chooses to honor.**

## Motivation

The IOU Bank separates four acts that ordinary fundraising systems often collapse:

1. a person writes a proposed value into existence;
2. other people judge whether the note appears worthy of being honored;
3. a person voluntarily accepts responsibility for honoring it; and
4. a person converts the proposed value into actual capital.

The writer creates the marketable item. The market does not have to believe the writer.

An IOU for 1,000,000 attributed to the **Master of Disaster** may remain visible as an offer while collective human judgment answers:

> **Yeah, okay. Let's not honor that one.**

The raw offer remains evidence. It does not become accepted or paid capital merely because the writer selected a large number.

## The IOU note

An IOU note is a written, marketable item within Pledge. It is not automatically an assigned duty and is not indiscriminately distributed to another user.

The writer chooses:

- face value;
- written content;
- presentation;
- whether to provide a name;
- manner of self-attribution; and
- any stated purpose included in the note.

The writer does not control:

- acknowledgment;
- credibility;
- acceptance;
- priority in the market;
- whether the note is honored; or
- who receives credit for honoring it.

The note must preserve the submitted artifact rather than reducing the contribution to an amount and database row.

## Template

The minimum written template is:

```text
IOU [amount]

Name (optional): ____________________
```

The word **optional** must be visible. An empty name field must not be represented as a failed identity submission.

The implementation may support additional note content or presentation without silently making attribution mandatory.

## Attribution

The writer chooses the note's manner of self-attribution.

The accepter independently chooses how to act when accepting and honoring a note:

- anonymously;
- with self-identification; or
- as a system-knowable user.

Writer attribution and accepter attribution are independent. An anonymous note may be honored by a system-knowable user. A named note may be honored anonymously.

The system must distinguish no attribution, self-attribution, and system-knowable attribution. It must not silently promote one into another.

## Market actions and states

The minimum note states are:

| State | Meaning |
|---|---|
| `offered` | A writer submitted the IOU artifact and proposed its face value |
| `acknowledged` | One or more users supplied a “Yeah, okay” signal |
| `accepted` | A user voluntarily accepted responsibility for honoring the note |
| `honored` | The accepted note's stated capital was supplied |
| `credited` | The system credited the completed contribution |

The implementation may preserve acknowledgments as events rather than collapsing them into one state. A note may receive zero, one, or many **Yeah, okay** signals.

### Yeah, okay

**Yeah, okay** means:

> This note appears worthy of being honored.

It does not mean:

> I accept responsibility for honoring this note.

Acknowledgment and acceptance must remain separate acts.

### Acceptance

Acceptance means that a user has deliberately chosen the note and accepted responsibility for attempting to honor it.

The IOU Bank must not assign an unselected note to a user merely because the user is eligible to accept one.

The accepter must be able to inspect available notes before choosing. The market may expose amount, artifact, attribution posture, acknowledgment evidence, and other deliberately inspectable metadata.

Only one active acceptance may control a note at a time unless a later RFC deliberately defines shared acceptance.

An acceptance may require a release or expiry mechanism so that an abandoned acceptance does not imprison the note indefinitely. The exact rule remains open.

### Honoring

Honoring occurs when the accepted note's stated capital is actually supplied through the applicable payment or capital-transfer mechanism.

Acceptance is not payment. Intention is not capital. The system must not describe an accepted but unpaid note as honored.

### Credit

Contribution credit belongs to the user who completes the act being credited.

The user who honors the note may receive credit for honoring it. The writer may separately receive credit for creating a note if Pledge later defines such credit. Writing, acknowledging, accepting, and honoring must not be collapsed into one undifferentiated contribution.

This RFC does not define reputation points, monetary ownership, repayment rights, or exchange value for contribution credit.

## Balances

The IOU Bank should expose distinct cumulative balances:

| Balance | Meaning |
|---|---|
| Offered balance | Sum of face values proposed by submitted notes |
| Acknowledged balance | Face value of notes receiving the required acknowledgment signal, if a threshold is defined |
| Accepted balance | Face value of notes under active acceptance |
| Honored balance | Capital actually supplied by honoring notes |

These balances must not be collapsed.

A million-unit note from the Master of Disaster may increase the offered balance. It does not increase the accepted or honored balance unless people choose to accept and honor it.

The difference among balances is evidence of collective human judgment.

## Shopping the notes

The IOU Bank should permit eligible accepters to browse or shop the available notes before accepting one.

The shopping surface exists to support choice, not to produce an automated ranking that substitutes machine judgment for human judgment. Search, ordering, filtering, or recommendation rules must be inspectable if introduced.

The surface should make clear:

- what the writer proposed;
- how the writer chose to attribute the note;
- which signals the note has received;
- whether it is available for acceptance;
- whether someone has already accepted it; and
- whether it has been honored.

## Relationship to the contribution catalog

The written IOU is a user-contributed artifact and should be represented in the Pledge contribution catalog.

- the catalog describes the contribution;
- object storage contains the submitted artifact;
- the receipt identifies the contributed artifact under Pledge's receipt rules; and
- the IOU Bank records the note's market and fulfillment state.

This RFC does not decide whether the IOU Bank is implemented as a separate table, a projection, a namespace within a broader catalog, or another storage structure.

## Relationship to the Capital Disposition Voting Test

Honored IOU notes may provide capital for [RFC 0001](./0001-capital-disposition-voting-test.md), but the two proposals remain distinct:

- RFC 0002 concerns how proposed value becomes contributed capital;
- RFC 0001 concerns how a vote governs the disposition of capital already received.

Using IOU Bank capital in the voting test requires an explicit declaration before users write, accept, or honor eligible notes.

The declaration must identify which actors receive voting standing: writers, accepters, users who honor notes, receipt bearers, or some combination. This RFC does not silently answer that question.

## Collective human judgment

Pledge does not certify a note's worth merely because the note exists.

Collective judgment appears through:

- attention;
- acknowledgment;
- refusal;
- acceptance;
- release;
- completion; and
- the time between these events.

Unaccepted notes are not necessarily errors. They are evidence of what people declined to carry.

Absence of acknowledgment or acceptance must be recorded without inventing a reason. “No user accepted this note” is supportable. “The community rejected this writer” is not established merely by silence.

## Abuse and absurdity

The market must tolerate offers that appear implausible, ridiculous, unattractive, or hostile without converting their face value into actual capital.

The primary restraint is deliberate human acceptance rather than automatic validation of the writer's proposed amount.

The system should preserve enough evidence to distinguish:

- a large offer;
- a widely acknowledged offer;
- an accepted obligation;
- a completed contribution; and
- attempted manipulation of market signals.

This RFC does not require Pledge to honor every note, guarantee acceptance, or suppress absurd notes merely because they are absurd.

## Functional requirements

An initial implementation must support:

1. creation of a written IOU artifact;
2. a writer-selected amount;
3. a visibly optional name field;
4. submission and receipting of the artifact;
5. listing of available notes;
6. inspection of deliberately visible note information;
7. a distinct **Yeah, okay** action;
8. voluntary acceptance of a selected note;
9. prevention of simultaneous exclusive acceptance;
10. recording of payment or other completion evidence;
11. credit for the user who honors the note;
12. distinct offered, acknowledged, accepted, honored, and credited evidence; and
13. independent attribution choices for writer and accepter.

## Non-goals

This RFC does not:

- require the writer to provide a name;
- guarantee that a note will be acknowledged, accepted, or honored;
- treat face value as received capital;
- establish one-person-one-vote;
- define general reputation;
- create repayment rights;
- define the note as legal tender, a security, or a legally negotiable instrument;
- require automated valuation;
- authorize collection or disbursement of money; or
- implement RFC 0001.

## Acceptance criteria

The RFC may be considered successfully implemented when an independent reader can verify that:

1. a writer created an IOU artifact with a chosen amount and optional attribution;
2. the artifact entered the available-note market;
3. users could inspect it before acting;
4. acknowledgment remained separate from acceptance;
5. an accepter deliberately selected the note;
6. no competing exclusive acceptance silently displaced that accepter;
7. honoring produced actual capital or valid completion evidence;
8. the honoring user received accurately described credit; and
9. offered, accepted, and honored balances remained distinguishable.

## Open questions

- What amounts and units may writers place on notes?
- Is **Yeah, okay** binary, cumulative, retractable, or threshold-bearing?
- Who may browse, acknowledge, accept, or honor notes?
- How long may an acceptance remain incomplete?
- How may an accepter release a note?
- What happens when payment fails after acceptance?
- What evidence proves that a note was honored?
- Does a writer receive contribution credit for creating a note?
- Does the user who honors a note receive a contribution receipt distinct from the artifact receipt?
- How are suspicious acknowledgment patterns exposed?
- Which IOU Bank metadata may system-knowable users inspect?
- What surrounding legal and payment classifications must be resolved before actual capital moves?

## Disposition

This RFC is proposed. It records the IOU Bank concept and does not authorize implementation, collection of money, or treatment of any offered amount as capital received.
