from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.event_log_detective.scenarios import SCENARIOS
from cognitive_data_arcade.profile.manager import ProfileManager
from cognitive_data_arcade.ui.menu import LessonMenuScene

_BG = (26, 26, 46)
_TILE_W, _TILE_H = 200, 90
_TILE_GAP = 24
_SELECTED_COLOR = (243, 156, 18)
_HOVER_COLOR = (60, 60, 100)
_DIM = (100, 100, 150)
_WHITE = (240, 240, 240)
_TILES_X = 188
_ROW1_Y = 180
_ROW2_Y = 360


def _tile_rect(col: int, row_y: int) -> pygame.Rect:
    return pygame.Rect(_TILES_X + col * (_TILE_W + _TILE_GAP), row_y, _TILE_W, _TILE_H)


class EventLogLevelScene(Scene):
    def __init__(self, pm: ProfileManager, strings: Strings) -> None:
        self._pm = pm
        self._strings = strings
        self._exp_idx: int = 0
        self._diff_idx: int = 1
        self._active_row: int = 0
        self._hover_exp: int = -1
        self._hover_diff: int = -1
        self._done = False
        self._next: Scene | None = None
        self._font_title = get_font(52)
        self._font_row = get_font(36)
        self._font_tile = get_font(32)
        self._font_desc = get_font(26)
        self._font_hint = get_font(28)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            self._hover_exp = -1
            self._hover_diff = -1
            for i in range(3):
                if _tile_rect(i, _ROW1_Y).collidepoint(pos):
                    self._hover_exp = i
                if _tile_rect(i, _ROW2_Y).collidepoint(pos):
                    self._hover_diff = i
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for i in range(3):
                if _tile_rect(i, _ROW1_Y).collidepoint(pos):
                    self._exp_idx = i
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
                self._exp_idx = max(0, self._exp_idx - 1)
            else:
                self._diff_idx = max(0, self._diff_idx - 1)
        elif event.key == pygame.K_RIGHT:
            if self._active_row == 0:
                self._exp_idx = min(2, self._exp_idx + 1)
            else:
                self._diff_idx = min(2, self._diff_idx + 1)
        elif event.key == pygame.K_RETURN:
            self._launch()

    def _launch(self) -> None:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.event_log_detective.game import EventLogDetectiveGame
        from cognitive_data_arcade.games.event_log_detective.info import get_game_info
        from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

        difficulties = ["easy", "medium", "hard"]
        scenario = SCENARIOS[self._exp_idx]
        difficulty = difficulties[self._diff_idx]
        pm, strings = self._pm, self._strings

        inner = EventLogDetectiveGame(scenario, difficulty, strings, pm)
        game_info = get_game_info(strings)
        restart_factory = lambda: EventLogLevelScene(pm, strings)
        pausable = PausableGame(inner, game_info, restart_factory, strings, pm)
        self._next = HowToPlayScene(
            game_info,
            strings,
            back_scene=pausable,
            esc_scene=EventLogLevelScene(pm, strings),
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
        title = self._font_title.render("Event Log Detective", True, _WHITE)
        surface.blit(title, (60, 50))

        # Experiment row label — use small font so it fits before the first tile at x=188
        if self._strings.language == "pl":
            exp_label_text = "Eksperyment"
        else:
            exp_label_text = "Experiment"
        exp_label = self._font_hint.render(exp_label_text, True, _DIM)
        surface.blit(
            exp_label, (10, _ROW1_Y + (_TILE_H - self._font_hint.get_height()) // 2)
        )

        # Experiment tiles
        for i, scenario in enumerate(SCENARIOS):
            if self._strings.language == "pl":
                full_name = scenario.title_pl
            else:
                full_name = scenario.title_en
            # Split "Exp 3: Multi-site Clinical Study" into prefix + subtitle
            if ": " in full_name:
                prefix, subtitle = full_name.split(": ", 1)
            else:
                prefix, subtitle = full_name, ""
            n_decisions = len(scenario.decisions)
            desc = (
                f"{n_decisions} decisions"
                if self._strings.language == "en"
                else f"{n_decisions} decyzji"
            )
            rect = _tile_rect(i, _ROW1_Y)
            selected = i == self._exp_idx
            hovered = i == self._hover_exp
            if selected:
                pygame.draw.rect(surface, _SELECTED_COLOR, rect, border_radius=8)
                text_color = _BG
            elif hovered:
                pygame.draw.rect(surface, _HOVER_COLOR, rect, border_radius=8)
                text_color = _WHITE
            else:
                pygame.draw.rect(surface, _DIM, rect, 2, border_radius=8)
                text_color = _DIM
            # Clip rendering to tile rect to prevent overflow into adjacent tiles
            old_clip = surface.get_clip()
            surface.set_clip(rect)
            prefix_surf = self._font_tile.render(prefix, True, text_color)
            surface.blit(
                prefix_surf, (rect.centerx - prefix_surf.get_width() // 2, rect.y + 10)
            )
            if subtitle:
                sub_surf = self._font_desc.render(subtitle, True, text_color)
                surface.blit(
                    sub_surf,
                    (rect.centerx - sub_surf.get_width() // 2, rect.y + 40),
                )
            desc_surf = self._font_desc.render(desc, True, text_color)
            surface.blit(
                desc_surf, (rect.centerx - desc_surf.get_width() // 2, rect.y + 64)
            )
            surface.set_clip(old_clip)

        # Difficulty row label — same small font as experiment label
        diff_label = self._font_hint.render(self._strings.picker_difficulty, True, _DIM)
        surface.blit(
            diff_label, (10, _ROW2_Y + (_TILE_H - self._font_hint.get_height()) // 2)
        )

        diff_names = [
            self._strings.level_easy,
            self._strings.level_medium,
            self._strings.level_hard,
        ]
        if self._strings.language == "pl":
            diff_descs = [
                "efekty wyboru",
                "wskazówka [H]",
                "bez pomocy",
            ]
        else:
            diff_descs = [
                "see effects",
                "hint [H]",
                "no help",
            ]

        for i, (name, desc) in enumerate(zip(diff_names, diff_descs)):
            rect = _tile_rect(i, _ROW2_Y)
            selected = i == self._diff_idx
            hovered = i == self._hover_diff
            if selected:
                pygame.draw.rect(surface, _SELECTED_COLOR, rect, border_radius=8)
                text_color = _BG
            elif hovered:
                pygame.draw.rect(surface, _HOVER_COLOR, rect, border_radius=8)
                text_color = _WHITE
            else:
                pygame.draw.rect(surface, _DIM, rect, 2, border_radius=8)
                text_color = _DIM
            old_clip = surface.get_clip()
            surface.set_clip(rect)
            name_surf = self._font_tile.render(name, True, text_color)
            desc_surf = self._font_desc.render(desc, True, text_color)
            surface.blit(
                name_surf, (rect.centerx - name_surf.get_width() // 2, rect.y + 18)
            )
            surface.blit(
                desc_surf, (rect.centerx - desc_surf.get_width() // 2, rect.y + 52)
            )
            surface.set_clip(old_clip)

        # Active-row indicator
        active_row_y = _ROW1_Y if self._active_row == 0 else _ROW2_Y
        indicator_rect = pygame.Rect(_TILES_X - 12, active_row_y + 35, 4, 20)
        pygame.draw.rect(surface, _SELECTED_COLOR, indicator_rect)

        # Hint at bottom center
        hint = self._font_hint.render(self._strings.level_hint, True, _DIM)
        surface.blit(hint, (w // 2 - hint.get_width() // 2, h - 50))
