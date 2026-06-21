# src/cognitive_data_arcade/games/you_were_the_dataset/phase_reveal.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    PURPLE as _PURPLE,
)

_W, _H = 1024, 720

# (text, color, t_start_ms)
_LINES = [
    ("Przez cały ten kurs...", _DIM, 1000),
    ("tworzyłeś dane.", _WHITE, 2500),
    ("Oto Twój kognitywny profil.", _PURPLE, 3500),
]
_HINT_T = 4000


class PhaseRevealScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._t = 0.0
        self._done = False
        self._next: Scene | None = None

        # Load profile now if not already set (real CSV path)
        if self._state.profile is None:
            from cognitive_data_arcade.games.you_were_the_dataset.profile_loader import load_profile

            self._state.profile = load_profile()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self._t >= 500:
            self._advance()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._t >= 500:
            self._advance()

    def _advance(self) -> None:
        from cognitive_data_arcade.games.you_were_the_dataset.phase_profile import PhaseProfileScene

        self._next = PhaseProfileScene(self._state)
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        self._t += dt_ms

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        for text, color, t_start in _LINES:
            if self._t >= t_start:
                surf = get_font(32 if text == "tworzyles dane." else 20).render(text, True, color)
                idx = [ln[0] for ln in _LINES].index(text)
                y = _H // 2 - 60 + idx * 56
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
        if self._t >= _HINT_T:
            hint = get_font(14).render("[SPACJA]", True, _DIM)
            surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 50))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
