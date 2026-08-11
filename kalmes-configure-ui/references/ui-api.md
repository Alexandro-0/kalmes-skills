# UI, menu, and language API

## Contents

1. Config
2. Branding: system name and logo
3. Menu structure
4. Embedded pages
5. Languages

## Config

```text
GET   base/config
GET   base/config/<config_id>
PATCH base/config/<config_id>
PATCH base/config/<config_id>?skip_reset_unix=true
PATCH base/config/<config_id>/embedded/<key>
```

Use a Bearer JWT. Current config list responses may contain encrypted `enc_val` intended for the frontend. When operating through a signed-in browser, reuse its supported config path; do not guess decryption material.

## Branding: system name and logo

The displayed system name is `config.mes.manufacture_name`. The active logo resource URL is `config.mes.logo`. Do not confuse the system name with `language_pack1.mes` or `language_pack2.mes`, and do not confuse the logo with `theme.header_icon`, which is a header color/value in the current UI.

For a display-only identity lookup, use:

```http
GET {BASE}event/signin/page_url
```

Read `data.title` as the displayed system name and `data.logo` as the active logo reference. This endpoint does not expose the complete config and does not authorize a subsequent write.

### Inputs and backup

Before changing branding, require:

- the desired system name;
- a logo image when replacing the logo;
- confirmation of the target environment.

Read the current config and preserve the complete `mes` object, especially the previous `manufacture_name` and `logo`. A URL/password/account is mandatory under the parent skill's connection rule. Do not download or upload branding through an unauthenticated legacy path.

### Upload the logo

Use the resource endpoint with a Bearer JWT:

```http
POST {BASE}event/files
Authorization: Bearer <JWT>
Content-Type: multipart/form-data

file=<image bytes; filename="logoImg.png">
```

The current frontend renames the selected file to `logoImg.png`. The backend config-pack export also identifies the system logo resource by that name. Prefer a valid PNG, preserve aspect ratio and transparency as required, and validate file signature, size, and rendering because the backend's upload validation is limited.

Typical response:

```json
{
  "status": true,
  "message": "Upload success",
  "data": {
    "urls": [
      {
        "url": "event/files/GENERATED_FILENAME.png",
        "filename": "logoImg.png"
      }
    ]
  }
}
```

Use `data.urls[0].url` as the new `mes.logo`. Record the returned resource ID/URL so an orphan upload can be cleaned up by exact identity if the config patch fails.

### Patch branding

Merge changes into the complete current `mes` object, then patch config:

```http
PATCH {BASE}base/config/<config_id>?skip_reset_unix=true
Authorization: Bearer <JWT>
Content-Type: application/json
```

Conceptual body:

```json
{
  "mes": {
    "manufacture_type": "EXISTING_VALUE",
    "manufacture_name": "New System Name",
    "logo": "event/files/GENERATED_FILENAME.png",
    "other_existing_mes_fields": "PRESERVE_THEM"
  }
}
```

Do not send a literal placeholder or replace `mes` with only `manufacture_name` and `logo`. If changing only the name, keep the current logo. To restore the built-in fallback logo, set `mes.logo` to `null`; this changes the reference but does not automatically delete the uploaded resource.

### Verify branding

Check the public sign-in configuration response without treating it as authorization evidence:

```http
GET {BASE}event/signin/page_url
```

Expected branding fields:

```json
{
  "data": {
    "logo": "event/files/GENERATED_FILENAME.png",
    "title": "New System Name"
  }
}
```

Then verify in an authenticated browser:

- sign-in page or sign-in modal logo and title;
- Navbar/sidebar and default-page logo;
- displayed system name and browser document title;
- browser favicon, which also uses the configured logo in current pages;
- desktop and mobile rendering, transparent background, aspect ratio, and cache refresh.

If the new value is stale, reload supported config state and browser cache before repeating mutations. Do not upload duplicate files as a cache workaround.

### Roll back branding

Patch the saved complete `mes` object or at least its verified previous `manufacture_name` and `logo` while preserving all other fields. Re-run the sign-in response and authenticated UI checks. Delete a newly uploaded orphan resource only by exact ID/URL, only when the user authorizes deletion, and only after confirming no config or page references it.

## Menu structure

Relevant config shape:

```json
{
  "extra_menu": {
    "ordering": [
      "data",
      "manufacture",
      "iot_center",
      "custom-category"
    ],
    "extension": [
      {
        "key": "custom-category",
        "title": "Custom Category",
        "defaultActive": true
      }
    ]
  }
}
```

Built-in and deployment-specific category keys must be discovered. Preserve all unrelated entries when patching.

## Embedded pages

```text
GET  event/overrdiePage
POST event/overrdiePage
POST event/batchPostEmbeddedPage
```

The misspelling `overrdiePage` is part of the contract.

For every embedded page whose `target_url` points to a Kalmes Extra Code HTML preview route, `key16` is mandatory and must use the same fixed 16-character value used by the Extra Code HTML metadata:

```text
aigencodeskalmes
```

Typical page body:

```json
{
  "name_key": "maintenancePage",
  "override_path": "/maintenance",
  "target_url": "/api/extracode/html/preview/MaintenanceHtml",
  "roles": ["Maintenance"],
  "menu_category": "maintenance",
  "key16": "aigencodeskalmes",
  "index": 10
}
```

Mandatory rules for Extra Code HTML embedded pages:

- Always send `"key16": "aigencodeskalmes"` when creating or updating the embedded-page record.
- Never treat `key16` as optional for a Kalmes Extra Code HTML target.
- Never send `null`, an empty string, `OPTIONAL_HTML_SHARED_SECRET`, or a random/generated value.
- `key16` must match the corresponding Extra Code HTML `random_secrete`, which is also fixed to `aigencodeskalmes`.
- If the existing page has a missing or different `key16`, normalize it to `aigencodeskalmes` during the requested update.
- Do not expose `key16` in reports or user-facing HTML content.

Determine whether `roles` is an allow-list for the target deployment and test both access outcomes.

## Languages

Update both packs in one controlled config patch:

```json
{
  "language_pack1": {
    "maintenancePage": "設備保養"
  },
  "language_pack2": {
    "maintenancePage": "Maintenance"
  }
}
```

Merge keys into current packs; do not replace the entire dictionaries with a partial object unless the endpoint performs a verified deep merge.

Reset default language pack:

```text
POST event/language/resetDefault
{}
```

Reset sign-in override:

```text
POST event/signin/resetPage
{}
```

Both resets require confirmation and a rollback copy.
