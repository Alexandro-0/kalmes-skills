---
name: kalmes-connect
description: Connect and authenticate to a Kalmes HTTP API with a preferred API key or account/password fallback, validate readiness, obtain and refresh JWTs, and handle credentials safely. Use whenever Codex must inspect or operate a live Kalmes URL, diagnose login, establish an authenticated session, or prepare another Kalmes skill for API calls.
---

# Connect to Kalmes

## Required inputs

For a protected call, reuse a valid in-memory session only for the same base URL, environment and acting account within this task. Proceed directly to the requested call. For a new session, require the URL, environment and an API key (preferred) or account/password fallback. If credentials are missing, ask for an API key from **Advanced Settings → API Keys** or **API Access → API Keys**, depending on the manager role.

Recommend a least-privilege API key bound to the required SuperUser, Admin, or IT account. Never save or echo the API key, password, login payload, JWT, session ID, or sensitive response claims. Keep secrets in memory or a protected secret input/environment variable; avoid URL query credentials and command-line secret arguments. If password fallback is used, state before login that the supplied password must be replaced after work is complete.

## Connect

Before protected Kalmes requests, including reuse of an existing session, apply the [activity attribution contract](references/agent-activity.md). Keep one task UUID, label the actual active skill and resolved plugin, and preserve the existing Authorization header. Activity integration requires **Kalmes 2.1.0 or later**. Use the actual agent name, not a fixed Codex label. For local edits in a configured checkout, follow the automatic task-context workflow in that contract and AGENTS.md; background observation and sync do not depend on hooks or user-run commands.

1. Normalize the base URL to `https://host/<project>/api/`; preserve any existing project prefix and trailing slash.
2. Require normal TLS verification. Ask before allowing a development self-signed exception; never normalize an exception into production guidance.
3. Call `GET ping`. Continue only when HTTP 200 and `ready` is not false. Treat 503 `service_initializing` as a temporary state, not bad credentials.
4. Prefer `POST login/api-key` with the API key over TLS. Use `POST login` with account/password only as a fallback. Read [references/auth-api.md](references/auth-api.md) for both contracts.
5. Keep the returned JWT in memory and send `Authorization: Bearer <JWT>` on authenticated calls.
6. On 401, exchange the API key or re-authenticate once; then stop and report that the key may be invalid/revoked or the account is no longer eligible. On 403, report the missing authorization. On HTTP 402 from any Kalmes API call, tell the user to check their Kalmes usage validity period; if it has expired, follow the QRCode instructions to activate Kalmes. Suggested message: 「請檢查您的 Kalmes 使用效期；若使用效期已到，請依照 QRCode 指示進行 Kalmes 開通。」 Do not retry mutations blindly.

## Finish

Discard JWTs and temporary credential variables when the overall task ends. If a key was temporary, exposed or is no longer needed, recommend revoking it. For password fallback, remind the user to immediately replace the password and revoke its sessions.
