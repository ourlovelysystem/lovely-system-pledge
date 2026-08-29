# History 017 — Bedrock functional-match evaluation pending

**Date:** 2026-08-29
**Status:** Proposed
**Specification:** N/A
**Supersedes:** None
**Related:** [History 016 — Native audio retained; playback conversion deferred](./2026-08-29-016-native-audio-conversion-deferred.md)

## Context

Pledge successfully transcribed a native WebM/Opus recording. Amazon Transcribe produced the transcript “Who are you?” with mean confidence 0.997 and minimum confidence 0.996.

Discussion then separated two different measurements:

- transcription confidence asks whether Amazon Transcribe recognized the spoken words reliably;
- functional match asks whether those words perform Pledge's requested function.

Confidence alone is insufficient. A clear recording of “Take this job and shove it” may receive high transcription confidence while failing to ask the listener to identify themselves.

Literal transcript matching was rejected:

> No. Fuck literal matches. That is not the target.

## Direction

The requested function is:

> Ask the listener to identify themselves.

The reference text “Who are you?” is an example of that function, not a required literal phrase.

A semantic evaluator should distinguish:

| Recording | Transcription confidence | Functional match | Candidate decision |
|---|---:|---:|---|
| “Who are you?” | High | 1.00 | Usable |
| “Halt! Who goes there?” | High | approximately 0.92 | Usable |
| “Who are you, dickwad?” | High | approximately 0.97 | Usable |
| “Take this job and shove it.” | High | approximately 0.03 | Unusable |
| Unclear audio that might say “Who are you?” | Low | Uncertain | Review |

The functional-match values above are illustrative, not measured or calibrated.

## Proposed mechanism

Amazon Transcribe does not supply functional match. Pledge would calculate it separately using a text model available through Amazon Bedrock.

Candidate evaluator input:

    requested_function: Ask the listener to identify themselves.
    reference_text: Who are you?
    transcript: Halt! Who goes there?

Candidate structured output:

    semantic_match_score: 0.92
    content_decision: usable
    content_reason: Asks the listener to identify themselves.

The score would be Pledge-generated system judgment, not an AWS probability or objective truth.

For the simplest implementation, Bedrock evaluation could remain a separate logical step inside the existing transcription-completion Lambda. It would require:

1. access to one Bedrock text model;
2. bedrock:InvokeModel permission;
3. a model-ID environment variable;
4. strict structured-output validation;
5. storage of score, decision, reason, model, and policy version; and
6. a calibration collection containing literal, creative, hostile, ambiguous, and unrelated recordings.

No new bucket, table, API route, browser workflow, or synchronous user wait is presently required.

## Creative readings under consideration

A semantic evaluator may recognize the following as performing the requested function:

- “Halt! Who goes there?”
- “State your name and purpose.”
- “Identify yourself, traveler.”
- “What name do you answer to?”
- “Who stands before Pledge?”
- “Name yourself, mortal.”
- “What do they call you?”
- “Speak your name and be known.”
- “Friend, foe, or confused passerby—who are you?”
- “You have reached the identity checkpoint. Say something incriminating about yourself.”
- “Who the fuck are you?”
- “I know who I am. Your turn.”
- “A stranger approaches. Care to fix that?”
- “This door requires a name. Got one?”
- “Tell Our Lovely System who just showed up.”
- “Reveal your secret identity—or your regular one.”
- “Who occupies that magnificent meat suit?”
- “Please provide one useful answer to the existential crisis: who are you?”

These examples describe desired semantic latitude. They are not yet an acceptance test, training set, guaranteed output, or approved content policy.

## Decisions

Decision pending.

The following points are established for evaluation:

- literal matching is not the target;
- transcription confidence and functional match are separate;
- functional match must evaluate meaning;
- creative, theatrical, rude, indirect, and humorous readings may remain usable when they perform the requested function;
- unrelated speech must not become usable merely because it was transcribed confidently; and
- any stored score must remain inspectable as system judgment.

No Bedrock model, prompt, threshold, automatic-acceptance band, review band, or implementation authority is selected by this entry.

## Corrections

The earlier suggestion that reference plus transcription confidence might be sufficient omitted the possibility of confidently transcribed but functionally unrelated speech. Functional match is a separate required judgment if Pledge is to automate catalogue admission without literal matching.

## Open questions

- Is Bedrock worth the additional evaluation and calibration machinery?
- Which model should perform the judgment?
- Should the evaluator use a score, categorical judgment, or both?
- What thresholds produce usable, unusable, and review-required decisions?
- How should prompt injection inside a transcript be neutralized?
- How much model and prompt context must be preserved for later inspection?
- Should uncertain decisions wait for human review?
- How should model-version changes affect previously admitted recordings?
- Which creative readings reveal weaknesses in the evaluator?

## Result

Bedrock semantic evaluation is documented as a candidate mechanism with decision pending.

No Bedrock integration or content decision has been implemented by this record.

## References

- [Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
- [Amazon Transcribe input and output](https://docs.aws.amazon.com/transcribe/latest/dg/how-input.html)
- [Pledge project history convention](./README.md)
