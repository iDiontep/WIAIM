"""Black-and-white figures for the MAU article."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 10,
    "axes.linewidth": 0.8,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
})


def _box(ax, xy, w, h, text, fc="white"):
    x, y = xy
    p = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.1, edgecolor="black", facecolor=fc,
    )
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", wrap=True)


def _arrow(ax, start, end):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=12,
        linewidth=1.1, color="black", shrinkA=1, shrinkB=1,
    ))


def fig_architecture():
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    _box(ax, (0.3, 2.0), 2.4, 1.4, "Сенсор-\nагент")
    _box(ax, (3.3, 2.0), 2.4, 1.4, "Локальное\nИУ")
    _box(ax, (6.3, 2.0), 2.6, 1.4, "Групповое\nИУ")
    _box(ax, (9.4, 3.4), 2.3, 1.2, "Радиоканал\n(QoS)")
    _box(ax, (9.4, 0.6), 2.3, 1.2, "Контур\nуправления")

    _arrow(ax, (2.7, 2.7), (3.3, 2.7))
    _arrow(ax, (5.7, 2.7), (6.3, 2.7))
    _arrow(ax, (8.9, 3.15), (9.4, 3.8))
    _arrow(ax, (9.4, 3.8), (8.9, 3.15))
    _arrow(ax, (8.9, 2.25), (9.4, 1.4))

    ax.text(6.0, 4.7, "Информационное устройство группы мобильных роботов", ha="center")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_architecture.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig_bitrate():
    channels = ["ESP-NOW", "Wi-Fi", "LoRa"]
    capacity = [500, 100000, 20]  # kbit/s, usable estimate
    flood = [480, 480, 480]
    policy = [105, 105, 105]
    degraded = [9, 9, 9]  # safety+telemetry only

    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    x = range(len(channels))
    w = 0.18
    ax.bar([i - 1.5 * w for i in x], capacity, w, label="Ёмкость канала", fill=False, hatch="///", edgecolor="black")
    ax.bar([i - 0.5 * w for i in x], flood, w, label="Полносвязный обмен", color="0.35", edgecolor="black")
    ax.bar([i + 0.5 * w for i in x], policy, w, label="Предложенная политика", color="0.75", edgecolor="black")
    ax.bar([i + 1.5 * w for i in x], degraded, w, label="Деградация (safety+telemetry)", color="1.0", edgecolor="black")
    ax.set_yscale("log")
    ax.set_xticks(list(x))
    ax.set_xticklabels(channels)
    ax.set_ylabel("Интенсивность, кбит/с")
    ax.set_xlabel("Профиль канала")
    ax.legend(frameon=False, loc="upper right")
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle=":", linewidth=0.6)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "fig2_bitrate.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_architecture()
    fig_bitrate()
    print("wrote", OUT)
