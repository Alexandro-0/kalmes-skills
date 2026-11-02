# Event Hub contract

All paths below are relative to the target project's API base. Send a Bearer JWT. Snapshot, test-listener management and SDK registration require Day1, SI, SuperUser or Reseller. Publishing defaults to those roles; a deployment can replace the allowed roles for individual event types with `EVENT_HUB_PUBLISH_ROLES`. On 404, check the base path and whether the running backend includes the requested endpoint.

## Publish and retry

`POST event-hub/events` with Content-Type application/json. The minimal body is `{"type":"event_hub.test"}`. Optional business data belongs in an object such as `{"type":"work_order.completed","data":{"workOrderId":"WO-101"}}`. An omitted data object becomes `{}`. Only these two top-level fields are accepted. Names are case-sensitive, up to 128 characters. Request size is limited to 64 KiB and one event may match up to 100 subscriptions.

HTTP 202 returns `{"data":{"id":"<record ID>","eventId":"<server UUID>","matched":2}}`. Match `data.id` to the snapshot record's `_id`, and `data.eventId` to its `event.eventId`. Treat them as separate identifiers.

Repeated ordinary POSTs create distinct events. For a request that may need replay, send an optional `Idempotency-Key` from the first attempt. Reuse that header, publisher and original payload after a timeout. A duplicate returns HTTP 200 with the original receipt. Reusing the key with different content returns 409. If a request without a key times out, inspect recent events before deciding whether another publication is appropriate.

## Register a business Handler

Within a module's authenticated `invoke`, register with:

```python
from kalmes_events import EventHub

hub = EventHub.current()
sub = hub.subscribe(key="completed", event_type="work_order.completed", handler="on_event")
```

Return `sub.id` to the caller. Define `on_event(event, context)` at module scope in the same file. Retain the ExtraCode API's `customize_authorization` hook (return `None` for default authentication). Invoke the registration API once with a management JWT. Plugin-qualified modules use the existing ExtraCode route's `?plugin=…` parameter. The SDK identifies the current module and plugin. Re-registering the same plugin/module/key updates that subscription. To cancel, call `hub.unsubscribe(key="completed")` inside its API. Changes affect future event intake.

The Handler receives the server-generated `eventId`, the type, data and the standard `created_at`, `created_at_format`, `updated_at`, `updated_at_format` fields. It runs outside the HTTP request. Return normally on success or raise an exception on failure. Use `context.delivery_id` to make side effects idempotent across retries. `context.subscription_id`, `context.publisher` and `context.attempt` identify the delivery context. A Handler has 30 seconds per attempt and up to three attempts.

## Verify delivery and listener state

| Operation | Request | Evidence |
|---|---|---|
| Enable or switch the account's persistent test listener | PUT `event-hub/test-listener` with `{"type":"event_hub.test"}` | Successful response contains `data.subscriptionId`, `type` and `enabled`. Wait for success before publishing. |
| Stop listening for future events | DELETE `event-hub/test-listener` | `data.enabled` is false. Previously accepted deliveries retain their original targets. |
| Inspect events and subscriptions | GET `event-hub/snapshot` | Top-level `events`, `subscriptions` and `testListenerId`. The inbox selects successful deliveries whose `subscriptionId` equals this account's `testListenerId`. |

Use `deliveries[].status` to distinguish pending, running, retry, succeeded and failed. The console lists 10 events per page and shows up to five recent successful test receipts within the 50-event snapshot. Socket.IO namespace `/event-hub` emits a `changed` hint. Fetch the authenticated snapshot for the payload and result. If a bounded wait ends with a pending or retry status, report that state with the event ID.
