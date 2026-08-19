from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.badges import SessionResult
from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    ORANGE as _HIGHLIGHT_COLOR,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _TITLE_COLOR,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings, level_title
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.profile.manager import Profile, ProfileManager

_BANNER_BG = (26, 26, 62)
_ITEM_COLOR = (160, 160, 160)
_SP_COLOR = (39, 174, 96)
_ACCENT_COLOR = (52, 152, 219)
_DIM_COLOR = (70, 70, 112)
_PANEL_BG = (18, 18, 42)
_BORDER_COLOR = (42, 42, 80)
_LEVEL_COLOR = (192, 132, 252)

# Maps SessionResult.task_name → lesson number for completion tracking.
# L03 (event_log_detective) is handled separately in EventLogLevelScene.
_TASK_LESSON_MAP: dict[str, int] = {
    "reaction_time": 2,
    "big_data_map": 1,
    "data_quality_lab": 4,
    "eda_sandbox": 6,
    "stroop": 7,
    "flanker": 8,
    "go_no_go": 9,
    "n_back": 10,
    "visual_search": 11,
    "cognitive_dashboard": 12,
    "distribution_playground": 13,
    "correlation_trap": 14,
    "hypothesis_arena": 15,
    "prediction_slider": 16,
    "feature_hunter": 17,
    "classifier_battle": 18,
    "overfitting_monster": 19,
    "anomaly_alert": 20,
    "text_tokenizer_lab": 21,
    "word_weight_factory": 22,
    "emotion_classifier": 23,
    "semantic_space_explorer": 24,
    "topic_detective": 25,
    "human_vs_model": 26,
    "social_network_simulator": 27,
    "misinformation_spread": 28,
    "recommendation_bubble": 29,
    "bias_blind_spot": 30,
    "you_were_the_dataset": 31,
    "architects_trial": 32,
}

_REFLECTION_TASK_MAP: dict[str, tuple[str, str]] = {
    "big_data_map": ("lesson_01", "REFLECTION"),
    "data_quality_lab": ("lesson_04", "REFLECTION"),
    "eda_sandbox": ("lesson_06", "REFLECTION"),
    "distribution_playground": ("lesson_13", "REFLECTION"),
    "correlation_trap": ("lesson_14", "REFLECTION"),
    "hypothesis_arena": ("lesson_15", "REFLECTION"),
    "prediction_slider": ("lesson_16", "REFLECTION"),
    "feature_hunter": ("lesson_17", "REFLECTION"),
    "classifier_battle": ("lesson_18", "REFLECTION"),
    "overfitting_monster": ("lesson_19", "REFLECTION"),
    "anomaly_alert": ("lesson_20", "REFLECTION"),
    "text_tokenizer_lab": ("lesson_21", "REFLECTION"),
    "word_weight_factory": ("lesson_22", "REFLECTION"),
    "emotion_classifier": ("lesson_23", "REFLECTION"),
    "semantic_space_explorer": ("lesson_24", "REFLECTION"),
    "topic_detective": ("lesson_25", "REFLECTION"),
    "human_vs_model": ("lesson_26", "REFLECTION"),
    "social_network_simulator": ("lesson_27", "REFLECTION"),
    "misinformation_spread": ("lesson_28", "REFLECTION"),
    "recommendation_bubble": ("lesson_29", "REFLECTION"),
    "bias_blind_spot": ("lesson_30", "REFLECTION"),
    "you_were_the_dataset": ("lesson_31", "REFLECTION"),
    "architects_trial": ("lesson_32", "REFLECTION"),
}


