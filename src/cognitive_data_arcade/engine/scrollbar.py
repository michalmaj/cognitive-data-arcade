from __future__ import annotations

import pygame

_TRACK = (42, 42, 80)
_THUMB = (120, 120, 160)


class ScrollBar:
    def __init__(
        self,
        total: int,
        visible: int,
        x: int,
        y: int,
        h: int,
        width: int = 6,
    ) -> None:
        self._total = total
        self._visible = visible
        self._x = x
        self._y = y
        self._h = h
        self._width = width
        self._scroll = 0
        self._drag_anchor: int | None = None

    @property
    def scroll(self) -> int:
        return self._scroll

    def scroll_to(self, value: int) -> None:
        """Set scroll position, clamped to valid range."""
        self._scroll = max(0, min(self._max_scroll(), value))

    def set_total(self, total: int) -> None:
        self._total = total
        self._scroll = min(self._scroll, self._max_scroll())

    def _max_scroll(self) -> int:
        return max(0, self._total - self._visible)

    def _thumb_h(self) -> int:
        if self._total <= self._visible:
            return self._h
        return max(20, round(self._visible / self._total * self._h))

    def _thumb_y(self) -> int:
        max_s = self._max_scroll()
        if max_s == 0:
            return self._y
        th = self._thumb_h()
        return self._y + round(self._scroll / max_s * (self._h - th))

    def handle_wheel(self, dy: int) -> bool:
        """Scroll by dy rows (positive = down). Returns True if scroll changed."""
        if self._total <= self._visible:
            return False
        old = self._scroll
        self._scroll = max(0, min(self._max_scroll(), self._scroll + dy))
        return self._scroll != old

    def handle_mousedown(self, pos: tuple[int, int]) -> bool:
        """Handle left-button press. Returns True if click was consumed by scrollbar.

        - Click on thumb: begin drag (stores drag_anchor)
        - Click on track above thumb: jump so thumb top aligns with click
        - Click on track below thumb: jump so thumb bottom aligns with click
        """
        if self._total <= self._visible:
            return False
        px, py = pos
        if not (self._x <= px < self._x + self._width):
            return False
        # Click is within scrollbar column -- consume it
        th = self._thumb_h()
        ty = self._thumb_y()
        max_s = self._max_scroll()
        if ty <= py < ty + th:
            self._drag_anchor = py - ty
        elif py < ty:
            new_s = round((py - self._y) / max(1, self._h - th) * max_s)
            self._scroll = max(0, min(max_s, new_s))
        else:
            new_s = round((py - self._y - th) / max(1, self._h - th) * max_s)
            self._scroll = max(0, min(max_s, new_s))
        return True

    def handle_mousemotion(self, pos: tuple[int, int], buttons: tuple) -> bool:
        """Continue drag if left button held. Returns True if scroll changed."""
        if not buttons[0]:
            self._drag_anchor = None
            return False
        if self._drag_anchor is None:
            return False
        py = pos[1]
        th = self._thumb_h()
        max_s = self._max_scroll()
        new_s = round((py - self._drag_anchor - self._y) / max(1, self._h - th) * max_s)
        new_s = max(0, min(max_s, new_s))
        if new_s == self._scroll:
            return False
        self._scroll = new_s
        return True

    def draw(self, surface: pygame.Surface) -> None:
        """Draw track and thumb. No-op if total <= visible."""
        if self._total <= self._visible:
            return
        r = self._width // 2
        pygame.draw.rect(
            surface, _TRACK,
            (self._x, self._y, self._width, self._h),
            border_radius=r,
        )
        th = self._thumb_h()
        ty = self._thumb_y()
        pygame.draw.rect(
            surface, _THUMB,
            (self._x, ty, self._width, th),
            border_radius=r,
        )
