from __future__ import annotations

import datetime
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import PausableGame
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.nback.config import (
    NBACK_1,
    NBACK_2,
    NBACK_3,
    NBACK_ADAPTIVE,
)
from cognitive_data_arcade.games.nback.game import NBackGame
from cognitive_data_arcade.games.nback.info import get_game_info
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene
from cognitive_data_arcade.ui.menu import LessonMenuScene

_BG = (26, 26, 46)
_TITLE_COLOR = (240, 240, 240)
_ITEM_COLOR = (160, 160, 160)
_HIGHLIGHT_COLOR = (243, 156, 18)
_NUM_OPTIONS = 4


class NBackLevelScene(Scene):
    def __init__(self, profile_manager: ProfileManager, strings: Strings) -> None:
        self._pm = profile_manager
        self._strings = strings
        self._selected = 0
        self._done = False
        self._next: Scene | None = None
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 52)
        self._font_item = pygame.font.SysFont(None, 34)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._next = LessonMenuScene(self._pm, self._strings)
            self._done = True
        elif event.key == pygame.K_UP:
            self._selected = max(0, self._selected - 1)
        elif event.key == pygame.K_DOWN:
            self._selected = min(_NUM_OPTIONS - 1, self._selected + 1)
        elif event.key == pygame.K_RETURN:
            self._launch()

    def _launch(self) -> None:
        configs = [NBACK_1, NBACK_2, NBACK_3, NBACK_ADAPTIVE]
        config = configs[self._selected]
        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "nback" / f"{sid}.csv"
        inner = NBackGame(config, self._pm, self._strings, pid, sid, csv_path)
        game_info = get_game_info(self._strings)
        restart_factory = lambda: NBackLevelScene(self._pm, self._strings)
        pausable = PausableGame(inner, game_info, restart_factory, self._strings, self._pm)
        self._next = HowToPlayScene(game_info, self._strings, back_scene=pausable)
        self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        _w, h = surface.get_size()

        title = self._font_title.render(self._strings.nback_level_title, True, _TITLE_COLOR)
        surface.blit(title, (60, 60))

        options = [
            self._strings.nback_level_1,
            self._strings.nback_level_2,
            self._strings.nback_level_3,
            self._strings.nback_level_adaptive,
        ]
        for i, label in enumerate(options):
            color = _HIGHLIGHT_COLOR if i == self._selected else _ITEM_COLOR
            prefix = ">> " if i == self._selected else "   "
            text = self._font_item.render(prefix + label, True, color)
            surface.blit(text, (80, 160 + i * 56))

        hint = self._font_item.render(self._strings.nback_level_hint, True, _ITEM_COLOR)
        surface.blit(hint, (60, h - 60))
