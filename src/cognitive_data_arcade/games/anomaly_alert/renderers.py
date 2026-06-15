# src/cognitive_data_arcade/games/anomaly_alert/renderers.py
from __future__ import annotations

from typing import Callable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.games.anomaly_alert.detector import Element
from cognitive_data_arcade.games.anomaly_alert.scenarios import Scenario

_FIG_W, _FIG_H, _DPI = 680, 624, 96

_AX_BG   = "#0f0f1a"
_FIG_BG  = "#111130"
_SPINE   = "#333355"
_TICK    = "#888899"
_NORMAL  = "#3498db"
_ANOM    = "#e74c3c"


def _ax_style(fig, ax) -> None:
    fig.patch.set_facecolor(_FIG_BG)
    ax.set_facecolor(_AX_BG)
    ax.tick_params(colors=_TICK, labelsize=8)
    for sp in ax.spines.values():
        sp.set_edgecolor(_SPINE)
    ax.xaxis.label.set_color(_TICK)
    ax.yaxis.label.set_color(_TICK)
    ax.title.set_color("#ccccdd")


def _point_px(ax, x_d: float, y_d: float) -> tuple[float, float]:
    """Convert data coords to pygame surface coords (y flipped)."""
    pt = ax.transData.transform([[x_d, y_d]])[0]
    return pt[0], _FIG_H - pt[1]


def _rect_px(
    ax, x0_d: float, y0_d: float, x1_d: float, y1_d: float
) -> tuple[float, float, float, float]:
    """Return (x_px, y_pg_top, w_px, h_px) for a data-space rectangle."""
    pts = ax.transData.transform([[x0_d, y0_d], [x1_d, y1_d]])
    x_min = min(pts[0, 0], pts[1, 0])
    x_max = max(pts[0, 0], pts[1, 0])
    yc_min = min(pts[0, 1], pts[1, 1])
    yc_max = max(pts[0, 1], pts[1, 1])
    return x_min, _FIG_H - yc_max, x_max - x_min, yc_max - yc_min


def render_timeseries(scenario: Scenario, seed: int) -> tuple[pygame.Surface, list[Element]]:
    rng = np.random.default_rng(seed)
    n = 80
    hr = 70 + rng.normal(0, 4, n)
    times = np.arange(n, dtype=float)

    anom_idxs = rng.choice(range(10, n - 10), size=2, replace=False)
    anom_idxs.sort()
    hr[anom_idxs[0]] = 70 + 4 * 4.0
    hr[anom_idxs[1]] = 70 - 4 * 4.0

    fig, ax = plt.subplots(figsize=(_FIG_W / _DPI, _FIG_H / _DPI), dpi=_DPI)
    ax.plot(times, hr, color=_NORMAL, linewidth=1.5, zorder=2)
    ax.scatter(times, hr, color=_NORMAL, s=18, zorder=3)
    ax.set_xlabel("Czas (s)")
    ax.set_ylabel("Tetno (bpm)")
    ax.set_title(scenario.name_pl)
    _ax_style(fig, ax)
    fig.tight_layout()
    fig.canvas.draw()

    anom_set = set(anom_idxs.tolist())
    elements: list[Element] = []
    for i in range(n):
        xp, yp = _point_px(ax, times[i], hr[i])
        xp = max(0.0, min(float(_FIG_W), xp))
        yp = max(0.0, min(float(_FIG_H), yp))
        elements.append(Element(xp, yp, 0.0, 0.0, i in anom_set, f"t={i}s"))

    surf = figure_to_surface(fig, (_FIG_W, _FIG_H))
    return surf, elements


