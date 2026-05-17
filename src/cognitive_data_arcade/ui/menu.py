from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.scene import Scene

_LESSONS = [
    (1, "Big Data in Cognitive Science"),
    (2, "Reaction Time Lab"),
    (3, "Event Logs and Data Formats"),
    (4, "Data Cleaning"),
    (5, "Missing Values and Outliers"),
    (6, "Exploratory Data Analysis"),
    (7, "Stroop Challenge"),
    (8, "Flanker Arena"),
    (9, "Go/No-Go Guard"),
    (10, "N-Back Memory Grid"),
]

_BG = (26, 26, 46)
_TITLE_COLOR = (240, 240, 240)
_ITEM_COLOR = (160, 160, 160)
_HIGHLIGHT_COLOR = (243, 156, 18)


class LessonMenuScene(Scene):
    def __init__(self) -> None:
        self._done = False
        self._selected = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._done = True
        elif event.key == pygame.K_UP:
            self._selected = max(0, self._selected - 1)
        elif event.key == pygame.K_DOWN:
            self._selected = min(len(_LESSONS) - 1, self._selected + 1)

    def update(self, dt_ms: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        font_title = pygame.font.SysFont(None, 52)
        font_item = pygame.font.SysFont(None, 34)

        title = font_title.render("Cognitive Data Arcade", True, _TITLE_COLOR)
        surface.blit(title, (40, 36))

        subtitle = font_item.render("↑↓ navigate   ESC quit", True, _ITEM_COLOR)
        surface.blit(subtitle, (42, 96))

        for i, (num, name) in enumerate(_LESSONS):
            color = _HIGHLIGHT_COLOR if i == self._selected else _ITEM_COLOR
            text = font_item.render(f"{num:02d}.  {name}", True, color)
            surface.blit(text, (60, 140 + i * 44))

    def is_done(self) -> bool:
        return self._done
