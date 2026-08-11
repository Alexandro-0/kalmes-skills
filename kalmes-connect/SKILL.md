---
name: kalmes-connect
description: Connect and authenticate to a Kalmes HTTP API with a preferred API key or account/password fallback, validate readiness, obtain and refresh JWTs, and handle credentials safely. Use whenever Codex must inspect or operate a live Kalmes URL, diagnose login, establish an authenticated session, or prepare another Kalmes skill for API calls.
---

# Connect to Kalmes

## Required inputs

Require the Kalmes URL, target environment, and one authentication method: an API key (preferred) or an account and password fallback. If authentication is absent, ask the user to create and provide an API key from **Advanced Settings → API Keys** or **API Access → API Keys**, depending on the manager role. Do not request account/password when a usable API key is available.

Recommend a least-privilege API key bound to the required SuperUser, Admin, or IT account. Never save or echo the API key, password, login payload, JWT, session ID, or sensitive response claims. Keep secrets in memory or a protected secret input/environment variable; avoid URL query credentials and command-line secret arguments. If password fallback is used, state before login that the supplied password must be replaced after work is complete.

## Connect

1. Normalize the base URL to `https://host/<project>/api/`; preserve any existing project prefix and trailing slash.
2. Require normal TLS verification. Ask before allowing a development self-signed exception; never normalize an exception into production guidance.
3. Call `GET ping`. Continue only when HTTP 200 and `ready` is not false. Treat 503 `service_initializing` as a temporary state, not bad credentials.
4. Prefer `POST login/api-key` with the API key over TLS. Use `POST login` with account/password only as a fallback. Read [references/auth-api.md](references/auth-api.md) for both contracts.
5. Keep the returned JWT in memory and send `Authorization: Bearer <JWT>` on authenticated calls.
6. On 401, exchange the API key or re-authenticate once; then stop and report that the key may be invalid/revoked or the account is no longer eligible. On 403, report the missing authorization; on 402, report the license problem. Do not retry mutations blindly.

## Finish

Discard JWTs and temporary credential variables. If an API key was temporary, exposed, or is no longer needed, tell the user to revoke it in **Advanced Settings → API Keys** or **API Access → API Keys**, depending on the manager role. Only when password fallback was used, tell the user: **Immediately change the password supplied for this operation and revoke or end its active sessions.** If the user asks Codex to rotate a secret, require a secure input surface and never repeat it in the response.
