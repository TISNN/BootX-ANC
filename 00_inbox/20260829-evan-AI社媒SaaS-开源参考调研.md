# AI 社媒 SaaS 开源参考项目调研

日期：2026-08-29
调研目的：为 AI 社媒 SaaS 寻找可参考的开源实现，重点看功能覆盖与架构设计
调研范围：用户指定 2 个项目 + 横向扩展 8 个项目

---

## 一、结论先行

**许可证是这次调研的第一约束，比功能更重要。** 你给的两个项目里，Beav 是 MIT-NC（非商用许可证，商用需作者书面许可），不能直接用于商业产品；dsh-oil-creator 是 MIT，可以放心用。

横向扫到的项目里，架构最成熟的两个（Postiz 35k stars、BrightBean Studio 2.2k stars）**都是 AGPL-3.0**。AGPL 与 GPL 的关键区别在于，通过网络提供服务也算分发，也就是说你一旦基于它们做 SaaS，就必须向用户公开全部源代码。这对闭源商业产品基本是致命的。

**推荐路线：以 BrightBean Studio 的架构设计为蓝本重写，不复用其代码；国内平台发布能力复用 MIT 许可的 Spreado；HITL 交互范式参考 LangChain 的 social-media-agent。**

详细组合见第五节。

---

## 二、项目全景

