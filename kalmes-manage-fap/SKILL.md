---
name: kalmes-manage-fap
description: Inspect, design, create, update, and retire Kalmes FAP collection definitions, including plugin ownership, bilingual fields, role permissions, references, embedded values, and master-detail sheet relationships. Use when a user mentions FAP, Collection definitions, dataManagement_config, collection columns, collectionName, plugin schemas, sheet or redirect relationships, or asks to change the data structure behind a Kalmes feature.
---

# Manage Kalmes FAP Collections

Manage collection definitions through the authenticated Kalmes HTTP API. Do not depend on the web Agent's internal `ReadCollectionInfo` or `updateFapCollection` tools.

## Connection gate

Require the Kalmes API URL, target environment, and an API key (preferred) or account/password fallback before protected reads or writes. Ask for an API key first when authentication is missing. Authenticate with `$kalmes-connect`; never persist or echo credentials or JWTs.

Read [references/fap-collections.md](references/fap-collections.md) before designing or mutating a definition.

## Workflow

1. Determine the plugin code. Use a stable ASCII identifier. If the user is continuing an existing plugin, preserve its exact code.
2. Query definitions by exact `collectionName` or plugin before designing. Never create a duplicate `collectionName`.
3. Read every referenced, embedded, parent, and child definition needed to understand the relationship graph.
4. Retrieve `system_roles` from the definition API and create an explicit read/write matrix for each column.
5. Preserve the current `id`, `version`, `plugin`, language pack, prompts, relationships, and unrelated columns when editing.
6. Propose the definition diff. On production, obtain explicit confirmation before the first schema write.
7. Create parent, option/reference, and child definitions in dependency order. Update parent sheet/redirect columns only after the child definition exists.
8. Read every changed definition back and verify unique names, column indexes, roles, endpoints, parent links, version behavior, and plugin ownership.
9. If runtime API or HTML modules are also required, continue with `$kalmes-develop-code`. If the request concerns record values rather than definitions, use `$kalmes-manage-data`.

## Safety

- Never perform CRUD against the backing `dataManagement_config` collection through a generic data endpoint.
- Treat `PATCH {"visibility":"h"}` on a collection definition as destructive. In the current implementation it can remove the backing business collection and its `_record` history, not merely hide the definition. Require an export, exact target confirmation, and a rollback plan immediately before the call.
- Do not silently grant every role. Show the intended role matrix and preserve current restrictions unless broader access is explicitly requested.
- Never invent a related API module or page route when the deployment returns one in `module_name`, `endpoints`, `url`, or `redirectUrl`.

## Completion

Report plugin code, created or updated collection names and IDs, relationship graph, role matrix, API module names, verification results, rollback material, and any definition that could not be safely changed. Require immediate password replacement and session revocation only if password fallback was used.
