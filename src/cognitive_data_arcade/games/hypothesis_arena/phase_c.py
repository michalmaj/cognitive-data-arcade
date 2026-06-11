# src/cognitive_data_arcade/games/hypothesis_arena/phase_c.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.hypothesis_arena.simulator import compute_power, min_n_for_power
from cognitive_data_arcade.games.hypothesis_arena.widgets import _AlphaButtons, _FloatSlider

_BG     = (15,  15,  35)
_PANEL  = (18,  18,  42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156,  18)
_BLUE   = ( 52, 152, 219)
_GREEN  = ( 39, 174,  96)
_RED    = (231,  76,  60)
_FIG_BG         = "#0f0f23"
_AX_BG          = "#1a1a3e"
_DARK_ORANGE_BG = (58, 42, 16)
_MUTED          = (80, 80, 100)

_LEFT_W   = 300
_AREA_H   = 672
_AREA_W   = 1024
_RIGHT_W  = _AREA_W - _LEFT_W  # 724
_SCROLL_H = 820
_MATRIX_H = 360
_CURVE_H  = 360
_DPI      = 100

_POPUPS_C: dict[str, ContextInfo] = {
    "cell_type1": ContextInfo(
        title="Błąd I rodzaju (fałszywy alarm)",
        body="Odrzucasz H0 gdy H0 jest prawdziwa. Prawdopodobieństwo = alfa. Np. ogłaszasz że lek działa, choć nie działa.",
        impact="Zmniejsz alfa (0.01) żeby rzadziej alarmować fałszywie — ale zwiększysz beta.",
    ),
    "cell_power": ContextInfo(
        title="Moc testu (trafne wykrycie)",
        body="Odrzucasz H0 gdy H0 jest fałszywa. Prawdopodobieństwo = 1-beta. Im większe N lub d, tym lepsza moc.",
        impact="Moc < 80% = za małe badanie. Moc 90%+ = solidna nauka.",
    ),
    "cell_type2": ContextInfo(
        title="Błąd II rodzaju (przeoczony efekt)",
        body="Nie odrzucasz H0 gdy H0 jest fałszywa. Prawdopodobieństwo = beta. Np. lek działa, ale badanie tego nie wykazało.",
        impact="Zmniejsz beta zwiększając N lub wybierając większe d do wykrycia.",
    ),
    "cell_correct": ContextInfo(
        title="Poprawna decyzja (brak efektu — OK)",
        body="Nie odrzucasz H0 gdy H0 jest prawdziwa. Prawdopodobieństwo = 1-alfa. Poprawna decyzja bez efektu.",
        impact="To dobry wynik — brak fałszywego alarmu gdy naprawdę nie ma efektu.",
    ),
    "power_curve": ContextInfo(
        title="Krzywa mocy",
        body="Pokazuje jak rośnie moc testu wraz z N przy ustalonym d i alfa. Cel: moc >= 80% (zielona linia).",
        impact="Pomarańczowy marker = Twoje aktualne N. Przesuwaj suwak N wzdłuż krzywej.",
    ),
}


