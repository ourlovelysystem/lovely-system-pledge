# RFC 0001 — Capital Disposition Voting Test

**Status:** Proposed  
**Date:** 2026-08-29  
**System:** Our Lovely System — Pledge  
**Authors:** Will Daly; Codex as recorder and drafting assistant  
**Discussion:** Not yet assigned  
**Supersedes:** Nothing

## Summary

Our Lovely System — Pledge should contain features whose purpose is to prove that voting works.

This RFC proposes a deliberately small test in which Pledge raises a bounded pool of capital, gives an eligible constituency a vote over its disposition, executes the winning result, and publishes evidence that the capital went where the vote directed.

The ballot contains three outcomes:

1. **Return to sender.**
2. **Give it to the CEO as a bonus.**
3. **Give it to the CEO's second-favorite charity.**

The CEO is the CEO's first-favorite charity.

## Motivation

A voting interface can prove that software accepts and counts ballots. It does not prove that voting governs anything.

This test places something valuable under voter control. Its success criterion is not a displayed tally. Its success criterion is faithful disposition of the capital according to rules published before voting begins.

The test is intentionally exposed to divergent interests:

- return to sender favors contributors who want their capital back;
- a CEO bonus permits an openly self-interested disposition; and
- the charity option redirects the capital to an identified third party.

The humor in the charity option is part of the disclosure. It exposes the CEO's self-interest instead of disguising it beneath institutional language.

## Governing claim

> **Our Lovely System does not prove voting works by displaying a tally. It proves voting works by placing something valuable under voter control and obeying the result.**

## Goals

The test should demonstrate that Pledge can:

1. receive and account for a bounded pool of capital;
2. issue contribution receipts;
3. define an electorate before observing ballots;
4. accept votes supported by declared evidence of standing;
5. prevent a single credential from voting twice in the same election;
6. close and tally the vote under published rules;
7. determine a result without discretionary substitution;
8. execute the winning disposition; and
9. publish evidence connecting the vote to the disposition.

## Non-goals

This RFC does not attempt to establish:

- one universal electorate for Our Lovely System;
- one permanent rule for weighting contributors;
- proof of personhood from possession of a receipt;
- general-purpose elections;
- governance authority beyond this bounded capital pool;
- that voting produces a morally good result; or
- that a majority vote can erase legal duties or borrowing terms.

## Constituency

This is a **contributor vote**. Eligibility comes from a valid receipt issued for an eligible contribution to this capital pool.

A receipt establishes contributor standing for this test. It does not, by itself, establish identity, personhood, comprehension, loyalty, wisdom, or general sovereignty.

The initial test proposes:

> **One eligible receipt may cast one ballot.**

If one contributor may acquire multiple eligible receipts, that fact must be disclosed before capital is accepted. The implementation must not silently describe receipt-weighted voting as one-person-one-vote.

Because a receipt is also treated as a shared secret, the published ballot record must not expose the receipt. Pledge may derive a referendum-specific ballot identifier from the receipt in order to detect duplicate use without publishing the bearer credential.

## Capital pool

Before accepting capital, Pledge must publish:

- the opening and closing conditions for contributions;
- the minimum, target, and maximum pool size;
- any fixed or variable contribution amount;
- fees and other amounts excluded from the distributable pool;
- conditions under which the test is canceled;
- what cancellation does to contributed capital; and
- when contributor receipts become eligible to vote.

Capital accepted for the test must not be presented as available for ordinary operating use while its disposition remains subject to the ballot.

## Ballot

The ballot must present exactly these mutually exclusive choices:

### A. Return to sender

Return each contributor's applicable share through the disclosed return mechanism.

This choice tests reversibility and contributor sovereignty. Administrative inconvenience does not authorize Pledge to retain the capital.

### B. Give it to the CEO as a bonus

Transfer the distributable pool to the CEO through a legally and operationally valid bonus mechanism disclosed before voting begins.

This choice tests whether Pledge will execute an openly self-interested result without replacing it with a more respectable institutional preference.

### C. Give it to the CEO's second-favorite charity

Transfer the distributable pool to the charity identified before voting begins as the CEO's second-favorite charity.

The charity must be named and fixed before ballots are observed. The CEO may not discover a new second-favorite charity after the count.

For clarity:

> **The CEO is the CEO's first-favorite charity.**

## Vote descriptor

Before voting opens, Pledge must publish a versioned vote descriptor containing:

