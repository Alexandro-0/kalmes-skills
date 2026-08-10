---
name: kalmes-connect
description: Connect and authenticate to a KalMES HTTP API, validate readiness, obtain and refresh JWTs, and handle credentials safely. Use whenever Codex must inspect or operate a live KalMES URL, diagnose login, establish an authenticated session, or prepare another KalMES skill for API calls.
---

# Connect to KalMES

## Required inputs

Require the user to provide the KalMES URL, account, and password before any live operation. Also determine whether the target is development, staging, or production. If any required value is absent, ask for it and do not attempt authentication.

Recommend a temporary least-privilege account. State before login that the user must replace the supplied password after work is complete. Never save or echo the password, login payload, JWT, session ID, or sensitive response claims. Avoid URL query credentials and command-line password arguments.

## Connect

1. Normalize the base URL to `https://host/<project>/api/`; preserve any existing project prefix and trailing slash.
2. Require normal TLS verification. Ask before allowing a development self-signed exception; never normalize an exception into production guidance.
3. Call `GET ping`. Continue only when HTTP 200 and `ready` is not false. Treat 503 `service_initializing` as a temporary state, not bad credentials.
4. Call `POST login` with the account and password over TLS. Read [references/auth-api.md](references/auth-api.md) for the contract.
5. Keep the returned JWT in memory and send `Authorization: Bearer <JWT>` on authenticated calls.
6. On 401, re-authenticate once; on 403, stop and report the missing authorization; on 402, report the license problem; do not retry mutations blindly.

## Finish

Discard tokens and temporary credential variables. Tell the user: **Immediately change the password supplied for this operation and revoke or end its active sessions.** If the user asks Codex to rotate it, require a newly chosen password through a secure input surface and never repeat it in the response.