class PhaseCScene(Scene):
    def __init__(self) -> None:
        self._done = False
        x0, w = 16, _LEFT_W - 32
        self._sl_n = _FloatSlider("N na grupę", 10, 500, 40, 10, x0, 60, w, fmt=".0f")
        self._sl_d = _FloatSlider("Rozmiar efektu (d)", 0.0, 1.0, 0.40, 0.05, x0, 128, w)
        self._alpha_btn = _AlphaButtons(x0, 222, 80, 28)
        self._power_surf: pygame.Surface | None = None
        self._scroll_y = 0
        self._popup = ContextPopup()
        self._register_popups()
        self._rebuild_curve()

    def _max_scroll(self) -> int:
        return max(0, _SCROLL_H - _AREA_H)

    def _power(self) -> float:
        return compute_power(int(self._sl_n.value), self._sl_d.value, self._alpha_btn.value)

    def _min_n(self) -> int:
        return min_n_for_power(0.80, self._sl_d.value, self._alpha_btn.value)

    def _register_popups(self) -> None:
        self._popup.clear()
        self._popup.register(self._sl_n.rect, ContextInfo(
            title="N na grupę",
            body="Zwiększaj N aby przesunąć punkt mocy wzdłuż krzywej w górę.",
            impact="Dla d=0.20 i alfa=0.05 potrzebujesz N ok. 394 żeby osiągnąć 80% mocy.",
        ))
        self._popup.register(self._sl_d.rect, ContextInfo(
            title="Rozmiar efektu (d)",
            body="Mniejsze d wymaga dużo więcej uczestników. d=0.50 wymaga ok. 4x mniej niż d=0.20.",
            impact="Zdefiniuj minimalny klinicznie ważny efekt zanim planujesz badanie.",
        ))
        self._popup.register(self._alpha_btn.rect, ContextInfo(
            title="Alpha",
            body="Zmiana alfa przesuwa całą krzywą mocy. Mniejsze alfa = mniej mocy przy tym samym N.",
            impact="alfa=0.01 wymaga większego N niż alfa=0.05 by osiągnąć tę samą moc.",
        ))
        sy = self._scroll_y
        cell_w = (_RIGHT_W - 120 - 8) // 2
        cell_h = 120
        col_x = [_LEFT_W + 120, _LEFT_W + 120 + cell_w + 4]
        row_y = [50 - sy, 50 + cell_h + 4 - sy]
        self._popup.register(
            pygame.Rect(col_x[0], row_y[0], cell_w, cell_h), _POPUPS_C["cell_type1"]
        )
        self._popup.register(
            pygame.Rect(col_x[1], row_y[0], cell_w, cell_h), _POPUPS_C["cell_power"]
        )
        self._popup.register(
            pygame.Rect(col_x[0], row_y[1], cell_w, cell_h), _POPUPS_C["cell_correct"]
        )
        self._popup.register(
            pygame.Rect(col_x[1], row_y[1], cell_w, cell_h), _POPUPS_C["cell_type2"]
        )
        curve_rect = pygame.Rect(_LEFT_W + 8, _MATRIX_H + 10 - sy, _RIGHT_W - 16, _CURVE_H)
        self._popup.register(curve_rect, _POPUPS_C["power_curve"])

    def _rebuild_curve(self) -> None:
        alpha = self._alpha_btn.value
        d = self._sl_d.value
        n_cur = int(self._sl_n.value)
        n_80 = self._min_n()
        fig, ax = plt.subplots(
            figsize=(_RIGHT_W / _DPI, _CURVE_H / _DPI), dpi=_DPI, facecolor=_FIG_BG
        )
        ax.set_facecolor(_AX_BG)
        ns = np.arange(10, 501, 5)
        powers = [compute_power(int(n), d, alpha) for n in ns]
        ax.plot(ns, powers, color="#3498db", lw=2)
        ax.axhline(0.80, color="#27ae60", lw=1.2, ls="--", alpha=0.7)
        ax.text(505, 0.80, "80%", color="#27ae60", fontsize=8, va="center")
        p_cur = compute_power(n_cur, d, alpha)
        ax.axvline(n_cur, color="#f39c12", lw=1.5, ls="--")
        ax.plot(n_cur, p_cur, "o", color="#f39c12", ms=7)
        label_y = min(p_cur + 0.06, 0.95)
        ax.text(n_cur, label_y, f"N={n_cur}\n{p_cur*100:.0f}%",
                ha="center", color="#f39c12", fontsize=8)
        if n_80 < 500:
            p80 = compute_power(n_80, d, alpha)
            ax.plot(n_80, p80, "o", color="#27ae60", ms=5, alpha=0.7)
            ax.text(n_80, max(p80 - 0.06, 0.05), f"N ok.{n_80}",
                    ha="center", color="#27ae60", fontsize=8)
        ax.set_xlim(10, 500)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("N na grupę", color="#787890", fontsize=9)
        ax.set_ylabel("Moc (1-beta)", color="#787890", fontsize=9)
        ax.set_title("Krzywa mocy", color="white", fontsize=10)
        ax.tick_params(colors="#787890", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a50")
        self._power_surf = figure_to_surface(fig, (_RIGHT_W, _CURVE_H))

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._popup.handle_event(event):
            return
        changed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for sl in [self._sl_n, self._sl_d]:
                if sl.handle_mousedown(event.pos):
                    changed = True
        elif event.type == pygame.MOUSEMOTION:
            for sl in [self._sl_n, self._sl_d]:
                if sl.handle_mousemotion(event.pos, event.buttons):
                    changed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._sl_n._dragging = False
            self._sl_d._dragging = False
        elif event.type == pygame.MOUSEWHEEL:
            old = self._scroll_y
            self._scroll_y = max(0, min(self._scroll_y - event.y * 30, self._max_scroll()))
            if self._scroll_y != old:
                self._register_popups()
        if self._alpha_btn.handle_event(event):
            changed = True
        if changed:
            self._rebuild_curve()
            self._register_popups()

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _LEFT_W, _AREA_H))
        self._draw_left_panel(surface)
        right_surf = pygame.Surface((_RIGHT_W, _SCROLL_H))
        right_surf.fill(_BG)
        self._draw_matrix(right_surf)
        if self._power_surf:
            right_surf.blit(self._power_surf, (0, _MATRIX_H + 10))
        surface.blit(right_surf, (_LEFT_W, -self._scroll_y))
        if self._max_scroll() > 0:
            hint = get_font(13).render("kółko myszy = przewijanie", True, (42, 42, 80))
            surface.blit(hint, (_LEFT_W + 8, _AREA_H - 18))
        self._popup.draw(surface)

    def _draw_left_panel(self, surface: pygame.Surface) -> None:
        surface.blit(get_font(20).render("Sandbox", True, _ORANGE), (16, 16))
        self._sl_n.draw(surface)
        self._sl_d.draw(surface)
        self._alpha_btn.draw(surface)
        power = self._power()
        beta  = 1.0 - power
        n_80  = self._min_n()
        font_sm = get_font(14)
        font_md = get_font(17)
        y = 280
        rows = [
            ("Moc (1-beta)",   f"{power * 100:.0f}%", _GREEN if power >= 0.80 else _ORANGE),
            ("beta (błąd II)", f"{beta  * 100:.0f}%", _ORANGE if beta > 0.20 else _DIM),
            ("alfa (błąd I)",  f"{self._alpha_btn.value * 100:.0f}%", _RED),
            ("N do mocy 80%",  f"ok. {n_80}", _WHITE),
        ]
        for label, val, col in rows:
            surface.blit(font_sm.render(label, True, _DIM), (12, y))
            surface.blit(font_md.render(val, True, col), (12, y + 14))
            y += 36
        if power < 0.50:
            warn_rect = pygame.Rect(8, y + 8, _LEFT_W - 16, 68)
            pygame.draw.rect(surface, _DARK_ORANGE_BG, warn_rect, border_radius=4)
            pygame.draw.rect(surface, _ORANGE, warn_rect, 2, border_radius=4)
            font_w = get_font(13)
            d = self._sl_d.value
            lines = [
                "Za małą moc!",
                f"{beta * 100:.0f}% szans że przeoczysz",
                f"prawdziwy efekt d={d:.2f}",
            ]
            wy = y + 12
            for line in lines:
                surface.blit(font_w.render(line, True, _ORANGE), (14, wy))
                wy += 18

    def _draw_matrix(self, right_surf: pygame.Surface) -> None:
        power = self._power()
        beta  = 1.0 - power
        alpha = self._alpha_btn.value
        font_hdr = get_font(15)
        font_big = get_font(28)
        font_sm  = get_font(13)
        font_row = get_font(14)

        title = font_hdr.render(
            "Macierz błędów — konsekwencje Twoich parametrów", True, _DIM
        )
        right_surf.blit(title, (8, 10))

        cell_w = (_RIGHT_W - 120 - 8) // 2
        cell_h = 120
        col_x  = [120, 120 + cell_w + 4]
        row_y  = [50, 50 + cell_h + 4]

        # column headers
        h1 = font_hdr.render("H0 PRAWDZIWE", True, _BLUE)
        h2 = font_hdr.render("H0 FAŁSZYWE", True, _ORANGE)
        right_surf.blit(h1, (col_x[0] + (cell_w - h1.get_width()) // 2, 33))
        right_surf.blit(h2, (col_x[1] + (cell_w - h2.get_width()) // 2, 33))

        # row labels
        rl1 = font_row.render("p < alfa", True, _WHITE)
        rl2 = font_row.render("p >= alfa", True, _WHITE)
        right_surf.blit(rl1, (4, row_y[0] + cell_h // 2 - 8))
        right_surf.blit(rl2, (4, row_y[1] + cell_h // 2 - 8))

        cells = [
            # (col_i, row_i, bg, border, big_val, main_lbl, sub_lbl, eq_lbl)
            (0, 0, (58, 26, 26), _RED,    f"{alpha*100:.0f}%",       "Błąd I rodzaju",   "Fałszywy alarm",   "= alfa"),
            (1, 0, (26, 58, 26), _GREEN,  f"{power*100:.0f}%",       "MOC testu",        "Trafne wykrycie",  "= 1-beta"),
            (0, 1, (20, 20, 50), _PANEL,  f"{(1-alpha)*100:.0f}%",   "Poprawna decyzja", "Brak efektu OK",   "= 1-alfa"),
            (1, 1, _DARK_ORANGE_BG, _ORANGE, f"{beta*100:.0f}%",      "Błąd II rodzaju",  "Przeoczony efekt", "= beta"),
        ]
        for ci, ri, bg, border, big_val, main_lbl, sub_lbl, eq_lbl in cells:
            x = col_x[ci]
            y = row_y[ri]
            cell = pygame.Rect(x, y, cell_w, cell_h)
            pygame.draw.rect(right_surf, bg, cell, border_radius=4)
            bw = 2 if border != _PANEL else 1
            pygame.draw.rect(right_surf, border, cell, bw, border_radius=4)
            text_col = border if border != _PANEL else _DIM
            big = font_big.render(big_val, True, text_col)
            right_surf.blit(big, (x + 8, y + 8))
            right_surf.blit(font_sm.render(main_lbl, True, text_col), (x + 8, y + 44))
            right_surf.blit(font_sm.render(sub_lbl,  True, _MUTED), (x + 8, y + 60))
            right_surf.blit(font_sm.render(eq_lbl,   True, _MUTED), (x + 8, y + 76))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> "Scene | None":
        return None
