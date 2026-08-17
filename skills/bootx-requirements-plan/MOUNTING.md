# 挂载说明 · 跨 Agent 通用

本技能本体是 `SKILL.md`（能力描述 + 触发条件 + 执行步骤 + 可复用脚本）。

**它不绑定任何单一 Agent**——`scripts/` 是纯 Python（任何能跑 Python 的环境都能用），`references/` 是纯 Markdown。唯一的 `name`/`description` YAML frontmatter 只是 WorkBuddy 技能加载器的元数据，其他 Agent 会忽略它，不影响能力本身。

各 Agent 按自己的机制挂载（把这份 SKILL.md 喂进对应位置即可）：

| Agent | 挂载方式 |
|-------|---------|
| **WorkBuddy** | 整个 `bootx-requirements-plan/` 目录复制到 `~/.workbuddy/skills/`（用户级）或 `{项目}/.workbuddy/skills/`（项目级），WorkBuddy 自动识别 SKILL.md |
| **Codex** | 在 `AGENTS.md` 中 `@skills/bootx-requirements-plan/SKILL.md` 引用，或将 SKILL.md 要点并入项目约定 |
| **Trae / Cursor** | 写成项目规则（Rules / `.cursor/rules` / `.trae/rules`），把 SKILL.md 内容作为规则正文 |
| **其他** | 把 `SKILL.md` 内容注入该工具的系统提示 / 规则 / 上下文即可 |

## 与 BootX-ANC 飞轮的关系

- 本技能最初是从 `knowledge/` 中反复被复用的「客户需求确认与方案规划」经验固化而来（已 ≥3 次验证）。
- 后续交付产生的新经验，先丢 `00_inbox/`，由每周清洗提炼回 `knowledge/`，再回流到这里迭代。
- 本仓库是「源仓库 + 评审区」：改技能在这里改，再分发到各人自己的 Agent 加载位。
