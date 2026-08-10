# KalMES Agent Sub Task HTTP API

All routes are relative to the authenticated KalMES API root.

## Discover internal skill keys

```text
GET extracode/agentSkillsDataApi
```

Use the returned internal Agent skill keys in `skillKeys`. They are not Codex `$kalmes-*` skill folder names.

## Create and read

```text
GET  extracode/agentSubTaskDataApi?taskId=<MAIN_TASK_ID>
GET  extracode/agentSubTaskDataApi/<database_id>
POST extracode/agentSubTaskDataApi
```

Create body:

```json
{
  "taskId": "ABCDEFGH",
  "code": "",
  "subTaskStatus": "Ready",
  "prompt": "Exact subtask prompt",
  "result": "",
  "receiverAgentId": "",
  "receiverAgentName": "",
  "skillKeys": "skillKey1,skillKey2"
}
```

The server assigns a visible code such as `ABCDEFGH-1`. Preserve the returned database `id`; PATCH uses that ID, not the visible code.

## Start the consumer

```text
GET extracode/subTaskConsumer
```

This call can start asynchronous task execution. A successful response means tasks were considered or launched, not that they finished.

## Update

```text
PATCH extracode/agentSubTaskDataApi/<database_id>
```

Example:

```json
{
  "subTaskStatus": "Success",
  "result": "Sanitized result"
}
```

Common states are `Ready`, `Success`, `Fail`, and `Cancel`; preserve other deployment-specific states when returned. Do not overwrite `taskId`, `code`, prompt, or receiver fields unless explicitly requested.

The web Agent's internal update tool cancels later subtasks when one becomes `Fail`. Direct HTTP PATCH does not perform that propagation in the current module. To preserve behavior:

1. read all records for the same `taskId`;
2. establish order from generated code/creation metadata;
3. PATCH the failed task;
4. PATCH only later non-terminal tasks to `Cancel`;
5. read the group back and report every affected ID/code.

## Polling

Poll the task group, not the consumer endpoint. Use moderate intervals and stop when all requested tasks are terminal, the user asks to stop, or an authorization/system error blocks progress. Do not expose prompts or results outside the user's authorized scope.
