# Сравнительная таблица беспроводных технологий для управления роботом/роем

Источники: см. [sources_usa.md](sources_usa.md), [sources_china.md](sources_china.md).  
Критерии заполнены по данным экспериментальных и обзорных работ 2018–2025.

| Технология | Дальность | Скорость | Задержка | Энергопотребление | Масштаб роя | Промышленность | Типичное применение |
|------------|-----------|----------|----------|-------------------|-------------|----------------|---------------------|
| **BLE 5.x** | 10–100 м | 125 kbps – 2 Mbps | 7–30 ms | Очень низкое | 10–50 узлов | Средняя | Телеметрия, датчики, простое управление |
| **Wi-Fi 6 (802.11ax)** | 50–200 м | 100 Mbps – 1 Gbps | 5–100 ms* | Высокое | 5–20 узлов** | Высокая | Видео, FPV, edge cloud, пром. Ethernet-замена |
| **ZigBee (802.15.4)** | 10–100 м | 250 kbps | 15–50 ms | Низкое | 50–100+ (mesh) | Высокая | Mesh-сенсорные сети, IoT-роботы |
| **LoRa / LoRaWAN** | 1–15 км | 0.3–50 kbps | 100 ms – 2 s | Очень низкое | 100+ (через GW) | Средняя | Телеметрия, команды, hostile environments |
| **5G URLLC** | 100 m – 1 km | 10–100 Mbps | 0.8–2 ms*** | Среднее | 10–100 | Очень высокая | Замкнутый контур, mobile manipulators, TSN |
| **ESP-NOW / nRF24** | 50–200 м | 250 kbps – 1 Mbps | 10–25 ms | Низкое | 10–30 | Низкая | Образовательные рои, indoor swarm |
| **UWB** | 10–200 м | 6.8 Mbps | < 1 ms (ranging) | Среднее | 10–50 | Растущая | Локализация + связь в рое (Tsinghua) |
| **Cellular LTE** | км | 10–100 Mbps | 20–50 ms | Высокое | 10–50 | Средняя | Удалённое управление, surveillance |

\* Wi-Fi: 5–25 ms в lab (ESP-NOW comparison); 100+ ms при росте числа клиентов (JESA 2025).  
\*\* Wi-Fi ограничен числом одновременных подключений без mesh.  
\*\*\* 5G air interface; end-to-end с TSN: < 0.8 ms (Electronics 2022); с MQTT/OPC UA: +10–30 ms (ICAR 2023).

## Детализация по источникам

### BLE 5.x
- **Дальность:** до 100 м (BLE 5 Long Range)
- **Энергия:** наименьшее среди протоколов с двусторонней связью (EACCO 2025, Sensors)
- **Ограничение:** низкая пропускная способность для видео/больших данных
- **Источник:** EACCO 2025; IJECE 2024

### Wi-Fi 6
- **Скорость:** до 9.6 Gbps (теор.), практически 100+ Mbps
- **Задержка:** TSN + Wi-Fi 6 — jitter снижается с 370 µs до 0.9 µs (802.1Qbv)
- **Ограничение:** помехи, congestion при плотном рое
- **Источник:** PIMRC 2024; Electronics 2022; JESA 2025

### ZigBee
- **Mesh:** до 65 000 узлов (теор.), на практике 50–100 для роботов
- **Промышленность:** IEC 62443, проверен в factory automation
- **Источник:** IJECE 2024; Park survey 2018

### LoRa
- **Дальность:** ≥ 10 km в urban (Electronics 2023 surveillance)
- **Помехоустойчивость:** лучшая среди 4 протоколов в hostile sites (IJECE 2024)
- **Ограничение:** unsuitable for real-time swarm coordination (JESA 2025)
- **Источник:** IJECE 2024; CN109048922A; Electronics 2023

### 5G URLLC
- **Задержка air:** 0.8–1 ms @ 99.9% (Electronics 2022)
- **Промышленность:** UR5 robot arm требует URLLC для max accuracy at max speed (ICJ 2019)
- **Edge cloud overhead:** 8–9% degradation in throughput vs Ethernet (ICAR 2023)
- **Источник:** Electronics 2022; ICJ 2019; ICAR 2023

## Рекомендации по выбору (для магистерской)

| Сценарий | Рекомендуемый протокол | Обоснование |
|----------|------------------------|-------------|
| Одиночный робот, real-time control | 5G URLLC + TSN или Wi-Fi 6 + TSN | Минимальная задержка, промышленные стандарты |
| Indoor swarm (5–20 роботов) | ESP-NOW mesh / ZigBee mesh / BLE mesh | Decentralized, low latency, no AP |
| Outdoor swarm / hostile environment | LoRa (commands) + Wi-Fi (data) hybrid | IJECE 2024, Electronics 2023 |
| Локализация + связь в рое | UWB | Tsinghua 2020–2025, cm-level ranging |
| Образовательный / прототип | nRF24L01 / HC-12 / ESP8266 | Habr guide, низкая стоимость |

## Гибридные архитектуры (тренд)

```
[Operator] ──LTE/5G──► [Cloud/Edge] ──Wi-Fi──► [Robot Swarm]
                              │
                    LoRa ◄────┴────► Emergency commands
                    BLE  ◄─────────► Local peer-to-peer
```

Источник: Multiple-Network-Based Control System (Electronics 2023); CN110799919A (DJI modular comm).
