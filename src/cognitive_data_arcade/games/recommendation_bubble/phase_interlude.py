from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    DIM as _DIM,
)

_W, _H = 1024, 768
_C_USER = (155, 89, 182)
_C_CURATOR = (39, 174, 96)
_C_ALGO = (230, 126, 34)


class PhaseInterludeScene(Scene):
    def __init__(self, state: GameState, next_act: str) -> None:
        # next_act: "curator" | "algo"
        self._state = state
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
        if self._next_act == "curator":
            from cognitive_data_arcade.games.recommendation_bubble.phase_curator import (
                PhaseCuratorScene,
            )

            self._next = PhaseCuratorScene(self._state)
        else:
            from cognitive_data_arcade.games.recommendation_bubble.phase_algo import PhaseAlgoScene

            self._next = PhaseAlgoScene(self._state)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        if self._next_act == "curator":
            d1 = self._state.diversity_act1
            d_color = (
                (231, 76, 60) if d1 < 0.35 else ((243, 156, 18) if d1 < 0.65 else (46, 204, 113))
            )
            lines = [
                (f"Twoj profil: roznorodnosc {int(d1 * 100)}%", d_color),
                ("", (0, 0, 0)),
                ("Teraz jestes KURATOREM.", _C_CURATOR),
                ("Masz 5 zamian, zeby zdywersyfikowac kolejke.", _DIM),
            ]
        else:
            d2 = self._state.diversity_act2
            d_color = (
                (231, 76, 60) if d2 < 0.35 else ((243, 156, 18) if d2 < 0.65 else (46, 204, 113))
            )
            lines = [
                (f"Po kuracji: roznorodnosc {int(d2 * 100)}%", d_color),
                ("", (0, 0, 0)),
                ("Teraz jestes ALGORYTMEM.", _C_ALGO),
                ("Klikaj tresci dla max. engagement.", _DIM),
                ("Diversity jest ukryta -- liczy sie wynik.", _DIM),
            ]

        y = _H // 2 - len(lines) * 24
        for text, color in lines:
            if text:
                surf = get_font(22).render(text, True, color)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 48

        hint = get_font(13).render("SPACJA aby kontynuowac", True, (80, 80, 100))
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 54))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