def render_barchart(scenario: Scenario, seed: int) -> tuple[pygame.Surface, list[Element]]:
    rng = np.random.default_rng(seed)
    n = 12
    scores = rng.normal(50, 8, n)
    scores = np.clip(scores, 10, 80)

    anom_idxs = rng.choice(range(n), size=2, replace=False)
    scores[anom_idxs[0]] = rng.uniform(220, 260)
    scores[anom_idxs[1]] = rng.uniform(200, 220)

    x = np.arange(n, dtype=float)

    fig, ax = plt.subplots(figsize=(_FIG_W / _DPI, _FIG_H / _DPI), dpi=_DPI)
    bars = ax.bar(x, scores, color=_NORMAL, width=0.7, zorder=2)
    ax.set_xlabel("Uczestnik")
    ax.set_ylabel("Wynik")
    ax.set_title(scenario.name_pl)
    ax.set_xticks(x)
    ax.set_xticklabels([str(i + 1) for i in range(n)], fontsize=7)
    _ax_style(fig, ax)
    fig.tight_layout()
    fig.canvas.draw()

    anom_set = set(anom_idxs.tolist())
    elements: list[Element] = []
    for i, (patch, val) in enumerate(zip(bars, scores)):
        left = patch.get_x()
        right = left + patch.get_width()
        xp, yp, wp, hp = _rect_px(ax, left, 0.0, right, val)
        elements.append(Element(xp, yp, wp, hp, i in anom_set, f"P{i+1}={val:.0f}"))

    surf = figure_to_surface(fig, (_FIG_W, _FIG_H))
    return surf, elements


def render_scatter(scenario: Scenario, seed: int) -> tuple[pygame.Surface, list[Element]]:
    rng = np.random.default_rng(seed)
    n = 30
    cx, cy = 400.0, 70.0
    cluster = rng.normal([cx, cy], [35, 7], (n, 2))

    anom_pts = np.array([
        [cx + 200.0, cy + 22.0],
        [cx - 195.0, cy - 20.0],
    ])
    all_pts = np.vstack([cluster, anom_pts])
    is_anom = [False] * n + [True, True]

    fig, ax = plt.subplots(figsize=(_FIG_W / _DPI, _FIG_H / _DPI), dpi=_DPI)
    ax.scatter(cluster[:, 0], cluster[:, 1], color=_NORMAL, s=22, alpha=0.75, zorder=2)
    ax.scatter(anom_pts[:, 0], anom_pts[:, 1], color=_ANOM, s=28, alpha=0.9, zorder=3)
    ax.set_xlabel("Czas reakcji (ms)")
    ax.set_ylabel("Dokladnosc (%)")
    ax.set_title(scenario.name_pl)
    _ax_style(fig, ax)
    fig.tight_layout()
    fig.canvas.draw()

    elements: list[Element] = []
    for pt, anom in zip(all_pts, is_anom):
        xp, yp = _point_px(ax, pt[0], pt[1])
        elements.append(Element(xp, yp, 0.0, 0.0, bool(anom), f"RT={pt[0]:.0f}ms"))

    surf = figure_to_surface(fig, (_FIG_W, _FIG_H))
    return surf, elements


def render_histogram(scenario: Scenario, seed: int) -> tuple[pygame.Surface, list[Element]]:
    rng = np.random.default_rng(seed)
    main_data = rng.normal(400, 60, 200)
    anom_vals = np.array([rng.uniform(1150, 1250), rng.uniform(1350, 1450)])
    all_data = np.concatenate([main_data, anom_vals])

    n_bins = 24
    edges = np.linspace(all_data.min() - 10, all_data.max() + 10, n_bins + 1)

    fig, ax = plt.subplots(figsize=(_FIG_W / _DPI, _FIG_H / _DPI), dpi=_DPI)
    counts, _, patches = ax.hist(all_data, bins=edges, color=_NORMAL, edgecolor=_SPINE, zorder=2)
    ax.set_xlabel("Czas odpowiedzi (ms)")
    ax.set_ylabel("Liczba")
    ax.set_title(scenario.name_pl)
    _ax_style(fig, ax)
    fig.tight_layout()
    fig.canvas.draw()

    anom_bins: set[int] = set()
    for v in anom_vals:
        idx = int(np.searchsorted(edges[1:], v))
        idx = min(idx, len(patches) - 1)
        anom_bins.add(idx)

    elements: list[Element] = []
    for i, (patch, left, right) in enumerate(zip(patches, edges[:-1], edges[1:])):
        h = patch.get_height()
        if h == 0:
            continue
        xp, yp, wp, hp = _rect_px(ax, left, 0.0, right, h)
        elements.append(Element(xp, yp, wp, hp, i in anom_bins, f"{left:.0f}-{right:.0f}ms"))

    surf = figure_to_surface(fig, (_FIG_W, _FIG_H))
    return surf, elements


