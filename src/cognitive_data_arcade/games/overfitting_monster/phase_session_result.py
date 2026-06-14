# src/cognitive_data_arcade/games/overfitting_monster/phase_session_result.py
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_BG     = (15, 15, 35)
_PANEL  = (18, 18, 42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_GREEN  = (39, 174, 96)
_ORANGE = (243, 156, 18)
_RED    = (231, 76, 60)
_BLUE   = (52, 152, 219)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"

_W, _H = 1024, 720

_STAR_COLORS = {3: "#2ecc71", 2: "#f39c12", 1: "#e74c3c"}


def _star_ascii(stars: int) -> str:
    mapping = {3: "xxx", 2: "xx.", 1: "x.."}
    return mapping.get(stars, "x..")


class PhaseSessionResultScene(Scene):
    def __init__(self, session_score: int, round_results: list[dict]) -> None:
        self._session_score = session_score
        self._round_results = round_results
        self._done = False
        self._next: Scene | None = None
        self._chart_surf = self._render_chart()

    def _render_chart(self) -> pygame.Surface:
        labels = [f"R{r['round_idx'] + 1}" for r in self._round_results]
        test_accs = [r["test_acc"] * 100 for r in self._round_results]
        bar_colors = [_STAR_COLORS[r["stars"]] for r in self._round_results]

        fig, ax = plt.subplots(figsize=(7, 2.5), dpi=96, facecolor=_FIG_BG)
        ax.set_facecolor(_AX_BG)
        bars = ax.bar(labels, test_accs, color=bar_colors, width=0.5)
        ax.set_ylim(0, 105)
        ax.set_ylabel("Test accuracy (%)", color="#787890", fontsize=8)
        ax.tick_params(colors="#787890", labelsize=8)
        for bar, r in zip(bars, self._round_results):
            # matplotlib renders Unicode stars fine (its own font system)
            star_str = "★" * r["stars"] + "☆" * (3 - r["stars"])
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    star_str, ha="center", va="bottom", fontsize=7,
                    color=_STAR_COLORS[r["stars"]])
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a50")
        return figure_to_surface(fig, (672, 240))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            btn = pygame.Rect(_W // 2 - 130, _H - 62, 260, 44)
            if btn.collidepoint(event.pos):
                from cognitive_data_arcade.games.overfitting_monster.phase_intro import (
                    PhaseIntroScene,
                )
                self._next = PhaseIntroScene()
                self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        # ASCII hyphen instead of em-dash (pygame Unicode bug)
        title = get_font(22).render("Wyniki sesji - Overfitting Monster", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        # Total score
        score_col = (_GREEN if self._session_score >= 450
                     else _ORANGE if self._session_score >= 300 else _RED)
        score_surf = get_font(36).render(str(self._session_score), True, score_col)
        surface.blit(score_surf, (_W // 2 - score_surf.get_width() // 2, 68))
        pts = get_font(14).render("punktow", True, _DIM)
        surface.blit(pts, (_W // 2 - pts.get_width() // 2, 112))

        # Chart
        if self._chart_surf:
            surface.blit(self._chart_surf, (_W // 2 - 336, 136))

        # Table header
        y = 396
        hdr = get_font(12).render(
            "  Runda   Scenariusz              k   Split   Test     Gap    Wynik",
            True, _DIM,
        )
        surface.blit(hdr, (20, y))
        y += 18

        for r in self._round_results:
            # ASCII stars (pygame Unicode bug - cannot render actual star characters)
            star_str = _star_ascii(r["stars"])
            row = get_font(12).render(
                f"    {r['round_idx'] + 1}       {r['scenario_name']:<20}  "
                f"{r['k']:>2}   {r['split_pct']}%   {r['test_acc']:.0%}   "
                f"{r['gap']:+.1f}pp   {r['score']}  {star_str}",
                True, _WHITE,
            )
            surface.blit(row, (20, y))
            y += 18

        # Replay button
        btn = pygame.Rect(_W // 2 - 130, _H - 62, 260, 44)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=6)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=6)
        lbl = get_font(18).render("Zagraj ponownie", True, _BLUE)
        surface.blit(lbl, (btn.centerx - lbl.get_width() // 2, btn.centery - lbl.get_height() // 2))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
