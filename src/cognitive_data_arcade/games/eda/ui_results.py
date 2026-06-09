# src/cognitive_data_arcade/games/eda/ui_results.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.games.eda.simulator import SimResult

_CHART_W, _CHART_H = 480, 240
_DPI = 100
_C1 = "#3498db"
_C2 = "#e74c3c"
_OUT = "#f39c12"
_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_GREEN = (39, 174, 96)
_RED = (231, 76, 60)
_ORANGE = (243, 156, 18)
_FIG_BG = "#0f0f23"
_AX_BG = "#1a1a3e"
_SPINE = "#2a2a50"
_TICK = "#787890"


def _interpret(r: SimResult) -> list[tuple[str, tuple]]:
    n = len(r.cond1)
    pooled_sd = (r.sd1 + r.sd2) / 2.0
    d = abs(r.observed_diff) / pooled_sd if pooled_sd > 0 else 0.0
    lines: list[tuple[str, tuple]] = []

    if r.p_value < 0.05:
        lines.append((f"Różnica istotna stat. (p={r.p_value:.3f} < 0.05).", _GREEN))
    else:
        lines.append((f"Brak istotności stat. (p={r.p_value:.3f} >= 0.05).", _RED))

    if d < 0.2:
        lines.append((f"Efekt znikomy (d={d:.2f}) — zbyt mały do wykrycia.", _RED))
    elif d < 0.5:
        lines.append((f"Efekt mały (d={d:.2f}). Potrzeba dużej próby.", _DIM))
    elif d < 0.8:
        lines.append((f"Efekt średni (d={d:.2f}) — wykrywalny przy N ~ 30.", _ORANGE))
    else:
        lines.append((f"Efekt duży (d={d:.2f}) — łatwy do wykrycia.", _GREEN))

    if r.p_value >= 0.05 and d >= 0.3:
        needed = min(200, round(16.0 / (d * d)))
        if needed > n:
            lines.append((f"Potrzebujesz ~{needed} os./warunek, masz {n}.", _ORANGE))

    impact = max(abs(r.mean1 - r.mean1_no_out), abs(r.mean2 - r.mean2_no_out))
    if impact > 20:
        lines.append((f"Outliery przesunęły średnią o {impact:.0f} ms — uwaga!", _ORANGE))
    elif impact > 5:
        lines.append((f"Outliery: mały wpływ na średnią ({impact:.0f} ms).", _DIM))

    return lines


class ChartPanel:
    def __init__(self) -> None:
        self._surface: pygame.Surface | None = None

    def update(self, result: SimResult) -> None:
        fig, (ax1, ax2) = plt.subplots(
            1, 2,
            facecolor=_FIG_BG,
            figsize=(_CHART_W / _DPI, _CHART_H / _DPI),
            dpi=_DPI,
        )
        _data = [
            (ax1, result.cond1, result.outlier_mask1, _C1, "Warunek 1 (baseline)",
             result.mean1, result.mean1_no_out),
            (ax2, result.cond2, result.outlier_mask2, _C2, "Warunek 2 (+efekt)",
             result.mean2, result.mean2_no_out),
        ]
        for ax, cond, mask, color, title, mean_all, mean_clean in _data:
            ax.set_facecolor(_AX_BG)
            normal = cond[~mask]
            outliers = cond[mask]
            ax.hist(normal, bins=20, color=color, alpha=0.8)
            if len(outliers) > 0:
                ax.hist(outliers, bins=20, color=_OUT, alpha=0.8)
            ax.axvline(mean_all, color="white", linewidth=1.5, linestyle="-")
            if abs(mean_all - mean_clean) > 2:
                ax.axvline(mean_clean, color="white", linewidth=1.0, linestyle="--")
            ax.set_title(title, color="white", fontsize=9)
            ax.set_xlabel("RT (ms)", color=_TICK, fontsize=8)
            ax.tick_params(colors=_TICK, labelsize=7)
            for spine in ax.spines.values():
                spine.set_edgecolor(_SPINE)
        plt.tight_layout(pad=1.2)
        self._surface = figure_to_surface(fig, (_CHART_W, _CHART_H))

    def draw(self, surface: pygame.Surface, x: int, y: int) -> None:
        if self._surface is None:
            msg = get_font(20).render("Kliknij GENERUJ aby wygenerować dane", True, _DIM)
            surface.blit(msg, (x + 10, y + _CHART_H // 2))
            return
        surface.blit(self._surface, (x, y))


class ResultsPanel:
    def __init__(self) -> None:
        self._result: SimResult | None = None
        self._threshold: int | None = None

    def update(self, result: SimResult, threshold: int | None) -> None:
        self._result = result
        self._threshold = threshold

    def draw(self, surface: pygame.Surface, x: int, y: int) -> None:
        if self._result is None:
            return
        r = self._result
        font = get_font(20)
        small = get_font(17)
        interp_font = get_font(18)
        dy = 0

        def blit(text: str, color: tuple = _WHITE, f=font) -> None:
            nonlocal dy
            surface.blit(f.render(text, True, color), (x, y + dy))
            dy += f.size("A")[1] + 3

        blit("Warunek 1             Warunek 2", _DIM)
        blit(f"mean: {r.mean1:6.1f} ms       mean: {r.mean2:6.1f} ms")
        blit(f"SD:   {r.sd1:6.1f} ms       SD:   {r.sd2:6.1f} ms")
        blit(f"bez outl: {r.mean1_no_out:.1f}       bez outl: {r.mean2_no_out:.1f}", _DIM, small)
        dy += 8
        blit(f"Obserwowana różnica: {r.observed_diff:+.1f} ms", _ORANGE)
        blit(f"t = {r.t_stat:.2f},  p = {r.p_value:.3f}", _DIM, small)
        dy += 8

        if self._threshold is not None:
            confirmed = r.observed_diff >= self._threshold
            color = _GREEN if confirmed else _RED
            verdict = "POTWIERDZONA" if confirmed else "OBALONA"
            sign = ">=" if confirmed else "<"
            blit(
                f"hipoteza >= {self._threshold} ms  ->  {verdict}"
                f"  ({r.observed_diff:.0f} {sign} {self._threshold})",
                color,
            )

        dy += 14
        pygame.draw.line(surface, (42, 42, 80), (x, y + dy), (x + 440, y + dy))
        dy += 10
        blit("Interpretacja:", _DIM, small)
        dy += 2
        for text, color in _interpret(r):
            blit(text, color, interp_font)
