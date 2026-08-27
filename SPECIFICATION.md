# Pledge Bootstrap Voice Solicitation Specification

**Version:** 0.0.0-alpha.1  
**Status:** Initial recoverable draft  
**Date:** 2026-08-27  
**Project:** `pledge.ourlovelysystem.org`

## 1. Purpose

Pledge is intended to solicit, collect, evaluate, and temporarily use contributed human voice recordings.

A new Pledge deployment begins with a bootstrapping problem: it is supposed to speak an auditory challenge, but it has no voice of its own. The first usable voice must therefore be solicited through text. Once a usable recording exists, Pledge may use its voice catalogue to speak to later visitors.

The first implementation is deliberately narrow. It establishes:

- the no-voice bootstrap state;
- a reusable voice-solicitation utility;
- immediate audio-envelope validation;
- asynchronous transcription and semantic validation;
- time-bounded permission to use a recording;
- a catalogue of eligible auditory challenges;
- priority handling for minimum-use commitments;
- normal and sulk behavior; and
- deletion of expired audio and associated transcripts.

The broader Pledge system may later use the same voice-solicitation utility in other contexts.

## 2. Governing distinction

Pledge does not wait for transcription before allowing the contributor to proceed.

Two validation stages exist.

### 2.1 Synchronous envelope validation

Pledge validates that an audio submission exists and is structurally usable. It does not validate what the speaker said.

An envelope is valid when, at minimum:

- an audio object was received;
- the upload completed;
- the object is non-empty;
- the media type is supported;
- the object can be decoded;
- its duration falls within configured limits; and
- it contains a minimally usable audio signal.

When the envelope is valid:

1. Pledge creates the durable submission record.
2. Pledge schedules asynchronous content processing.
3. Pledge allows the contributor to pass through immediately.
4. Pledge sends the contributor to the **Come Back Soon** page.

Envelope acceptance is not catalogue acceptance.

### 2.2 Asynchronous content validation

Offline processing evaluates the recording after the contributor has left the submission workflow.

Pledge knows:

- the text solicitation presented when the audio was collected;
- the requested auditory function;
- the submitted audio;
- the applicable permission period; and
- the submission record to which processing results belong.

The asynchronous process:

1. transcribes the audio;
2. preserves transcription-confidence information when available;
3. compares the transcript to the requested function;
4. calculates a semantic match score;
5. decides whether the track is usable, unusable, or uncertain;
6. attaches the transcript, score, and decision to the durable submission record; and
7. adds a usable, unexpired track to the appropriate catalogue.

The contributor does not wait for any of these steps.

## 3. Bootstrap state

A new deployment has no eligible auditory challenge recordings.

The landing page communicates:

> Pledge has no voice of its own. Can Pledge borrow your voice?

If the visitor agrees, Pledge invokes the reusable voice-solicitation utility in the bootstrap context.

The bootstrap solicitation asks the visitor to record a voice track that performs the auditory function:

> Ask the listener: “Who are you?”

After Pledge accepts the audio envelope, the visitor is directed to the **Come Back Soon** page.

The page contains a link back to the landing page.

Bootstrap mode ends when the catalogue contains at least one usable and unexpired `who_are_you` voice track.

## 4. Illustrative bootstrap sequence

1. Will Daly visits `pledge.ourlovelysystem.org`.
2. Pledge has no eligible voice.
3. Pledge asks in text whether it may borrow Will’s voice.
4. Will agrees.
5. Pledge asks Will to record an auditory “Who are you?” challenge.
6. Will records the requested track.
7. Pledge validates the audio envelope only.
8. The envelope passes.
9. Pledge creates a durable submission record.
10. Pledge queues offline transcription and content validation.
11. Pledge sends Will to the Come Back Soon page.
12. Will follows its link to the landing page.
13. If Will’s recording has completed processing and is usable, Pledge now has a voice.
14. Pledge challenges Will using an eligible catalogue track, potentially his own:

> Who are you?

If processing has not finished, or if no submitted track has become usable, Pledge remains in its no-eligible-voice behavior.

## 5. Reusable voice-solicitation utility

Voice solicitation is a system utility for varying contexts.

Each invocation provides a solicitation contract containing at least:

| Field | Meaning |
|---|---|
| `context` | Why the voice is being requested |
| `display_text` | Text shown to the contributor |
| `requested_function` | What the resulting track must accomplish |
| `reference_text` | A representative phrase, when one exists |
| `catalogue` | Eligible destination catalogue |
| `duration_options` | Permitted borrowing periods |
| `minimum_use_options` | Permitted minimum-use commitments |
| `audio_constraints` | Media, size, duration, and signal rules |
| `validation_policy_version` | Content-validation rules applied later |
| `retention_policy_version` | Retention rules governing the submission |

