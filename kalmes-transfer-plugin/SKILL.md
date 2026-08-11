---
name: kalmes-transfer-plugin
description: Export Kalmes plugin components into a portable .tar pack and safely preflight, import, upgrade, verify, and roll back plain or device-bound encrypted plugin packs through authenticated APIs. Use when a user asks to export, download, package, inspect, install, import, upload, migrate, or upgrade a Kalmes plugin tar; move a plugin between Kalmes environments; or diagnose a plugin pack format or import failure.
---

# Transfer Kalmes Plugin Packs

Use the authenticated Kalmes plugin-pack APIs for portable Extra Code releases. Do not confuse a plugin pack with a full config pack or a Docker image tar.

## Connection and safety gate

Require the Kalmes API URL, target environment, and an API key (preferred) or account/password fallback. Authenticate with `$kalmes-connect`; never persist or echo credentials or JWTs.

For export, also require the intended plugin name, immutable version, exact code/FAP/ENV scope, and a secure local output path. For import, require the tar path, whether it is plain or device-bound encrypted, and the expected plugin/version.

Treat import as a high-impact mutation. It can overwrite code and metadata, merge ENV/UI/language/access/FAP definitions, and automatically execute every packaged `Initial` module. It is not transactional and may partially succeed. Before upload, inventory collisions, back up every affected object, state the exact target and changes, and obtain explicit confirmation immediately before the mutation. Never upload a tar merely to inspect it.

Read [references/plugin-pack-api.md](references/plugin-pack-api.md) before exporting or importing. Use `$kalmes-test-release` for acceptance and rollback testing.

## Choose the operation

- Export a plain portable pack: `POST event/plugin/pack` with JSON; save the binary response.
- Import or upgrade a plain pack: `POST extracode/pluginPack` with multipart field `file`.
- Import a device-bound encrypted pack: `POST event/activenpg` with multipart field `file` only when it was prepared for the target installation.
- Do not use `event/config/pack` for plugins. Do not use the manager-only `event/dvenpg` encryption workflow unless the user explicitly requests that separate distribution process and its server-side source tar is available.

## Preflight a plain tar

Run the bundled inspector before any import and after every export:

```text
python scripts/inspect_plugin_tar.py <plugin.tar>
```

The inspector reads without extracting. Stop on an invalid archive, unsafe member, ambiguous plugin root, invalid UTF-8/JSON metadata, missing declared file, duplicate path, size-limit violation, or missing required metadata. Review warnings, especially `flat=true`, unknown code types, unlisted files, and packaged `Initial` modules.

For an encrypted pack, do not claim that plain-tar inspection passed. Verify its trusted origin, checksum, expected plugin/version, and target installation binding through an approved channel.

## Export workflow

1. Authenticate, call `ping`, identify the source environment, and inventory active Extra Code metadata, source folders, FAP definition IDs, and ENV names.
2. Use a stable ASCII `name` and immutable `version` containing only letters, digits, dots, underscores, or hyphens. Reject separators, traversal text, or a reused release version.
3. Select a non-empty `resources` list with each current metadata `id`, exact filename, and source `plugin` folder. Select FAP definitions by ID. Package ENV names with non-secret examples only; the exporter does not copy current ENV values.
4. Prefer `flat=false` so files install under a versioned plugin folder. Use `flat=true` only for a verified legacy requirement because it writes directly into the shared `extraCode` directory. Set `expose` deliberately.
5. Submit the manifest to `POST event/plugin/pack`. Require a successful binary response; preserve the server filename when available and calculate a SHA-256 checksum.
6. Run `inspect_plugin_tar.py`. Confirm `meta.json` matches the requested name/version/scope and that every selected code file is both declared and present.
7. Store the tar and checksum in the approved release location. Do not treat the pack as a backup of business data, arbitrary resources, ENV secrets, or complete system config.

## Import workflow

1. Preflight the plain tar locally. Record its SHA-256, plugin name/version, `flat`, `expose`, code files/types, ENV names, FAP collections, UI/language keys, and all `Initial` files. For encrypted tar, record equivalent trusted release metadata without attempting ordinary tar inspection.
2. Authenticate and inventory the target. Back up matching code metadata/source/versions, ENV records, embedded pages, affected config language/menu/access fields, FAP definitions, scheduler/job state, and any data needed to reverse `Initial` effects.
3. Produce a collision and change plan. Remember that importing updates or inserts declared objects but does not remove obsolete objects from an older release.
4. Run non-production compatibility tests. Immediately before upload, identify the target environment, checksum, plugin/version, collisions, automatic `Initial` execution, backup, and rollback plan; obtain explicit confirmation.
5. Upload exactly one lowercase `.tar` file in multipart field `file` to the correct plain or encrypted endpoint. Do not blindly retry a timeout or ambiguous result because the first request may have written data and executed `Initial` code.
6. Evaluate both HTTP status and response body. HTTP 200 alone is insufficient; an invalid extension can return a failure body with 200, while successful imports normally return `Plugin Upgrade Success!` and may list ENV values requiring configuration.
7. Read back and verify every code file and metadata record, HTML `key16` contract, ENV, embedded page, language key, menu/access rule, and FAP definition. Configure required ENV values through the approved secret path.
8. Verify `Initial` side effects and logs independently; its exception can be logged without making the overall import response fail. Run allowed/denied API tests, page tests, job-duplication checks, and old-feature smoke tests.
9. On failure, stop further execution and restore in dependency order with `$kalmes-test-release`. Never improvise deletion of partially imported objects without exact IDs and verified backups.

## Completion

Report the operation, source and target environments, plugin/version, plain or encrypted mode, filename, size, SHA-256, included or affected resources, preflight result, confirmation, HTTP result, read-back tests, `Initial` verification, required ENV follow-up, rollback material, and unresolved risks. Never include secrets, JWTs, ENV values, or sensitive source.
