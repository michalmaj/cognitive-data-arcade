# src/cognitive_data_arcade/games/overfitting_monster/phase_intro.py
from __future__ import annotations

import random

import numpy as np
import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_BG    = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM   = (120, 120, 160)
_BLUE  = (52, 152, 219)
_W, _H = 1024, 720

_LINES = [
    "Jesteś badaczem ML. Twoim zadaniem: dobrać k dla KNN i podział danych,",
    "by model dobrze generalizował — nie tylko zapamiętał dane treningowe.",
    "",
    "Dwa suwaki: podział trening/test i wartość k (liczba sąsiadów KNN).",
    "Obserwuj na żywo dokładność na treningu i teście.",
    "Uważaj na duży gap — to znak overfittingu!",
    "",
    "5 rund. PPM na ekranie = podpowiedź o scenariuszu.",
]


class PhaseIntroScene(Scene):
    def __init__(self, session_seed: int | None = None) -> None:
        self._session_seed = (
            session_seed if session_seed is not None else random.randint(0, 10 ** 6)
        )
        rng = np.random.default_rng(self._session_seed)
        self._scenario_order: list[int] = rng.permutation(5).tolist()
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            self._advance()

    def _advance(self) -> None:
        from cognitive_data_arcade.games.overfitting_monster.phase_draw import PhaseDrawScene
        from cognitive_data_arcade.games.overfitting_monster.scenarios import SCENARIOS
        self._next = PhaseDrawScene(
            scenario=SCENARIOS[self._scenario_order[0]],
            round_idx=0,
            session_seed=self._session_seed,
            session_score=0,
            round_results=[],
            scenario_order=self._scenario_order,
        )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 60))
        title = get_font(28).render("Overfitting Monster", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        y = 150
        for line in _LINES:
            if line:
                surf = get_font(16).render(line, True, _DIM)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 32

        btn = pygame.Rect(_W // 2 - 120, _H - 90, 240, 48)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=8)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=8)
        lbl = get_font(20).render("Zacznij grę", True, _BLUE)
        surface.blit(lbl, (_W // 2 - lbl.get_width() // 2, _H - 76))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
