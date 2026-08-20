---
title: "BootX 品牌体系与资产归档"
layer: facts
source: "00_inbox/20260817-evan-bootx品牌命名与官网工作记录.md"
date: 2026-08-17
tags: [BootX, 品牌, 命名, 资产归档, facts]
confidence: high
---

# BootX 品牌体系与资产归档

## 一句话
旧名 FDE 已统一更名为 **BootX**（X 大写），对外品牌名 / 知识库 / 官网仓库命名须一致；品牌资产集中在 `materials/bootx-品牌/` 且保持扁平结构。

## 详情
- **更名决策**：2026-08-16 由 Evan 拍板，FDE → BootX（X 大写），对外统一使用，所有文档/代码仓库命名以此为准，避免再次出现 FDE/BootX 混用。
- **品牌全案产出**（已归档至 `materials/bootx-品牌/`）：品牌全案/设计/介绍 HTML、FDE 命名方案、字标 SVG（`bootx-staged-launch.svg` / `bootx-staged-launch-lockup.svg`）、`bootx-logo.png`（1024×1024）、`bootx-logo-full.png`（1000×300，已作为本仓库 `README.md` 头图）。
- **资产归档规则**：HTML 演示稿 + woff2 字体 + SVG 素材放进 `materials/bootx-品牌/` 并保持扁平结构，使 `url('archivo-black.woff2')` 等相对引用在仓库内可直接打开。
- **关联仓库**：BootX-ANC（本知识库）、TISNN/BootX（官方网站独立代码仓库，2026-08-17 由 Evan 构建并 push）。

## 怎么用
新建任何对外文档/页面时，品牌名写 **BootX**（X 大写）；引用品牌字体/素材时连同 woff2 一起复制并保持扁平目录，否则单文件打开会缺字体、乱码。

## 关联
- 同主题其他条目：（暂无）
- 原始产出物：`archive/2026-W34-20260817-evan-bootx品牌命名与官网工作记录.md`

## 状态
- [ ] 候选固化（被 ≥3 次验证后迁入 `skills/`）
