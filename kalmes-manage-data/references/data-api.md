# KalMES data and file API

All routes below are relative to `{BASE}` and, except ping/public exceptions, use `Authorization: Bearer <JWT>`.

## Schema-driven base CRUD

```text
GET    base/<column>?<filters>
GET    base/<column>/<id>?<filters>
POST   base/<column>
PATCH  base/<column>/<id>
DELETE base/<column>/<id>
PATCH  base/<column>/<id>/embedded/<key>
POST   base/<column>/<id>/embedded_array/<key>
PATCH  base/<column>/<id>/embedded_array/<key>/<embedded_id>
POST   footprint/<column>/<id>
GET    versions/<column>/<id>
```

Known schema-backed columns include `account`, `assets`, `config`, `extra_code`, `iot_device`, and `resource`; deployments may add more. Inspect before use.

The `GET base/config` response is encrypted into `enc_val` for the web client. Prefer the existing KalMES client/config workflow when decoding is required; never invent a key.

## Record collections

```text
GET  records/<column>?<filters>
POST records/<column>
GET  records/iot/<column>?<filters>
```

Record POST adds the authenticated `user_id`. Use record collections for feature-owned events/history when no server schema deployment is available, but define and validate the document contract in the feature API.

## Query filters

Common filters:

```text
field=value
field=a,b,c
limit=20&offset=0
@gt.field=10
@gte.field=10
@lt.field=20
@lte.field=20
@eq.field=value
@ne.field=value
@between.field=10,20
@range.field=10,20
visibility=v
```

URL-encode keys and values. Always set a sensible limit for exploratory list operations.

## Files

General file facade:

```text
POST file                         multipart field: file
GET  file/<generated_file_name>
```

Event resource facade:

```text
POST event/files                 multipart field: file
GET  event/files/<file_name>
GET  event/files/<from_key>/<id>
```

Upload responses normally return generated URLs and original names. Treat user filenames as untrusted. Verify allowed extension, MIME, size, quota, and access at the feature layer because current backend checks are limited.

## Mutation safety

Capture the pre-change document before PATCH. For DELETE or bulk import, require explicit confirmation and export enough data for restoration. Consider endpoint success codes inconsistent across legacy handlers: validate both HTTP status and response body fields.
