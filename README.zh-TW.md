# Kalmes Skills

[English](./README.md) | [繁體中文](./README.zh-TW.md)

一套提供 AI Coding Agent（例如 OpenAI Codex）使用的 **Kalmes Agent Skills**。

Kalmes Skills 將操作 Kalmes 所需要的 Workflow、API 規範、安全規則、開發流程與技術參考資料拆分成可重複使用的 Skill，讓 AI Agent 能夠理解如何連線、操作、開發、設定與維護 Kalmes 系統。

---

## 什麼是 Kalmes Skills？

Kalmes Skills 是一組可重複使用的 Agent Skill，讓 AI Agent 知道如何執行特定的 Kalmes 操作。

與其將所有 Kalmes API、開發規範、安全規則與操作流程全部放進一個大型 Prompt，Kalmes Skills 將不同能力拆分成各自獨立的 Skill。

例如：

```text
使用者需求
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

AI Agent 可以依照當前任務選擇適合的 Skill，只有在需要時才載入詳細的操作內容。

這樣可以讓 Kalmes 相關知識更加：

- 可重複使用
- 模組化
- 容易維護
- 可以互相組合
- 容易更新
- 更安全地被 AI Agent 執行

---

# Skill 清單

## Installation

| Skill                                      | 用途                                                                                         |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- |
| [`kalmes-install-v2`](./kalmes-install-v2) | 在 Windows、macOS 或 Linux 安裝 Docker 與部署 Kalmes V2，並驗證容器及系統就緒狀態。           |

## Orchestration

| Skill                                              | 用途                                                                                                     |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [`kalmes-build-software`](./kalmes-build-software) | 建立完整的 Kalmes 功能，協調資料結構、API、HTML、UI 設定、權限、測試、封裝、Release 與 Rollback 等流程。 |

## Connection & API

| Skill                                            | 用途                                                                     |
| ------------------------------------------------ | ------------------------------------------------------------------------ |
| [`kalmes-connect`](./kalmes-connect)             | 連線並驗證 Kalmes HTTP API、確認系統可用狀態，並安全地管理登入 Session。 |
| [`kalmes-invoke-module`](./kalmes-invoke-module) | 透過已驗證的 HTTP Request 呼叫既有的 Kalmes Extra Code API Module。      |

## Data & FAP

| Skill                                          | 用途                                                                               |
| ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| [`kalmes-analyze-data`](./kalmes-analyze-data) | 對 Kalmes 資料進行唯讀的探索、查詢、關聯、彙整與資料分析。                         |
| [`kalmes-manage-data`](./kalmes-manage-data)   | 建立與管理 Kalmes Runtime Record、檔案、History、Embedded Value 與 Business Data。 |
| [`kalmes-manage-fap`](./kalmes-manage-fap)     | 檢視、設計、建立、更新與退役 Kalmes FAP Collection Definition 及其關聯。           |

## Development & UI

| Skill                                          | 用途                                                                                       |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [`kalmes-develop-code`](./kalmes-develop-code) | 開發與維護 Kalmes Extra Code API、HTML Page、Job、Scheduler 與可重複使用的 Python Module。 |
| [`kalmes-configure-ui`](./kalmes-configure-ui) | 設定 Kalmes Branding、Embedded Page、Menu、Route、Label、Language Pack 與 UI 相關設定。    |

## Access & Operations

| Skill                                                | 用途                                                                                      |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [`kalmes-manage-access`](./kalmes-manage-access)     | 管理 Kalmes User、Role、Permission、Menu Restriction、Action Restriction 與 Page Access。 |
| [`kalmes-manage-subtasks`](./kalmes-manage-subtasks) | 建立、檢視、執行與監控 Kalmes 內部 Agent Sub Task Queue。                                 |
| [`kalmes-send-email`](./kalmes-send-email)           | 透過 Kalmes 寄送 HTML Email，並在需要時設定或排查 Kalmes Email Integration。              |

## Testing & Release

| Skill                                                | 用途                                                                                               |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [`kalmes-transfer-plugin`](./kalmes-transfer-plugin) | 安全地匯出、預檢、匯入、驗證及回滾一般或加密的 Kalmes Plugin tar 套件。                            |
| [`kalmes-test-release`](./kalmes-test-release)       | 驗證、封裝、Release、監控與 Rollback Kalmes 自訂功能。                                             |

## Skill Maintenance

| Skill                                            | 用途                                                                                          |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| [`kalmes-update-skills`](./kalmes-update-skills) | 安全地同步、編輯、驗證、安裝，並在明確授權後發布 canonical Kalmes Skills Repository。        |

---

# Repository 結構

每一個 Skill 都存放於自己的獨立目錄中。

典型的 Skill 結構如下：

```text
kalmes-example-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── ...
```

依照不同 Skill 的需求，也可能包含：

```text
scripts/
assets/
```

等其他目錄。

---

## `SKILL.md`

`SKILL.md` 是一個 Skill 最主要的操作說明文件。

其中可能包含：

- Skill 名稱
- Skill 描述
- 使用時機
- Preconditions
- Workflow
- 必要輸入
- 安全規則
- 驗證方式
- Completion Requirement
- 與其他 Kalmes Skills 的協作方式

`SKILL.md` 應盡量保持清楚、精簡，並以實際可執行的 Workflow 為主。

---

## `references/`

`references/` 用來保存 Agent 在需要更多技術細節時才需要載入的參考資料。

內容可能包含：

- Kalmes API Contract
- HTTP Request / Response 格式
- FAP 規範
- Data Structure 定義
- 開發流程
- Security 注意事項
- 範例
- 測試流程
- Release 流程

大量的技術細節應優先放入 `references/`，而不是全部塞進 `SKILL.md`。

---

## `agents/`

`agents/` 用來保存不同 Agent Environment 所需要的 Metadata 或設定。

例如：

```text
agents/
└── openai.yaml
```

這樣可以保留 Agent-specific 的設定，同時避免將這些內容混入主要的 Skill Workflow。

---

# 安裝方式

依照不同使用情境，可以使用以下方式安裝 Kalmes Skills。

---

## 方法一 — Clone 完整 Kalmes Skills

最建議的方式是直接 Clone 完整 Repository：

```bash
git clone https://github.com/Alexandro-0/kalmes-skills.git
```

推薦安裝完整 Repository，是因為許多 Kalmes Skills 之間具有協作關係。

例如：

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

安裝完整的 Skills Collection，可以確保 Agent 在執行複雜 Workflow 時能取得所需要的相關 Skills。

---

## 方法二 — 安裝到 Codex Repository

若要在 OpenAI Codex 中使用 Repository-local Skills，可以將 Skills 放到：

```text
your-project/
└── .agents/
    └── skills/
        ├── kalmes-connect/
        ├── kalmes-analyze-data/
        ├── kalmes-manage-data/
        └── ...
