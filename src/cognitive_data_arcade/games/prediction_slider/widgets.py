from __future__ import annotations

import pygame
from cognitive_data_arcade.engine.fonts import get_font

_WHITE     = (240, 240, 240)
_DIM       = (120, 120, 160)
_ORANGE    = (243, 156,  18)
_BLUE      = ( 52, 152, 219)
_TRACK     = ( 42,  42,  80)
_PANEL     = ( 18,  18,  42)
_BLUE_DARK = ( 26,  58,  90)


class _FloatSlider:
    """Horizontal slider — identical to hypothesis_arena.widgets._FloatSlider."""
    def __init__(
        self, label: str, min_v: float, max_v: float, default: float,
        step: float, x: int, y: int, w: int, fmt: str = ".2f",
    ) -> None:
        self._label = label
        self._min = min_v
        self._max = max_v
        self._step = step
        self._value = default
        self._x, self._y, self._w = x, y, w
        self._fmt = fmt
        self._dragging = False
        self.rect = pygame.Rect(x - 6, y - 2, w + 12, 42)

    @property
    def value(self) -> float:
        return self._value

    def _thumb_x(self) -> int:
        ratio = (self._value - self._min) / max(1e-9, self._max - self._min)
        return self._x + round(ratio * self._w)

    def _track_y(self) -> int:
        return self._y + 26

    def _set_from_pixel(self, px: int) -> None:
        ratio = (px - self._x) / max(1, self._w)
        steps = round(ratio * (self._max - self._min) / self._step)
        raw = self._min + steps * self._step
        self._value = max(self._min, min(self._max, raw))

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        ty = self._track_y()
        if self._x <= px <= self._x + self._w and abs(py - ty) <= 14:
            self._set_from_pixel(px)
            self._dragging = True
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
        surface.blit(font_lbl.render(self._label, True, _DIM), (self._x, self._y))
        val_str = format(self._value, self._fmt)
        vw = font_val.size(val_str)[0]
        surface.blit(font_val.render(val_str, True, _WHITE), (self._x + self._w - vw, self._y))
        ty = self._track_y()
        pygame.draw.rect(surface, _TRACK, (self._x, ty - 2, self._w, 4), border_radius=2)
        tx = self._thumb_x()
        filled = max(0, tx - self._x)
        if filled > 0:
            pygame.draw.rect(surface, _ORANGE, (self._x, ty - 2, filled, 4), border_radius=2)
        pygame.draw.circle(surface, _ORANGE, (tx, ty), 8)


class _VerticalSlider:
    """Vertical prediction slider for Phase B overlay on scatter plot.
    x_px: fixed screen x (center of slider)
    y_top_px / y_bot_px: track extent in inner surface coords
    y_min / y_max: data space range
    """
    def __init__(
        self, x_px: int, y_top_px: int, y_bot_px: int,
        y_min: float, y_max: float,
    ) -> None:
        self._x = x_px
        self._y_top = y_top_px
        self._y_bot = y_bot_px
        self._y_min = y_min
        self._y_max = y_max
        self._value = (y_min + y_max) / 2.0
        self._dragging = False
        self.rect = pygame.Rect(x_px - 22, y_top_px, 44, y_bot_px - y_top_px)

    @property
    def value(self) -> float:
        return self._value

    def _thumb_y(self) -> int:
        ratio = (self._value - self._y_min) / max(1e-9, self._y_max - self._y_min)
        return self._y_bot - round(ratio * (self._y_bot - self._y_top))

    def _set_from_pixel(self, py: int) -> None:
        ratio = (self._y_bot - py) / max(1, self._y_bot - self._y_top)
        self._value = self._y_min + ratio * (self._y_max - self._y_min)
        self._value = max(self._y_min, min(self._y_max, self._value))

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        px, py = pos
        ty = self._thumb_y()
        if abs(px - self._x) <= 22 and abs(py - ty) <= 14:
            self._set_from_pixel(py)
            self._dragging = True
            return True
        return False

    def handle_mousemotion(self, pos: tuple[int, int], buttons: tuple) -> bool:
        if not buttons[0]:
            self._dragging = False
            return False
        if not self._dragging:
            return False
        old = self._value
        self._set_from_pixel(pos[1])
        return self._value != old

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.line(surface, _TRACK, (self._x, self._y_top), (self._x, self._y_bot), 3)
        ty = self._thumb_y()
        pygame.draw.circle(surface, _ORANGE, (self._x, ty), 10)
        pygame.draw.circle(surface, _WHITE, (self._x, ty), 10, 2)
        font = get_font(13)
        val_txt = font.render(f"{self._value:.1f}", True, _WHITE)
        surface.blit(val_txt, (self._x - val_txt.get_width() // 2, max(self._y_top, ty - 22)))
