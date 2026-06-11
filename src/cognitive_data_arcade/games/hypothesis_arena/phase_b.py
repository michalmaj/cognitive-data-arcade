# src/cognitive_data_arcade/games/hypothesis_arena/phase_b.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.hypothesis_arena.simulator import (
    TwoGroupResult, _SCENARIOS, compute_power, generate_two_groups,
    min_n_for_power, strength_label,
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
_FIG_BG = "#0f0f23"

_TOP_H  = 80
_AREA_H = 672
_AREA_W = 1024
_SCAT_W = 570
_CTRL_W = _AREA_W - _SCAT_W  # 454
_SCAT_H = _AREA_H - _TOP_H   # 592
_DPI    = 100


def _make_n_slider(x: int, y: int, w: int, max_n: int) -> _FloatSlider:
    default = min(30, max_n)
    return _FloatSlider("N na grupę", 10, max_n, default, 10, x, y, w, fmt=".0f")


class PhaseBScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._scenario_idx = 0
        self._state = "waiting"
        self._result: TwoGroupResult | None = None
        self._chart_surf: pygame.Surface | None = None
        self._score = 0
        cx = _SCAT_W + 16
        cw = _CTRL_W - 32
        self._sl_n = _make_n_slider(cx, _TOP_H + 56, cw, _SCENARIOS[0].max_n)
        self._alpha_btn = _AlphaButtons(cx, _TOP_H + 144, 80, 28)

    @property
    def _scenario(self):
        return _SCENARIOS[self._scenario_idx]

    def _run_experiment(self) -> None:
        sc = self._scenario
        n = int(self._sl_n.value)
        alpha = self._alpha_btn.value
        self._result = generate_two_groups(n=n, true_d=sc.true_d, seed=sc.seed + n)
        self._chart_surf = self._render_scatter(n, alpha)
        self._state = "revealed"

    def _render_scatter(self, n: int, alpha: float) -> pygame.Surface:
        r = self._result
        fig, ax = plt.subplots(
            figsize=(_SCAT_W / _DPI, _SCAT_H / _DPI), dpi=_DPI, facecolor=_FIG_BG
        )
        ax.set_facecolor("#1a1a3e")
        if r is not None:
            rng = np.random.default_rng(12)
            jit = rng.uniform(-0.18, 0.18, n)
            ax.scatter(jit,       r.x_ctrl,  s=14, alpha=0.6, color="#3498db", label="Kontrola")
            ax.scatter(jit + 1.0, r.x_treat, s=14, alpha=0.6, color="#f39c12", label="Interwencja")
            ax.hlines(r.x_ctrl.mean(),  -0.28, 0.28, colors="#3498db", lw=2.5)
            ax.hlines(r.x_treat.mean(),  0.72, 1.28, colors="#f39c12", lw=2.5)
            ax.set_xticks([0, 1])
            ax.set_xticklabels(
                [f"Kontrola\nN={n}", f"Interwencja\nN={n}"],
                color="white", fontsize=9,
            )
            p_color = "#e74c3c" if r.p_value < alpha else "#27ae60"
            ax.text(0.98, 0.97, f"p = {r.p_value:.4f}",
                    transform=ax.transAxes, ha="right", va="top",
                    color=p_color, fontsize=11, fontweight="bold")
        ax.legend(fontsize=9, facecolor=_FIG_BG, labelcolor="white", framealpha=0.5)
        ax.tick_params(colors="#787890", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a50")
        surf = figure_to_surface(fig, (_SCAT_W, _SCAT_H))
        return surf

    def _power(self) -> float:
        return compute_power(
            int(self._sl_n.value), self._scenario.true_d, self._alpha_btn.value
        )

    def _is_well_designed(self) -> bool:
        r = self._result
        alpha = self._alpha_btn.value
        sc = self._scenario
        if sc.true_d == 0.0:
            return r is not None and r.p_value >= alpha
        return self._power() >= 0.80

    def _feedback(self) -> tuple[str, tuple]:
        r = self._result
        alpha = self._alpha_btn.value
        sc = self._scenario
        power = self._power()
        pct = f"{power * 100:.0f}%"
        if sc.true_d == 0.0:
            if r.p_value >= alpha:
                return "Poprawnie — brak efektu, brak istotności", _GREEN
            return "Fałszywy alarm! d=0.00 ale p<alfa", _RED
        if r.p_value < alpha and abs(r.cohens_d) < 0.20:
            return "Pułapka! p<alfa ale d trywialny", _RED
        if power >= 0.80:
            return f"Dobrze zaprojektowany eksperyment (moc {pct})", _GREEN
        if power >= 0.50:
            return f"Moc brzegowa ({pct}) — ryzykowny projekt", _ORANGE
        return f"Za mała moc ({pct}) — prawdziwy efekt przeoczony", _RED

    def _advance(self) -> None:
        if self._is_well_designed():
            self._score += 1
        if self._scenario_idx < len(_SCENARIOS) - 1:
            self._scenario_idx += 1
        else:
            self._scenario_idx = 0
            self._score = 0
        self._state = "waiting"
        self._result = None
        self._chart_surf = None
        cx = _SCAT_W + 16
        cw = _CTRL_W - 32
        self._sl_n = _make_n_slider(cx, _TOP_H + 56, cw, self._scenario.max_n)

    def handle_event(self, event: pygame.event.Event) -> None:
        changed = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # run button
            run_rect = pygame.Rect(_SCAT_W + 16, _TOP_H + 188, _CTRL_W - 32, 36)
            if run_rect.collidepoint(pos):
                self._run_experiment()
                return
            # next/restart button (only in revealed state)
            if self._state == "revealed":
                btn_rect = pygame.Rect(_SCAT_W + 16, _TOP_H + 426, _CTRL_W - 32, 36)
                if btn_rect.collidepoint(pos):
                    self._advance()
                    return
            # slider
            if self._sl_n.handle_mousedown(pos):
                changed = True
        elif event.type == pygame.MOUSEMOTION:
            if self._sl_n.handle_mousemotion(event.pos, event.buttons):
                changed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._sl_n._dragging = False
        if self._alpha_btn.handle_event(event):
            changed = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_top_bar(surface)
        if self._state == "waiting":
            self._draw_waiting(surface)
        else:
            if self._chart_surf:
                surface.blit(self._chart_surf, (0, _TOP_H))
        self._draw_controls(surface)
        if self._state == "revealed" and self._result is not None:
            self._draw_verdict(surface)

    def _draw_top_bar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL, (0, 0, _AREA_W, _TOP_H))
        sc = self._scenario
        font_sm = get_font(13)
        font_lg = get_font(20)
        counter = f"Scenariusz {self._scenario_idx + 1} / {len(_SCENARIOS)}"
        surface.blit(font_sm.render(counter, True, _ORANGE), (12, 6))
        surface.blit(font_lg.render(sc.title_pl, True, _WHITE), (12, 22))
        ctx = sc.context_pl[:88]
        surface.blit(font_sm.render(ctx, True, _DIM), (12, 54))
        chip = font_sm.render(f"max N = {sc.max_n}", True, _DIM)
        surface.blit(chip, (_AREA_W - chip.get_width() - 12, 18))

    def _draw_waiting(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (20, 20, 50), (0, _TOP_H, _SCAT_W, _SCAT_H))
        font = get_font(17)
        msg = "Uruchom eksperyment żeby zobaczyć dane"
        tw = font.size(msg)[0]
        surface.blit(
            font.render(msg, True, _DIM),
            (_SCAT_W // 2 - tw // 2, _TOP_H + _SCAT_H // 2),
        )

    def _draw_controls(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL, (_SCAT_W, _TOP_H, _CTRL_W, _SCAT_H))
        hdr = get_font(17).render("Zaprojektuj eksperyment", True, _BLUE)
        surface.blit(hdr, (_SCAT_W + 16, _TOP_H + 16))
        self._sl_n.draw(surface)
        self._alpha_btn.draw(surface)
        # run button
        run_rect = pygame.Rect(_SCAT_W + 16, _TOP_H + 188, _CTRL_W - 32, 36)
        pygame.draw.rect(surface, (26, 42, 26), run_rect, border_radius=4)
        pygame.draw.rect(surface, _GREEN, run_rect, 2, border_radius=4)
        lbl = get_font(17).render("Uruchom eksperyment", True, _GREEN)
        lw = lbl.get_width()
        surface.blit(lbl, (_SCAT_W + 16 + (_CTRL_W - 32 - lw) // 2, _TOP_H + 198))

    def _draw_verdict(self, surface: pygame.Surface) -> None:
        r = self._result
        alpha = self._alpha_btn.value
        power = self._power()
        n_80 = min_n_for_power(0.80, self._scenario.true_d, alpha)
        font_sm = get_font(14)
        font_md = get_font(17)
        y = _TOP_H + 238
        rows = [
            ("p-value",     f"{r.p_value:.4f}", _GREEN if r.p_value >= alpha else _RED),
            ("Cohen's d",   f"{r.cohens_d:.3f} ({strength_label(r.cohens_d)})", _WHITE),
            ("Moc testu",   f"{power * 100:.0f}%", _GREEN if power >= 0.80 else _ORANGE),
            ("N do mocy 80%", f"ok. {n_80}", _WHITE),
        ]
        for label, val, col in rows:
            surface.blit(font_sm.render(label, True, _DIM), (_SCAT_W + 16, y))
            surface.blit(font_md.render(val, True, col), (_SCAT_W + 16, y + 14))
            y += 34
        # feedback
        msg, col = self._feedback()
        fb_rect = pygame.Rect(_SCAT_W + 16, y + 4, _CTRL_W - 32, 56)
        bg = (58, 26, 26) if col == _RED else ((26, 42, 26) if col == _GREEN else (58, 42, 16))
        pygame.draw.rect(surface, bg, fb_rect, border_radius=4)
        pygame.draw.rect(surface, col, fb_rect, 2, border_radius=4)
        surface.blit(font_sm.render(msg, True, col), (_SCAT_W + 22, y + 14))
        # next/restart button
        is_last = self._scenario_idx == len(_SCENARIOS) - 1
        btn_lbl = "Zagraj ponownie" if is_last else "Dalej"
        btn_rect = pygame.Rect(_SCAT_W + 16, _TOP_H + 426, _CTRL_W - 32, 36)
        pygame.draw.rect(surface, _PANEL, btn_rect, border_radius=4)
        pygame.draw.rect(surface, _BLUE, btn_rect, 2, border_radius=4)
        tw = get_font(17).size(btn_lbl)[0]
        surface.blit(
            get_font(17).render(btn_lbl, True, _BLUE),
            (_SCAT_W + 16 + (_CTRL_W - 32 - tw) // 2, _TOP_H + 436),
        )
        # score
        score_txt = f"Wynik: {self._score} / {len(_SCENARIOS)}"
        surface.blit(
            get_font(14).render(score_txt, True, _DIM),
            (_SCAT_W + 16, _TOP_H + _SCAT_H - 30),
        )

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> "Scene | None":
        return None
