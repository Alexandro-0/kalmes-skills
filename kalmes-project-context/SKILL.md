---
name: kalmes-project-context
description: Read and maintain Kalmes project requirements, effective designs, API/page/schedule/role/schema inventories, revision history, and development handoffs across agent sessions. Use when resuming a project, recording requested requirements or decisions, mapping dependencies, or saving progress. Does not execute the resources it documents.
---

# Kalmes Project Context

Use the authenticated `project-context` HTTP API. Read [references/api.md](references/api.md) for contracts, payloads, filters and version rules. Reuse the target and session from `$kalmes-connect`. Activity-collector upload credentials cannot access these APIs.

## Establish context

1. Check `GET project-context/capabilities` for `protocol_version: 1`. If unsupported/unavailable, report the persistence limitation and continue independently authorized source work; do not claim synchronization.
2. Resolve a known project ID or search `project-context/projects?q=...`. Verify its repositories and plugins. URL project prefix, activity collector label, plugin code and knowledge project UUID are different identifiers. Do not create duplicate projects.
3. Get `projects/<id>/context`, preferably with `requirement_id`. Read full relevant documents by ID and follow list cursors when `has_more` is true. A partial context is not a complete inventory.
4. Preserve the requirement version and document revisions used for this run. Distinguish effective specifications, drafts and observed facts. Explicit new user instructions take precedence over stored specifications; record the change and its source.

## Record requested work

- Capture scope, design, decisions/rationale, stable acceptance IDs and open questions. Preserve the original intent; do not present an agent assumption as an accepted decision.
- Publish a specification when user instructions or the established project workflow authorize it. Existing explicit approval is sufficient; do not ask for it again. Publishing a specification does not deploy software.
- Read current content before a write. PATCH intended `data` fields with the integer `version` and a meaningful `reason`. On 409, reread and merge; never blindly retry with a newer version or overwrite another agent's changes.
- Reuse stable keys for create retries. Identical creates by the same owner return the existing document; changed content returns 409. After an uncertain response, read back by key before retrying.

## Resource inventory

Record API contracts, pages, schedules, roles and schemas with purpose, source location, plugin, requirement links and dependencies. Put type-specific contracts in `details`. Distinguish UI visibility from server authorization; recording role permissions does not grant them.

Use read-only discovery within project scope; `include_core=true` adds core registrations. Review candidates before saving. Discovery does not prove runtime behavior or completeness and never runs jobs or imports Extra Code. Inspect source and appropriate runtime APIs for missing information.

Use `planned` for designs, `created` for observed registrations and `verified` only with a timezone-bearing `observed_at` and concrete `evidence`. Use `needs_review` when uncertain. A missing result is not proof of deletion; mark known removals `retired`, preserving history. Do not store credentials or source secrets.

## Handoff

At meaningful milestones and completion, append completed work, acceptance/test results, remaining work, blockers and next steps. Include the exact requirement version used, resource IDs and the same run UUID used for activity attribution. If the specification changed during execution, record the mismatch and needed revalidation; do not relabel old evidence as verification of a new version.

Handoffs are append-only; corrections are new records. Activity details expire after 90 days, so store durable results in the handoff itself. Do not paste entire conversations or large source files.

## Integration and attribution

`$kalmes-build-software`, `$kalmes-develop-code` and `$kalmes-test-release` use this workflow when a knowledge project is in scope. Query before development, update affected resources after verification, and append a final handoff. Persist only authorized work.

Follow `$kalmes-connect` → `references/agent-activity.md`: actual agent, `X-Kalmes-Skill: kalmes-project-context`, existing run UUID and resolved plugin when applicable. Update skill on transitions; clear stale plugin labels. These labels are descriptive, not authorization.

## Completion

Report project/requirement IDs, effective/draft versions, resources, handoff ID, validation and next steps. State whether persistence succeeded. JSON/Markdown exports are current snapshots, not a second writable authority or complete historical backup.
