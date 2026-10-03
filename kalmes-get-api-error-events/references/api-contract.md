# API error-events contract

## Request

`GET <API_BASE_URL>api-error-events`

Header: `Authorization: Bearer <JWT>` from the established Kalmes session.

| Parameter | Format / bounds | Default |
| --- | --- | --- |
| `start` | ISO 8601 datetime with timezone; inclusive | `end` minus 15 minutes |
| `end` | ISO 8601 datetime with timezone; inclusive | Current server time |
| `limit` | Integer 1–100 | 50 |
| `offset` | Integer 0–100000 | 0 |

`start` must not be later than `end`. Use `Z` or an explicit UTC offset. Example parameter object for a specific interval:

```json
{
  "start": "2026-10-03T18:20:00+08:00",
  "end": "2026-10-03T18:35:00+08:00",
  "limit": 50,
  "offset": 0
}
```

Pass this object through query encoding; an unescaped `+` in a URL can become a space. No server-side path/account/status/plugin filters, total count, or event-detail endpoint are defined. Full stored event details are included in each returned row.

## Success response

HTTP 200 with `Cache-Control: no-store`:

```json
{
  "data": [
    {
      "id": "event-id",
      "created_at": "2026-10-03T10:29:53.621000+00:00",
      "method": "GET",
      "path": "/kal/api/extracode/example",
      "endpoint": "extraCode.get_extra_code_by_filename",
      "source": "extracode",
      "plugin": "",
      "status_code": 500,
      "user_id": null,
      "account": null,
      "message": "division by zero",
      "exceptions": [
        {
          "type": "ZeroDivisionError",
          "message": "division by zero",
          "stack": "Traceback (most recent call last):\n  ...\nZeroDivisionError: division by zero\n"
        }
      ]
    }
  ],
  "has_more": false,
  "start": "2026-10-03T10:20:00+00:00",
  "end": "2026-10-03T10:35:00+00:00"
}
```

There is no required top-level `status` or `message` on success. Records are sorted by `created_at` descending, then ID descending. Datetimes are returned in UTC. Freeze the effective response bounds when paging so the default moving window does not change between requests. Offset pagination is not a transactional snapshot; concurrent late inserts may shift rows. Deduplicate IDs and qualify results when that matters.

`source` is `extracode` for the Extra Code blueprint and `api` otherwise. `plugin` is the captured plugin query value, or an empty string. `path` excludes the query string. Request bodies and headers are not stored. The response `message` may itself contain JSON encoded as a string.

Storage bounds: message up to 16,384 characters (response bytes are first capped at 16,384); at most five recent exception captures per request; each exception message up to 16,384 characters and each stack's trailing 32,768 characters. No retention deletion or historical backfill is automatic.

## Errors

| HTTP | Meaning / handling |
| --- | --- |
| 400 | Invalid ISO datetime, reversed range, or invalid limit/offset; inspect `message` and correct the query. |
| 401 | Missing/invalid authentication; reconnect once using the existing connection workflow. |
| 403 | Account role is not allowed; report permission failure. |
| 404 | Wrong prefix or endpoint absent in this deployment; verify version/support. |
| 503 | Runtime initializing or event query/storage unavailable; report the response and stop repeated requests. |

A successful empty `data` array means no recorded events matched that query; it does not prove the service had no failures.
