# `kalmesMailSender` setup and failure reference

Read this reference only for first-time setup or after an ordinary send fails. It reflects the updated `kalmesMailSender.py` verified on the Kalmes 1.4.26 instance.

## Current API behavior

Call the module over authenticated HTTP:

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

Required payload fields are `to_mails`, `subject`, and `html_content`. `to_mails` accepts one address, a comma-delimited string, or a list. The optional `text_fallback` overrides the plain-text fallback.

The updated module accepts optional `sender_email` and `sender_apw`, but an ordinary call must omit them. When they are absent or empty, `_get_mail_credentials()` correctly falls back to the server-side `GMAIL_ADDRESS`/`APP_PASSWORD` values and then the Kalmes ENV values.

Expected success:

```json
{
  "message": "sent",
  "data": {
    "ok": true,
    "sent_to": ["recipient@example.com"],
    "subject": "Subject",
    "mode": "html",
    "sender": "configured-sender@example.com"
  }
}
```

The module now rejects non-`POST` methods with `405` and returns `400` for missing required payload fields.

## Gmail setup

1. Use a dedicated Gmail or Google Workspace sender account.
2. Enable Google 2-Step Verification.
3. Create an App Password for Kalmes when the account policy permits it.
4. Have the user enter these values directly in the protected server-side ENV interface:
   - `kalmes_mail_sender_account`
   - `kalmes_mail_sender_gmail_app_password`
5. Never ask the user to paste the App Password into the conversation and never read it back.
6. Reload the module or service after changing ENV because the global values are initialized at import time.
7. Ensure the Kalmes host can resolve `smtp.gmail.com` and connect to TLS port 465.

The updated code removes spaces from the App Password automatically. Google may revoke App Passwords after the main account password changes. Recheck current requirements in [Google Account Help](https://support.google.com/accounts/answer/185833).

## Remaining considerations

These do not block an ordinary requested send. Address them only when the user asks for production hardening or when they cause a failure.

| Area | Current behavior |
|---|---|
| Recipient visibility | Multiple recipients are joined into the visible `To` header; there is no BCC support |
| Acceptance evidence | `sent_to` echoes the requested recipients; `smtp.send_message()` refusal data is not returned |
| Authorization | `customize_authorization()` currently returns `True` |
| Error disclosure | Some SMTP exception branches still return or print traceback details |
| Retry safety | There is no idempotency key; do not automatically resend after an uncertain timeout |
| Unsupported features | No CC, BCC, reply-to, attachment, queue, or dry-run support |

## Troubleshooting only after failure

| Result | Likely cause | Next action |
|---|---|---|
| `400` with missing fields | Recipient, subject, or HTML is absent | Correct only the named field and retry once |
| `400` sender/App Password missing | Server ENV is absent or was not reloaded | Configure the masked ENV values and reload |
| `401` Gmail authentication failed | Sender/App Password mismatch, revocation, or account policy | Verify the configured sender and replace the App Password through the secret interface |
| `403` | Kalmes caller lacks permission | Stop; do not bypass authorization |
| `502` SMTP error | Gmail rejected the request or SMTP failed | Use the sanitized SMTP code/message to inspect only that failure |
| Connection timeout | DNS, firewall, proxy, or outbound port 465 | Check reachability from the Kalmes host without exposing credentials |
| Timeout after submission | Delivery result is uncertain | Do not resend automatically; check inbox/log evidence first |

A `200` response means the send function completed without raising an exception. It does not prove inbox delivery or that the recipient read the message.