The bootstrap context uses:

- context: `bootstrap`;
- requested function: ask the listener who they are;
- reference text: `Who are you?`; and
- catalogue: `who_are_you`.

Later contexts may request other auditory functions without requiring a new recording subsystem.

## 6. Semantic acceptance

Pledge is not hostile to humor, grammatical variation, or stylistic interpretation.

The validator does not require exact repetition of the reference text. It asks:

> Is this recording recognizably performing the requested auditory function?

For the requested function “ask the listener who they are,” all of the following should be capable of acceptance:

| Example transcript | Intended disposition |
|---|---|
| “Who are you?” | Accept |
| “Who are you, dickwad?” | Accept |
| “Who you are?” | Accept |
| “Who you?” | Accept |
| “Sing me your name.” | Accept |
| Speech unrelated to the listener’s identity | Reject or review |

Added humor is not a failure merely because it was not present in the reference text.

A track fails when it does not adequately perform the requested function.

## 7. Scores and decisions

Pledge should preserve two different measures when the transcription provider makes them available.

### 7.1 Transcription confidence

Transcription confidence estimates how confidently the speech-recognition system identified the spoken words.

It does not measure whether those words serve Pledge’s requested function.

### 7.2 Semantic match score

The semantic match score estimates how closely the transcript performs the requested function.

This is a system score, not a calibrated probability that the decision is objectively correct.

Illustrative output:

```json
{
  "requested_function": "ask the listener who they are",
  "reference_text": "Who are you?",
  "transcript": "Who are you, dickwad?",
  "transcription_confidence": 0.91,
  "semantic_match_score": 0.94,
  "decision": "usable"
}
```

Provisional score bands may begin as:

| Semantic match | Provisional treatment |
|---:|---|
| 0.80–1.00 | Automatically usable |
| 0.60–0.79 | Candidate for acceptance or review |
| 0.35–0.59 | Review or hold |
| 0.00–0.34 | Automatically unusable |

These thresholds are not locked. They must be calibrated against an actual test collection containing literal, humorous, rearranged, abbreviated, semantically equivalent, noisy, and unrelated recordings.

A low transcription-confidence result may still represent a good recording. Uncertainty should remain inspectable rather than being silently converted into rejection.

## 8. Submission and catalogue states

Suggested submission states:

```text
uploading
envelope_rejected
envelope_accepted
transcription_pending
transcribed
validation_pending
usable
unusable
review_required
expired
withdrawn
purged
```

A track is eligible for selection only when:

- its envelope was accepted;
- asynchronous processing completed;
- its decision is `usable`;
- its borrowing permission is active;
- it has not expired;
- it has not been withdrawn;
- it has not been purged; and
- it belongs to the requested catalogue.

## 9. Normal voice state

When one or more eligible `who_are_you` recordings exist, Pledge is no longer in bootstrap mode.

At authentication time, Pledge selects an eligible auditory challenge from the catalogue and plays it to the visitor.

Ordinary selection is random, subject to unmet minimum-use commitments.

Pledge therefore speaks with borrowed voices rather than a permanent voice of its own.

## 10. Sulk mode

If Pledge once had an eligible voice but no eligible voice remains, it enters **sulk mode**.

Sulk mode presents a textual sob story:

> Once upon a time I had a voice. Now I have none. May I borrow yours?

Acceptance invokes the same reusable voice-solicitation utility.

Bootstrap and sulk mode share the same technical no-eligible-voice condition. They differ in presentation and system history:

- bootstrap: Pledge has not yet acquired its first usable voice;
- sulk: Pledge previously had a voice and lost eligibility to use it.

## 11. Time-bound borrowing

Every contributed track has a defined authorization period.

The test system must support borrowing periods measured in minutes so expiration and purging can be exercised efficiently.

After testing and validation, ordinary options are expected to move toward periods measured in days or longer.

When the borrowing period expires:

1. the track immediately becomes ineligible for playback;
2. the audio track is purged;
3. associated transcriptions are purged; and
4. the catalogue is recalculated.

An audit record may preserve that a submission and purge event occurred without preserving the expired voice or transcript. The exact non-content audit fields remain to be defined.

The authorization clock and its start event must be explicit. Candidate start events include envelope acceptance, catalogue acceptance, or first use. This version does not select among them.

