# Authentication API

Let `{BASE}` be the configured KalMES API URL, normally `https://host/<project>/api/`.

## Readiness

```http
GET {BASE}ping
```

Expected fields include `message`, `ready`, and `initialization_error`. A non-ping request may return HTTP 503 with `message: service_initializing` while startup is incomplete.

## Login

```http
POST {BASE}login
Content-Type: application/json

{"account":"ACCOUNT","password":"PASSWORD"}
```

The web client may instead send `{ "enc": "..." }`; direct clients may use the documented account/password body only over verified TLS.

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
