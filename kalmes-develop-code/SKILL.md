---
name: kalmes-develop-code
description: Read, create, edit, run, version, and integrate Kalmes Extra Code for Python APIs, FAP data modules, single-file HTML pages, initialization and scheduled jobs, and reusable Python modules. Use when a user asks external Codex to read Kalmes source by exact filename, implement or modify a Kalmes API or HTML page, follow FAP API or HTML conventions, create a schedule, run Initial code, build an integration, or maintain shared server modules.
---
# Develop Kalmes Code

Operate through authenticated HTTP endpoints and repository files available to Codex. Do not depend on the web Agent's internal `CreateApiSourceCode`, `CreateHtmlSourceCode`, `CreateRunnableCode`, `RunScheduler`, or `readSourceCode` tools.

## Mandatory safety gate

Require the Kalmes URL, target environment, and an API key (preferred) or account/password fallback before protected source reads or changes. Ask for an API key first when authentication is missing, then authenticate with `$kalmes-connect`. Never persist or echo credentials, tokens, environment secrets, or source containing secrets.

Creating, uploading, or running Extra Code is remote code execution. Inspect current source and versions first. On production, show the intended filenames, types, routes, side effects, dependencies, job IDs, tests, and rollback before the first write or run.

## Select a code type

- `API`: request/response logic exposed through `extracode/<name>`.
- `Html`: a single-file HTML/CSS/JavaScript page rendered by the HTML preview route.
- `Initial`: explicit/startup initialization and scheduler registration.
- `Others`: importable shared Python module with no route by default.

Read [references/code-api.md](references/code-api.md) for source lifecycle and runtime endpoints.

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

1. Inventory code metadata and ensure the filename and plugin code are intentional. Read current source and version list when editing.
2. If the feature uses FAP definitions, inspect them with `$kalmes-manage-fap` before designing code.
3. For an API or collection data module, read [references/fap-api.md](references/fap-api.md).
4. For a single-file FAP HTML page, read [references/fap-html.md](references/fap-html.md).
5. For a scheduled task, read [references/scheduler.md](references/scheduler.md).
6. Create from a supported template or upload a file. Keep API, Html, and Initial filenames ending in `.py` in source metadata while route names omit `.py`. For `Html`, always apply the mandatory shared-secret rule above.
7. Implement the documented `invoke` contract, validation, and explicit authorization. Never rely on menu visibility or an internal tool's injected identity.
8. Keep credentials and environment secrets in the protected Kalmes environment facility, not source. The fixed HTML routing key defined above is supplied through the HTML metadata/write contract and must not be copied into static HTML.
9. Save source, read it back, test in non-production, then invoke the runtime route. Do not run Initial merely to syntax-check it.
10. Test success, malformed input, unauthorized, forbidden, dependency failure, retry, and repeat execution.
11. Preserve the prior version and document rollback. Register user-facing HTML with `$kalmes-configure-ui`.

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
