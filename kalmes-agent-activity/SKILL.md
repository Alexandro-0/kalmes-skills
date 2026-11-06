---
name: kalmes-agent-activity
description: Configure automatic local file tracking and synchronization, label agent and skill activity, or review bounded activity records in Kalmes 2.1.0 or later. Use when a user wants to know which agent changed code, configuration, data or plugins, set up automatic activity collection, investigate missing records, or disable a collector. Works with any coding agent; hooks are optional.
---

# Kalmes Agent Activity

**Requires Kalmes 2.1.0 or later.** Older versions do not provide this skill's activity APIs, scoped collector credentials, or automatic synchronization contract. Never claim tracking is connected solely because the server accepts attribution headers.

Read the shared activity contract in `$kalmes-connect` → `references/agent-activity.md` for labels and automatic task context. Use the actual agent name; never assume Codex. Filesystem observation alone cannot establish the author, skill or plugin of an edit.

## Enable automatic local tracking

1. Resolve the user's intended Kalmes URL, authenticated account and Git checkout. Reuse an authorized session through `$kalmes-connect`. Check `GET agent-activities/capabilities`: require `protocol_version: 1` and `scoped_collectors: true`. A 404 or unsupported capability requires upgrading to Kalmes 2.1.0+; 401/403 require resolving authentication/permissions.
2. Locate `tools/agent_activity.py`, `agent_activity_auto.py` and `activity_credentials.py` in the Kalmes 2.1.0+ source checkout. The collector can track another Git repository through `--repo`. Require Python 3.10+, Git and Windows for the current automatic-startup/credential-store implementation. Do not claim these Windows integrations work on another OS.
3. Inspect `auto-status --repo <checkout>` first. If enabled and healthy, reuse the configuration. For an authorized setup, run `enable-auto --repo <checkout> --base-url <confirmed-api-url>` with a bootstrap JWT only in the short-lived process environment `KALMES_TOKEN`. Use `--ca-file <trusted-ca-file>` when a known development CA is needed; keep certificate and hostname verification enabled.
4. Pairing stores only a revocable, project-bound upload credential in Windows Credential Manager, registers a current-user Windows logon command and starts one hidden worker. Do not persist passwords, ordinary JWTs or API keys. Remove bootstrap variables afterwards. No agent-specific hook, transcript parser or manual scan/sync loop is required.
5. Verify `running`, `startup`, `health`, and pending counts. Observe the next authorized edit reaching the activity API/UI. If a separate test edit is needed, use an isolated disposable file, verify create/update/delete and remove the file. Never modify production application data merely to test tracking.

Nested independent repositories and worktrees need separate pairing. Never silently change a configured destination while records are queued. A worker observes every 10 seconds and sends one batch of at most 25 events/64 KB per cycle; offline retries back off to 5 minutes. Existing files form the initial baseline, not new activity.

## Review activity without large queries

- Open **Plugin code → AI activity** (`/<project>/plugin/agent-activity`) or request `GET agent-activities` with the existing authorized JWT. Collector credentials cannot read activity or other Kalmes APIs.
- Start with the relevant task ID, skill/plugin/source and a narrow time window. Defaults: last 24 hours, 25 summaries, read operations excluded. Maximum: 31 days and 100 entries per page; retention: 90 days.
- Follow `next_cursor` only when more results are needed. Keep the original filters/window with that cursor. Stop after answering the request; never drain all pages for a routine overview. Fetch `GET agent-activities/<id>` only for selected details.
- Explain local observation separately from a server-observed API result. Show actual labels and timestamps; missing attribution remains unknown. File details contain fingerprints, sizes and line counts, not raw source or a diff.

## Diagnose or disable

Use `auto-status`: queued records plus a sync error indicate deferred upload; a scan error indicates an observation gap. Check the confirmed server, trusted CA, role and credential status without printing secrets. Preserve the queue when diagnosing. Do not retry successful application mutations to manufacture activity records.

For requested shutdown, run `disable-auto --repo <checkout>`; it removes that checkout's startup entry, stops observation and preserves the outbox. Add `--revoke` when the user wants to disconnect the collector: it revokes the scoped credential and removes its Windows credential entry. Do not delete recorded history as part of disabling.

Report the configured checkout, target, observed worker/sync state and any compatibility gap. Verify the startup entry and worker restart, but do not claim an actual OS reboot was tested unless one occurred.
