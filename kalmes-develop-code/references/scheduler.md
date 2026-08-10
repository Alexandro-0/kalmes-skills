# Scheduler development and operation

## Discover jobs

When deployed, use:

```text
GET extracode/kalmesSchedulerApi
```

The current module returns registered or suspended jobs that have a known filename mapping. Treat an empty result as “no visible mapped jobs,” not proof that the scheduler has no internal jobs.

## Create scheduler code

Create an Extra Code `Initial` module with a parameterless `invoke`:

```python
import JobListener
import MyApiController

JOB_ID = "plugin-purpose-daily"

def invoke():
    def event():
        MyApiController.log(JOB_ID, "trigger")
        # idempotent task body

    JobListener.add_cron_job(
        JOB_ID,
        event,
        hour=23,
        minute=59,
        misfire_grace_time=60,
    )
```

For interval work, use `add_interval_job` with an intentional interval. Use a globally stable plugin-prefixed job ID and make both registration and event execution safe to repeat.

## Save and register

1. Read the existing job list and choose a non-conflicting ID.
2. Create or update the `Initial` source through the Extra Code source APIs.
3. Read the source back and review side effects.
4. On production, obtain explicit confirmation.
5. Register/run it with:

```text
POST extracode/run/<filename_with_extension>
{}
```

6. Read the visible scheduler list and verify the expected next run.
7. Verify that running registration twice does not create duplicate jobs.

Do not run Initial code merely to syntax-check it.

## Cancel or restart

If `kalmesSchedulerApi` is deployed and authorized:

```text
PATCH extracode/kalmesSchedulerApi/<job_id>
{"visibility":"h"}
```

cancels/removes a job, while:

```text
PATCH extracode/kalmesSchedulerApi/<job_id>
{"restart":"true"}
```

attempts to re-run the mapped Initial file.

Both are high-impact operations. Require exact job ID, current state, filename mapping, explicit user intent, and a recovery plan immediately before the call.
