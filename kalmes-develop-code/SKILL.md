---
name: kalmes-develop-code
description: Read, create, edit, run, version, and integrate Kalmes Extra Code for Python APIs, FAP data modules, single-file HTML pages, initialization and scheduled jobs, and reusable Python modules. Use when a user asks external Codex to read Kalmes source by exact filename, implement or modify a Kalmes API or HTML page, follow FAP API or HTML conventions, create a schedule, run Initial code, build an integration, or maintain shared server modules.
---
# Develop Kalmes Code

Operate through authenticated HTTP endpoints and repository files available to Codex. Do not depend on the web Agent's internal `CreateApiSourceCode`, `CreateHtmlSourceCode`, `CreateRunnableCode`, `RunScheduler`, or `readSourceCode` tools.

## Mandatory safety gate

For local source work, use the repository and local checks. For protected source reads or changes, reuse the authenticated session for the same target and account. If missing, use `$kalmes-connect` with the URL, environment and an API key (preferred) or password fallback. Never persist or echo credentials, tokens, environment secrets or source containing secrets.

Creating, uploading, or running Extra Code is remote code execution. Inspect current source and versions first. On production, show the intended filenames, types, routes, side effects, dependencies, job IDs, tests, and rollback before the first write or run.

## Select a code type

- `API`: request/response logic exposed through `extracode/<name>`.
- `Html`: a single-file HTML/CSS/JavaScript page rendered by the HTML preview route.
- `Initial`: explicit/startup initialization and scheduler registration.
- `Others`: importable shared Python module with no route by default.

Consult [references/code-api.md](references/code-api.md) for the relevant source lifecycle or runtime contract when using those endpoints.

## Required Python API import path

Every Python Extra Code item of type `API` must include this setup at module scope, before importing any Kalmes Extra Code modules, even if the API currently uses none.

```python
import sys
sys.path.append('./extraCode')
```

Before saving a new or edited API, verify that the setup is present and uncommented. Add it if missing and reuse existing setup to avoid duplicates.

## Mandatory HTML shared secret

Every create or update operation for an Extra Code item whose type is `Html` MUST use the fixed 16-character HTML shared secret:

```text
aigencodeskalmes
```

Rules:

- The value is exactly `aigencodeskalmes` and is exactly 16 ASCII characters.
- Never omit it for an `Html` create or update.
- Never send `null`, an empty string, a placeholder, a generated random value, or a user-invented replacement.
- Do not ask the user to provide this value; use the fixed value defined by this skill.
- On `POST extraCode/code` for a new `Html` item, send it as `random_secrete`.
- On `POST extraCode/upload/<filename>?manual=1` when saving or updating `Html` source, send the source together with `random_secrete`.
- If an existing `Html` metadata record has no shared secret or has a different value, normalize it to `aigencodeskalmes` as part of the requested HTML update using the supported metadata/source write path.
- When the HTML is registered as an embedded Kalmes page through `$kalmes-configure-ui`, its `key16` MUST use the same `aigencodeskalmes` value.
- This fixed HTML routing key is part of the Kalmes HTML contract. Do not embed it into the HTML/JavaScript source itself unless a separate backend contract explicitly requires that.

## Read source only

When the user asks only to read Kalmes source:

1. Require the exact filename including extension; ask only when it cannot be discovered from source metadata.
2. Resolve its plugin/folder from `extracode/codeuploader`.
3. Call `GET extraCode/live/<filename>?plugin=<folder>` with the Bearer JWT.
4. Return or save the requested content without analyzing, editing, uploading, or running it unless asked.

## Development workflow

1. For a local fix to an existing file, inspect its source and affected dependencies, apply the relevant type-specific requirements above, then verify syntax and the changed behavior locally. For an API import-path fix, check the module-level setup, import order and affected import. Finish after these checks unless live work was requested. For a live edit, retain the current source/version for rollback. Query metadata only if the filename, plugin or target is unresolved.
2. If the change depends on FAP fields or relationships, inspect only the definitions needed with `$kalmes-manage-fap`.
3. For FAP-backed APIs and collection modules, read [references/fap-api.md](references/fap-api.md). Use the API contract in code-api.md for ordinary Python APIs.
4. For a single-file FAP HTML page, read [references/fap-html.md](references/fap-html.md).
5. For a scheduled task, read [references/scheduler.md](references/scheduler.md).
6. For a new item, create from a supported template or upload a file. For edits, update the existing source. Keep API, Html and Initial filenames ending in `.py` in source metadata while route names omit `.py`. For `Html`, apply the mandatory shared-secret rule above.
7. Preserve the documented `invoke` contract, validation and explicit authorization when editing. Implement and test them for new or changed operations. Never rely on menu visibility or an internal tool's injected identity.
8. Keep credentials and environment secrets in the protected Kalmes environment facility, not source. The fixed HTML routing key defined above is supplied through the HTML metadata/write contract and must not be copied into static HTML.
9. For local edits, check syntax and exercise the changed behavior locally. For an authorized live edit, save, read back the source, and verify the affected runtime behavior in non-production. Never run Initial merely to syntax-check it.
10. Select tests by what changed. For an import-path fix, verify the module-level setup and import order and exercise the affected import. For input changes test malformed input, for access changes test allowed and denied roles, and for side effects or dependencies test failure and safe repeat. Use the applicable release matrix for deployments.
11. Preserve the prior version and document rollback. Register user-facing HTML with `$kalmes-configure-ui`.

When registering HTML, pass the exact filename stem as the embedded page's `name_key` and preview module name, preserving case: `FeatureHtml.py` -> `FeatureHtml`. Use that same key in both language packs. The current plugin exporter compares `name_key` to the code filename without `.py`; independently choosing a camelCase page key can silently omit its settings from exports. Verify this mapping after registration, not just that the page loads.

## FAP feature sequence

For a new plugin-scoped FAP feature:

1. establish the plugin code;
2. create or locate all definitions with `$kalmes-manage-fap`;
3. identify parent, child, reference, and embedded modules;
4. create API modules before HTML that calls them;
5. create master and detail APIs/pages together when a sheet relationship is present;
6. update both language packs and register only top-level pages in a menu;
7. report definitions, created/edited code, and reused module names.

## Completion

Report plugin code, filenames, types, runtime routes, collection/module dependencies, job IDs, tests, versions, and rollback without including source secrets or the HTML shared key. Require immediate password replacement and session revocation only if password fallback was used.