class SessionSummaryScene(Scene):
    def __init__(
        self,
        session: SessionResult,
        new_badge_ids: list[str],
        profile_before: Profile,
        profile_after: Profile,
        strings: Strings,
        profile_manager: ProfileManager,
        csv_path: Path | None = None,
        analysis_factory: Callable[[Path, Strings, Scene], Scene] | None = None,
    ) -> None:
        self._session = session
        self._new_badge_ids = new_badge_ids
        self._profile_before = profile_before
        self._profile_after = profile_after
        self._strings = strings
        self._pm = profile_manager
        self._next: Scene | None = None
        self._done = False
        self._go_to_profile = False
        self._csv_path = csv_path
        self._analysis_factory = analysis_factory
        self._go_to_analysis = False
        lesson_num = _TASK_LESSON_MAP.get(session.task_name)
        if lesson_num is not None:
            profile_manager.complete_lesson(lesson_num)
        self._font_sm = get_font(24)
        self._font_title = get_font(56)
        self._font_sub = get_font(30)
        self._font_stat = get_font(52)
        self._font_hint = get_font(26)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._done = True
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
            self._done = True
        elif event.key == pygame.K_p:
            self._done = True
            self._go_to_profile = True
        elif event.key == pygame.K_s and self._csv_path is not None:
            self._done = True
            self._go_to_analysis = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        if self._next is not None:
            return self._next
        if not self._done:
            return None
        from cognitive_data_arcade.ui.menu import LessonMenuScene

        if self._go_to_analysis and self._csv_path is not None:
            if self._analysis_factory is not None:
                self._next = self._analysis_factory(self._csv_path, self._strings, self)
            else:
                from cognitive_data_arcade.analytics.rt_analysis import (
                    build_histogram,
                    load_session,
                    session_stats,
                )
                from cognitive_data_arcade.engine.chart import figure_to_surface
                from cognitive_data_arcade.ui.analysis_scene import AnalysisScene

                df = load_session(self._csv_path)
                stats = session_stats(df)
                fig = build_histogram(df)
                chart = figure_to_surface(fig, (680, 550))
                self._next = AnalysisScene(chart, stats, self._strings, back_scene=self)
        elif self._go_to_profile:
            from cognitive_data_arcade.ui.profile_screen import ProfileScene

            back = LessonMenuScene(self._pm, self._strings)
            self._next = ProfileScene(self._pm, self._strings, back)
        else:
            menu = LessonMenuScene(self._pm, self._strings)
            self._next = self._maybe_reflection(menu)
        return self._next

    def _maybe_reflection(self, back: Scene) -> Scene:
        entry = _REFLECTION_TASK_MAP.get(self._session.task_name)
        if entry is None:
            return back
        from importlib import import_module

        mod = import_module(f"cognitive_data_arcade.lessons.{entry[0]}")
        reflection = getattr(mod, entry[1], None)
        if reflection is None:
            return back
        from cognitive_data_arcade.ui.reflection_scene import ReflectionScene

        return ReflectionScene(reflection, self._strings, back_scene=back)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w = surface.get_width()
        h = surface.get_height()

        # Lesson tag
        tag = self._font_sm.render(self._session.task_name, True, _DIM_COLOR)
        surface.blit(tag, (w // 2 - tag.get_width() // 2, 28))

        # Title
        title = self._font_title.render(self._strings.session_complete, True, _TITLE_COLOR)
        surface.blit(title, (w // 2 - title.get_width() // 2, 52))

        # Subtitle
        sub = self._font_sub.render(self._strings.session_subtitle, True, _ITEM_COLOR)
        surface.blit(sub, (w // 2 - sub.get_width() // 2, 110))

        # Divider
        pygame.draw.line(surface, _BORDER_COLOR, (100, 146), (w - 100, 146))

        # Stats row
        stats = [
            (
                self._strings.label_arcade_points,
                f"+{self._session.arcade_points_earned}",
                _HIGHLIGHT_COLOR,
            ),
            (
                self._strings.label_accuracy,
                f"{self._session.accuracy:.0%}",
                _ACCENT_COLOR,
            ),
            (
                self._strings.label_avg_rt,
                f"{self._session.avg_reaction_time_ms:.0f} ms",
                _ITEM_COLOR,
            ),
        ]
        box_w, box_h = 240, 100
        gap = 20
        total_box_w = 3 * box_w + 2 * gap
        box_x0 = (w - total_box_w) // 2
        box_y = 160

        for i, (label, value, color) in enumerate(stats):
            bx = box_x0 + i * (box_w + gap)
            pygame.draw.rect(surface, _PANEL_BG, (bx, box_y, box_w, box_h), border_radius=6)
            pygame.draw.rect(surface, _BORDER_COLOR, (bx, box_y, box_w, box_h), 1, border_radius=6)
            lbl = self._font_sm.render(label, True, _DIM_COLOR)
            surface.blit(lbl, (bx + box_w // 2 - lbl.get_width() // 2, box_y + 10))
            val = self._font_stat.render(value, True, color)
            surface.blit(val, (bx + box_w // 2 - val.get_width() // 2, box_y + 38))

        # Badges section
        section_y = box_y + box_h + 22
        lbl_new = self._font_sm.render(self._strings.label_new_badges, True, _DIM_COLOR)
        surface.blit(lbl_new, (box_x0, section_y))
        section_y += 24

        if self._new_badge_ids:
            pill_x = box_x0
            for bid in self._new_badge_ids:
                name = self._strings.badge_names.get(bid, bid)
                pill_surf = self._font_sm.render(f"✦ {name}", True, _HIGHLIGHT_COLOR)
                pill_w = pill_surf.get_width() + 20
                pill_h = 28
                pygame.draw.rect(
                    surface,
                    _PANEL_BG,
                    (pill_x, section_y, pill_w, pill_h),
                    border_radius=14,
                )
                pygame.draw.rect(
                    surface,
                    _HIGHLIGHT_COLOR,
                    (pill_x, section_y, pill_w, pill_h),
                    1,
                    border_radius=14,
                )
                surface.blit(pill_surf, (pill_x + 10, section_y + 5))
                pill_x += pill_w + 10
        else:
            no_badge = self._font_sm.render(self._strings.label_no_new_badges, True, _DIM_COLOR)
            surface.blit(no_badge, (box_x0, section_y))

        # Level-up banner (conditional)
        before_total = self._profile_before.arcade_points + self._profile_before.science_points
        after_total = self._profile_after.arcade_points + self._profile_after.science_points
        before_lvl = level_title(before_total, self._strings)
        after_lvl = level_title(after_total, self._strings)

        banner_y = section_y + 46
        if before_lvl != after_lvl:
            banner_rect = pygame.Rect(100, banner_y, w - 200, 44)
            pygame.draw.rect(surface, _BANNER_BG, banner_rect, border_radius=6)
            pygame.draw.rect(surface, _LEVEL_COLOR, banner_rect, 1, border_radius=6)
            lvl_text = f">>  {self._strings.label_level_up}  {before_lvl}  ->  {after_lvl}"
            lvl_surf = self._font_sm.render(lvl_text, True, _LEVEL_COLOR)
            surface.blit(lvl_surf, (w // 2 - lvl_surf.get_width() // 2, banner_y + 13))

        # Footer hints
        hints = [
            (self._strings.hint_space, _TITLE_COLOR),
            (self._strings.hint_p, _ITEM_COLOR),
            (self._strings.hint_esc, _ITEM_COLOR),
        ]
        if self._csv_path is not None:
            hints.append((self._strings.analysis_hint_s, _HIGHLIGHT_COLOR))
        hint_y = h - 40
        hint_total = sum(self._font_hint.size(t)[0] for t, _ in hints) + 60
        hint_x = (w - hint_total) // 2
        for hint_text, hint_color in hints:
            hs = self._font_hint.render(hint_text, True, hint_color)
            surface.blit(hs, (hint_x, hint_y))
            hint_x += hs.get_width() + 30
