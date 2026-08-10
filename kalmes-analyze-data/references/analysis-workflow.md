# KalMES read-only analysis workflow

## Query plan

Record:

- business question and requested grain;
- current-data and history collections;
- definition and module names;
- selected fields and relationship keys;
- date range and timezone;
- filters, limit, pagination, and expected volume;
- aggregation and output format.

Use the smallest query that can answer the question. For interval modules, `start` and `end` are normally 13-digit Unix timestamps in milliseconds. Convert the user's local time range explicitly and state the timezone.

## Current and history modules

Read the collection definition through `$kalmes-manage-fap`. Prefer:

```text
module_name.api.data
module_name.api.history
```

Call those module names through `$kalmes-invoke-module` using GET. If a module is missing, report its exact expected name and stop that part of the analysis; do not generate or deploy code under a read-only request.

History records commonly include:

- `record_type`: create, edit/update, or remove;
- `user_id` and `account`;
- `data`: submitted change;
- `primary`: earlier object snapshot;
- `created_at` and `created_date`;
- a source-record ID such as `<collection>_id`.

Verify these fields from the response before relying on them.

## Relationship handling

- `reference`: join stored ID(s) to the foreign collection and display its configured `displayKey`.
- `embedded`: the stored value is a copied document; do not assume it reflects the foreign record's latest state.
- sheet child: filter child data by `foreign_id=<parent id>`.
- `visibility=h`: omit by default and include only for explicit deleted/retired analysis.

Avoid uncontrolled fan-out. Collect unique join IDs, query them in bounded groups when supported, and state when the deployment forces multiple requests.

## Output checks

- Compare returned count with requested limit and pagination.
- Check duplicate business keys, missing references, nulls, and timestamp range boundaries.
- Preserve numeric precision and distinguish counts from percentages.
- Prefer business labels and bilingual definition names.
- Include raw IDs only in an audit appendix or when the user needs exact follow-up targets.
- Mark sampled or truncated results prominently.
