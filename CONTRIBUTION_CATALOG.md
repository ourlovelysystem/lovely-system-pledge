# Pledge Contribution Catalog and Deferred Deletion Function

**Date:** 2026-08-28  
**Status:** Requirements description; deletion implementation deferred

## Source statement

> When a user shares something with Pledge, that something should be catalogued in Our Lovely System - Pledge catalog. Should I call it an object catalog? That catalog will describe but will not contain user contributed artifacts. S3 will be the primary store. Users will get a UUIDv4 which keys their contributions. This will serve as a receipt. The receipt will be treated as a shared secret. A delete function will be enabled and will be outward facing. The delete function which we will describe now and defer on implementation will permit the bearer to submit a deletion request. That deletion request will require three approvals to proceed. Save the description. I am not ready to answer questions and give specifics at this time. Evaluate.

## Requirements traceable to the source statement

| ID | Requirement |
|---|---|
| PLEDGE-CATALOG-001 | When a user shares something with Pledge, the contribution shall be catalogued in the Our Lovely System — Pledge catalog. |
| PLEDGE-CATALOG-002 | The catalog shall describe user-contributed artifacts but shall not contain the artifacts. |
| PLEDGE-CATALOG-003 | Amazon S3 shall be the primary store for user-contributed artifacts. |
| PLEDGE-CATALOG-004 | Each contribution shall be keyed by a UUIDv4 provided to the user. |
| PLEDGE-CATALOG-005 | The provided UUIDv4 shall serve as the user's receipt for the contribution. |
| PLEDGE-CATALOG-006 | The receipt shall be treated as a shared secret. |
| PLEDGE-DELETE-001 | Pledge shall provide an outward-facing delete function. |
| PLEDGE-DELETE-002 | The delete function shall permit the bearer of the receipt to submit a deletion request. |
| PLEDGE-DELETE-003 | A deletion request shall require three approvals before it proceeds. |
| PLEDGE-DELETE-004 | The delete function is described now and its implementation is deferred. |

## Evaluation

### Catalog name

**Object catalog** is workable, but it can be read as a catalog of S3 objects or as a store containing objects. This catalog instead describes contributions whose artifacts reside in S3.

**Contribution catalog** is the clearer current name because it identifies what each catalog entry represents without implying that the table contains the contributed artifact. **Artifact catalog** would also be defensible if the catalog's scope is limited to contributed artifacts rather than contributions more broadly.

This document uses **contribution catalog** as a descriptive label. The permanent table and product terminology remain undecided.

### Separation of description and content

Keeping descriptive catalog records separate from the artifacts they describe establishes a clear boundary:

- the catalog describes the contribution;
- S3 stores the contributed artifact;
- the UUIDv4 identifies the contribution;
- the user's copy of that UUIDv4 functions as both receipt and shared secret.

### Deletion model

The proposed deletion path separates possession of the receipt from authority to complete deletion:

1. the bearer presents the receipt;
2. the bearer submits a deletion request;
3. the request awaits three approvals;
4. deletion may proceed only after the approval requirement is satisfied.

The receipt therefore permits initiation of the deletion process. It does not, by itself, authorize immediate deletion.

## Deliberately unspecified

The following matters are not defined by the source statement and are not requirements in this document:

- the permanent catalog name;
- DynamoDB table names, keys, indexes, or record schema;
- catalog fields beyond the UUIDv4 relationship;
- whether one UUIDv4 identifies a contribution, artifact, or catalog entry when those concepts diverge;
- how the UUIDv4 is delivered, displayed, stored, recovered, or rotated;
- how bearer possession is proven;
- whether additional authentication is required;
- the deletion endpoint, request format, or user interface;
- who or what may approve;
- whether approvals must be distinct;
- approval order, timing, expiry, revocation, quorum mechanics, or conflict handling;
- what “proceed” entails;
- deletion scope across S3 objects, catalog records, replicas, derivatives, logs, transcripts, or backups;
- retention, tombstone, audit, notification, or recovery behavior;
- failure handling; and
- implementation timing.

These questions remain open because Will Daly stated that he is not ready to answer questions or provide specifics at this time.
