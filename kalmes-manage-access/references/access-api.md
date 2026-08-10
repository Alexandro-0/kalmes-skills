# Account and access API

## Account endpoints

```text
GET   base/account
POST  register
PATCH base/account/<account_id>
POST  force-reset-password
POST  force-delete-account
```

Typical creation body:

```json
{"account":"user@example.com","password":"TEMPORARY","role":"Operator"}
```

Typical role update:

```json
{"role":"Admin"}
```

Force reset:

```json
{"account":"user@example.com","password":"NEW_TEMPORARY"}
```

Known built-in roles include `Day1`, `Reseller`, `SuperUser`, `Admin`, `Operator`, `Kanban`, `SI`, and `Client`; inspect the deployment for custom roles.

Security facts from the current repository:

- `register` and `force-delete-account` do not currently enforce an adequate authenticated role boundary.
- generic `base/account` requires JWT, but account role PATCH lacks a clear administrative role check in the account hook;
- `force-reset-password` checks for `SuperUser`, `Reseller`, or `Day1`;
- therefore apply a stricter client policy and report the server-side gap.

## Custom roles and menu access

Patch the config document:

```json
{
  "extra_roles": ["Client", "Maintenance"],
  "language_pack1": {"_Maintenance": "維修人員"},
  "language_pack2": {"_Maintenance": "Maintenance"},
  "mes_menu_accessibility": {
    "category_deny_list": {
      "iot_center": ["Operator", "Kanban"]
    },
    "action_deny_list": [
      {"path": "/config/settings", "roles": ["Operator", "Kanban"]}
    ]
  }
}
```

`category_deny_list` and `action_deny_list` are denial structures. Merge carefully; an omitted role may grant visibility.

## Embedded-page roles

Use:

```text
GET  event/overrdiePage
POST event/overrdiePage
POST event/batchPostEmbeddedPage
```

Page objects contain `roles`. Current frontend combines some privileged default roles with page roles. Verify actual allow/deny behavior with direct navigation and the page's backing APIs.

## Backend authorization

The config mesLogic hook permits config patch for `Reseller`, `Day1`, `SI`, `Admin`, or `SuperUser`, while some frontend settings pages are narrower. Follow the stricter intended policy. Menu and route controls are frontend-facing; each Extra Code API must implement its own role/ownership authorization.
