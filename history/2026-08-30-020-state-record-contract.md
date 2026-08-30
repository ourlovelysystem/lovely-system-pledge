# History 020 — State-record contract

**Date:** 2026-08-30
**Status:** Accepted direction
**Specification:** N/A
**Supersedes:** None
**Related:** [History 019 — Ready transition implemented](./2026-08-30-019-ready-transition-implemented.md)

## Context

Pledge’s state table is a small collection of individually typed parameter records. The browser state endpoint and transcription-completion Lambda both depend on exact attribute names and value types.

Manual console testing confirmed that Pledge exposes any returned `run_mode` value. It renders a dedicated page only for values it recognizes.

## Direction

The minimum record form is:

```json
{
  "parameter_name": { "S": "run_mode" },
  "parameter_value": { "S": "ready" }
}
```

`parameter_name` is the partition key. `parameter_value` is required and typed by that parameter’s contract.

`updated_at` is not a DynamoDB system attribute and is not part of the required minimum form. The completion Lambda currently writes it when changing `run_mode`; manual console changes do not. It is optional automation metadata, not an authoritative last-change timestamp.

## Decisions

| Parameter | Valid values | Effect | Absent, wrong type, or unrecognized value |
|---|---|---|---|
| `run_mode` | String `ready` | Render the blank Ready page. | Render the diagnostic state page. |
| `run_mode` | String `voiceless` | Render the voice-lending page. | Render the diagnostic state page. |
| `save_transcript_to_object` | Boolean `true` or `false` | `true`: load the transcript object from the Pledge S3 bucket. `false`: load the Amazon Transcribe transcript URL. | Treated as `false`. |
| `save_transcript_to_database` | Boolean `true` or `false` | `true`: store `transcript_text` in the catalog. `false`: remove it from the catalog. | Treated as `false`. |

`run_mode = "standby"` is not a separately recognized frontend mode. It happens to produce the diagnostic page, as do an empty string and arbitrary strings such as `"yabba dabba doo"`.

Boolean parameter form:

```json
{
  "parameter_name": { "S": "save_transcript_to_database" },
  "parameter_value": { "BOOL": true }
}
```

## Corrections

The initial draft incorrectly labeled `updated_at` as required. It is application-written metadata, not an AWS-maintained system field.

## Open questions

- Remove `updated_at` from the completion Lambda’s state write, or explicitly retain it as limited automation metadata.
- Add the catalog-deletion trigger that rechecks eligibility and sets `run_mode = "voiceless"` when the final eligible recording is deleted.
- Define additional recognized run modes only when Pledge needs their distinct pages.

## Result

The required state-record contract is documented. No attribute name or value is changed by this entry.

## References

- [Pledge history convention](./README.md)
- [History 019 — Ready transition implemented](./2026-08-30-019-ready-transition-implemented.md)
