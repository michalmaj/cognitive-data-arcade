from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font

_BG     = (15, 15, 35)
_TRACK  = (40, 40, 80)
_THUMB  = (240, 240, 240)
_DIM    = (120, 120, 160)


class SliderWidget:
    """Horizontal integer slider from min_val to max_val."""

    def __init__(
        self,
        rect: pygame.Rect,
        min_val: int,
        max_val: int,
        value: int,
    ) -> None:
        self.rect = rect
        self.min_val = min_val
        self.max_val = max_val
        self._value = max(min_val, min(max_val, value))
        self._dragging = False

    @property
    def value(self) -> int:
        return self._value

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if abs(event.pos[1] - self.rect.centery) <= 20:
                self._dragging = True
                self._update_from_x(event.pos[0])
        elif event.type == pygame.MOUSEMOTION and self._dragging and event.buttons[0]:
            self._update_from_x(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False

    def _update_from_x(self, x: int) -> None:
        ratio = (x - self.rect.x) / max(self.rect.w, 1)
        ratio = max(0.0, min(1.0, ratio))
        self._value = round(self.min_val + ratio * (self.max_val - self.min_val))

    def draw(
        self,
        surface: pygame.Surface,
        *,
        label: str = "",
        value_text: str = "",
        color: tuple[int, int, int] = (52, 152, 219),
    ) -> None:
        cy = self.rect.centery
        # Track
        track = pygame.Rect(self.rect.x, cy - 3, self.rect.w, 6)
        pygame.draw.rect(surface, _TRACK, track, border_radius=3)
        # Fill
        ratio = (self._value - self.min_val) / max(self.max_val - self.min_val, 1)
        fill_w = int(ratio * self.rect.w)
        if fill_w > 0:
            fill = pygame.Rect(self.rect.x, cy - 3, fill_w, 6)
            pygame.draw.rect(surface, color, fill, border_radius=3)
        # Thumb
        thumb_x = self.rect.x + fill_w
        pygame.draw.circle(surface, _THUMB, (thumb_x, cy), 9)
        pygame.draw.circle(surface, color, (thumb_x, cy), 9, 2)
        # Label (above left)
        if label:
            lbl = get_font(13).render(label, True, _DIM)
            surface.blit(lbl, (self.rect.x, self.rect.y - 18))
        # Value text (above right)
        if value_text:
            vt = get_font(14).render(value_text, True, color)
            surface.blit(vt, (self.rect.right - vt.get_width(), self.rect.y - 18))
