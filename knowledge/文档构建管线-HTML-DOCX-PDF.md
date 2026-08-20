---
title: "文档构建管线 HTML → DOCX → PDF"
layer: actions
source: "00_inbox/20260817-evan-威吉瑞需求确认方案规划书交付.md"
date: 2026-08-17
tags: [文档管线, 工作流, SOP, actions]
confidence: high
---

# 文档构建管线 HTML → DOCX → PDF

## 一句话
对客文档先用 HTML 做富视觉，再用 `scripts/docx_blocks.py` 转可编辑 Word，最后 Chrome headless 打印 PDF（保留图与配色）。

## 详情
- **HTML 富视觉**：封面 / 彩色表头 / 卡片 / callout / 架构图，先在这一层把版式做漂亮。
- **DOCX 转换**：`scripts/docx_blocks.py` 把 HTML 转为可编辑 Word，方便客户二次编辑。
- **PDF 导出**：Chrome headless 打印 PDF，保留图与配色，作为正式发送版。
- **架构图复用**：`assets/anc_diagram.svg` 改标签即可复用，不必每次重画。
- 威吉瑞《需求确认与方案规划书》即三态（HTML + DOCX + PDF）产出。

## 怎么用
需要做「好看 + 可编辑 + 可打印」三态对客文档时，直接套这条管线；架构图优先改 `anc_diagram.svg` 标签而非重画。

## 关联
- 同主题其他条目：`knowledge/对外文档硬规则.md`
- 原始产出物：`archive/2026-W34-20260817-evan-威吉瑞需求确认方案规划书交付.md`

## 状态
- [x] 候选固化（成熟工作流，建议固化进 `skills/` 或 `skills/bootx-requirements-plan` 的构建环节）
