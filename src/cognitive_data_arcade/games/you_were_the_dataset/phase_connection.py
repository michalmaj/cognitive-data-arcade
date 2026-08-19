# src/cognitive_data_arcade/games/you_were_the_dataset/phase_connection.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    PURPLE as _PURPLE,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState

_W, _H = 1024, 768

# (lines_list, t_start_ms)
_CARDS = [
    (
        [
            "Skad pochodzi ta wiedza?",
            "",
            "Kazde klikniecie SPACJI",
            "-> plik CSV -> obliczenie -> ten wynik.",
        ],
        0,
    ),
    (
        [
            "Byles jednoczesnie:",
            "",
            "  naukowcem -- kto zbiera dane",
            "  i uczestnikiem -- kto je generuje.",
        ],
        3000,
    ),
    (
        [
            "Dane to nie liczby.",
            "",
            "Dane to slad zachowania.",
            "Twojego zachowania.",
            "",
            "Teraz wiesz skad AI wie",
            "co wiesz, czego chcesz, kim jestes.",
        ],
        6000,
    ),
]
_ADVANCE_AFTER = 6000  # allow SPACE-to-advance only after all cards visible

# Lines that get purple/white highlight (by card index, line index)
_HIGHLIGHT_WHITE = {(0, 0), (1, 0), (2, 0)}  # first line of each card
_HIGHLIGHT_PURPLE = {(2, 3), (2, 6)}  # "Twojego zachowania." and "kim jestes."


class PhaseConnectionScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._t = 0.0
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._done:
            return
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and self._t >= _ADVANCE_AFTER
        ) or (
            event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self._t >= _ADVANCE_AFTER
        ):
            self._advance()

    def _advance(self) -> None:
        from cognitive_data_arcade.games.you_were_the_dataset.phase_result import PhaseResultScene

        self._next = PhaseResultScene(self._state)
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        self._t += dt_ms

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        y_base = 140
        for card_idx, (lines, t_start) in enumerate(_CARDS):
            if self._t < t_start:
                break
            for line_idx, line in enumerate(lines):
                if not line:
                    y_base += 18
                    continue
                key = (card_idx, line_idx)
                if key in _HIGHLIGHT_PURPLE:
                    color = _PURPLE
                    font_size = 20
                elif key in _HIGHLIGHT_WHITE:
                    color = _WHITE
                    font_size = 20
                else:
                    color = _DIM
                    font_size = 16
                surf = get_font(font_size).render(line, True, color)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y_base))
                y_base += font_size + 8
            y_base += 24

        if self._t >= _ADVANCE_AFTER:
            hint = get_font(14).render("[SPACJA]", True, _DIM)
            surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 50))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
