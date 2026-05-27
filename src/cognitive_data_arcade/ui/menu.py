from __future__ import annotations

from pathlib import Path

import pygame

from cognitive_data_arcade.engine.i18n import Strings, get_strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import ProfileManager

_LESSONS = [
    (1, "Big Data in Cognitive Science"),
    (2, "Reaction Time Lab"),
    (3, "Event Logs and Data Formats"),
    (4, "Data Cleaning"),
    (5, "Missing Values and Outliers"),
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


class LessonMenuScene(Scene):
    def __init__(self, profile_manager: ProfileManager, strings: Strings) -> None:
        self._pm = profile_manager
        self._strings = strings
        self._selected = 0
        self._next: Scene | None = None
        self._done = False
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 52)
        self._font_item = pygame.font.SysFont(None, 34)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self._done = True
        elif event.key == pygame.K_UP:
            self._selected = max(0, self._selected - 1)
        elif event.key == pygame.K_DOWN:
            self._selected = min(len(_LESSONS) - 1, self._selected + 1)
        elif event.key == pygame.K_p:
            from cognitive_data_arcade.ui.profile_screen import ProfileScene

            back = LessonMenuScene(self._pm, self._strings)
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
            lesson_num = _LESSONS[self._selected][0]
            if lesson_num == 1:
                self._launch_big_data_map()
            elif lesson_num == 2:
                self._launch_rt_lab()
            elif lesson_num == 8:
                self._launch_flanker()
            elif lesson_num == 7:
                self._launch_stroop()
        elif event.key == pygame.K_z:
            self._launch_stroop_picker()

    def _launch_big_data_map(self) -> None:
        from cognitive_data_arcade.games.big_data_map.game import (
            BigDataMapGame,
        )  # deferred to avoid circular import

        self._next = BigDataMapGame(self._strings, self._pm)
        self._done = True

    def _launch_rt_lab(self) -> None:
        import datetime

        from cognitive_data_arcade.games.reaction_time.config import DEFAULT_CONFIG
        from cognitive_data_arcade.games.reaction_time.game import ReactionTimeGame

        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "reaction_time" / f"{sid}.csv"
        self._next = ReactionTimeGame(
            DEFAULT_CONFIG, self._pm, self._strings, pid, sid, csv_path
        )
        self._done = True

    def _launch_stroop(self) -> None:
        import datetime

        from cognitive_data_arcade.games.stroop.config import STANDARD
        from cognitive_data_arcade.games.stroop.game import StroopGame

        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "stroop" / f"{sid}.csv"
        self._next = StroopGame(STANDARD, self._pm, self._strings, pid, sid, csv_path)
        self._done = True

    def _launch_stroop_picker(self) -> None:
        from cognitive_data_arcade.ui.stroop_session_picker import (
            StroopSessionPickerScene,
        )

        sessions_dir = Path("data") / "generated" / "stroop"
        self._next = StroopSessionPickerScene(sessions_dir, self._strings, self._pm)
        self._done = True

    def _launch_flanker(self) -> None:
        import datetime

        from cognitive_data_arcade.games.flanker.config import STANDARD
        from cognitive_data_arcade.games.flanker.game import FlankerGame

        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "flanker" / f"{sid}.csv"
        self._next = FlankerGame(STANDARD, self._pm, self._strings, pid, sid, csv_path)
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
            text = self._font_item.render(f"{num:02d}.  {name}", True, color)
            surface.blit(text, (60, 140 + i * 44))