| 项目 | Stars | 技术栈 | 平台覆盖 | 许可证 | 商用可用性 |
|---|---|---|---|---|---|
| [Postiz](https://github.com/gitroomhq/postiz-app) | 35,237 | TypeScript / NestJS / NextJS / Prisma / Temporal | 14 个海外平台 | AGPL-3.0 | 受限，改后做 SaaS 须开源 |
| [Beav](https://github.com/Jamailar/Beav)（原 RedBox） | 高 | Electron 桌面端 | 采集为主，发布弱 | MIT-NC | **不可商用**，需书面授权 |
| [mixpost](https://github.com/inovector/mixpost) | 3,554 | PHP / Laravel / Vue | 海外主流 | 需核实 | 待定 |
| [social-media-agent](https://github.com/langchain-ai/social-media-agent) | 2,759 | TypeScript / LangGraph | Twitter、LinkedIn | 需核实（LangChain 系通常 MIT） | 大概率可用 |
| [BrightBean Studio](https://github.com/brightbeanxyz/brightbean-studio) | 2,209 | Python / Django 5 / HTMX / Alpine | 10+ 海外平台 | AGPL-3.0 | 受限，同上 |
| [trypost](https://github.com/trypostit/trypost) | 562 | PHP / Laravel / Vue | 海外主流 | 需核实 | 待定 |
| [Spreado](https://github.com/BadKid90s/Spreado) | 122 | Python / Playwright | **抖音、小红书、快手、视频号** | MIT | **可直接用** |
| [dsh-oil-creator](https://github.com/oil-oil/dsh-oil-creator) | 低 | TypeScript / DeepSeek Harness 插件 | 公众号、视频号（草稿） | MIT | **可直接用** |
| [meiti-ai / ALQQ](https://github.com/zhuixin8/meiti-ai) | 30 | Tauri + 云端 | **20+ 国内平台** | 专有，仓库无源码 | 仅功能对标 |
| [Wanmeiyifa](https://github.com/cml227/Wanmeiyifa) | 44 | 未详 | 国内多平台图文 | 需核实 | 待定 |

---

## 三、逐项目分析

### 3.1 Postiz（35k stars，架构天花板）

**功能**

- 多平台排期与发布，14 个海外平台（X、LinkedIn、Instagram、TikTok、YouTube、Facebook、Pinterest、Threads、Reddit、Slack、Discord、Mastodon、Bluesky、Dribbble）
- AI 内容生成、数据分析、团队协作
- 对外 API + NodeJS SDK + N8N 节点 + Make.com 集成
- 新出了 Postiz agent CLI，面向 OpenClaw 等 Agent

**架构**

- Pnpm workspaces 单仓多包
- NextJS 前端 + NestJS 后端
- Prisma + PostgreSQL
- **Temporal 做工作流编排**
- Resend 发邮件

**值得借鉴**

1. **Temporal 作为编排引擎**。这是 Postiz 架构里最有价值的一点。Temporal 原生支持长时任务、自动重试、状态持久化，更重要的是它支持 signal 机制，天然适合 human-in-the-loop——一个工作流可以挂起数天等待人工信号再继续。这跟我们的三档信任机制是同一个问题的工业级解法。
2. **明确的合规声明**值得抄作业。Postiz 在 README 里公开写：使用官方 OAuth 流程、不做自动化或爬取、不代持用户的 API Key、用户始终直接与平台认证。这段声明本身就是产品信任资产。
3. **生态集成**（N8N、Make、SDK）是获客渠道，不只是功能。

**风险**

AGPL-3.0。**用它的代码做闭源 SaaS 等于给自己的产品判了开源。** 只能参考架构思路，不能复用代码。

---

### 3.2 BrightBean Studio（2.2k stars，工程实现最成熟）

这个项目虽然 star 数不算顶级，但工程质量是这批里最高的，尤其是它把"多平台 SaaS 的脏活"都做完了。

**架构**

```
brightbean-studio/
├── config/settings/          # base / development / production / test 四套配置
├── apps/
│   ├── accounts/             # 自定义 User、OAuth、会话
│   ├── organizations/        # 组织
│   ├── workspaces/           # 工作空间
│   ├── members/              # RBAC、邀请、中间件
│   ├── settings_manager/     # 可级联的默认配置
│   ├── credentials/          # 平台凭据加密存储
│   └── common/               # 加密字段、作用域化的 model manager
├── providers/                # 平台 API 模块，一个平台一个文件
├── templates/components/     # HTMX 局部模板
└── theme/                    # django-tailwind
```

技术栈：Django 5.x + HTMX + Alpine.js + Tailwind 4 + PostgreSQL 16+，后台任务用 django-background-tasks（不依赖 Redis）。

**值得借鉴（重点）**

1. **`providers/` 一层一平台的模块化设计**。这是平台适配层的标准答案，新增平台不改核心代码。我们的平台适配器应当照抄这个目录范式。
2. **审批工作流分级**：`none / optional / internal / internal + client` 四档，带线程化评论、提醒、完整审计轨迹。这和我们设计的三档信任机制几乎完全一致，可以直接对齐。
3. **Client Portal**：30 天 magic-link，客户不用注册账号就能审批或拒绝帖子。对代理商和 MCN 客群极其重要，因为他们要给客户看内容。
4. **发布引擎的工程细节**：自动重试、按账号限流追踪、90 天发布审计日志。这些是"不封号"卖点的技术底座。
5. **诊断命令**：`diagnose_facebook --account-id <uuid>` 检查 token 实际授予的 scope、webhook 订阅了哪些字段。这类运维工具是自托管产品的刚需，README 里还专门点出"这一步容易漏且静默失败"。
6. **REST API + MCP server 双协议**，并且提供了预置的 agent skill。MCP 接口让外部 Agent（Claude Desktop、Cursor、自研 Agent）能直接驱动产品，这是 AI 原生产品的关键接口。
7. **白标友好**：每个工作空间可配 logo、配色、默认话题标签、首条评论、发布模板。对代理商客群是加分项。
8. **凭据加密存储 + 按组织隔离**，且平台凭据支持环境变量与 admin 两级配置。

**风险**

同为 AGPL-3.0。另外它只覆盖海外平台，国内平台要自己接。

---

### 3.3 social-media-agent（LangChain 官方，HITL 范式）

**功能**

输入一个 URL，自动生成 Twitter 与 LinkedIn 帖子。核心不在生成，而在**人在环路**的流程设计。

**架构**

- LangGraph 构建状态图
- 关键节点 `interrupt` 挂起，等待人审核、修改、接受或拒绝
- **Agent Inbox**：专门 UI 承载所有被挂起的事件，支持接受、响应等操作
- Arcade 处理社媒 OAuth（把认证外包出去）
- FireCrawl 抓网页，Supabase 存图
- Slack 频道作为输入源，cron 定时拉取后批量生成

**值得借鉴**

1. **interrupt + Agent Inbox 是 HITL 的通用范式**。这个模式跟平台无关，可以直接移植到我们的产品：Agent 生成内容后在审核节点挂起，人通过收件箱式 UI 批量处理，处理完工作流继续。我们 PRD 里的三档信任机制，技术实现就应该是这个样子。
2. **Slack 作为内容输入与通知通道**，大幅降低使用门槛。对国内可以换成企业微信或飞书。
3. **Cron + 异步**：往 Slack 丢链接，定时任务自动拉取并生成，人只管审核。这正是"定时自动创作 + 人工放行"的雏形。
4. **Prompt 分层配置**：`BUSINESS_CONTEXT` / `POST_STRUCTURE_INSTRUCTIONS` / `POST_CONTENT_RULES` / few-shot examples 四层分离。这解决了我们"品牌调性如何配置化"的问题，比笼统的"调性设置"清晰得多。其中 few-shot examples 被 README 明确标为"最重要的部分之一"。

**风险**

许可证需核实。只支持 Twitter 和 LinkedIn，平台层没有参考价值。

---

### 3.4 Spreado（122 stars，国内平台唯一的可用实现）

这是本次调研里**对国内产品最有直接价值的项目**，因为它是唯一一个 MIT 许可、且把抖音、小红书、快手、视频号四个国内平台发布跑通的开源实现。

**实现方式**

- Playwright 驱动真实浏览器（自动检测系统 Chrome / Edge，回退到内置 Chromium）
- 扫码登录，Cookie 保存到本地 `cookies/{platform}/{account}/account.json`
- 支持标题、描述、标签、封面、地理位置
- 支持定时发布与草稿
- **插件化架构**：新平台放进 `plugins/` 目录即自动发现
- CLI + Python API 双接口
- 自带 Agent Skill，给 Claude、Codex、Cursor、Windsurf 等使用

**关键结论**

它证实了我们在 PRD 里的判断：**抖音和小红书没有可用的官方内容发布接口，只能走浏览器自动化这条路。**

同时它也揭示了一个设计取舍。Spreado 是本地单机 CLI 工具，风险由用户自己承担；我们做多租户 SaaS，如果沿用 Cookie 方案，风险会被放大——同一个服务端 IP 批量操作大量账号，触发风控的概率远高于用户本机操作。

**建议**

- 可以作为 P1 阶段接入抖音与小红书的技术底座，直接复用其 Playwright 流程
- 但必须做改造：按客户隔离出口 IP、严格限速、Cookie 加密存储、异常熔断
- 或者更稳妥：提供"客户端发布代理"模式，发布动作下沉到客户本机执行，服务端只做编排与调度。这样既覆盖平台，又规避集中式风控风险

**风险**

Cookie 方案本质上是模拟用户操作，平台政策变化会直接导致失效，维护成本长期存在。

---

### 3.5 Beav（MIT-NC，架构可看代码不可用）

**功能矩阵（这是最完整的一份功能清单，值得逐条对标）**

| 采集与数据 | 洞察与选题 | 内容创作 | 视觉与媒体 | 排期与自动化 |
|---|---|---|---|---|
| 爆款视频采集 | 评论区洞察 | 结构化 Brief | AI 配图 | 内容日历 |
| 单条 / 主页采集 | 智能选题 | 图文稿 / 长文 | 商品图 / 套图 | 一次 / 每天 / 工作日 |
| 批量 / 关键词采集 | 选题中心 | 短视频脚本 | 社媒封面 | 每周 / 固定间隔 |
| 评论区采集 | 视频转录与摘要 | 口播稿 / 分镜 | 视频片段 | 定时自动创作 |
| 网页 / 公众号 / 摘录 | 知识库检索 | 标题 / 标签 / CTA | 数字人口播 / 音频 | 执行状态与产物 |
| 本地文件 / 文件夹 | 账号独立上下文 | 多平台发布文案 | 人物 / 商品主体复用 | 技能市场一键安装 |
| 图片 / 视频 / 素材包 | 真实来源引用 | 可编辑稿件项目 | 媒体库复用 | 外部 Agent 接入 |
| 自动社媒调研、博主订阅每日更新 | | | | |

**产品设计理念值得抄**

1. **"通用 AI 不懂内容资产"**这句定位判断很准。它把产品定义为"素材库 + 运营工作台"，而不是"生成器"。
2. **自动社媒调研**：围绕账号定位自主检索多平台公开内容，筛选后沉淀进知识库，成为后续选题依据。
3. **跨平台博主订阅**：订阅博主主页，每天自动抓取更新存进知识库，像追踪一个持续更新的素材源。
4. **技能市场**：按调研选题、文案风格、脚本优化、图片制作、视频制作分类，一键安装。这是把"能力"插件化、社区化的思路。
5. **主体复用**：人物或商品主体可在不同内容间复用，保持形象一致性。这是素材资产化的具体落地。
6. **MCP 接入宿主 Agent**：让 Codex 或 WorkBuddy 通过 MCP 连接本机 Beav，任务交给 Beav 内部 Agent，用户仍在 Beav UI 里查看审批。README 里明确一句"浏览器 UI 只供用户操作，不作为 Agent 控制通道"，这个边界划得很清楚。
7. **本地优先 + 自选模型（OpenAI-compatible）**。

**风险**

**MIT-NC，明确禁止商业使用，需作者书面许可。** 只能借鉴理念与功能清单，不能复用任何代码。

另外 README 声明：开源版本保留完整架构与核心实现用于学习研究，但生产安装包独立迭代、版本滞后，不作为生产版本的完整镜像。即便不考虑许可证，拿到的代码也不是最新的。

---

### 3.6 dsh-oil-creator（MIT，人机协同的边界划得好）

DeepSeek Harness 上的本地内容工作台插件，单人视频创作者导向。

**核心设计：一条片子就是一个文件夹**

```
~/Movies/视频项目/
└── 2026-08-19_DeepSeek Harness 上手/
    ├── topic.md
    ├── script.md
    ├── xxx.mp4
    ├── xxx.srt
    ├── xxx_subtitled.mp4
    ├── xxx_3x4.png / _4x3.png / _16x9.png
    ├── publish-package.json
    └── 公众号文章/
```

不建立封闭数据库，正文和产物就是普通文件，任何编辑器和 AI 文件工具都能读。插件只把工作台状态存进 `~/.dsh-oil-creator/overlay.json`。

**这张表是它最值得学的地方：**

| 阶段 | AI 与插件可以做什么 | 仍由人确认什么 |
|---|---|---|
| 选题与脚本 | 新建规范目录，读写 topic/script，遵守长期脚本规则 | 选题方向和最终表达 |
| 录制与剪辑 | 绑定并打开工程，等待导出文件稳定落盘 | 录制、时间线剪辑和导出 |
| 字幕与封面 | 启动字幕工作流，烧录字幕，生成三画幅封面 | 专有名词、标题和错别字 |
| 发布 | 把本地材料交给发布器准备多平台草稿 | 各平台最终"发表"按钮 |
| 数据回收 | 同步已发布作品的播放、赞、评和链接 | 登录状态和异常匹配结果 |

README 里一句话点透了态度：**"工作台不会假装替人完成录制、剪辑或最终发布。"**

**值得借鉴**

1. **不建立封闭内容数据库，用文件系统作为内容底座**。这个选择让 AI 文件工具、编辑器、脚本都能直接参与，是真正的"AI 原生"数据设计。
2. **人机职责表格化**。每一阶段明确"AI 做什么 / 人确认什么"，比笼统说"人机协同"可执行得多。我们的三档信任机制应该做成这种颗粒度。
3. **停在最关键的一步**：准备好多平台草稿，停在最终发表前，把最后一下留给人。
4. **先预览、再确认、后执行**：目录创建、配置保存、批量重命名都遵守这个原则，默认不执行、不删除文件。
5. **可选能力插件化**：字幕、封面、Screen Studio、发布、公众号各自独立，缺哪项只关掉那一项，不影响核心片库。
6. **长任务追踪**：启动后立即返回，由工作台继续观察文件产物和任务状态。

**局限**

单人视频创作者导向，没有多账号矩阵，不适合我们的 SaaS 场景。参考价值主要在理念层。

---

### 3.7 meiti-ai / ALQQ（专有软件，功能对标用）

仓库明确声明：**不含源代码，免费但专有，禁止反编译、二次分发、转售或克隆为同类产品。**

**但它的功能清单是国内市场最完整的对标物：**

- 20+ 平台分发，其中 17 个支持视频上传
- 三种内容形态：图文、动态/微头条、视频
- AI 写文、去 AI 味、热点选题
- 账号定位/人设：每个号设定人设、风格、平台调性
- 知识库：上传 PDF / Word / Excel / TXT，AI 整理为写作素材
- 产品库：带货与品牌内容
- 定时计划：自动「抓热点 → AI 成文 → 多账号发布」无人值守
- 桌面端用本机 IP 与 Cookie 发布，强调"全程肉眼可见、更安全、更像真人"
- 接入模型：DeepSeek、硅基流动、智谱 GLM、火山引擎（豆包）、Cloudflare AI、OpenAI 兼容接口
- 提供开放 REST API

**两个必须注意的竞争信号**

1. **它完全免费**，功能还覆盖 20+ 平台。这直接构成我们定价的压力，也说明国内"多平台分发"这项能力正在快速商品化，很难靠它单独收钱。
2. **它选择桌面端用本机 IP 发布**，而不是云端集中发布。这个选择本身就是对风控风险的回应，印证了我们对 Cookie 方案集中化风险的判断。

---

## 四、许可证红线

这一节建议在做任何技术选型前先过一遍。

| 许可证 | 约束 | 对我们的影响 |
|---|---|---|
| **MIT** | 可商用、可闭源、可修改，只需保留版权声明 | 安全。Spreado、dsh-oil-creator 属此类 |
| **AGPL-3.0** | 相比 GPL，明确**通过网络提供服务也算分发**。修改后提供网络服务，必须向用户公开完整源代码 | **Postiz、BrightBean Studio 属此类。基于它们做闭源商业 SaaS 会强制我们开源整个产品** |
| **MIT-NC** | 禁止商业使用，商用需书面许可 | **Beav 属此类。代码一行都不能用** |
| **专有** | 无授权 | meiti-ai 仓库无源码，只能功能对标 |

**可执行结论**

- 能直接复用代码的：Spreado（国内平台发布）、dsh-oil-creator（内容工程与人机协同）
- 只能借鉴架构与理念、必须重写实现的：Postiz、BrightBean Studio、Beav
- 需先确认许可证再动：mixpost、trypost、social-media-agent、Wanmeiyifa

需要说明的是，"参考架构"与"复用代码"的边界在法律上并不总是清晰，尤其 AGPL 的传染性认定存在解释空间。**如果后续真要深度参考 AGPL 项目的设计，建议先让法务过一遍。** 上面的分级是工程视角的初步判断，不构成法律意见。

---

## 五、推荐技术组合

采用分层拼装，每层选用许可证最安全、实现最成熟的参考。

| 层 | 参考来源 | 用法 |
|---|---|---|
| **平台适配层** | BrightBean Studio 的 `providers/` 范式 | 照搬目录结构与接口约定，自己实现。国内平台部分参考 Spreado 的 Playwright + Cookie 流程 |
| **编排引擎** | Postiz 用 Temporal；LangChain 用 LangGraph | 二选一。团队规模小、要快 → LangGraph；要求工业级可靠性、长时任务与人工挂起 → Temporal。考虑到 Evan 的 studylandsedu 项目已在用 Temporal，团队有基础，**倾向 Temporal** |
| **HITL 交互** | LangChain 的 interrupt + Agent Inbox | 直接借鉴范式：生成后在审核节点挂起，收件箱式 UI 批量处理，处理后工作流继续 |
| **审批分级** | BrightBean Studio 的 none / optional / internal / internal+client | 对齐我们 PRD 的三档信任机制，并补充 Client Portal（magic-link 免注册审批） |
| **内容底座** | dsh-oil-creator 的文件系统优先 | 内容以文件与目录组织，避免封闭数据库，便于 AI 工具直接操作 |
| **功能清单** | Beav 的功能矩阵 + meiti-ai 的平台清单 | 作为需求对照表逐条打勾，不复用代码 |
| **对外接口** | BrightBean Studio 的 REST + MCP 双协议 | MCP 接口让外部 Agent 能驱动产品，是 AI 原生的关键；同时配一个预置 agent skill |
| **运维诊断** | BrightBean Studio 的 `diagnose_facebook` 命令 | 每个平台配一个连通性与 scope 自检命令，这是自托管与多租户产品的刚需 |

---

## 六、对 PRD 的修订建议

基于本次调研，建议对 `AI社媒SaaS-PRD.md` 做以下调整：

**1. 平台适配策略可以放宽，但需要加一条约束**

原 PRD 建议 MVP 只做官方接口平台，抖音与小红书放 P1。调研后发现 Spreado（MIT）已经把抖音、小红书、快手、视频号的发布跑通，技术门槛比预期低。

建议改为：MVP 仍以官方接口平台（视频号、公众号、企业微信）为主，但把 Spreado 的接入作为**并行技术验证**，不阻塞 MVP。若验证通过，P1 即可扩展。

同时必须新增一条风险缓解设计：**发布动作下沉到客户端代理执行，服务端只做编排与调度**，避免服务端 IP 集中操作大量账号触发风控。

**2. 三档信任机制的技术实现要明确**

原 PRD 只写了产品层面的三档。建议补上技术实现范式：LangGraph interrupt 或 Temporal signal，配合 Agent Inbox 式审核队列。同时补 BrightBean 的 Client Portal 设计，因为代理商和 MCN 需要让客户看内容。

**3. 补一条竞争风险：国内多平台分发正在商品化**

meiti-ai / ALQQ 完全免费且支持 20+ 平台。这意味着"多平台一键分发"本身很难成为付费点。

这进一步强化了 PRD 里支柱一（Agent 化生产）和支柱二（可控自动化）的重要性：**卖点必须放在"内容怎么来"和"发了会不会出事"，而不是"能发多少个平台"。** 后者正在变成免费的基础能力。

**4. 定价需要重新审视**

面对免费竞品，PRD 里 1,980 的入门档可能没有竞争力。建议考虑：入门档降价或功能做足免费额度引流，把收入重心放在专业版与代理版上，靠 Agent 能力与合规能力收钱，而不是靠分发平台数量。

**5. 新增：对外接口与生态**

原 PRD 没有写 API 与 MCP。建议补上，理由有两条：Postiz 与 BrightBean 都把生态集成（N8N、Make、SDK、MCP）当作获客渠道；MCP 接口是"AI 原生"定位的实际落地，也是让产品能被其他 Agent 调用的关键。

---

## 七、待核实事项

| 事项 | 为什么重要 |
|---|---|
| mixpost、trypost、social-media-agent、Wanmeiyifa 的许可证 | 若为 MIT，可作为额外参考；若为 AGPL 则受限 |
| 微信视频号、公众号当前官方接口的内容发布权限 | 直接决定 MVP 平台可行性，需查最新开放平台文档 |
| 企业微信的分发能力边界 | 原 PRD 将其列为 MVP 平台之一，需确认能做什么 |
| TikTok 国内版（抖音）开放平台是否对个人开发者开放发布权限 | 决定抖音是走 API 还是只能走 Spreado 方案 |
| 各视频生成模型（即梦、可灵、海螺）的实时单价与批量折扣 | PRD 成本模型全部基于此，必须实测校准 |

---

## 八、参考链接

- Postiz：https://github.com/gitroomhq/postiz-app
- BrightBean Studio：https://github.com/brightbeanxyz/brightbean-studio
- social-media-agent：https://github.com/langchain-ai/social-media-agent
- Spreado：https://github.com/BadKid90s/Spreado
- Beav：https://github.com/Jamailar/Beav
- dsh-oil-creator：https://github.com/oil-oil/dsh-oil-creator
- meiti-ai / ALQQ：https://github.com/zhuixin8/meiti-ai
- mixpost：https://github.com/inovector/mixpost
- trypost：https://github.com/trypostit/trypost
- Wanmeiyifa：https://github.com/cml227/Wanmeiyifa
