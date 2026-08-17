# -*- coding: utf-8 -*-
"""bootx 可复用 Word 排版积木。

用于生成「客户需求确认与方案规划书」等精排文档。依赖 python-docx。
主题色集中在 PALETTE 中，修改后调用 apply_palette() 生效。

用法见 scripts/build_skeleton.py。
"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------- 主题色（黑金，可覆盖） ----------
PALETTE = dict(
    ACCENT='1C1C1E', ACCENT2='C98A2D',
    ACCENT_SOFT='EFEFEF', ACCENT2_SOFT='F8F0E1',
    BG2='F7F7F7', RULE='E0E0E0',
    TOP='B02323', ORANGE='C0392B', GOLD='C98A2D', MUTED='6B6B6B',
    WARN_BG='FBEDE6', INK='1C1C1E', WHITE='FFFFFF',
    FONT='Microsoft YaHei',
)

# 由 PALETTE 解析为模块级常量
ACCENT=ACCENT2=ACCENT_SOFT=ACCENT2_SOFT=BG2=RULE=None
TOP=ORANGE=GOLD=MUTED=WARN_BG=INK=WHITE=FONT=None

def apply_palette():
    """把 PALETTE 的值同步到模块级常量，供各函数读取。"""
    g = globals()
    for k, v in PALETTE.items():
        g[k] = v

apply_palette()

# ---------- 底层工具 ----------
def set_cell_shading(cell, color_hex):
    tcPr=cell._tc.get_or_add_tcPr()
    shd=OxmlElement('w:shd')
    shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),color_hex)
    tcPr.append(shd)

def set_cell_borders(cell, color=RULE, sz=4, sides=('top','left','bottom','right')):
    tcPr=cell._tc.get_or_add_tcPr()
    borders=OxmlElement('w:tcBorders')
    for s in ['top','left','bottom','right']:
        e=OxmlElement(f'w:{s}')
        if s in sides:
            e.set(qn('w:val'),'single'); e.set(qn('w:sz'),str(sz)); e.set(qn('w:space'),'0'); e.set(qn('w:color'),color)
        else:
            e.set(qn('w:val'),'nil')
        borders.append(e)
    tcPr.append(borders)

def set_table_borders(t, color=RULE, sz=4):
    tblPr=t._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for s in ['top','left','bottom','right','insideH','insideV']:
        e=OxmlElement(f'w:{s}')
        e.set(qn('w:val'),'single'); e.set(qn('w:sz'),str(sz)); e.set(qn('w:space'),'0'); e.set(qn('w:color'),color)
        borders.append(e)
    tblPr.append(borders)

def clear_table_borders(t):
    tblPr=t._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for s in ['top','left','bottom','right','insideH','insideV']:
        e=OxmlElement(f'w:{s}'); e.set(qn('w:val'),'nil'); borders.append(e)
    tblPr.append(borders)

def set_font(run, size=10.5, bold=None, color=None, italic=None, name=FONT):
    run.font.name=name
    rPr=run._element.get_or_add_rPr(); rFonts=rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts=OxmlElement('w:rFonts'); rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'),name); rFonts.set(qn('w:ascii'),name); rFonts.set(qn('w:hAnsi'),name)
    if size is not None: run.font.size=Pt(size)
    if bold is not None: run.font.bold=bold
    if italic is not None: run.font.italic=italic
    if color is not None: run.font.color.rgb=RGBColor.from_string(color)

def set_col_widths(t, widths_cm):
    for j,w in enumerate(widths_cm):
        for row in t.rows:
            row.cells[j].width=Cm(w)

# ---------- 段落 ----------
def para(doc, text='', size=10.5, bold=False, color=None, align=None, after=6, before=0, italic=False, line=1.5):
    p=doc.add_paragraph()
    if align is not None: p.alignment=align
    pf=p.paragraph_format; pf.space_after=Pt(after); pf.space_before=Pt(before); pf.line_spacing=line
    if text=='':
        return p
    r=p.add_run(text); set_font(r,size=size,bold=bold,color=color,italic=italic)
    return p

def rich(doc, parts, size=10.5, after=6, before=0, align=None, line=1.5):
    p=doc.add_paragraph()
    if align is not None: p.alignment=align
    pf=p.paragraph_format; pf.space_after=Pt(after); pf.space_before=Pt(before); pf.line_spacing=line
    for (txt,b,col) in parts:
        r=p.add_run(txt); set_font(r,size=size,bold=b,color=col or INK)
    return p

# ---------- 结构块 ----------
def section_head(doc, no, title, en=None):
    """章节号块 + 中文标题（不渲染英文副标题）。"""
    doc.add_paragraph().paragraph_format.space_after=Pt(2)
    t=doc.add_table(rows=1, cols=2); t.alignment=WD_TABLE_ALIGNMENT.LEFT
    clear_table_borders(t)
    c0=t.cell(0,0); set_cell_shading(c0,ACCENT); c0.width=Cm(1.2)
    p=c0.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.vertical_alignment=WD_ALIGN_VERTICAL.CENTER
    p.paragraph_format.space_after=Pt(0); p.paragraph_format.space_before=Pt(0)
    r=p.add_run(no); set_font(r,size=13,bold=True,color=WHITE)
    c1=t.cell(0,1)
    p=c1.paragraphs[0]; p.paragraph_format.space_after=Pt(0)
    r=p.add_run(title); set_font(r,size=16,bold=True,color=INK)
    set_col_widths(t,[1.2,16.6])
    doc.add_paragraph().paragraph_format.space_after=Pt(3)

def h3(doc, text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(12); p.paragraph_format.space_after=Pt(4)
    r=p.add_run(text); set_font(r,size=13,bold=True,color=ACCENT)

def h4(doc, text):
    p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(6); p.paragraph_format.space_after=Pt(3)
    r=p.add_run(text); set_font(r,size=11,bold=True,color=INK)

def lead(doc, text):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(6)
    r=p.add_run(text); set_font(r,size=10.5,color=MUTED)

def spacer(doc, after=6):
    doc.add_paragraph().paragraph_format.space_after=Pt(after)

def card_grid(doc, items, cols=3, widths_cm=None):
    """items: [(标题, 正文), …]；等高卡片网格。"""
    n=len(items); rows=(n+cols-1)//cols
    t=doc.add_table(rows=rows, cols=cols); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t,color=RULE,sz=4)
    idx=0
    for ri in range(rows):
        for ci in range(cols):
            cell=t.cell(ri,ci); set_cell_shading(cell,'FFFFFF'); set_cell_borders(cell,color=RULE,sz=4)
            cell.vertical_alignment=WD_ALIGN_VERTICAL.CENTER
            if idx<n:
                title,body=items[idx]
                p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(1); p.paragraph_format.line_spacing=1.15
                r=p.add_run(title); set_font(r,size=11,bold=True,color=ACCENT)
                p2=cell.add_paragraph(); p2.paragraph_format.space_before=Pt(2); p2.paragraph_format.space_after=Pt(0); p2.paragraph_format.line_spacing=1.15
                r2=p2.add_run(body); set_font(r2,size=9.5,color=MUTED)
            idx+=1
    if widths_cm: set_col_widths(t,widths_cm)
    spacer(doc,2)

def render_cell(cell, val):
    """单元格内容：str / (txt,b,col) 列表 / 多层列表。"""
    if val is None: return
    is_multi = isinstance(val,list) and len(val)>0 and isinstance(val[0],list)
    is_single = isinstance(val,list) and len(val)>0 and isinstance(val[0],tuple)
    if is_multi:
        paras=val
    elif is_single:
        paras=[val]
    else:
        paras=[val]
    for pi,para in enumerate(paras):
        p=cell.paragraphs[0] if pi==0 else cell.add_paragraph()
        p.paragraph_format.space_after=Pt(3)
        if isinstance(para,str):
            r=p.add_run(para); set_font(r,size=10,color=INK)
        elif isinstance(para,list):
            for (txt,b,col) in para:
                r=p.add_run(txt); set_font(r,size=10,bold=b,color=col or INK)

def data_table(doc, headers, rows, widths_cm=None, header_fill=None, zebra=True, total_text=None, total_val=None, merge_total=1):
    """标准数据表：表头主色底白字，偶数行浅灰斑马纹。"""
    if header_fill is None: header_fill=ACCENT
    cols=len(headers)
    t=doc.add_table(rows=1, cols=cols); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t,color=RULE,sz=4)
    hdr=t.rows[0].cells
    for j,h in enumerate(headers):
        set_cell_shading(hdr[j],header_fill); hdr[j].vertical_alignment=WD_ALIGN_VERTICAL.CENTER
        p=hdr[j].paragraphs[0]; r=p.add_run(h); set_font(r,size=10.5,bold=True,color=WHITE)
    for ri,row in enumerate(rows):
        cells=t.add_row().cells
        for j,val in enumerate(row):
            set_cell_shading(cells[j], BG2 if (zebra and ri%2==1) else 'FFFFFF')
            cells[j].vertical_alignment=WD_ALIGN_VERTICAL.CENTER
            render_cell(cells[j], val)
    if total_text is not None:
        cells=t.add_row().cells
        if merge_total and merge_total>1:
            merged=cells[0]
            for k in range(1,merge_total): merged=merged.merge(cells[k])
            set_cell_shading(merged,header_fill); merged.vertical_alignment=WD_ALIGN_VERTICAL.CENTER
            p=merged.paragraphs[0]; r=p.add_run(total_text); set_font(r,size=10,bold=True,color=WHITE)
        else:
            set_cell_shading(cells[0],header_fill); p=cells[0].paragraphs[0]; r=p.add_run(total_text); set_font(r,size=10,bold=True,color=WHITE)
        for j in range(merge_total,cols):
            set_cell_shading(cells[j],header_fill); p=cells[j].paragraphs[0]
            r=p.add_run(str(total_val) if j==cols-1 else ''); set_font(r,size=10,bold=True,color=WHITE)
    if widths_cm: set_col_widths(t,widths_cm)
    spacer(doc,4)
    return t

def callout(doc, lines, style='accent'):
    """底色块提示框。style: accent / gold / warn。"""
    bg={'accent':ACCENT_SOFT,'gold':ACCENT2_SOFT,'warn':WARN_BG}[style]
    t=doc.add_table(rows=1, cols=1); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t,color=bg,sz=4)
    c=t.cell(0,0); set_cell_shading(c,bg)
    for i,line in enumerate(lines):
        p=c.paragraphs[0] if i==0 else c.add_paragraph()
        p.paragraph_format.space_after=Pt(2)
        if isinstance(line,list):
            for (txt,b,col) in line:
                r=p.add_run(txt); set_font(r,size=10.5,bold=b,color=col or INK)
        else:
            r=p.add_run(line); set_font(r,size=10.5,color=INK)
    spacer(doc,3)

def pain(doc, tag, title, body, impact):
    """痛点卡：金边 + 浅金底，标签/标题/描述/影响度。"""
    t=doc.add_table(rows=1, cols=1); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t,color=ACCENT2,sz=6)
    c=t.cell(0,0); set_cell_shading(c,ACCENT2_SOFT); c.vertical_alignment=WD_ALIGN_VERTICAL.CENTER
    p=c.paragraphs[0]; p.paragraph_format.space_after=Pt(1); r=p.add_run(tag); set_font(r,size=10,bold=True,color=ACCENT2)
    p2=c.add_paragraph(); p2.paragraph_format.space_before=Pt(2); p2.paragraph_format.space_after=Pt(1); p2.paragraph_format.line_spacing=1.2; r2=p2.add_run(title); set_font(r2,size=12,bold=True,color=INK)
    p3=c.add_paragraph(); p3.paragraph_format.space_before=Pt(1.5); p3.paragraph_format.space_after=Pt(1); p3.paragraph_format.line_spacing=1.2; r3=p3.add_run(body); set_font(r3,size=10,color=INK)
    p4=c.add_paragraph(); p4.paragraph_format.space_before=Pt(1.5); p4.paragraph_format.space_after=Pt(0); r4=p4.add_run(impact); set_font(r4,size=9.5,color=MUTED)
    spacer(doc,3)

def mod(doc, idx, title, priority, blocks):
    """需求模块块：标题 + 优先级标签 + 子项（sub/p/li/rich）。"""
    t=doc.add_table(rows=1, cols=1); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t,color=RULE,sz=4)
    c=t.cell(0,0); set_cell_shading(c,'FFFFFF')
    p=c.paragraphs[0]
    r=p.add_run(f'{idx}  '); set_font(r,size=12,bold=True,color=ACCENT)
    r=p.add_run(title+'  '); set_font(r,size=12,bold=True,color=INK)
    r=p.add_run(f'[{priority}]'); set_font(r,size=10,bold=True,color=ACCENT2)
    for kind,text in blocks:
        if kind=='sub':
            pp=c.add_paragraph(); pp.paragraph_format.space_before=Pt(8); pp.paragraph_format.space_after=Pt(2)
            r=pp.add_run(text); set_font(r,size=10.5,bold=True,color=ACCENT)
        elif kind=='p':
            pp=c.add_paragraph(); pp.paragraph_format.space_after=Pt(3)
            r=pp.add_run(text); set_font(r,size=10,color=INK)
        elif kind=='li':
            pp=c.add_paragraph(); pp.paragraph_format.left_indent=Cm(0.6); pp.paragraph_format.space_after=Pt(2)
            r=pp.add_run('• '+text); set_font(r,size=10,color=INK)
        elif kind=='rich':
            pp=c.add_paragraph(); pp.paragraph_format.space_after=Pt(3)
            for (txt,b,col) in text:
                r=pp.add_run(txt); set_font(r,size=10,bold=b,color=col or INK)
    spacer(doc,4)

def phase(doc, pno, title, body):
    """分期块：左侧编号块 + 右侧标题/描述。"""
    t=doc.add_table(rows=1, cols=2); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t,color=RULE,sz=4)
    c0=t.cell(0,0); set_cell_shading(c0,ACCENT); c0.width=Cm(1.8)
    p=c0.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.vertical_alignment=WD_ALIGN_VERTICAL.CENTER
    r=p.add_run(pno); set_font(r,size=14,bold=True,color=WHITE)
    c1=t.cell(0,1); set_cell_shading(c1,BG2)
    p=c1.paragraphs[0]; r=p.add_run(title); set_font(r,size=11.5,bold=True,color=ACCENT)
    p2=c1.add_paragraph(); p2.paragraph_format.space_before=Pt(3); r2=p2.add_run(body); set_font(r2,size=10,color=INK)
    spacer(doc,4)

# ---------- 文档初始化与保存 ----------
def new_doc():
    doc=Document()
    sec=doc.sections[0]
    sec.page_height=Cm(29.7); sec.page_width=Cm(21)
    sec.top_margin=Cm(2); sec.bottom_margin=Cm(2); sec.left_margin=Cm(2.2); sec.right_margin=Cm(2.2)
    st=doc.styles['Normal']; st.font.name=FONT; st.font.size=Pt(10.5)
    st.element.rPr.rFonts.set(qn('w:eastAsia'),FONT)
    pf=st.paragraph_format; pf.line_spacing=1.5; pf.space_after=Pt(6)
    return doc

def save_doc(doc, path):
    doc.save(path)
    return path
