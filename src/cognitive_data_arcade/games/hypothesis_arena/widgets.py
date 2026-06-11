from __future__ import annotations

import pygame
from cognitive_data_arcade.engine.fonts import get_font

_WHITE  = (240, 240, 240)
_DIM    = (120, 120, 160)
_ORANGE = (243, 156, 18)
_BLUE   = ( 52, 152, 219)
_TRACK  = ( 42,  42,  80)
_PANEL  = ( 18,  18,  42)


class _FloatSlider:
    def __init__(
        self,
        label: str,
        min_v: float,
        max_v: float,
        default: float,
        step: float,
        x: int,
        y: int,
        w: int,
        fmt: str = ".2f",
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
        surface.blit(font_val.render(val_str, True, _WHITE),
                     (self._x + self._w - vw, self._y))
        ty = self._track_y()
        pygame.draw.rect(surface, _TRACK,
                         (self._x, ty - 2, self._w, 4), border_radius=2)
        tx = self._thumb_x()
        filled = max(0, tx - self._x)
        if filled > 0:
            pygame.draw.rect(surface, _ORANGE,
                             (self._x, ty - 2, filled, 4), border_radius=2)
        pygame.draw.circle(surface, _ORANGE, (tx, ty), 8)


class _AlphaButtons:
    _ALPHAS = [0.01, 0.05, 0.10]

    def __init__(self, x: int, y: int, w_each: int, h: int) -> None:
        self._x, self._y = x, y
        self._w, self._h = w_each, h
        self._selected = 1  # default: 0.05
        gap = 6
        self.rect = pygame.Rect(x - 4, y - 4, len(self._ALPHAS) * (w_each + gap) + 8, h + 8)

    @property
    def value(self) -> float:
        return self._ALPHAS[self._selected]

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        gap = 6
        for i in range(len(self._ALPHAS)):
            bx = self._x + i * (self._w + gap)
            btn = pygame.Rect(bx, self._y, self._w, self._h)
            if btn.collidepoint(event.pos):
                if self._selected != i:
                    self._selected = i
                    return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        font = get_font(16)
        gap = 6
        lbl_surf = font.render("Alpha (α)", True, _DIM)
        surface.blit(lbl_surf, (self._x, self._y - 22))
        for i, alpha in enumerate(self._ALPHAS):
            bx = self._x + i * (self._w + gap)
            btn = pygame.Rect(bx, self._y, self._w, self._h)
            selected = i == self._selected
            bg    = (26,  58,  90) if selected else (18, 18, 42)
            border = _BLUE       if selected else (42, 42, 80)
            bw     = 2           if selected else 1
            pygame.draw.rect(surface, bg, btn, border_radius=3)
            pygame.draw.rect(surface, border, btn, bw, border_radius=3)
            color = _BLUE if selected else _DIM
            txt = font.render(str(alpha), True, color)
            tw, th = font.size(str(alpha))
            surface.blit(txt, (bx + (self._w - tw) // 2, self._y + (self._h - th) // 2))
