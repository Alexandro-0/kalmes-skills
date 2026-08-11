---
name: kalmes-analyze-data
description: Perform read-only discovery, querying, joining, summarization, and analysis of Kalmes collection data and operation history through existing collection modules. Use when a user asks to inspect records, analyze trends, compare collections, query audit or historical activity, explain Kalmes data, or export a readable table without changing live data.
---

# Analyze Kalmes Data

Keep this workflow read-only. If fulfilling the request requires creating, updating, deleting, or running code with side effects, stop and route that part to the appropriate mutation skill.

## Connection and scope

Require the Kalmes API URL, target environment, requested business scope, intended output, and an API key (preferred) or account/password fallback. Ask for an API key first when authentication is missing, then authenticate with `$kalmes-connect`. Apply least privilege and do not expose records beyond the user's requested administrative scope.

Read [references/analysis-workflow.md](references/analysis-workflow.md) before querying.

## Workflow

1. Translate the question into collections, fields, relationships, filters, date range, aggregation, and output format.
2. Use `$kalmes-manage-fap` to read the relevant definitions and obtain each collection's data and history module names.
3. Build a bounded query plan. Prefer selective server filters, explicit limits, and 13-digit millisecond timestamps for supported `start` and `end` intervals.
4. Use `$kalmes-invoke-module` with `GET` only. Query data modules for current records and history modules for operation records.
5. Resolve `reference`, `embedded`, and sheet relationships from definitions. Join only the keys needed for the answer.
6. Normalize types, timestamps, visibility, and bilingual display names. Distinguish missing, zero, and null values.
7. Compute and cross-check the requested result. State sampling, truncation, timezone, missing modules, and data-quality assumptions.
8. Present readable Markdown or CSV-style output. Prefer business labels over raw IDs while retaining IDs only when needed for traceability.

## Guardrails

- Do not issue POST, PATCH, or DELETE under this skill.
- Do not query an unbounded collection. Paginate or narrow the time/filter range.
- Exclude `visibility=h` unless deleted/retired data is explicitly part of the question.
- Treat history `data` as the submitted change and `primary` as the earlier object only after verifying the deployment's module contract.
- Do not claim completeness when a module is missing, access is denied, a page is truncated, or a related definition cannot be resolved.

## Completion

Report the collections and modules queried, time range and timezone, filters, row counts, result, assumptions, and any missing coverage. Require immediate password replacement and session revocation only if password fallback was used.
