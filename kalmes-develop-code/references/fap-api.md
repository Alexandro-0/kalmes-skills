# FAP API development conventions

## Contract

An API module exposes:

```python
def invoke(method, query_param, data, header, resource_id=None, uid=None):
    return 200, {"message": "success", "data": {}}

def customize_authorization(method, query_param, data, header, resource_id=None):
    return True
```

Keep the authorization signature exact. Implement explicit allow/deny behavior and test it with allowed and denied accounts. A return value of `None` has deployment-specific behavior and must not be treated as secure authorization without verification.

## Collection-backed module

Read the definition through `$kalmes-manage-fap`. Use its `collectionName`, columns, `rolePermissions`, related modules, and language pack. Do not hard-code an unrelated sample collection.

Common `MyApiController` operations inside server code:

| Operation | Function |
|---|---|
| list | `get_primary_list` |
| interval list | `get_primary_list_interval` |
| one record | `get_primary` |
| create | `post_primary` |
| update | `patch_primary` |
| hard delete | `delete_primary` |
| remove all | `remove_primary_list` |
| embedded object update | `patch_embedded` |
| embedded array create/update | `post_embedded_array`, `patch_embedded_array` |

Validate method, IDs, payload types, required fields, uniqueness, ownership, and role permissions before calling these functions.

## Data rules

- Never accept client-provided `id` on create or update.
- Exclude hidden, password, and unauthorized columns from responses.
- On create, generate a missing unique code only when the definition and business rule require it.
- On update, prevent changes to immutable unique keys unless the requirement explicitly permits and validates them.
- Use `query_param["save_record"]` with a meaningful event type such as `create`, `edit`, or `remove` when audit history is required.
- Prefer `PATCH {"visibility":"h"}` for business-record retirement. Do not confuse this with FAP definition retirement, which can remove the entire backing collection.
- Return sanitized 4xx errors for expected failures. Do not return full tracebacks to clients in production.

## Master-detail

For a sheet child:

- require `foreign_id` on child POST;
- filter child list requests by `foreign_id`;
- verify the referenced parent exists and the caller may access it;
- return enough parent data for the detail page without recursive sheet navigation;
- create separate master and detail module names and routes.

## Save and verify

Use the source lifecycle in [code-api.md](code-api.md), not internal Agent tools. After upload:

1. read the source back;
2. call the runtime `extracode/<name>` route;
3. test GET/POST/PATCH as applicable;
4. verify unauthorized and forbidden behavior;
5. preserve the previous source version for rollback.
