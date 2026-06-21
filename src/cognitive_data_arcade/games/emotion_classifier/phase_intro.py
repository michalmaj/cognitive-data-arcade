# src/cognitive_data_arcade/games/emotion_classifier/phase_intro.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    PURPLE as _PURPLE,
)

_W, _H = 1024, 720
_PANEL = (18, 18, 42)

_LINES = [
    "Twoim zadaniem jest oznaczyć słowa o wyraźnym sentymencie.",
    "Lewym przyciskiem (LPM) zaznaczasz słowa pozytywne,",
    "prawym (PPM) -- negatywne. Kliknij ponownie, aby odznaczać.",
    "",
    "Obserwuj panel po prawej -- leksykon sumuje wagi na żywo.",
    "Odkryj, gdzie leksykon się myli: negacja, intensywność, ironia.",
    "",
    "Jeśli chcesz wskazówki, kliknij PPM na pustym miejscu zdania.",
    "",
    "8 rund. Zdobądź jak najwięcej punktów!",
]


class PhaseIntroScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            self._advance()

    def _advance(self) -> None:
        from cognitive_data_arcade.games.emotion_classifier.sentences import (
            SENTENCE_BANK,
            draw_session,
        )
        from cognitive_data_arcade.games.emotion_classifier.phase_round import PhaseRoundScene

        sentences = draw_session(SENTENCE_BANK)
        self._next = PhaseRoundScene(
            sentences=sentences, round_idx=0, session_score=0, round_results=[]
        )
        self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(28).render("Emotion Classifier", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        y = 140
        for line in _LINES:
            if line:
                surf = get_font(16).render(line, True, _DIM)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 36

        btn = pygame.Rect(_W // 2 - 130, _H - 90, 260, 50)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=8)
        pygame.draw.rect(surface, _PURPLE, btn, 2, border_radius=8)
        lbl = get_font(20).render("Zacznij grę", True, _PURPLE)
        surface.blit(lbl, (_W // 2 - lbl.get_width() // 2, _H - 74))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
