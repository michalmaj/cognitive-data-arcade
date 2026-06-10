# src/cognitive_data_arcade/games/distribution_playground/phase_c.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.distribution_playground.phase_a import _param_key
from cognitive_data_arcade.games.distribution_playground.simulator import (
    CompareResult, SimResult, compare, simulate,
)
from cognitive_data_arcade.games.distribution_playground.widgets import (
    ShapeTab, Slider, SliderSpec,
)

_BG      = (15, 15, 35)
_WHITE   = (240, 240, 240)
_DIM     = (120, 120, 160)
_BLUE    = (52, 152, 219)
_RED     = (231, 76, 60)
_ORANGE  = (243, 156, 18)
_FIG_BG  = "#0f0f23"
_AX_BG   = "#1a1a3e"
_AREA_H  = 672
_HALF    = 512
_CHART_W = 700
_CHART_H = 340
_STATS_W = 280
_DPI     = 100

_SLIDERS_BY_TYPE: dict[str, list[SliderSpec]] = {
    "normal": [
        SliderSpec("Średnia (mu) ms", 200, 800, 400, 10),
        SliderSpec("Odch. std (sigma) ms", 20, 200, 80, 10),
        SliderSpec("Próbka (N)", 20, 200, 50, 10),
    ],
    "uniform": [
        SliderSpec("Minimum ms", 100, 600, 300, 10),
        SliderSpec("Maksimum ms", 300, 1000, 600, 10),
        SliderSpec("Próbka (N)", 20, 200, 50, 10),
    ],
    "exgaussian": [
        SliderSpec("Średnia (mu) ms", 200, 600, 350, 10),
        SliderSpec("Odch. std (sigma) ms", 20, 150, 60, 10),
        SliderSpec("Ogon exp. (tau) ms", 20, 300, 100, 10),
        SliderSpec("Próbka (N)", 20, 200, 50, 10),
    ],
}

_POPUP_STATS = {
    "delta":    ContextInfo("Delta średnia", "Różnica średnich: x_sr_B - x_sr_A", "Pokazuje przesunięcie, ale nie uwzględnia zmienności"),
    "cohens_d": ContextInfo("Cohen's d", "Standaryzowana różnica: (mu_A-mu_B)/sigma_pool. d>0.8=duży efekt", "Pozwala porównać efekt niezależnie od jednostki"),
    "p_value":  ContextInfo("p-value (test Welcha)", "Prawdop. wyniku przy H0: mu_A=mu_B", "p<0.05 = odrzucamy H0; ale zależy od N!"),
    "sd_ratio": ContextInfo("sigma_A / sigma_B", "Stosunek odchyleń standardowych obu prób", "Różnica zmienności między grupami"),
}


class _ControlPanel:
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple) -> None:
        self._x, self._y, self._w, self._h = x, y, w, h
        self._color = color
        self._tabs = ShapeTab(x=x + 4, y=y + 4, w=w - 8)
        self._sliders: list[Slider] = []
        self._seed = 0
        self._build_sliders()

    @property
    def dist_type(self) -> str:
        return self._tabs.dist_type

    def get_params(self) -> dict[str, float]:
        specs = _SLIDERS_BY_TYPE[self._tabs.dist_type]
        return {_param_key(spec.label): float(sl.value)
                for spec, sl in zip(specs, self._sliders)}

    def simulate(self) -> SimResult:
        self._seed += 1
        return simulate(self._tabs.dist_type, self.get_params(), rng_seed=self._seed)

    def _build_sliders(self) -> None:
        specs = _SLIDERS_BY_TYPE[self._tabs.dist_type]
        self._sliders = [
            Slider(spec, x=self._x + 8, y=self._y + 44 + i * 50, w=self._w - 16)
            for i, spec in enumerate(specs)
        ]

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        if self._tabs.handle_mousedown(pos):
            self._build_sliders()
            return True
        for sl in self._sliders:
            if sl.handle_mousedown(pos):
                return True
        return False

    def handle_mousemotion(self, pos: tuple[int, int], buttons: tuple) -> bool:
        changed = False
        for sl in self._sliders:
            if sl.handle_mousemotion(pos, buttons):
                changed = True
        return changed

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (20, 20, 48),
                         (self._x, self._y, self._w, self._h))
        pygame.draw.rect(surface, self._color,
                         (self._x, self._y, self._w, self._h), width=2, border_radius=4)
        self._tabs.draw(surface)
        for sl in self._sliders:
            sl.draw(surface)


class PhaseCScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._panel_a = _ControlPanel(x=0, y=0, w=_HALF, h=260, color=_BLUE)
        self._panel_b = _ControlPanel(x=_HALF + 4, y=0, w=_HALF - 4, h=260, color=_RED)
        self._popup = ContextPopup()
        self._result_a: SimResult | None = None
        self._result_b: SimResult | None = None
        self._compare: CompareResult | None = None
        self._chart_surf: pygame.Surface | None = None
        self._resimulate()
        self._register_stat_popups()

    def _resimulate(self) -> None:
        self._result_a = self._panel_a.simulate()
        self._result_b = self._panel_b.simulate()
        self._compare = compare(self._result_a, self._result_b)
        self._chart_surf = _render_overlay(self._result_a, self._result_b)

    def _register_stat_popups(self) -> None:
        self._popup.clear()
        stats_x = _CHART_W + 8
        stats_y = 280
        for i, key in enumerate(["delta", "cohens_d", "p_value", "sd_ratio"]):
            rect = pygame.Rect(stats_x, stats_y + i * 40, _STATS_W, 30)
            self._popup.register(rect, _POPUP_STATS[key])

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._popup.handle_event(event):
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            changed_a = self._panel_a.handle_mousedown(event.pos)
            changed_b = self._panel_b.handle_mousedown(event.pos)
            if changed_a or changed_b:
                self._resimulate()
        elif event.type == pygame.MOUSEMOTION:
            changed_a = self._panel_a.handle_mousemotion(event.pos, event.buttons)
            changed_b = self._panel_b.handle_mousemotion(event.pos, event.buttons)
            if changed_a or changed_b:
                self._resimulate()

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def draw(self, surface: pygame.Surface, offset_y: int = 0) -> None:
        area = pygame.Surface((1024, _AREA_H))
        area.fill(_BG)

        self._panel_a.draw(area)
        self._panel_b.draw(area)

        if self._chart_surf:
            area.blit(self._chart_surf, (0, 268))

        if self._compare and self._result_a and self._result_b:
            _draw_compare_stats(area, self._compare, self._result_a, self._result_b)

        self._popup.draw(area)
        surface.blit(area, (0, offset_y))


def _draw_compare_stats(
    surface: pygame.Surface,
    c: CompareResult,
    a: SimResult,
    b: SimResult,
) -> None:
    font_h = get_font(16)
    font   = get_font(15)
    x = _CHART_W + 8
    y = 280
    surface.blit(font_h.render("Porównanie", True, _ORANGE), (x, y - 24))

    rows = [
        f"Delta srednia: {c.delta_mean:+.1f} ms",
        f"Cohen's d: {c.cohens_d:.2f}",
        f"p-value: {c.p_value:.3f}",
        f"sd_A / sd_B: {c.sd_ratio:.2f}",
    ]
    for i, label in enumerate(rows):
        surface.blit(font.render(label, True, _WHITE), (x + 4, y + 6 + i * 40))


def _render_overlay(a: SimResult, b: SimResult) -> pygame.Surface:
    fig, ax = plt.subplots(facecolor=_FIG_BG,
                           figsize=(_CHART_W / _DPI, _CHART_H / _DPI), dpi=_DPI)
    ax.set_facecolor(_AX_BG)
    ax.hist(a.samples, bins="auto", density=True,
            color="#3498db", alpha=0.6, edgecolor="none", label="A")
    ax.hist(b.samples, bins="auto", density=True,
            color="#e74c3c", alpha=0.6, edgecolor="none", label="B")
    ax.legend(facecolor="#1a1a3e", edgecolor="#2a2a50", labelcolor="#c0c0d8", fontsize=8)
    ax.tick_params(colors="#787890")
    for spine in ax.spines.values():
        spine.set_color("#2a2a50")
    ax.set_xlabel("RT (ms)", color="#787890", fontsize=9)
    return figure_to_surface(fig, (_CHART_W, _CHART_H))
