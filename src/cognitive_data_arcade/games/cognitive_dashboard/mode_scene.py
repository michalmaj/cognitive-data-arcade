# src/cognitive_data_arcade/games/cognitive_dashboard/mode_scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession
from cognitive_data_arcade.profile.manager import ProfileManager

_BG    = (26, 26, 46)
_WHITE = (240, 240, 240)
_DIM   = (100, 100, 150)
_ORANGE = (243, 156, 18)
_W, _H = 1024, 768

_BTN_W, _BTN_H = 440, 100
_BTN_GAP = 40
_BTN_Y = 320


def _btn_rect(idx: int) -> pygame.Rect:
    total = 2 * _BTN_W + _BTN_GAP
    left = (_W - total) // 2
    x = left + idx * (_BTN_W + _BTN_GAP)
    return pygame.Rect(x, _BTN_Y, _BTN_W, _BTN_H)


class CognitiveDashboardModeScene(Scene):
    def __init__(self, pm: ProfileManager, strings: Strings) -> None:
        self._pm = pm
        self._strings = strings
        self._selected = 0
        self._hover = -1
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._hover = -1
            for i in range(2):
                if _btn_rect(i).collidepoint(event.pos):
                    self._hover = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(2):
                if _btn_rect(i).collidepoint(event.pos):
                    self._launch(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from cognitive_data_arcade.ui.menu import LessonMenuScene
                self._next = LessonMenuScene(self._pm, self._strings)
                self._done = True
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_TAB):
                self._selected = 1 - self._selected
            elif event.key == pygame.K_RETURN:
                self._launch(self._selected)

    def _launch(self, idx: int) -> None:
        from cognitive_data_arcade.games.cognitive_dashboard.config import generate_synthetic
        from cognitive_data_arcade.games.cognitive_dashboard.dashboard_scene import CognitiveDashboardScene

        if idx == 0:
            session = DashboardSession()
        else:
            session = generate_synthetic()

        self._next = CognitiveDashboardScene(session, self._strings, self._pm)
        self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        title = get_font(48).render("Cognitive Dashboard", True, _WHITE)
        surface.blit(title, (w // 2 - title.get_width() // 2, 100))

        subtitle = get_font(28).render("Lekcja 12 -- Porownywanie zadan poznawczych", True, _DIM)
        surface.blit(subtitle, (w // 2 - subtitle.get_width() // 2, 170))

        labels = ["Zagraj -- zbierz dane", "Dane syntetyczne"]
        descs  = ["8 prob z kazdego zadania", "Losowe, typowe wyniki"]
        for i in range(2):
            rect = _btn_rect(i)
            selected = i == self._selected
            hovered  = i == self._hover
            if selected or hovered:
                pygame.draw.rect(surface, _ORANGE, rect, border_radius=8)
                tc = _BG
            else:
                pygame.draw.rect(surface, _DIM, rect, 2, border_radius=8)
                tc = _DIM
            lbl = get_font(30).render(labels[i], True, tc)
            desc = get_font(22).render(descs[i], True, tc)
            surface.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.y + 22))
            surface.blit(desc, (rect.centerx - desc.get_width() // 2, rect.y + 60))

        hint = get_font(24).render("strzalki + ENTER = wybor  |  ESC = wstecz", True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 50))
