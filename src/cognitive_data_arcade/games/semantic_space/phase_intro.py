from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    BLUE as _BLUE,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_W, _H = 1024, 768
_PANEL = (18, 18, 42)

_SLIDES = [
    (
        "Czym jest embedding?",
        [
            "Kazde slowo to punkt w przestrzeni matematycznej.",
            "Slowa uzywane w podobnych kontekstach laduja blisko siebie.",
            "'kot' i 'pies' sa blizej siebie niz 'kot' i 'tablica'.",
            "",
            "Embeddingi koduja znaczenie jako geometrie.",
        ],
    ),
    (
        "Podobne slowa = bliskie punkty",
        [
            "Slowa zgrupowane sa w klastry tematyczne.",
            "Emocje blisko emocji, zwierzeta blisko zwierzat.",
            "Odleglosc miedzy punktami = niepodobienstwo semantyczne.",
            "",
            "Nawet analogie sa zakodowane: krol - mezczyzna + kobieta = krolowa.",
        ],
    ),
    (
        "Twoje zadanie: 8 misji",
        [
            "Eksploruj mape 50 polskich slow.",
            "Kliknij wezel, zeby zobaczyc jego sasiadow.",
            "",
            "Misje: znajdz sasiadow, wykryj intruza,",
            "odkryj most semantyczny, rozwiaz analogie.",
            "",
            "Nacisnij SPACJE lub kliknij, aby zaczac!",
        ],
    ),
]


class PhaseIntroScene(Scene):
    def __init__(self) -> None:
        self._slide = 0
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN) or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._advance()

    def _advance(self) -> None:
        if self._slide < len(_SLIDES) - 1:
            self._slide += 1
        else:
            from cognitive_data_arcade.games.semantic_space.missions import build_session
            from cognitive_data_arcade.games.semantic_space.phase_mission import PhaseMissionScene

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
        title_lbl = get_font(24).render("Semantic Space Explorer", True, _WHITE)
        surface.blit(title_lbl, (_W // 2 - title_lbl.get_width() // 2, 14))

        slide_title, lines = _SLIDES[self._slide]
        st = get_font(22).render(slide_title, True, _BLUE)
        surface.blit(st, (_W // 2 - st.get_width() // 2, 100))

        y = 160
        for line in lines:
            if line:
                surf = get_font(16).render(line, True, _DIM)
                surface.blit(surf, (_W // 2 - surf.get_width() // 2, y))
            y += 38

        # Slide indicator dots
        for i in range(len(_SLIDES)):
            col = _BLUE if i == self._slide else (50, 50, 80)
            pygame.draw.circle(surface, col, (_W // 2 - (len(_SLIDES) - 1) * 14 + i * 28, 540), 6)

        btn = pygame.Rect(_W // 2 - 140, _H - 90, 280, 50)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=8)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=8)
        label = "Dalej" if self._slide < len(_SLIDES) - 1 else "Zacznij gre"
        lbl = get_font(20).render(label, True, _BLUE)
        surface.blit(lbl, (_W // 2 - lbl.get_width() // 2, _H - 74))
        hint = get_font(14).render("SPACJA lub klik — dalej", True, _DIM)
        surface.blit(hint, (_W // 2 - hint.get_width() // 2, _H - 28))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
