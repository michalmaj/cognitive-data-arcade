from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
)

_W, _H = 1024, 720
_PANEL = (18, 18, 42)
_GOLD = (240, 165, 0)

_SLIDES = [
    (
        "Co to jest LDA?",
        [
            "Wyobraz sobie detektywa ktory szuka ukrytych wzorcow w tekstach.",
            "LDA odkrywa tematy automatycznie -- bez etykiet,",
            "tylko z wspolwystepowania slow.",
            "",
            "Temat to nie kategoria. To rozklad prawdopodobienstwa nad slowami.",
        ],
    ),
    (
        "Odcisk palca tematu",
        [
            "Kazdy temat to lista slow z wagami.",
            "Top-5 slow to 'odcisk palca' -- widoczny w panelu bocznym.",
            "",
            "Sport: bieg, medal, trening, zawodnik, turniej.",
            "LDA sam wyliczyl te odciski z korpusu tekstow.",
        ],
    ),
    (
        "Dokument = mieszanina",
        [
            "Jeden artykul moze byc w 70% o sporcie i 20% o zdrowiu.",
            "LDA zwraca rozklad -- nie pojedyncza etykiete.",
            "",
            "Twoim zadaniem: 8 misji detektywa tematow.",
            "Nacisnij SPACJE lub kliknij, zeby zaczac!",
        ],
    ),
]


class PhaseIntroScene(Scene):
    def __init__(self) -> None:
        self._slide = 0
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self._advance()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._advance()

    def _advance(self) -> None:
        if self._slide < len(_SLIDES) - 1:
            self._slide += 1
        else:
            from cognitive_data_arcade.games.topic_detective.missions import build_session
            from cognitive_data_arcade.games.topic_detective.phase_mission import PhaseMissionScene

            self._next = PhaseMissionScene(
                missions=build_session(),
                round_idx=0,
                session_score=0,
                round_results=[],
            )
            self._done = True

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title_lbl = get_font(24).render("Topic Detective", True, _WHITE)
        surface.blit(title_lbl, (_W // 2 - title_lbl.get_width() // 2, 14))

        slide_title, lines = _SLIDES[self._slide]
        st = get_font(22).render(slide_title, True, _GOLD)
        surface.blit(st, (_W // 2 - st.get_width() // 2, 100))

        y = 160
        for line in lines:
            if line:
                surf = get_font(16).render(line, True, _DIM)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 38

        for i in range(len(_SLIDES)):
            col = _GOLD if i == self._slide else (50, 50, 80)
            pygame.draw.circle(surface, col, (_W // 2 - (len(_SLIDES) - 1) * 14 + i * 28, 540), 6)

        btn = pygame.Rect(_W // 2 - 140, _H - 90, 280, 50)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=8)
        pygame.draw.rect(surface, _GOLD, btn, 2, border_radius=8)
        label = "Dalej" if self._slide < len(_SLIDES) - 1 else "Zacznij gre"
        lbl = get_font(20).render(label, True, _GOLD)
        surface.blit(lbl, (_W // 2 - lbl.get_width() // 2, _H - 74))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
