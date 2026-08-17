---
title: "BootX 品牌命名与官网工作记录"
layer: inbox
author: evan
date: 2026-08-17
tags: [bootx, 品牌, 官网, 命名]
---

# BootX 品牌命名与官网（2026-08-16 ~ 08-17）

## 背景
FDE 社群/团队需要一个统一的对外品牌。2026-08-16 由 Evan 拍板：将旧名 FDE 统一更名为 **BootX**（X 大写），并完成品牌设计与品牌全案。2026-08-17 基于该品牌上线了官方网站，并推送到 GitHub 独立仓库。

## 产出
- 品牌命名决策：FDE → **BootX**（X 大写），对外统一使用，所有文档/代码仓库命名以此为准。
- 品牌设计 + 品牌全案（已归档至 `materials/bootx-品牌/`）：
  - `bootX品牌全案.html` —— 品牌全案主文档
  - `bootX品牌设计.html` —— 品牌设计
  - `bootX品牌介绍.html` —— 品牌介绍
  - `bootX英文字标参考.html` —— 英文名标参考
  - `bootX-01切线字标精调.html` —— 切线字标精调
  - `FDE命名方案.html` —— FDE → BootX 命名方案
  - `assets/` —— 字标 SVG（bootx-staged-launch.svg / bootx-staged-launch-lockup.svg），实际 SVG 品牌资产用于 Staged Launch 图标与 Micro Cut 字标
  - `bootx-logo.png`（1024×1024）—— 主 logo 位图文件
  - `bootx-logo-full.png`（1000×300）—— 完整字标组合，已放在 `README.md` 开头作为仓库头图
- 官方网站仓库：`https://github.com/TISNN/BootX`（2026-08-17 由 Evan 构建并 push，独立仓库，与本知识库 BootX-ANC 分离）

## 可复用点
1. 品牌资产集中归档：HTML 演示稿 + 字体（woff2）+ SVG 素材放进 `materials/bootx-品牌/`，保持扁平结构使 `url('archivo-black.woff2')` 等相对引用在仓库内可直接打开。
2. 对外品牌名统一为 BootX（X 大写），与 BootX-ANC 知识库、BootX 官网仓库命名保持一致，避免再次出现 FDE/BootX 混用。

## 踩过的坑
1. 品牌 HTML 依赖根目录 woff2 字体，单文件复制会缺字体、打开乱码 → 需连同 3 个 woff2 一起复制并保持扁平结构（已处理）。

## 涉及的内部实体
- BootX：FDE 社群/团队统一对外品牌名（旧名 FDE）。
- BootX-ANC：内部 ANC 知识库仓库（本仓库）。
- TISNN/BootX：官方网站代码仓库。