```

例如：

```text
kalmes-skills/
    ↓
your-project/.agents/skills/
```

安裝完成後，Agent 即可探索可使用的 Skills，並在需要時載入對應的 `SKILL.md`。

---

## 方法三 — 只安裝特定 Skill

你也可以只安裝需要的 Skill。

例如：

```text
.agents/
└── skills/
    ├── kalmes-connect/
    └── kalmes-analyze-data/
```

如果只安裝部分 Skills，建議先檢查該 Skill 的 `SKILL.md`，確認是否有引用其他 `$kalmes-*` Skill。

對大部分需要連線至實際 Kalmes Environment 的 Workflow 而言：

```text
kalmes-connect
```

可以視為基礎 Skill。

---

## 不使用 Git 下載

如果使用者沒有安裝 Git，也可以直接透過 GitHub：

```text
Code → Download ZIP
```

下載並解壓縮整個 Repository。

接著將需要的 Skill Directory 複製到 Agent Skills 目錄即可。

一個 Skill 應該視為完整的 Directory，例如：

```text
kalmes-analyze-data/
├── SKILL.md
├── agents/
└── references/
```

如果 Skill 有其他支援檔案，不建議只單獨複製 `SKILL.md`。

---

# 如何使用 Kalmes Skills

當 Skills 已經安裝到 AI Agent 的環境後，一般情況下可以直接使用自然語言描述需求。

例如：

```text
分析我的 Kalmes 生產紀錄，
整理最近 30 天每個工作區的生產數量。
```

Agent 可以選擇：

```text
kalmes-analyze-data
```

如果是比較大型的開發需求：

```text
幫我建立一套 Kalmes 設備維護功能，
需要設備資料、維護紀錄、HTML 管理頁面、角色與選單。
```

Agent 可以透過：

```text
kalmes-build-software
```

協調整個 Workflow。

如果 Agent Environment 支援，也可以明確指定 Skill：

```text
使用 $kalmes-analyze-data 分析生產紀錄。
```

或：

```text
使用 $kalmes-build-software 完成這個功能。
```

---

# 連線至 Kalmes

需要操作實際 Kalmes Environment 的 Skills，可能需要以下資訊：

```text
Kalmes URL
Kalmes account
Kalmes password
Target environment
```

例如 Target Environment：

```text
development
staging
production
```

實際需要哪些資料，依照各 Skill 的 `SKILL.md` 定義。

`kalmes-connect` 提供其他 Kalmes Skills 共用的 Authentication 與 Connection Workflow。

---

# 安全性

部分 Kalmes Skills 可以對實際 Kalmes 系統執行具有權限或破壞性的操作。

例如：

- 建立或修改 Business Data
- 修改 FAP Collection Definition
- Upload 或執行 Extra Code
- 修改 User
- 修改 Role
- 修改 Permission
- 修改 Menu 或系統設定
- 執行 Job
- 設定 Scheduler
- 發送 Email
- Import Configuration
- 啟用或修改 Plugin
- Delete 或 Retire Resource
- Deploy 至 Production

在允許 AI Agent 操作實際環境之前，應先確認相關 `SKILL.md` 中的 Workflow 與 Safety Rule。

---

## Credential 規則

不要將 Kalmes Credential 寫入：

```text
SKILL.md
Source Code
Git Repository
Log
Report
Committed Configuration
公開文件
```

建議優先使用：

- Agent 專用的 Kalmes API Key，不要直接提供帳號密碼
- Temporary Credential
- Environment Variable
- Secret Management System
- Least-Privilege Account
- Environment-specific Account

請依管理者角色，從 **進階設定 → API Keys** 或 **API Access → API Keys** 建立 Agent Key，只綁定工作所需的 SuperUser、Admin 或 IT 帳號，將 64 字元 Key 存入 Secret Manager，並撤銷臨時或已暴露的 Key。帳號密碼登入僅作為備援方式。

Production Environment 的操作應搭配適當的：

- Access Control
- Validation
- Backup
- Monitoring
- Audit Log
- Rollback Procedure

---

# Skill 設計原則

Kalmes Skills 遵循以下幾項核心設計原則。

---

## Focused Responsibility

每個 Skill 應該代表一個明確且可辨識的能力。

不要把所有 Kalmes 功能全部塞進一個大型 Skill。

例如：

```text
kalmes-connect
kalmes-manage-data
kalmes-manage-fap
kalmes-develop-code
```

每個 Skill 都有自己負責的範圍。

---

## Progressive Disclosure

Agent 一開始只需要知道：

- Skill 是做什麼的
- 什麼情況應該使用

當 Skill 被選用時，才載入完整的 `SKILL.md`。

如果需要更深入的 API 或技術細節，再進一步讀取：

```text
references/
```

這樣可以減少不必要的 Context 使用量。

---

## Composable Workflows

Skill 可以互相協作，也可以將特定操作交給其他專門的 Skill。

例如：

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

因此複雜功能可以由多個較小、職責清楚的 Skills 組合完成。

---

## Safe Live-System Operation

Kalmes Skills 應清楚區分不同影響程度的操作。

例如：

```text
Read Operation
    ↓
