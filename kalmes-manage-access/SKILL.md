---
name: kalmes-manage-access
description: Manage Kalmes users, built-in and custom roles, account role assignments, menu category denial, action/path denial, and embedded-page roles. Use when creating or changing users, assigning roles, restricting a Kalmes feature, reviewing permissions, resetting a user password, or validating allowed and denied access.
---

# Manage Kalmes Access

## Mandatory credentials and safety

Reuse the valid session for the same target and acting account. If missing, connect with `$kalmes-connect` using a least-privilege eligible administrator binding. Never persist or echo credentials, passwords, JWTs, session IDs or sensitive claims. For password fallback, require password replacement and session revocation at handoff.

Account creation, role elevation, password reset, account deletion, and global logout are sensitive. Require explicit intent, identify the target account, show the intended role change, and verify the acting account is authorized. Never rely on the fact that a legacy route is publicly callable.

Read [references/access-api.md](references/access-api.md).

## Access workflow

1. Verify the acting role for the requested operation without exposing tokens.
2. For a lookup, read the requested account or role and return the result. For a change, inspect the target and the rules that determine its effective access. Inventory all denial maps and page roles for a full permissions review.
3. Apply only the steps for the requested change. Build a role-by-operation matrix when designing or reviewing permissions.
4. Reuse a role where its business meaning fits; otherwise add a stable key to `extra_roles` and labels to both language packs.
5. Assign the account role with a targeted PATCH.
6. Configure category denial, action/path denial, and embedded-page roles. Preserve unrelated rules.
7. Test with an allowed account and a denied account. A hidden menu is not proof; direct route/API access must produce the intended 401/403 behavior.
8. Report gaps where the server enforces only JWT or frontend routing. Do not describe such controls as secure RBAC.

## Prohibited shortcuts

- Do not create arbitrary elevated accounts through the currently public `register` route without an authenticated administrative workflow and explicit request.
- Do not call `force-delete-account` as a routine delete; current code exposes it too broadly and performs a hard delete.
- Do not reveal account lists, roles, or password state beyond the requested administrative scope.
- Do not downgrade the only recovery administrator without a confirmed recovery path.

## Completion

Report the access matrix, changed account/role keys, category/path/page rules, and positive/negative tests. Require immediate password replacement and session revocation only if password fallback was used.

## Activity attribution

Activity integration requires **Kalmes 2.1.0 or later**. For Kalmes HTTP calls, including reused sessions, follow the shared attribution contract in `$kalmes-connect` → `references/agent-activity.md`: label the actual agent and skill, keep one task UUID, and include the resolved plugin when needed. For local edits in a configured checkout, follow its automatic task-context workflow and AGENTS.md; background observation and synchronization do not depend on Codex, hooks or user-run commands.
