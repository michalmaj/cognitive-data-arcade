from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.correlation_trap.simulator import (
    CorrResult, generate_correlated,
)

_BG     = (15, 15, 35)
_PANEL  = (18, 18, 42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156, 18)
_TRACK  = (42, 42, 80)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"

_LEFT_W  = 389
_AREA_H  = 672
_CHART_W = 610
_CHART_H = 540
_DPI     = 100

_POPUPS_A: dict[str, ContextInfo] = {
    "slider_r": ContextInfo(
        title="Korelacja Pearsona (r)",
        body=(
            "r mierzy liniowy zwiazek miedzy zmiennymi. Zakres: -1 do +1.\n"
            "r=0 to brak zwiazku liniowego."
        ),
        impact="Wyzsze |r| -> punkty blizej linii trendu.",
    ),
    "slider_n": ContextInfo(
        title="Liczba obserwacji (N)",
        body=(
            "Wieksze N -> stabilniejsze szacunki r.\n"
            "Przy malym N nawet duze r moze byc przypadkowe."
        ),
        impact="N < 30 to za malo by ufac r bez testu istotnosci.",
    ),
    "slider_noise": ContextInfo(
        title="Szum (noise)",
        body=(
            "Dodatkowy rozrzut Y niezalezny od r strukturalnego.\n"
            "Wizualnie chmura wyglada mniej 'liniowo'."
        ),
        impact="Duzy szum przy r=0.8 pokazuje ze wizualna ocena moze mylic.",
    ),
    "scatter": ContextInfo(
        title="Wykres punktowy (scatterplot)",
        body=(
            "Kazda kropka to jedna obserwacja (X, Y).\n"
            "Ksztalt chmury: liniowy, krzywoliniowy lub brak zwiazku."
        ),
        impact="Zawsze patrz na wykres przed podaniem r!",
    ),
    "stat_r": ContextInfo(
        title="r Pearsona — co to znaczy?",
        body=(
            "r = cov(X,Y) / (sigma_X * sigma_Y). Zaklada liniowosc.\n"
            "Nieliniowe zaleznosci daja r ~ 0 mimo wzorca."
        ),
        impact="Zawsze wykreslaj dane — samo r nie wystarcza!",
    ),
    "stat_r2": ContextInfo(
        title="R2 — wspolczynnik determinacji",
        body=(
            "R2 = r^2 mowi jaki % wariancji Y wyjasnaja X.\n"
            "R2=0.49 -> X wyjasnaia 49% wariancji Y."
        ),
        impact="Pozostale 1-R2 to wariancja niewyjasniona modelem.",
    ),
    "strength_scale": ContextInfo(
        title="Sila korelacji — skala werbalna",
        body=(
            "|r| < 0.3 slaba; 0.3-0.5 umiarkowana;\n"
            "0.5-0.7 silna; > 0.7 bardzo silna. Wartosci umowne!"
        ),
        impact="W psychologii r=0.3 bywa wazne mimo 'slabej' etykiety.",
    ),
}

_SCALE_CELLS = [
    ("silna -",    (192,  57,  43), (240, 240, 240), "bardzo silna -"),
    ("umiark. -",  (231,  76,  60), (240, 240, 240), "umiarkowana -"),
    ("slaba",      ( 42,  42,  80), (160, 160, 200), "slaba +"),
    ("umiark. +",  ( 41, 128, 185), (240, 240, 240), "umiarkowana +"),
    ("silna +",    ( 26, 111, 181), (240, 240, 240), "bardzo silna +"),
]


class _FloatSlider:
    """Minimal float-value slider for Phase A."""

    def __init__(
        self,
        label: str,
        min_v: float,
        max_v: float,
        default: float,
        step: float,
        x: int,
        y: int,
        w: int,
        fmt: str = ".2f",
    ) -> None:
        self._label = label
        self._min = min_v
        self._max = max_v
        self._step = step
        self._value = default
        self._x, self._y, self._w = x, y, w
        self._fmt = fmt
        self._dragging = False
        self.rect = pygame.Rect(x - 6, y - 2, w + 12, 42)

    @property
    def value(self) -> float:
        return self._value

    def _thumb_x(self) -> int:
        ratio = (self._value - self._min) / max(1e-9, self._max - self._min)
        return self._x + round(ratio * self._w)

    def _track_y(self) -> int:
        return self._y + 26

    def _set_from_pixel(self, px: int) -> None:
        ratio = (px - self._x) / max(1, self._w)
        steps = round(ratio * (self._max - self._min) / self._step)
        raw = self._min + steps * self._step
        self._value = max(self._min, min(self._max, raw))

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        ty = self._track_y()
        if self._x <= px <= self._x + self._w and abs(py - ty) <= 14:
            self._set_from_pixel(px)
            self._dragging = True
            return True
        return False

    def handle_mousemotion(self, pos: tuple[int, int], buttons: tuple) -> bool:
        if not buttons[0]:
            self._dragging = False
            return False
        if not self._dragging:
            return False
        old = self._value
        self._set_from_pixel(pos[0])
        return self._value != old

    def draw(self, surface: pygame.Surface) -> None:
        font_lbl = get_font(16)
        font_val = get_font(18)
        surface.blit(font_lbl.render(self._label, True, _DIM), (self._x, self._y))
        val_str = format(self._value, self._fmt)
        vw = font_val.size(val_str)[0]
        surface.blit(font_val.render(val_str, True, _WHITE),
                     (self._x + self._w - vw, self._y))
        ty = self._track_y()
        pygame.draw.rect(surface, _TRACK,
                         (self._x, ty - 2, self._w, 4), border_radius=2)
        tx = self._thumb_x()
        filled = max(0, tx - self._x)
        if filled > 0:
            pygame.draw.rect(surface, _ORANGE,
                             (self._x, ty - 2, filled, 4), border_radius=2)
        pygame.draw.circle(surface, _ORANGE, (tx, ty), 8)


