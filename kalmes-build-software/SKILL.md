---
name: kalmes-build-software
description: Build complete plugin-scoped software features inside an existing KalMES system by coordinating authentication, FAP collection definitions, data, Python APIs, single-file HTML pages, jobs, modules, files, email, branding, menus, translations, roles, testing, packaging, and rollback. Use when a user asks Codex outside KalMES to implement an end-to-end KalMES application, FAP workflow, dashboard, integration, plugin, web feature, or MES extension rather than one isolated change.
---

# Build KalMES Software

Treat a feature as complete only when its data, behavior, UI, access, verification, and recovery path are all addressed.

## Mandatory connection gate

Before reading or changing a live KalMES system, require the user to provide:

- the KalMES base URL ending at, or convertible to, `/<project>/api/`;
- a KalMES account;
- its password.

If any value is missing, stop live operations and ask for it. Recommend a temporary, least-privilege account. Never write credentials or tokens into repository files, skill files, command history, logs, source code, reports, or final responses. Keep them only in process memory or a temporary environment variable when a tool requires it.

Tell the user before starting that they must replace the supplied password after the operation. At handoff, always repeat: **Immediately change the password supplied for this operation and revoke or end its active sessions.** Do not claim the credential cleanup is complete unless the user confirms it.

## Workflow

1. Confirm the URL, account, password, target environment, requested behavior, roles, and acceptance criteria. Establish a stable ASCII plugin code; preserve the user's existing plugin code when continuing prior work.
2. Connect with `$kalmes-connect`; call `ping`, then `login`, and retain the JWT without exposing it.
3. Inventory existing config, embedded pages, FAP definitions by plugin, runtime data, code names, module names, roles, and menu keys. Reuse names and structures where possible.
4. Design the feature using [references/workflow.md](references/workflow.md). Identify reversible and destructive changes.
5. Design or update FAP definitions and their parent/reference graph with `$kalmes-manage-fap`; use `$kalmes-manage-data` for runtime records and files.
6. Implement APIs, HTML, initialization jobs, schedules, and shared modules with `$kalmes-develop-code`. Exercise existing runtime modules through `$kalmes-invoke-module`.
7. If the feature sends email, operate it with `$kalmes-send-email`; use its fast path for an explicit send request and enter setup or diagnosis only when needed.
8. Configure requested system name/logo branding, register pages and menu structure, and update both language packs with `$kalmes-configure-ui`.
9. Configure accounts, roles, category denial, action denial, and page roles with `$kalmes-manage-access`.
10. Test success, validation, unauthorized, forbidden, retry, and rollback paths with `$kalmes-test-release`.
11. If the user explicitly wants the internal KalMES Agent queue to continue work, create and run it with `$kalmes-manage-subtasks`; do not substitute that queue for ordinary Codex implementation.
12. Summarize plugin code, definitions, changed resources, endpoint/module names, roles, tests, rollback instructions, and unresolved risks. Require password replacement and session revocation.

## Change discipline

- Inspect before mutating. Save the current config and source version needed for rollback.
- Use stable identifiers and idempotent create-or-update behavior.
- Ask for explicit confirmation before definition retirement, deletes, account removal, collection clearing, config-pack import, plugin activation, bulk overwrite, queue execution, or production execution of arbitrary code.
- Never use UI hiding as authorization. Test the server response with allowed and denied roles.
- Do not use undocumented or apparently public sensitive routes as a shortcut around authentication.
- Do not promise arbitrary software capabilities. Stay within KalMES extension surfaces unless the user separately authorizes repository or infrastructure changes.

## Definition of done

Require all applicable items: verified plugin code and FAP definitions, persisted data, validated API, working HTML/page, verified system name/logo branding, registered menu, two language packs, enforced roles, file handling, scheduled behavior, negative tests, version/backup, release evidence, rollback steps, and credential-rotation reminder.
