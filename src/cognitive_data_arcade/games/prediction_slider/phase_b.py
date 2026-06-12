# src/cognitive_data_arcade/games/prediction_slider/phase_b.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.prediction_slider.simulator import (
    Scenario, _SCENARIOS, fit_line, predict, simulate_scenario,
)
from cognitive_data_arcade.games.prediction_slider.widgets import _VerticalSlider

_BG     = (15,  15,  35)
_PANEL  = (18,  18,  42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156,  18)
_BLUE   = ( 52, 152, 219)
_GREEN  = ( 39, 174,  96)
_RED    = (231,  76,  60)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"

_AREA_W = 1024
_AREA_H = 672
_TOP_H  = 80
_CHART_H = _AREA_H - _TOP_H  # 592
_DPI    = 100

# matplotlib axis fractions — adjust if slider alignment is off after visual check
_AX_LEFT_FRAC  = 0.09
_AX_RIGHT_FRAC = 0.97
_AX_TOP_FRAC   = 0.92
_AX_BOT_FRAC   = 0.12

_AX_LEFT    = int(_AX_LEFT_FRAC * _AREA_W)                  # 92
_AX_RIGHT   = int(_AX_RIGHT_FRAC * _AREA_W)                 # 993
_AX_TOP_REL = int((1 - _AX_TOP_FRAC) * _CHART_H)            # 47
_AX_BOT_REL = int((1 - _AX_BOT_FRAC) * _CHART_H)            # 521

_AX_TOP_ABS = _TOP_H + _AX_TOP_REL   # 127 (in inner surface coords)
_AX_BOT_ABS = _TOP_H + _AX_BOT_REL   # 601

_N_SLIDERS = 5


def _x_data_to_px(x_data: float, sc: Scenario) -> int:
    ratio = (x_data - sc.x_min) / (sc.x_max - sc.x_min)
    return _AX_LEFT + int(ratio * (_AX_RIGHT - _AX_LEFT))


def _y_data_to_px(y_data: float, sc: Scenario) -> int:
    ratio = (y_data - sc.y_min) / (sc.y_max - sc.y_min)
    return _AX_BOT_ABS - int(ratio * (_AX_BOT_ABS - _AX_TOP_ABS))


class PhaseBScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._scenario_idx = 0
        self._state = "waiting"   # "waiting" | "revealed"
        self._score = 0
        self._round_score = 0
        self._x_data: np.ndarray | None = None
        self._y_data: np.ndarray | None = None
        self._x_pts: np.ndarray | None = None
        self._sliders: list[_VerticalSlider] = []
        self._scatter_surf: pygame.Surface | None = None
        self._load_scenario()

    @property
    def _scenario(self) -> Scenario:
        return _SCENARIOS[self._scenario_idx]

    def _load_scenario(self) -> None:
        sc = self._scenario
        self._x_data, self._y_data = simulate_scenario(sc)
        self._x_pts = np.linspace(
            sc.x_min + 0.1 * (sc.x_max - sc.x_min),
            sc.x_max - 0.1 * (sc.x_max - sc.x_min),
            _N_SLIDERS,
        )
        self._sliders = [
            _VerticalSlider(
                x_px=_x_data_to_px(xp, sc),
                y_top_px=_AX_TOP_ABS,
                y_bot_px=_AX_BOT_ABS,
                y_min=sc.y_min,
                y_max=sc.y_max,
            )
            for xp in self._x_pts
        ]
        self._scatter_surf = self._render_scatter(show_regression=False)
        self._state = "waiting"

    def _render_scatter(
        self,
        show_regression: bool = False,
        predictions: list[float] | None = None,
    ) -> pygame.Surface:
        sc = self._scenario
        fig, ax = plt.subplots(
            figsize=(_AREA_W / _DPI, _CHART_H / _DPI),
            dpi=_DPI, facecolor=_FIG_BG,
        )
        fig.subplots_adjust(
            left=_AX_LEFT_FRAC, right=_AX_RIGHT_FRAC,
            bottom=_AX_BOT_FRAC, top=_AX_TOP_FRAC,
        )
        ax.set_facecolor(_AX_BG)
        ax.scatter(self._x_data, self._y_data, s=18, alpha=0.65, color="#3498db")
        ax.set_xlim(sc.x_min - 0.05 * (sc.x_max - sc.x_min),
                    sc.x_max + 0.05 * (sc.x_max - sc.x_min))
        ax.set_ylim(sc.y_min - 0.05 * (sc.y_max - sc.y_min),
                    sc.y_max + 0.05 * (sc.y_max - sc.y_min))

        for xp in self._x_pts:
            ax.axvline(xp, color="#f39c12", ls="--", lw=1.2, alpha=0.8)

        if show_regression and self._x_data is not None:
            slope, intercept, r2, _ = fit_line(self._x_data, self._y_data)
            x_line = np.linspace(sc.x_min, sc.x_max, 100)
            ax.plot(x_line, slope * x_line + intercept, color="#e74c3c", lw=2, zorder=4)
            ax.text(0.97, 0.97, f"R² = {r2:.3f}",
                    transform=ax.transAxes, ha="right", va="top",
                    color="#e74c3c", fontsize=10, fontweight="bold")
            if predictions is not None:
                y_range = sc.y_max - sc.y_min
                for xp, pred in zip(self._x_pts, predictions):
                    y_true = predict(xp, slope, intercept)
                    err_norm = abs(pred - y_true) / y_range
                    col = "#27ae60" if err_norm <= 0.15 else "#e74c3c"
                    ax.plot([xp, xp], [pred, y_true], color=col, lw=2, zorder=5)
                    ax.scatter([xp], [pred], s=70, color=col, zorder=6, marker="^")

        ax.set_xlabel(sc.x_label_pl, color="#787890", fontsize=8)
        ax.set_ylabel(sc.y_label_pl, color="#787890", fontsize=8)
        ax.tick_params(colors="#787890", labelsize=7)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a50")

        return figure_to_surface(fig, (_AREA_W, _CHART_H))

    def _compute_score(self) -> int:
        sc = self._scenario
        slope, intercept, _, _ = fit_line(self._x_data, self._y_data)
        errors = [
            abs(sl.value - predict(xp, slope, intercept))
            for xp, sl in zip(self._x_pts, self._sliders)
        ]
        mae = float(np.mean(errors))
        y_range = sc.y_max - sc.y_min
        normalized_mae = mae / y_range
        return max(0, int(100 - normalized_mae * 200))

    def _confirm(self) -> None:
        predictions = [sl.value for sl in self._sliders]
        self._scatter_surf = self._render_scatter(show_regression=True, predictions=predictions)
        self._round_score = self._compute_score()
        self._score += self._round_score
        self._state = "revealed"

    def _next_scenario(self) -> None:
        if self._scenario_idx < len(_SCENARIOS) - 1:
            self._scenario_idx += 1
            self._load_scenario()
        else:
            self._scenario_idx = 0
            self._score = 0
            self._load_scenario()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            confirm_rect = pygame.Rect(_AREA_W - 180, _AREA_H - 52, 164, 36)
            next_rect    = pygame.Rect(_AREA_W - 180, _AREA_H - 52, 164, 36)
            if self._state == "waiting" and confirm_rect.collidepoint(pos):
                self._confirm()
                return
            if self._state == "revealed" and next_rect.collidepoint(pos):
                self._next_scenario()
                return
            if self._state == "waiting":
                for sl in self._sliders:
                    if sl.handle_mousedown(pos):
                        break
        elif event.type == pygame.MOUSEMOTION:
            if self._state == "waiting":
                for sl in self._sliders:
                    sl.handle_mousemotion(event.pos, event.buttons)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for sl in self._sliders:
                sl._dragging = False

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        if self._scatter_surf:
            surface.blit(self._scatter_surf, (0, _TOP_H))
        if self._state == "waiting":
            for sl in self._sliders:
                sl.draw(surface)
        self._draw_confirm_button(surface)
        if self._state == "revealed":
            self._draw_verdict(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL, (0, 0, _AREA_W, _TOP_H))
        sc = self._scenario
        font_sm = get_font(13)
        font_lg = get_font(20)
        counter = f"Scenariusz {self._scenario_idx + 1} / {len(_SCENARIOS)}"
        surface.blit(font_sm.render(counter, True, _ORANGE), (12, 6))
        surface.blit(font_lg.render(sc.title_pl, True, _WHITE), (12, 22))
        score_txt = f"Wynik: {self._score}"
        sw = get_font(16).size(score_txt)[0]
        surface.blit(get_font(16).render(score_txt, True, _DIM), (_AREA_W - sw - 12, 28))

    def _draw_confirm_button(self, surface: pygame.Surface) -> None:
        if self._state == "waiting":
            btn_rect = pygame.Rect(_AREA_W - 180, _AREA_H - 52, 164, 36)
            pygame.draw.rect(surface, (26, 42, 26), btn_rect, border_radius=4)
            pygame.draw.rect(surface, _GREEN, btn_rect, 2, border_radius=4)
            lbl = get_font(16).render("Zatwierdź predykcję", True, _GREEN)
            surface.blit(lbl, (_AREA_W - 180 + (164 - lbl.get_width()) // 2, _AREA_H - 43))
        else:
            is_last = self._scenario_idx == len(_SCENARIOS) - 1
            lbl_txt = "Graj ponownie" if is_last else "Następny scenariusz"
            btn_rect = pygame.Rect(_AREA_W - 200, _AREA_H - 52, 184, 36)
            pygame.draw.rect(surface, _PANEL, btn_rect, border_radius=4)
            pygame.draw.rect(surface, _BLUE, btn_rect, 2, border_radius=4)
            lbl = get_font(16).render(lbl_txt, True, _BLUE)
            surface.blit(lbl, (_AREA_W - 200 + (184 - lbl.get_width()) // 2, _AREA_H - 43))

    def _draw_verdict(self, surface: pygame.Surface) -> None:
        font = get_font(17)
        col = _GREEN if self._round_score >= 70 else (_ORANGE if self._round_score >= 40 else _RED)
        txt = f"Wynik rundy: {self._round_score} / 100"
        surface.blit(font.render(txt, True, col), (12, _AREA_H - 48))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None
