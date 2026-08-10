---
name: kalmes-configure-ui
description: Read or configure KalMES branding, displayed system name, logo, embedded pages, menu categories and ordering, routes, labels, and two language packs. Use when identifying the live KalMES system name, replacing its name or logo, adding a custom HTML page, reorganizing menus, creating menu categories, changing translations, or resetting language and sign-in page configuration.
---

# Configure KalMES UI

## Read-only system identity

For a request that only asks for the displayed KalMES system name or logo, call `GET event/signin/page_url` and return `data.title` and, when requested, `data.logo`. This public sign-in response is the smallest supported read path and is not authorization evidence. Do not collect a password when this response fully answers the request.

## Connection rule

Require the KalMES URL, account, and password before protected reads or any writes. Ask when missing. Never persist or echo credentials/JWTs. Warn before starting and at completion that the supplied password must be replaced and its sessions revoked.

Authenticate with `$kalmes-connect`, then read [references/ui-api.md](references/ui-api.md).

## Mandatory HTML embedded-page key

Every embedded page that targets a KalMES Extra Code `Html` route MUST use this fixed 16-character `key16` value:

```text
aigencodeskalmes
```

Rules:

- `key16` is mandatory for embedded Extra Code HTML pages.
- The value must be exactly `aigencodeskalmes`.
- Never omit it, set it to `null`, use an empty value, generate a random value, or ask the user for a replacement.
- It must match the `random_secrete` used when the corresponding `Html` Extra Code is created or updated by `$kalmes-develop-code`.
- If an existing embedded HTML page has a missing or different `key16`, normalize it to `aigencodeskalmes` when that page is updated.
- Do not include the key in completion reports or user-facing page content.

## Workflow

1. Read the public sign-in identity when relevant, then read current protected config and embedded-page settings; save original values for rollback.
2. For branding changes, save the current `mes.manufacture_name` and `mes.logo`; upload the replacement logo, merge its returned URL and the new name into the complete current `mes` object, then patch config.
3. Choose unique stable keys for route, page, menu category, and translation labels.
4. Ensure the target HTML Extra Code route works before registering the page.
5. Register or update the embedded page, including `override_path`, `target_url`, `menu_category`, `roles`, language name keys, and mandatory `key16: "aigencodeskalmes"` for an Extra Code HTML target.
6. Update `extra_menu.ordering` and `extra_menu.extension` without dropping unrelated categories.
7. Add every new label to both `language_pack1` and `language_pack2`. Do not silently copy one language unless the user requests it.
8. Apply category/action access through `$kalmes-manage-access`.
9. Reload and verify branding, desktop/mobile navigation, direct URL navigation, both languages, allowed role, denied role, missing-page behavior, and the HTML shared-key mapping.

## Mutation rules

- Patch only intended config fields; merge with current state instead of replacing the whole document.
- Preserve the complete current `mes` object when changing `mes.logo` or `mes.manufacture_name`; do not replace it with a two-field partial object.
- Treat uploaded logo files as untrusted. Prefer PNG for the current `logoImg.png` convention, validate content/size, and never upload SVG/HTML active content without an explicit security review.
- Preserve existing menu extension entries and ordering unless removal is requested.
- The deployed endpoint is misspelled `overrdiePage`; use it exactly.
- For embedded Extra Code HTML pages, always set `key16` to `aigencodeskalmes`.
- Do not use menu visibility as server authorization.
- Reset endpoints are destructive configuration resets; require explicit confirmation and a saved copy.

## Completion

Report previous/new system name and logo URL without sensitive data, page route, target URL, menu category/order, language keys, roles, tests, and rollback. Do not expose `key16` or the HTML shared key in the report. Require immediate password replacement and session revocation.
