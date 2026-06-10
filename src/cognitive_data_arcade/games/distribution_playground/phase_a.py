# src/cognitive_data_arcade/games/distribution_playground/phase_a.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.distribution_playground.simulator import (
    SimResult, simulate,
)
from cognitive_data_arcade.games.distribution_playground.widgets import (
    ShapeTab, Slider, SliderSpec,
)

_BG      = (15, 15, 35)
_PANEL   = (18, 18, 42)
_WHITE   = (240, 240, 240)
_DIM     = (120, 120, 160)
_ORANGE  = (243, 156, 18)
_FIG_BG  = "#0f0f23"
_AX_BG   = "#1a1a3e"

_LEFT_W  = 388     # 38% of 1024
_AREA_H  = 672     # 720 - 48 nav bar
_TAB_H   = 36

_CHART_W = 620
_CHART_H = 420
_DPI     = 100

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

_POPUP_CONTENT: dict[str, ContextInfo] = {
    "mu":    ContextInfo("Srednia (mu)", "Centrum rozkladu. mu = suma(x) / N", "Przesuwa caly rozklad w lewo/prawo"),
    "sigma": ContextInfo("Odch. std (sigma)", "Przecietne odchylenie od sredniej.", "Wieksze sigma -> szerszy, nizszy rozklad"),
    "tau":   ContextInfo("Ogon exp. (tau)", "Srednia skladowej wykladniczej w Ex-Gaussian", "Wieksze tau -> dluzszy ogon prawostronny"),
    "N":     ContextInfo("Probka (N)", "Liczba losowanych obserwacji", "Wieksze N -> bardziej stabilny histogram"),
    "min":   ContextInfo("Minimum", "Dolna granica rozkladu jednostajnego", "Przesuwa lewy kraniec rozkladu"),
    "max":   ContextInfo("Maksimum", "Gorna granica rozkladu jednostajnego", "Przesuwa prawy kraniec rozkladu"),
    "mean":  ContextInfo("Srednia probkowa", "x_sr = suma(x_i) / N", "Czula na outliery"),
    "median":ContextInfo("Mediana", "Wartosc srodkowa po posortowaniu probki", "Odporna na outliery"),
    "sd":    ContextInfo("Odchylenie std.", "Przecietne odchylenie obserwacji od sredniej", "Wieksze SD = szerszy rozklad"),
    "iqr":   ContextInfo("IQR", "Q3 - Q1: srodkowe 50% danych", "Odporny na outliery miernik rozrzutu"),
    "skew":  ContextInfo("Skosnosc", "Miara asymetrii. 0=symetryczny, >0=ogon w prawo", "RT-y maja skosnosc >0 (prawy ogon)"),
}


def _param_key(label: str) -> str:
    lo = label.lower()
    if "minimum" in lo or lo.startswith("min"):
        return "min"
    if "maksimum" in lo or lo.startswith("maks"):
        return "max"
    if "mu" in lo or "srednia" in lo:
        return "mu"
    if "sigma" in lo or "odch" in lo:
        return "sigma"
    if "tau" in lo or "ogon" in lo:
        return "tau"
    return "N"


class PhaseAScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._tabs = ShapeTab(x=_LEFT_W + 8, y=8, w=_CHART_W - 16)
        self._sliders: list[Slider] = []
        self._result: SimResult | None = None
        self._chart_surf: pygame.Surface | None = None
        self._popup = ContextPopup()
        self._seed = 0
        self._build_sliders()
        self._resimulate()

    def _build_sliders(self) -> None:
        dist = self._tabs.dist_type
        specs = _SLIDERS[dist]
        self._sliders = [
            Slider(spec, x=20, y=80 + i * 58, w=_LEFT_W - 40)
            for i, spec in enumerate(specs)
        ]
        self._register_slider_popups()

    def _register_slider_popups(self) -> None:
        self._popup.clear()
        dist = self._tabs.dist_type
        if dist == "normal":
            keys = ["mu", "sigma", "N"]
        elif dist == "uniform":
            keys = ["min", "max", "N"]
        else:
            keys = ["mu", "sigma", "tau", "N"]
        for slider, key in zip(self._sliders, keys):
            self._popup.register(slider.rect, _POPUP_CONTENT[key])

    def _get_params(self) -> dict[str, float]:
        dist = self._tabs.dist_type
        specs = _SLIDERS[dist]
        return {_param_key(spec.label): float(sl.value)
                for spec, sl in zip(specs, self._sliders)}

    def _resimulate(self) -> None:
        self._result = simulate(self._tabs.dist_type, self._get_params(), rng_seed=self._seed)
        self._seed += 1
        self._chart_surf = _render_chart(self._result)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._popup.handle_event(event):
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._tabs.handle_mousedown(event.pos):
                self._build_sliders()
                self._resimulate()
                return
            changed = False
            for sl in self._sliders:
                if sl.handle_mousedown(event.pos):
                    changed = True
            if changed:
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

        font_h = get_font(16)
        area.blit(font_h.render("Parametry", True, _ORANGE), (12, 12))

        self._tabs.draw(area)
        for sl in self._sliders:
            sl.draw(area)

        if self._result:
            _draw_stats(area, self._result, y=_AREA_H - 160)

        if self._chart_surf:
            area.blit(self._chart_surf, (_LEFT_W + 4, _TAB_H + 12))

        self._popup.draw(area)
        surface.blit(area, (0, offset_y))


def _draw_stats(surface: pygame.Surface, r: SimResult, y: int) -> None:
    font = get_font(15)
    col = _DIM
    stats = [
        ("Srednia", f"{r.mean:.1f} ms"),
        ("Mediana", f"{r.median:.1f} ms"),
        ("SD",      f"{r.sd:.1f} ms"),
        ("IQR",     f"{r.iqr:.1f} ms"),
        ("Skosnosc",f"{r.skewness:.2f}"),
    ]
    for i, (lbl, val) in enumerate(stats):
        col_x = 12 + (i % 2) * 160
        row_y = y + (i // 2) * 22
        surface.blit(font.render(f"{lbl}: {val}", True, _DIM), (col_x, row_y))


def _render_chart(r: SimResult) -> pygame.Surface:
    fig, ax = plt.subplots(facecolor=_FIG_BG,
                           figsize=(_CHART_W / _DPI, _CHART_H / _DPI), dpi=_DPI)
    ax.set_facecolor(_AX_BG)
    ax.hist(r.samples, bins="auto", density=True,
            color="#3498db", alpha=0.7, edgecolor="none")
    ax.tick_params(colors="#787890")
    for spine in ax.spines.values():
        spine.set_color("#2a2a50")
    ax.set_xlabel("RT (ms)", color="#787890", fontsize=9)
    ax.set_ylabel("Gestosc", color="#787890", fontsize=9)
    return figure_to_surface(fig, (_CHART_W, _CHART_H))
