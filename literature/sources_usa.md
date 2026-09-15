# Источники: США и международные (IEEE, arXiv)

Дата поиска: 2025-09-12. Целевой минимум: 10 статей. Найдено: **18 релевантных источников**.

## Обзорные статьи (survey / tutorial)

| # | Авторы | Название | Год | Журнал/конф. | DOI | Релевантность |
|---|--------|----------|-----|--------------|-----|---------------|
| 1 | Park P. et al. | Wireless Network Design for Control Systems: A Survey | 2018 | IEEE Communications Surveys & Tutorials | [10.1109/COMST.2017.2749498](https://doi.org/10.1109/COMST.2017.2749498) | Фундаментальный обзор WNCS: задержка, потери пакетов, энергопотребление, Industry 4.0 |
| 2 | Claudio E. et al. | When Robotics Meets Wireless Communications: An Introductory Tutorial | 2024 | Proceedings of the IEEE | [10.1109/JPROC.2023.3344698](https://doi.org/10.1109/JPROC.2023.3344698) | Междисциплинарный tutorial: CaR, 5G/6G, рои роботов |
| 3 | — | Towards Wireless Communications in Automation: An Overview | 2024 | IEEE PIMRC | [10.1109/PIMRC53205.2024.10817208](https://doi.org/10.1109/PIMRC53205.2024.10817208) | Требования к беспроводным ICN для мобильных роботов |
| 4 | — | Wireless TSN: A Comprehensive Survey | 2024 | IEEE Access / ComMag | [10.1109/ACCESS.2024.10735349](https://doi.org/10.1109/ACCESS.2024.10735349) | Wireless TSN для робототехники и Industry 4.0 |
| 5 | Oubbati O.S. et al. | Routing in Flying Ad Hoc Networks: Survey, Constraints, and Future Challenge Perspectives | 2019 | IEEE Access | [10.1109/ACCESS.2019.2923898](https://doi.org/10.1109/ACCESS.2019.2923898) | Маршрутизация в FANET — применимо к БПЛА-роям |
| 6 | Brambilla M. et al. | Swarm robotics: a review from the swarm engineering perspective | 2013 | Swarm Intelligence | [10.1007/s11721-013-0092-2](https://doi.org/10.1007/s11721-013-0092-2) | Классический обзор рой-робототехники |
| 7 | Khan A. et al. | Convergence of ML and Robotics Communication in Collaborative Assembly | 2019 | J. Intelligent & Robotic Systems | [10.1007/s10846-019-01079-x](https://doi.org/10.1007/s10846-019-01079-x) | ML + беспроводная связь в роях (наземные, подводные, воздушные) |

## Экспериментальные и прикладные исследования

| # | Авторы | Название | Год | Журнал/конф. | DOI | Технология |
|---|--------|----------|-----|--------------|-----|------------|
| 8 | — | Performance of 5G Trials for Industrial Automation | 2022 | Electronics (MDPI) | [10.3390/electronics11030412](https://doi.org/10.3390/electronics11030412) | 5G URLLC, задержка ~0.8–1 ms |
| 9 | — | Prototype of 5G Integrated with TSN for Edge-Controlled Mobile Robotics | 2022 | Electronics (MDPI) | [10.3390/electronics11111666](https://doi.org/10.3390/electronics11111666) | 5G + IEEE 802.1Qbv TSN, мобильные роботы |
| 10 | — | An Operational 5G Edge Cloud-Controlled Robotic Cell Based on MQTT and OPC UA | 2023 | IEEE ICAR | [10.1109/ICAR58858.2023.10406936](https://doi.org/10.1109/ICAR58858.2023.10406936) | 5G edge cloud, промышленная ячейка |
| 11 | — | Performance Evaluation of Closed-loop Industrial Applications Over Imperfect Networks | 2019 | ICJ | [10.36244/icj.2019.2.4](https://doi.org/10.36244/icj.2019.2.4) | URLLC + UR5 robot arm, замкнутый контур |
| 12 | — | Experimental analysis: Wi-Fi, Bluetooth, ZigBee and LoRa for mobile multi-robot in hostile sites | 2024 | IJECE | [10.11591/ijece.v14i3.pp2753-2761](https://doi.org/10.11591/ijece.v14i3.pp2753-2761) | Сравнительный эксперимент 4 протоколов |
| 13 | — | Swarm Robot Communication Using ESP-NOW Mesh Protocol | 2025 | JESA (IIETA) | [10.18280/jesa.590507](https://doi.org/10.18280/jesa.590507) | ESP-NOW mesh vs Wi-Fi, задержка 10–25 ms |
| 14 | — | EACCO: Optimizing Computation and Communication for Energy-Efficient Swarm Robotics | 2025 | Sensors (MDPI) | [10.3390/s26092839](https://doi.org/10.3390/s26092839) | BLE, LoRa, Wi-Fi — энергопотребление |
| 15 | — | Multiple-Network-Based Control System for Unmanned Surveillance | 2023 | Electronics (MDPI) | [10.3390/electronics12030595](https://doi.org/10.3390/electronics12030595) | Гибрид: LoRa + Wi-Fi + BT + LTE |
| 16 | Signer S. et al. | Mixed-Criticality Wireless Communication for Robot Swarms | 2022 | WMC Workshop | [White Rose](https://eprints.whiterose.ac.uk/id/eprint/204460/) | Протокол AirTight для роя |
| 17 | — | DMPC-Swarm: Distributed MPC on Nano UAV Swarms | 2025 | Autonomous Robots | [10.1007/s10514-025-10211-w](https://doi.org/10.1007/s10514-025-10211-w) | Mesh + DMPC, до 16 квадрокоптеров |
| 18 | Siciliano B. et al. | Control Techniques for Safe, Ergonomic, and Efficient HRC: A Survey | 2022 | IEEE TASE | [10.1109/TASE.2021.3129675](https://doi.org/10.1109/TASE.2021.3129675) | Коботы, рост публикаций с 2019 |

## Ключевые выводы из источников США

1. **5G URLLC** достигает задержки 0.8–1 ms на физическом уровне, но полный контур управления роботом добавляет 10–30 ms (MQTT/OPC UA, edge cloud).
2. **Сравнительные эксперimentы** (IJECE 2024) показывают преимущество LoRa в помехоустойчивости; Wi-Fi/BT — для высокой скорости на короткой дистанции.
3. **ESP-NOW mesh** (10–25 ms) превосходит Wi-Fi (100+ ms) для indoor swarm.
4. **Wireless TSN + 5G** — перспективное направление для промышленной мобильной робототехники.
5. **Mixed-criticality protocols** (AirTight) — новый подход к надёжности связи в роях.

## Рекомендуемые для углублённого чтения (топ-5)

1. Park et al. 2018 — Wireless Network Design for Control Systems
2. Claudio et al. 2024 — Robotics Meets Wireless Communications
3. IJECE 2024 — Experimental comparison Wi-Fi/BT/ZigBee/LoRa
4. 5G TSN Mobile Robotics 2022
5. DMPC-Swarm 2025
