from __future__ import annotations

from typing import Callable

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 768
_BG = (10, 10, 26)
_DIM = (100, 100, 130)
_GREEN = (46, 204, 113)
_RED = (231, 76, 60)
_AMBER = (240, 165, 0)
_DURATION_MS = 1500


class PhaseFeedbackScene(Scene):
    def __init__(
        self,
        is_correct: bool,
        score: int,
        answers: list[str],
        mission_type: str,
        next_scene_factory: Callable[[], "Scene | None"],
    ) -> None:
        self._is_correct = is_correct
        self._score = score
        self._answers = answers
        self._mission_type = mission_type
        self._factory = next_scene_factory
        self._timer = 0.0
        self._done = False
        self._next: "Scene | None" = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._advance()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._advance()

    def _advance(self) -> None:
        if self._done:
            return
        self._next = self._factory()
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        if self._done:
            return
        self._timer += dt_ms
        if self._timer >= _DURATION_MS:
            self._advance()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        color = _GREEN if self._is_correct else _RED
        verdict = "Dobrze!" if self._is_correct else "Niestety."
        v_surf = get_font(52).render(verdict, True, color)
        surface.blit(v_surf, (_W // 2 - v_surf.get_width() // 2, 160))

        pts = get_font(28).render(f"+{self._score} pkt", True, _AMBER)
        surface.blit(pts, (_W // 2 - pts.get_width() // 2, 240))

        if not self._is_correct and self._answers:
            hint_lbl = get_font(16).render("Poprawna odpowiedz:", True, _DIM)
            surface.blit(hint_lbl, (_W // 2 - hint_lbl.get_width() // 2, 310))
            answers_str = "  |  ".join(self._answers[:3])
            a_surf = get_font(20).render(answers_str, True, _GREEN)
            surface.blit(a_surf, (_W // 2 - a_surf.get_width() // 2, 340))

        hint = get_font(13).render("SPACJA / klik -- nastepna misja", True, _DIM)
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 40))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> "Scene | None":
        return self._next
