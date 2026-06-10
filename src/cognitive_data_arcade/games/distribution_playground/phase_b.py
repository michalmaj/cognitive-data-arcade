# src/cognitive_data_arcade/games/distribution_playground/phase_b.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.distribution_playground.phase_a import _param_key
from cognitive_data_arcade.games.distribution_playground.simulator import (
    SimResult, match_score, random_target, simulate,
)
from cognitive_data_arcade.games.distribution_playground.widgets import (
    ShapeTab, Slider, SliderSpec,
)

_BG     = (15, 15, 35)
_PANEL  = (18, 18, 42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156, 18)
_GREEN  = (39, 174, 96)
_RED    = (231, 76, 60)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"
_LEFT_W = 388
_AREA_H = 672
_CHART_W = 620
_CHART_H = 370
_DPI    = 100
_MAX_HINTS = 3
_SUCCESS_THRESHOLD = 85.0

_SLIDERS: dict[str, list[SliderSpec]] = {
    "normal": [
        SliderSpec("Srednia (mu) ms", 200, 800, 400, 10),
        SliderSpec("Odch. std (sigma) ms", 20, 200, 80, 10),
        SliderSpec("Probka (N)", 20, 200, 50, 10),
    ],
    "uniform": [
        SliderSpec("Minimum ms", 100, 600, 300, 10),
        SliderSpec("Maksimum ms", 300, 1000, 600, 10),
        SliderSpec("Probka (N)", 20, 200, 50, 10),
    ],
    "exgaussian": [
        SliderSpec("Srednia (mu) ms", 200, 600, 350, 10),
        SliderSpec("Odch. std (sigma) ms", 20, 150, 60, 10),
        SliderSpec("Ogon exp. (tau) ms", 20, 300, 100, 10),
        SliderSpec("Probka (N)", 20, 200, 50, 10),
    ],
}


