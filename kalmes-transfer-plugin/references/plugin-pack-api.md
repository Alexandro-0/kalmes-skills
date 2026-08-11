# Kalmes plugin tar API and format

## Contents

1. API endpoints
2. Export request
3. Plain tar layout
4. `meta.json` contract
5. Import effects
6. Responses and failure behavior
7. Verification and rollback

## 1. API endpoints

All paths are relative to the authenticated Kalmes API root and require a Bearer JWT in current server code.

```text
POST event/plugin/pack       JSON manifest; returns a plain tar
POST extracode/pluginPack    multipart field file; imports a plain tar
POST event/activenpg         multipart field file; decrypts and imports a target-bound tar
```

The current handlers check for a JWT but do not enforce a dedicated plugin-install role. Do not interpret route reachability as authorization policy. Apply least privilege, an approved change, explicit confirmation, and server-side post-verification.

`POST event/dvenpg` is a separate manager distribution path. It encrypts a tar already present in the server `ResourceFolder` using a target installation ID; it is not the normal export endpoint.

## 2. Export request

Minimum shape:

```json
{
  "name": "inventory-tools",
  "version": "1.2.0",
  "resources": [
    {
      "id": "EXTRA_CODE_METADATA_ID",
      "name": "InventoryApi.py",
      "plugin": "inventory-tools1.1.0"
    }
  ],
  "envs": [
    {
      "name": "INVENTORY_SERVICE_URL",
      "example": "https://service.example.invalid"
    }
  ],
  "flat": false,
  "expose": false,
  "fap_ds": ["FAP_DEFINITION_ID"]
}
```

`name`, `version`, and `resources` are directly indexed by the backend and are required. Treat `resources` as non-empty. `envs`, `flat`, `expose`, and `fap_ds` are optional in the handler but should be sent explicitly for a reproducible release.

For every resource, `id` selects active metadata while `name` and optional `plugin` locate the source file. A stale or mismatched ID can produce an incomplete pack. Inspect the returned archive instead of trusting HTTP success.

The server response is a binary tar with a `Content-Disposition` filename normally shaped as `<name>_<version>.tar`. Preserve the response filename when the HTTP client exposes it.

## 3. Plain tar layout

Current exports use a wrapper directory created by concatenating plugin name and version:

```text
inventory-tools1.2.0/
├── meta.json
├── files/
│   ├── InventoryApi.py
│   ├── InventoryHtml.py
│   └── InventoryInitial.py
└── resource/
```

The importer accepts `meta.json` plus `files/` at the tar root or under one deeper wrapper path. It rejects archives containing multiple candidate plugin roots. The uploaded filename does not need to match the internal wrapper name, but it must end with lowercase `.tar`.

The current importer consumes `meta.json` and `files/`. Do not assume arbitrary content under `resource/` is installed.

## 4. `meta.json` contract

Typical metadata:

```json
{
  "plugin_name": "inventory-tools",
  "version": "1.2.0",
  "flat": false,
  "expose": false,
  "menu_access": [],
  "env": [
    {"name": "INVENTORY_SERVICE_URL", "example": ""}
  ],
  "files": [
    {
      "name": "InventoryApi.py",
      "type": "API",
      "hashTag": "inventory",
      "manual": false
    }
  ],
  "override": [],
  "language_pack1": {},
  "language_pack2": {},
  "menu_forbidden_access": {},
  "fap_ds": []
}
```

- `plugin_name` and `version` form the default install folder under `extraCode`.
- `flat=true` installs files directly in shared `extraCode` and increases collision risk.
- `expose=false` marks imported code as not exposed; a missing value currently behaves as exposed.
- `env` contains names and examples, not exported live values. New target ENV records use the example as their initial value; existing values are normally preserved.
- `files` drives Extra Code metadata upsert. Each declared file must exist under `files/`.
- `override` merges embedded-page definitions and menu placement.
- `language_pack1` and `language_pack2` merge keys into target config.
- `menu_forbidden_access` merges category denial rules.
- `fap_ds` upserts FAP definitions by `collectionName`; it does not export business records.

The importer recognizes code types such as `API`, `Html`, `Others`, and `Initial`. Verify current target support. After importing HTML, verify that Extra Code metadata and embedded-page registration still use the required `aigencodeskalmes` `key16` contract.

## 5. Import effects

The plain and encrypted routes converge on the same importer after decryption. The importer can:

1. Copy or overwrite code files.
2. Insert or update Extra Code metadata by name, type, and folder.
3. Insert ENV records or reassign existing ENV records to the imported plugin, then reload ENV.
4. Insert or update embedded pages and extend menu ordering/categories.
5. Merge both language packs.
6. Insert or update FAP definitions by `collectionName`.
7. Merge category denial rules.
8. Import every `Initial` module and call parameterless `invoke()`.

There is no transaction spanning these steps. A late error can leave earlier writes in place. The importer does not remove target objects absent from the new pack, so upgrades can leave obsolete code, jobs, ENV records, pages, or definitions.

`Initial` exceptions are caught and logged inside the import loop. The endpoint can still return success, so independently verify initialization and scheduled-job side effects.

## 6. Responses and failure behavior

Plain import request:

```http
POST {BASE}extracode/pluginPack
Authorization: Bearer <JWT>
Content-Type: multipart/form-data

file=@inventory-tools_1.2.0.tar
```

Encrypted import uses the same multipart field at `{BASE}event/activenpg`. The encrypted archive must be bound to the target installation; ordinary tar inspection is not applicable before approved decryption.

Typical successful body:

```json
{"message":"Plugin Upgrade Success!"}
```

When the pack declares ENV names, success may be:

```json
{"message":"Plugin Upgrade Success! Please edit env value: ['INVENTORY_SERVICE_URL']"}
```

Important failure behavior:

- missing JWT: HTTP 401;
- no multipart file: HTTP 400;
- filename not ending in lowercase `.tar`: current routes can return HTTP 200 with `status=false`;
- unsafe or unreadable tar: HTTP 400 with a tar extraction message;
- missing or ambiguous `meta.json` plus `files/` root: HTTP 400;
- metadata/import exception: normally HTTP 400 with `format error`;
- unexpected endpoint exception: HTTP 500.

Do not retry automatically after a timeout, disconnect, or ambiguous response. Inspect target state first because earlier writes or `Initial` execution may already have occurred.

## 7. Verification and rollback

Before import, preserve exact target state for every object named in metadata:

- Extra Code metadata, source, history, folder, exposure, hash tag, and HTML key;
- ENV records and plugin ownership without placing values in reports;
- embedded-page records and affected menu/config/language/access fields;
- FAP definitions and compatibility-relevant business data;
- scheduler/job IDs and side effects expected from `Initial` modules.

After import, read all objects back and test code, APIs, pages, permissions, FAP relationships, ENV-dependent integrations, and duplicate job registration. Compare the installed state to `meta.json`, not only to the response message.

Rollback in dependency order: stop new traffic and jobs; restore code/source metadata; restore embedded-page/menu/language/access config; restore FAP definitions and compatible data; restore ENV ownership/values through the secret path; remove only newly created objects with exact verified IDs; then rerun old-feature smoke and access tests.
