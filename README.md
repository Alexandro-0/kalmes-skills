# Kalmes Skills

[English](./README.md) | [繁體中文](./README.zh-TW.md)

A collection of reusable Agent Skills for working with **Kalmes** through AI coding agents such as OpenAI Codex.

Kalmes Skills provide structured workflows, operational knowledge, API conventions, safety rules, and supporting references that help AI agents understand how to work with, extend, configure, and operate a Kalmes environment.

---

## What are Kalmes Skills?

Kalmes Skills are reusable instruction bundles that teach an AI agent how to perform specific operations against a Kalmes environment.

Instead of placing every Kalmes API convention, workflow, safety rule, and implementation detail into a single prompt, capabilities are separated into focused Skills.

For example:

```text
User Request
    │
    ▼
kalmes-build-software
    │
    ├── kalmes-connect
    ├── kalmes-manage-fap
    ├── kalmes-manage-data
    ├── kalmes-develop-code
    ├── kalmes-configure-ui
    ├── kalmes-manage-access
    ├── kalmes-transfer-plugin
    └── kalmes-test-release
```

An AI agent can select the appropriate Skill for a task and load detailed instructions only when needed.

This allows Kalmes-related knowledge to remain:

- reusable
- modular
- maintainable
- composable
- easier to update
- safer to execute

---

# Skill Catalog

## Installation

| Skill                                          | Purpose                                                                                                      |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [`kalmes-install-v2`](./kalmes-install-v2)     | Install Docker and deploy Kalmes V2 on Windows, macOS, or Linux, then validate the containers and readiness. |

## Orchestration

| Skill                                              | Purpose                                                                                                                                                         |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`kalmes-build-software`](./kalmes-build-software) | Build complete Kalmes features by coordinating data structures, APIs, HTML, UI configuration, permissions, testing, packaging, release, and rollback workflows. |

## Connection & API

| Skill                                            | Purpose                                                                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| [`kalmes-connect`](./kalmes-connect)             | Connect and authenticate to a Kalmes HTTP API, validate readiness, and manage authenticated sessions safely. |
| [`kalmes-invoke-module`](./kalmes-invoke-module) | Invoke existing Kalmes Extra Code API modules through authenticated HTTP requests.                           |

## Data & FAP

| Skill                                          | Purpose                                                                                          |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [`kalmes-analyze-data`](./kalmes-analyze-data) | Perform read-only discovery, querying, joining, summarization, and analysis of Kalmes data.      |
| [`kalmes-manage-data`](./kalmes-manage-data)   | Create and manage Kalmes runtime records, files, history, embedded values, and business data.    |
| [`kalmes-manage-fap`](./kalmes-manage-fap)     | Inspect, design, create, update, and retire Kalmes FAP collection definitions and relationships. |

## Development & UI

| Skill                                          | Purpose                                                                                                    |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [`kalmes-develop-code`](./kalmes-develop-code) | Develop and maintain Kalmes Extra Code APIs, HTML pages, jobs, schedulers, and reusable Python modules.    |
| [`kalmes-configure-ui`](./kalmes-configure-ui) | Configure Kalmes branding, embedded pages, menus, routes, labels, language packs, and UI-related settings. |

## Access & Operations

| Skill                                                | Purpose                                                                                                  |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`kalmes-manage-access`](./kalmes-manage-access)     | Manage Kalmes users, roles, permissions, menu restrictions, action restrictions, and page access.        |
| [`kalmes-manage-subtasks`](./kalmes-manage-subtasks) | Create, inspect, execute, and monitor Kalmes internal Agent Sub Task queues.                             |
| [`kalmes-send-email`](./kalmes-send-email)           | Send HTML email through Kalmes and configure or troubleshoot the Kalmes email integration when required. |

## Testing & Release

| Skill                                                | Purpose                                                                                                      |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [`kalmes-transfer-plugin`](./kalmes-transfer-plugin) | Safely export, preflight, import, verify, and roll back plain or encrypted Kalmes plugin tar packages.       |
| [`kalmes-test-release`](./kalmes-test-release)       | Verify, package, release, monitor, and roll back Kalmes custom features.                                     |

## Skill Maintenance

| Skill                                            | Purpose                                                                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| [`kalmes-update-skills`](./kalmes-update-skills) | Safely synchronize, edit, validate, install, and explicitly publish the canonical Kalmes Skills repository. |

---

# Repository Structure

Each Skill is stored in its own directory.

