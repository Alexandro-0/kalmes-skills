# Authentication API

Let `{BASE}` be the configured Kalmes API URL, normally `https://host/<project>/api/`.

## Readiness

```http
GET {BASE}ping
```

Expected fields include `message`, `ready`, and `initialization_error`. A non-ping request may return HTTP 503 with `message: service_initializing` while startup is incomplete.

## API key login (recommended for Agents)

Create a 64-character API key in **Advanced Settings → API Keys** (`SuperUser`, `SI`, `Reseller`, and `Day1`) or **API Access → API Keys** (`Admin` and `IT`), then bind it to a `SuperUser`, `Admin`, or `IT` account. Kalmes stores only its SHA-256 hash and shows the full key once.

```http
POST {BASE}login/api-key
Content-Type: application/json

{"api_key":"KALMES_API_KEY"}
```

The endpoint also accepts the 64-character key as a `text/plain` body. Prefer JSON for an explicit contract. A successful response includes both the raw JWT and the ready-to-use Authorization value:

```json
{
  "message": "success",
  "status": true,
  "data": {
    "uid": "ACCOUNT_UUID",
    "token": "JWT",
    "token_type": "Bearer",
    "authorization": "Bearer JWT",
    "user": {
      "id": "ACCOUNT_UUID",
      "account": "ACCOUNT",
      "role": "Admin",
      "sid": "SESSION_ID"
    }
  }
}
```

The JWT contains `auth_method=api_key`, `api_key_id`, and a masked `api_key_fingerprint`; it never contains the reusable raw API key. Kalmes rechecks the key binding during JWT validation, so revoking the key, deleting the account, or changing it to an ineligible role invalidates issued JWTs.

Never echo, log, commit, or persist the API key or returned JWT. On HTTP 401, retry the exchange at most once and then report a revoked/invalid key or ineligible account. On HTTP 402, report the license problem.

## Account/password login (fallback)

```http
POST {BASE}login
Content-Type: application/json

{"account":"ACCOUNT","password":"PASSWORD"}
```

Use this method only when the user cannot provide an API key. The web client may instead send `{ "enc": "..." }`; direct clients may use the documented account/password body only over verified TLS. After the operation, require password replacement and session revocation.

## API key administration

These management endpoints require a JWT belonging to `SuperUser`, `Admin`, `IT`, `Reseller`, or `Day1` (`SI` is the legacy internal role ID displayed as IT). `Reseller` and `Day1` may manage keys, but keys still bind only to `SuperUser`, `Admin`, or `IT` accounts:

```http
GET {BASE}api-keys
Authorization: Bearer <JWT>
```

```http
POST {BASE}api-keys
Authorization: Bearer <JWT>
Content-Type: application/json

{"account_id":"ACCOUNT_UUID","label":"Codex production agent"}
```

The create response is the only response containing `data.api_key`. Copy it directly into an approved Secret Manager.

```http
DELETE {BASE}api-keys/<KEY_UUID>
Authorization: Bearer <JWT>
```

Revocation is immediate for future exchanges and JWTs issued from that key.

Successful response shape:

```json
{
  "message": "success",
  "status": true,
  "data": {
    "uid": "ACCOUNT_UUID",
    "token": "JWT",
    "user": {
      "id": "ACCOUNT_UUID",
      "account": "ACCOUNT",
      "role": "ROLE",
      "attributes": {},
      "sid": "SESSION_ID"
    }
  }
}
```

Do not log any field above except non-sensitive role/status information.

## Session login and refresh

```http
POST {BASE}login/session
{"uid":"ACCOUNT_UUID","expire":"EXISTING_SESSION_ID"}
```

`expire` is the existing session identifier despite its name.

```http
POST {BASE}event/kmrfext
Authorization: Bearer <JWT>
{}
```

Adopt a returned replacement token when present.

## Password and session endpoints

```http
POST {BASE}reset-my-password
{"account":"ACCOUNT","old_password":"OLD","password":"NEW"}
```

```http
POST {BASE}force-reset-password
Authorization: Bearer <JWT>
{"account":"TARGET","password":"NEW"}
```

The force-reset route is intended for `SuperUser`, `Reseller`, or `Day1`. Never put old or new passwords in source control or output.

```http
POST {BASE}event/logoutAll
Authorization: Bearer <JWT>
{}
```

Current server behavior restricts logout-all to specific elevated roles. Report 403 without bypass attempts.
