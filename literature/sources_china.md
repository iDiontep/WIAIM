# Источники: Китай (CNKI, IEEE с китайской аффилиацией, патенты CN)

Дата поиска: 2025-09-12. Целевой минимум: 10 источников. Найдено: **14 релевантных источников**.

## Академические статьи (CNKI / китайские журналы)

| # | Авторы | Название | Год | Журнал | DOI | Тема |
|---|--------|----------|-----|--------|-----|------|
| 1 | HE Lyulong, ZHANG Jiaqiang et al. | 有向通信拓扑和时延条件下的无人机集群时变编队控制 | 2020 | 北京航空航天大学学报 | [10.13700/j.bh.1001-5965.2019.0206](https://doi.org/10.13700/j.bh.1001-5965.2019.0206) | UAV swarm, communication delay, formation control |
| 2 | JIA Xiao, ZHANG Guoliang et al. | 异构多机器人编队相互通信时延精确控制 | 2018 | 计算机工程与应用 | [10.3778/j.issn.1002-8331.1701-0225](http://cea.ceaj.org/CN/10.3778/j.issn.1002-8331.1701-0225) | Heterogeneous robots, fixed/zero delay |
| 3 | LIU Xingyu, GUO Ronghua et al. | 基于通信功率自适应的无人机集群协同导航控制方法 | 2024 | 系统工程与电子技术 | [10.12305/j.issn.1001-506X.2024.10.30](https://www.sys-ele.com/CN/10.12305/j.issn.1001-506X.2024.10.30) | Adaptive comm power, swarm navigation |
| 4 | — | 大规模无人机集群通信定位一体化技术 | 2024 | 信号处理 | [10.16798/j.issn.1003-0530.2024.01.001](https://signal.ejournal.org.cn/article/doi/10.16798/j.issn.1003-0530.2024.01.001) | Comm + ranging for UAV swarm |
| 5 | — | 一种考虑通信时延的多移动机器人协同编队控制方法 | 2021 | CN Patent / 发明 | CN110743581 (см. патенты) | Multi-robot formation with delay |

## IEEE / arXiv с аффилиацией China (Tsinghua, BUAA, HIT)

| # | Авторы | Название | Год | Журнал/конф. | DOI/URL | Аффилиация |
|---|--------|----------|-----|--------------|---------|------------|
| 6 | Li C., Lu W., Liang B. et al. | Nav-SCOPE: Swarm Robot Cooperative Perception and Coordinated Navigation | 2024 | arXiv / IROS | [10.48550/arXiv.2409.10049](https://doi.org/10.48550/arXiv.2409.10049) | Tsinghua University |
| 7 | Li C., Lu W. et al. | Highly Efficient Observation Process based on FFT Filtering for Robot Swarm Collaborative Navigation | 2024 | IROS 2024 | [arXiv:2405.07687](https://arxiv.org/abs/2405.07687) | Tsinghua University |
| 8 | Duan S., Su R., Xu C. et al. | Ultra-Wideband Radio Channel Characteristics for Near-Ground Swarm Robots Communication | 2020 | IEEE Trans. Wireless Communications | [10.1109/TWC.2020.2982345](https://doi.org/10.1109/TWC.2020.2982345) | Tsinghua / BUAA |
| 9 | — | Robust and Scalable Multi-Robot Localization Using Stereo UWB Arrays | 2025 | IEEE RA-L | Tsinghua NICLab | UWB 100 Hz, 3D ranging для роя |

## Китайские патенты (как источники технологий)

| # | Номер | Заявитель | Год | Технология | Суть |
|---|-------|-----------|-----|------------|------|
| 10 | CN110799919A | DJI (SZ DJI Technology) | 2020 | Wi-Fi, BT, ZigBee, 2G–5G | Модульная смена коммуникационных модулей в пульте робота |
| 11 | CN110636102B | Tianyu Jingwei | 2022 | 4G/5G | Система связи БПЛА через базовые станции и IDC |
| 12 | CN109048922A | — | 2019 | LoRa | Управление промышленным роботом через LoRa gateway + cloud |
| 13 | CN112015120B | — | 2021 | Wi-Fi | Шинная система управления пром. роботом с Wi-Fi |
| 14 | CN112771476A | Midea Group | 2021 | Wireless remote | Удалённое управление роботом через беспроводную связь |

## Поисковые запросы CNKI (для самостоятельного углубления)

```
无线通信 机器人 控制
群体机器人 无线传感器网络
物联网 工业机器人 通信
蓝牙 机器人 远程控制
LoRa 机器人 通信
5G 工业机器人 控制
```

## Ключевые выводы из китайских источников

1. **Фокус на communication delay** — большинство китайских работ моделируют задержку связи как ключевой фактор стабильности формации/роя.
2. **UAV swarm dominance** — основной объект исследований: дроны, а не промышленные манипуляторы; применимо к теме «рой роботов».
3. **Tsinghua (清华)** — лидер по UWB и ad-hoc связи для роя; сжатие данных до bit-level для экономии канала.
4. **DJI, Huawei, Midea** — ключевые патентообладатели: модульная связь, 4G/5G, адаптивная мощность.
5. **LoRa + cloud** — популярная архитектура для удалённого управления промышленными роботами в Китае.

## Сравнение подходов США vs Китай

| Аспект | США (IEEE) | Китай (CNKI/IEEE CN) |
|--------|------------|----------------------|
| Фокус протоколов | 5G URLLC, Wi-Fi 6, TSN, ESP-NOW | LoRa, 4G/5G, UWB, adaptive power |
| Объект | Industrial robots, cobots, nano-UAV | UAV swarm, heterogeneous multi-robot |
| Метрики | Latency (ms), jitter, throughput | Communication delay in control loop, formation stability |
| Патенты | ABB, Siemens, Georgia Tech | DJI, Huawei, Midea, пром. IoT |
