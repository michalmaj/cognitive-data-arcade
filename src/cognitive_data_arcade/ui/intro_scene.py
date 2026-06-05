from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_DIM = (100, 100, 150)

_FADE_MS = 100.0
_TITLE_TEXT = "COGNITIVE DATA ARCADE"


class TitleScene(Scene):
    def __init__(self, pm: ProfileManager, strings: Strings) -> None:
        self._pm = pm
        self._strings = strings
        self._alpha: float = 0.0
        self._done = False
        self._next: Scene | None = None
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 64)
        self._font_hint = pygame.font.SysFont(None, 26)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._alpha = 255.0
            if event.key == pygame.K_ESCAPE:
                self._pm.set_seen_intro(True)
                self._go_to_menu()
            else:
                self._advance()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._alpha = 255.0
            self._advance()

    def _advance(self) -> None:
        profile = self._pm.load()
        if not profile.seen_intro:
            from cognitive_data_arcade.ui.app_tutorial_scene import AppTutorialScene
            self._next = AppTutorialScene(self._pm, self._strings)
            self._done = True
        else:
            self._go_to_menu()

    def _go_to_menu(self) -> None:
        from cognitive_data_arcade.ui.menu import LessonMenuScene
        self._next = LessonMenuScene(self._pm, self._strings)
        self._done = True

    def update(self, dt_ms: float) -> None:
        if self._alpha < 255.0:
            self._alpha = min(255.0, self._alpha + 255.0 * dt_ms / _FADE_MS)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        title_surf = self._font_title.render(_TITLE_TEXT, True, _WHITE)
        hint_surf = self._font_hint.render(self._strings.intro_hint, True, _DIM)

        title_x = w // 2 - title_surf.get_width() // 2
        title_y = h // 2 - title_surf.get_height() // 2 - 20
        hint_x = w // 2 - hint_surf.get_width() // 2
        hint_y = title_y + title_surf.get_height() + 40

        overlay = pygame.Surface((w, h))
        overlay.fill(_BG)
        overlay.blit(title_surf, (title_x, title_y))
        overlay.blit(hint_surf, (hint_x, hint_y))
        overlay.set_alpha(int(self._alpha))
        surface.blit(overlay, (0, 0))
