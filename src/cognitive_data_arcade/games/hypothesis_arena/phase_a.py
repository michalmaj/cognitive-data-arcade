# src/cognitive_data_arcade/games/hypothesis_arena/phase_a.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pygame
from scipy import stats as sp_stats

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.context_popup import ContextInfo, ContextPopup
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.hypothesis_arena.simulator import (
    TwoGroupResult, compute_power, generate_two_groups, strength_label,
)
from cognitive_data_arcade.games.hypothesis_arena.widgets import _AlphaButtons, _FloatSlider

_BG     = (15,  15,  35)
_PANEL  = (18,  18,  42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156,  18)
_BLUE   = ( 52, 152, 219)
_GREEN  = ( 39, 174,  96)
_RED    = (231,  76,  60)
_TRACK  = ( 42,  42,  80)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"

_LEFT_W   = 340
_AREA_H   = 672
_CHART_W  = 660
_SCROLL_H = 920
_DPI      = 100
_N_SIM    = 1000

_POPUPS_A: dict[str, ContextInfo] = {
    "slider_n": ContextInfo(
        title="N na grupe",
        body="Liczba uczestnikow w kazdej z dwoch grup. Wieksze N -> mniejszy blad standardowy -> latwiej wykryc efekt.",
        impact="Przesun N do 300 przy d=0.10 — p spadnie ponizej 0.05 mimo trywialnego efektu!",
    ),
    "slider_d": ContextInfo(
        title="Cohen's d — prawdziwy rozmiar efektu",
        body="d = roznica srednich / odchylenie pooled. Skala: <0.10 pomijalny, 0.10-0.30 maly, 0.30-0.50 sredni, 0.50-0.80 duzy.",
        impact="d=0.10 to efekt realny, ale w praktyce bez znaczenia klinicznego.",
    ),
    "alpha_btn": ContextInfo(
        title="Poziom istotnosci alfa",
        body="Prawdopodobienstwo bledu I rodzaju — odrzucenia H0 gdy jest prawdziwa. alfa=0.05 to konwencja, nie prawo natury.",
        impact="alfa=0.01 zmniejsza falszywe alarmy, ale zwieksza przeoczenia (blad II rodzaju).",
    ),
    "chart_curves": ContextInfo(
        title="Rozklady populacji — wizualizacja efektu",
        body="Niebieska krzywa = kontrola, pomaranczowa = interwencja. Strzalka d pokazuje odleglosc miedzy srednimi w jednostkach SD.",
        impact="Male d oznacza duze nakladanie sie rozkladow — ciezko odroznic grupy.",
    ),
    "chart_dots": ContextInfo(
        title="Proba — dane z biezacego eksperymentu",
        body="Losowa proba o zadanym N z populacji o zadanym d. Kazde odswiezenie losuje nowa probe.",
        impact="Przy malym N wyniki sa bardzo zmienne — p zmienia sie drastycznie miedzy probami.",
    ),
    "chart_hist": ContextInfo(
        title="Histogram p-value z 1000 symulacji",
        body="Dystrybucja p-value po 1000 niezaleznych eksperymentach o tym samym N i d. Czerwony slupek = p < alfa.",
        impact="Przy d=0 histogram powinien byc jednostajny (kazde p rownie prawdopodobne).",
    ),
    "stats_block": ContextInfo(
        title="Blok statystyk",
        body="t-stat: obserwowana statystyka testowa. Moc: prawdopodobienstwo wykrycia efektu o tym d przy tym N i alfa.",
        impact="Moc < 50% oznacza ze badanie jest za slabe — czesciej przeoczysz efekt niz go wykryjesz.",
    ),
}


def _gauss(x: float, mu: float, sigma: float) -> float:
    return float(np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi)))