def render_boxplot(scenario: Scenario, seed: int) -> tuple[pygame.Surface, list[Element]]:
    rng = np.random.default_rng(seed)
    n = 35
    group_a = rng.uniform(38, 62, n).tolist()
    group_b = rng.uniform(42, 68, n).tolist()

    anom_a = float(rng.uniform(85, 95))
    anom_b = float(rng.uniform(15, 25))
    group_a.append(anom_a)
    group_b.append(anom_b)

    fig, ax = plt.subplots(figsize=(_FIG_W / _DPI, _FIG_H / _DPI), dpi=_DPI)
    bp = ax.boxplot(
        [group_a, group_b],
        tick_labels=["Grupa A", "Grupa B"],
        showfliers=True,
        flierprops=dict(marker="o", color=_ANOM, markersize=7, markerfacecolor=_ANOM),
        medianprops=dict(color="#2ecc71"),
        boxprops=dict(color=_NORMAL),
        whiskerprops=dict(color=_TICK),
        capprops=dict(color=_TICK),
    )
    ax.set_ylabel("Wynik")
    ax.set_title(scenario.name_pl)
    _ax_style(fig, ax)
    fig.tight_layout()
    fig.canvas.draw()

    elements: list[Element] = []
    for gi, flier_line in enumerate(bp["fliers"]):
        xs = flier_line.get_xdata()
        ys = flier_line.get_ydata()
        for xd, yd in zip(xs, ys):
            xp, yp = _point_px(ax, xd, yd)
            elements.append(Element(xp, yp, 0.0, 0.0, True, f"G{'AB'[gi]}={yd:.1f}"))

    surf = figure_to_surface(fig, (_FIG_W, _FIG_H))
    return surf, elements


def render_heatmap(scenario: Scenario, seed: int) -> tuple[pygame.Surface, list[Element]]:
    rng = np.random.default_rng(seed)
    n_rows, n_cols = 6, 8
    data = rng.uniform(-0.3, 0.6, (n_rows, n_cols))

    anom_positions = [(1, 3), (4, 6)]
    for r, c in anom_positions:
        row_mean = data[r].mean()
        row_std = max(data[r].std(), 0.05)
        data[r, c] = row_mean + 2.6 * row_std

    channels = ["F3", "F4", "C3", "C4", "P3", "P4"]
    conditions = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4"]

    fig, ax = plt.subplots(figsize=(_FIG_W / _DPI, _FIG_H / _DPI), dpi=_DPI)
    ax.imshow(data, aspect="auto", cmap="Blues", origin="upper")
    ax.set_xticks(range(n_cols))
    ax.set_xticklabels(conditions, fontsize=8)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(channels, fontsize=8)
    ax.set_title(scenario.name_pl)
    _ax_style(fig, ax)
    fig.tight_layout()
    fig.canvas.draw()

    anom_set = set(anom_positions)
    elements: list[Element] = []
    for r in range(n_rows):
        for c in range(n_cols):
            xp, yp, wp, hp = _rect_px(ax, c - 0.5, r - 0.5, c + 0.5, r + 0.5)
            elements.append(
                Element(xp, yp, wp, hp, (r, c) in anom_set, f"{channels[r]}-{conditions[c]}")
            )

    surf = figure_to_surface(fig, (_FIG_W, _FIG_H))
    return surf, elements


CHART_RENDERER: dict[str, Callable[[Scenario, int], tuple[pygame.Surface, list[Element]]]] = {
    "timeseries": render_timeseries,
    "barchart":   render_barchart,
    "scatter":    render_scatter,
    "histogram":  render_histogram,
    "boxplot":    render_boxplot,
    "heatmap":    render_heatmap,
}
