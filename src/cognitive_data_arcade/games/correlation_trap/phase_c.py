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
    CorrResult, _SANDBOX_VARS, _sandbox_corr, _sandbox_seed, generate_correlated,
)

_BG     = (15, 15, 35)
_PANEL  = (18, 18, 42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156, 18)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"

_AREA_H    = 672
_TOP_H     = 56
_HINT_H    = 40
_SCATTER_W = 716
_SCATTER_H = _AREA_H - _TOP_H - _HINT_H
_STATS_W   = 1024 - _SCATTER_W
_CHART_W   = 700
_CHART_H   = _SCATTER_H - 16
_DPI       = 100

_ROW_H     = 26   # dropdown row height

_POPUPS_C: dict[str, ContextInfo] = {
    "dropdown_x": ContextInfo(
        title="Zmienna X (os pozioma)",
        body=(
            "Zmienna X to predyktor lub niezalezna w ukladzie.\n"
            "Tu wybierasz co wyswietlic na osi poziomej wykresu."
        ),
        impact="Zamiana X i Y nie zmienia r Pearsona (jest symetryczny)!",
    ),
    "dropdown_y": ContextInfo(
        title="Zmienna Y (os pionowa)",
        body=(
            "Zmienna Y to wynik lub zalezna w ukladzie.\n"
            "Tu wybierasz co wyswietlic na osi pionowej wykresu."
        ),
        impact="Zamiana X i Y nie zmienia r Pearsona (jest symetryczny)!",
    ),
    "scatter": ContextInfo(
        title="Eksploracja par zmiennych",
        body=(
            "Sandbox pozwala zestawic dowolne dwie zmienne.\n"
            "Znajdz pary z r > 0.8 — przyczynowosc czy zmienna ukryta?"
        ),
        impact="Wysoka r w danych obserwacyjnych prawie zawsze wymaga wyjasnienia.",
    ),
    "r_hero": ContextInfo(
        title="r Pearsona dla wybranej pary",
        body=(
            "Obliczony na 120 syntetycznych punktach danych.\n"
            "Dane odzwierciedlaja realistyczne korelacje z literatury."
        ),
        impact="Porownaj kilka par — znajdz najsilniejsza i najslabsza korelacje!",
    ),
    "r2_display": ContextInfo(
        title="R2 dla wybranej pary",
        body=(
            "R2 mowi jaki % zmiennosci Y wyjasnaja zmienna X.\n"
            "R2=0.77 oznacza ze X 'odpowiada' za 77% wariancji Y."
        ),
        impact="Ale 'wyjasniac' nie znaczy 'powodowac'!",
    ),
    "swap_btn": ContextInfo(
        title="Zamien osie (<->)",
        body=(
            "Zamienia X i Y miejscami. Wykres sie obraca,\n"
            "ale r Pearsona pozostaje identyczne!"
        ),
        impact="Dowod ze korelacja Pearsona jest symetryczna: r(X,Y) = r(Y,X).",
    ),
    "strength_label": ContextInfo(
        title="Sila korelacji",
        body=(
            "|r| < 0.3 slaba; 0.3-0.5 umiarkowana;\n"
            "0.5-0.7 silna; > 0.7 bardzo silna."
        ),
        impact="Znalazles pary z rozna sila? Zastanow sie co je laczy!",
    ),
}


