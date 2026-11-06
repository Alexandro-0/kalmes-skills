# Activity attribution and automatic local tracking

**Activity integration requires Kalmes 2.1.0 or later.** The dedicated `$kalmes-agent-activity` skill covers pairing, health checks and bounded queries. Legacy servers may ignore attribution headers; that does not mean they saved records. Check `GET agent-activities/capabilities` once per target/session when establishing support (`protocol_version: 1`, `scoped_collectors: true`). A missing feature should be reported as an activity compatibility gap, not retried as an application mutation.

## Shared API session

Apply to authenticated Kalmes requests, including reuse of a session established by another skill:

```text
X-Kalmes-Agent: <actual agent name, e.g. codex, claude, gemini>
X-Kalmes-Skill: <actual active kalmes skill name>
X-Kalmes-Run-Id: <one UUID for this user task>
```

Reuse a local collector's run ID when one exists; otherwise generate a UUID once. Reuse it across skills, requests and retries for this task. Update Skill on transitions. If the resolved plugin is absent from the API path/body, add `X-Kalmes-Plugin`; clear stale plugin labels when changing scope. Use ASCII values or URL-encode non-ASCII identifiers. Never invent an agent, skill or plugin to fill missing labels.

Keep Authorization unchanged. Labels grant no access and are not identity proof. Do not put prompts, source, credentials or private task descriptions in them. No separate reporting POST is needed for API actions: the server observes the actual request and result. `X-Kalmes-Activity-Id` identifies a saved event; `X-Kalmes-Activity: unavailable` is an audit gap. Do not replay a successful mutation to obtain a record.

## Automatic local observation, independent of hooks

Once the user has enabled collection for a checkout, a standalone worker tracks and syncs file changes even when the agent has no hooks or does not read this skill. Unlabelled changes appear as **workspace observation**, since filesystem changes do not reveal their author. It does not read private agent transcripts.

For accurate task labels, the agent runs the following lifecycle itself; the user does not need to execute commands:

1. Follow the repository's `AGENTS.md` and inspect `auto-status` using its collector. If enabled, run `auto-start --repo <checkout> --agent <actual-agent> --skill <active-skill> --run-id <task-uuid>` before local edits. Pass `--plugin <resolved-plugin>` when known; pass an empty plugin value when clearing a previous scope. Reuse the returned run ID in API headers.
2. Repeat `auto-start` with the same run ID when changing skills and before later edit groups to renew the 30-minute attribution lease. A different active task must not be overwritten; use a separate worktree for concurrent agents.
3. After validation, run `auto-stop --repo <checkout> --run-id <same-uuid>`. This captures final changes and returns to continuous workspace observation; synchronization remains automatic. Inspect health to distinguish queued uploads from completed sync.

If automatic collection has not been configured, do not invent a destination or persist authentication. When setup is within the user's requested scope, use `$kalmes-agent-activity`; otherwise report that local synchronization is not configured. Ordinary API operations can still proceed within their own authorization.

The worker starts on Windows login, scans every 10 seconds, sends at most 25 events/64 KB per tick and retries offline uploads with bounded backoff. Configuration and outbox live in the checkout's private Git directory. Only a project-bound upload credential persists in Windows Credential Manager; never store the user's password, normal JWT or API key. The worker removes bootstrap credentials from its child environment. Hooks are optional and are not installed by this workflow.

File records retain paths, hashes, sizes and line counts, not raw code. Human edits in the same checkout may be observed during an agent's labelled task. Ignored, secret, linked and oversized files are excluded. Files created and removed entirely between scans may not be observed. Unsupported or remote-only environments must not be presented as automatically covered.
