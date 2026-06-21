# src/cognitive_data_arcade/games/architects_trial/phase_intro.py
from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.architects_trial.game_state import GameState

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    PURPLE as _PURPLE,
)

_W, _H = 1024, 720

# (text, color, t_show_ms, font_size)
_LINES = [
    ("Rok 2027. Miasto wdraza system AI.", _WHITE, 500, 22),
    ("Ty jestes architektem.", _PURPLE, 2000, 34),
    ("Komisja etyczna czeka.", _DIM, 3500, 18),
]
_ADVANCE_AFTER = 500  # ms before SPACE works


class PhaseIntroScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._t = 0.0
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._t >= _ADVANCE_AFTER and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            self._advance()

    def update(self, dt_ms: float = 0.0) -> None:
        self._t += dt_ms

    def _advance(self) -> None:
        if self._done:
            return
        from cognitive_data_arcade.games.architects_trial.phase_domain_picker import (
            PhaseDomainPickerScene,
        )

        self._next = PhaseDomainPickerScene(self._state)
        self._done = True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        y = _H // 2 - 60
        for text, color, t_show, size in _LINES:
            if self._t >= t_show:
                surf = get_font(size).render(text, True, color)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += size + 20
        if self._t >= 4000:
            hint = get_font(14).render("[dowolny klawisz]", True, _DIM)
            surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 60))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
