# History 002 — Root README welcomes before it instructs

**Date:** 2026-08-27  
**Status:** Corrected  
**Specification:** [0.0.0-alpha.1](../SPECIFICATION.md)  
**Supersedes:** The opening presentation introduced in [commit 7b4bc03](https://github.com/ourlovelysystem/lovely-system-pledge/commit/7b4bc03af3fa8af3110e10227790f1794b4b3100)  
**Related:** [Project-history convention](./README.md)

## Context

The first root-level pointer to the project-history convention opened with “Required orientation” and immediately told readers what they were expected to read and do. It made the history convention difficult to miss, but it placed procedural enforcement ahead of Pledge itself.

The operator's response was direct: “I do not like the tone of the root readme. The demanding language turned me off right away.”

## Direction

The root README should welcome and orient. It should explain Pledge before introducing repository procedure. The project-history convention must remain easy to find and useful to human and AI contributors without making the repository's front door sound like a compliance notice.

## Decisions

- Lead with Pledge's purpose and bootstrap premise.
- Present the specification, project history, and hostile review under a plain “Start here” heading.
- Describe the value of reading project history rather than opening with a command.
- Keep the detailed convention precise in `history/README.md`.
- Preserve the prominent root-level link so the convention remains discoverable.

## Corrections

The original root README overcorrected for discoverability by using demanding language before establishing context. Discoverability and procedural clarity do not require an admonishing opening.

No functional Pledge requirement changed.

## Open questions

None.

## Result

The root README now introduces Pledge first and offers its records as the shortest route into the project. The history convention remains prominent and unchanged in substance.

## References

- [Root README](../README.md)
- [Project-history convention](./README.md)
- [Commit that introduced the earlier wording](https://github.com/ourlovelysystem/lovely-system-pledge/commit/7b4bc03af3fa8af3110e10227790f1794b4b3100)
