# src/cognitive_data_arcade/games/distribution_playground/widgets.py
from __future__ import annotations

from dataclasses import dataclass

import pygame

from cognitive_data_arcade.engine.fonts import get_font

_TRACK  = (42, 42, 80)
_DIM    = (120, 120, 160)
_ACTIVE = (243, 156, 18)
_WHITE  = (240, 240, 240)
_BG     = (26, 26, 46)
_THUMB_R = 8
_TRACK_H = 4
_SLIDER_W = 240


@dataclass
class SliderSpec:
    label:   str
    min_val: int
    max_val: int
    default: int
    step:    int


class Slider:
    def __init__(self, spec: SliderSpec, x: int, y: int, w: int = _SLIDER_W) -> None:
        self._spec = spec
        self._x, self._y, self._w = x, y, w
        self._value = spec.default
        self._dragging = False
        self.focused: bool = False
        self.rect = pygame.Rect(x - 6, y - 2, w + 12, 36)

    @property
    def value(self) -> int:
        return self._value

    def set_value(self, v: int) -> None:
        self._value = max(self._spec.min_val, min(self._spec.max_val, v))

    def _thumb_x(self) -> int:
        ratio = (self._value - self._spec.min_val) / max(1, self._spec.max_val - self._spec.min_val)
        return self._x + round(ratio * self._w)

    def _track_y(self) -> int:
        return self._y + 20

    def _set_from_pixel(self, px: int) -> None:
        ratio = (px - self._x) / max(1, self._w)
        steps = round(ratio * (self._spec.max_val - self._spec.min_val) / self._spec.step)
        raw = self._spec.min_val + steps * self._spec.step
        self._value = max(self._spec.min_val, min(self._spec.max_val, raw))

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        ty = self._track_y()
        if self._x <= px <= self._x + self._w and abs(py - ty) <= _THUMB_R + 6:
            self._set_from_pixel(px)
            self._dragging = True
            self.focused = True
            return True
        return False

    def handle_mousemotion(self, pos: tuple[int, int], buttons: tuple) -> bool:
        if not buttons[0]:
            self._dragging = False
            return False
        if not self._dragging:
            return False
        old = self._value
        self._set_from_pixel(pos[0])
        return self._value != old

    def draw(self, surface: pygame.Surface) -> None:
        font_lbl = get_font(16)
        font_val = get_font(18)
        surface.blit(font_lbl.render(self._spec.label, True, _DIM), (self._x, self._y))
        val_str = str(self._value)
        vw = font_val.size(val_str)[0]
        surface.blit(font_val.render(val_str, True, _WHITE), (self._x + self._w - vw, self._y))
        ty = self._track_y()
        pygame.draw.rect(surface, _TRACK,
                         (self._x, ty - _TRACK_H // 2, self._w, _TRACK_H), border_radius=2)
        tx = self._thumb_x()
        filled = max(0, tx - self._x)
        if filled > 0:
            fc = _ACTIVE if self.focused else _DIM
            pygame.draw.rect(surface, fc,
                             (self._x, ty - _TRACK_H // 2, filled, _TRACK_H), border_radius=2)
        pygame.draw.circle(surface, _ACTIVE if self.focused else _DIM, (tx, ty), _THUMB_R)


_SHAPES = [
    ("normal",     "Normalny"),
    ("uniform",    "Jednostajny"),
    ("exgaussian", "Ex-Gaussian"),
]
_TAB_H   = 28
_TAB_GAP = 4


class ShapeTab:
    """Horizontal tab bar for selecting distribution type."""

    def __init__(self, x: int, y: int, w: int) -> None:
        self._x, self._y, self._w = x, y, w
        self._selected = 0
        n = len(_SHAPES)
        tw = (w - _TAB_GAP * (n - 1)) // n
        self._rects = [
            pygame.Rect(x + i * (tw + _TAB_GAP), y, tw, _TAB_H)
            for i in range(n)
        ]

    @property
    def dist_type(self) -> str:
        return _SHAPES[self._selected][0]

    def select(self, dist_type: str) -> None:
        for i, (dt, _) in enumerate(_SHAPES):
            if dt == dist_type:
                self._selected = i
                return

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        for i, rect in enumerate(self._rects):
            if rect.collidepoint(pos):
                self._selected = i
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        font = get_font(15)
        for i, (rect, (_, label)) in enumerate(zip(self._rects, _SHAPES)):
            active = i == self._selected
            bg = (60, 60, 120) if active else (26, 26, 46)
            border = (243, 156, 18) if active else (60, 60, 100)
            pygame.draw.rect(surface, bg, rect, border_radius=4)
            pygame.draw.rect(surface, border, rect, width=1, border_radius=4)
            col = _WHITE if active else _DIM
            tw, th = font.size(label)
            surface.blit(font.render(label, True, col),
                         (rect.x + (rect.w - tw) // 2, rect.y + (rect.h - th) // 2))
