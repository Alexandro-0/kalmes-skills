---
name: kalmes-build-software
description: Build complete plugin-scoped software features inside an existing Kalmes system by coordinating authentication, FAP collection definitions, data, Python APIs, single-file HTML pages, jobs, modules, files, email, branding, menus, translations, roles, testing, packaging, and rollback. Use when a user asks Codex outside Kalmes to implement an end-to-end Kalmes application, FAP workflow, dashboard, integration, plugin, web feature, or MES extension rather than one isolated change.
---

# Build Kalmes Software

Treat a feature as complete only when its data, behavior, UI, access, verification, and recovery path are all addressed.

## Mandatory connection gate

Before reading or changing a live Kalmes system, require the user to provide:

- the Kalmes base URL ending at, or convertible to, `/<project>/api/`;
- an API key (preferred), or a Kalmes account and password fallback;
- the target environment.

If authentication is missing, ask the user to create an API key from **Advanced Settings → API Keys** or **API Access → API Keys**, depending on the manager role, before offering account/password fallback. Recommend the least-privilege eligible bound account. Never write credentials or tokens into repository files, skill files, command history, logs, source code, reports, or final responses. Keep them only in process memory or a protected temporary environment variable when a tool requires it.

Only when password fallback is used, tell the user before starting that they must replace it after the operation. At handoff repeat: **Immediately change the password supplied for this operation and revoke or end its active sessions.** If a temporary API key was used, recommend revocation when it is no longer needed.

## Workflow

1. Confirm the URL, API key or fallback account/password, target environment, requested behavior, roles, and acceptance criteria. Establish a stable ASCII plugin code; preserve the user's existing plugin code when continuing prior work.
2. Connect with `$kalmes-connect`; call `ping`, prefer `login/api-key`, and retain the JWT without exposing it.
3. Inventory existing config, embedded pages, FAP definitions by plugin, runtime data, code names, module names, roles, and menu keys. Reuse names and structures where possible.
4. Design the feature using [references/workflow.md](references/workflow.md). Identify reversible and destructive changes.
5. Design or update FAP definitions and their parent/reference graph with `$kalmes-manage-fap`; use `$kalmes-manage-data` for runtime records and files.
6. Implement APIs, HTML, initialization jobs, schedules, and shared modules with `$kalmes-develop-code`. Exercise existing runtime modules through `$kalmes-invoke-module`.
7. If the feature sends email, operate it with `$kalmes-send-email`; use its fast path for an explicit send request and enter setup or diagnosis only when needed.
8. Configure requested system name/logo branding, register pages and menu structure, and update both language packs with `$kalmes-configure-ui`.
9. Configure accounts, roles, category denial, action denial, and page roles with `$kalmes-manage-access`.
10. Test success, validation, unauthorized, forbidden, retry, and rollback paths with `$kalmes-test-release`.
11. If the user explicitly wants the internal Kalmes Agent queue to continue work, create and run it with `$kalmes-manage-subtasks`; do not substitute that queue for ordinary Codex implementation.
12. Summarize plugin code, definitions, changed resources, endpoint/module names, roles, tests, rollback instructions, and unresolved risks. Require password replacement and session revocation only when password fallback was used.

## Change discipline

- Inspect before mutating. Save the current config and source version needed for rollback.
- Use stable identifiers and idempotent create-or-update behavior.
- Ask for explicit confirmation before definition retirement, deletes, account removal, collection clearing, config-pack import, plugin activation, bulk overwrite, queue execution, or production execution of arbitrary code.
- Never use UI hiding as authorization. Test the server response with allowed and denied roles.
- Do not use undocumented or apparently public sensitive routes as a shortcut around authentication.
- Do not promise arbitrary software capabilities. Stay within Kalmes extension surfaces unless the user separately authorizes repository or infrastructure changes.

## Definition of done

Require all applicable items: verified plugin code and FAP definitions, persisted data, validated API, working HTML/page, verified system name/logo branding, registered menu, two language packs, enforced roles, file handling, scheduled behavior, negative tests, version/backup, release evidence, rollback steps, and credential-rotation reminder.
