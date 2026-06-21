"""Generic SPACE-to-advance interlude for Bias Blind Spot."""

from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState

_W, _H = 1024, 720
_BG = (8, 12, 20)


class PhaseInterludeScene(Scene):
    """Show configurable lines then advance to next phase on SPACE.

    Args:
        state:     shared GameState.
        lines:     list of (text, color) tuples to display.
        next_act:  "engineer" | "regulator" — determines which scene to spawn next.
    """

    def __init__(
        self,
        state: GameState,
        lines: list[tuple[str, tuple[int, int, int]]],
        next_act: str,
    ) -> None:
        self._state = state
        self._lines = lines
        self._next_act = next_act
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._advance()

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def _advance(self) -> None:
        if self._done:
            return
        self._done = True
        if self._next_act == "engineer":
            from cognitive_data_arcade.games.bias_blind_spot.phase_engineer import (
                PhaseEngineerScene,
            )

            self._next = PhaseEngineerScene(self._state)
        else:
            from cognitive_data_arcade.games.bias_blind_spot.phase_regulator import (
                PhaseRegulatorScene,
            )

            self._next = PhaseRegulatorScene(self._state)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        y = _H // 2 - len(self._lines) * 24
        for text, color in self._lines:
            if text:
                surf = get_font(20).render(text, True, color)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 48
        hint = get_font(13).render("SPACJA aby kontynuowac", True, (80, 80, 100))
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 54))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
