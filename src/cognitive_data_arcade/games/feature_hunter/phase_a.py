from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.feature_hunter.config import EASY, MEDIUM, HARD, DifficultyConfig

_BG    = (15, 15, 35)
_PANEL = (18, 18, 42)
_WHITE = (240, 240, 240)
_DIM   = (120, 120, 160)
_GREEN = (39, 174, 96)
_ORANGE = (243, 156, 18)
_RED   = (231, 76, 60)
_W, _H = 1024, 720

_DIFFICULTIES = [
    (EASY,   _GREEN,  "4 cechy  |  bez limitu czasu  |  podpowiedzi z r"),
    (MEDIUM, _ORANGE, "6 cech   |  45 sekund          |  tylko wykres"),
    (HARD,   _RED,    "8 cech   |  20 sekund          |  brak podpowiedzi"),
]


class PhaseAScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, (diff, col, desc) in enumerate(_DIFFICULTIES):
                btn_rect = self._btn_rect(i)
                if btn_rect.collidepoint(event.pos):
                    from cognitive_data_arcade.games.feature_hunter.phase_b import PhaseBScene
                    self._next = PhaseBScene(diff)
                    self._done = True
                    return

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        title = get_font(28).render("Feature Hunter", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 80))
        sub = get_font(16).render("Wybierz poziom trudności", True, _DIM)
        surface.blit(sub, (_W // 2 - sub.get_width() // 2, 128))

        for i, (diff, col, desc) in enumerate(_DIFFICULTIES):
            btn_rect = self._btn_rect(i)
            pygame.draw.rect(surface, _PANEL, btn_rect, border_radius=8)
            pygame.draw.rect(surface, col, btn_rect, 2, border_radius=8)
            name_lbl = get_font(22).render(diff.name_pl, True, col)
            surface.blit(name_lbl, (btn_rect.x + 20, btn_rect.y + 14))
            desc_lbl = get_font(13).render(desc, True, _DIM)
            surface.blit(desc_lbl, (btn_rect.x + 20, btn_rect.y + 44))

    def _btn_rect(self, i: int) -> pygame.Rect:
        return pygame.Rect(_W // 2 - 280, 200 + i * 130, 560, 80)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
