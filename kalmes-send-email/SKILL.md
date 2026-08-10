---
name: kalmes-send-email
description: Send HTML email from external Codex through the authenticated KalMES kalmesMailSender HTTP module, and configure or troubleshoot its Gmail SMTP setup only when needed. Use when Codex is asked to send an email through KalMES, enable KalMES email, or diagnose a failed KalMES email request.
---

# Send Email from KalMES

Default to the fast path. Do not audit the module, ENV, SMTP configuration, authorization, recipient privacy, or delivery behavior before an ordinary send. Inspect those only during first-time setup or after the API is blocked or fails.

## Fast path: send immediately

1. Reuse the current authenticated KalMES connection. If none is available, ask only for the KalMES URL, account, and password, then connect with `$kalmes-connect`.
2. Require only:
   - exact recipient address or addresses;
   - a non-empty subject;
   - message content.
3. When all three are present and the user has asked to send, treat that request as authorization for one send. Do not add a separate preview, confirmation round, test send, source inspection, ENV check, or permission audit.
4. Convert plain text to simple HTML without changing its meaning. If the user supplied HTML, use it as requested unless it contains an obvious credential or executable script.
5. Send an authenticated HTTP request immediately:

```http
POST {BASE}extracode/kalmesMailSender
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "to_mails": ["recipient@example.com"],
  "subject": "Subject",
  "html_content": "<p>Message</p>"
}
```

Use one string for one recipient or a JSON list of individual addresses for several recipients. Do not put `sender_email`, `sender_apw`, or any credential in the payload.

6. Report the HTTP/module result briefly. A successful response means the send function completed; do not delay the response by investigating inbox delivery unless the user asks.

If a required recipient, subject, or message is missing, ask only for the missing value. Do not start the setup workflow merely because optional details are absent.

## Diagnose only when blocked

- On `401`, reconnect once and retry once.
- On `400`, correct only the missing or invalid request field.
- On `403`, report that the account lacks permission; do not bypass it.
- On SMTP authentication, missing sender, connection, code, or ENV errors, read [references/mail-api.md](references/mail-api.md) and inspect only the failing layer.
- On a timeout after submission, report the result as uncertain and do not automatically resend because the first call may have succeeded.
- Do not expand a simple failure into unrelated production hardening unless the user asks for it.

## First-time setup only

Use this section only when the user asks to configure email, the module is absent, or a send fails because SMTP is not configured.

1. Read [references/mail-api.md](references/mail-api.md).
2. Configure `kalmes_mail_sender_account` and `kalmes_mail_sender_gmail_app_password` in the protected server-side ENV store.
3. Have the user enter the Gmail App Password directly in a masked secret interface. Never ask them to paste it into the conversation or read it back.
4. Repair `kalmesMailSender.py` only if its current implementation prevents the documented API call from working.
5. Reload the module/service if ENV changes are not picked up, then return to the fast path.

## Credential handling

Never echo or save KalMES or Gmail passwords, JWTs, or SMTP credentials. If the user supplied a KalMES password during the task, remind them afterward to replace it and revoke or end its active sessions. Revoke a Gmail App Password only if it was exposed, temporary, or no longer needed.