- the exact ballot question and choices;
- the capital pool governed by the vote;
- the eligible receipt population;
- the unit of voting power;
- opening and closing conditions;
- quorum, if any;
- winning threshold;
- treatment of abstention;
- tie handling;
- invalid-ballot handling;
- whether provisional results will be shown;
- the execution deadline;
- the evidence required to prove execution; and
- any predeclared condition that makes an outcome impossible to execute.

The descriptor must become immutable no later than the acceptance of the first ballot. A later correction requires a new version and an inspectable explanation. The electorate, weighting, and winning rule may not be selected after observing the result.

## State progression

The test should expose at least these states:

1. `proposed`
2. `capital_open`
3. `capital_closed`
4. `voting_open`
5. `voting_closed`
6. `tallied`
7. `execution_pending`
8. `executed`
9. `verified`

Failure states must remain visible. Examples include `capital_failed`, `vote_failed`, `execution_blocked`, and `verification_failed`.

The system must not label the test `verified` merely because the tally completed.

## Execution

The winning outcome is binding within the advertised scope of the test.

- If **Return to sender** wins, Pledge returns the applicable capital.
- If **CEO bonus** wins, Pledge pays the bonus.
- If **Second-favorite charity** wins, Pledge pays the preidentified charity.

Embarrassment, administrative inconvenience, dislike of the result, or a later preference by the CEO is not grounds for substitution.

All ballot options must be reviewed for operational and legal executability before capital is accepted. If surrounding law prevents a promised disposition, that conflict must be disclosed rather than hidden behind an apparent execution success.

## Evidence of execution

The public result should establish:

- the governing vote-descriptor version;
- the eligible receipt count;
- ballots accepted, rejected, and abstained;
- the final tally;
- the winning outcome;
- the distributable amount;
- fees or exclusions;
- when execution occurred;
- the destination or return mechanism appropriate to the winning choice; and
- evidence sufficient to connect the transfer to the result.

Evidence should protect receipt secrets, payment credentials, and unnecessarily identifying contributor information.

## Failure meaning

The test fails if Pledge:

- changes the electorate or counting rule after observing ballots;
- accepts duplicate ballots from the same voting credential in one election;
- declares a winner contrary to the published rule;
- substitutes a different disposition;
- retains capital after return to sender wins;
- redirects the CEO bonus because the result appears improper;
- changes the named charity after observing ballots;
- describes an unexecuted result as executed; or
- exposes contribution receipts as part of the voting record.

A surfaced failure is still useful evidence. It does not become success merely because it was surfaced.

## Security and abuse

This feature deliberately places a valuable under voter control. That creates incentives to accumulate, transfer, steal, automate, or misuse voting credentials.

The first test need not solve every future voting problem. It must truthfully disclose its credential model, reject duplicate use of the same credential within the election, protect receipt secrets, and preserve evidence of attempted exploitation.

Any containment action taken during an active incident must be recorded. Temporary containment must not silently rewrite the permanent voting rule.

## Privacy

Publication should expose the chain from capital to vote to disposition without unnecessarily exposing contributors.

Contributor names, payment details, receipt secrets, and borrowed electronic valuables are not made public merely because aggregate voting evidence is public.

## Alternatives considered

### Advisory poll

Rejected as insufficient for this test. It demonstrates preference collection without demonstrating that voters govern a consequence.

### Symbolic or valueless token

Rejected as insufficient for this test. It lowers the cost of failure by removing the thing the vote is supposed to govern.

### CEO discretion after the vote

Rejected. A discretionary result would test consultation, not voting.

## Acceptance criteria

The RFC may be considered successfully implemented when:

1. the vote descriptor was published before voting;
2. eligible receipt holders were able to cast ballots;
3. duplicate receipt use was rejected;
4. the tally followed the published rule;
5. the winning disposition was executed without substitution;
6. execution evidence was published without publishing receipt secrets; and
7. an independent reader can reconstruct why the capital reached its destination.

## Open questions

The following must be resolved before implementation or capital collection:

- How much capital should the first test raise?
- Is each contribution fixed at one amount?
- May one contributor obtain multiple eligible receipts?
- What quorum and winning threshold apply?
- How are ties resolved?
- What exact return mechanism supports return to sender?
- Which charity is the CEO's second-favorite charity?
- What costs are removed from the distributable pool?
- Which constituency may inspect nonpublic voting metadata?
- What event triggers a referendum concerning exploitation of the voting mechanism?
- Who verifies execution, given that the executing component may not solely certify itself?

## Disposition

This RFC is proposed. It does not authorize collection of capital, open a vote, name a charity, award a bonus, or ratify a voting constitution.
