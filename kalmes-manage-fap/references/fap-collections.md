# FAP collection definition contract

## Contents

1. HTTP API
2. Definition shape
3. Column types
4. Relationships
5. Reserved fields and destructive behavior

## 1. HTTP API

Use the authenticated Extra Code module rather than the web Agent's internal tool:

```text
GET   extracode/dataManagementConfigApi?<filters>
GET   extracode/dataManagementConfigApi/<definition_id>
POST  extracode/dataManagementConfigApi
PATCH extracode/dataManagementConfigApi/<definition_id>
```

Useful exact filters include `collectionName=<name>` and, on deployments that store it as a queryable field, `plugin=<plugin_code>`. If plugin filtering is unsupported, request a bounded list and filter the returned `plugin` field locally. Preserve query-key spelling returned by the target deployment.

GET responses include `data`, and current implementations also include `system_roles`. Definitions may include a computed structure such as:

```json
{
  "module_name": {
    "api": {
      "data": "OrderDataApi",
      "history": "OrderHistoryApi"
    }
  }
}
```

Use returned module names with `$kalmes-invoke-module`.

## 2. Definition shape

Typical create body:

```json
{
  "collectionName": "order",
  "displayName": "訂單",
  "columns": [],
  "type": "dataflow",
  "parentWorkflow": "",
  "childrenProcedure": "",
  "languagePack": [],
  "apiPrompt": [],
  "uiPrompt": "",
  "version": "2.0+",
  "plugin": "myPlugin"
}
```

- `collectionName`: stable unique storage name.
- `displayName`: user-facing name.
- `type`: normally `dataflow` for current FAP features; legacy definitions may use `workflow` or `procedure`.
- `parentWorkflow`: parent collection name for a sheet child; otherwise empty.
- `version`: preserve the current value on edits. New definitions use `2.0+`.
- `plugin`: stable plugin ownership code.

Do not send generated `id`, timestamp, or visibility fields in a create body unless the deployment contract explicitly requires them.

## 3. Column types

Every column needs a unique `key`, `name1`, `name2`, `type`, `required`, `hidden`, `rolePermissions`, and deterministic `index`.

```json
{
  "key": "name",
  "name1": "名稱",
  "name2": "Name",
  "type": "string",
  "required": true,
  "hidden": false,
  "rolePermissions": {"r": ["Operator"], "w": ["Operator"]},
  "index": 0
}
```

Supported conventions:

- `string`: optional `unique`, `camera`, `upload`, and `signature`.
- `number`: numeric value.
- `date`: date without time.
- `select`: `list` of stable `{id, name}` options.
- `reference`: stores related record ID(s); include `foreign`, `endpoints`, `displayKey`, `displayKey2`, and `multiple`.
- `embedded`: stores a copied related document; include the same discovery/display fields and normally `multiple: false`.
- `sheet`: version `2.0+` parent-to-child navigation; include `url`.
- `redirect`: legacy parent-to-child navigation; include `redirectUrl`.

Use the related definition's returned module name or endpoint when available. Do not construct a route from memory if the deployment provides it.

## 4. Relationships

For an option relationship, use `reference` or `embedded` and create/read the foreign definition first.

For master-detail:

- create the parent and child as separate definitions;
- set the child's `parentWorkflow` to the parent's `collectionName`;
- require `foreign_id` in child record creation;
- add a `sheet` column to the version `2.0+` parent, or `redirect` only for a legacy unversioned parent;
- do not add a recursive child-to-parent navigation column;
- do not register a detail-only HTML page as a top-level menu item.

## 5. Reserved fields and destructive behavior

Runtime records may include `id`, `created_at`, `created_at_format`, `created_date`, `created_month`, `updated_at`, `updated_at_format`, and `visibility`. Only `visibility` is normally user-editable. `visibility=v` means active; `visibility=h` means hidden/retired.

Do not mutate the `dataManagement_config` backing collection through generic CRUD.

In the current `dataManagementConfigApi`, retiring a definition with:

```http
PATCH extracode/dataManagementConfigApi/<definition_id>
{"visibility":"h"}
```

can remove both the business collection and `<collectionName>_record` data before patching the definition. Treat this as a destructive delete, not a recoverable soft hide.
