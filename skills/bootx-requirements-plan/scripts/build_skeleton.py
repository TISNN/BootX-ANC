# -*- coding: utf-8 -*-
"""最小示例：用 docx_blocks 生成一个「需求确认与方案规划书」骨架。
直接运行会产出 /tmp/bootx_skeleton.docx，可作为新客户文档的起点。

用法：
    python build_skeleton.py            # 默认输出 /tmp/bootx_skeleton.docx
    python build_skeleton.py 输出路径.docx
"""
import sys
import docx_blocks as B

OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/bootx_skeleton.docx'

doc = B.new_doc()

# ---------- 封面（含客户 Logo，可选） ----------
for _ in range(2):
    doc.add_paragraph()
logo_path = '/path/to/client_logo.png'   # 换成真实路径；缺失则跳过
try:
    lp = doc.add_paragraph(); lp.alignment = B.WD_ALIGN_PARAGRAPH.CENTER; lp.paragraph_format.space_after = B.Pt(8)
    lr = lp.add_run(''); lr.add_picture(logo_path, width=B.Cm(3.5))
except Exception:
    pass
p = doc.add_paragraph(); p.alignment = B.WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = B.Pt(8)
r = p.add_run('客户名 · 业务 AI 转型'); B.set_font(r, size=26, bold=True, color=B.ACCENT)
p = doc.add_paragraph(); p.alignment = B.WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('需求确认与方案规划书'); B.set_font(r, size=22, bold=True, color=B.ACCENT)
p = doc.add_paragraph(); p.alignment = B.WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_before = B.Pt(10)
r = p.add_run('根据双方前期沟通整理，明确贵司现状、核心需求与 AI 转型路径，并给出参考报价与商务模式。')
B.set_font(r, size=11, color=B.MUTED)
B.spacer(doc, 8)
meta = [['致 · 客户公司全称', '文档性质 · 需求确认 / 前期沟通版'],
        ['阶段 · 意向确认（未签约）', '日期 · 2026-xx-xx']]
t = doc.add_table(rows=2, cols=2); t.alignment = B.WD_TABLE_ALIGNMENT.CENTER
B.set_table_borders(t, color=B.ACCENT, sz=6)
for i, row in enumerate(meta):
    for j, val in enumerate(row):
        c = t.cell(i, j); B.set_cell_shading(c, B.ACCENT_SOFT)
        p = c.paragraphs[0]; p.alignment = B.WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(val); B.set_font(r, size=10.5, bold=True, color=B.ACCENT)
B.set_col_widths(t, [8.4, 8.4])
for _ in range(3):
    doc.add_paragraph()

# ---------- 00 一页纸结论 ----------
B.section_head(doc, '00', '一页纸结论')
B.lead(doc, '一句话概括本方案的核心目标、最高优先级与启动方式。')
B.card_grid(doc, [
    ('核心目标', '先减工作量，再谈增长；把"一人服务 100 家"向 500–1000 家推进。'),
    ('最高优先级', 'AI 客服 + 客户管理：解放微信沟通与跟进，建立客户分层与知识基础。'),
    ('启动方式', '建议"基础客服验证"先跑通价值；个人微信自动化先做技术验证再试点。'),
], cols=3, widths_cm=[5.6, 5.6, 5.6])
B.callout(doc, [
    [('首期投入参考：', True, B.INK)],
    [('首期（预算内）以企业微信官方接口落地"基础客服提效验证"，约 ', False, B.INK),
     ('2.48–2.98 万元', True, B.ACCENT),
     ('。', False, B.INK)],
    [('个人微信自动化单列，须先做技术验证，不与首期捆绑。', False, B.MUTED)],
], style='gold')

# ---------- 01 客户背景（示例一节） ----------
B.section_head(doc, '01', '关于客户（背景整理）')
B.lead(doc, '基于官网、公开工商信息与前期沟通整理，如有偏差以贵司确认为准。')
B.h3(doc, '1.1 公司概况')
B.data_table(doc, ['项目', '内容'], [
    ['公司全称', '客户公司全称'],
    ['成立时间', '20xx 年 x 月'],
    ['运营总部', '城市 / 园区'],
    ['核心团队', [('创始人/总经理 ', False, B.INK), ('姓名', True, B.ACCENT),
                 ('（对外品牌名"', False, B.INK), ('品牌', True, B.ACCENT),
                  ('"），税务专家，具多年税务机关经验', False, B.INK)]],
    ['企业规模', '小微企业（团队约 30 余人）；A 级纳税人；多商标；对外投资多家企业'],
], widths_cm=[4, 12.8])

B.save_doc(doc, OUT)
print('SAVED', OUT)
