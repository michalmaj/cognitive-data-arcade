# src/cognitive_data_arcade/games/prediction_slider/phase_a.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.prediction_slider.simulator import fit_line, simulate_data
from cognitive_data_arcade.games.prediction_slider.widgets import _FloatSlider

_BG     = (15,  15,  35)
_PANEL  = (18,  18,  42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156,  18)
_GREEN  = ( 39, 174,  96)
_RED    = (231,  76,  60)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"

_LEFT_W  = 300
_AREA_H  = 672
_CHART_W = 1024 - _LEFT_W  # 724
_DPI     = 100


def _style_ax(ax) -> None:
    ax.tick_params(colors="#787890", labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a50")


class PhaseAScene(Scene):
    def __init__(self) -> None:
        self._done = False
        x0, w = 16, _LEFT_W - 32
        self._sl_n     = _FloatSlider("N (rozmiar próby)", 10, 300, 50, 5, x0, 60, w, fmt=".0f")
        self._sl_sigma = _FloatSlider("Szum (sigma)", 0.1, 3.0, 1.0, 0.1, x0, 128, w)
        self._sl_slope = _FloatSlider("Nachylenie (slope)", -2.0, 2.0, 1.0, 0.1, x0, 196, w)
        self._chart_surf: pygame.Surface | None = None
        self._fitted_slope = 0.0
        self._fitted_intercept = 0.0
        self._r2 = 0.0
        self._rmse = 0.0
        self._regenerate()

    def _regenerate(self) -> None:
        n = int(self._sl_n.value)
        sigma = self._sl_sigma.value
        slope = self._sl_slope.value
        x, y = simulate_data(n=n, slope=slope, intercept=2.0, noise=sigma, seed=None)
        fs, fi, r2, residuals = fit_line(x, y)
        self._fitted_slope = fs
        self._fitted_intercept = fi
        self._r2 = r2
        self._rmse = float(np.sqrt(np.mean(residuals ** 2)))
        self._chart_surf = self._render_chart(x, y, fs, fi, r2, residuals)

    def _render_chart(
        self, x, y, fs, fi, r2, residuals
    ) -> pygame.Surface:
        fig = plt.figure(
            figsize=(_CHART_W / _DPI, _AREA_H / _DPI),
            dpi=_DPI, facecolor=_FIG_BG,
        )
        gs = fig.add_gridspec(2, 1, height_ratios=[0.6, 0.4])
        gs.update(left=0.12, right=0.97, top=0.96, bottom=0.06, hspace=0.45)
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])

        ax1.set_facecolor(_AX_BG)
        ax1.scatter(x, y, s=18, alpha=0.65, color="#3498db")
        x_line = np.linspace(x.min(), x.max(), 100)
        ax1.plot(x_line, fs * x_line + fi, color="#e74c3c", lw=2)
        r2_col = "#27ae60" if r2 >= 0.7 else ("#f39c12" if r2 >= 0.4 else "#e74c3c")
        ax1.text(0.97, 0.95, f"R² = {r2:.3f}", transform=ax1.transAxes,
                 ha="right", va="top", color=r2_col, fontsize=10, fontweight="bold")
        ax1.set_title("Dane i linia regresji", color="white", fontsize=9)
        _style_ax(ax1)

        ax2.set_facecolor(_AX_BG)
        y_hat = fs * x + fi
        ax2.scatter(y_hat, residuals, s=14, alpha=0.65, color="#f39c12")
        ax2.axhline(0, color="#e74c3c", lw=1.5, ls="--")
        ax2.set_xlabel("Wartości dopasowane", color="#787890", fontsize=8)
        ax2.set_ylabel("Reszty", color="#787890", fontsize=8)
        ax2.set_title("Wykres reszt", color="white", fontsize=9)
        _style_ax(ax2)

        return figure_to_surface(fig, (_CHART_W, _AREA_H))

    def handle_event(self, event: pygame.event.Event) -> None:
        changed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for sl in [self._sl_n, self._sl_sigma, self._sl_slope]:
                if sl.handle_mousedown(event.pos):
                    changed = True
        elif event.type == pygame.MOUSEMOTION:
            for sl in [self._sl_n, self._sl_sigma, self._sl_slope]:
                if sl.handle_mousemotion(event.pos, event.buttons):
                    changed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for sl in [self._sl_n, self._sl_sigma, self._sl_slope]:
                sl._dragging = False
        if changed:
            self._regenerate()

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _LEFT_W, _AREA_H))
        surface.blit(get_font(20).render("Parametry", True, _ORANGE), (16, 16))
        self._sl_n.draw(surface)
        self._sl_sigma.draw(surface)
        self._sl_slope.draw(surface)
        self._draw_stats(surface)
        if self._chart_surf is not None:
            surface.blit(self._chart_surf, (_LEFT_W, 0))

    def _draw_stats(self, surface: pygame.Surface) -> None:
        font_sm = get_font(14)
        font_md = get_font(17)
        r2_col = _GREEN if self._r2 >= 0.7 else (_ORANGE if self._r2 >= 0.4 else _RED)
        rows = [
            ("R²",          f"{self._r2:.3f}",              r2_col),
            ("Slope (fitted)",    f"{self._fitted_slope:.3f}",    _WHITE),
            ("Intercept",        f"{self._fitted_intercept:.3f}", _WHITE),
            ("RMSE",             f"{self._rmse:.3f}",            _WHITE),
        ]
        y = 270
        for label, val, col in rows:
            surface.blit(font_sm.render(label, True, _DIM), (12, y))
            surface.blit(font_md.render(val, True, col), (12, y + 14))
            y += 36

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None
