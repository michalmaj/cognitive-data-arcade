# src/cognitive_data_arcade/games/distribution_playground/scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.distribution_playground.phase_a import PhaseAScene
from cognitive_data_arcade.games.distribution_playground.phase_b import PhaseBScene
from cognitive_data_arcade.games.distribution_playground.phase_c import PhaseCScene

_BG     = (15, 15, 35)
_NAV_BG = (18, 18, 45)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ACTIVE = (243, 156, 18)
_NAV_H  = 48
_PHASE_NAMES = ["Eksploracja", "Zgadywanie", "Porównanie"]


class DistributionPlaygroundScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._next: Scene | None = None
        self._phase = 1  # 1-indexed
        self._phases: list[Scene] = [PhaseAScene(), PhaseBScene(), PhaseCScene()]

    def current_phase(self) -> int:
        return self._phase

    def _active(self) -> Scene:
        return self._phases[self._phase - 1]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._phase = (self._phase % 3) + 1
                return
            if event.key == pygame.K_LEFT:
                self._phase = ((self._phase - 2) % 3) + 1
                return
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            adjusted = _offset_mouse_event(event, dy=-_NAV_H)
            self._active().handle_event(adjusted)
        else:
            self._active().handle_event(event)

    def update(self, dt_ms: float) -> None:
        self._active().update(dt_ms)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_nav(surface)
        inner = pygame.Surface((1024, 720 - _NAV_H))
        inner.fill(_BG)
        phase_scene = self._active()
        phase_scene.draw(inner, offset_y=0)
        surface.blit(inner, (0, _NAV_H))

    def _draw_nav(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _NAV_BG, (0, 0, 1024, _NAV_H))
        font_nav = get_font(18)
        font_sub = get_font(14)

        lbl = f"Faza {self._phase} / 3  -  {_PHASE_NAMES[self._phase - 1]}"
        tw  = font_nav.size(lbl)[0]
        surface.blit(font_nav.render(lbl, True, _ACTIVE), ((1024 - tw) // 2, 8))

        surface.blit(font_nav.render("<", True, _WHITE), (20, 10))
        surface.blit(font_nav.render(">", True, _WHITE), (1024 - 36, 10))

        surface.blit(font_sub.render("LEWO / PRAWO = zmień fazę", True, _DIM), (20, _NAV_H - 16))


def _offset_mouse_event(event: pygame.event.Event, dy: int) -> pygame.event.Event:
    d = dict(event.__dict__)
    if "pos" in d:
        x, y = d["pos"]
        d["pos"] = (x, y + dy)
    return pygame.event.Event(event.type, d)
