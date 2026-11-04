---
name: kalmes-event-hub
description: Use the Kalmes Event Hub (事件中心) to publish typed JSON events, register persistent ExtraCode observers, test send and receive, and trace delivery to a Handler or test inbox. Applies to event-hub endpoints and the Event Hub console.
---

# Kalmes Event Hub

Reuse the target project and authenticated session. If a connection is needed, follow `$kalmes-connect`. Read the [Event Hub contract](references/event-hub.md) for request and response shapes, the ExtraCode SDK and retry semantics.

- **Publish an event.** Send the requested `type` and optional JSON object `data` once and return its receipt. Inspect deliveries only if requested or diagnosing a failure. The server assigns the ID and timestamps. Matching subscribers can execute live business Handlers.
- **Register an Observer.** Use the SDK inside the authenticated ExtraCode API's `invoke` and point it to a synchronous function in that module. For creating or installing the module itself, follow `$kalmes-develop-code`. Verify the enabled type, module, key and Handler in the subscriptions snapshot.
- **Test a round trip.** Open the project's Event Hub under Plugin 程式碼 → 事件中心 → 測試工具. For an isolated test choose a fresh type, use 測試收發 → 傾聽並送出, and verify the same returned event ID appears in 我的傾聽收件匣. The test listener persists and each account has one. If temporarily switching it for verification, record its prior state and restore it afterward. Use 只發布事件 when existing subscriptions should handle the test.
- **Investigate a missing delivery.** Start with the snapshot. Match the receipt ID to the event record and inspect each delivery's subscription ID, status, attempts and error. A 202 receipt establishes acceptance. Report Handler success only from its delivery record. Zero matches means there were no enabled matching subscriptions at acceptance. The snapshot covers the most recent 50 events.

The 資料流 tab explains the stages and the API 說明 tab shows examples for the target environment. For an HTTP 5xx investigation requiring backend error records, use `$kalmes-get-api-error-events`.
