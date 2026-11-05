# -*- coding: utf-8 -*-
"""Статья «Вестник науки», шаблон А4: обзор сигналов управления протезом."""
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent
DOCX = ROOT / "obzor_signalov_proteza_nizhney_konechnosti.docx"
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


def add_labeled(doc, label, text):
    p = doc.add_paragraph()
    _fmt(p, first=1.25, align="justify")
    add_text(p, label, bold=True)
    add_text(p, text)
    return p


def add_h(doc, text):
    return add_p(doc, text, first=0, align="center", before=12, after=6, bold=True)


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


def set_cell(cell, text, *, bold=False, size=11):
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
        set_cell(table.rows[0].cells[j], h, bold=True, size=11)
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            set_cell(table.rows[i].cells[j], val, size=11)
    add_p(doc, "", first=0, after=6)
    return table


def build():
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
    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

    core = doc.core_properties
    core.title = "Обзор методов получения сигналов управления протезом нижней конечности"
    core.author = "Даниил Ионин"
    core.category = "Вестник науки"

    add_p(doc, "УДК 615.477.2:612.741", first=0, align="left")
    add_p(
        doc,
        "ОБЗОР МЕТОДОВ ПОЛУЧЕНИЯ СИГНАЛОВ УПРАВЛЕНИЯ ПРОТЕЗОМ НИЖНЕЙ КОНЕЧНОСТИ",
        first=0, align="center", before=12, after=12, bold=True,
    )
    add_p(doc, "Даниил Ионин", first=0, align="right", bold=True)
    add_p(
        doc,
        "Национальный исследовательский ядерный университет «МИФИ»,",
        first=0, align="right",
    )
    add_p(doc, "Россия, г. Москва", first=0, align="right", after=6)

    add_labeled(
        doc,
        "Аннотация: ",
        "В статье рассматривается получение сигналов, по которым активный протез нижней конечности "
        "выбирает момент сустава и режим ходьбы. Показано, что лабораторные силовые модули опираются "
        "на угол сустава, нагрузку в гильзе и датчики самого протеза, а волевое намерение снимают "
        "поверхностной электромиограммой остаточных мышц. Большое место занимает различие двух контуров: "
        "прямого отображения миограммы в момент колена и распознавания режима локомоции. "
        "Отмечается, что механические датчики протеза выделяют стояние, посадку и ходьбу без приборов "
        "на сохранённой ноге. Подчеркивается, что добавление электромиограммы к этим каналам снижает "
        "ошибку распознавания перехода между ровной поверхностью, пандусом и лестницей, а направленная "
        "мышечная реиннервация добавляет каналы с мышц бедра. В основной части сопоставлены источник "
        "сигнала, вычисляемая команда и условия, в которых команда действует. В заключение указано, "
        "что проверку опоры сохраняют по механике протеза, а биосигнал используют как добавку момента "
        "или как признак смены режима.",
    )
    add_labeled(
        doc,
        "Ключевые слова: ",
        "протез нижней конечности, сигнал управления, поверхностная электромиография, "
        "распознавание намерения, импедансное управление, мехатроника.",
    )

    add_p(
        doc,
        "REVIEW OF METHODS FOR ACQUIRING CONTROL SIGNALS OF A LOWER-LIMB PROSTHESIS",
        first=0, align="center", before=12, after=8, bold=True,
    )
    add_p(
        doc,
        "The paper considers the signals by which an active lower-limb prosthesis selects joint torque "
        "and the locomotion mode. Laboratory powered modules rely on joint angle, socket load and the "
        "prosthesis sensors themselves, while volitional intent is taken from the surface electromyogram "
        "of residual muscles. Two loops are distinguished: a direct mapping of the myogram into knee "
        "torque and recognition of the locomotion mode. Prosthesis sensors alone separate standing, "
        "sitting and walking without instruments on the intact leg. Adding the electromyogram to these "
        "channels lowers the error of transitions among level ground, ramps and stairs, and targeted "
        "muscle reinnervation adds channels from thigh muscles. The source of the signal, the command "
        "computed from it and the conditions in which the command acts are compared. Stance safety "
        "remains a mechanical check, and the biosignal is used as a torque increment or as a feature "
        "of a mode change.",
        first=1.25, align="justify",
    )
    add_labeled(
        doc,
        "Key words: ",
        "lower-limb prosthesis, control signal, surface electromyography, intent recognition, "
        "impedance control, mechatronics.",
    )

    add_h(doc, "Введение")
    add_p(
        doc,
        "После ампутации бедра или голени сустав протеза и мышцы, которые двигали утраченный сегмент, "
        "разъединены. Пассивный модуль запасает и рассеивает энергию шага. Подъём по лестнице, подъём "
        "по уклону и отталкивание стопой требуют положительной работы колена, голеностопа или обоих "
        "суставов, и пассивный узел эту работу не отдаёт. Активный протез способен отдать момент, если "
        "команда согласована с фазой шага и с намерением человека. Обзоры управления разделяют эту "
        "задачу на верхний уровень, где выбирают деятельность, средний, где задают закон внутри "
        "деятельности, и нижний, где отрабатывают момент привода [1]. Сигнал управления — это измерение, "
        "по которому один из уровней принимает решение.",
    )
    add_p(
        doc,
        "Источники измерения делятся на две группы. К первой относятся датчики самого изделия: угол и "
        "угловая скорость сустава, сила в приводе, нагрузка между гильзой и модулем. Ко второй относится "
        "электромиограмма остаточных мышц, то есть электрическое следствие команды, которую центральная "
        "нервная система уже послала к периферии. Серийные микропроцессорные колени долгое время "
        "обходились первой группой. Миоэлектрический контур добавляет вторую и тем самым возвращает "
        "человеку канал, которого нет в чисто механическом законе [4]. Цель работы — сопоставить "
        "способы получения этих сигналов и показать, какую команду каждый способ способен выдать "
        "коленному и голеностопному модулю. Клиническая эффективность устройств по цитируемым опытам "
        "не доказывается: числа ниже взяты из самих источников и относятся к описанным там условиям.",
    )

    add_h(doc, "Механические сигналы протеза")
    add_p(
        doc,
        "Силовой протез бедра с приводами колена и голеностопа можно вести по импедансу, не задавая "
        "жёсткую траекторию угла. В лабораторном пневматическом прототипе на каждом суставе стоят "
        "датчик угла и датчик силы цилиндра, по которому судят о моменте. Между гильзой и модулем "
        "установлен трёхосевой датчик: осевая сила, момент в сагиттальной плоскости и момент во "
        "фронтальной. По этим каналам цикл шага делят на четыре состояния. Удар пятки открывает "
        "подгрузку, угол тыльного сгибания стопы открывает отталкивание, разгрузка стопы открывает "
        "перенос, знак угловой скорости колена отделяет сгибание переноса от разгибания. Внутри "
        "состояния момент пассивен и складывается из линейной жёсткости, кубической жёсткости "
        "относительно равновесного угла и линейного демпфирования по угловой скорости [2]:",
    )
    formula = doc.add_paragraph()
    _fmt(formula, first=0, align="center", before=6, after=6)
    add_text(formula, "τ = k", italic=True)
    add_text(formula, "1", italic=True, sub=True)
    add_text(formula, "(θ − θ", italic=True)
    add_text(formula, "e", italic=True, sub=True)
    add_text(formula, ") + k", italic=True)
    add_text(formula, "2", italic=True, sub=True)
    add_text(formula, "(θ − θ", italic=True)
    add_text(formula, "e", italic=True, sub=True)
    add_text(formula, ")", italic=True)
    add_text(formula, "3", italic=True, sup=True)
    add_text(formula, " + bθ̇", italic=True)
    add_text(formula, "    (1)")
    add_p(
        doc,
        "Здесь τ — момент сустава, θ — измеренный угол, θe — равновесный угол текущего состояния, "
        "k1 и k2 — коэффициенты жёсткости, b — коэффициент демпфирования. Пока коэффициенты "
        "положительны, сустав внутри состояния приходит к равновесию и сам по себе мощность не "
        "отдаёт. Мощность появляется при смене равновесного угла, а смену запускает измерение "
        "на протезе, то есть действие пользователя. Если следующее состояние не наступило, модуль "
        "остаётся в текущем равновесии. Такой закон координации шага по ровной поверхности обходится "
        "без прибора на сохранённой ноге и без электромиограммы [2].",
    )
    add_p(
        doc,
        "Те же механические каналы используют и выше, на уровне выбора деятельности. По кадрам "
        "сигналов протеза строят признаки, снижают размерность и относят кадр к стоянию, посадке "
        "или ходьбе. Обученные модели затем работают в реальном времени и переключают средний "
        "контур. В опыте с одним человеком с односторонней ампутацией бедра распознаватель отметил "
        "все 90 задуманных переходов между этими тремя деятельностями. Шесть переходов были отмечены "
        "без намерения пользователя. Средние контуры специально перекрывались по функции, и эти "
        "шесть ошибок не нарушили пользование и не были замечены. Приборы на сохранённой ноге "
        "для этого распознавания не требовались [3].",
    )
    add_p(
        doc,
        "Механический сигнал появляется после того, как протез уже начал движение или уже принял "
        "нагрузку. Для ровной ходьбы и для тройки «стояние — посадка — ходьба» этого достаточно. "
        "Переход на лестницу или пандус желательно узнать раньше, чем он полностью проявится "
        "в угле и в силе. Здесь измерение с протеза дополняют сигналом, который возникает "
        "в мышце до видимого шага.",
    )

    add_h(doc, "Поверхностная электромиограмма")
    add_p(
        doc,
        "Поверхностная электромиограмма — напряжение на коже над мышцей, связанное с её активацией. "
        "Для протеза голени часть мышц голени может сохраниться. Для протеза бедра голень утрачена, "
        "и источник остаётся на культе бедра: передняя и задняя группы, в том числе под гильзой. "
        "Обзор миоэлектрического управления силовым протезом нижней конечности сводит интерфейс "
        "к четырём вопросам: как устроен мышечный источник, включая хирургическое усиление канала, "
        "каким датчиком снимают сигнал, каким алгоритмом его декодируют и в какой закон попадает "
        "результат — в надзорный выбор режима или в прямую команду момента [4]. Автономный закон "
        "по датчикам изделия уже ведёт циклический шаг. Электромиограмма добавляет эфферентный "
        "канал, которого в автономном законе нет.",
    )
    add_p(
        doc,
        "Снимаемый сигнал нестационарен в течение шага, поэтому классификатор режима привязывают "
        "к фазе, а не строят одно правило на весь цикл. В исследовании семи режимов — ровная ходьба, "
        "перешагивание препятствия, подъём и спуск по лестнице, поворот в сторону измерительной ноги, "
        "поворот в противоположную сторону и стояние — для восьми людей без ампутации электроды "
        "ставили над мышцами выше колена, чтобы приблизить набор к культе бедра. Средние ошибки "
        "распознавания в четырёх выделенных фазах составили 12,4 ± 5,0 %, 6,0 ± 4,7 %, 7,5 ± 5,1 % "
        "и 5,2 ± 3,7 %. Пилотная проверка на двух людях с высокой ампутацией бедра дала сопоставимый "
        "порядок ошибок [5]. Эти проценты описывают распознавание режима по записанной миограмме. "
        "Они не равны ошибке момента на изделии и не учитывают сдвиг электрода в гильзе при поте "
        "и при долгой ходьбе.",
    )

    add_h(doc, "Прямое управление моментом")
    add_p(
        doc,
        "В прямом контуре величина электромиограммы входит в формулу момента, а класс «лестница» "
        "или «ровная поверхность» отдельно не вычисляется. Для подъёма по лестнице приставным "
        "шагом, когда ноги чередуются, момент колена силового протеза бедра собирают из импеданса, "
        "заданного состоянием опоры или переноса, и из члена, пропорционального поверхностной "
        "миограмме мышц остаточного бедра. Порог контакта стопы с опорой переключает равновесное "
        "положение импеданса. В опоре пользователь меняет отдаваемую мощность амплитудой миограммы. "
        "В переносе траекторию в основном держит номинальный импеданс, а вклад миограммы остаётся "
        "меньшим. Предварительная проверка на одном человеке с односторонней ампутацией бедра "
        "показала повторяемый чередующийся подъём [6].",
    )
    add_p(
        doc,
        "Прямой контур удобен там, где одно и то же сокращение должно сразу изменить момент, "
        "а набор режимов заранее не замкнут. Плата состоит в том, что закон не называет среду. "
        "Различие лестницы и ровной поверхности спрятано в состоянии опоры и в коэффициенте "
        "при миограмме. Если одного канала и порога контакта мало, чтобы отличить уклон, "
        "в формуле нет отдельного блока, который этот уклон назовёт. Для такого блока сигнал "
        "обрабатывают иначе: из окна миограммы получают класс, и уже класс выбирает готовый закон.",
    )

    add_h(doc, "Распознавание режима локомоции")
    add_p(
        doc,
        "Классификационный контур выдаёт имя деятельности. По электромиограмме, привязанной к фазе "
        "шага, отличают ровную ходьбу, лестницу, поворот и стояние [5]. Имя режима переключает "
        "заранее настроенный средний закон, а момент внутри шага по-прежнему может считаться "
        "по импедансу и по датчикам протеза. Ошибка здесь — неверная метка режима. На переходе "
        "между средами она опаснее, чем в установившемся шаге, потому что привод ещё работает "
        "по предыдущему закону, а человек уже поставил ногу на новую поверхность.",
    )
    add_p(
        doc,
        "Число независимых команд ограничено тем, сколько различимых активаций даёт культя. "
        "Направленная мышечная реиннервация увеличивает этот набор хирургически. В наблюдении "
        "одного человека после вычленения в коленном суставе ветви большеберцового и малоберцового "
        "нервов подшили к двигательным точкам оставшихся мышц задней группы бедра. Попытка тыльного "
        "и подошвенного сгибания утраченной стопы стала видна как сокращение этих мышц и как "
        "отдельная электромиограмма. Декодер распознавания образов принимал сигналы нативных "
        "и реиннервированных мышц вместе с датчиками протеза. Доля ошибок управления в реальном "
        "времени по всем режимам ходьбы составила 12,9 % по одним механическим датчикам, 2,2 % "
        "после добавления миограммы нативных мышц и 1,8 % после добавления миограммы "
        "реиннервированных мышц. Ошибки, способные привести к потере равновесия, встретились "
        "в 2 % проб при чисто механическом управлении и не встретились при управлении с реиннервацией. "
        "Тот же набор каналов позволил переставлять ногу сидя и проходить лестницы и пандусы [7]. "
        "Это одно клиническое наблюдение, а не групповое испытание. Оно показывает, какой канал "
        "можно получить, когда собственных мышц стопы на культе бедра уже нет.",
    )

    add_h(doc, "Совместный съём миограммы и механики")
    add_p(
        doc,
        "Механический канал и электромиограмма ошибаются в разных местах, поэтому их соединяют. "
        "В офлайновой оценке на восьми людях с ампутацией бедра, которые ходили на силовом протезе "
        "колена и голеностопа по ровной поверхности, пандусам и лестницам, миограмма сама по себе "
        "распознавала намерение хуже, чем набор механических датчиков: инерциальные модули, углы, "
        "скорости и силовые ячейки. Соединение миограммы с этим набором снизило ошибку и на "
        "переходах между режимами, и в установившемся шаге. Учёт предыстории датчиков сетью "
        "динамического байесовского вывода дополнительно снизил ошибку установившегося шага "
        "относительно линейного дискриминанта и не увеличил ошибку перехода. Вместе миограмма, "
        "механика и предыстория уменьшили среднюю ошибку перехода с 18,4 % до 12,2 % и среднюю "
        "ошибку установившегося шага с 3,8 % до 1,0 % [8].",
    )
    add_p(
        doc,
        "Отсюда следует практический порядок съёма, а не замена одного датчика другим. Опору, "
        "контакт стопы и фазу шага по-прежнему берут с протеза: эти величины прямо измеряют "
        "нагрузку и угол [2; 3]. Электромиограмму добавляют там, где по механике переход виден "
        "поздно или где пользователю нужна непрерывная добавка момента [6; 8]. Реиннервация "
        "имеет смысл, когда собственных независимых мышц культи мало для задуманного числа команд [7]. "
        "Обзор управления относит и механическое распознавание деятельности, и волевой биосигнал "
        "к разным входам одной иерархии, а не к двум несовместимым изделиям [1; 4].",
    )

    add_h(doc, "Сопоставление методов")
    add_p(
        doc,
        "Шесть разобранных способов отличаются точкой, в которой измерение превращается в команду. "
        "Импеданс по состоянию шага превращает угол и нагрузку в момент внутри уже выбранной фазы. "
        "Надзорный распознаватель по датчикам протеза превращает кадр тех же сигналов в имя "
        "деятельности из короткого списка. Прямое миоэлектрическое управление превращает амплитуду "
        "миограммы в добавку момента. Фазовый классификатор и схема с реиннервацией превращают "
        "набор миографических каналов в метку режима. Совместный съём оставляет механику основным "
        "источником и использует миограмму как добавочный признак. Сводка приведена в таблице 1.",
    )
    add_table(
        doc,
        "Таблица 1 – Способы получения сигнала управления протезом нижней конечности",
        ["Способ", "Что измеряют", "Какая команда получается", "Условие источника"],
        [
            [
                "Импеданс по состоянию шага",
                "Угол сустава, сила привода, нагрузка гильзы",
                "Момент внутри фазы; мощность при смене равновесия",
                "Ровная ходьба, лабораторный силовой протез бедра [2]",
            ],
            [
                "Надзор по датчикам протеза",
                "Кадры сигналов изделия, без сохранённой ноги",
                "Стояние, посадка или ходьба",
                "Один человек, 90 задуманных переходов найдены [3]",
            ],
            [
                "Прямой миоэлектрический момент",
                "Поверхностная миограмма мышц бедра и контакт стопы",
                "Добавка момента колена в опоре",
                "Один человек, чередующийся подъём по лестнице [6]",
            ],
            [
                "Фазовое распознавание по миограмме",
                "Электроды выше колена, окно внутри фазы шага",
                "Метка из семи режимов локомоции",
                "Восемь людей без ампутации и два с ампутацией бедра [5]",
            ],
            [
                "Миограмма после реиннервации",
                "Нативные и реиннервированные мышцы бедра плюс датчики протеза",
                "Режим ходьбы и перестановка ноги сидя",
                "Одно наблюдение после вычленения в колене [7]",
            ],
            [
                "Слияние миограммы и механики",
                "Остаточная миограмма, инерциальные датчики, угол и нагрузка",
                "Режим с учётом предыстории сигналов",
                "Восемь людей с ампутацией бедра, офлайн-оценка [8]",
            ],
        ],
    )
    add_p(
        doc,
        "Таблица задаёт выбор измерительной схемы под задачу модуля. Если модуль должен устойчиво "
        "пройти ровный шаг и отличить стояние от ходьбы, достаточно угла, нагрузки и кадров "
        "сигналов протеза [2; 3]. Если в опоре нужна волевая прибавка момента, к контакту стопы "
        "добавляют поверхностную миограмму остаточного бедра [6]. Если нужно заранее назвать "
        "лестницу или пандус, миограмму включают в классификатор вместе с механикой и с предысторией "
        "шага [5; 8]. Реиннервация расширяет набор мышц, с которых эту миограмму снимают, и в "
        "описанном наблюдении дальше снизила ошибку уже после того, как нативная миограмма была "
        "добавлена к механике [7].",
    )

    add_h(doc, "Заключение")
    add_p(
        doc,
        "Сигнал управления активным протезом нижней конечности получают двумя дополняющими "
        "путями. Датчики изделия — угол, сила привода, нагрузка гильзы — задают фазу шага, "
        "проверяют опору и отличают стояние, посадку и ходьбу. Поверхностная электромиограмма "
        "остаточных мышц задаёт волевую величину момента либо признак режима, который по одной "
        "механике виден позже. Прямое управление отображает амплитуду миограммы в момент колена "
        "при известном контакте стопы. Классификатор отображает окно миограммы в имя режима "
        "и переключает готовый закон. Соединение каналов на восьми пользователях силового протеза "
        "бедра снизило ошибку перехода между ровной поверхностью, пандусом и лестницей с 18,4 % "
        "до 12,2 % и ошибку установившегося шага с 3,8 % до 1,0 %. Направленная мышечная "
        "реиннервация добавляет каналы стопы на мышцы бедра, когда собственных мышц уже нет. "
        "Для мехатронного модуля отсюда следует состав измерительной схемы: механический контур "
        "опоры сохраняют, а биосигнал подключают как добавку момента или как признак смены режима.",
    )

    add_h(doc, "Список литературы")
    refs_ru = [
        "[1] Tucker M. R., Olivier J., Pagel A. и др. Control strategies for active lower extremity "
        "prosthetics and orthotics: a review // Journal of NeuroEngineering and Rehabilitation. "
        "2015. Vol. 12. P. 1–29.",
        "[2] Sup F., Bohara A., Goldfarb M. Design and control of a powered transfemoral prosthesis "
        "// The International Journal of Robotics Research. 2008. Vol. 27, № 2. P. 263–273.",
        "[3] Varol H. A., Sup F., Goldfarb M. Multiclass real-time intent recognition of a powered "
        "lower limb prosthesis // IEEE Transactions on Biomedical Engineering. 2010. Vol. 57, № 3. "
        "P. 542–551.",
        "[4] Fleming A., Stafford N., Huang S. и др. Myoelectric control of robotic lower limb "
        "prostheses: a review of electromyography interfaces, control paradigms, challenges and "
        "future directions // Journal of Neural Engineering. 2021. Vol. 18, № 4. Art. 041004.",
        "[5] Huang H., Kuiken T. A., Lipschutz R. D. A strategy for identifying locomotion modes "
        "using surface electromyography // IEEE Transactions on Biomedical Engineering. 2009. "
        "Vol. 56, № 1. P. 65–73.",
        "[6] Hoover C. D., Fulk G. D., Fite K. B. Stair ascent with a powered transfemoral prosthesis "
        "under direct myoelectric control // IEEE/ASME Transactions on Mechatronics. 2013. Vol. 18, "
        "№ 3. P. 1191–1200.",
        "[7] Hargrove L. J., Simon A. M., Young A. J. и др. Robotic leg control with EMG decoding "
        "in an amputee with nerve transfers // The New England Journal of Medicine. 2013. Vol. 369, "
        "№ 13. P. 1237–1242.",
        "[8] Young A. J., Kuiken T. A., Hargrove L. J. Analysis of using EMG and mechanical sensors "
        "to enhance intent recognition in powered lower limb prostheses // Journal of Neural "
        "Engineering. 2014. Vol. 11, № 5. Art. 056021.",
    ]
    for item in refs_ru:
        add_ref(doc, item)

    add_h(doc, "Bibliography")
    refs_en = [
        "[1] Tucker M. R., Olivier J., Pagel A., et al. Control strategies for active lower extremity "
        "prosthetics and orthotics: a review. Journal of NeuroEngineering and Rehabilitation, 2015, "
        "vol. 12, pp. 1–29.",
        "[2] Sup F., Bohara A., Goldfarb M. Design and control of a powered transfemoral prosthesis. "
        "The International Journal of Robotics Research, 2008, vol. 27, no. 2, pp. 263–273.",
        "[3] Varol H. A., Sup F., Goldfarb M. Multiclass real-time intent recognition of a powered "
        "lower limb prosthesis. IEEE Transactions on Biomedical Engineering, 2010, vol. 57, no. 3, "
        "pp. 542–551.",
        "[4] Fleming A., Stafford N., Huang S., et al. Myoelectric control of robotic lower limb "
        "prostheses: a review of electromyography interfaces, control paradigms, challenges and "
        "future directions. Journal of Neural Engineering, 2021, vol. 18, no. 4, art. 041004.",
        "[5] Huang H., Kuiken T. A., Lipschutz R. D. A strategy for identifying locomotion modes "
        "using surface electromyography. IEEE Transactions on Biomedical Engineering, 2009, vol. 56, "
        "no. 1, pp. 65–73.",
        "[6] Hoover C. D., Fulk G. D., Fite K. B. Stair ascent with a powered transfemoral prosthesis "
        "under direct myoelectric control. IEEE/ASME Transactions on Mechatronics, 2013, vol. 18, "
        "no. 3, pp. 1191–1200.",
        "[7] Hargrove L. J., Simon A. M., Young A. J., et al. Robotic leg control with EMG decoding "
        "in an amputee with nerve transfers. The New England Journal of Medicine, 2013, vol. 369, "
        "no. 13, pp. 1237–1242.",
        "[8] Young A. J., Kuiken T. A., Hargrove L. J. Analysis of using EMG and mechanical sensors "
        "to enhance intent recognition in powered lower limb prostheses. Journal of Neural "
        "Engineering, 2014, vol. 11, no. 5, art. 056021.",
    ]
    for item in refs_en:
        add_ref(doc, item)

    doc.save(DOCX)
    return DOCX


if __name__ == "__main__":
    print(build())