class _Dropdown:
    """Simple dropdown widget — no external library."""

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        vars: list[dict],
        border_color: tuple,
        initial_idx: int = 0,
    ) -> None:
        self._x, self._y, self._w, self._h = x, y, w, h
        self._vars = vars
        self._border = border_color
        self._selected = initial_idx
        self._open = False
        self._hover = -1

    @property
    def selected_key(self) -> str:
        return self._vars[self._selected]["key"]

    @property
    def selected_label(self) -> str:
        return self._vars[self._selected]["label"]

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self._x, self._y, self._w, self._h)

    @property
    def is_open(self) -> bool:
        return self._open

    def select_key(self, key: str) -> None:
        for i, v in enumerate(self._vars):
            if v["key"] == key:
                self._selected = i
                return

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            if self._open:
                for i in range(len(self._vars)):
                    row = pygame.Rect(self._x, self._y + self._h + i * _ROW_H, self._w, _ROW_H)
                    if row.collidepoint(event.pos):
                        self._hover = i
                        return True
                self._hover = -1
            return False
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        pos = event.pos
        if pygame.Rect(self._x, self._y, self._w, self._h).collidepoint(pos):
            self._open = not self._open
            return True
        if self._open:
            for i in range(len(self._vars)):
                row = pygame.Rect(self._x, self._y + self._h + i * _ROW_H, self._w, _ROW_H)
                if row.collidepoint(pos):
                    self._selected = i
                    self._open = False
                    self._hover = -1
                    return True
            self._open = False
        return False

    def draw(self, surface: pygame.Surface) -> None:
        font = get_font(15)
        bg   = (18, 18, 46)
        pygame.draw.rect(surface, bg, (self._x, self._y, self._w, self._h))
        pygame.draw.rect(surface, self._border, (self._x, self._y, self._w, self._h), 1)
        label = f"{self.selected_label} >"
        surface.blit(font.render(label, True, self._border), (self._x + 6, self._y + 5))
        if not self._open:
            return
        for i, v in enumerate(self._vars):
            ry = self._y + self._h + i * _ROW_H
            row_bg = (30, 30, 64) if i == self._hover else (18, 18, 46)
            pygame.draw.rect(surface, row_bg, (self._x, ry, self._w, _ROW_H))
            pygame.draw.rect(surface, (46, 46, 96), (self._x, ry, self._w, _ROW_H), 1)
            col = self._border if i == self._selected else (136, 136, 160)
            surface.blit(font.render(v["label"], True, col), (self._x + 6, ry + 4))


