# Plugin deployment and routing

Use this contract when creating a portable plugin, changing its installation mode, or diagnosing a page/API that cannot load after import. Keep the deployment choice consistent through code metadata, page registration, HTML-to-API calls, packaging, and destination verification.

## Choose the installation mode

| Concern | Shared directory | Versioned plugin directory |
| --- | --- | --- |
| Manifest | `flat=true` | `flat=false` |
| Default destination | `extraCode/<filename>` | `extraCode/<plugin_name><version>/<filename>` |
| HTML preview request | Omit this application's `plugin` parameter | Select the installed HTML folder with `plugin=<folder>` |
| Application API request | Omit `plugin` when the API is also shared | Select the installed API folder with `plugin=<folder>` |
| Upgrade concern | Same-name files can be overwritten | Existing page registrations and callers must select the intended new folder |

Prefer versioned directories for portable releases, subject to verified target support. Use shared-directory installation for a verified compatibility requirement or an explicitly chosen shared layout with reviewed collisions. Changing `flat` alone does not update existing callers or prove either mode works.

Distinguish these identifiers:

- `resources[].plugin` in an export request locates **source** code. Preserve its actual source folder even when exporting a flat destination.
- Manifest `plugin_name`, `version`, and `flat` determine the default **destination** layout. Neither the download filename nor an arbitrary tar wrapper name selects runtime code.
- Runtime `plugin` selects the installed folder of the requested module. Read back the destination metadata instead of retaining the development folder or guessing from a branded package filename.
- `expose` controls the code exposure flag independently of installation layout; it does not repair routing or replace authorization.
- Python `sys.path` affects imports after a module is selected. It does not select the initial HTML/API module for the HTTP loader. Preserve the API import-path requirement in `$kalmes-develop-code` and verify actual cross-module dependencies separately.

A development source folder may differ from the final destination. Record the chosen mode, source locations, destination folder rule, HTML target, and API dependencies before packaging. Keep version selection in verified deployment metadata/configuration rather than hard-coding a development folder into reusable source.

## Carry the folder through the complete request

For a same-package HTML/API pair in versioned mode, verify all four transitions:

1. Import installs the files and records their actual folder in code metadata.
2. The embedded page's preview target selects the HTML folder, and iframe URL assembly preserves that query parameter alongside the platform's routing/authentication parameters.
3. The HTML renderer validates and makes the necessary folder value available to its template.
4. The browser uses that value when calling the API in the same folder.

For flat mode, verify both the preview and the application API select the shared location; remove stale application folder selectors within the authorized change. Do not remove unrelated `plugin` parameters globally: platform helpers such as `MesFunctionUtils.js` may live in their own folder.

Illustrative **final HTTP paths**, with authentication omitted:

```text
# Shared HTML and API
/project/api/extracode/html/preview/DemoPortal
/project/api/extracode/DemoApi?action=state

# Both installed in demo1.2.0
/project/api/extracode/html/preview/DemoPortal?plugin=demo1.2.0
/project/api/extracode/DemoApi?action=state&plugin=demo1.2.0
```

Use the target's verified prefix and stored `target_url` convention. Its stored target may omit prefixes added by the platform; do not duplicate `/project` or `/api`. Keep `name_key`, the preview module name, language keys, and the final `override_path` segment equal to the exact HTML filename stem. Folder selection belongs in the supported query contract, not a guessed extra path segment or a renamed page key.

When HTML and API are deliberately installed in different folders, resolve their locations separately. Reusing the HTML folder for every API call is valid only for a verified same-folder dependency. Configure and validate an explicit API location through a supported renderer/configuration contract; do not invent a query option that the application does not consume. Do not forward the whole page query or credentials into API URLs.

## Verify what the importer preserves

The documented importer rebuilds `override_path` and, for newly inserted pages, `target_url`. A correct query in the exported manifest is therefore not proof of correct destination routing. Test both first installation and updating an existing page; either branch can lose a selector or retain an old one.

Use the supported code metadata/source APIs and `GET event/overrdiePage` to compare the installed folder, registered target, final iframe request, and application API request. Preserve page identity, routing-key contracts, roles and unrelated query parameters. Repair only the affected settings within scope. If the deployed importer drops required selectors, report that limitation or arrange an authorized registration update; changing the tar alone may not persist the repair.

If a correctly addressed request still cannot load, distinguish missing source, loader/compiled-source compatibility, and wrong-version cache behavior from application/data errors. Do not claim a specific platform defect from a file-not-found screenshot alone. Do not bypass unavailable APIs through runtime files, containers or databases.

The local inspector warns about missing, stale, or ambiguous page folder selectors. These are review warnings because destination importers may rewrite or inject them. `VALID` means structural checks passed; even a matching selector cannot establish renderer propagation, API availability, or destination runtime success. Do not upload a package merely to test a warning.

## Keep data and initialization separate

Versioned code folders do not automatically namespace Collection names, business keys, or existing records. A frontend-only update can depend on an already installed compatible backend; document and verify that dependency instead of assuming missing packaged FAP means missing live data.

Inspect packaged Initial modules and page startup behavior before runtime tests. Import can execute Initial modules, and opening a page can call an activation API that writes data. Use read-only metadata/source checks first, then authorized non-production tests with appropriate backups. Switching an entry point back to an old code folder does not restore schemas or data, or prove old-code compatibility with current data.

## Acceptance scenarios

Exercise the chosen mode and any conversion or dependency affected by the change; do not imply untested modes passed.

| Scenario | Required evidence |
| --- | --- |
| Flat installation | Shared metadata/source, no stale application folder query, working page and API, reviewed same-name collisions |
| Versioned first install | Destination folder selected by both preview and API; renderer preserves the selector |
| Versioned upgrade | Existing page selects the new folder and API version, with no silent fallback to an old/shared module |
| Different HTML/API folders | Each request selects its documented dependency rather than copying the HTML folder blindly |
| Broken or missing selector | Clear failure or review warning; no claim that tar structure establishes runtime readiness |
| Startup and rollback | Initialization effects accounted for; code, registration and compatible data can be restored |

For a reusable local reproduction, use a synthetic HTML page and a read-only API with no business data or Initial side effects. Report local inspection separately from live import/runtime results. The inspector regression suite can be run without a Kalmes server:

```text
python -B kalmes-transfer-plugin/scripts/test_inspect_plugin_tar.py
```
