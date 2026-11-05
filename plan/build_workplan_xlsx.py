"""Собрать план статьи (Максимкин / Ионин) в книгу Excel.

Листы:
  Tasks        — задачи, даты, критерии, живая проверка зависимостей
  Gantt        — недели от старта плана, формула пересечения с датами Tasks
  Зависимости  — рёбра «задача → предшественница»
  Баланс       — роли и доля календарных дней
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).with_name("emg_kometa_workplan.xlsx")

PROJECT_START = date(2026, 10, 20)

ALEX = "Александр Максимкин"
DANIIL = "Даниил Ионин"

# id, short, full, person, start, end, deps, acceptance, block
TASKS = [
    ("T01", "Научная база",
     "Систематизация научной базы: 25–30 источников по ЭМГ-управлению протезами",
     ALEX, date(2026, 10, 20), date(2026, 10, 27), [],
     "Таблица источников (тема/метод/метрики/вывод)", "Наука"),
    ("T02", "Метрики естественности",
     "Обзор методов оценки «естественности ходьбы» и метрик",
     ALEX, date(2026, 10, 20), date(2026, 10, 26), [],
     "Список метрик с формулами и ссылками", "Наука"),
    ("T03", "Инвентаризация датчиков",
     "Инвентаризация датчиков и проверка «вживую» (30 с записи каждого)",
     DANIIL, date(2026, 10, 20), date(2026, 10, 24), [],
     "Таблица датчиков + файлы записей", "Эксп."),
    ("T04", "Требования к сенсорике",
     "Требования к сенсорике под «Комету» (крепление, питание, частоты)",
     DANIIL, date(2026, 10, 25), date(2026, 10, 27), ["T03"],
     "1 стр. требований", "Эксп."),
    ("T05", "Обоснование архитектуры",
     "Обоснование выбора архитектуры управления (baseline: порог vs LDA)",
     ALEX, date(2026, 10, 28), date(2026, 11, 3), ["T01", "T02"],
     "1–2 абз. + схема + ссылки", "Наука"),
    ("T06", "План испытаний «Кометы»",
     "План будущих испытаний на «Комете» (3 сценария)",
     DANIIL, date(2026, 10, 31), date(2026, 11, 4), ["T04"],
     "План 1–2 стр.", "Эксп."),
    ("T07", "Протокол эксперимента",
     "Протокол эксперимента: испытуемые, условия, синхронизация",
     ALEX, date(2026, 11, 4), date(2026, 11, 10), ["T02", "T05"],
     "Протокол с обоснованием", "Наука"),
    ("T08", "Предобработка ЭМГ",
     "Реализация предобработки ЭМГ (фильтр, огибающая, окно, признаки)",
     DANIIL, date(2026, 11, 5), date(2026, 11, 12), ["T05"],
     "Скрипт + unit-тест", "Эксп."),
    ("T09", "Baseline-классификатор",
     "Реализация baseline-классификатора фаз походки",
     DANIIL, date(2026, 11, 13), date(2026, 11, 19), ["T08"],
     "Точность ≥ порога + confusion matrix", "Эксп."),
    ("T10", "Related Work",
     "Написание Related Work (1.5–2 стр., IEEE)",
     ALEX, date(2026, 11, 11), date(2026, 11, 18), ["T01"],
     "Раздел готов, ссылки IEEE", "Наука"),
    ("T11", "Сбор датасета",
     "Сбор датасета: 3 испытуемых × 3 условия, ЭМГ+IMU",
     DANIIL, date(2026, 11, 20), date(2026, 11, 27), ["T07", "T08"],
     "Датасет + метаданные", "Эксп."),
    ("T12", "Графики и метрики",
     "Прогон алгоритма, графики (огибающие, фазы vs разметка, задержка)",
     DANIIL, date(2026, 11, 28), date(2026, 12, 4), ["T09", "T11"],
     "Графики + таблица метрик", "Эксп."),
    ("T13", "Готовность «Кометы»",
     "Оценка готовности «Кометы» к биоэлектрическому управлению",
     DANIIL, date(2026, 11, 28), date(2026, 12, 4), ["T06"],
     "Отчёт + перечень доработок", "Эксп."),
    ("T14", "Method",
     "Написание Method (методология, метрики, обоснование)",
     ALEX, date(2026, 11, 19), date(2026, 11, 30), ["T05", "T07"],
     "Раздел воспроизводим", "Наука"),
    ("T15", "Experimental Setup",
     "Написание Experimental Setup",
     DANIIL, date(2026, 12, 5), date(2026, 12, 9), ["T11"],
     "Раздел готов", "Эксп."),
    ("T16", "Results",
     "Оформление Results: графики, таблицы, подписи IEEE",
     DANIIL, date(2026, 12, 10), date(2026, 12, 15), ["T12"],
     "Все рисунки 300 dpi/вектор", "Эксп."),
    ("T17", "Introduction",
     "Написание Introduction",
     ALEX, date(2026, 12, 1), date(2026, 12, 8), ["T10"],
     "1–1.5 стр., без «воды»", "Наука"),
    ("T18", "«Комета»: будущее",
     "Раздел «Будущее применение на „Комете“»",
     DANIIL, date(2026, 12, 16), date(2026, 12, 18), ["T13"],
     "Раздел готов", "Эксп."),
]

PROJECT_END = max(item[5] for item in TASKS)
N_WEEKS = (PROJECT_END - PROJECT_START).days // 7 + 1
DEP_LAST = 2 + sum(len(item[6]) for item in TASKS)

NAVY = "1B3A4B"
BLUE = "1F6AA5"
BLUE_SOFT = "E7F1F8"
GREEN = "1E7A46"
GREEN_SOFT = "E7F6EE"
RED = "FDEDEC"
RED_FONT = "A93226"
OK_FONT = "196F3D"
GOLD = "F8F1DE"
GRID = "E6EAED"
WHITE = "FFFFFF"
INK = "1C2833"
MUTED = "5D6D7E"
LINE = "D5DDE3"

thin = Border(
    left=Side(style="thin", color=LINE),
    right=Side(style="thin", color=LINE),
    top=Side(style="thin", color=LINE),
    bottom=Side(style="thin", color=LINE),
)
hair = Border(
    left=Side(style="hair", color="EEF2F4"),
    right=Side(style="hair", color="EEF2F4"),
    top=Side(style="hair", color="EEF2F4"),
    bottom=Side(style="hair", color="EEF2F4"),
)

fill_navy = PatternFill("solid", fgColor=NAVY)
fill_blue = PatternFill("solid", fgColor=BLUE)
fill_green = PatternFill("solid", fgColor=GREEN)
fill_blue_soft = PatternFill("solid", fgColor=BLUE_SOFT)
fill_green_soft = PatternFill("solid", fgColor=GREEN_SOFT)
fill_gold = PatternFill("solid", fgColor=GOLD)
fill_white = PatternFill("solid", fgColor=WHITE)
fill_grid = PatternFill("solid", fgColor="F7F9FA")
fill_red = PatternFill("solid", fgColor=RED)
fill_input = PatternFill("solid", fgColor="FFF8E1")

font_title = Font(name="Calibri", size=16, bold=True, color=NAVY)
font_header = Font(name="Calibri", size=10, bold=True, color=WHITE)
font_body = Font(name="Calibri", size=10, color=INK)
font_small = Font(name="Calibri", size=9, color=MUTED)
font_bold = Font(name="Calibri", size=10, bold=True, color=INK)
font_white = Font(name="Calibri", size=10, bold=True, color=WHITE)
font_link = Font(name="Calibri", size=10, color=INK)

center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

# Tasks sheet geometry
HEADER_ROW = 3
FIRST = 4
LAST = FIRST + len(TASKS) - 1  # 25

# Gantt geometry
G_WEEK_START_ROW = 4
G_WEEK_END_ROW = 5
G_HEADER_ROW = 6
G_FIRST = 7
G_LAST = G_FIRST + len(TASKS) - 1  # 28
G_FIRST_WEEK_COL = 4  # D


def weeks():
    for i in range(N_WEEKS):
        start = PROJECT_START + timedelta(days=7 * i)
        end = start + timedelta(days=6)
        yield i + 1, start, end


def apply_header_row(ws, row, start_col, end_col):
    for col in range(start_col, end_col + 1):
        cell = ws.cell(row, col)
        cell.fill = fill_navy
        cell.font = font_header
        cell.alignment = center
        cell.border = thin


def build():
    wb = Workbook()
    wb.calculation.calcMode = "auto"
    wb.calculation.fullCalcOnLoad = True
    wb.properties.title = "План статьи: ЭМГ-управление и «Комета»"
    wb.properties.subject = "Максимкин — научный контур; Ионин — экспериментальный контур"
    wb.properties.creator = "plan/build_workplan_xlsx.py"

    ws_tasks = wb.active
    ws_tasks.title = "Tasks"
    ws_deps = wb.create_sheet("Зависимости")
    ws_gantt = wb.create_sheet("Gantt", 1)
    ws_bal = wb.create_sheet("Баланс")

    write_tasks(ws_tasks)
    write_deps(ws_deps)
    write_gantt(ws_gantt)
    write_balance(ws_bal)

    ws_tasks.sheet_properties.tabColor = BLUE
    ws_gantt.sheet_properties.tabColor = GREEN
    ws_deps.sheet_properties.tabColor = "B9770E"
    ws_bal.sheet_properties.tabColor = NAVY

    wb.active = ws_gantt
    wb.save(OUT)
    return OUT


def write_tasks(ws):
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 110
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.horizontalCentered = True
    ws.oddHeader.left.text = "План статьи · ЭМГ / «Комета»"
    ws.oddFooter.right.text = "Стр. &P из &N"
    ws.print_title_rows = "1:3"
    ws.page_setup.horizontalDpi = 300
    ws.page_setup.verticalDpi = 300
    ws.freeze_panes = "A4"

    ws.merge_cells("A1:J1")
    ws["A1"] = "Задачи статьи: научный контур и эксперимент на «Комете»"
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")

    ws.merge_cells("A2:J2")
    ws["A2"] = (
        "Длительность считается формулой (конец − начало + 1) и включает выходные. "
        "Столбец «Проверка» сравнивает старт с окончанием каждой предшественницы: "
        "конфликт, если задача начинается в день окончания предшественницы или раньше. "
        "Диаграмма на листе Gantt пересчитывается из этих дат."
    )
    ws["A2"].font = font_small
    ws["A2"].alignment = left_align
    ws.row_dimensions[1].height = 26
    ws.row_dimensions[2].height = 36

    headers = [
        "ID", "Задача", "Исполнитель", "Начало", "Конец",
        "Длит. (дн)", "Зависит от", "Критерий приёмки", "Блок", "Проверка",
    ]
    for col, name in enumerate(headers, 1):
        ws.cell(HEADER_ROW, col, name)
    apply_header_row(ws, HEADER_ROW, 1, len(headers))
    ws.row_dimensions[HEADER_ROW].height = 22

    for i, (tid, _short, full, person, start, end, deps, accept, block) in enumerate(TASKS):
        row = FIRST + i
        ws.cell(row, 1, tid).alignment = center
        ws.cell(row, 2, full).alignment = left_align
        ws.cell(row, 3, person).alignment = left_align
        c_start = ws.cell(row, 4, start)
        c_end = ws.cell(row, 5, end)
        c_start.number_format = "YYYY-MM-DD"
        c_end.number_format = "YYYY-MM-DD"
        c_start.alignment = center
        c_end.alignment = center
        dur = ws.cell(row, 6, f"=E{row}-D{row}+1")
        dur.alignment = center
        dur.font = font_bold
        dep_text = ", ".join(deps) if deps else "—"
        ws.cell(row, 7, dep_text).alignment = center
        ws.cell(row, 8, accept).alignment = left_align
        ws.cell(row, 9, block).alignment = center
        check = ws.cell(
            row, 10,
            f'=IF(COUNTIF(Зависимости!A:A,A{row})=0,"—",'
            f'IF(COUNTIFS(Зависимости!A:A,A{row},Зависимости!E:E,"Конфликт")>0,"Конфликт","ОК"))',
        )
        check.alignment = center
        for col in range(1, 11):
            cell = ws.cell(row, col)
            cell.font = font_bold if col in (1, 6, 10) else font_body
            cell.border = thin
            cell.fill = fill_white
        ws.row_dimensions[row].height = 32

    # Restore bold on duration and id after the loop overwrote fonts.
    for row in range(FIRST, LAST + 1):
        ws.cell(row, 1).font = font_bold
        ws.cell(row, 6).font = font_bold
        ws.cell(row, 10).font = font_bold

    soft_alex = FormulaRule(formula=[f'$C{FIRST}="{ALEX}"'], fill=fill_blue_soft)
    soft_dan = FormulaRule(formula=[f'$C{FIRST}="{DANIIL}"'], fill=fill_green_soft)
    ws.conditional_formatting.add(f"A{FIRST}:I{LAST}", soft_alex)
    ws.conditional_formatting.add(f"A{FIRST}:I{LAST}", soft_dan)

    conflict_fill = PatternFill("solid", fgColor="F5B7B1")
    ok_fill = PatternFill("solid", fgColor="ABEBC6")
    ws.conditional_formatting.add(
        f"J{FIRST}:J{LAST}",
        FormulaRule(
            formula=[f'J{FIRST}="Конфликт"'],
            fill=conflict_fill,
            font=Font(name="Calibri", size=10, bold=True, color="7B241C"),
        ),
    )
    ws.conditional_formatting.add(
        f"J{FIRST}:J{LAST}",
        FormulaRule(
            formula=[f'J{FIRST}="ОК"'],
            fill=ok_fill,
            font=Font(name="Calibri", size=10, bold=True, color=OK_FONT),
        ),
    )

    dv_person = DataValidation(type="list", formula1=f'"{ALEX},{DANIIL}"', allow_blank=False)
    dv_person.error = "Выберите исполнителя из списка"
    dv_person.errorTitle = "Исполнитель"
    dv_person.add(f"C{FIRST}:C{LAST}")
    ws.add_data_validation(dv_person)

    dv_block = DataValidation(type="list", formula1='"Наука,Эксп."', allow_blank=False)
    dv_block.add(f"I{FIRST}:I{LAST}")
    ws.add_data_validation(dv_block)

    widths = {
        "A": 8, "B": 62, "C": 26, "D": 14, "E": 14,
        "F": 13, "G": 18, "H": 48, "I": 12, "J": 14,
    }
    for col, width in widths.items():
        ws.column_dimensions[col].width = width

    ws.auto_filter.ref = f"A{HEADER_ROW}:J{LAST}"
    ws.oddHeader.center.text = ""
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = 0.4
    ws.page_margins.right = 0.4
    ws.page_margins.top = 0.6
    ws.page_margins.bottom = 0.5
    ws.sheet_view.zoomScale = 110


def write_deps(ws):
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 120
    ws.freeze_panes = "A3"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    ws.merge_cells("A1:F1")
    ws["A1"] = "Зависимости: старт задачи должен быть строго позже окончания предшественницы"
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 26

    headers = [
        "Задача", "Предшественница", "Окончание предшественницы",
        "Старт задачи", "Статус", "Пояснение",
    ]
    for col, name in enumerate(headers, 1):
        ws.cell(2, col, name)
    apply_header_row(ws, 2, 1, len(headers))
    ws.row_dimensions[2].height = 30

    edges = []
    for tid, _short, _full, _person, _start, _end, deps, _accept, _block in TASKS:
        for pred in deps:
            edges.append((tid, pred))

    for i, (tid, pred) in enumerate(edges):
        row = 3 + i
        ws.cell(row, 1, tid).alignment = center
        ws.cell(row, 2, pred).alignment = center
        end_c = ws.cell(row, 3, f'=VLOOKUP(B{row},Tasks!$A$4:$E${LAST},5,FALSE)')
        start_c = ws.cell(row, 4, f'=VLOOKUP(A{row},Tasks!$A$4:$E${LAST},4,FALSE)')
        end_c.number_format = "YYYY-MM-DD"
        start_c.number_format = "YYYY-MM-DD"
        end_c.alignment = center
        start_c.alignment = center
        ws.cell(row, 5, f'=IF(D{row}<=C{row},"Конфликт","ОК")').alignment = center
        ws.cell(
            row, 6,
            f'=IF(E{row}="Конфликт",A{row}&" начинается не позже окончания "&B{row},"")',
        ).alignment = left_align
        # Номер строки только для конфликтов; #N/A прячет обычные связи от AGGREGATE.
        ws.cell(row, 7, f'=IF(E{row}="Конфликт",ROW(),NA())')
        for col in range(1, 7):
            ws.cell(row, col).font = font_body
            ws.cell(row, col).border = thin
            ws.cell(row, col).fill = fill_white
        ws.cell(row, 5).font = font_bold
        ws.row_dimensions[row].height = 20

    last_edge = 2 + len(edges)
    ws.conditional_formatting.add(
        f"A3:F{last_edge}",
        FormulaRule(formula=['$E3="Конфликт"'], fill=PatternFill("solid", fgColor="F5B7B1")),
    )
    ws.conditional_formatting.add(
        f"E3:E{last_edge}",
        FormulaRule(
            formula=['E3="ОК"'],
            fill=PatternFill("solid", fgColor="ABEBC6"),
            font=Font(name="Calibri", size=10, bold=True, color=OK_FONT),
        ),
    )
    ws.auto_filter.ref = f"A2:F{last_edge}"

    widths = {"A": 14, "B": 20, "C": 30, "D": 16, "E": 14, "F": 62, "G": 12}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    ws.column_dimensions["G"].hidden = True

    ws.oddHeader.left.text = "Зависимости плана"
    ws.page_margins.left = 0.5
    ws.page_margins.right = 0.5


def write_gantt(ws):
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 110
    ws.freeze_panes = "D7"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.page_setup.paperSize = ws.PAPERSIZE_A3
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:6"
    ws.print_title_cols = "A:C"
    ws.page_setup.horizontalCentered = True
    ws.page_margins.left = 0.35
    ws.page_margins.right = 0.35
    ws.page_margins.top = 0.55
    ws.page_margins.bottom = 0.45
    ws.oddHeader.left.text = (
        f"Диаграмма Ганта · {PROJECT_START.strftime('%d.%m.%Y')} – {PROJECT_END.strftime('%d.%m.%Y')}"
    )
    ws.oddFooter.right.text = "Стр. &P из &N"

    last_week_col = G_FIRST_WEEK_COL + N_WEEKS - 1  # 14 = N
    last_letter = get_column_letter(last_week_col)

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=last_week_col)
    ws["A1"] = (
        f"Диаграмма Ганта · статья по ЭМГ-управлению, {N_WEEKS} недель от "
        f"{PROJECT_START.strftime('%d.%m.%Y')}"
    )
    ws["A1"].font = font_title
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 26

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=last_week_col)
    ws["A2"] = (
        "Квадрат стоит в неделе, если интервал задачи хотя бы одним днём пересекает эту неделю. "
        "Неделя — 7 календарных дней от 20.10.2026. Цвет берётся из исполнителя на листе Tasks. "
        "Строки 4–5 (границы недель) скрыты: их читают формулы."
    )
    ws["A2"].font = font_small
    ws["A2"].alignment = left_align
    ws.row_dimensions[2].height = 32

    ws.merge_cells("A3:B3")
    ws["A3"] = "Александр Максимкин — научный контур"
    ws["A3"].font = Font(name="Calibri", size=10, bold=True, color=WHITE)
    ws["A3"].fill = fill_blue
    ws["A3"].alignment = center
    ws["B3"].fill = fill_blue
    ws["C3"] = "Даниил Ионин — эксперимент"
    ws["C3"].font = Font(name="Calibri", size=10, bold=True, color=WHITE)
    ws["C3"].fill = fill_green
    ws["C3"].alignment = center
    ws.row_dimensions[3].height = 22

    week_list = list(weeks())
    ws.cell(G_WEEK_START_ROW, 3, "Начало недели")
    ws.cell(G_WEEK_END_ROW, 3, "Конец недели")
    for idx, (_n, start, end) in enumerate(week_list):
        col = G_FIRST_WEEK_COL + idx
        c1 = ws.cell(G_WEEK_START_ROW, col, start)
        c2 = ws.cell(G_WEEK_END_ROW, col, end)
        c1.number_format = "YYYY-MM-DD"
        c2.number_format = "YYYY-MM-DD"
        c1.font = font_small
        c2.font = font_small
        c1.alignment = center
        c2.alignment = center

    ws.row_dimensions[G_WEEK_START_ROW].hidden = True
    ws.row_dimensions[G_WEEK_END_ROW].hidden = True

    headers_left = ["ID", "Задача", "Исполнитель"]
    for col, name in enumerate(headers_left, 1):
        ws.cell(G_HEADER_ROW, col, name)
    for idx, (n, start, end) in enumerate(week_list):
        col = G_FIRST_WEEK_COL + idx
        label = f"W{n}\n{start.strftime('%d.%m')}–{end.strftime('%d.%m')}"
        ws.cell(G_HEADER_ROW, col, label)
    apply_header_row(ws, G_HEADER_ROW, 1, last_week_col)
    ws.row_dimensions[G_HEADER_ROW].height = 32

    for i in range(len(TASKS)):
        row = G_FIRST + i
        src = FIRST + i
        ws.cell(row, 1, f"=Tasks!A{src}").alignment = center
        ws.cell(row, 2, f"=Tasks!B{src}").alignment = left_align
        ws.cell(row, 3, f"=Tasks!C{src}").alignment = left_align
        for col in range(1, 4):
            ws.cell(row, col).font = font_body
            ws.cell(row, col).border = thin
        ws.cell(row, 1).font = font_bold
        for w in range(N_WEEKS):
            col = G_FIRST_WEEK_COL + w
            letter = get_column_letter(col)
            formula = (
                f'=IF(OR(Tasks!$D{src}="",Tasks!$E{src}=""),"",'
                f'IF(AND(Tasks!$D{src}<={letter}${G_WEEK_END_ROW},'
                f'Tasks!$E{src}>={letter}${G_WEEK_START_ROW}),"■",""))'
            )
            cell = ws.cell(row, col, formula)
            cell.alignment = center
            cell.font = font_white
            cell.border = hair
            cell.fill = fill_grid
        ws.row_dimensions[row].height = 30

    # Label tint follows the executor; bar color follows the square.
    ws.conditional_formatting.add(
        f"A{G_FIRST}:C{G_LAST}",
        FormulaRule(formula=[f'$C{G_FIRST}="{ALEX}"'], fill=fill_blue_soft),
    )
    ws.conditional_formatting.add(
        f"A{G_FIRST}:C{G_LAST}",
        FormulaRule(formula=[f'$C{G_FIRST}="{DANIIL}"'], fill=fill_green_soft),
    )
    ws.conditional_formatting.add(
        f"D{G_FIRST}:{last_letter}{G_LAST}",
        FormulaRule(
            formula=[f'AND(D{G_FIRST}="■",$C{G_FIRST}="{ALEX}")'],
            fill=fill_blue,
            font=font_white,
        ),
    )
    ws.conditional_formatting.add(
        f"D{G_FIRST}:{last_letter}{G_LAST}",
        FormulaRule(
            formula=[f'AND(D{G_FIRST}="■",$C{G_FIRST}="{DANIIL}")'],
            fill=fill_green,
            font=font_white,
        ),
    )

    load_row_a = G_LAST + 2
    load_row_d = G_LAST + 3
    ws.cell(load_row_a, 3, "Задач Александра в неделе").font = font_bold
    ws.cell(load_row_d, 3, "Задач Даниила в неделе").font = font_bold
    ws.cell(load_row_a, 3).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(load_row_d, 3).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(load_row_a, 3).fill = fill_blue_soft
    ws.cell(load_row_d, 3).fill = fill_green_soft
    for w in range(N_WEEKS):
        col = G_FIRST_WEEK_COL + w
        letter = get_column_letter(col)
        ca = ws.cell(
            load_row_a, col,
            f'=COUNTIFS($C${G_FIRST}:$C${G_LAST},"{ALEX}",{letter}${G_FIRST}:{letter}${G_LAST},"■")',
        )
        cd = ws.cell(
            load_row_d, col,
            f'=COUNTIFS($C${G_FIRST}:$C${G_LAST},"{DANIIL}",{letter}${G_FIRST}:{letter}${G_LAST},"■")',
        )
        for cell, fill in ((ca, fill_blue_soft), (cd, fill_green_soft)):
            cell.font = font_bold
            cell.alignment = center
            cell.fill = fill
            cell.border = thin
    ws.row_dimensions[load_row_a].height = 20
    ws.row_dimensions[load_row_d].height = 20

    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 54
    ws.column_dimensions["C"].width = 26
    for w in range(N_WEEKS):
        ws.column_dimensions[get_column_letter(G_FIRST_WEEK_COL + w)].width = 12

    ws.auto_filter.ref = f"A{G_HEADER_ROW}:{last_letter}{G_LAST}"
    ws.sheet_view.zoomScale = 110
    ws.oddHeader.center.text = ""


def write_balance(ws):
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 120
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins.left = 0.6
    ws.page_margins.right = 0.5
    ws.page_margins.top = 0.6
    ws.page_margins.bottom = 0.5
    ws.merge_cells("A1:G1")
    ws["A1"] = "Роли и баланс нагрузки"
    ws["A1"].font = font_title
    ws.row_dimensions[1].height = 26

    ws.merge_cells("A2:C2")
    ws["A2"] = ALEX
    ws["A2"].font = font_white
    ws["A2"].fill = fill_blue
    ws["A2"].alignment = center

    ws.merge_cells("E2:G2")
    ws["E2"] = DANIIL
    ws["E2"].font = font_white
    ws["E2"].fill = fill_green
    ws["E2"].alignment = center
    ws.row_dimensions[2].height = 22

    alex_lines = [
        "Исследования и текст научного контура.",
        "База, метрики естественности ходьбы, обоснование порога и LDA.",
        "Протокол эксперимента: испытуемые, условия, синхронизация.",
        "Текст: Introduction, Related Work, Method.",
    ]
    dan_lines = [
        "Эксперименты и текст экспериментального контура.",
        "Датчики, требования к сенсорике, план испытаний «Кометы».",
        "Предобработка, классификатор, датасет, графики, готовность «Кометы».",
        "Текст: Experimental Setup, Results, будущее применение на «Комете».",
    ]
    for i, (a, d) in enumerate(zip(alex_lines, dan_lines), start=3):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=3)
        ws.merge_cells(start_row=i, start_column=5, end_row=i, end_column=7)
        ws.cell(i, 1, a).alignment = left_align
        ws.cell(i, 5, d).alignment = left_align
        ws.cell(i, 1).font = font_body
        ws.cell(i, 5).font = font_body
        ws.cell(i, 1).fill = fill_blue_soft
        ws.cell(i, 5).fill = fill_green_soft
        ws.row_dimensions[i].height = 28

    # Workload table driven by Tasks.
    ws["A9"] = "Нагрузка по календарным дням"
    ws["A9"].font = Font(name="Calibri", size=13, bold=True, color=NAVY)
    ws.merge_cells("A9:D9")

    for col, name in enumerate(["Исполнитель", "Задач", "Календарных дней", "Доля"], 1):
        ws.cell(10, col, name)
    apply_header_row(ws, 10, 1, 4)

    ws["A11"] = ALEX
    ws["A12"] = DANIIL
    ws["A13"] = "Всего"
    for row, person in ((11, ALEX), (12, DANIIL)):
        ws.cell(row, 2, f'=COUNTIF(Tasks!$C$4:$C${LAST},A{row})')
        ws.cell(row, 3, f'=SUMIF(Tasks!$C$4:$C${LAST},A{row},Tasks!$F$4:$F${LAST})')
        ws.cell(row, 4, f'=IF(SUM($C$11:$C$12)=0,"—",C{row}/SUM($C$11:$C$12))')
        ws.cell(row, 4).number_format = "0.0%"
    ws["B13"] = "=B11+B12"
    ws["C13"] = "=C11+C12"
    ws["D13"] = "=D11+D12"
    ws["D13"].number_format = "0.0%"
    for row, fill in ((11, fill_blue_soft), (12, fill_green_soft), (13, fill_gold)):
        for col in range(1, 5):
            cell = ws.cell(row, col)
            cell.font = font_bold if col > 1 or row == 13 else font_body
            cell.fill = fill
            cell.border = thin
            cell.alignment = center if col > 1 else left_align
        ws.row_dimensions[row].height = 22
    ws["A13"].font = font_bold

    ws.merge_cells("A15:D15")
    ws["A15"] = (
        "Доля считается по календарным дням, включая выходные. "
        "Параллельные задачи одного человека в одной неделе видны внизу листа Gantt."
    )
    ws["A15"].font = font_small
    ws["A15"].alignment = left_align
    ws.row_dimensions[15].height = 32

    ws["A17"] = "Зависимости"
    ws["A17"].font = Font(name="Calibri", size=13, bold=True, color=NAVY)
    ws.merge_cells("A17:D17")
    ws.merge_cells("A18:D18")
    ws["A18"] = (
        "Правило: дата начала строго позже даты окончания каждой предшественницы. "
        "Список рёбер — на листе «Зависимости»."
    )
    ws["A18"].font = font_small
    ws["A18"].alignment = left_align
    ws.row_dimensions[18].height = 28

    ws["A19"] = "Конфликтов"
    ws["B19"] = f'=COUNTIF(Tasks!J{FIRST}:J{LAST},"Конфликт")'
    ws["A19"].font = font_bold
    ws["B19"].font = Font(name="Calibri", size=14, bold=True, color=RED_FONT)
    ws["B19"].alignment = center
    ws["B19"].fill = fill_red
    ws["B19"].border = thin
    ws["A19"].border = thin
    ws["A19"].fill = fill_red
    ws["A19"].alignment = left_align
    ws["A25"] = "Какие связи конфликтуют"
    ws["A25"].font = Font(name="Calibri", size=11, bold=True, color=NAVY)
    # SMALL/AGGREGATE, без TEXTJOIN: работает и в Excel без динамических массивов.
    for offset, row in enumerate((26, 27), start=1):
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
        ws.cell(
            row, 1,
            f'=IFERROR(INDEX(Зависимости!F:F,_xlfn.AGGREGATE(15,6,Зависимости!$G$3:$G${DEP_LAST},{offset})),"")',
        )
        ws.cell(row, 1).font = font_body
        ws.cell(row, 1).alignment = left_align
        ws.cell(row, 1).fill = fill_red
        ws.row_dimensions[row].height = 22

    ws["A21"] = "Дедлайн конференции"
    ws["A21"].font = Font(name="Calibri", size=13, bold=True, color=NAVY)
    ws.merge_cells("A21:D21")

    ws["A22"] = "Дата дедлайна (введите)"
    ws["B22"] = None
    ws["B22"].fill = fill_input
    ws["B22"].number_format = "YYYY-MM-DD"
    ws["B22"].border = thin
    ws["B22"].alignment = center
    ws["A22"].font = font_body
    ws["A22"].alignment = left_align
    ws["A22"].border = thin
    ws.merge_cells("C22:D22")
    ws["C22"] = "Жёлтая ячейка — поле ввода"
    ws["C22"].font = font_small
    ws["C22"].alignment = left_align

    ws["A23"] = "Окончание плана"
    ws["B23"] = f"=MAX(Tasks!E{FIRST}:E{LAST})"
    ws["B23"].number_format = "YYYY-MM-DD"
    ws["A24"] = "Запас, календарных дней"
    ws["B24"] = '=IF(B22="","—",B22-B23)'
    for row in (23, 24):
        ws.cell(row, 1).font = font_body
        ws.cell(row, 1).alignment = left_align
        ws.cell(row, 1).border = thin
        ws.cell(row, 2).font = font_bold
        ws.cell(row, 2).alignment = center
        ws.cell(row, 2).border = thin
        ws.cell(row, 2).fill = fill_white
    ws.row_dimensions[22].height = 22
    ws.row_dimensions[23].height = 22
    ws.row_dimensions[24].height = 22

    # Chart data is the workload table itself (rows 11–12, days in column C).
    chart = BarChart()
    chart.type = "col"
    chart.grouping = "clustered"
    chart.title = "Календарные дни"
    chart.y_axis.title = None
    chart.x_axis.title = None
    data = Reference(ws, min_col=3, min_row=10, max_row=12)
    cats = Reference(ws, min_col=1, min_row=11, max_row=12)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.shape = 4
    chart.style = 10
    chart.y_axis.majorGridlines = None
    chart.overlap = 0
    chart.gapWidth = 80
    chart.width = 12
    chart.height = 6
    # Series graphical properties differ across openpyxl versions; default style is enough.
    ws.add_chart(chart, "E10")

    widths = {"A": 42, "B": 22, "C": 24, "D": 14, "E": 28, "F": 22, "G": 28}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width

    ws.oddHeader.left.text = "Баланс нагрузки"
    ws.sheet_view.zoomScale = 120


if __name__ == "__main__":
    path = build()
    print(path)
