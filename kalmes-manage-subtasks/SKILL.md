---
name: kalmes-manage-subtasks
description: Create, inspect, start, cancel, fail, complete, and monitor Kalmes internal Agent Sub Task queue items through authenticated Extra Code APIs. Use when a user asks external Codex to create a Kalmes Main Task and ordered subtasks, run the subTaskConsumer queue, update a subtask status or result, or inspect task progress by Main Task number.
---

# Manage Kalmes Agent Subtasks

Operate the Kalmes internal queue over HTTP. These are persistent server-side Agent tasks, not Codex collaboration subagents or Codex tasks.

## Connection gate

Require the Kalmes URL, target environment, explicit queue intent, and an API key (preferred) or account/password fallback. Ask for an API key first when authentication is missing. Authenticate with `$kalmes-connect`, then read [references/subtask-api.md](references/subtask-api.md).

## Create an ordered task

1. Use the user-provided Main Task ID or generate eight uppercase ASCII letters. Reuse the same ID for every subtask in the sequence.
2. Split the request into ordered, independently checkable prompts. A subtask must fail when later steps must not continue after its failure.
3. Query the server-side Agent Skills list and validate each comma-separated `skillKeys` value. These are internal Kalmes skill keys, not `$kalmes-*` Codex skill names.
4. POST each subtask in order with `subTaskStatus: "Ready"` and empty `code`, `result`, receiver ID, and receiver name. The API assigns the visible subtask code.
5. Read the task group back and verify order, generated codes, status, prompt, and skill keys.
6. Return the Main Task number to the user.

## Run and monitor

- Call the `subTaskConsumer` GET endpoint only when the user explicitly asks to execute the queue. It may start asynchronous work; its response is not proof of completion.
- Poll the task group at a reasonable interval and stop on terminal states. Report `Ready`, running/deployment-specific states, `Success`, `Fail`, and `Cancel` exactly as returned.
- Do not start the consumer repeatedly merely because tasks remain `Ready`.

## Update

Resolve a visible subtask code to the unique database `id` before PATCH. Allow only the requested status/result fields. When marking a subtask `Fail`, preserve the internal queue rule by cancelling later ready subtasks in the same Main Task after verifying their order.

## Safety

Starting the consumer can execute arbitrary Agent prompts and their associated tools. On production, show the queued prompts, skill keys, and expected side effects before the first run. Require confirmation for cancellation, failure propagation, or any rewrite of completed results.

## Completion

Report Main Task ID, subtask codes and statuses, whether the consumer was invoked, terminal results, cancelled follow-on tasks, and unresolved failures. Never include credentials or JWTs. Require immediate password replacement and session revocation only if password fallback was used.
