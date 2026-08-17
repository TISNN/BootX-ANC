# 贡献与协作规范（CONTRIBUTING）

适用于所有 BootX 团队成员。目标：让知识回流零摩擦、可追溯、可复用。

---

## 1. 投递产出物（人人要做）

- **往哪丢**：`00_inbox/`，清洗前不要自己归类。
- **命名**：`YYYYMMDD-作者-主题.md`
  - 例：`20260817-evan-威吉瑞报价模型.md`、`20260820-lin-周报模板.md`
- **格式**：用 `_templates/inbox-submission.md` 模板，至少包含：
  - 背景：为什么做这件事
  - 产出：核心结论 / 产物链接
  - 可复用点：哪些方法、模板、决策值得下次直接用
  - 坑：踩过什么雷
- **提交**：`git add 00_inbox/ && git commit -m "inbox: 主题" && git push`

> 不要求完美。哪怕只写三行"这次怎么做的、下次注意什么"也行。飞轮靠量转动。

---

## 2. 命名与归类约定

- **投递文件**：`YYYYMMDD-作者-主题.md`（中文主题可，作者用英文/拼音缩写）。
- **知识条目文件**：`主题关键词.md`（小写中划线或中文均可，用关键词命名，便于检索）。
- 知识条目在 frontmatter 里标 `layer`（facts / interactions / actions），**不再按目录分类**。
- 周报：`knowledge/YYYY-Www.md`，同一主题的多份材料在周报里用二级标题聚合，原始材料留 `archive/`。

---

## 3. 清洗流程（自动化执行，人工可复核）

每周定时任务读取 `00_inbox/` 全部新增文件 → 按 `_automation/weekly-clean-prompt.md` 提炼 →
写入 `knowledge/`（知识条目带 `layer` 标签）+ 聚合 `knowledge/YYYY-Www.md` 周报 →
**确认清洗成功后**将已处理原始文件移入 `archive/` → `git commit + push`。

人工复核节点：清洗产出进入主分支前，由一名成员（轮值）确认知识条目无敏感信息、归类准确。

> 归档安全规则：只有清洗步骤确认完成、知识已落盘，才移动原始文件。清洗失败则保留 `00_inbox/` 原样，下轮重试。

---

## 4. 技能固化（飞轮最高形态）

- 当某条知识被反复验证有效（≥3 次被不同人复用），从 `knowledge/` 提炼为 Agent 技能，**源文件放进 `skills/` 作为候选评审区**。
- **注意**：`skills/` 是「源仓库 + 评审区」，不是 WorkBuddy 的加载位置。WorkBuddy 从以下位置加载技能：
  - 用户级：`~/.workbuddy/skills/`
  - 项目级：`{workspace}/.workbuddy/skills/`
- 正式上线流程：候选在 `skills/` 评审通过后，用 skill-creator 正式创建（或把 `SKILL.md` 复制到上述加载目录），再通过仓库分发到全员。
- 技能遵循 WorkBuddy Skill 格式（`SKILL.md` + 可选 `references/` `scripts/` `assets/`）。

---

## 5. 敏感数据与边界

- 客户合同、财务明细、个人隐私：**不入库**或脱敏后入库（用占位符代替真实姓名/金额）。
- 内部未公开战略：标注 `confidential`，仅团队核心成员可见分支。
- 一切入库内容默认可被团队 Agent 检索——投稿前请自审。

---

## 6. Git 工作流

- 主分支：`main`
- 日常：直接在 `main` 上 `commit + push`（小团队、低冲突）。
- 大改动（结构调整、技能上线）：开短期分支 → PR → 轮值复核合并。
- 冲突：文件级锁（不同人不同文件），极少冲突；真冲突时人工合并。
- 远程仓库：首次使用前需配置 `git remote add origin <url>`；未配置远程时清洗只 commit 不 push。
