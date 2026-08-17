---
name: bootx-requirements-plan
description: "This skill should be used when bootx needs to produce a client-facing
  requirements-confirmation and solution-planning document for a service
  enterprise, especially in pre-sales or pre-payment stages where requirements
  must be locked before quoting. It encodes the end-to-end workflow: fact-gathering
  and cross-verification, the canonical 8-section outline, the ANC knowledge-flywheel
  architecture narrative, validation-first modular quotation logic with risky
  platform-automation items quoted separately, client-facing tone and style rules,
  and the HTML to DOCX to PDF build pipeline."
---

# bootx 客户需求确认与方案规划书

## Purpose
Produce a client-facing 需求确认与方案规划书 for bootx's service-enterprise prospects
(财税 / 企业服务 / AI 转型 等), used in the pre-payment / 意向阶段. The document
locks requirements, presents an AI transformation plan, and gives a validation-first
quotation so bootx quotes *after* alignment, not before.

## When to use
- A user asks to "给客户出需求文档 / 方案规划书 / 需求确认书", or to "整理客户背景" before quoting.
- The engagement is not yet paid (未签约 / 意向): the rule is 先定需求，再报价.
- The prospect is a service enterprise with pain points in 客户沟通/跟进、客户分层、
  咨询承载、流程标准化、新媒体获客.
- Trigger phrases: 财税 AI 转型、ANC 知识飞轮、FDE 陪跑、个人微信自动化、企业知识库、
  语气蒸馏、数字员工、需求确认与方案规划.

## Workflow

### 1. Gather materials
Collect and read before writing: prior internal drafts (md / html / docx),
the client's official website (WebFetch), the internal knowledge base in the FDE
folder (e.g. `ANC知识飞轮机制与落地实践.md`, `AI如何助力企业转型-分享稿`), and any
meeting transcript. Do not invent business data the user has not supplied.

### 2. Cross-verify facts (critical)
WebSearch the client's legal entity, founder / 法定代表人, 注册资本 / 股东,
参保人数, 注册 / 运营地址, 经营范围, 资质荣誉. Sources conflict constantly
(QCC vs 启信宝 vs 官网). Resolve and record the verified set. In the
client-facing doc, AVOID printing numbers that conflict across sources
(use "约 / 多家 / 团队约 30 余人"); keep precise-but-unverified figures out of
the external version. Fix obvious internal typos (e.g. 横景 → 横琴).

### 3. Build the document (see references/structure.md)
Follow the canonical 8-section outline:
封面 → 00 一页纸结论 → 01 客户背景 → 02 诊断痛点 → 03 目标与思路
→ 04 需求模块总览 → 05 ANC 架构与知识飞轮 → 06 分期实施规划
→ 07 报价与商务模式 → 08 下一步与待确认.
Embed the methodology pillars: workflow-first, human-in-the-loop, 知识飞轮 / ANC,
and bootx's FDE 陪跑 role (position bootx as a 陪跑方, not a tool vendor).

### 4. Quotation logic (see references/quotation_logic.md)
Use validation-first, modular pricing. CRITICAL: items depending on
platform-constrained channels (e.g. 个人微信自动读取/发送) must be a STANDALONE
technical-verification + quote line, never bundled free into a fixed first-phase
price. Define the recommended first phase from the confirmed budget / entry path.

### 5. Apply style rules (see references/style_rules.md)
Client-facing tone (贵司 / 您), NO version number on the external doc,
NO em-dash (——), NO literal `**`, apply humanizer-zh to cut AI-phrasing,
neutral / black-gold theme, insert the client's logo on the cover.

### 6. Build outputs (see references/build_pipeline.md, scripts/docx_blocks.py)
1. Author in HTML for rich visuals (cover, colored table headers, card grids,
   callouts, architecture diagram).
2. Convert to editable Word via python-docx using `scripts/docx_blocks.py`
   (reusable shading / border / table / card / callout helpers + themed palette).
3. Export PDF via Chrome headless print (preserves diagram + colors).
Embed the ANC architecture diagram as a PNG (a generic template lives in
`assets/anc_diagram.svg`).

### 7. Review before sending
Cross-verify facts again, list open items for the client to confirm
(entry path, budget, data deployment, policy source), then present
HTML / PDF / DOCX.

## Bundled resources
- `references/structure.md` — the 8-section outline, what each section contains, and the ANC diagram description.
- `references/style_rules.md` — tone, formatting, theme, and logo rules.
- `references/quotation_logic.md` — validation-first modular quotation and the risky-item separation rule.
- `references/build_pipeline.md` — HTML → DOCX → PDF commands and caveats (SVG→PNG, print-background).
- `scripts/docx_blocks.py` — reusable python-docx helpers (palette, shading, borders, data_table, card_grid, callout, pain, mod, phase, section_head).
- `scripts/build_skeleton.py` — minimal example calling docx_blocks to produce a skeleton doc.
- `assets/anc_diagram.svg` — generic ANC knowledge-flywheel architecture diagram template (edit labels per client).
