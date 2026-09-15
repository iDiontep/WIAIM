# WIAIM — Wireless Interface Applification in Mechatronics

## Тема научной работы (магистерская диссертация)

**Сравнительный анализ беспроводных технологий связи для управления одиночным роботом и роем роботов в системах мехатроники**

## Статус проекта

| Этап | Статус | Файл |
|------|--------|------|
| Ключевые слова и критерии | ✅ | [literature/keywords.md](literature/keywords.md) |
| Источники США (18) | ✅ | [literature/sources_usa.md](literature/sources_usa.md) |
| Источники Китай (14) | ✅ | [literature/sources_china.md](literature/sources_china.md) |
| Источники RU/EU | ✅ | [literature/sources_ru_eu.md](literature/sources_ru_eu.md) |
| Патентный поиск (40) | ✅ | [patents/patents_matrix.md](patents/patents_matrix.md) |
| Анализ патентов | ✅ | [patents/analysis.md](patents/analysis.md) |
| Сравнительная таблица | ✅ | [literature/comparison_table.md](literature/comparison_table.md) |
| Актуальность (черновик) | ✅ | [chapters/01_relevance.md](chapters/01_relevance.md) |
| BibTeX библиография (42) | ✅ | [literature/bibliography.bib](literature/bibliography.bib) |

## Структура репозитория

```
WIAIM/
├── WIAIM.md
├── README.md
├── literature/
│   ├── keywords.md
│   ├── sources_usa.md
│   ├── sources_china.md
│   ├── sources_ru_eu.md
│   ├── comparison_table.md
│   └── bibliography.bib
├── patents/
│   ├── search_queries.md
│   ├── patents_matrix.md
│   └── analysis.md
└── chapters/
    └── 01_relevance.md
```

## Ключевые результаты

### Актуальность
- 4,28 млн промышленных роботов в мире (IFR 2024)
- Рост патентной активности 2018–2025 (ABB, DJI, Siemens, Georgia Tech)
- Научный пробел: нет систематического сравнения протоколов для mechatronics

### Сравнение технологий (кратко)
| Протокол | Лучше для |
|----------|-----------|
| 5G URLLC | Real-time industrial control |
| Wi-Fi 6 + TSN | Mobile manipulators, high bandwidth |
| LoRa | Long range, telemetry, hostile env |
| BLE/ZigBee mesh | Indoor swarm, low energy |
| ESP-NOW | Educational/research swarms |

### Патенты
- **20 US** + **18 CN** + 2 PCT
- Топ assignees: ABB, DJI, Siemens, Georgia Tech, Midea

## Следующие шаги (рекомендации)

1. Углублённое чтение топ-5 источников из sources_usa.md
2. Доступ к CNKI через вуз для полных текстов китайских статей
3. Написание главы 2 «Обзор литературы» на основе comparison_table.md
4. Опционально: экспериментальный benchmark 2–3 протоколов (ESP-NOW vs Wi-Fi vs LoRa)

## Вспомогательные источники (начальные)

- https://supereyes.ru/articles/arduino-i-robototekhnika/besprovodnye-tekhnologii-v-robototekhnike/
- https://habr.com/ru/articles/743734/
- https://enjoy-robotics.ru/tpost/g759lg6ea1-moduli-svyazi
