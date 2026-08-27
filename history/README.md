# Pledge Project History

> **Required reading for humans and AI agents:** Read this file before proposing or making a material change to Pledge. Then read the current specification and the newest history entries relevant to the work. Do not rely on a Git diff, a chat transcript, or remembered context alone.

This directory is Pledge's durable, human-readable project memory. Its purpose is to preserve enough context that a future contributor—or an AI agent such as Codex, ChatGPT, or Grok—can recover what was requested, what was decided, what was corrected, what remains uncertain, and why the project changed.

## What belongs where

| Record | What it proves |
|---|---|
| Git commits | The exact files and lines that changed |
| Project history in this directory | The human explanation of direction, decisions, corrections, rejected paths, and unresolved questions |
| Runtime audit trail | Actions taken inside a deployed Pledge system; this is operational evidence and does not belong in this directory |

These records complement one another. A commit is not a substitute for an explanation, and a history entry is not a substitute for the code.

## Required convention

Create one Markdown file for each meaningful project event.

Use this filename:

```text
YYYY-MM-DD-NNN-short-title.md
```

- `NNN` is a zero-padded, monotonically increasing project-wide sequence number.
- Use a short, concrete, lowercase title separated by hyphens.
- Add every entry to the index in this file.
- Treat published entries as append-oriented history. Do not silently rewrite an earlier decision.
- When direction changes, write a new entry that identifies what it supersedes or corrects.
- Typographical, formatting, and broken-link repairs may be made in place through ordinary Git history.

## When an entry is required

Record an entry when work includes any of the following:

- a material requirement or design decision;
- a change of scope, priority, terminology, or system direction;
- a correction of a prior misunderstanding;
- a meaningful implementation or deployment milestone;
- a rejected, abandoned, or superseded approach;
- a hostile review and the project's response;
- a security, privacy, retention, identity, authorization, or audit-policy change;
- a failure whose cause or consequence will matter to future work.

Do not create history noise for an isolated typo or a purely mechanical refactor unless it changes meaning or exposes a meaningful failure.

## Required entry structure

```md
# History NNN — Concrete title

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted direction | Implemented | Superseded | Corrected | Abandoned
**Specification:** Version or N/A
**Supersedes:** Link or None
**Related:** Commits, issues, reviews, or other records

## Context

## Direction

## Decisions

## Corrections

## Open questions

## Result

## References
```

A section may say `None`, but it must not disappear. Consistent headings make the history scannable by people and machine-readable by agents.

## Rules of evidence and voice

Every entry must:

- distinguish the operator's stated requirements from an assistant's interpretation and from an implementation choice;
- quote critical direction when the exact wording carries meaning;
- identify assumptions as assumptions;
- avoid inventing motives, consent, decisions, or certainty;
- state corrections plainly, including what was previously misunderstood;
- preserve rejected or abandoned paths when they explain the present design;
- contain enough context to recover the intent without access to the original chat;
- link the specification, commits, issues, reviews, and superseding entries when available.

If two sources conflict, do not quietly reconcile them. Record the conflict and leave an open question or ask the operator.

## Orientation checklist

Before material work, a human or AI contributor must:

1. Read the root `README.md`.
2. Read the current `SPECIFICATION.md`.
3. Read this convention.
4. Read the newest entries relevant to the proposed work.
5. Check linked open reviews and issues when they affect the work.
6. Separate repository-backed facts from assumptions before acting.

After material work, the contributor must:

1. Create or update the appropriate history entry.
2. Add it to the index below.
3. Link the implementation commit, issue, review, or specification when one exists.
4. Commit the history record with the material change, or immediately afterward when a commit URL is needed.

This is a repository convention, not an optional writing preference. An agent given access to this repository is expected to discover and follow it. The prominent notice in the root README exists so that the convention is difficult to miss; it does not replace the responsibility to inspect the repository.

## History index

| No. | Date | Status | Entry |
|---:|---|---|---|
| 001 | 2026-08-27 | Accepted direction | [Bootstrap voice solicitation specification](./2026-08-27-001-bootstrap-voice-specification.md) |
