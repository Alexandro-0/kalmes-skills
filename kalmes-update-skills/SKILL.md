---
name: kalmes-update-skills
description: Safely locate, synchronize, modify, validate, install, and optionally publish the canonical Kalmes Skills repository at https://github.com/Alexandro-0/kalmes-skills. Use when a user asks to pull or install the latest Kalmes skills, update an installed copy, add or edit a kalmes-* skill, repair repository conventions or UTF-8, refresh catalogs and UI metadata, prepare a branch or commit, or explicitly publish changes to GitHub through a push, pull request, tag, or release.
---

# Update Kalmes Skills

Use `https://github.com/Alexandro-0/kalmes-skills.git` as the canonical repository. Treat source maintenance, local installation refresh, and GitHub publication as distinct operations with different authorization.

## Establish repository state

1. Locate the repository root with Git rather than assuming a fixed machine path. If no clone exists and the user asked to install or work on the repository, clone the canonical URL into the user-selected destination.
2. Read applicable repository instructions, the full affected `SKILL.md`, its directly linked references, `agents/openai.yaml`, and the relevant English and Traditional Chinese README sections before editing.
3. Inspect `git status --short --branch`, current branch, upstream, `origin`, and local commits. Run `git fetch origin`, then calculate `origin/main...HEAD` ahead/behind counts.
4. Preserve all existing changes. Never use hard reset, discard, force checkout, automatic stash, or force push. Stop a sync that would overlap dirty files or require a history decision.

Read [references/repository-workflow.md](references/repository-workflow.md) for exact Git decisions, repository conventions, installation refresh, and publication gates.

## Choose the operation

- **Synchronize a clean Git clone:** fetch and fast-forward only when the clone is behind and has no local-only commits. If it is ahead, diverged, dirty, or on an unexpected branch, report the state and preserve it.
- **Refresh copied installed skills:** validate the canonical source first, compare the selected complete skill directories, preserve local customizations, and replace only the copies the user placed in scope. Do not overwrite an entire skills home implicitly.
- **Modify source skills:** make the requested focused changes in a branch or current worktree the user authorized, preserve unrelated changes, update cross-references and catalogs, and validate the whole repository.
- **Publish:** commit, push, open a pull request, tag, or create a release only when the user explicitly requests that action. Verify the canonical remote immediately before publishing and never force-update shared history.

## Editing workflow

1. Define the triggering user requests and affected skills. Reuse an existing focused skill when possible; create a new `kalmes-*` directory only for a distinct capability.
2. Keep the skill folder and frontmatter `name` identical, lowercase, and hyphenated. In `SKILL.md`, use only `name` and `description` frontmatter fields; put all triggering conditions in `description` and write the body as operational instructions.
3. Use the display brand `Kalmes` exactly. Preserve lowercase `kalmes-*` skill identifiers, `$kalmes-*` invocations, repository names, URLs, API paths, environment variables, and code identifiers when their spelling is part of a contract.
4. Keep `SKILL.md` concise. Put detailed contracts in directly linked `references/`; add deterministic `scripts/` only for repeatable or fragile work and test every added script.
5. Keep secrets, tokens, private URLs, production records, generated caches, and temporary test artifacts out of the repository. Document destructive or high-impact actions and confirmation gates.
6. Keep `agents/openai.yaml` aligned with the skill. Quote interface strings and ensure `default_prompt` explicitly invokes `$<skill-name>`. Regenerate UI metadata when it becomes stale.
7. For a new, removed, or renamed skill, update both `README.md` and `README.zh-TW.md` catalogs and any architecture or installation examples that claim to enumerate it. Repair all `$kalmes-*` and relative reference links.
8. Save text as strict UTF-8. Do not mechanically rewrite unrelated files or line endings.

## Validation gate

Run the bundled repository validator from the repository root:

```text
python kalmes-update-skills/scripts/validate_repository.py . --require-canonical-origin
```

Also run the available skill framework validator against every top-level skill directory. Run representative tests for changed scripts and realistic forward-tests for complex workflow changes. Then run `git diff --check`, inspect the complete diff, and confirm no unrelated files, secrets, placeholders, generated artifacts, or broken links are present.

Do not declare success or publish while any required check fails. If a framework validator fails only because Windows selected a legacy locale, rerun it in explicit UTF-8 mode; do not convert already-valid UTF-8 files to the locale encoding.

## Publication gate

Before an authorized commit or push, fetch again and re-evaluate status and ahead/behind state. Stage only intended paths, inspect the staged diff, use a concise change-focused commit message, and push a non-force branch. Prefer a `codex/` topic branch and pull request for review; push directly to `main`, create tags, or create a GitHub release only when explicitly requested.

## Completion

Report the repository path, canonical remote verification, branch and ahead/behind state, operation performed, skills and supporting files changed, UTF-8 and structural validation results, script/forward-test results, diff scope, commit/push/PR/release status, and remaining decisions. Never claim GitHub is updated unless the corresponding remote action succeeded.
