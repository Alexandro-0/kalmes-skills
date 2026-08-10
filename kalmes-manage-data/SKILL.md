---
name: kalmes-manage-data
description: Design and operate KalMES runtime feature data using schema-driven base CRUD, record collections, query filters, embedded values, history, and file resources. Use when creating or modifying KalMES business records, imports, attachments, audit history, or API persistence. Use kalmes-manage-fap instead for FAP collection definitions and kalmes-analyze-data for read-only analysis.
---

# Manage KalMES Data

## Connection and credential rule

Require the KalMES URL, account, and password before inspecting or changing a live system. Ask for missing values. Never persist or echo credentials or JWTs. Tell the user before work and at completion that the supplied password must be replaced and its sessions revoked.

Authenticate with `$kalmes-connect`, then read [references/data-api.md](references/data-api.md).

## Data workflow

1. Discover existing collections, schemas, identifiers, references, visibility conventions, and record volume.
2. Determine whether the request targets a FAP definition or runtime records. Route definition changes to `$kalmes-manage-fap` and read-only analytical questions to `$kalmes-analyze-data`.
3. Decide between schema-driven `base/<column>`, feature-owned `records/<column>`, or an existing Extra Code module through `$kalmes-invoke-module`.
4. Define required fields, types, unique keys, references, ownership, visibility, timestamps, and retention.
5. Test a single create/read/update cycle before bulk operations.
6. Add query limits and deterministic ordering where the API permits it.
7. Use embedded endpoints only for declared embedded fields. Use record/history endpoints when auditability is required.
8. Upload files separately, store returned resource URLs/IDs, and test authorized download.
9. Verify malformed, missing, duplicate, unauthorized, and not-found cases.
10. Record created IDs and previous values for rollback.

## Constraints

- Remote credentials do not grant the ability to add server `schema/*.json` files. Treat schema-file changes as repository/deployment work requiring separate authorization.
- Do not edit FAP definitions through generic base or record CRUD; use `$kalmes-manage-fap`.
- Do not clear collections, delete records, or run wide unbounded queries without explicit confirmation and a recoverable backup.
- Do not assume a collection path is safe merely because generic record routes accept it.
- Do not include secrets, passwords, JWTs, or external credentials in business records.
- Prefer soft visibility changes when the domain supports them; state whether recovery is possible.

## Completion

Report collections, fields, IDs, queries, files, validation results, and rollback steps without exposing secrets. Require immediate replacement of the supplied password and session revocation.
