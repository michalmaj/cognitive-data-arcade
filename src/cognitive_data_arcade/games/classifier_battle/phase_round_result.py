from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.classifier_battle.scenarios import Scenario

_BG    = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM   = (120, 120, 160)
_RED   = (231, 76, 60)
_BLUE  = (52, 152, 219)
_GREEN = (39, 174, 96)
_YELLOW = (243, 156, 18)
_PURPLE = (155, 89, 182)
_ORANGE = (230, 126, 34)

_W, _H = 1024, 720
_TOP_H = 40
_LEFT_W = 520
_DOT_R = 5
_TOTAL_ROUNDS = 5

_CLF_COLORS = {
    "liniowy": _GREEN,
    "knn": _PURPLE,
    "drzewo": _ORANGE,
}
_CLF_NAMES = {
    "liniowy": "Liniowy",
    "knn": "KNN",
    "drzewo": "Drzewo",
}


@dataclass
class RoundDisplay:
    scenario: Scenario
    player_acc: float
    clf_accs: dict[str, float]
    score: int
    polyline_norm: list[tuple[float, float]]
    X: np.ndarray
    y: np.ndarray


def _wrap_text(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class PhaseRoundResultScene(Scene):
    def __init__(
        self,
        display: RoundDisplay,
        round_idx: int,
        session_seed: int,
        session_score: int,
        round_results: list[dict],
    ) -> None:
        self._display = display
        self._round_idx = round_idx
        self._session_seed = session_seed
        self._session_score = session_score
        self._round_results = round_results
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._btn_rect().collidepoint(event.pos):
                self._advance()

    def _btn_rect(self) -> pygame.Rect:
        return pygame.Rect(_W // 2 - 130, _H - 62, 260, 44)

    def _advance(self) -> None:
        is_last = self._round_idx >= _TOTAL_ROUNDS - 1
        if is_last:
            from cognitive_data_arcade.games.classifier_battle.phase_session_result import PhaseSessionResultScene
            self._next = PhaseSessionResultScene(
                session_score=self._session_score,
                round_results=self._round_results,
            )
        else:
            from cognitive_data_arcade.games.classifier_battle.phase_draw import PhaseDrawScene
            from cognitive_data_arcade.games.classifier_battle.scenarios import SCENARIOS
            next_idx = self._round_idx + 1
            self._next = PhaseDrawScene(
                scenario=SCENARIOS[next_idx],
                round_idx=next_idx,
                session_seed=self._session_seed,
                session_score=self._session_score,
                round_results=self._round_results,
            )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        d = self._display

        # Top strip
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _TOP_H))
        strip = get_font(18).render(
            f"Runda {self._round_idx + 1}/{_TOTAL_ROUNDS}  —  {d.scenario.name_pl}  —  Wyniki",
            True, _WHITE,
        )
        surface.blit(strip, (_W // 2 - strip.get_width() // 2, 10))

        # Left panel: scatter replay
        left_rect = pygame.Rect(0, _TOP_H, _LEFT_W, _H - _TOP_H - 70)
        pygame.draw.rect(surface, _PANEL, left_rect)
        self._draw_scatter(surface, left_rect, d)

        # Right panel
        right_x = _LEFT_W + 8
        right_w = _W - right_x - 8
        self._draw_right(surface, right_x, right_w, d)

        # Button
        btn = self._btn_rect()
        btn_label = "Następna runda" if self._round_idx < _TOTAL_ROUNDS - 1 else "Zakończ"
        pygame.draw.rect(surface, _PANEL, btn, border_radius=6)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=6)
        lbl = get_font(18).render(btn_label, True, _BLUE)
        surface.blit(lbl, (btn.centerx - lbl.get_width() // 2, btn.centery - lbl.get_height() // 2))

    def _draw_scatter(self, surface: pygame.Surface, rect: pygame.Rect,
                      d: RoundDisplay) -> None:
        # Compute misclassified mask
        if d.polyline_norm:
            from cognitive_data_arcade.games.classifier_battle.classifier import predict_labels
            pred = predict_labels(d.polyline_norm, d.X, d.y)
            misclassified = pred != d.y
        else:
            misclassified = np.zeros(len(d.X), dtype=bool)

        # Draw points
        for i, (x, y) in enumerate(d.X):
            cx = int(rect.x + x * rect.w)
            cy = int(rect.y + y * rect.h)
            color = (231, 76, 60) if d.y[i] == 0 else (52, 152, 219)
            pygame.draw.circle(surface, color, (cx, cy), _DOT_R)
            if misclassified[i]:
                font = get_font(11)
                xlbl = font.render("x", True, (255, 255, 255))
                surface.blit(xlbl, (cx - xlbl.get_width() // 2, cy - xlbl.get_height() // 2))

        # Draw boundary polyline
        if len(d.polyline_norm) >= 2:
            pts = [(int(rect.x + nx * rect.w), int(rect.y + ny * rect.h))
                   for nx, ny in d.polyline_norm]
            pygame.draw.lines(surface, _YELLOW, False, pts, 2)

    def _draw_right(self, surface: pygame.Surface, rx: int, rw: int,
                    d: RoundDisplay) -> None:
        y = _TOP_H + 12
        acc_label = get_font(14).render("Dokładność klasyfikacji:", True, _DIM)
        surface.blit(acc_label, (rx, y))
        y += 24

        bar_max_w = rw - 80
        rows = [("Ty", d.player_acc, _YELLOW)] + [
            (_CLF_NAMES[k], v, _CLF_COLORS[k])
            for k, v in d.clf_accs.items()
        ]
        for name, acc, color in rows:
            name_lbl = get_font(13).render(name, True, color)
            surface.blit(name_lbl, (rx, y))
            bar_rect = pygame.Rect(rx + 60, y + 2, int(bar_max_w * acc), 14)
            pygame.draw.rect(surface, color, bar_rect, border_radius=3)
            pct = get_font(12).render(f"{acc:.0%}", True, color)
            surface.blit(pct, (rx + 62 + bar_max_w, y + 1))
            y += 28

        y += 10
        pygame.draw.line(surface, _DIM, (rx, y), (rx + rw, y))
        y += 8

        font = get_font(13)
        for line in _wrap_text(d.scenario.insight_pl, font, rw - 4):
            surf = font.render(line, True, _DIM)
            surface.blit(surf, (rx, y))
            y += 20

        y += 16
        score_col = _GREEN if d.score >= 100 else (_YELLOW if d.score >= 70 else _RED)
        score_surf = get_font(32).render(f"+{d.score} pkt", True, score_col)
        surface.blit(score_surf, (rx + rw // 2 - score_surf.get_width() // 2, y))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
