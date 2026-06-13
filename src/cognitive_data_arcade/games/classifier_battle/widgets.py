from __future__ import annotations

import numpy as np
import pygame

from cognitive_data_arcade.engine.fonts import get_font

_RED    = (231, 76, 60)
_BLUE   = (52, 152, 219)
_YELLOW = (243, 156, 18)
_BG     = (15, 15, 35)
_BORDER = (40, 40, 80)
_DOT_RADIUS = 6


class DrawCanvas:
    """Freehand decision boundary drawn over a 2D scatter plot."""

    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self._X: np.ndarray = np.empty((0, 2))
        self._y: np.ndarray = np.empty(0, dtype=int)
        self._polyline: list[tuple[int, int]] = []
        self._drawing = False

    def load_data(self, X: np.ndarray, y: np.ndarray) -> None:
        """X in [0,1]^2, y binary labels 0/1."""
        self._X = X
        self._y = y
        self._polyline = []
        self._drawing = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self._polyline = [event.pos]
                self._drawing = True
        elif event.type == pygame.MOUSEMOTION and self._drawing and event.buttons[0]:
            self._polyline.append(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._drawing = False

    def clear(self) -> None:
        self._polyline = []
        self._drawing = False

    @property
    def polyline(self) -> list[tuple[int, int]]:
        """Polyline in screen pixel coordinates."""
        return self._polyline

    @property
    def polyline_normalised(self) -> list[tuple[float, float]]:
        """Polyline in [0,1] space relative to the canvas rect."""
        return [
            ((x - self.rect.x) / self.rect.w, (y - self.rect.y) / self.rect.h)
            for x, y in self._polyline
        ]

    def is_valid(self) -> bool:
        """True when polyline vertical span >= 60% of canvas height."""
        if len(self._polyline) < 2:
            return False
        ys = [p[1] for p in self._polyline]
        return (max(ys) - min(ys)) >= 0.6 * self.rect.h

    def draw(
        self,
        surface: pygame.Surface,
        *,
        misclassified: np.ndarray | None = None,
    ) -> None:
        """Draw background, data points, and polyline onto surface."""
        pygame.draw.rect(surface, _BG, self.rect)
        pygame.draw.rect(surface, _BORDER, self.rect, 1)

        for i, (x, y) in enumerate(self._X):
            cx = int(self.rect.x + x * self.rect.w)
            cy = int(self.rect.y + y * self.rect.h)
            color = _RED if self._y[i] == 0 else _BLUE
            pygame.draw.circle(surface, color, (cx, cy), _DOT_RADIUS)

            if misclassified is not None and misclassified[i]:
                font = get_font(12)
                x_lbl = font.render("x", True, (255, 255, 255))
                surface.blit(x_lbl, (cx - x_lbl.get_width() // 2, cy - x_lbl.get_height() // 2))

        if len(self._polyline) >= 2:
            pygame.draw.lines(surface, _YELLOW, False, self._polyline, 2)