class PhaseBScene(Scene):
    def __init__(self) -> None:
        self._done = False
        import numpy as np
        self._rng = np.random.default_rng(None)
        self._tabs = ShapeTab(x=_LEFT_W + 8, y=8, w=_CHART_W - 16)
        self._sliders: list[Slider] = []
        self._hints_used = 0
        self._revealed = False
        self._success = False
        self._target: SimResult | None = None
        self._target_surf: pygame.Surface | None = None
        self._student_surf: pygame.Surface | None = None
        self._student_result: SimResult | None = None
        self._seed = 0
        self._build_sliders()
        self.new_target()

    def hints_used(self) -> int:
        return self._hints_used

    def target_revealed(self) -> bool:
        return self._revealed

    def use_hint(self) -> None:
        if self._hints_used < _MAX_HINTS:
            self._hints_used += 1

    def give_up(self) -> None:
        self._revealed = True

    def new_target(self) -> None:
        self._target = random_target(self._rng)
        self._target_surf = _render_chart(self._target, alpha=True)
        self._hints_used = 0
        self._revealed = False
        self._success = False
        self._resimulate()

    def _build_sliders(self) -> None:
        specs = _SLIDERS[self._tabs.dist_type]
        self._sliders = [
            Slider(spec, x=20, y=80 + i * 58, w=_LEFT_W - 40)
            for i, spec in enumerate(specs)
        ]

    def _get_params(self) -> dict[str, float]:
        dist = self._tabs.dist_type
        specs = _SLIDERS[dist]
        return {_param_key(spec.label): float(sl.value)
                for spec, sl in zip(specs, self._sliders)}

    def _resimulate(self) -> None:
        self._student_result = simulate(self._tabs.dist_type, self._get_params(),
                                        rng_seed=self._seed)
        self._seed += 1
        self._student_surf = _render_chart(self._student_result, alpha=False)
        if self._target:
            score = match_score(
                self._tabs.dist_type, self._get_params(),
                self._target.dist_type, self._target.params,
            )
            self._success = score >= _SUCCESS_THRESHOLD

    def handle_event(self, event: pygame.event.Event) -> None:
        hint_rect    = pygame.Rect(20, _AREA_H - 80, 120, 30)
        give_up_rect = pygame.Rect(150, _AREA_H - 80, 120, 30)
        new_rect     = pygame.Rect(280, _AREA_H - 80, 120, 30)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hint_rect.collidepoint(event.pos):
                self.use_hint()
                return
            if give_up_rect.collidepoint(event.pos):
                self.give_up()
                return
            if new_rect.collidepoint(event.pos):
                self.new_target()
                return
            if self._tabs.handle_mousedown(event.pos):
                self._build_sliders()
                self._resimulate()
                return
            for sl in self._sliders:
                if sl.handle_mousedown(event.pos):
                    self._resimulate()
        elif event.type == pygame.MOUSEMOTION:
            changed = False
            for sl in self._sliders:
                if sl.handle_mousemotion(event.pos, event.buttons):
                    changed = True
            if changed:
                self._resimulate()

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def draw(self, surface: pygame.Surface, offset_y: int = 0) -> None:
        area = pygame.Surface((1024, _AREA_H))
        area.fill(_BG)
        pygame.draw.rect(area, _PANEL, (0, 0, _LEFT_W, _AREA_H))

        font = get_font(15)
        font_h = get_font(16)
        area.blit(font_h.render("Parametry (Twoje)", True, (100, 180, 255)), (12, 12))

        self._tabs.draw(area)
        for sl in self._sliders:
            sl.draw(area)

        chart_x = _LEFT_W + 4
        chart_y = 44
        if self._target_surf:
            area.blit(self._target_surf, (chart_x, chart_y))
        if self._student_surf:
            area.blit(self._student_surf, (chart_x, chart_y))

        if self._target:
            score = match_score(
                self._tabs.dist_type, self._get_params(),
                self._target.dist_type, self._target.params,
            )
            score_col = _GREEN if score >= _SUCCESS_THRESHOLD else _ORANGE
            area.blit(font.render(f"Dopasowanie: {score:.0f}%", True, score_col),
                      (_LEFT_W + 8, _AREA_H - 90))

        if self._success:
            area.blit(get_font(18).render("Swietnie! Dalej ->", True, _GREEN),
                      (_LEFT_W + 8, _AREA_H - 60))

        if self._hints_used >= 1 and self._target:
            area.blit(font.render(f"Typ: {self._target.dist_type}", True, _ORANGE),
                      (20, _AREA_H - 120))
        if self._revealed and self._target:
            for i, (k, v) in enumerate(self._target.params.items()):
                area.blit(font.render(f"Cel {k}: {v:.0f}", True, _DIM),
                          (20, _AREA_H - 140 + i * 18))

        for lbl, rect, enabled in [
            ("Wskazowka",  pygame.Rect(20, _AREA_H - 80, 120, 30), self._hints_used < _MAX_HINTS),
            ("Poddaj sie", pygame.Rect(150, _AREA_H - 80, 120, 30), not self._revealed),
            ("Nowy cel",   pygame.Rect(280, _AREA_H - 80, 120, 30), True),
        ]:
            col = (60, 60, 100) if enabled else (40, 40, 60)
            pygame.draw.rect(area, col, rect, border_radius=4)
            pygame.draw.rect(area, (100, 100, 160), rect, width=1, border_radius=4)
            tw, th = font.size(lbl)
            area.blit(font.render(lbl, True, _WHITE if enabled else _DIM),
                      (rect.x + (rect.w - tw) // 2, rect.y + (rect.h - th) // 2))

        area.blit(font.render(f"Wskazowki: {self._hints_used}/{_MAX_HINTS}", True, _DIM),
                  (20, _AREA_H - 105))

        surface.blit(area, (0, offset_y))


def _render_chart(r: SimResult, *, alpha: bool = False) -> pygame.Surface:
    color = "#aaaaaa" if alpha else "#3498db"
    fig, ax = plt.subplots(facecolor=_FIG_BG,
                           figsize=(_CHART_W / _DPI, _CHART_H / _DPI), dpi=_DPI)
    ax.set_facecolor(_AX_BG)
    a = 0.35 if alpha else 0.7
    ax.hist(r.samples, bins="auto", density=True, color=color, alpha=a, edgecolor="none")
    ax.tick_params(colors="#787890")
    for spine in ax.spines.values():
        spine.set_color("#2a2a50")
    surf = figure_to_surface(fig, (_CHART_W, _CHART_H))
    if alpha:
        surf.set_alpha(100)
    return surf