A typical Skill structure looks like:

```text
kalmes-example-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── ...
```

Depending on the Skill, additional directories such as `scripts/` or `assets/` may also be included.

---

## `SKILL.md`

`SKILL.md` is the primary instruction file for a Skill.

It may define:

- Skill name
- Skill description
- activation conditions
- preconditions
- workflow instructions
- required inputs
- safety requirements
- validation procedures
- completion requirements
- interactions with other Kalmes Skills

The goal is to keep the main Skill workflow clear and operational.

---

## `references/`

The `references/` directory contains supporting technical documentation that an agent can load when additional details are required.

References may include:

- Kalmes API contracts
- HTTP request and response formats
- FAP conventions
- data structure definitions
- implementation procedures
- security considerations
- examples
- testing procedures
- release procedures

Large technical details should generally be stored in `references/` instead of making `SKILL.md` unnecessarily large.

---

## `agents/`

The `agents/` directory contains agent-specific metadata and configuration.

For example:

```text
agents/
└── openai.yaml
```

This allows a Skill to provide metadata for supported agent environments without mixing it into the main workflow documentation.

---

# Installation

There are several ways to install Kalmes Skills depending on how you intend to use them.

---

## Option 1 — Clone All Kalmes Skills

The recommended option is to clone the entire repository:

```bash
git clone https://github.com/Alexandro-0/kalmes-skills.git
```

This is recommended because many Kalmes Skills are designed to collaborate with other Skills.

For example:

```text
kalmes-build-software
        │
        ├── kalmes-connect
        ├── kalmes-manage-fap
        ├── kalmes-manage-data
        ├── kalmes-develop-code
        ├── kalmes-configure-ui
        ├── kalmes-manage-access
        ├── kalmes-transfer-plugin
        └── kalmes-test-release
```

Installing the complete collection ensures that related workflows are available when an agent needs them.

---

## Option 2 — Install into a Codex Repository

For repository-local usage with OpenAI Codex, place the Skills under:

```text
your-project/
└── .agents/
    └── skills/
        ├── kalmes-connect/
        ├── kalmes-analyze-data/
        ├── kalmes-manage-data/
        └── ...
```

For example:

```text
kalmes-skills/
    ↓
your-project/.agents/skills/
```

After installation, the agent can discover available Skills and load the appropriate `SKILL.md` when required.

---

## Option 3 — Install Selected Skills

Individual Skills may also be installed separately.

For example:

```text
.agents/
└── skills/
    ├── kalmes-connect/
    └── kalmes-analyze-data/
```

When installing individual Skills, review their `SKILL.md` files for dependencies or references to other `$kalmes-*` Skills.

For most workflows that communicate with a live Kalmes environment, `kalmes-connect` should be considered a foundational Skill.

---

## Download without Git

If Git is not available, use GitHub:

```text
Code → Download ZIP
```

Extract the repository and copy the required Skill directories into your Agent Skills directory.

A Skill should normally be copied as a complete directory.

For example:

```text
kalmes-analyze-data/
├── SKILL.md
├── agents/
└── references/
```

Do not copy only `SKILL.md` if the Skill contains supporting files.

---

# Using Kalmes Skills

Once the Skills are available to your AI agent, you can normally describe the task in natural language.

For example:

```text
Analyze production records from my Kalmes system and summarize
production quantity by workstation for the last 30 days.
```

The agent may select:

```text
kalmes-analyze-data
```

For a larger development request:

```text
Build a Kalmes maintenance management feature with equipment,
maintenance records, an HTML management page, roles, and menus.
```

The agent may coordinate the workflow through:

```text
kalmes-build-software
```

When supported by the agent environment, a Skill may also be explicitly requested:

```text
Use $kalmes-analyze-data to analyze the production records.
```

or:

```text
Use $kalmes-build-software to implement this feature.
```

---

# Connecting to Kalmes

Skills that interact with a live Kalmes environment may require information such as:

```text
Kalmes URL
Kalmes account
Kalmes password
Target environment
```

Example environment types:

```text
development
staging
production
```

The exact requirements are defined by each Skill.

`kalmes-connect` provides the common authentication and connection workflow used by other Kalmes Skills.

---

# Security

Some Kalmes Skills can perform privileged or destructive operations against a live Kalmes system.

These operations may include:

- creating or modifying business data
- modifying FAP collection definitions
- uploading or executing Extra Code
- changing users or roles
- changing permissions
- modifying menus and system configuration
- running jobs
- configuring schedulers
- sending email
- importing configuration
- activating or changing plugins
- deleting or retiring resources
- deploying changes to production

