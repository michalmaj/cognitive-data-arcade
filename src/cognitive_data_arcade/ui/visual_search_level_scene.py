from __future__ import annotations

import datetime
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import PausableGame
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

_BG              = (26, 26, 46)
_TILE_W, _TILE_H = 200, 90
_TILE_GAP        = 24
_SELECTED_COLOR  = (243, 156, 18)
_HOVER_COLOR     = (60, 60, 100)
_DIM             = (100, 100, 150)
_WHITE           = (240, 240, 240)
_TILES_X         = 188
_ROW1_Y          = 180   # mode row y
_ROW2_Y          = 360   # difficulty row y

_MODES       = ("letters", "shapes")
_MODE_LABELS = ("Litery", "Kształty")
_MODE_DESCS  = ("X/O  T/L", "koła / kwadraty")

_DIFFS       = ("easy", "medium", "hard")
_DIFF_LABELS = ("Łatwy", "Średni", "Trudny")
_DIFF_DESCS  = ("8 el.", "16 el.", "24 el.")


def _tile_rect(col: int, row_y: int) -> pygame.Rect:
    return pygame.Rect(_TILES_X + col * (_TILE_W + _TILE_GAP), row_y, _TILE_W, _TILE_H)


class VisualSearchLevelScene(Scene):
    def __init__(self, pm: ProfileManager, strings: Strings) -> None:
        self._pm = pm
        self._strings = strings
        self._mode_idx: int = 0     # default: Letters
        self._diff_idx: int = 1     # default: Medium
        self._active_row: int = 0   # 0=mode row, 1=difficulty row
        self._hover_mode: int = -1
        self._hover_diff: int = -1
        self._done = False
        self._next: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self._hover_mode = -1
            self._hover_diff = -1
            for i in range(2):
                if _tile_rect(i, _ROW1_Y).collidepoint(pos):
                    self._hover_mode = i
            for i in range(3):
                if _tile_rect(i, _ROW2_Y).collidepoint(pos):
                    self._hover_diff = i
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for i in range(2):
                if _tile_rect(i, _ROW1_Y).collidepoint(pos):
                    self._mode_idx = i
                    self._active_row = 0
                    return
            for i in range(3):
                if _tile_rect(i, _ROW2_Y).collidepoint(pos):
                    self._diff_idx = i
                    self._active_row = 1
                    return
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            from cognitive_data_arcade.ui.menu import LessonMenuScene
            self._next = LessonMenuScene(self._pm, self._strings)
            self._done = True
        elif event.key == pygame.K_UP:
            self._active_row = 0
        elif event.key == pygame.K_DOWN:
            self._active_row = 1
        elif event.key == pygame.K_LEFT:
            if self._active_row == 0:
                self._mode_idx = max(0, self._mode_idx - 1)
            else:
                self._diff_idx = max(0, self._diff_idx - 1)
        elif event.key == pygame.K_RIGHT:
            if self._active_row == 0:
                self._mode_idx = min(1, self._mode_idx + 1)
            else:
                self._diff_idx = min(2, self._diff_idx + 1)
        elif event.key == pygame.K_RETURN:
            self._launch()

    def _launch(self) -> None:
        from cognitive_data_arcade.games.visual_search.config import VSConfig
        from cognitive_data_arcade.games.visual_search.game import VisualSearchGame
        from cognitive_data_arcade.games.visual_search.info import get_game_info

        mode = _MODES[self._mode_idx]
        diff = _DIFFS[self._diff_idx]
        cfg  = VSConfig(mode=mode, difficulty=diff)

        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "visual_search" / f"{sid}.csv"

        inner     = VisualSearchGame(cfg, self._pm, self._strings, pid, sid, csv_path)
        game_info = get_game_info(self._strings)
        restart_factory = lambda: VisualSearchLevelScene(self._pm, self._strings)
        pausable  = PausableGame(inner, game_info, restart_factory, self._strings, self._pm)
        self._next = HowToPlayScene(
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=VisualSearchLevelScene(self._pm, self._strings),
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

        font_title = get_font(48)
        font_row   = get_font(32)
        font_tile  = get_font(28)
        font_desc  = get_font(22)
        font_hint  = get_font(24)

        title = font_title.render("Visual Search Lab", True, _WHITE)
        surface.blit(title, (60, 50))

        # Mode row (2 tiles)
        mode_label = font_row.render("Tryb bodźców", True, _DIM)
        surface.blit(mode_label, (60, _ROW1_Y - font_row.get_height() - 8))
        for i, (name, desc) in enumerate(zip(_MODE_LABELS, _MODE_DESCS)):
            rect = _tile_rect(i, _ROW1_Y)
            selected = (i == self._mode_idx)
            hovered  = (i == self._hover_mode)
            if selected:
                pygame.draw.rect(surface, _SELECTED_COLOR, rect, border_radius=8)
                tc = _BG
            elif hovered:
                pygame.draw.rect(surface, _HOVER_COLOR, rect, border_radius=8)
                tc = _WHITE
            else:
                pygame.draw.rect(surface, _DIM, rect, 2, border_radius=8)
                tc = _DIM
            ns = font_tile.render(name, True, tc)
            ds = font_desc.render(desc, True, tc)
            surface.blit(ns, (rect.centerx - ns.get_width() // 2, rect.y + 18))
            surface.blit(ds, (rect.centerx - ds.get_width() // 2, rect.y + 52))

        # Difficulty row (3 tiles)
        diff_label = font_row.render("Trudność", True, _DIM)
        surface.blit(diff_label, (60, _ROW2_Y - font_row.get_height() - 8))
        for i, (name, desc) in enumerate(zip(_DIFF_LABELS, _DIFF_DESCS)):
            rect = _tile_rect(i, _ROW2_Y)
            selected = (i == self._diff_idx)
            hovered  = (i == self._hover_diff)
            if selected:
                pygame.draw.rect(surface, _SELECTED_COLOR, rect, border_radius=8)
                tc = _BG
            elif hovered:
                pygame.draw.rect(surface, _HOVER_COLOR, rect, border_radius=8)
                tc = _WHITE
            else:
                pygame.draw.rect(surface, _DIM, rect, 2, border_radius=8)
                tc = _DIM
            ns = font_tile.render(name, True, tc)
            ds = font_desc.render(desc, True, tc)
            surface.blit(ns, (rect.centerx - ns.get_width() // 2, rect.y + 18))
            surface.blit(ds, (rect.centerx - ds.get_width() // 2, rect.y + 52))

        # Active-row indicator (orange bar to the left of active row)
        active_y = _ROW1_Y if self._active_row == 0 else _ROW2_Y
        pygame.draw.rect(surface, _SELECTED_COLOR,
                         (_TILES_X - 12, active_y + 35, 4, 20))

        # Bottom hint
        hint = font_hint.render("ENTER — start  |  ESC — wstecz", True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 50))
