# skills · 通用 Agent 技能源 + 候选评审区

被验证有效的知识进一步固化为 Agent 技能，分发到全员。

**这是飞轮最高形态**：不是"让 AI 知道"，而是"让 AI 能干"。

## 定位：Agent 无关

BootX 团队用多个 Agent（Codex / WorkBuddy / Trae / Cursor 等），所以本目录存的是**中性的 `SKILL.md`**（能力描述 + 触发条件 + 执行步骤 + 可复用提示词/脚本），不绑定任何单一工具。

本目录的角色是「**源仓库 + 评审区**」：
1. 知识条目在 `knowledge/` 被 ≥3 次复用验证有效 → 在这里起草 `SKILL.md`。
2. 团队评审通过后，各人按自己用的 Agent 挂载（见下表）。
3. 通过本仓库把技能源分发到全员。

## 各 Agent 如何挂载（示意，按需维护）

| Agent | 挂载方式 |
|-------|---------|
| Codex | 复制进项目 `AGENTS.md` 或 Codex skills 约定 |
| WorkBuddy | 复制到 `~/.workbuddy/skills/`（用户级）或 `{项目}/.workbuddy/skills/`（项目级） |
| Trae / Cursor | 写成项目规则（Rules / `.cursor/rules`） |
| 其他 | 把 `SKILL.md` 内容注入该工具的规则/上下文即可 |

> 原则：挂载机制各工具不同，但**技能本体（这份 Markdown）是通用的**——存一份，多处挂载。

## 结构

每个技能一个子目录：`skill-主题/`，含 `SKILL.md`（及可选 `references/`、`scripts/`、`assets/`）。

例：`skill-requirements-plan/`、`skill-weekly-clean/`。

## 固化标准

某条知识被 ≥3 次不同人复用且验证有效，即可从 `knowledge/` 提炼入此目录。

> 提示：起步阶段不必急着做技能。先让知识在 `knowledge/` 里被各 Agent 检索到，等某条知识反复被用到，再固化成技能。