class PhaseAScene(Scene):
    def __init__(self) -> None:
        self._done = False
        x0, w = 20, _LEFT_W - 40
        self._sl_r     = _FloatSlider("Korelacja (r)",  -1.0, 1.0,  0.50, 0.01, x0, 80,  w)
        self._sl_n     = _FloatSlider("Probka (N)",     20,   500,  150,  10,   x0, 148, w, fmt=".0f")
        self._sl_noise = _FloatSlider("Szum (noise)",    0.0,  1.0,  0.00, 0.05, x0, 216, w)
        self._sliders  = [self._sl_r, self._sl_n, self._sl_noise]
        self._result: CorrResult | None = None
        self._chart_surf: pygame.Surface | None = None
        self._popup = ContextPopup()
        self._register_popups()
        self._regenerate()

    def _register_popups(self) -> None:
        self._popup.clear()
        scatter_rect = pygame.Rect(_LEFT_W + 4, 8, _CHART_W, _CHART_H)
        stat_r_rect  = pygame.Rect(12, 290, _LEFT_W - 24, 22)
        stat_r2_rect = pygame.Rect(12, 314, _LEFT_W - 24, 22)
        scale_rect   = pygame.Rect(12, _AREA_H - 78, _LEFT_W - 24, 32)
        self._popup.register(self._sl_r.rect,     _POPUPS_A["slider_r"])
        self._popup.register(self._sl_n.rect,     _POPUPS_A["slider_n"])
        self._popup.register(self._sl_noise.rect, _POPUPS_A["slider_noise"])
        self._popup.register(scatter_rect,        _POPUPS_A["scatter"])
        self._popup.register(stat_r_rect,         _POPUPS_A["stat_r"])
        self._popup.register(stat_r2_rect,        _POPUPS_A["stat_r2"])
        self._popup.register(scale_rect,          _POPUPS_A["strength_scale"])

    def _regenerate(self) -> None:
        r     = self._sl_r.value
        n     = int(self._sl_n.value)
        noise = self._sl_noise.value
        seed  = n * 7 + 42
        self._result = generate_correlated(r, noise, n, seed=seed)
        self._chart_surf = _render_chart(self._result)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._popup.handle_event(event):
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            changed = any(sl.handle_mousedown(event.pos) for sl in self._sliders)
            if changed:
                self._regenerate()
        elif event.type == pygame.MOUSEMOTION:
            changed = any(
                sl.handle_mousemotion(event.pos, event.buttons)
                for sl in self._sliders
            )
            if changed:
                self._regenerate()

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

        for sl in self._sliders:
            sl.draw(area)

        if self._result:
            _draw_stats(area, self._result)
            _draw_scale(area, self._result.strength)

        if self._chart_surf:
            title_font = get_font(14)
            area.blit(title_font.render("Wykres punktowy — X vs Y", True, _DIM),
                      (_LEFT_W + 4 + (_CHART_W - title_font.size("Wykres punktowy — X vs Y")[0]) // 2, 8))
            area.blit(self._chart_surf, (_LEFT_W + 4, 28))

        self._popup.draw(area)
        surface.blit(area, (0, offset_y))


def _draw_stats(surface: pygame.Surface, result: CorrResult) -> None:
    font = get_font(15)
    y = 280
    stats = [
        ("r Pearson",    f"{result.r:+.3f}"),
        ("R2",           f"{result.r2:.3f}"),
        ("Sila",         result.strength),
        ("N obserwacji", str(len(result.x))),
    ]
    for i, (lbl, val) in enumerate(stats):
        row_y = y + i * 22
        surface.blit(font.render(f"{lbl}:", True, _DIM), (12, row_y))
        surface.blit(font.render(val, True, _WHITE), (140, row_y))


def _draw_scale(surface: pygame.Surface, strength: str) -> None:
    font = get_font(10)
    y  = _AREA_H - 78
    x0 = 12
    w  = _LEFT_W - 24
    cw = w // 5
    for i, (label, bg, fg, match_key) in enumerate(_SCALE_CELLS):
        rx = x0 + i * cw
        pygame.draw.rect(surface, bg, (rx, y, cw - 2, 28))
        if strength == match_key:
            pygame.draw.rect(surface, (243, 156, 18), (rx, y, cw - 2, 28), 1)
        tw = font.size(label)[0]
        surface.blit(font.render(label, True, fg), (rx + (cw - 2 - tw) // 2, y + 9))


def _render_chart(result: CorrResult) -> pygame.Surface:
    fig, ax = plt.subplots(
        facecolor=_FIG_BG,
        figsize=(_CHART_W / _DPI, _CHART_H / _DPI),
        dpi=_DPI,
    )
    ax.set_facecolor(_AX_BG)
    ax.scatter(result.x, result.y, color="#3498db", alpha=0.65, s=20)
    m = float(result.r * result.y.std() / max(1e-9, result.x.std()))
    b = float(result.y.mean() - m * result.x.mean())
    x_line = [float(result.x.min()), float(result.x.max())]
    y_line = [m * xv + b for xv in x_line]
    ax.plot(x_line, y_line, color="#f39c12", linestyle="--", alpha=0.6)
    ax.text(
        0.98, 0.98,
        f"r = {result.r:+.3f}",
        transform=ax.transAxes,
        color="#f39c12",
        fontsize=10,
        va="top",
        ha="right",
    )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#2a2a50")
    return figure_to_surface(fig, (_CHART_W, _CHART_H))
