# End-to-end feature workflow

## Contents

1. Requirement model
2. Architecture mapping
3. Implementation order
4. Acceptance matrix
5. Example blueprint

## 1. Requirement model

Capture:

- actors and allowed/denied roles;
- plugin code, FAP collection definitions, business records, required fields, uniqueness, references, sheets, and lifecycle;
- API operations and error behavior;
- pages, menu category, route, labels in both languages, and attachments;
- requested system name, logo asset, branding surfaces, and fallback behavior;
- immediate, startup, interval, or cron behavior;
- external integrations and secrets;
- target environment, availability impact, audit needs, and rollback objective.

Do not begin writes from a vague request. Produce a concise change set and acceptance criteria first.

## 2. Architecture mapping

| Requirement | KalMES surface |
|---|---|
| FAP collection definition and relationships | `extracode/dataManagementConfigApi` |
| Schema-backed system entity | `base/<column>` and server `schema/*.json` |
| Feature-owned event/history data | `records/<column>` |
| Business API | Extra Code type `API` and `extracode/<name>` |
| Embedded UI | Extra Code type `Html` plus embedded-page registration |
| Startup action or job registration | Extra Code type `Initial` |
| Shared Python library | Extra Code type `Others` |
| Gmail/HTML email notification | `kalmesMailSender` through `$kalmes-send-email` |
| Attachment | `file` or `event/files` |
| System name and logo | config `mes.manufacture_name`, resource upload, and `mes.logo` |
| Menu ordering/category | config `extra_menu` |
| Labels | config `language_pack1` and `language_pack2` |
| Category visibility | `mes_menu_accessibility.category_deny_list` |
| Built-in path visibility | `mes_menu_accessibility.action_deny_list` |
| Embedded-page access | embedded-page `roles` |
| Portable release | plugin pack |
| Internal Agent task queue | `agentSubTaskDataApi` and `subTaskConsumer` |

Changing `schema/*.json` is a repository/deployment change, not a general remote configuration API. If only URL credentials are available, use existing schemas or feature-owned records and state the limitation.

## 3. Implementation order

1. Read current state and export affected config/source.
2. Preserve or choose a stable plugin code and collision-resistant collection, file, route, menu, translation, role, and scheduler-job identifiers.
3. Add FAP definitions in relationship order, then storage and seed data.
4. Add shared module, API, then HTML.
5. Add schedule registration only after the called API/data behavior passes tests.
6. If email is required, use the sender fast path when already configured; configure or diagnose it only when needed.
7. Apply requested branding and register embedded page, menu, and translations.
8. Add role restrictions.
9. Run acceptance and negative tests.
10. Package or document the release and verify rollback.

## 4. Acceptance matrix

Test at minimum:

| Area | Positive | Negative |
|---|---|---|
| Authentication | valid login and JWT call | invalid password and expired/invalid token |
| Data | create/read/update/query | missing required field, duplicate, invalid reference |
| API | expected response and status | malformed body, dependency failure |
| HTML | route loads and saves | API failure is visible and recoverable |
| Access | allowed role succeeds | denied role receives 403, not merely a hidden menu |
| Schedule | idempotent registration and one execution | duplicate start and job failure |
| Files | allowed upload/download | invalid type/size/name where enforced |
| Email | approved role sends once to a controlled inbox | denied role, invalid recipient, SMTP failure, and uncertain retry |
| Branding | name/logo appear on sign-in, shell, title, and favicon | invalid file and rollback restore prior brand |
| Recovery | restore prior source/config | verify no orphan menu/page/job remains |

## 5. Example blueprint

For an equipment-maintenance feature:

- store maintenance plans and executions in named records;
- create an API Extra Code module for validation and CRUD orchestration;
- create an HTML Extra Code page for list/edit operations;
- upload evidence through the resource API;
- create an Initial module that registers an overdue-check interval/cron job with a stable job ID;
- register the HTML route in an embedded page and menu category;
- add both language packs;
- create or reuse a maintenance role and restrict category, action, and page access;
- test a maintenance user and a denied user;
- preserve source versions/config export and document removal of page, menu, code, records, and job.