Always review the relevant `SKILL.md` before allowing an AI agent to operate against a live system.

---

## Credential Rules

Do not store Kalmes credentials in:

```text
SKILL.md
source code
Git repositories
logs
reports
committed configuration files
public documentation
```

Prefer:

- a dedicated Kalmes API key for Agents instead of an account password
- temporary credentials
- environment variables
- secret-management systems
- least-privilege accounts
- environment-specific accounts

Create Agent keys in **Advanced Settings → API Keys** or **API Access → API Keys**, depending on the manager role. Bind only the required SuperUser, Admin, or IT account, store the 64-character key in a Secret Manager, and revoke temporary or exposed keys. Use account/password login only as a fallback.

Production operations should use appropriate:

- access control
- validation
- backup
- monitoring
- audit logs
- rollback procedures

---

# Skill Design Principles

Kalmes Skills follow several core design principles.

---

## Focused Responsibility

Each Skill should represent a recognizable capability.

Avoid putting all Kalmes functionality into one large Skill.

For example:

```text
kalmes-connect
kalmes-manage-data
kalmes-manage-fap
kalmes-develop-code
```

Each Skill owns a specific area of responsibility.

---

## Progressive Disclosure

The agent initially needs only enough information to understand:

- what a Skill does
- when it should be used

Detailed instructions are loaded from `SKILL.md` when the Skill is selected.

Larger technical documentation remains in `references/` until required.

This helps reduce unnecessary context usage.

---

## Composable Workflows

Skills may collaborate with or delegate operations to other Skills.

For example:

```text
kalmes-build-software
        │
        ├── connect
        ├── define data
        ├── implement code
        ├── configure UI
        ├── configure access
        └── test & release
```

This allows complex workflows to be assembled from smaller specialized capabilities.

---

## Safe Live-System Operation

Kalmes Skills should clearly distinguish between different levels of system impact.

For example:

```text
Read operation
    ↓
Write operation
    ↓
Destructive operation
    ↓
Production operation
```

Higher-impact operations should require stronger validation, explicit user intent, and appropriate rollback planning.

---

# Creating a New Kalmes Skill

Create a new directory using the `kalmes-` prefix:

```text
kalmes-your-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
```

A minimal `SKILL.md` may begin with:

```yaml
---
name: kalmes-your-skill
description: Describe what this Skill does and when an agent should use it.
---
```

Then define the workflow:

```markdown
# Your Kalmes Skill

## Preconditions

Describe required inputs and environment requirements.

## Workflow

1. Validate inputs.
2. Connect to Kalmes when required.
3. Perform the operation.
4. Validate the result.

## Safety

Define operations that require additional validation or protection.

## Completion

Define what information should be returned when the task is complete.
```

Keep each Skill focused on one recognizable capability.

If extensive API documentation, examples, or technical specifications are required, place them under `references/`.

---

# Contributing

Contributions are welcome.

When modifying or adding a Skill:

1. Keep the Skill focused on a clear user goal.
2. Preserve the `kalmes-*` naming convention.
3. Keep `SKILL.md` concise and operational.
4. Put detailed technical documentation under `references/`.
5. Do not include credentials, access tokens, private URLs, or production data.
6. Explicitly document destructive or high-impact operations.
7. Verify references to other Kalmes Skills.
8. Test the workflow before submitting changes.

For substantial changes, open an Issue or Pull Request describing:

```text
Problem
Expected workflow
Affected Skills
Compatibility considerations
Security considerations
```

---

# Versioning

Kalmes Skills may evolve independently as their workflows and Kalmes capabilities change.

When introducing significant changes, consider documenting:

- breaking changes
- new capabilities
- deprecated workflows
- required Kalmes versions
- compatibility considerations

Future releases may provide individual downloadable Skill packages and versioned release artifacts.

---

# License

This project is licensed under the **Apache License 2.0**.

See [`LICENSE`](./LICENSE) for details.

---

# About Kalmes Skills

Kalmes Skills provide a reusable Agent workflow layer for interacting with and extending Kalmes.

The goal is to make complex Kalmes operations:

**discoverable, composable, repeatable, maintainable, and safer for AI agents to execute.**

Instead of teaching an agent the entire Kalmes platform in every prompt, install the Skills once and allow the agent to load the right operational knowledge when it needs it.
