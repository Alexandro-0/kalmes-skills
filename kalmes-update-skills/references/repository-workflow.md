# Kalmes Skills repository workflow

## Contents

1. Canonical repository
2. Safe discovery and synchronization
3. Source update conventions
4. Installed-copy refresh
5. Validation
6. Commit and publication
7. Completion record

## 1. Canonical repository

Use this public repository as the source of truth:

```text
https://github.com/Alexandro-0/kalmes-skills
https://github.com/Alexandro-0/kalmes-skills.git
```

The default integration branch is `main`. Verify the live remote and default branch instead of relying on a cached assumption. A contributor fork may be valid for a pull-request workflow, but never describe it as the canonical `origin` and never publish to an unexpected remote.

Repository-level files include the English and Traditional Chinese READMEs, `.gitattributes`, `LICENSE`, and top-level `kalmes-*` skill directories. Each skill normally contains `SKILL.md`, `agents/openai.yaml`, and only the scripts, references, or assets it actually needs.

## 2. Safe discovery and synchronization

Discover a candidate clone:

```text
git -C <candidate> rev-parse --show-toplevel
git -C <repo> status --short --branch
git -C <repo> remote -v
git -C <repo> branch --show-current
git -C <repo> rev-parse --abbrev-ref --symbolic-full-name @{upstream}
```

On PowerShell, quote `@{upstream}` when needed so the shell does not parse it. Confirm that `origin` normalizes to the canonical URL before a maintainer publication.

Fetch without changing the worktree:

```text
git -C <repo> fetch origin
git -C <repo> rev-list --left-right --count origin/main...HEAD
```

The first count is remote-only commits (local is behind); the second is local-only commits (local is ahead).

Use this decision table:

| Worktree | Behind | Ahead | Action |
| --- | ---: | ---: | --- |
| clean | 0 | 0 | Already synchronized; validate. |
| clean | greater than 0 | 0 | Fast-forward with `git merge --ff-only origin/main`, then validate. |
| clean | 0 | greater than 0 | Preserve local commits; do not pull. Validate and publish only if requested. |
| clean | greater than 0 | greater than 0 | Diverged; report both sides and require an explicit merge/rebase choice. |
| dirty | any | any | Preserve changes; do not sync until overlap and ownership are resolved. |

Do not use `git reset --hard`, destructive checkout, automatic stash, force pull, or force push as a synchronization shortcut. Do not delete and reclone over a working directory.

If no clone exists and the user asked to install or create one, first resolve a specific destination, ensure it does not contain unrelated data, and run:

```text
git clone https://github.com/Alexandro-0/kalmes-skills.git <destination>
```

## 3. Source update conventions

Before editing an existing skill:

1. Read its complete `SKILL.md`.
2. Read each directly linked reference needed for the requested change.
3. Inspect `agents/openai.yaml` and cross-skill `$kalmes-*` references.
4. Check both READMEs for catalog or example entries.
5. Review the current diff so user changes remain distinct.

Required invariants:

- Top-level skill folder and frontmatter `name` match and use lowercase letters, digits, and hyphens.
- `SKILL.md` frontmatter contains only `name` and `description`.
- The display brand is exactly `Kalmes`; contract identifiers retain their required lowercase or uppercase form.
- UI metadata strings are quoted, the short description remains concise, and `default_prompt` contains `$<skill-name>`.
- Relative links resolve from the containing `SKILL.md`.
- Detailed specifications live in `references/`, preferably one level from `SKILL.md`.
- Text is UTF-8; scripts and metadata contain no credentials or private production material.
- High-impact workflows identify scope, confirmation, verification, and rollback.

When adding a skill, use the available skill initialization tooling rather than hand-building inconsistent scaffolding. Create only necessary resource directories, remove every placeholder, add the skill to both catalogs, and integrate it with related workflows only where the dependency is real.

When removing or renaming a skill, search the entire repository for folder names, `$skill` invocations, links, UI prompts, catalog rows, examples, and installation instructions. Treat renaming as a compatibility change and preserve an old identifier unless the user accepts breakage.

## 4. Installed-copy refresh

First determine whether the installed skills directory is itself the canonical Git clone, a repository-local `.agents/skills` copy, or a personal skills directory. Do not assume these are interchangeable.

For a Git clone, use the synchronization decision table and validate after fast-forwarding.

For copied skills:

1. Validate the canonical source clone.
2. Enumerate only the skill directories the user asked to refresh.
3. Compare source and installed copies and identify local-only files or edits.
4. Preserve or back up local customizations before replacement.
5. Copy each selected skill as a complete directory so `SKILL.md`, `agents/`, and linked resources remain consistent.
6. Validate the destination and tell the user whether the host application or task must be restarted for discovery.

Never recursively overwrite a broad personal skills home merely because one Kalmes skill needs an update. Do not alter system or third-party skills.

## 5. Validation

Run the bundled repository validator:

```text
python kalmes-update-skills/scripts/validate_repository.py <repo>
```

Before maintainer publication, require canonical origin:

```text
python kalmes-update-skills/scripts/validate_repository.py <repo> --require-canonical-origin
```

Then run the current skill framework validator against every top-level `kalmes-*/SKILL.md`. On Windows, use explicit UTF-8 mode if the validator otherwise inherits a legacy code page.

Additional required checks:

```text
git -C <repo> diff --check
git -C <repo> status --short
git -C <repo> diff
git -C <repo> diff --cached
```

Run each changed script on representative valid and invalid inputs. For workflow-heavy changes, forward-test with user-like requests and no leaked expected answer. Remove temporary artifacts before completion.

## 6. Commit and publication

Local edits do not authorize a commit, and a commit does not authorize a push. A push does not authorize a pull request, tag, release, or merge. Perform only the remote action explicitly requested by the user.

For an authorized topic-branch workflow:

```text
git -C <repo> switch -c codex/<short-change-name>
git -C <repo> add -- <exact paths>
git -C <repo> diff --cached
git -C <repo> commit -m "<concise change summary>"
git -C <repo> fetch origin
git -C <repo> push -u origin codex/<short-change-name>
```

Re-evaluate ahead/behind and inspect staged content before committing or pushing. Never stage unrelated dirty files. Never embed GitHub tokens in repository files, shell history, skill instructions, remote URLs, or reports.

Prefer a pull request into `main` for review. Describe the problem, expected workflow, affected skills, compatibility, security, validation, and rollback or migration considerations. Create a tag or release only for an explicitly approved version and verified commit; do not invent version numbers.

## 7. Completion record

Return:

- canonical and actual remote;
- repository path, branch, upstream, and ahead/behind counts;
- synchronization, source edit, installed refresh, or publication operation;
- changed skills and repository files;
- validator, UTF-8, link, script, and forward-test results;
- remaining dirty or untracked files;
- commit hash and branch only if committed;
- pushed branch, pull-request URL, tag, or release URL only if those actions succeeded;
- unresolved compatibility or publication decisions.