Write Operation
    ↓
Destructive Operation
    ↓
Production Operation
```

影響程度越高的操作，應要求更嚴格的：

- Validation
- User Intent
- Safety Check
- Rollback Planning

---

# 建立新的 Kalmes Skill

建立新的 Skill 時，使用 `kalmes-` 作為名稱前綴：

```text
kalmes-your-skill/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
```

最基本的 `SKILL.md` 可以從以下 Front Matter 開始：

```yaml
---
name: kalmes-your-skill
description: Describe what this Skill does and when an agent should use it.
---
```

接著定義 Workflow：

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

每個 Skill 應盡可能聚焦在單一且明確的 Capability。

如果需要大量 API 文件、範例或技術規格，建議放入：

```text
references/
```

而不是讓 `SKILL.md` 變得過於龐大。

---

# Contributing

歡迎對 Kalmes Skills 提出改善與貢獻。

新增或修改 Skill 時，請遵循以下原則：

1. Skill 應聚焦於明確的使用者目標。
2. 保持 `kalmes-*` 的命名規則。
3. `SKILL.md` 應保持精簡並以實際操作 Workflow 為主。
4. 詳細技術文件放入 `references/`。
5. 不要提交 Credential、Access Token、Private URL 或 Production Data。
6. 明確說明 Destructive 或 High-impact Operation。
7. 確認其他 Kalmes Skill 的 Reference 是否正確。
8. 提交變更前應測試 Workflow。

如果是較大的修改，建議建立 Issue 或 Pull Request，並描述：

```text
Problem
Expected workflow
Affected Skills
Compatibility considerations
Security considerations
```

---

# Versioning

Kalmes Skills 可以隨著 Kalmes 功能與 Workflow 的演進而持續更新。

進行較大的修改時，建議記錄：

- Breaking Change
- 新增 Capability
- Deprecated Workflow
- Kalmes Version Requirement
- Compatibility Consideration

未來也可以透過 GitHub Release 提供個別 Skill 的版本化 Download Package。

例如：

```text
kalmes-analyze-data-1.2.0.zip
kalmes-build-software-2.0.0.zip
kalmes-connect-1.1.0.zip
```

讓使用者可以直接下載特定版本的 Skill。

---

# License

本專案採用 **Apache License 2.0**。

詳細內容請參考：

[`LICENSE`](./LICENSE)

---

# 關於 Kalmes Skills

Kalmes Skills 提供一層可重複使用的 Agent Workflow Layer，讓 AI Agent 能夠操作與擴充 Kalmes。

目標是讓複雜的 Kalmes 操作具備：

**可探索、可組合、可重複執行、可維護，並且能更安全地由 AI Agent 執行。**

不需要在每一次 Prompt 中重新教 AI Agent 整套 Kalmes 平台。

只需要安裝 Kalmes Skills，讓 Agent 在需要時載入正確的操作知識即可。
