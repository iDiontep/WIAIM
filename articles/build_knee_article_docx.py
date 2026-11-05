# -*- coding: utf-8 -*-
"""Build a Word manuscript from articles/knee_emg_patent_review.md."""
import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent
MD = ROOT / "knee_emg_patent_review.md"
DOCX = ROOT / "knee_emg_patent_review.docx"
FONT = "Times New Roman"


def _font(run, size=14, bold=False, italic=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), FONT)


def _fmt(p, *, first=True, align="justify", before=0, after=0):
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.first_line_indent = Cm(1.0) if first else Cm(0)
    pf.alignment = {
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "left": WD_ALIGN_PARAGRAPH.LEFT,
    }[align]


def add_rich(p, text, size=14, bold=False, italic=False):
    """Render **bold**, *italic* markers and \\( ... \\) as italic."""
    pattern = re.compile(r"(\*\*[^*]+\*\*|\\\(.+?\\\)|\*[^*]+\*)")
    pos = 0
    for match in pattern.finditer(text):
        if match.start() > pos:
            run = p.add_run(text[pos:match.start()])
            _font(run, size=size, bold=bold, italic=italic)
        token = match.group(0)
        if token.startswith("**"):
            run = p.add_run(token[2:-2])
            _font(run, size=size, bold=True, italic=italic)
        elif token.startswith("\\("):
            run = p.add_run(token[2:-2].replace("\\", ""))
            _font(run, size=size, bold=bold, italic=True)
        else:
            run = p.add_run(token[1:-1])
            _font(run, size=size, bold=bold, italic=True)
        pos = match.end()
    if pos < len(text):
        run = p.add_run(text[pos:])
        _font(run, size=size, bold=bold, italic=italic)


def add_p(doc, text, **kwargs):
    p = doc.add_paragraph()
    _fmt(p, **kwargs)
    size = 14
    add_rich(p, text, size=size)
    return p


def add_table(doc, rows):
    headers, body = rows[0], rows[1:]
    table = doc.add_table(rows=1 + len(body), cols=len(headers))
    table.style = "Table Grid"
    table.autofit = True
    for j, value in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = ""
        paragraph = cell.paragraphs[0]
        _fmt(paragraph, first=False, align="center")
        add_rich(paragraph, value, size=10, bold=True)
    for i, row in enumerate(body, start=1):
        for j, value in enumerate(row):
            cell = table.rows[i].cells[j]
            cell.text = ""
            paragraph = cell.paragraphs[0]
            _fmt(paragraph, first=False, align="left")
            add_rich(paragraph, value, size=10)
    return table


def parse_blocks(text):
    lines = text.splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("# "):
            blocks.append(("title", line[2:].strip()))
            i += 1
            continue
        if line.startswith("## "):
            blocks.append(("h", line[3:].strip()))
            i += 1
            continue
        if line.startswith("### "):
            blocks.append(("h3", line[4:].strip()))
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = lines[i].strip().strip("|")
                cells = [cell.strip() for cell in raw.split("|")]
                if not all(set(cell) <= set("-: ") for cell in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
            continue
        if line.startswith("\\["):
            chunk = [line]
            i += 1
            while i < len(lines) and lines[i].strip() != "\\]":
                chunk.append(lines[i])
                i += 1
            i += 1
            body = " ".join(part.strip() for part in chunk)
            body = body.replace("\\[", "").replace("\\]", "")
            body = re.sub(r"\s+", " ", body).strip()
            blocks.append(("formula", body, ""))
            continue
        if re.match(r"^\d+\. ", line):
            blocks.append(("item", line))
            i += 1
            continue
        paragraph = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "\\[")):
            if re.match(r"^\d+\. ", lines[i]):
                break
            paragraph.append(lines[i].strip())
            i += 1
        blocks.append(("p", " ".join(paragraph)))
    return blocks


def build():
    blocks = parse_blocks(MD.read_text(encoding="utf-8"))
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(1.5)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)

    pending_caption = None
    for block in blocks:
        kind = block[0]
        if kind == "title":
            p = doc.add_paragraph()
            _fmt(p, first=False, align="center", before=0, after=12)
            add_rich(p, block[1], bold=True)
        elif kind == "h":
            p = doc.add_paragraph()
            _fmt(p, first=False, align="center", before=12, after=6)
            add_rich(p, block[1], bold=True)
        elif kind == "h3":
            p = doc.add_paragraph()
            _fmt(p, first=False, align="center", before=8, after=4)
            add_rich(p, block[1], italic=True)
        elif kind == "formula":
            p = doc.add_paragraph()
            _fmt(p, first=False, align="center", before=6, after=6)
            add_rich(p, block[1], italic=True)
            if block[2]:
                add_rich(p, f"    ({block[2]})")
        elif kind == "item":
            add_p(doc, block[1], first=True, align="justify")
        elif kind == "p":
            text = block[1]
            if text.startswith("**Таблица"):
                pending_caption = text.replace("**", "")
                continue
            align = "center" if text.startswith("**УДК") or text.startswith("Ф. И. О.") or text.startswith("Рукопись") else "justify"
            first = align == "justify"
            add_p(doc, text, first=first, align=align, before=0, after=0)
        elif kind == "table":
            if pending_caption:
                p = doc.add_paragraph()
                _fmt(p, first=False, align="center", before=10, after=4)
                add_rich(p, pending_caption, italic=True)
                pending_caption = None
            add_table(doc, block[1])
            spacer = doc.add_paragraph()
            _fmt(spacer, first=False, after=6)
    doc.save(DOCX)
    return DOCX


if __name__ == "__main__":
    print(build())
