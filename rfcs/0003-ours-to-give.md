# RFC 0003 — Ours to Give

**Status:** Proposed; naming and governing expression accepted  
**Date:** 2026-08-29  
**System:** Our Lovely System — Pledge  
**Authors:** Will Daly; Codex as recorder and drafting assistant  
**Related:** [RFC 0001 — Capital Disposition Voting Test](./0001-capital-disposition-voting-test.md)  
**Supersedes:** [RFC 0002 — IOU Bank](./0002-iou-bank.md)

## Summary

This RFC proposes **Ours to Give**, abbreviated **OTG**, as a test capital generator for Our Lovely System — Pledge.

A writer creates and submits an **Ours to Give pledge** carrying a writer-selected amount and a writer-selected manner of attribution. The name field is specifically marked **optional**.

The pledge carries this governing expression:

> **This was mine to give.  
> Now it's ours to give.**

Other users may inspect OTG pledges, acknowledge one with a **Yeah, okay**, accept one, honor it, and receive accurately described credit for the act they complete.

The written pledge is given when submitted. Its stated capital becomes ours to give when the pledge is honored.

## Why Ours to Give

RFC 0002 used an IOU frame. The operator identified two defects:

1. **I Owe Our Lovely System** separates the writer from the system by placing the writer outside it as debtor and the system outside the writer as creditor.
2. “I owe” frames the interaction as debt, while the intended expression is an offering: **“This is my body which is given to you.”**

The operator then proposed:

> **This was mine to give. Now it's ours to give.**

This correction changes the moral architecture without discarding the useful market mechanics.

The writer is not a debtor to an external institution. The writer gives a pledge into a collective that the writer may help constitute. The accepter does not collect a debt from the writer. The accepter receives a pledge and chooses whether to carry it into consequence.

## Governing claims

> **This was mine to give. Now it's ours to give.**

> **The writer gives form. The accepter gives consequence. Honoring makes the stated capital ours to give.**

> **The capital does not become ours to keep. It becomes ours to give.**

## The OTG pledge

An OTG pledge is a written, marketable contribution artifact within Pledge.

The writer chooses:

- proposed amount;
- written content;
- presentation;
- whether to provide a name;
- manner of self-attribution; and
- any stated purpose.

The writer does not control:

- acknowledgment;
- collective credibility judgments;
- acceptance;
- priority in the market;
- whether the pledge is honored;
- where honored capital is ultimately given; or
- who receives credit for honoring it.

The submitted artifact remains part of the contribution record. It must not be reduced to an amount and database row.

## Template

The minimum OTG artifact is:

```text
OURS TO GIVE

Amount: __________

This was mine to give.
Now it's ours to give.

Name — optional: ____________________
```

The word **optional** must be visible. An empty name field is an attribution choice, not an identity failure.

## What is given at each stage

Ours to Give preserves an evidentiary distinction between artifact and capital.

### Submission

Submitting gives the written OTG pledge to the collective. The writer contributes:

- the artifact;
- its proposed amount;
- its language and presentation;
- its chosen attribution posture; and
- the opportunity for another person to carry it forward.

The proposed amount is not yet capital received.

### Acceptance

Acceptance means a user deliberately selects the pledge and accepts responsibility for attempting to honor it.

The accepter receives the opportunity and chooses to carry it. Acceptance does not create payment and does not transform the writer into a debtor.

### Honoring

Honoring occurs when the accepter supplies the stated capital through the applicable completion mechanism.

At that point, the value moves from proposed amount to contributed capital:

> **Now it's ours to give.**

## Attribution

The writer chooses the pledge's manner of attribution.

The accepter independently chooses to act:

- anonymously;
- with self-identification; or
- as a system-knowable user.

Writer attribution and accepter attribution are independent. An unattributed OTG may be honored by a system-knowable user. An attributed OTG may be honored anonymously.

Pledge must distinguish no attribution, self-attribution, and system-knowable attribution. It must not silently promote one into another.

## Market actions and states

The minimum OTG states are:

| State | Meaning |
|---|---|
| `offered` | A writer submitted the OTG artifact and proposed an amount |
| `acknowledged` | One or more users supplied a “Yeah, okay” signal |
| `accepted` | A user voluntarily accepted responsibility for honoring the pledge |
| `honored` | The pledge's stated capital was supplied |
| `credited` | Pledge credited the completed contribution accurately |

Acknowledgments may remain individual events rather than becoming one irreversible state.

### Yeah, okay

**Yeah, okay** means:

> This OTG appears worthy of being honored.

It does not mean:

> I accept responsibility for honoring this OTG.

Acknowledgment and acceptance remain separate acts.

### Shopping OTGs

Eligible users may browse or shop available OTG pledges before selecting one.

The market may expose:

- proposed amount;
- submitted artifact;
- writer-selected attribution posture;
- acknowledgment evidence;
- availability;
- acceptance status; and
- honoring status.

Search, ordering, filtering, and recommendation rules must be inspectable if introduced. Machine ordering must not be represented as collective human judgment.

### Acceptance integrity

