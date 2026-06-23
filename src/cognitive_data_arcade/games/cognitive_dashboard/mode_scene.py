from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession
from cognitive_data_arcade.profile.manager import ProfileManager

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
    GREEN as _GREEN,
    ORANGE as _ORANGE,
)

_W, _H = 1024, 768

_BTN_W, _BTN_H = 290, 110
_BTN_GAP = 28
_BTN_Y = 300
_N_BTNS = 3


def _btn_rect(idx: int) -> pygame.Rect:
    total = _N_BTNS * _BTN_W + (_N_BTNS - 1) * _BTN_GAP
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

        from cognitive_data_arcade.games.cognitive_dashboard.csv_loader import has_any_csv_data

        self._has_data = has_any_csv_data()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._hover = -1
            for i in range(_N_BTNS):
                if _btn_rect(i).collidepoint(event.pos):
                    self._hover = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(_N_BTNS):
                if _btn_rect(i).collidepoint(event.pos):
                    self._launch(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from cognitive_data_arcade.ui.menu import LessonMenuScene

                self._next = LessonMenuScene(self._pm, self._strings)
                self._done = True
            elif event.key in (pygame.K_LEFT, pygame.K_TAB):
                self._selected = (self._selected - 1) % _N_BTNS
            elif event.key == pygame.K_RIGHT:
                self._selected = (self._selected + 1) % _N_BTNS
            elif event.key == pygame.K_RETURN:
                self._launch(self._selected)

    def _launch(self, idx: int) -> None:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.cognitive_dashboard.config import generate_synthetic
        from cognitive_data_arcade.games.cognitive_dashboard.csv_loader import (
            load_session_from_csv,
        )
        from cognitive_data_arcade.games.cognitive_dashboard.dashboard_scene import (
            CognitiveDashboardScene,
        )
        from cognitive_data_arcade.games.cognitive_dashboard.info import get_game_info

        if idx == 0:
            session = load_session_from_csv()
        elif idx == 1:
            session = DashboardSession()
        else:
            session = generate_synthetic()

        strings, pm = self._strings, self._pm

        def make_dashboard() -> Scene:
            inner = CognitiveDashboardScene(session, strings, pm)
            return PausableGame(inner, get_game_info(strings), make_dashboard, strings, pm)

        self._next = make_dashboard()
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

        subtitle = get_font(26).render("Lekcja 12 -- Porownywanie zadan poznawczych", True, _DIM)
        surface.blit(subtitle, (w // 2 - subtitle.get_width() // 2, 165))

        labels = ["Moje dane", "Zagraj teraz", "Dane syntetyczne"]
        descs = [
            "CSV z poprzednich sesji" if self._has_data else "Brak zapisanych sesji",
            "8 prob z kazdego zadania",
            "Losowe, typowe wyniki",
        ]
        colors = [_GREEN if self._has_data else _DIM, _ORANGE, _DIM]

        for i in range(_N_BTNS):
            rect = _btn_rect(i)
            selected = i == self._selected
            hovered = i == self._hover
            btn_color = colors[i]
            if selected or hovered:
                pygame.draw.rect(surface, btn_color, rect, border_radius=8)
                tc = _BG
            else:
                pygame.draw.rect(surface, btn_color, rect, 2, border_radius=8)
                tc = btn_color
            lbl = get_font(26).render(labels[i], True, tc)
            desc = get_font(19).render(descs[i], True, tc)
            surface.blit(lbl, (rect.centerx - lbl.get_width() // 2, rect.y + 26))
            surface.blit(desc, (rect.centerx - desc.get_width() // 2, rect.y + 68))

        hint = get_font(22).render("strzalki + ENTER = wybor  |  ESC = wstecz", True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 44))
