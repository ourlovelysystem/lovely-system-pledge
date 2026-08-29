# History 012 — Transcript storage recommendation corrected

**Date:** 2026-08-29  
**Status:** Corrected  
**Specification:** N/A  
**Supersedes:** None  
**Related:** [Computahhh Event 151](https://github.com/ourlovelysystem/lovely-system-computahhh/blob/main/events/2026-08-29-151.md); [hostile review invitation](https://github.com/ourlovelysystem/lovely-system-nasty-oracle/issues/1)

## Context

Pledge now stores borrowed audio durably in S3 and records each electronic valuable in DynamoDB. The next processing increment will transcribe submitted audio, evaluate whether it performs the requested auditory function, and update the catalog with useful metrics.

Codex initially recommended storing:

- the complete Amazon Transcribe result in S3; and
- readable transcript text and summary metrics in DynamoDB.

A weighted comparison assigned 90% to the combined S3-and-DynamoDB approach, 86% to S3 only, and 65% to DynamoDB only. The analysis treated S3 transcript storage as necessary durable evidence and treated DynamoDB as a rebuildable projection of that transcript.

The operator objected:

> The transcript is derived from the audio file. Audio file is already on durable storage. I think your estimates factoring s3 durability are therefore less than compelling.

## Direction

The objection is sustained.

The durable borrowed asset is the audio recording:

```text
electronic-valuables/<receipt_id>
```

The transcript is a derived interpretation of that audio. Loss of the DynamoDB transcript does not destroy the borrowed evidence because Pledge can transcribe the durable audio again.

The corrected present recommendation is:

> **Keep the audio in S3. Put the derived transcript and useful transcription metrics in DynamoDB. Do not create a second S3 transcript artifact until exact historical provider output has a demonstrated use.**

## Decisions

### 1. The audio remains canonical

The audio object is what the user lent. It remains the source from which transcription can be regenerated.

### 2. The transcript belongs in the operational catalog

The electronic-valuables item should contain the readable transcript and useful processing information, including:

```text
transcript_text
transcription_status
transcription_job_name
transcription_confidence_mean
transcription_confidence_min
recognized_word_count
recognized_duration_seconds
transcription_completed_at
transcription_policy_version
content_decision
semantic_match_score
content_reason
```

Exact attribute names remain subject to implementation review. The governing direction is that useful transcript content and metrics belong in the catalog.

### 3. S3 transcript output is deferred

Pledge will not store complete provider JSON in S3 merely because S3 is more durable.

A separate S3 transcript artifact becomes justified if Pledge establishes a need to preserve exactly what a particular transcription system reported at a particular time, including word-level alternatives, timings, confidence values, and provider-specific output.

### 4. Retranscription is reconstruction, not perfect historical reproduction

The transcript can be regenerated from audio, but a later provider model may produce different words, punctuation, timing, or confidence scores.

The catalog should therefore preserve enough processing context to explain the current interpretation:

- provider;
- job identifier;
- completion time;
- language;
- policy version; and
- transcript and summary metrics.

Whether exact historical provider output deserves separate preservation remains open.

### 5. Catalog item size remains bounded

DynamoDB has a 400 KB item limit. Pledge's recording control solicits short recordings, so transcript text should ordinarily remain far below that boundary. The implementation must still reject or externalize an unexpectedly large derived result rather than allowing a catalog update to fail ambiguously.

## Corrections

The original weighting improperly treated transcript durability as independent from audio durability.

That double-counted the preservation benefit of S3:

```text
durable audio
+ durable derived transcript
```

without adequately crediting this reconstruction path:

```text
durable audio
→ retranscription
→ rebuilt catalog transcript
```

The corrected weighted evaluation is:

| Criterion | Weight | DDB only | S3 only | S3 + DDB |
|---|---:|---:|---:|---:|
| Catalog usefulness | 30% | 10/10 | 4/10 | 10/10 |
| Simplicity and consistency | 25% | 10/10 | 8/10 | 5/10 |
| Historical processing evidence | 15% | 7/10 | 10/10 | 10/10 |
| Rebuildability from audio | 10% | 9/10 | 10/10 | 10/10 |
| Size tolerance | 10% | 6/10 | 10/10 | 9/10 |
| Reporting and analysis | 10% | 6/10 | 9/10 | 9/10 |
| **Weighted result** | **100%** | **89%** | **77%** | **83%** |

These scores are structured judgments rather than measured probabilities.

## Hostile review invited

Pledge invites hostile review of the corrected recommendation.

Useful attacks include:

1. Is a transcript genuinely reproducible when provider models, vocabulary, punctuation, and confidence calibration change?
2. Does retranscription reconstruct the catalog or create a new interpretation that falsely replaces history?
3. Is the transcript itself consequential evidence once it determines whether a borrowed voice becomes usable?
4. Does storing transcript text only in DynamoDB violate the rule that nothing important should exist only in DynamoDB?
5. Is the 400 KB item limit being dismissed too casually?
6. Does putting transcript text beside public or inspectable catalog metadata create a privacy or access-control problem?
7. Would storing the provider result in S3 cost so little that declining to preserve it is false economy?
8. Is the proposed processing context sufficient to reproduce or challenge a content decision?
9. Should the system preserve exact provider output only for disputed or consequential decisions?
10. What evidence would demonstrate that S3 transcript preservation has become useful rather than merely comforting?

The project requests the sharp version. A hostile reviewer should attack the reconstruction premise rather than accepting “derived” as a synonym for “disposable.”

## Open questions

- Must Pledge preserve the exact historical interpretation used to admit a recording into the usable catalog?
- Is the transcript important evidence or merely replaceable processing output?
- Should disputed, rejected, or manually reviewed recordings preserve richer provider output?
- What maximum transcript length belongs in the catalog?
- What access classes may inspect transcript text?
- What processing metadata is required to make a later retranscription meaningfully comparable?

## Result

The storage recommendation has been corrected before transcription implementation.

Current direction:

```text
S3:
  durable borrowed audio

DynamoDB:
  derived transcript
  transcription metrics
  content evaluation
  processing context

S3 transcript artifact:
  deferred until exact historical output has a demonstrated use
```

No transcription pipeline has been implemented by this record.

## References

- [Pledge specification](../SPECIFICATION.md)
- [Pledge project history convention](./README.md)
- [Computahhh Event 151](https://github.com/ourlovelysystem/lovely-system-computahhh/blob/main/events/2026-08-29-151.md)
- [Hostile review invitation](https://github.com/ourlovelysystem/lovely-system-nasty-oracle/issues/1)

## Subsequent correction — hostile review scope

The operator subsequently corrected the review invitation:

> I don't want to narrow the scope of the hostile review. I am also considering the possibility that we may not want to keep the transcript at all.

The earlier list of suggested attacks is preserved as evidence of how Codex narrowed the invitation. It is not the scope of the requested review.

The hostile reviewer is invited to attack the entire design, its premises, its omissions, and the framing of the question. The reviewer is specifically free to reject every presented storage option, including the assumption that Pledge should retain transcript text after content evaluation.

No decision has been made to retain or discard transcripts. The live candidate set now includes at least:

- retain transcript text in DynamoDB;
- retain complete transcript output in S3;
- retain both;
- retain the transcript temporarily and purge it after evaluation;
- retain only derived metrics and the content decision;
- retain only evidence that transcription occurred;
- retain nothing derived after evaluation; and
- reject transcription as the validation mechanism.

The reviewer is not required to choose among these candidates and may identify alternatives not listed here.

