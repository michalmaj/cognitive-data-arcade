from __future__ import annotations

import datetime
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import PausableGame
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.stroop.config import EASY, MEDIUM, HARD
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene
from cognitive_data_arcade.ui.menu import LessonMenuScene

_BG = (26, 26, 46)
_TILE_W, _TILE_H = 200, 90
_TILE_GAP = 24
_SELECTED_COLOR = (243, 156, 18)   # orange
_HOVER_COLOR = (60, 60, 100)
_DIM = (100, 100, 150)
_WHITE = (240, 240, 240)
_TILES_X = 188   # x of first tile (centers 3 tiles in 1024px: (1024 - 3*200 - 2*24) / 2 = 188)
_ROW_Y = 280     # single row y position (single-axis picker)


def _tile_rect(col: int, row_y: int) -> pygame.Rect:
    return pygame.Rect(_TILES_X + col * (_TILE_W + _TILE_GAP), row_y, _TILE_W, _TILE_H)


class StroopLevelScene(Scene):
    def __init__(self, pm: ProfileManager, strings: Strings) -> None:
        self._pm = pm
        self._strings = strings
        self._diff_idx: int = 1  # default Medium
        self._done = False
        self._next: Scene | None = None
        self._hover_diff: int = -1  # which tile is hovered (-1 = none)
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 52)
        self._font_row = pygame.font.SysFont(None, 36)
        self._font_tile = pygame.font.SysFont(None, 32)
        self._font_desc = pygame.font.SysFont(None, 26)
        self._font_hint = pygame.font.SysFont(None, 28)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._hover_diff = -1
            for col in range(3):
                if _tile_rect(col, _ROW_Y).collidepoint(event.pos):
                    self._hover_diff = col
                    break
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for col in range(3):
                if _tile_rect(col, _ROW_Y).collidepoint(event.pos):
                    self._diff_idx = col
                    break
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._next = LessonMenuScene(self._pm, self._strings)
            self._done = True
        elif event.key == pygame.K_LEFT:
            self._diff_idx = max(0, self._diff_idx - 1)
        elif event.key == pygame.K_RIGHT:
            self._diff_idx = min(2, self._diff_idx + 1)
        elif event.key == pygame.K_RETURN:
            self._launch()

    def _launch(self) -> None:
        configs = [EASY, MEDIUM, HARD]
        config = configs[self._diff_idx]
        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "stroop" / f"{sid}.csv"
        from cognitive_data_arcade.games.stroop.game import StroopGame
        from cognitive_data_arcade.games.stroop.info import get_game_info
        inner = StroopGame(config, self._pm, self._strings, pid, sid, csv_path)
        game_info = get_game_info(self._strings)
        restart_factory = lambda: StroopLevelScene(self._pm, self._strings)
        pausable = PausableGame(inner, game_info, restart_factory, self._strings, self._pm)
        self._next = HowToPlayScene(
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=StroopLevelScene(self._pm, self._strings),
        )
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

        # Title
        title = self._font_title.render(self._strings.stroop_title, True, _WHITE)
        surface.blit(title, (60, 50))

        # Row label
        row_label = self._font_row.render(self._strings.picker_difficulty, True, _DIM)
        surface.blit(row_label, (60, _ROW_Y + (_TILE_H - self._font_row.get_height()) // 2))

        # Tiles
        names = [self._strings.level_easy, self._strings.level_medium, self._strings.level_hard]
        descs = [self._strings.stroop_easy_desc, self._strings.stroop_medium_desc, self._strings.stroop_hard_desc]
        for i, (name, desc) in enumerate(zip(names, descs)):
            rect = _tile_rect(i, _ROW_Y)
            selected = (i == self._diff_idx)
            hovered = (i == self._hover_diff)
            if selected:
                pygame.draw.rect(surface, _SELECTED_COLOR, rect, border_radius=8)
                text_color = _BG
            elif hovered:
                pygame.draw.rect(surface, _HOVER_COLOR, rect, border_radius=8)
                text_color = _WHITE
            else:
                pygame.draw.rect(surface, _DIM, rect, 2, border_radius=8)
                text_color = _DIM
            name_surf = self._font_tile.render(name, True, text_color)
            desc_surf = self._font_desc.render(desc, True, text_color)
            surface.blit(name_surf, (rect.centerx - name_surf.get_width() // 2, rect.y + 18))
            surface.blit(desc_surf, (rect.centerx - desc_surf.get_width() // 2, rect.y + 52))

        # Hint
        hint = self._font_hint.render(self._strings.level_hint, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 50))