Only one active acceptance may control an OTG at a time unless a later RFC defines shared acceptance.

Acceptance should eventually support release or expiry so an abandoned acceptance does not imprison the pledge indefinitely. The exact behavior remains open.

## Collective human judgment

Pledge does not certify an OTG's worth merely because it exists.

Collective judgment appears through:

- attention;
- acknowledgment;
- refusal;
- acceptance;
- release;
- completion; and
- time between events.

An OTG proposing 1,000,000 from the **Master of Disaster** may remain visible while people respond:

> **Yeah, okay. Let's not honor that one.**

The offer remains evidence. It does not become accepted or honored capital merely because the writer chose a large amount.

Silence must not be overinterpreted. “No user accepted this OTG” is supportable. “The community rejected this writer” is not established by silence alone.

## Balances

Ours to Give should expose distinct cumulative balances:

| Balance | Meaning |
|---|---|
| Offered balance | Sum of amounts proposed by submitted OTGs |
| Acknowledged balance | Proposed value of OTGs meeting any declared acknowledgment threshold |
| Accepted balance | Proposed value under active acceptance |
| Honored balance | Capital actually supplied by honoring OTGs |

These balances must not be collapsed.

The difference among them is evidence of collective human judgment and completed action.

## Credit

Credit must describe the completed act.

- The writer may receive credit for creating an OTG if Pledge later defines that credit.
- A user may receive credit for acknowledging an OTG if Pledge later defines that credit.
- The accepter may receive credit for accepting responsibility.
- The user who honors the OTG may receive credit for supplying its capital.

These acts must not be collapsed into one undifferentiated contribution.

This RFC does not define reputation points, monetary ownership, repayment rights, or exchange value for contribution credit.

## Contribution custody

The OTG artifact is a contribution to Pledge:

- the contribution catalog describes it;
- object storage holds it;
- its unique object key serves as its receipt under Pledge's receipt rules; and
- the OTG market records acknowledgment, acceptance, honoring, and credit events.

This RFC does not select a permanent table, projection, or namespace for the OTG market.

## Relationship to the Capital Disposition Voting Test

Honored OTGs may capitalize [RFC 0001](./0001-capital-disposition-voting-test.md).

The proposals remain distinct:

- RFC 0003 governs how an offered artifact becomes honored capital;
- RFC 0001 governs how voters decide where received capital will be given.

Using honored OTG capital in the voting test requires advance disclosure. The vote must state whether standing belongs to writers, accepters, users who honor OTGs, receipt bearers, or some combination.

The relationship completes the expression:

> **This was mine to give.  
> Now it's ours to give.  
> The vote determines where we give it.**

## Functional requirements

An initial implementation must support:

1. creation of a written OTG artifact;
2. a writer-selected amount;
3. a visibly optional name field;
4. writer-selected attribution posture;
5. submission and receipting of the artifact;
6. listing and inspection of available OTGs;
7. a distinct **Yeah, okay** action;
8. voluntary acceptance of a selected OTG;
9. prevention of competing exclusive acceptance;
10. recording of honoring evidence;
11. accurate credit for completed acts;
12. distinct offered, acknowledged, accepted, honored, and credited evidence; and
13. distinct offered, acknowledged, accepted, and honored balances.

## Non-goals

This RFC does not:

- require a writer's name;
- make the writer a debtor to Pledge;
- guarantee that an OTG will be acknowledged, accepted, or honored;
- treat proposed value as capital received;
- establish general reputation or voting power;
- create repayment rights;
- define the OTG as legal tender, a security, or a legally negotiable instrument;
- require automated valuation;
- authorize collection or disbursement of money; or
- implement RFC 0001.

## Acceptance criteria

The RFC may be considered successfully implemented when an independent reader can verify that:

1. a writer created an OTG with a chosen amount and optional attribution;
2. submission preserved the artifact without treating its face value as received capital;
3. users could inspect the OTG before acting;
4. acknowledgment remained separate from acceptance;
5. an accepter deliberately selected the OTG;
6. acceptance did not convert the writer into a debtor;
7. honoring produced actual capital or valid completion evidence;
8. credit described the completed act accurately; and
9. offered, accepted, and honored balances remained distinguishable.

## Open questions

- What amounts and units may writers place on OTGs?
- Is **Yeah, okay** cumulative, retractable, or threshold-bearing?
- Who may browse, acknowledge, accept, or honor OTGs?
- How long may an acceptance remain incomplete?
- How may an accepter release an OTG?
- What happens when payment fails after acceptance?
- What evidence proves that an OTG was honored?
- Which acts produce contribution receipts or credit?
- How are suspicious acknowledgment patterns exposed?
- Which OTG metadata may system-knowable users inspect?
- Which OTG relationships produce standing in a capital-disposition vote?
- What surrounding legal and payment classifications must be resolved before capital moves?

## Disposition

The **Ours to Give** name and governing expression are accepted direction. The feature described by this RFC remains proposed. This RFC supersedes RFC 0002 and does not authorize implementation, collection of money, or treatment of proposed value as capital received.
