# 构建流水线（HTML → DOCX → PDF）

## 总体策略
1. 先在 HTML 里完成丰富视觉（封面、表头配色、卡片网格、callout、架构图）。
2. 用 `scripts/docx_blocks.py`（python-docx）生成可编辑 Word，架构图转 PNG 内嵌。
3. 用 Chrome 无头打印生成高保真 PDF（保留配色与图）。

## 环境
- python-docx：在隔离 venv 中 `pip install python-docx`（脚本用 `/Users/evanxu/.venv-html-to-docx`）。
- Chrome：macOS 用 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`（无头打印）。

## SVG 架构图 → PNG
Word 转换引擎不认 SVG，需先转 PNG：
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --default-background-color=FFFFFFFF --window-size=1360,940 \
  --screenshot=/tmp/diagram.png "file:///path/to/diagram.svg"
```
再把 HTML 里的 `<svg>…</svg>` 替换为
`<img src="data:image/png;base64,…" style="width:100%;max-width:16cm;">` 再转 DOCX。

## HTML → DOCX（python-docx）
直接调用 `scripts/docx_blocks.py` 里的积木函数（不要用线性化转换器，会丢失卡片/表头配色）：
```python
import docx_blocks as B
doc = B.new_doc()          # 已设页边距/正文中文字体/行距
B.section_head(doc, '01', '关于客户（背景整理）')
B.data_table(doc, ['项目','内容'], rows, widths_cm=[4,12.8])
B.card_grid(doc, [('标题','正文'), …], cols=3, widths_cm=[5.6,5.6,5.6])
B.callout(doc, [[('首期投入参考：',True,B.P['INK']),('…',False,B.P['ACCENT'])]], style='gold')
B.pain(doc, '痛点 1', '标题', '描述', '影响度：高（9/10）')
B.mod(doc, 'M1', 'AI 客服机器人', '最高', [('p','…'),('sub','(1) …'),('li','…')])
B.phase(doc, 'P1', '一期 · …', '…')
B.save_doc(doc, '/path/out.docx')
```
主题色在 `docx_blocks.PALETTE` 中，改完调 `docx_blocks.apply_palette()` 生效。

## HTML → PDF（Chrome 无头）
先给 HTML 加打印背景色规则（否则表头蓝/黑底打印成空白）：
```css
@media print { * { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
```
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer \
  --print-to-pdf="/path/out.pdf" "file:///path/in.html"
```

## 校验清单
- `*` 字面数量 = 0；`——` 破折号数量 = 0；英文章节副标题 = 无。
- 嵌入图片含架构图 PNG 与客户 Logo；关键内容（客户名 / 罗祖威 / 横琴 / 方案A / 2.48 / 5.98 / 知识飞轮）齐全。
- 对外文档无版本号。
