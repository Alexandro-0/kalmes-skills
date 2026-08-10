---
name: kalmes-invoke-module
description: Invoke an existing KalMES Extra Code API module over authenticated HTTP with GET, POST, PATCH, or DELETE, including query parameters, payloads, resource IDs, and bounded response projection. Use when a user asks Codex outside KalMES to run or call a KalMES module, exercise a generated collection API, reproduce the internal UseModules or tool_run_api_module behavior, or interact with module-backed collection data.
---

# Invoke a KalMES Module

Translate the web Agent's internal module tool into a normal authenticated HTTP request. Never assume that `tool_run_api_module` exists in external Codex.

## Preconditions

Require the KalMES URL, account, password, target environment, exact module name, HTTP method, and intended operation. Authenticate with `$kalmes-connect`.

For module and collection discovery, read the definition with `$kalmes-manage-fap`. For request construction, read [references/module-http.md](references/module-http.md).

## Workflow

1. Resolve the exact module name from the user's request, a collection's `module_name`, an API document, or existing source metadata. Do not guess.
2. Determine the supported method, resource ID, query parameters, and payload from the module contract.
3. For `GET`, apply a limit/date range when the result may be large. Request only the needed records and project response fields locally.
4. For `POST`, `PATCH`, or `DELETE`, require explicit user intent, capture the current record when possible, and identify retry and rollback behavior.
5. Send the request to `extracode/<module_name>` or `extracode/<module_name>/<resource_id>` with the Bearer JWT.
6. Validate both HTTP status and response body. On 401, reconnect once; on 403, stop; on timeout after a mutation, report uncertainty and do not replay automatically.
7. Return the relevant data in a readable format without exposing credentials, tokens, hidden fields, or unnecessary IDs.

## Boundaries

- The internal tool's `filter_key` is not a standard KalMES HTTP parameter. Use server-supported filters and then project fields in Codex.
- Do not import or execute server Python modules in the local Codex process as a substitute for calling the target KalMES system.
- Do not use a module merely because its filename exists. Confirm it implements the API `invoke` contract and is intended to be exposed.
- Use `$kalmes-analyze-data` for multi-collection read-only analysis and `$kalmes-develop-code` when the needed module does not exist.

## Completion

Report module, method, endpoint shape, non-secret filters, status, affected or returned record count, and any uncertain side effect. If a KalMES password was supplied, require immediate replacement and session revocation.
