---
name: kalmes-manage-access
description: Manage Kalmes users, built-in and custom roles, account role assignments, menu category denial, action/path denial, and embedded-page roles. Use when creating or changing users, assigning roles, restricting a Kalmes feature, reviewing permissions, resetting a user password, or validating allowed and denied access.
---

# Manage Kalmes Access

## Mandatory credentials and safety

Require the Kalmes URL and an API key (preferred) or account/password fallback before live operations. Ask for an API key first when authentication is missing. Use a least-privilege eligible administrator binding where possible. Never persist or echo credentials, new passwords, JWTs, session IDs, or sensitive claims. Only when password fallback is used, tell the user before starting and at handoff to replace the supplied password and revoke its sessions.

Account creation, role elevation, password reset, account deletion, and global logout are sensitive. Require explicit intent, identify the target account, show the intended role change, and verify the acting account is authorized. Never rely on the fact that a legacy route is publicly callable.

Read [references/access-api.md](references/access-api.md).

## Access workflow

1. Authenticate with `$kalmes-connect` and record the acting role without exposing tokens.
2. Read current config, role list, target account, menu denial maps, action denial list, and embedded-page roles.
3. Build an access matrix of role by category by path/API operation.
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
