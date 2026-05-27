from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo
from cognitive_data_arcade.engine.scene import Scene

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_ORANGE = (243, 156, 18)
_DIM = (100, 100, 150)
_KEY_COLOR = (39, 174, 96)

_LEFT_MARGIN = 60
_TOP_Y = 50


class HowToPlayScene(Scene):
    def __init__(
        self,
        game_info: GameInfo,
        strings: Strings,
        back_scene: Scene | None,
    ) -> None:
        self._game_info = game_info
        self._strings = strings
        self._back_scene = back_scene
        self._done = False
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 54)
        self._font_desc = pygame.font.SysFont(None, 30)
        self._font_key = pygame.font.SysFont(None, 28)
        self._font_hint = pygame.font.SysFont(None, 26)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_SPACE,
            pygame.K_RETURN,
            pygame.K_ESCAPE,
        ):
            self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._back_scene if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()
        y = _TOP_Y

        title = self._font_title.render(self._game_info.title, True, _WHITE)
        surface.blit(title, (_LEFT_MARGIN, y))
        y += title.get_height() + 20

        pygame.draw.line(surface, _DIM, (_LEFT_MARGIN, y), (w - _LEFT_MARGIN, y))
        y += 16

        for line in self._game_info.description_lines:
            surf = self._font_desc.render(line, True, _DIM)
            surface.blit(surf, (_LEFT_MARGIN, y))
            y += surf.get_height() + 10
        y += 20

        header = self._font_key.render("Klawisze / Keys", True, _ORANGE)
        surface.blit(header, (_LEFT_MARGIN, y))
        y += header.get_height() + 10

        for key, desc in self._game_info.key_bindings:
            key_surf = self._font_key.render(key, True, _KEY_COLOR)
            surface.blit(key_surf, (_LEFT_MARGIN, y))
            desc_surf = self._font_key.render(desc, True, _WHITE)
            surface.blit(desc_surf, (_LEFT_MARGIN + 120, y))
            y += key_surf.get_height() + 8

        hint = self._font_hint.render(self._strings.howtoplay_hint_skip, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 40))
