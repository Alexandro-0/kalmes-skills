# Extra Code module HTTP contract

Let `{BASE}` be the authenticated Kalmes API root, normally `https://host/<project>/api/`.

## Route

```text
GET|POST|PATCH|DELETE {BASE}extracode/<module_name>
GET|POST|PATCH|DELETE {BASE}extracode/<module_name>/<resource_id>
```

Send:

```http
Authorization: Bearer <JWT>
Content-Type: application/json
```

- URL-encode every query key and value.
- Omit the resource path segment when no resource ID is needed.
- Use an empty JSON object only when the endpoint expects a body; do not invent fields.

The server calls a module shaped like:

```python
def invoke(method, query_param, data, header, resource_id=None, uid=None):
    return 200, {"message": "success", "data": {}}
```

## Discovery

Prefer a collection definition's returned:

```json
{
  "module_name": {
    "api": {
      "data": "CollectionDataApi",
      "history": "CollectionHistoryApi"
    }
  }
}
```

Some deployments also expose:

```text
GET extracode/datamng_apiGenerator?collectionName=<name>
```

Use it only when present and authorized. A 404 means the helper is unavailable, not that the collection has no API.

## Request mapping

| Internal web tool argument | External HTTP equivalent |
|---|---|
| `module_name` | route segment after `extracode/` |
| `method` | HTTP verb |
| `query_param` | URL query string |
| `payload` | JSON request body |
| `resource_id` | final route segment |
| `filter_key` | local response projection; not a standard server parameter |

For GET list operations, use server-supported `limit`, `offset`, exact field filters, and `start`/`end` intervals where documented.

## Failure handling

- `400`: correct the named request problem; do not broaden the payload.
- `401`: re-authenticate once and repeat only a read or a mutation known not to have reached the handler.
- `403`: stop and report the authorization or license boundary.
- `404`: verify the exact module name and deployed source metadata.
- `409`: report the conflict; do not overwrite automatically.
- `5xx`: preserve sanitized evidence and avoid mutation retries until side effects are known.
- Timeout after POST/PATCH/DELETE: outcome is uncertain; read current state before considering a retry.
