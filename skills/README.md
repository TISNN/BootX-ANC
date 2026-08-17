# skills · 技能源仓库 + 候选评审区

被验证有效的知识进一步固化为 Agent 技能（Skill），分发到全员。

**这是飞轮最高形态**：不是"让 AI 知道"，而是"让 AI 能干"。

## ⚠️ 重要：这里不是 WorkBuddy 的加载位置

WorkBuddy 实际从以下目录加载技能，**不是这个 git 仓库**：

- 用户级（跨项目）：`~/.workbuddy/skills/`
- 项目级（当前项目）：`{workspace}/.workbuddy/skills/`

本目录的角色是「**源仓库 + 评审区**」：
1. 知识条目在 `knowledge/` 被 ≥3 次复用验证有效 → 在这里起草 `SKILL.md`。
2. 团队评审通过后，用 skill-creator 正式创建，或把 `SKILL.md` 复制到上述加载目录。
3. 通过本仓库把技能配置分发到全员。

## 结构

每个技能一个子目录：`skill-主题/`，含 `SKILL.md`（及可选 `references/`、`scripts/`、`assets/`），遵循 WorkBuddy Skill 格式。

例：`skill-requirements-plan/`、`skill-weekly-clean/`。

## 固化标准

某条知识被 ≥3 次不同人复用且验证有效，即可从 `knowledge/` 提炼入此目录。
