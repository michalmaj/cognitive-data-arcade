from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
)

_W, _H = 1024, 720
_PANEL = (16, 20, 36)
_C_APP = (155, 89, 182)
_C_ENG = (39, 174, 96)
_C_REG = (230, 126, 34)

_LINES = [
    ("Algorytm ocenia wnioski kredytowe.", _DIM),
    ("Ale czy jest sprawiedliwy?", _DIM),
    ("", _DIM),
    ("AKT 1 -- APLIKANT", _C_APP),
    ("Przeanalizuj decyzje algorytmu. Znajdz wzorzec.", _DIM),
    ("", _DIM),
    ("AKT 2 -- INZYNIER", _C_ENG),
    ("Usuwaj cechy modelu. Obserwuj jak zmienia sie bias.", _DIM),
    ("", _DIM),
    ("AKT 3 -- REGULATOR", _C_REG),
    ("Wybierz kryterium sprawiedliwosci. Obserwuj konsekwencje.", _DIM),
]


class PhaseIntroScene(Scene):
    def __init__(self, state: GameState) -> None:
        self._state = state
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            self._advance()

    def _advance(self) -> None:
        if self._done:
            return
        from cognitive_data_arcade.games.bias_blind_spot.phase_applicant import PhaseApplicantScene

        self._next = PhaseApplicantScene(self._state)
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(26).render("Bias Blind Spot", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))
        y = 100
        for text, color in _LINES:
            if text:
                surf = get_font(16).render(text, True, color)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 34
        btn = pygame.Rect(_W // 2 - 140, _H - 90, 280, 50)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=8)
        pygame.draw.rect(surface, _WHITE, btn, 1, border_radius=8)
        lbl = get_font(20).render("Zacznij gre  [dowolny klawisz]", True, _WHITE)
        surface.blit(lbl, (_W // 2 - lbl.get_width() // 2, _H - 74))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
