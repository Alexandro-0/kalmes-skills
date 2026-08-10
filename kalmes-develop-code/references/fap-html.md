# FAP single-file HTML conventions

## Runtime model

Build one HTML document containing its CSS and JavaScript. KalMES renders it inside a same-origin iframe. Do not embed credentials or JWTs.

Include the helper exactly as supported by the target deployment; the standard current form is:

```html
<script src="api/download/MesFunctionUtils.js?plugin=mesEnv.kalVer"></script>
```

Initialize rendered query parameters with:

```js
let query_param = {{query_param|safe}};
```

Use only required keys from `query_param`; never append the whole object to an API URL.

## Authenticated API helpers

Use the helper functions with `getToken()`:

```js
const api = await API_GET('api/' + endpoint, getToken());
const created = await API_POST('api/' + endpoint, getToken(), payload);
const updated = await API_PATCH('api/' + endpointWithId, getToken(), payload);
```

Read `api.resp` only after checking the helper's returned status/error shape. Show a recoverable error state to the user.

For potentially large data, use an intentional date range, pagination, or server filter. Add a date picker only when volume and the API contract justify it.

## Definition-driven fields

- Render only fields allowed by returned `columns`.
- Do not render `id`, `_id`, hidden, password, or unauthorized fields.
- Use `name1`/`name2` or the returned language pack for labels.
- Make a generated unique `code` optional on create and immutable on edit when the API generates it.
- For `reference`, load options from its endpoint and display `displayKey`.
- For `embedded`, send the document shape expected by the API rather than inventing an ID-only structure.
- When an optional reference/embedded selection is cleared, send `null`.

## Sheet/master-detail

For a child page:

```js
let foreign_id = query_param.id;
```

Require it before child POST and send it in the child payload. Filter the child list with only `foreign_id`. Load and display selected parent fields, excluding recursive sheet/redirect controls.

A parent sheet/redirect column becomes a button that navigates to the detail page with the parent record ID. Use the deployment's existing `reactNavigate`/root-path convention or a verified parent-window navigation; do not navigate to an unverified guessed route inside the iframe.

Do not register a detail-only page as a top-level menu item.

## UX and delivery

- Make the page responsive and keyboard accessible.
- Use a light, readable design unless the user specifies another style.
- Avoid implementation labels such as “CRUD” in customer-facing UI.
- Set a meaningful title with the supported helper or parent document contract.
- Escape untrusted values before inserting them into HTML.
- After source upload, test direct load, API failures, both languages, mobile width, allowed/denied roles, and master-detail navigation.
