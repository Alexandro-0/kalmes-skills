---
name: kalmes-test-release
description: Verify, package, release, monitor, and roll back KalMES custom features, including FAP definitions, Extra Code APIs and HTML, data, schedules, menus, languages, roles, files, source versions, config packs, and plugin packs. Use before or after deploying a KalMES feature, diagnosing a failed release, preparing a plugin, or proving acceptance and recovery.
---

# Test and Release KalMES Features

## Connection gate

Require the KalMES URL, account, and password before live tests or release operations. Ask for missing values and identify the environment. Never persist or echo credentials, JWTs, source secrets, plugin secrets, or config encryption material. Tell the user before work and at handoff to replace the supplied password and revoke its sessions.

Production releases, plugin activation, config import, code execution, data cleanup, and rollback are high impact. Require an approved change set, backup, maintenance expectations, and explicit confirmation immediately before the high-impact mutation.

Read [references/test-release.md](references/test-release.md).

## Verification workflow

1. Authenticate with `$kalmes-connect`; verify `ping` readiness and license prerequisites.
2. Inventory and back up affected FAP definitions and backing data, config, embedded pages, code source/versions, records, resource IDs, roles, menu keys, and job IDs.
3. Test code syntax/contract in non-production, then run API and HTML contract tests.
4. Test data validation, idempotency, pagination, files, external dependency failure, and safe retry.
5. Test allowed and denied accounts by direct endpoint and page navigation.
6. Test scheduler registration twice, execution behavior, misfire/retry assumptions, and duplicate prevention. When available, verify through `GET extracode/kalmesSchedulerApi`; do not claim cancel/restart coverage unless its PATCH behavior is deployed and tested.
7. Release the smallest reversible unit. Re-read state after each write.
8. Perform smoke tests and capture non-secret evidence.
9. Exercise or dry-run rollback, then document exact restoration order.

## Release gate

Do not approve production release when any applicable item lacks evidence: server-side authorization, invalid-input handling, secret handling, backup, rollback, job idempotency, two-language labels, direct-route access control, dependency timeout, or post-release smoke test.

## Completion

Return a concise release record: environment, versions, changed IDs/routes, test matrix, results, remaining risks, monitoring, and rollback. Never include secrets. Require immediate replacement of the supplied password and session revocation.
