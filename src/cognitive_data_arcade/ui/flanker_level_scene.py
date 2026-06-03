from __future__ import annotations

import dataclasses
import datetime
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import PausableGame
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.flanker.config import (
    QUICK, STANDARD, FULL,
    DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD,
)
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene
from cognitive_data_arcade.ui.menu import LessonMenuScene

_BG = (26, 26, 46)
_TILE_W, _TILE_H = 200, 90
_TILE_GAP = 24
_SELECTED_COLOR = (243, 156, 18)
_HOVER_COLOR = (60, 60, 100)
_DIM = (100, 100, 150)
_WHITE = (240, 240, 240)
_TILES_X = 188
_ROW1_Y = 180   # session row y
_ROW2_Y = 360   # difficulty row y


def _tile_rect(col: int, row_y: int) -> pygame.Rect:
    return pygame.Rect(_TILES_X + col * (_TILE_W + _TILE_GAP), row_y, _TILE_W, _TILE_H)


class FlankerLevelScene(Scene):
    def __init__(self, pm: ProfileManager, strings: Strings) -> None:
        self._pm = pm
        self._strings = strings
        self._session_idx: int = 1  # default Standard
        self._diff_idx: int = 1     # default Medium
        self._active_row: int = 0   # 0=session row, 1=difficulty row
        self._hover_session: int = -1
        self._hover_diff: int = -1
        self._done = False
        self._next: Scene | None = None
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 52)
        self._font_row = pygame.font.SysFont(None, 36)
        self._font_tile = pygame.font.SysFont(None, 32)
        self._font_desc = pygame.font.SysFont(None, 26)
        self._font_hint = pygame.font.SysFont(None, 28)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self._hover_session = -1
            self._hover_diff = -1
            for i in range(3):
                if _tile_rect(i, _ROW1_Y).collidepoint(pos):
                    self._hover_session = i
                if _tile_rect(i, _ROW2_Y).collidepoint(pos):
                    self._hover_diff = i
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for i in range(3):
                if _tile_rect(i, _ROW1_Y).collidepoint(pos):
                    self._session_idx = i
                    self._active_row = 0
                    return
                if _tile_rect(i, _ROW2_Y).collidepoint(pos):
                    self._diff_idx = i
                    self._active_row = 1
                    return
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._next = LessonMenuScene(self._pm, self._strings)
            self._done = True
        elif event.key == pygame.K_UP:
            self._active_row = 0
        elif event.key == pygame.K_DOWN:
            self._active_row = 1
        elif event.key == pygame.K_LEFT:
            if self._active_row == 0:
                self._session_idx = max(0, self._session_idx - 1)
            else:
                self._diff_idx = max(0, self._diff_idx - 1)
        elif event.key == pygame.K_RIGHT:
            if self._active_row == 0:
                self._session_idx = min(2, self._session_idx + 1)
            else:
                self._diff_idx = min(2, self._diff_idx + 1)
        elif event.key == pygame.K_RETURN:
            self._launch()

    def _launch(self) -> None:
        from cognitive_data_arcade.games.flanker.game import FlankerGame
        from cognitive_data_arcade.games.flanker.info import get_game_info
        session_presets = [QUICK, STANDARD, FULL]
        diff_overrides = [DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD]
        config = dataclasses.replace(session_presets[self._session_idx], **diff_overrides[self._diff_idx])
        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "flanker" / f"{sid}.csv"
        inner = FlankerGame(config, self._pm, self._strings, pid, sid, csv_path)
        game_info = get_game_info(self._strings)
        restart_factory = lambda: FlankerLevelScene(self._pm, self._strings)
        pausable = PausableGame(inner, game_info, restart_factory, self._strings, self._pm)
        self._next = HowToPlayScene(
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=FlankerLevelScene(self._pm, self._strings),
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
        title = self._font_title.render("Flanker", True, _WHITE)
        surface.blit(title, (60, 50))

        # Session row
        session_label = self._font_row.render(self._strings.picker_session, True, _DIM)
        surface.blit(session_label, (60, _ROW1_Y + (_TILE_H - self._font_row.get_height()) // 2))

        session_names = [
            self._strings.level_quick,
            self._strings.level_standard,
            self._strings.level_full,
        ]
        session_descs = [
            f"24 {self._strings.level_trials_suffix}",
            f"48 {self._strings.level_trials_suffix}",
            f"96 {self._strings.level_trials_suffix}",
        ]
        for i, (name, desc) in enumerate(zip(session_names, session_descs)):
            rect = _tile_rect(i, _ROW1_Y)
            selected = (i == self._session_idx)
            hovered = (i == self._hover_session)
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

        # Difficulty row
        diff_label = self._font_row.render(self._strings.picker_difficulty, True, _DIM)
        surface.blit(diff_label, (60, _ROW2_Y + (_TILE_H - self._font_row.get_height()) // 2))

        diff_names = [
            self._strings.level_easy,
            self._strings.level_medium,
            self._strings.level_hard,
        ]
        diff_descs = [
            self._strings.flanker_easy_desc,
            self._strings.flanker_medium_desc,
            self._strings.flanker_hard_desc,
        ]
        for i, (name, desc) in enumerate(zip(diff_names, diff_descs)):
            rect = _tile_rect(i, _ROW2_Y)
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

        # Active-row indicator: small orange filled rect to the left of the active row
        active_row_y = _ROW1_Y if self._active_row == 0 else _ROW2_Y
        indicator_rect = pygame.Rect(_TILES_X - 12, active_row_y + 35, 4, 20)
        pygame.draw.rect(surface, _SELECTED_COLOR, indicator_rect)

        # Hint at bottom center
        hint = self._font_hint.render(self._strings.level_hint, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 50))
