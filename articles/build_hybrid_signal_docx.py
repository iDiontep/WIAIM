# -*- coding: utf-8 -*-
"""Разделы 1–7 статьи о гибридном сигнале коленного модуля. Шаблон А4 «Вестника науки»."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
DOCX = ROOT / "hybrid_signal_knee.docx"
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


def _fmt(p, *, first=1.25, align="justify", before=0, after=0, left=0):
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.left_indent = Cm(left)
    pf.first_line_indent = Cm(first) if first else Cm(0)
    pf.alignment = {
        "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "center": WD_ALIGN_PARAGRAPH.CENTER,
        "left": WD_ALIGN_PARAGRAPH.LEFT,
        "right": WD_ALIGN_PARAGRAPH.RIGHT,
    }[align]


def add_text(p, text, size=14, bold=False, italic=False, sub=False, sup=False):
    run = p.add_run(text)
    _font(run, size=size, bold=bold, italic=italic)
    run.font.subscript = sub
    run.font.superscript = sup
    return run


def add_p(doc, text, **kwargs):
    size = kwargs.pop("size", 14)
    bold = kwargs.pop("bold", False)
    italic = kwargs.pop("italic", False)
    p = doc.add_paragraph()
    _fmt(p, **kwargs)
    add_text(p, text, size=size, bold=bold, italic=italic)
    return p


def add_h(doc, text):
    return add_p(doc, text, first=0, align="center", before=12, after=6, bold=True)


def add_labeled(doc, label, text):
    p = doc.add_paragraph()
    _fmt(p, first=1.25, align="justify")
    add_text(p, label, bold=True)
    add_text(p, text)
    return p


def add_ref(doc, text):
    p = doc.add_paragraph()
    _fmt(p, first=0, align="justify", after=4, left=0.75)
    p.paragraph_format.first_line_indent = Cm(-0.75)
    add_text(p, text, size=14)
    return p


def shade_header(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "F2F2F2")
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell(cell, text, *, bold=False, size=10):
    cell.text = ""
    p = cell.paragraphs[0]
    _fmt(p, first=0, align="center" if bold else "left")
    add_text(p, text, size=size, bold=bold)
    if bold:
        shade_header(cell)


def add_table(doc, caption, headers, rows):
    cap = doc.add_paragraph()
    _fmt(cap, first=0, align="center", before=10, after=4)
    add_text(cap, caption, italic=True)
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.autofit = True
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement("w:tblPr")
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    tblW.set(qn("w:w"), str(int(Cm(17).twips)))
    tblW.set(qn("w:type"), "dxa")
    for j, h in enumerate(headers):
        set_cell(table.rows[0].cells[j], h, bold=True)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            set_cell(table.rows[i].cells[j], val)
    add_p(doc, "", first=0, after=6)
    return table


def add_figure(doc, path, caption, width_cm=15.2):
    p = doc.add_paragraph()
    _fmt(p, first=0, align="center", before=8)
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width_cm))
    cap = doc.add_paragraph()
    _fmt(cap, first=0, align="center", after=8)
    add_text(cap, caption, italic=True)


def _box(ax, x, y, w, h, text):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.0, edgecolor="black", facecolor="white",
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=11)


def _arrow(ax, x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", mutation_scale=12,
            linewidth=1.0, color="black",
        )
    )


def draw_figures():
    FIG.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.family"] = FONT
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    _box(ax, 0.3, 4.3, 3.2, 1.1, "Миограмма EMG\nвеличина момента")
    _box(ax, 0.3, 2.45, 3.2, 1.1, "Сила опоры F\nзнак и допуск")
    _box(ax, 0.3, 0.6, 3.2, 1.1, "Углы колена и бедра\nкоэффициент")
    _box(ax, 6.2, 2.15, 3.2, 1.5, "Момент колена T")
    _arrow(ax, 3.5, 4.85, 6.2, 3.15)
    _arrow(ax, 3.5, 3.0, 6.2, 2.9)
    _arrow(ax, 3.5, 1.15, 6.2, 2.65)
    fig.tight_layout()
    block = FIG / "hybrid_block.png"
    fig.savefig(block, dpi=200)
    plt.close(fig)

    force = [i * 0.5 for i in range(0, 321)]

    def k_fg(f):
        if f <= 40:
            return 1.0
        if f >= 80:
            return 0.0
        return (80 - f) / 40

    def k_eg(f):
        if f <= 50:
            return 0.0
        if f >= 100:
            return 1.0
        return (f - 50) / 50

    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.plot(force, [k_fg(f) for f in force], color="black", linewidth=1.8, label="Сгибание, kFG")
    ax.plot(
        force, [k_eg(f) for f in force], color="black", linewidth=1.8,
        linestyle="--", label="Разгибание, kEG",
    )
    ax.set_xlim(0, 160)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel("Вертикальная сила опоры, Н")
    ax.set_ylabel("Коэффициент допуска")
    ax.legend(frameon=False, loc="center right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    thresh = FIG / "hybrid_thresholds.png"
    fig.savefig(thresh, dpi=200)
    plt.close(fig)
    return block, thresh


def add_formula(doc):
    p = doc.add_paragraph()
    _fmt(p, first=0, align="center", before=6, after=6)
    add_text(p, "T = k", italic=True)
    add_text(p, "FG", italic=True, sub=True)
    add_text(p, "(F) · k", italic=True)
    add_text(p, "FT", italic=True, sub=True)
    add_text(p, "(θ", italic=True)
    add_text(p, "thigh", italic=True, sub=True)
    add_text(p, ") · EMG − k", italic=True)
    add_text(p, "EG", italic=True, sub=True)
    add_text(p, "(F) · k", italic=True)
    add_text(p, "EK", italic=True, sub=True)
    add_text(p, "(θ", italic=True)
    add_text(p, "knee", italic=True, sub=True)
    add_text(p, ") · EMG + T", italic=True)
    add_text(p, "d", italic=True, sub=True)
    add_text(p, "    (1)")


def build():
    block, thresh = draw_figures()
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin = Cm(2.0)
    section.right_margin = Cm(2.0)

    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = Pt(14)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    core = doc.core_properties
    core.title = (
        "Гибридный сигнал коленного модуля: сила опоры как допуск фазы "
        "и миограмма как величина момента"
    )
    core.author = "Даниил Ионин"
    core.category = "Вестник науки"

    add_p(doc, "УДК 615.477.2:612.741", first=0, align="left")
    add_p(
        doc,
        "ГИБРИДНЫЙ СИГНАЛ КОЛЕННОГО МОДУЛЯ: СИЛА ОПОРЫ КАК ДОПУСК ФАЗЫ "
        "И МИОГРАММА КАК ВЕЛИЧИНА МОМЕНТА",
        first=0, align="center", before=12, after=12, bold=True,
    )
    add_p(doc, "Даниил Ионин", first=0, align="right", bold=True)
    add_p(
        doc,
        "Национальный исследовательский ядерный университет «МИФИ»,",
        first=0, align="right",
    )
    add_p(doc, "Россия, г. Москва", first=0, align="right", after=8)

    add_labeled(
        doc,
        "Аннотация: ",
        "В статье разбирается гибридный сигнал силового коленного модуля при подъёме по лестнице. "
        "Показано, что вертикальная сила опоры задаёт допуск и знак момента: сгибание разрешено "
        "при разгруженной стопе, разгибание — после порога нагрузки. Непрерывная миограмма одной "
        "задней мышцы культи задаёт величину этого момента и в опоре, и в переносе. В разобранной "
        "сессии одного человека величина видна по росту момента опоры вместе со скоростью и с "
        "дополнительным грузом и по подъёму спиной вперёд. Обычный перенос лицом вперёд миограмма "
        "почти не меняет, и шаг там во многом идёт на динамике голени. Отмечается, что чередующийся "
        "шаг и смена темпа уже получаются по одним механическим датчикам, а сравнения с таким законом "
        "источник не содержит. В заключение механика оставлена контуром безопасности, а проверка "
        "двух ролей на модуле «Комета» записана как программа измерений, а не как результат.",
    )
    add_labeled(
        doc,
        "Ключевые слова: ",
        "коленный модуль протеза, гибридное управление, поверхностная электромиография, "
        "сила опоры, подъём по лестнице, естественность ходьбы.",
    )
    add_p(
        doc,
        "HYBRID KNEE-MODULE SIGNAL: GROUND REACTION FORCE AS PHASE PERMISSION "
        "AND THE MYOGRAM AS TORQUE MAGNITUDE",
        first=0, align="center", before=12, after=8, bold=True,
    )
    add_p(
        doc,
        "The paper analyses a hybrid signal of a powered knee module during stair ascent. "
        "Vertical ground reaction force sets the permission and the sign of knee torque: flexion "
        "is allowed when the foot is unloaded, and extension after a load threshold. A continuous "
        "myogram of one posterior residual muscle sets the torque magnitude in both stance and swing. "
        "In the single-subject session examined here, that magnitude appears as stance torque rising "
        "with speed and with an added load, and as backward stair ascent. During ordinary forward "
        "swing the myogram barely changes the torque, and the step largely follows the shank dynamics. "
        "Alternating steps and a change of cadence are already obtained from mechanical sensors alone, "
        "and the source does not compare the law with such a controller. Mechanics is left as the safety "
        "loop, and a check of the two roles on the Kometa knee module is stated as a measurement "
        "programme, not as a result.",
        first=1.25, align="justify",
    )
    add_labeled(
        doc,
        "Key words: ",
        "prosthetic knee module, hybrid control, surface electromyography, ground reaction force, "
        "stair ascent, gait naturalness.",
    )

    add_h(doc, "Введение")
    add_p(
        doc,
        "Подъём по лестнице требует положительной работы колена в опоре [1]. Силовой протез отдаёт "
        "эту работу по закону, который должен совпасть с шагом человека. В распространённом законе "
        "фазу ведут встроенные механические датчики, без непрерывной команды мышцы [2]. На лестнице "
        "такой закон уже даёт просвет над ступенью, удобный темп и разный рисунок шага [3]. "
        "Момент, который человек задал бы сокращением мышцы при том же положении культи, из этих "
        "датчиков не следует. Поверхностная миограмма его даёт, но электрод в гильзе легко теряет "
        "контакт, и ложное сокращение не должно переворачивать нагруженное колено.",
    )
    add_p(
        doc,
        "Цель статьи — выделить роли сигналов в гибридном законе коленного модуля и указать, "
        "какое наблюдаемое свойство лестничного шага связано с каждой ролью. Предмет — опубликованный "
        "контроллер подъёма, в котором одна миограмма задней мышцы культи задаёт величину момента, "
        "а вертикальная сила разрешает сгибание или разгибание. Тезис состоит в том, что сила "
        "является сигналом допуска и знака, миограмма — сигналом величины в обеих фазах. Вклад "
        "величины виден по опоре с грузом и по нестандартному переносу. Обычный перенос вперёд "
        "этот вклад почти не показывает.",
    )
    add_p(
        doc,
        "Дальше статья идёт от проблемы к этому тезису. Сначала зафиксировано, зачем вообще отделять "
        "допуск от величины. Затем собраны три схемы, из которых получается гибрид, и разобран "
        "один лестничный закон с формулой и порогами силы. После этого зафиксировано, что здесь "
        "называется естественностью, сведены роли сигналов и показано, какой контур остаётся у механики. "
        "Последний раздел ограничивает вывод одним испытуемым и одной сессией. Проверка тех же ролей "
        "на модуле «Комета» записана как программа измерений, без собственных результатов и без "
        "утверждения, что гибрид превосходит механический закон.",
    )

    add_h(doc, "1. Проблема")
    add_p(
        doc,
        "Подъём по лестнице требует в фазе опоры положительной работы колена и голеностопа: "
        "эти суставы поднимают массу тела, а не только тормозят движение голени [1]. "
        "Пассивный коленный модуль такую работу не отдаёт. Силовой модуль отдаёт её только тогда, "
        "когда момент согласован с шагом человека.",
    )
    add_p(
        doc,
        "Серийные силовые протезы и большая часть лабораторных законов ведут эту согласованность "
        "по встроенным механическим датчикам и по конечному автомату фазы. Непрерывной команды "
        "от мышцы в таком законе нет [2]. На лестнице адаптивный механический контроллер уже "
        "меняет просвет над ступенью по положению бедра в переносе и помощь в опоре по углу колена "
        "в момент контакта стопы. Человек поднимается в удобном ему темпе и разным рисунком шага: "
        "приставным, чередующимся и через ступень [3]. Команда сустава при этом выведена из движения "
        "культи и из состояния протеза. Момента, который человек задал бы сокращением мышцы "
        "при том же положении культи, в этом законе нет.",
    )
    add_p(
        doc,
        "Поверхностная миограмма такой момент даёт. Одновременно это хрупкий канал. Электрод "
        "смещается в гильзе, на сигнал влияют пот, утомление мышцы и кровенаполнение культи. "
        "Если ложных событий больше, чем полезных, канал не оправдывает усложнения протеза. "
        "Вопрос статьи в том, при каком разделении сигналов миограмма на лестнице сохраняет "
        "величину момента и не получает права сменить его знак под нагрузкой.",
    )

    add_h(doc, "2. Три схемы, из которых собирается гибрид")
    add_p(
        doc,
        "Из опубликованных законов складываются три схемы. Гибридный сигнал не подменяет их "
        "одним датчиком. Он оставляет каждой схеме свою роль.",
    )
    add_p(
        doc,
        "Первая схема механическая. Положение бедра в переносе задаёт траекторию просвета, "
        "угол колена в момент постановки стопы задаёт момент в опоре [3]. Датчик силы "
        "и инерциальный модуль сообщают фазу и темп. Сокращение остаточной мышцы в формулу "
        "момента не входит. Человек влияет на протез тем, как двигает культю и как нагружает стопу.",
    )
    add_p(
        doc,
        "Вторая схема вводит миограмму в момент лестницы и различает опору и перенос. "
        "В опыте чередующегося подъёма момент колена в опоре пропорционален поверхностной "
        "миограмме мышц остаточного бедра, контакт стопы переключает равновесие импеданса, "
        "а перенос в основном держит номинальный импеданс. Проверка выполнена на одном человеке "
        "с односторонней ампутацией бедра [4]. Отдельно описано волевое управление протезным "
        "коленом по поверхностной миограмме вне опоры на протез [5]. К лестничному шагу "
        "эта вторая работа не относится.",
    )
    add_p(
        doc,
        "Третья схема ограничивает миограмму опорой. В совместном нейронном управлении "
        "разгибающий момент колена в опоре пропорционален миограмме остаточной biceps femoris, "
        "а перенос ведётся по движению культи. На двух людях с ампутацией бедра так получены "
        "вставание, присед, выпад, ходьба и переходы между этими действиями без отдельной метки "
        "режима. Лестница в протокол не входила [6].",
    )
    add_p(
        doc,
        "Контроллер лестницы 2023 года собирает из этих пределов четвёртую схему [7]. "
        "Ограничение миограммы одной опорой снижает участие человека: протезом можно управлять "
        "только пока стопа на земле, и подъёма по лестнице такой предел не даёт. Съём сгибания "
        "и разгибания с пары мышц-антагонистов упирается в совместную активацию и перекрёстные "
        "помехи, так что два направления трудно развести даже после обучения. Волевую миограмму "
        "вне опоры, описанную в [5], тот же разбор относит к схемам, из которых закон ходьбы "
        "не получился. Поэтому в гибриде остаётся одна мышца на оба знака момента, а знак "
        "выбирает не классификатор режима и не вторая мышца, а сила опоры.",
    )
    add_figure(
        doc, block,
        "Рисунок 1 – Роли в гибридном сигнале: миограмма задаёт величину, сила опоры задаёт знак "
        "и допуск, углы меняют коэффициент",
    )

    add_h(doc, "3. Разбор контроллера лестницы")
    add_p(
        doc,
        "Разобранный закон реализован на силовом колене Utah Bionic Knee с пассивной стопой "
        "Ottobock Taleo. Вертикальную силу измеряет тензодатчик в пирамидке между коленом и стопой. "
        "Один электрод Ottobock 13E202 стоит внутри гильзы на задней поверхности культи, "
        "над остаточной biceps femoris. Испытуемый один: мужчина 32 лет, 77,25 кг, рост 1,8 м, "
        "шесть лет после ампутации бедра. Знакомство с контроллером на лестнице из четырёх ступеней "
        "заняло около 15 минут, запись сделана на лестнице из 11 ступеней за одну сессию [7].",
    )
    add_p(
        doc,
        "Момент колена складывается из сгибающей и разгибающей частей, обе пропорциональны "
        "одной и той же миограмме, и из демпфирования:",
    )
    add_formula(doc)
    add_p(
        doc,
        "Здесь T — заданный момент колена, EMG — непрерывный сигнал одной мышцы, F — вертикальная "
        "сила опоры, θthigh — ориентация бедра по инерциальному датчику, θknee — угол колена, "
        "Td — момент виртуального демпфирования. Коэффициенты kFG и kEG зависят только от силы "
        "и решают допуск. Коэффициенты kFT и kEK зависят от положения ноги и меняют чувствительность. "
        "Класса «лестница» в формуле нет.",
    )
    add_p(
        doc,
        "Сгибание от миограммы разрешено, когда стопа почти разгружена. Коэффициент kFG равен 1 "
        "при силе ниже 40 Н и равен 0 при силе выше 80 Н; между этими порогами он спадает линейно. "
        "Разгибание от миограммы разрешено, когда стопа нагружена. Коэффициент kEG равен 0 при силе "
        "ниже 50 Н, линейно растёт до 1 между 50 и 100 Н и дальше остаётся равным 1. Пока человек "
        "не поставил на протез вес больше 50 Н, миограмма колено не разгибает. Пока сила выше 80 Н, "
        "та же миограмма колено не сгибает. Переход между знаками непрерывен по силе, а не переключён "
        "меткой фазы [7]. Зависимость коэффициентов от силы показана на рисунке 2.",
    )
    add_figure(
        doc, thresh,
        "Рисунок 2 – Допуск сгибания и разгибания по вертикальной силе опоры. "
        "Пороги взяты из закона (1): 40–80 Н для сгибания и 50–100 Н для разгибания",
        width_cm=14.5,
    )
    add_p(
        doc,
        "Углы не заменяют ни силу, ни миограмму. Чувствительность сгибания высока в начале переноса, "
        "когда бедро близко к вертикали и голень нужно быстро убрать со ступени, и падает к нулю "
        "к концу переноса, когда бедро ушло вперёд и стопа зависает над следующей ступенью. "
        "Чувствительность разгибания высока в начале опоры, при согнутом колене, и падает к нулю "
        "по мере разгибания, когда подъём тела уже сделан. Демпфирование притормаживает колено "
        "в конце переноса и у полного разгибания. После ампутации бедра biceps femoris теряет "
        "функцию сгибания колена и остаётся разгибателем тазобедренного сустава. В опоре при подъёме "
        "она и так активна, то есть пользователю не предлагают новый рисунок сокращения для "
        "разгибающего момента [7].",
    )
    add_p(
        doc,
        "На этой схеме человек поднялся чередующимся шагом быстро и медленно, с рюкзаком 13,6 кг "
        "и без него, а также спиной вперёд. Длительность шага составила 3,9 ± 0,2 с на медленном "
        "подъёме и 1,6 ± 0,2 с на быстром. Пик разгибающего момента в опоре вырос с 39,6 ± 9,8 Н·м "
        "до 50,4 ± 17,4 Н·м, то есть на 27 %. Пик сгибающего момента в переносе при этом почти "
        "не изменился: 5,7 ± 2,0 Н·м и 5,5 ± 1,1 Н·м, разница 4,4 %. С рюкзаком видимой разницы "
        "траектории угла колена не отмечено, а пик разгибания в опоре вырос с 35,6 ± 7,3 Н·м "
        "до 54,3 ± 4,6 Н·м, на 53 %. Мощность в опоре выросла на 78 %. Сгибающий момент в переносе "
        "остался близким: 4,8 ± 1,1 Н·м без груза и 4,2 ± 0,8 Н·м с грузом [7].",
    )
    add_p(
        doc,
        "Подъём спиной вперёд меняет уже перенос. Пик угла колена в переносе составил 98,1 ± 7,8° "
        "лицом вперёд и 71,0 ± 4,4° спиной вперёд. Пик сгибающего момента вырос с 4,3 ± 1,5 Н·м "
        "до 8,6 ± 1,4 Н·м, пик миограммы — с 1,6 ± 0,6 В до 3,7 ± 0,3 В. В обсуждении темп "
        "чередующегося подъёма на этом контроллере оценен диапазоном 31–75 ступеней в минуту [7]. "
        "Все числа относятся к одному человеку и к одной сессии.",
    )

    add_h(doc, "4. Что в этой статье называется естественностью")
    add_p(
        doc,
        "Естественность здесь не ощущение «своей ноги» и не близость кривой к средней кривой "
        "здорового шага. В статье она означает четыре наблюдаемых свойства лестничного подъёма "
        "на разобранном контроллере. Первое — чередующийся шаг, а не только приставной. "
        "Второе — смена темпа в диапазоне 31–75 ступеней в минуту. Третье — рост момента в опоре "
        "вместе со скоростью и с дополнительным грузом. Четвёртое — возможность поставить стопу "
        "иначе, чем вперёд, с соответствующим ростом миограммы и сгибающего момента.",
    )
    add_p(
        doc,
        "Первые два свойства механический адаптивный закон уже показывает без миограммы: "
        "чередующийся подъём, удобный темп и разный рисунок шага получены по положению бедра "
        "и углу колена [3]. Вкладом канала величины в разобранном опыте остаются два других. "
        "При том же типе подъёма момент опоры меняется вместе с грузом, хотя траектория угла "
        "колена визуально не расходится. В переносе лицом вперёд момент сгибания почти не зависит "
        "от скорости и груза: авторы относят это к пассивной динамике голени. Миограмма становится "
        "решающей, когда постановка стопы нестандартная, как при подъёме спиной вперёд [7].",
    )
    add_p(
        doc,
        "В это определение не входят симметрия шага со сохранённой ногой, расход энергии, "
        "фантомная боль и устойчивость эффекта через 3, 6 и 12 месяцев. Разобранный источник "
        "этого не измерял. Не входит и сравнение с тем же человеком на контроллере без миограммы: "
        "такого сравнения в сессии не было. Поэтому четыре свойства описывают, что удалось "
        "наблюдать, и не являются оценкой превосходства над другими законами.",
    )

    add_h(doc, "5. Роли сигналов")
    add_p(
        doc,
        "Гибридный сигнал — это назначение ролей, а не список датчиков. Сила опоры несёт допуск "
        "и знак. Непрерывная миограмма одной задней мышцы несёт величину в обеих фазах. "
        "Углы несут коэффициент чувствительности и демпфирование. В обычном переносе вперёд "
        "величина момента мала и шаг во многом идёт на динамике голени. В нестандартном переносе "
        "ту же величину снова несёт миограмма. Сонарография A-mode, то есть ультразвуковой снимок "
        "деформации мышцы, в литературе рассмотрена как возможная замена канала величины: "
        "по ней офлайн отличали режим ходьбы у людей с ампутацией бедра [8]. В закон (1) "
        "она не входила. Сводка ролей приведена в таблице 1.",
    )
    add_table(
        doc,
        "Таблица 1 – Роли сигналов в гибридном контуре лестницы",
        ["Роль", "Какой сигнал её несёт", "Чем это показано"],
        [
            [
                "Допуск фазы и знак момента",
                "Вертикальная сила опоры",
                "Сгибание разрешено ниже 40–80 Н, разгибание — после 50–100 Н [7]",
            ],
            [
                "Величина момента в опоре",
                "Непрерывная миограмма biceps femoris",
                "Момент разгибания растёт со скоростью на 27 % и с рюкзаком 13,6 кг на 53 % "
                "при сходной траектории угла [7]",
            ],
            [
                "Обычный перенос вперёд",
                "Динамика голени; миограмма величину почти не меняет",
                "Разница сгибающего момента между быстрым и медленным подъёмом 4,4 % [7]",
            ],
            [
                "Нестандартная постановка стопы",
                "Та же миограмма",
                "Подъём назад: миограмма с 1,6 ± 0,6 В до 3,7 ± 0,3 В, момент с 4,3 ± 1,5 Н·м "
                "до 8,6 ± 1,4 Н·м [7]",
            ],
            [
                "Возможная замена канала величины",
                "Сонарография A-mode",
                "Офлайн-распознавание режима ходьбы; в закон (1) не входила [8]",
            ],
        ],
    )
    add_p(
        doc,
        "Таблица задаёт состав измерительной схемы коленного модуля. Тензодатчик вертикальной силы "
        "обязателен как допуск: без него одна миограмма не знает, сгибать колено или разгибать. "
        "Один канал миограммы обязателен как величина: без него груз и подъём назад нечем задать "
        "отдельно от положения культи. Второй мышечный канал и метка режима для этого закона "
        "не требуются. Сонарография остаётся кандидатом на место миограммы, если электрод "
        "в гильзе не удаётся удержать, и не вторым независимым законом переноса.",
    )

    add_h(doc, "6. Что остаётся механике")
    add_p(
        doc,
        "Порог силы — прямой ответ на ложное срабатывание миограммы. Пока тензодатчик видит "
        "нагрузку выше 80 Н, сокращение мышцы не переводит колено в сгибание. Пока нагрузка "
        "ниже 50 Н, то же сокращение не начинает разгибать колено и поднимать тело. Механический "
        "контур по силе и углу поэтому не отменяется и не считается временной заменой биосигнала. "
        "Он держит безопасность опоры и фазу. Инерциальный датчик бедра и угол колена остаются "
        "в коэффициентах kFT и kEK и в демпфировании: они согласуют чувствительность с положением "
        "ноги [7].",
    )
    add_p(
        doc,
        "Миограмма добавляет то, чего из этих механических каналов не вывести. При рюкзаке "
        "траектория угла колена визуально та же, а момент разгибания в опоре другой. При подъёме "
        "назад растёт и миограмма, и сгибающий момент переноса. Оба факта получены на одном "
        "человеке [7]. Микропроцессорное управление по датчикам изделия сохраняет за собой "
        "ровный шаг, узнавание опоры и запрет опасного знака момента. Гибрид подключает биосигнал "
        "туда, где величина момента должна следовать за намерением, а не за уже случившимся "
        "движением культи.",
    )

    add_h(doc, "7. Ограничения и следующий шаг")
    add_p(
        doc,
        "Опыт, на котором держится разбор, ограничен самим источником. Испытуемый один, "
        "разнообразие длины культи и силы остаточных мышц в него не входит. Нет разбора "
        "сохранённой ноги и корпуса, поэтому влияние закона на весь шаг неизвестно. "
        "Нет сравнения с тем же человеком без миограммы, поэтому выигрыш относительно "
        "механического контроллера лестницы не измерен. Закон (1) относится к подъёму. "
        "Переносится ли одна мышца и те же пороги силы на спуск, ровную ходьбу и неровную "
        "поверхность, по этой сессии не видно [7]. Сонарография в замкнутый контур момента "
        "не ставилась [8].",
    )
    add_p(
        doc,
        "Отсюда не следует, что гибридная схема превосходит другие по естественности. "
        "Следует более узкое утверждение. В опубликованном лестничном законе вертикальная сила "
        "является сигналом допуска и знака, непрерывная миограмма одной задней мышцы — сигналом "
        "величины момента в обеих фазах, а вклад величины виден по опоре с грузом и по "
        "нестандартному переносу. Обычный перенос вперёд этот вклад почти не показывает.",
    )
    add_p(
        doc,
        "Проверка на коленном модуле «Комета» по этому разбору является программой, а не результатом. "
        "Новый датчик для неё не разрабатывается: нужны уже имеющиеся тензодатчик вертикальной силы "
        "и один канал поверхностной миограммы с задней поверхности культи. Сценариев три. "
        "Первый — ровный шаг, чтобы увидеть, открывает ли сила разгибание только после опоры "
        "и не даёт ли миограмме согнуть нагруженное колено. Второй — подъём лицом вперёд, "
        "чтобы увидеть, меняется ли момент опоры при том же рисунке угла, если меняется нагрузка. "
        "Третий — постановка стопы с изменением зазора в переносе, чтобы увидеть, меняет ли "
        "миограмма сгибающий момент, когда движение перестаёт совпадать с динамикой голени. "
        "Критерий успеха разделён по ролям. Сила считается пригодной, если она открывает "
        "и закрывает знак момента на порогах того же порядка, что в законе (1). Миограмма "
        "считается пригодной, если при закрытом знаке её рост меняет величину момента в опоре "
        "и в нестандартном переносе. Классификатор режима в эту проверку не входит: базовый "
        "гибрид обходится без метки «лестница». Ощущение человека, расход энергии и повтор "
        "через месяцы в эту проверку тоже не входят. Их нужно закладывать отдельным протоколом, "
        "после того как роли двух каналов на модуле подтверждены записью.",
    )

    add_h(doc, "Список литературы")
    refs_ru = [
        "[1] McFadyen B. J., Winter D. A. An integrated biomechanical analysis of normal stair "
        "ascent and descent // Journal of Biomechanics. 1988. Vol. 21, № 9. P. 733–744.",
        "[2] Fleming A., Stafford N., Huang S. и др. Myoelectric control of robotic lower limb "
        "prostheses: a review of electromyography interfaces, control paradigms, challenges and "
        "future directions // Journal of Neural Engineering. 2021. Vol. 18, № 4. Art. 041004.",
        "[3] Hood S., Gabert L., Lenzi T. Powered knee and ankle prosthesis with adaptive control "
        "enables climbing stairs with different stair heights, cadences, and gait patterns "
        "// IEEE Transactions on Robotics. 2022. Vol. 38, № 3. P. 1430–1441.",
        "[4] Hoover C. D., Fulk G. D., Fite K. B. Stair ascent with a powered transfemoral "
        "prosthesis under direct myoelectric control // IEEE/ASME Transactions on Mechatronics. "
        "2013. Vol. 18, № 3. P. 1191–1200.",
        "[5] Ha K. H., Varol H. A., Goldfarb M. Volitional control of a prosthetic knee using "
        "surface electromyography // IEEE Transactions on Biomedical Engineering. 2011. Vol. 58, "
        "№ 1. P. 144–151.",
        "[6] Hunt G. R., Hood S., Lenzi T. Stand-up, squat, lunge, and walk with a robotic knee "
        "and ankle prosthesis under shared neural control // IEEE Open Journal of Engineering "
        "in Medicine and Biology. 2021. Vol. 2. P. 267–277.",
        "[7] Creveling S., Cowan M., Sullivan L. M. и др. Volitional EMG control enables stair "
        "climbing with a robotic powered knee prosthesis // IEEE/RSJ International Conference "
        "on Intelligent Robots and Systems (IROS). Detroit, 2023. P. 2152–2157.",
        "[8] Murray R., Mendez J., Gabert L. и др. Ambulation mode classification of individuals "
        "with transfemoral amputation through A-mode sonomyography and convolutional neural "
        "networks // Sensors. 2022. Vol. 22, № 23. Art. 9350.",
    ]
    for item in refs_ru:
        add_ref(doc, item)

    add_h(doc, "Bibliography")
    refs_en = [
        "[1] McFadyen B. J., Winter D. A. An integrated biomechanical analysis of normal stair "
        "ascent and descent. Journal of Biomechanics, 1988, vol. 21, no. 9, pp. 733–744.",
        "[2] Fleming A., Stafford N., Huang S., et al. Myoelectric control of robotic lower limb "
        "prostheses: a review of electromyography interfaces, control paradigms, challenges and "
        "future directions. Journal of Neural Engineering, 2021, vol. 18, no. 4, art. 041004.",
        "[3] Hood S., Gabert L., Lenzi T. Powered knee and ankle prosthesis with adaptive control "
        "enables climbing stairs with different stair heights, cadences, and gait patterns. "
        "IEEE Transactions on Robotics, 2022, vol. 38, no. 3, pp. 1430–1441.",
        "[4] Hoover C. D., Fulk G. D., Fite K. B. Stair ascent with a powered transfemoral "
        "prosthesis under direct myoelectric control. IEEE/ASME Transactions on Mechatronics, "
        "2013, vol. 18, no. 3, pp. 1191–1200.",
        "[5] Ha K. H., Varol H. A., Goldfarb M. Volitional control of a prosthetic knee using "
        "surface electromyography. IEEE Transactions on Biomedical Engineering, 2011, vol. 58, "
        "no. 1, pp. 144–151.",
        "[6] Hunt G. R., Hood S., Lenzi T. Stand-up, squat, lunge, and walk with a robotic knee "
        "and ankle prosthesis under shared neural control. IEEE Open Journal of Engineering "
        "in Medicine and Biology, 2021, vol. 2, pp. 267–277.",
        "[7] Creveling S., Cowan M., Sullivan L. M., et al. Volitional EMG control enables stair "
        "climbing with a robotic powered knee prosthesis. IEEE/RSJ International Conference "
        "on Intelligent Robots and Systems (IROS), Detroit, 2023, pp. 2152–2157.",
        "[8] Murray R., Mendez J., Gabert L., et al. Ambulation mode classification of individuals "
        "with transfemoral amputation through A-mode sonomyography and convolutional neural "
        "networks. Sensors, 2022, vol. 22, no. 23, art. 9350.",
    ]
    for item in refs_en:
        add_ref(doc, item)

    doc.save(DOCX)
    return DOCX


if __name__ == "__main__":
    print(build())
