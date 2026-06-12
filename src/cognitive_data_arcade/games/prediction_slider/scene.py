from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_BG     = (15,  15,  35)
_PANEL  = (18,  18,  42)
_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156,  18)

_NAV_H   = 48
_W       = 1024
_INNER_H = 720 - _NAV_H  # 672

_PHASE_NAMES = ["Eksploracja", "Gra", "Sandbox"]


class _StubScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None: pass
    def update(self, dt_ms: float = 0.0) -> None: pass
    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((20, 20, 50))
    def is_done(self) -> bool: return False
    def next_scene(self) -> Scene | None: return None


def _load_phases() -> list[Scene]:
    try:
        from cognitive_data_arcade.games.prediction_slider.phase_a import PhaseAScene
        from cognitive_data_arcade.games.prediction_slider.phase_b import PhaseBScene
        from cognitive_data_arcade.games.prediction_slider.phase_c import PhaseCScene
        return [PhaseAScene(), PhaseBScene(), PhaseCScene()]
    except ImportError:
        return [_StubScene(), _StubScene(), _StubScene()]


class PredictionSliderScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._phase_idx = 0
        self._phases: list[Scene] = _load_phases()
        self._inner = pygame.Surface((_W, _INNER_H))

    @property
    def _active(self) -> Scene:
        return self._phases[self._phase_idx]

    def _offset_mouse_event(self, event: pygame.event.Event, dy: int) -> pygame.event.Event:
        d = dict(event.__dict__)
        if "pos" in d:
            x, y = d["pos"]
            d["pos"] = (x, y + dy)
        return pygame.event.Event(event.type, d)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._phase_idx = (self._phase_idx + 1) % len(self._phases)
                return
            if event.key == pygame.K_LEFT:
                self._phase_idx = (self._phase_idx - 1) % len(self._phases)
                return
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            event = self._offset_mouse_event(event, dy=-_NAV_H)
        self._active.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        self._active.update(dt_ms)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, _NAV_H))
        font = get_font(18)
        font_sm = get_font(14)
        surface.blit(font.render("<", True, _DIM), (12, (_NAV_H - 20) // 2))
        surface.blit(font.render(">", True, _DIM), (_W - 22, (_NAV_H - 20) // 2))
        tab_w = 160
        tab_x0 = (_W - len(_PHASE_NAMES) * tab_w) // 2
        for i, name in enumerate(_PHASE_NAMES):
            tx = tab_x0 + i * tab_w
            active = i == self._phase_idx
            col = _ORANGE if active else _DIM
            lbl = f"{i+1}. {name}"
            tw = font.size(lbl)[0]
            surface.blit(font.render(lbl, True, col), (tx + (tab_w - tw) // 2, (_NAV_H - 20) // 2))
            if active:
                pygame.draw.line(surface, _ORANGE, (tx + 4, _NAV_H - 3), (tx + tab_w - 4, _NAV_H - 3), 2)
        hint = font_sm.render("LEWO / PRAWO = zmień fazę", True, _DIM)
        surface.blit(hint, (20, _NAV_H - 16))
        self._inner.fill(_BG)
        self._active.draw(self._inner)
        surface.blit(self._inner, (0, _NAV_H))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return None
