# Project context API v1

Paths are relative to the authenticated Kalmes API root. Check `GET project-context/capabilities`; `protocol_version: 1` confirms support. Do not infer capabilities from deployment version strings.

## Access

Bearer JWT and existing account/API-key validation apply. Roles: SI, Reseller, SuperUser, Day1. The creator owns the project; owners and SuperUser/Day1 manage membership, editors write, readers read. All members still need an eligible role. Activity upload credentials are not accepted. Use dedicated APIs, not generic records CRUD.

The server issues project/document UUIDs. `key` is a stable identifier, 1–100 letters, digits, underscores, dots, colons or hyphens, unique per project and kind. Project keys are deployment-wide unique.

## Routes after `project-context/`

| Method | Path | Purpose |
| --- | --- | --- |
| GET / POST | `projects` | List / create projects |
| GET / PATCH | `projects/<pid>` | Read / update project |
| GET / POST | `projects/<pid>/<kind>` | List / create documents |
| GET / PATCH | `projects/<pid>/<kind>/<id>` | Read / update document; handoffs reject PATCH |
| POST | `projects/<pid>/requirements/<id>/publish` | Publish effective specification |
| GET | `projects/<pid>/<kind>/<id>/history` | Immutable revisions; project history uses kind `projects`, id `<pid>` |
| GET | `projects/<pid>/context?requirement_id=<id>` | Effective development context |
| GET | `projects/<pid>/discovery?include_core=true` | Read-only candidates; core flag is optional |
| GET | `projects/<pid>/export?format=json` | Current snapshot; supports `json` / `markdown` |

Kinds: `requirements`, `resources`, `handoffs`. Lists return `{data: [...summaries], next_cursor}`; single reads/writes return `{data: document}`. Read details before updates: lists omit large bodies.

List filters: `q` (key/title/summary, max 80), `type` (resource type), `plugin`, `requirement_id` (resources/handoffs), `depends_on` (reverse resource links), `include_archived=true`. Use `limit` 1–100 (default 50) and opaque `cursor`, keeping filters unchanged. History limit 1–30 (default 10).

## Writes

Create:

```json
{"key":"REQ-001","reason":"User requested order management","data":{"title":"Order management","requirements_md":"Create valid orders.","design_md":"Reuse the order API.","acceptance":[{"id":"AC-01","text":"A valid order persists."}],"work_status":"planned"}}
```

PATCH merges intended data fields; arrays and `details` replace the whole value:

```json
{"version":1,"reason":"Clarified validation","data":{"design_md":"Reject incomplete orders before storage."}}
```

Publish:

```json
{"version":2,"reason":"User confirmed scope and acceptance"}
```

Every change, including publication, increments `version` and stores actor, reason, time and an immutable revision. Publish requires requirements text and acceptance criteria. Later specification edits become drafts while `published.data` and `published.version` preserve the effective baseline. Progress-only edits do not unpublish. `archived: true` hides documents by default; it does not delete them.

409: conflict/reused key with changed content; reread and merge. Identical create retries by the same owner return the existing document. After an uncertain response, read back before retrying. 400: invalid input; 401: auth; 403: role/project access; 404: missing or wrong-project ID; 405: handoff edit; 413: size limits; 503: storage unavailable.

## Data fields

Common: required `title` (max 180), `summary` (2000), `archived` boolean. Unknown fields are rejected. Markdown fields max 16000 characters; normalized documents max 96 KiB; request max 128 KiB. Label/ID arrays max 100 entries, each max 240 characters. Never store credentials.

- Projects: `constraints_md`, `plugins`, `repositories`, `readers`, `editors`. Membership lists contain account IDs, not role names.
- Requirements: `requirements_md`, `design_md`, `decisions_md`, `open_questions_md`, `acceptance` (unique `{id,text}` entries), `work_status`: `planned`, `in_progress`, `blocked`, `implemented`, `verified`. Server-owned `spec_status`: `draft` / `approved`. Editing verified specifications returns work status to `implemented` for revalidation.
- Resources: `resource_type`: `api`, `page`, `schedule`, `role`, `schema`; `plugin`, `location`, `status`: `planned`, `created`, `verified`, `needs_review`, `retired`; `design_md`, `details` object, `requirement_ids`, `related_resource_ids`, `observed_at`, `evidence`. References must exist in the same project. Related resource IDs mean this resource uses/depends on them; `depends_on=<id>` finds dependents. Verified records require a past ISO timestamp with timezone and evidence; contract changes without fresh observation become `needs_review`.
- Handoffs: `requirement_id` and `requirement_version` together, or neither for project-wide work; `run_id`, `completed_md`, `validation_md`, `remaining_md`, `blockers_md`, `next_steps_md`, `resource_ids`. Supply at least validation or next steps. Use the committed requirement version actually used; it can be a draft for design work, which does not prove release acceptance. Handoffs cannot be rewritten.

Suggested resource details: APIs have methods, inputs, outputs, errors and roles; pages have menu, workflow and roles; schedules have trigger, timezone, module, enabled and retry behavior; roles have responsibilities, page/API permissions and data scope; schemas have collection, fields, indexes and relationships. Link API/page/data dependencies with resource IDs. Recording metadata never executes or grants anything.

## Context, discovery, export

Context returns project conventions, effective requirements, separately listed unpublished requirements, resource summaries and five latest relevant handoffs. With `requirement_id`, return its full effective specification; otherwise requirement summaries include acceptance criteria. `has_more` identifies omissions; use paginated lists/details. `context_version` hashes the returned `document_revisions`; it is not a global transaction/repository revision. Recheck relevant versions before writing.

Discovery reads plugin code metadata and FAP definitions. Core opt-in adds Flask routes, loaded schemas, registered scheduler jobs and project-context developer roles. It never imports Extra Code, runs Initial code, tests side effects, changes roles or retires missing entries. Results are bounded with warnings. Review a candidate, then POST its `key`/`data`; read existing records before merging new observations with PATCH.

Export includes current heads, effective snapshots and handoffs (including archived). It omits full revision history. Limits: 1000 documents / 8 MiB. Use paginated APIs/history for larger projects and MongoDB backups for full recovery. Knowledge has no TTL; activity details retain the existing 90-day policy.
