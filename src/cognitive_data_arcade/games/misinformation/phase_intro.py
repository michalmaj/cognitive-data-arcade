# src/cognitive_data_arcade/games/misinformation/phase_intro.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 720
_BG    = (15, 10, 20)
_PANEL = (22, 12, 28)
_WHITE = (240, 240, 240)
_DIM   = (140, 120, 160)
_RED   = (231, 76, 60)
_BLUE  = (52, 152, 219)

_LINES = [
    ("Dezinformacja rozchodzi sie w sieciach spolecznych jak epidemia.", _DIM),
    ("", _DIM),
    ("AKT 1 -- SPREADER", _RED),
    ("Klikaj szare wezly, zeby je zarazic dezinformacja.", _DIM),
    ("Auto-SIR rozchodzi infekcje co 0.5s.  Cel: zarazic >=60%.", _DIM),
    ("", _DIM),
    ("AKT 2 -- FACT-CHECKER", _BLUE),
    ("Klikaj czerwone wezly, zeby je wyleczyc.", _DIM),
    ("SIR nie zatrzymuje sie!  Cel: zdrowych pozostac >=80%.", _DIM),
    ("", _DIM),
    ("3 rundy -- coraz wieksza, bardziej bezskalowa siec.", _DIM),
]


class PhaseIntroScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            self._advance()

    def _advance(self) -> None:
        from cognitive_data_arcade.games.misinformation.networks import ROUNDS
        from cognitive_data_arcade.games.misinformation.phase_act import PhaseActScene
        self._next = PhaseActScene(
            cfg=ROUNDS[0],
            round_idx=0,
            act="spreader",
            session_scores=[],
        )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(26).render("Misinformation Spread", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        y = 110
        for text, color in _LINES:
            if text:
                surf = get_font(16).render(text, True, color)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 30

        btn = pygame.Rect(_W // 2 - 140, _H - 90, 280, 50)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=8)
        pygame.draw.rect(surface, _WHITE, btn, 1, border_radius=8)
        lbl = get_font(20).render("Zacznij gre  [dowolny klawisz]", True, _WHITE)
        surface.blit(lbl, (_W // 2 - lbl.get_width() // 2, _H - 74))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