## 12. Minimum-use commitment

A contribution may carry an **at least X uses** parameter.

The parameter is intended to make a newly lent voice likely to be heard promptly, including by the contributor who returns to Pledge soon after submitting it.

Tracks with unmet minimum-use commitments move ahead of the ordinary random-selection pool.

Selection behavior:

1. discard ineligible tracks from consideration;
2. identify eligible tracks where `completed_uses < minimum_uses`;
3. select from that priority group;
4. if no eligible priority tracks exist, select randomly from the ordinary eligible catalogue; and
5. increment `completed_uses` after successful playback.

Time-bound permission remains controlling. A minimum-use commitment must not silently extend permission after expiration. If the time period expires first, the track becomes ineligible and is purged even if Pledge failed to satisfy X uses.

The interface must not describe “at least X” as guaranteed unless the system actually guarantees it within the authorized period.

## 13. Durable records

A minimal submission record should preserve:

```text
submission_id
context
solicitation_text
requested_function
reference_text
catalogue
audio_object_reference
audio_media_type
audio_duration
audio_hash
envelope_accepted_at
borrowing_starts_at
expires_at
minimum_uses
completed_uses
transcription_status
transcript
transcription_confidence
semantic_match_score
catalogue_decision
validation_policy_version
retention_policy_version
withdrawn_at
purged_at
created_at
updated_at
```

This list expresses recoverable intent, not a locked physical schema.

The system should distinguish temporary content from durable event metadata so that audio and transcripts can be purged without erasing the fact that governed processing occurred.

## 14. State derivation

The landing behavior is derived from current inventory and history.

| Condition | Mode |
|---|---|
| No eligible voice has ever existed | Bootstrap |
| At least one eligible voice exists | Normal voice |
| A voice existed previously but none is currently eligible | Sulk |

Eligibility is computed from durable state. It should not depend on a manually maintained “has voice” flag that can drift away from the catalogue.

## 15. Initial functional boundary

The first build should include:

- the Pledge landing page;
- bootstrap/no-voice presentation;
- consent to lend a voice;
- the reusable solicitation interface;
- browser audio recording;
- synchronous envelope validation;
- immediate navigation to Come Back Soon after envelope acceptance;
- the Come Back Soon return link;
- durable submission metadata;
- durable temporary audio storage;
- asynchronous transcription;
- semantic comparison against the known requested function;
- inspectable scores and decisions;
- automatic catalogue eligibility;
- random challenge selection;
- minimum-use priority selection;
- test-scale expiration in minutes;
- automatic purge of expired audio and transcripts; and
- sulk-mode presentation.

## 16. Explicit non-requirements for this version

Version 0.0.0-alpha.1 does not require:

- exact-phrase matching;
- synchronous transcription;
- waiting for catalogue acceptance before admitting the contributor;
- speaker biometric identification;
- proof of civil identity;
- trustees;
- agents;
- seniority;
- coups;
- permanent voice ownership;
- permanent retention of contributed audio; or
- implementation of every future Pledge authorization gate.

Those broader concepts remain part of Pledge’s direction but are outside this bootstrap specification.

## 17. Unresolved parameters

The following decisions remain open:

- exact landing-page copy and controls;
- whether declining the solicitation has a dedicated path;
- supported audio formats;
- minimum and maximum recording duration;
- signal-quality threshold;
- authorization-clock start event;
- minute-scale testing choices;
- later production duration choices;
- permitted values for minimum uses;
- priority selection within multiple unmet commitments;
- whether catalogue acceptance can occur without human review;
- semantic model or algorithm;
- initial score thresholds;
- review workflow;
- handling of transcription failure;
- handling of purge failure;
- precise audit record retained after content purge;
- whether a contributor can withdraw before expiration;
- how immediate return behaves while transcription remains pending; and
- whether the system identifies that a visitor heard their own contributed voice.

## 18. Recovery statement

If implementation context is lost, recover the intended system from this rule:

> Pledge begins mute. It asks a visitor through text to lend a recording that can ask “Who are you?” Pledge validates only the audio envelope before allowing the visitor to proceed. It transcribes and semantically evaluates the recording offline, tolerating humor and nonliteral phrasing. Usable recordings enter a time-bound catalogue. Tracks with unmet minimum-use commitments receive selection priority; otherwise selection is random. Expired audio and transcripts are purged. If no eligible voice has ever existed, Pledge bootstraps. If it loses all voices later, Pledge sulks and asks to borrow another.