def _style_ax(ax) -> None:
    ax.tick_params(colors="#787890", labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a2a50")


class PhaseAScene(Scene):
    def __init__(self) -> None:
        self._done = False
        x0, w = 16, _LEFT_W - 32
        self._sl_n = _FloatSlider("N na grupe", 10, 500, 50, 10, x0, 60, w, fmt=".0f")
        self._sl_d = _FloatSlider("Cohen's d (prawdziwy)", 0.0, 1.0, 0.50, 0.05, x0, 128, w)
        self._alpha_btn = _AlphaButtons(x0, 222, 80, 28)
        self._result: TwoGroupResult | None = None
        self._chart_surf: pygame.Surface | None = None
        self._scroll_y = 0
        self._popup = ContextPopup()
        self._register_popups()
        self._regenerate()

    def _max_scroll(self) -> int:
        return max(0, _SCROLL_H - _AREA_H)

    def _register_popups(self) -> None:
        self._popup.clear()
        self._popup.register(self._sl_n.rect, _POPUPS_A["slider_n"])
        self._popup.register(self._sl_d.rect, _POPUPS_A["slider_d"])
        self._popup.register(self._alpha_btn.rect, _POPUPS_A["alpha_btn"])
        stats_rect = pygame.Rect(8, 290, _LEFT_W - 16, 130)
        self._popup.register(stats_rect, _POPUPS_A["stats_block"])
        sy = self._scroll_y
        chart_h_each = (_SCROLL_H - 20) // 3
        for i, key in enumerate(["chart_curves", "chart_dots", "chart_hist"]):
            y0 = i * chart_h_each + 6 - sy
            rect = pygame.Rect(_LEFT_W + 4, y0, _CHART_W, chart_h_each - 8)
            self._popup.register(rect, _POPUPS_A[key])

    def _regenerate(self) -> None:
        n = int(self._sl_n.value)
        d = self._sl_d.value
        self._result = generate_two_groups(n=n, true_d=d, seed=None)
        self._chart_surf = self._render_charts(n, d)

    def _render_charts(self, n: int, d: float) -> pygame.Surface:
        alpha = self._alpha_btn.value
        fig = plt.figure(
            figsize=(_CHART_W / _DPI, _SCROLL_H / _DPI),
            dpi=_DPI,
            facecolor=_FIG_BG,
        )
        axs = fig.subplots(3, 1)
        fig.subplots_adjust(left=0.08, right=0.97, top=0.97, bottom=0.03, hspace=0.55)

        # Chart 1: overlapping normal curves
        ax1 = axs[0]
        ax1.set_facecolor(_AX_BG)
        xs = np.linspace(-4, 4 + d, 400)
        ax1.fill_between(xs, 0, [_gauss(x, 0, 1) for x in xs],
                         alpha=0.35, color="#3498db", label="Kontrola")
        ax1.fill_between(xs, 0, [_gauss(x, d, 1) for x in xs],
                         alpha=0.35, color="#f39c12", label="Interwencja")
        ax1.axvline(0, color="#3498db", lw=1, ls="--")
        ax1.axvline(d, color="#f39c12", lw=1, ls="--")
        if abs(d) > 0.01:
            mid_y = _gauss(d / 2, d / 2, 1) * 1.1
            ax1.annotate("", xy=(d, mid_y), xytext=(0, mid_y),
                         arrowprops=dict(arrowstyle="<->", color="white", lw=1.2))
            ax1.text(d / 2, mid_y + 0.02, f"d={d:.2f}",
                     ha="center", color="white", fontsize=8)
        ax1.legend(fontsize=8, facecolor=_FIG_BG, labelcolor="white", framealpha=0.5)
        ax1.set_title("Rozklady populacji", color="white", fontsize=9)
        _style_ax(ax1)

        # Chart 2: dot plot of sample
        ax2 = axs[1]
        ax2.set_facecolor(_AX_BG)
        if self._result is not None:
            rng = np.random.default_rng(7)
            jit = rng.uniform(-0.15, 0.15, n)
            ax2.scatter(jit,       self._result.x_ctrl,  s=12, alpha=0.6, color="#3498db")
            ax2.scatter(jit + 1.0, self._result.x_treat, s=12, alpha=0.6, color="#f39c12")
            ax2.hlines(self._result.x_ctrl.mean(),  -0.25, 0.25, colors="#3498db", lw=2)
            ax2.hlines(self._result.x_treat.mean(),  0.75, 1.25, colors="#f39c12", lw=2)
            ax2.set_xticks([0, 1])
            ax2.set_xticklabels(
                [f"Kontrola\nN={n}", f"Interwencja\nN={n}"],
                color="white", fontsize=8,
            )
        ax2.set_title("Dane z biezacej proby", color="white", fontsize=9)
        _style_ax(ax2)

        # Chart 3: p-value histogram
        ax3 = axs[2]
        ax3.set_facecolor(_AX_BG)
        rng2 = np.random.default_rng(99)
        p_vals = []
        for _ in range(_N_SIM):
            c  = rng2.standard_normal(n)
            t_ = rng2.standard_normal(n) + d
            _, pv = sp_stats.ttest_ind(c, t_)
            p_vals.append(pv)
        p_arr = np.array(p_vals)
        bins = np.linspace(0, 1, 11)
        counts, _ = np.histogram(p_arr, bins=bins)
        bar_colors = ["#e74c3c" if b < alpha else "#3a3a70" for b in bins[:-1]]
        ax3.bar(bins[:-1], counts, width=0.1, align="edge",
                color=bar_colors, edgecolor="#0f0f23", lw=0.5)
        ax3.axvline(alpha, color="#e74c3c", lw=1.5, ls="--")
        ax3.text(alpha + 0.01, counts.max() * 0.9, f"alfa={alpha}",
                 color="#e74c3c", fontsize=8)
        pct = 100 * (p_arr < alpha).mean()
        ax3.text(0.98, 0.92, f"{pct:.0f}% istotnych",
                 transform=ax3.transAxes, ha="right", color="white", fontsize=8)
        ax3.set_xlabel("p-value", color="#787890", fontsize=8)
        ax3.set_title("Histogram p-value (1000 symulacji)", color="white", fontsize=9)
        _style_ax(ax3)

        surf = figure_to_surface(fig, (_CHART_W, _SCROLL_H))
        return surf

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
            self._regenerate()
            self._register_popups()

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _LEFT_W, _AREA_H))

        # header
        surface.blit(get_font(20).render("Parametry", True, _ORANGE), (16, 16))

        self._sl_n.draw(surface)
        self._sl_d.draw(surface)
        self._alpha_btn.draw(surface)

        if self._result is not None:
            self._draw_stats(surface)

        if self._chart_surf is not None:
            surface.blit(self._chart_surf, (_LEFT_W, -self._scroll_y))

        if self._max_scroll() > 0:
            hint = get_font(13).render("kolko myszy = przewijanie", True, _TRACK)
            surface.blit(hint, (_LEFT_W + 8, _AREA_H - 18))

        self._popup.draw(surface)

    def _draw_stats(self, surface: pygame.Surface) -> None:
        r = self._result
        alpha = self._alpha_btn.value
        power = compute_power(int(self._sl_n.value), self._sl_d.value, alpha)
        font_sm = get_font(14)
        font_md = get_font(17)

        p_color = _RED if r.p_value < alpha else _GREEN
        rows = [
            ("p-value",    f"{r.p_value:.4f}", p_color),
            ("Cohen's d",  f"{r.cohens_d:.3f}  ({strength_label(r.cohens_d)})", _WHITE),
            ("t-stat",     f"{r.t_stat:.3f}", _WHITE),
            ("Moc testu",  f"{power * 100:.0f}%", _ORANGE if power < 0.8 else _GREEN),
        ]
        y = 294
        for label, val, col in rows:
            surface.blit(font_sm.render(label, True, _DIM), (12, y))
            surface.blit(font_md.render(val, True, col), (12, y + 14))
            y += 36

        # trap warning
        if r.p_value < alpha and abs(r.cohens_d) < 0.20:
            warn_rect = pygame.Rect(8, y + 4, _LEFT_W - 16, 58)
            pygame.draw.rect(surface, (58, 26, 26), warn_rect, border_radius=4)
            pygame.draw.rect(surface, _RED, warn_rect, 2, border_radius=4)
            font_w = get_font(13)
            lines = [
                "Pulapka!",
                f"p={r.p_value:.3f} ale d={r.cohens_d:.2f} (trywialny)",
                "Stat. istotne != wazne klinicznie!",
            ]
            wy = y + 8
            for line in lines:
                surface.blit(font_w.render(line, True, _RED), (14, wy))
                wy += 16

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> None:
        return None
