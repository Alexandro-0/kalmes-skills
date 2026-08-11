# Kalmes test, release, and rollback reference

## Test matrix

For every changed API, record method/path, acting role, request category, expected HTTP status/body, observed result, and cleanup.

Required categories:

- readiness and valid/invalid login;
- happy-path create/read/update and safe repeat;
- malformed JSON, missing field, invalid ID, duplicate, and not found;
- missing JWT, invalid JWT, allowed role, denied role, and ownership mismatch;
- file type/size/name and authorized download;
- HTML loading, API error display, translation switch, menu route, and direct URL;
- external timeout/non-2xx response;
- scheduled function repeatability and duplicate job registration;
- FAP definition round-trip, relationship integrity, backing-data preservation, and definition-retirement rollback;
- rollback restoration and removal of newly created references.

Avoid destructive tests on production. Use tagged temporary records and remove them only after verifying exact IDs.

## Source version APIs

```text
GET  extraCode/live/<filename>
POST extraCode/upload/<filename>?manual=1
GET  extracode/codeVersion/<filename>
GET  extracode/codeHistory/<history_name>
```

Capture the current source/version before upload. After upload, read it back and run contract tests. Roll back using the verified previous source rather than reconstructing it from memory.

## Config backup and import

```text
GET  event/config/pack
POST event/config/pack          multipart file
```

Config pack download is restricted to `Day1` in current server code; upload requires JWT but is a high-privilege operation. Never import merely to inspect a pack. Require explicit confirmation and verify target environment identity.

For smaller UI/access changes, save the exact original config fields and embedded-page objects instead of relying only on a full pack.

## Plugin packaging and activation

```text
POST event/plugin/pack          JSON manifest; returns tar
POST extracode/pluginPack       multipart tar
POST event/activenpg            multipart encrypted tar
```

Typical manifest fields include `name`, `version`, `resources`, `envs`, `flat`, `expose`, and `fap_ds`. Use a new immutable version, list dependencies, exclude credentials, and verify imported code, pages, menu, language, data references, and initial actions.

## Rollback order

Prefer this dependency-aware sequence:

1. Stop traffic or disable navigation to the new page.
2. Prevent new scheduled executions; use the verified `kalmesSchedulerApi` only when deployed and authorized, otherwise restore/remove the registering Initial code and restart only through the deployment's approved process.
3. Restore API/HTML/module source versions.
4. Restore embedded-page and menu/access/language config.
5. Restore data only when schema and code compatibility are established.
6. Remove newly uploaded resources and test records by exact ID if safe and requested.
7. Re-run readiness, authentication, old-feature smoke, and access tests.

## Security release notes

The repository documents legacy sensitive routes with insufficient authorization. A passing UI test is not a security test. Record server-side 401/403 evidence. Do not treat public register, hard account deletion, public source download, or JWT-only high-privilege operations as acceptable policy; report and contain them.
