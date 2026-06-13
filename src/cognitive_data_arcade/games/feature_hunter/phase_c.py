from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_BG    = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM   = (120, 120, 160)
_ORANGE = (243, 156, 18)
_GREEN = (39, 174, 96)
_RED   = (231, 76, 60)
_BLUE  = (52, 152, 219)
_FIG_BG = "#0f0f23"
_AX_BG  = "#1a1a3e"
_W, _H = 1024, 720

_MSG_GREEN  = "Świetna intuicja! Cechy z wyraźnym trendem rzeczywiście pomagają modelom."
_MSG_ORANGE = "Nieźle! Słabe korelacje są trudne do wychwycenia — modele też mają z tym problem."
_MSG_RED    = "Selekcja cech jest trudna! Sprawdź, które cechy cię zaskoczyły."


class PhaseCScene(Scene):
    def __init__(
        self,
        session_score: int,
        round_results: list[tuple[int, int, int]],  # (correct, total, score) per round
    ) -> None:
        self._session_score = session_score
        self._round_results = round_results
        self._done = False
        self._next: Scene | None = None
        self._chart_surf = self._render_bar_chart()

    def _render_bar_chart(self) -> pygame.Surface:
        rounds = [f"R{i+1}" for i in range(len(self._round_results))]
        scores = [r[2] for r in self._round_results]
        fig, ax = plt.subplots(figsize=(6, 2), dpi=100, facecolor=_FIG_BG)
        ax.set_facecolor(_AX_BG)
        ax.bar(rounds, scores, color="#f39c12", width=0.5)
        ax.set_ylim(0, max(scores or [1]) * 1.25)
        ax.tick_params(colors="#787890", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a50")
        return figure_to_surface(fig, (600, 200))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            btn = pygame.Rect(_W // 2 - 120, _H - 70, 240, 44)
            if btn.collidepoint(event.pos):
                from cognitive_data_arcade.games.feature_hunter.phase_a import PhaseAScene
                self._next = PhaseAScene()
                self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 60))

        title = get_font(24).render("Wyniki sesji — Feature Hunter", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        total_rounds = len(self._round_results)
        mean_acc = (
            sum(r[0] / r[1] for r in self._round_results) / total_rounds
            if total_rounds > 0 else 0.0
        )
        score_col = _GREEN if self._session_score >= 300 else (_ORANGE if self._session_score >= 150 else _RED)
        score_surf = get_font(36).render(str(self._session_score), True, score_col)
        surface.blit(score_surf, (_W // 2 - score_surf.get_width() // 2, 74))
        pts_surf = get_font(14).render("punktów", True, _DIM)
        surface.blit(pts_surf, (_W // 2 - pts_surf.get_width() // 2, 118))

        # Round table
        font = get_font(14)
        header = font.render("Runda   Poprawne   Wynik rundy", True, _DIM)
        surface.blit(header, (120, 158))
        for i, (correct, total, score) in enumerate(self._round_results):
            col = _GREEN if correct == total else (_ORANGE if correct >= total - 1 else _RED)
            row = get_font(14).render(
                f"  {i+1}       {correct}/{total}         {score} pkt", True, col
            )
            surface.blit(row, (120, 182 + i * 22))

        # Bar chart
        if self._chart_surf:
            surface.blit(self._chart_surf, (_W // 2 - 300, 296))

        # Educational message
        msg = _MSG_GREEN if mean_acc >= 0.80 else (_MSG_ORANGE if mean_acc >= 0.60 else _MSG_RED)
        msg_surf = get_font(13).render(msg, True, _DIM)
        surface.blit(msg_surf, (_W // 2 - msg_surf.get_width() // 2, 516))

        # Replay button
        btn = pygame.Rect(_W // 2 - 120, _H - 70, 240, 44)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=6)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=6)
        btn_lbl = get_font(18).render("Zagraj ponownie", True, _BLUE)
        surface.blit(btn_lbl, (_W // 2 - btn_lbl.get_width() // 2, _H - 58))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
