from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_ORANGE = (243, 156, 18)
_GREEN = (39, 174, 96)
_DIM = (100, 100, 150)

_LEFT = 80
_TITLE_Y = 60
_DIVIDER_Y = 110
_KEYS_Y = 135
_ROW_H = 46
_KEY_COL_W = 180


class AppTutorialScene(Scene):
    def __init__(self, pm: ProfileManager, strings: Strings) -> None:
        self._pm = pm
        self._strings = strings
        self._done = False
        self._next: Scene | None = None
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 44)
        self._font_key = pygame.font.SysFont(None, 30)
        self._font_hint = pygame.font.SysFont(None, 26)
        self._key_rows: list[tuple[str, str]] = [
            ("UP / DOWN", strings.app_tutorial_nav),
            ("ENTER", strings.app_tutorial_enter),
            ("T", strings.app_tutorial_theory),
            ("P", strings.app_tutorial_profile),
            ("O", strings.app_tutorial_options),
        ]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._exit()
        elif event.type == pygame.KEYDOWN and event.key in (
            pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE
        ):
            self._exit()

    def _exit(self) -> None:
        from cognitive_data_arcade.ui.menu import LessonMenuScene
        self._pm.set_seen_intro(True)
        self._next = LessonMenuScene(self._pm, self._strings)
        self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        title = self._font_title.render(self._strings.app_tutorial_title, True, _ORANGE)
        surface.blit(title, (_LEFT, _TITLE_Y))

        pygame.draw.line(surface, _DIM, (_LEFT, _DIVIDER_Y), (w - _LEFT, _DIVIDER_Y))

        y = _KEYS_Y
        for key_label, desc in self._key_rows:
            key_surf = self._font_key.render(key_label, True, _GREEN)
            surface.blit(key_surf, (_LEFT, y))
            desc_surf = self._font_key.render(desc, True, _WHITE)
            surface.blit(desc_surf, (_LEFT + _KEY_COL_W, y))
            y += _ROW_H

        hint = self._font_hint.render(self._strings.app_tutorial_hint, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 44))
