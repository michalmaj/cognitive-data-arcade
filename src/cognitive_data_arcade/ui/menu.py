from __future__ import annotations

from pathlib import Path

import pygame

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.i18n import Strings, get_strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_LESSONS = [
    (1, "Big Data in Cognitive Science"),
    (2, "Reaction Time Lab"),
    (3, "Event Logs and Data Formats"),
    (4, "Data Quality Lab"),
    (6, "Exploratory Data Analysis"),
    (7, "Stroop Challenge"),
    (8, "Flanker Arena"),
    (9, "Go/No-Go Guard"),
    (10, "N-Back Memory Grid"),
]

_BG = (26, 26, 46)
_TITLE_COLOR = (240, 240, 240)
_ITEM_COLOR = (160, 160, 160)
_HIGHLIGHT_COLOR = (243, 156, 18)

_MENU_TOP = 140
_ROW_H = 44
_POPUP_W = 320
_POPUP_H = 160


class LessonMenuScene(Scene):
    def __init__(self, profile_manager: ProfileManager, strings: Strings, selected: int = 0) -> None:
        self._pm = profile_manager
        self._strings = strings
        self._selected = selected
        self._next: Scene | None = None
        self._done = False
        self._popup_visible: bool = False
        self._popup_selected: int = 0  # 0=Play, 1=Teoria
        audio.play_music("menu")
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 52)
        self._font_item = pygame.font.SysFont(None, 34)

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._popup_visible:
            self._handle_popup_event(event)
            return
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            idx = (y - _MENU_TOP) // _ROW_H
            if 0 <= idx < len(_LESSONS):
                self._selected = idx
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            idx = (y - _MENU_TOP) // _ROW_H
            if 0 <= idx < len(_LESSONS):
                self._selected = idx
                self._popup_visible = True
                self._popup_selected = 0
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._done = True
        elif event.key == pygame.K_UP:
            self._selected = max(0, self._selected - 1)
            audio.play_sfx("navigate")
        elif event.key == pygame.K_DOWN:
            self._selected = min(len(_LESSONS) - 1, self._selected + 1)
            audio.play_sfx("navigate")
        elif event.key == pygame.K_p:
            from cognitive_data_arcade.ui.profile_screen import ProfileScene

            back = LessonMenuScene(self._pm, self._strings, self._selected)
            self._next = ProfileScene(self._pm, self._strings, back)
            self._done = True
        elif event.key == pygame.K_l:
            new_lang = "en" if self._strings.language == "pl" else "pl"
            self._pm.set_language(new_lang)
            self._strings = get_strings(new_lang)
        elif event.key == pygame.K_a:
            from cognitive_data_arcade.ui.session_picker import SessionPickerScene

            sessions_dir = Path("data") / "generated" / "reaction_time"
            self._next = SessionPickerScene(sessions_dir, self._strings, self._pm)
            self._done = True
        elif event.key == pygame.K_RETURN:
            self._launch_selected_game()
        elif event.key == pygame.K_o:
            from cognitive_data_arcade.ui.options_scene import OptionsScene

            back = LessonMenuScene(self._pm, self._strings, self._selected)
            self._next = OptionsScene(self._pm, self._strings, back)
            self._done = True
        elif event.key == pygame.K_t:
            lesson_num = _LESSONS[self._selected][0]
            if lesson_num in (1, 2, 3, 4, 6, 7, 8, 9, 10):
                from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene

                back = LessonMenuScene(self._pm, self._strings, self._selected)
                self._next = LessonReaderScene(
                    lesson_num, self._strings, back,
                    play_factory=self._game_factory_for(lesson_num),
                )
                self._done = True
        elif event.key == pygame.K_z:
            self._launch_stroop_picker()

    def _launch_selected_game(self) -> None:
        audio.play_sfx("select")
        lesson_num = _LESSONS[self._selected][0]
        if lesson_num == 1:
            self._launch_big_data_map()
        elif lesson_num == 2:
            self._launch_rt_lab()
        elif lesson_num == 3:
            self._launch_event_log_detective()
        elif lesson_num == 4:
            self._launch_data_cleaning()
        elif lesson_num == 8:
            self._launch_flanker()
        elif lesson_num == 9:
            self._launch_gono()
        elif lesson_num == 10:
            self._launch_nback()
        elif lesson_num == 6:
            self._launch_eda()
        elif lesson_num == 7:
            self._launch_stroop()

    def _teoria_available(self) -> bool:
        lesson_num = _LESSONS[self._selected][0]
        return lesson_num in (1, 2, 3, 4, 6, 7, 8, 9, 10)

    def _handle_popup_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._popup_visible = False
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_TAB):
                self._popup_selected = 1 - self._popup_selected
            elif event.key == pygame.K_RETURN:
                self._confirm_popup()
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            surf = pygame.display.get_surface()
            if surf is None:
                return
            w, h = surf.get_size()
            px = (w - _POPUP_W) // 2
            py = (h - _POPUP_H) // 2
            play_rect = pygame.Rect(px + 20, py + 80, 120, 40)
            teoria_rect = pygame.Rect(px + 180, py + 80, 120, 40)
            from cognitive_data_arcade.engine.mouse import hit
            if event.type == pygame.MOUSEMOTION:
                if hit(play_rect, event.pos):
                    self._popup_selected = 0
                elif hit(teoria_rect, event.pos) and self._teoria_available():
                    self._popup_selected = 1
            elif event.button == 1:
                if hit(play_rect, event.pos):
                    self._popup_selected = 0
                    self._confirm_popup()
                elif hit(teoria_rect, event.pos) and self._teoria_available():
                    self._popup_selected = 1
                    self._confirm_popup()

    def _game_factory_for(self, lesson_num: int):
        if lesson_num == 1:
            return self._make_big_data_map_game
        if lesson_num == 2:
            return self._make_rt_lab_game
        if lesson_num == 3:
            pm, strings = self._pm, self._strings

            def _make_eld() -> Scene:
                from cognitive_data_arcade.ui.event_log_level_scene import EventLogLevelScene
                return EventLogLevelScene(pm, strings)

            return _make_eld
        if lesson_num == 4:
            return self._make_data_cleaning_game
        if lesson_num == 6:
            return self._make_eda_game
        if lesson_num == 7:
            pm, strings = self._pm, self._strings
            def _make_stroop():
                from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene
                return StroopLevelScene(pm, strings)
            return _make_stroop
        if lesson_num == 8:
            pm, strings = self._pm, self._strings
            def _make_flanker():
                from cognitive_data_arcade.ui.flanker_level_scene import FlankerLevelScene
                return FlankerLevelScene(pm, strings)
            return _make_flanker
        if lesson_num == 9:
            pm, strings = self._pm, self._strings
            def _make_gono():
                from cognitive_data_arcade.ui.gono_level_scene import GoNoGoLevelScene
                return GoNoGoLevelScene(pm, strings)
            return _make_gono
        if lesson_num == 10:
            pm, strings = self._pm, self._strings
            def _make_nback():
                from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene
                return NBackLevelScene(pm, strings)
            return _make_nback
        return None

    def _confirm_popup(self) -> None:
        self._popup_visible = False
        if self._popup_selected == 0:
            self._launch_selected_game()
        elif self._popup_selected == 1 and self._teoria_available():
            lesson_num = _LESSONS[self._selected][0]
            from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene

            back = LessonMenuScene(self._pm, self._strings, self._selected)
            self._next = LessonReaderScene(
                lesson_num, self._strings, back,
                play_factory=self._game_factory_for(lesson_num),
            )
            self._done = True

    def _draw_popup(self, surface: pygame.Surface) -> None:
        w, h = surface.get_size()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))
        px = (w - _POPUP_W) // 2
        py = (h - _POPUP_H) // 2
        pygame.draw.rect(surface, (18, 18, 42), (px, py, _POPUP_W, _POPUP_H), border_radius=8)
        pygame.draw.rect(surface, (42, 42, 80), (px, py, _POPUP_W, _POPUP_H), 1, border_radius=8)
        name = _LESSONS[self._selected][1]
        title_surf = self._font_item.render(name, True, (240, 240, 240))
        surface.blit(title_surf, (px + _POPUP_W // 2 - title_surf.get_width() // 2, py + 16))
        play_color = _HIGHLIGHT_COLOR if self._popup_selected == 0 else _ITEM_COLOR
        play_surf = self._font_item.render(f"[ {self._strings.label_play_game} ]", True, play_color)
        surface.blit(play_surf, (px + 20, py + 80))
        teoria_color = (70, 70, 112)
        if self._teoria_available():
            teoria_color = _HIGHLIGHT_COLOR if self._popup_selected == 1 else _ITEM_COLOR
        teoria_surf = self._font_item.render(f"[ {self._strings.label_theory_lesson} ]", True, teoria_color)
        surface.blit(teoria_surf, (px + 180, py + 80))
        hint_surf = self._font_item.render(self._strings.label_esc_close, True, (70, 70, 112))
        surface.blit(hint_surf, (px + _POPUP_W // 2 - hint_surf.get_width() // 2, py + _POPUP_H - 30))

    def _launch_big_data_map(self) -> None:
        self._next = self._make_big_data_map_game()
        self._done = True

    def _make_big_data_map_game(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame
        from cognitive_data_arcade.games.big_data_map.info import get_game_info
        from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

        inner = BigDataMapGame(self._strings, self._pm)
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_big_data_map_game, self._strings, self._pm
        )
        return HowToPlayScene(
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_rt_lab(self) -> None:
        self._next = self._make_rt_lab_game()
        self._done = True

    def _launch_event_log_detective(self) -> None:
        from cognitive_data_arcade.ui.event_log_level_scene import EventLogLevelScene

        self._next = EventLogLevelScene(self._pm, self._strings)
        self._done = True

    def _make_rt_lab_game(self) -> Scene:
        import datetime

        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.reaction_time.config import DEFAULT_CONFIG
        from cognitive_data_arcade.games.reaction_time.game import ReactionTimeGame
        from cognitive_data_arcade.games.reaction_time.info import get_game_info
        from cognitive_data_arcade.ui.how_to_play_scene import HowToPlayScene

        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "reaction_time" / f"{sid}.csv"
        inner = ReactionTimeGame(
            DEFAULT_CONFIG, self._pm, self._strings, pid, sid, csv_path
        )
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_rt_lab_game, self._strings, self._pm
        )
        return HowToPlayScene(
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_data_cleaning(self) -> None:
        self._next = self._make_data_cleaning_game()
        self._done = True

    def _make_data_cleaning_game(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.data_cleaning.info import get_game_info
        from cognitive_data_arcade.games.data_cleaning.scene import DataCleaningScene

        inner = DataCleaningScene(self._strings, self._pm)
        game_info = get_game_info(self._strings)
        # DataCleaningScene has its own INTRO phase; HowToPlayScene is redundant
        return PausableGame(
            inner, game_info, self._make_data_cleaning_game, self._strings, self._pm
        )

    def _launch_eda(self) -> None:
        self._next = self._make_eda_game()
        self._done = True

    def _make_eda_game(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.eda.info import get_game_info
        from cognitive_data_arcade.games.eda.scene import EDAScene

        inner = EDAScene()
        game_info = get_game_info(self._strings)
        return PausableGame(
            inner, game_info, self._make_eda_game, self._strings, self._pm
        )

    def _launch_stroop(self) -> None:
        from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene

        self._next = StroopLevelScene(self._pm, self._strings)
        self._done = True

    def _launch_stroop_picker(self) -> None:
        from cognitive_data_arcade.ui.stroop_session_picker import (
            StroopSessionPickerScene,
        )

        sessions_dir = Path("data") / "generated" / "stroop"
        self._next = StroopSessionPickerScene(sessions_dir, self._strings, self._pm)
        self._done = True

    def _launch_flanker(self) -> None:
        from cognitive_data_arcade.ui.flanker_level_scene import FlankerLevelScene

        self._next = FlankerLevelScene(self._pm, self._strings)
        self._done = True

    def _launch_gono(self) -> None:
        from cognitive_data_arcade.ui.gono_level_scene import GoNoGoLevelScene

        self._next = GoNoGoLevelScene(self._pm, self._strings)
        self._done = True

    def _launch_nback(self) -> None:
        from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene

        self._next = NBackLevelScene(self._pm, self._strings)
        self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)

        title = self._font_title.render(self._strings.menu_title, True, _TITLE_COLOR)
        surface.blit(title, (40, 36))

        subtitle = self._font_item.render(
            self._strings.menu_subtitle, True, _ITEM_COLOR
        )
        surface.blit(subtitle, (42, 96))

        for i, (num, name) in enumerate(_LESSONS):
            color = _HIGHLIGHT_COLOR if i == self._selected else _ITEM_COLOR
            text = self._font_item.render(f"{i + 1:02d}.  {name}", True, color)
            surface.blit(text, (60, 140 + i * 44))

        if self._popup_visible:
            self._draw_popup(surface)