class PhaseCScene(Scene):
    def __init__(self) -> None:
        self._done = False
        dd_h = 32
        dd_y = (_TOP_H - dd_h) // 2
        dd_w = 180
        self._dd_x = _Dropdown( 80, dd_y, dd_w, dd_h, _SANDBOX_VARS, (52, 152, 219), 0)
        self._dd_y = _Dropdown(350, dd_y, dd_w, dd_h, _SANDBOX_VARS, (231, 76, 60),  1)
        self._swap_rect = pygame.Rect(350 + dd_w + 8, dd_y, 80, dd_h)
        self._result: CorrResult | None = None
        self._chart_surf: pygame.Surface | None = None
        self._popup = ContextPopup()
        self._regenerate()
        self._register_popups()

    def _x_key(self) -> str:
        return self._dd_x.selected_key

    def _y_key(self) -> str:
        return self._dd_y.selected_key

    def _x_label(self) -> str:
        return self._dd_x.selected_label

    def _y_label(self) -> str:
        return self._dd_y.selected_label

    def _regenerate(self) -> None:
        xk, yk = self._x_key(), self._y_key()
        r = _sandbox_corr(xk, yk)
        seed = _sandbox_seed(xk, yk)
        self._result = generate_correlated(r, noise=0.0, n=120, seed=seed)
        self._chart_surf = _render_chart(self._result, self._x_label(), self._y_label())

    def _register_popups(self) -> None:
        self._popup.clear()
        scatter_r = pygame.Rect(0, _TOP_H, _SCATTER_W, _SCATTER_H)
        r_hero_r  = pygame.Rect(_SCATTER_W + 4, _TOP_H + 40, _STATS_W - 8, 60)
        r2_r      = pygame.Rect(_SCATTER_W + 4, _TOP_H + 140, _STATS_W - 8, 30)
        str_r     = pygame.Rect(_SCATTER_W + 4, _TOP_H + 110, _STATS_W - 8, 28)
        self._popup.register(self._dd_x.rect,  _POPUPS_C["dropdown_x"])
        self._popup.register(self._dd_y.rect,  _POPUPS_C["dropdown_y"])
        self._popup.register(scatter_r,        _POPUPS_C["scatter"])
        self._popup.register(r_hero_r,         _POPUPS_C["r_hero"])
        self._popup.register(r2_r,             _POPUPS_C["r2_display"])
        self._popup.register(self._swap_rect,  _POPUPS_C["swap_btn"])
        self._popup.register(str_r,            _POPUPS_C["strength_label"])

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._popup.handle_event(event):
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._swap_rect.collidepoint(event.pos):
                xk, yk = self._x_key(), self._y_key()
                self._dd_x.select_key(yk)
                self._dd_y.select_key(xk)
                self._regenerate()
                self._register_popups()
                return
        changed_x = self._dd_x.handle_event(event)
        changed_y = self._dd_y.handle_event(event)
        if changed_x or changed_y:
            # prevent same variable on both axes
            if self._x_key() == self._y_key():
                keys = [v["key"] for v in _SANDBOX_VARS]
                next_idx = (keys.index(self._y_key()) + 1) % len(keys)
                self._dd_y.select_key(keys[next_idx])
            self._regenerate()
            self._register_popups()

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def draw(self, surface: pygame.Surface, offset_y: int = 0) -> None:
        area = pygame.Surface((1024, _AREA_H))
        area.fill(_BG)

        # top bar
        pygame.draw.rect(area, (18, 18, 42), (0, 0, 1024, _TOP_H))
        f14 = get_font(14)
        area.blit(f14.render("Os X:", True, _DIM), (12, (_TOP_H - f14.get_height()) // 2))
        area.blit(f14.render("vs.", True, _DIM), (272, (_TOP_H - f14.get_height()) // 2))
        area.blit(f14.render("Os Y:", True, _DIM), (310, (_TOP_H - f14.get_height()) // 2))
        pygame.draw.rect(area, (18, 18, 60), self._swap_rect, border_radius=4)
        pygame.draw.rect(area, (52, 152, 219), self._swap_rect, 1, border_radius=4)
        sw_lbl = "<->"
        sw_tw = f14.size(sw_lbl)[0]
        area.blit(f14.render(sw_lbl, True, (52, 152, 219)),
                  (self._swap_rect.x + (self._swap_rect.w - sw_tw) // 2,
                   self._swap_rect.y + (self._swap_rect.h - f14.get_height()) // 2))

        # scatter
        if self._chart_surf:
            area.blit(self._chart_surf, (0, _TOP_H + 4))

        # stats panel
        sx = _SCATTER_W + 4
        pygame.draw.rect(area, (18, 18, 42), (_SCATTER_W, _TOP_H, _STATS_W, _SCATTER_H))
        pygame.draw.line(area, (46, 46, 96), (_SCATTER_W, _TOP_H), (_SCATTER_W, _TOP_H + _SCATTER_H))
        if self._result:
            _draw_stats_panel(area, self._result, sx)

        # hint bar
        pygame.draw.rect(area, (18, 18, 42), (0, _AREA_H - _HINT_H, 1024, _HINT_H))
        hint = "Wyprobuj rozne kombinacje — znajdz najsilniejsza i najslabsza korelacje!"
        f13 = get_font(13)
        tw  = f13.size(hint)[0]
        area.blit(f13.render(hint, True, _DIM), ((1024 - tw) // 2, _AREA_H - _HINT_H + 12))

        # dropdowns drawn LAST so they overlay the scatter
        self._dd_x.draw(area)
        self._dd_y.draw(area)

        self._popup.draw(area)
        surface.blit(area, (0, offset_y))


def _draw_stats_panel(surface: pygame.Surface, result: CorrResult, sx: int) -> None:
    f13   = get_font(13)
    f_r   = get_font(32)
    f_str = get_font(14)
    r_str = f"{result.r:+.3f}"
    surface.blit(f13.render("r Pearson", True, (120, 120, 160)), (sx, _TOP_H + 14))
    rw = f_r.size(r_str)[0]
    surface.blit(f_r.render(r_str, True, _ORANGE), (sx + (_STATS_W - 8 - rw) // 2, _TOP_H + 36))
    surface.blit(f_str.render(result.strength, True, _WHITE), (sx, _TOP_H + 110))
    surface.blit(f13.render(f"R2: {result.r2:.3f}", True, _DIM), (sx, _TOP_H + 140))


def _render_chart(result: CorrResult, x_label: str, y_label: str) -> pygame.Surface:
    fig, ax = plt.subplots(
        facecolor=_FIG_BG,
        figsize=(_CHART_W / _DPI, _CHART_H / _DPI),
        dpi=_DPI,
    )
    ax.set_facecolor(_AX_BG)
    ax.scatter(result.x, result.y, color="#3498db", alpha=0.65, s=20)
    if abs(result.r) > 0.05:
        m = float(result.r * result.y.std() / max(1e-9, result.x.std()))
        b = float(result.y.mean() - m * result.x.mean())
        x_line = [float(result.x.min()), float(result.x.max())]
        ax.plot(x_line, [m * xv + b for xv in x_line],
                color="#f39c12", linestyle="--", alpha=0.6)
    ax.set_xlabel(x_label, color="#787890", fontsize=9)
    ax.set_ylabel(y_label, color="#787890", fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#2a2a50")
    return figure_to_surface(fig, (_CHART_W, _CHART_H))
