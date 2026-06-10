from __future__ import annotations

from dataclasses import dataclass

import pygame

from cognitive_data_arcade.engine.fonts import get_font

_BG      = (20, 20, 50, 230)
_BORDER  = (100, 100, 200)
_TITLE   = (243, 156, 18)
_BODY    = (200, 200, 220)
_IMPACT  = (100, 220, 140)
_W       = 300
_PAD     = 10
_LINE_H  = 20


@dataclass(frozen=True)
class ContextInfo:
    title:  str
    body:   str
    impact: str


class ContextPopup:
    def __init__(self) -> None:
        self._entries: list[tuple[pygame.Rect, ContextInfo]] = []
        self._active: ContextInfo | None = None
        self._pos: tuple[int, int] = (0, 0)

    def register(self, rect: pygame.Rect, info: ContextInfo) -> None:
        self._entries.append((rect, info))

    def clear(self) -> None:
        self._entries.clear()
        self._active = None

    def is_visible(self) -> bool:
        return self._active is not None

    def current_title(self) -> str:
        return self._active.title if self._active else ""

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self._active:
                self._active = None
                return True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                for rect, info in self._entries:
                    if rect.collidepoint(event.pos):
                        self._active = info
                        self._pos = event.pos
                        return True
                self._active = None
                return False
            elif event.button == 1:
                if self._active:
                    self._active = None
                    return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        if not self._active:
            return
        info = self._active
        font_title  = get_font(17)
        font_body   = get_font(15)
        font_impact = get_font(15)

        title_surf   = font_title.render(info.title, True, _TITLE)
        body_lines   = _wrap(info.body, font_body, _W - 2 * _PAD)
        impact_lines = _wrap(info.impact, font_impact, _W - 2 * _PAD)
        total_lines  = len(body_lines) + len(impact_lines)
        h = _PAD * 3 + _LINE_H + total_lines * _LINE_H + 4

        sw, sh = surface.get_size()
        x, y = self._pos
        x = min(x, sw - _W - 4)
        y = min(y, sh - h - 4)
        x = max(x, 2)
        y = max(y, 2)

        popup = pygame.Surface((_W, h), pygame.SRCALPHA)
        pygame.draw.rect(popup, _BG, (0, 0, _W, h), border_radius=6)
        pygame.draw.rect(popup, _BORDER, (0, 0, _W, h), width=1, border_radius=6)
        popup.blit(title_surf, (_PAD, _PAD))
        cy = _PAD + _LINE_H + 4
        for line in body_lines:
            popup.blit(font_body.render(line, True, _BODY), (_PAD, cy))
            cy += _LINE_H
        for line in impact_lines:
            popup.blit(font_impact.render(line, True, _IMPACT), (_PAD, cy))
            cy += _LINE_H
        surface.blit(popup, (x, y))


def _wrap(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if font.size(test)[0] <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]
