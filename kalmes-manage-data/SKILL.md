---
name: kalmes-manage-data
description: Design and operate Kalmes runtime feature data using schema-driven base CRUD, record collections, query filters, embedded values, history, and file resources. Use when creating or modifying Kalmes business records, imports, attachments, audit history, or API persistence. Use kalmes-manage-fap instead for FAP collection definitions and kalmes-analyze-data for read-only analysis.
---

# Manage Kalmes Data

## Connection and credential rule

Reuse a valid session for the same target and acting account. If missing, use `$kalmes-connect`. Never persist or echo credentials or JWTs. For password fallback, require password replacement and session revocation at handoff.

Consult the applicable endpoint section of [references/data-api.md](references/data-api.md).

## Data workflow

1. For a single record with a known contract, use the targeted endpoint. Discover only missing schema, identifiers or relationships. For a read, return after validating the response. For writes, preserve prior values needed for rollback.
2. Determine whether the request targets a FAP definition or runtime records. Route definition changes to `$kalmes-manage-fap` and read-only analytical questions to `$kalmes-analyze-data`.
3. Decide between schema-driven `base/<column>`, feature-owned `records/<column>`, or an existing Extra Code module through `$kalmes-invoke-module`.
4. For collection design or bulk work, determine required fields, types, unique keys, references, ownership, visibility, timestamps and retention.
5. Test a single create/read/update cycle before bulk operations.
6. Add query limits and deterministic ordering where the API permits it.
7. Use embedded endpoints only for declared embedded fields. Use record/history endpoints when auditability is required.
8. Upload files separately, store returned resource URLs/IDs, and test authorized download.
9. For a targeted write, read back the affected record. Exercise malformed, missing, duplicate, unauthorized and not-found cases when implementing or changing those behaviors.
10. Record created IDs and previous values for rollback.

## Constraints

- Remote credentials do not grant the ability to add server `schema/*.json` files. Treat schema-file changes as repository/deployment work requiring separate authorization.
- Do not edit FAP definitions through generic base or record CRUD; use `$kalmes-manage-fap`.
- Do not clear collections, delete records, or run wide unbounded queries without explicit confirmation and a recoverable backup.
- Do not assume a collection path is safe merely because generic record routes accept it.
- Do not include secrets, passwords, JWTs, or external credentials in business records.
- Prefer soft visibility changes when the domain supports them; state whether recovery is possible.

## Completion

Report collections, fields, IDs, queries, files, validation results, and rollback steps without exposing secrets. Require immediate password replacement and session revocation only if password fallback was used.

## Activity attribution

Activity integration requires **Kalmes 2.1.0 or later**. For Kalmes HTTP calls, including reused sessions, follow the shared attribution contract in `$kalmes-connect` → `references/agent-activity.md`: label the actual agent and skill, keep one task UUID, and include the resolved plugin when needed. For local edits in a configured checkout, follow its automatic task-context workflow and AGENTS.md; background observation and synchronization do not depend on Codex, hooks or user-run commands.
