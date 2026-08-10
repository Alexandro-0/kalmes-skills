# Extra Code API and contracts

Use `{BASE}` for the configured API root and a Bearer JWT for protected calls.

## Metadata and source lifecycle

```text
GET   extracode/codeuploader?visibility=v
POST  extracode/codeuploader                         multipart file
PATCH extracode/codeuploader/<id>                    metadata/visibility
POST  extraCode/code                                 create from template
GET   extraCode/live/<filename>?plugin=<folder>      read source
POST  extraCode/upload/<filename>?manual=1           {"code":"..."}
GET   extracode/codeVersion/<filename>
GET   extracode/codeHistory/<history_name>
POST  extracode/run/<filename>
```

`POST extraCode/code` requires JWT and a `pro` or `premium` license. Supported body:

```json
{
  "name": "FeatureApi.py",
  "type": "API",
  "random_secrete": "HTML_SHARED_SECRET_IF_NEEDED",
  "hashTag": "OPTIONAL_TAG"
}
```

Supported template types are `API`, `Html`, `Initial`, and `Others`. Source read/write has additional license constraints in current backend behavior. Treat HTTP 403 as a license or authorization boundary, not a reason to seek a bypass.

## Runtime API routes

For a file `FeatureApi.py`, the route name is normally `FeatureApi`:

```text
GET|POST|PATCH|DELETE extracode/FeatureApi
GET|POST|PATCH|DELETE extracode/FeatureApi/<resource_id>
```

The module must expose:

```python
def invoke(method, query_param, data, header, resource_id=None, uid=None):
    return 200, {"message": "success", "data": {}}
```

Optional authorization hook:

```python
def customize_authorization(method, query_param, data, header, resource_id=None):
    return True
```

The handler loads code dynamically and may use the hook to permit or deny. Implement explicit allow/deny logic and test it. Validate `method`, payload, IDs, role/ownership, and exception behavior inside the module.

## HTML

```text
GET extracode/html/preview/<name>
GET|POST|PATCH|DELETE extracode/html/preview/api/<api_name>[/<resource_id>]
```

An Html module returns a Flask response from `invoke`. Escape untrusted content, use authenticated APIs, restrict parent-window messaging, and do not embed credentials or JWTs in static HTML. Register the displayed application route separately through embedded-page APIs.

## Initial and schedule

Run an Initial file explicitly with:

```text
POST extracode/run/<filename>
```

The endpoint imports the file and calls parameterless `invoke()`. It executes arbitrary code; require confirmation on production.

Scheduler pattern:

```python
import JobListener

def invoke():
    def event():
        pass

    JobListener.add_cron_job(
        "feature-overdue-daily",
        event,
        hour=23,
        minute=59,
        misfire_grace_time=60,
    )
    # Or add_interval_job(job_id, event, seconds=..., misfire_grace_time=60)
```

Use deterministic job IDs and functions safe for retries. The server starts Initial code during initialization. Avoid destructive work directly in initialization; register jobs or perform idempotent setup.

## Modules

Create shared code as `Others`, then import and reload it from API/Html/Initial code where hot editing is expected:

```python
import importlib
import FeatureModule
importlib.reload(FeatureModule)
```

Do not expose a module as an HTTP API unless it implements the API contract intentionally.

## High-risk legacy behavior

Some source download/preview routes are less protected than their write routes. Always authenticate anyway. Never use a public legacy route to retrieve code without authorization. Path components must be controlled and must not contain traversal sequences.
