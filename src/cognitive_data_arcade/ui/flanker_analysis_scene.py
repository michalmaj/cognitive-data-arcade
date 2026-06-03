from __future__ import annotations

import math
from pathlib import Path

import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene

_BG = (26, 26, 46)
_WHITE = (240, 240, 240)
_ORANGE = (243, 156, 18)
_DIM = (100, 100, 150)

_CHART_X = 20
_CHART_Y = 20
_STATS_X = 720
_FOOTER_H = 30


def _fmt_rt(value: float) -> str:
    return "— ms" if math.isnan(value) else f"{value:.0f} ms"


class FlankerAnalysisScene(Scene):
    def __init__(
        self,
        csv_path: Path,
        strings: Strings,
        back_scene: Scene,
    ) -> None:
        from cognitive_data_arcade.analytics import flanker_analysis

        df = flanker_analysis.load_session(csv_path)
        self._stats = flanker_analysis.session_stats(df)
        fig = flanker_analysis.build_comparison_chart(df)
        self._chart = figure_to_surface(fig, (680, 550))

        self._strings = strings
        self._back_scene = back_scene
        self._done = False

        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 34)
        self._font_label = pygame.font.SysFont(None, 24)
        self._font_value = pygame.font.SysFont(None, 32)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._done = True
        elif event.type == pygame.KEYDOWN and event.key in (
            pygame.K_SPACE,
            pygame.K_ESCAPE,
            pygame.K_RETURN,
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
        _w, h = surface.get_size()

        surface.blit(self._chart, (_CHART_X, _CHART_Y))

        panel_y = _CHART_Y + 10
        title_surf = self._font_title.render("Flanker Effect", True, _WHITE)
        surface.blit(title_surf, (_STATS_X, panel_y))
        panel_y += 44

        stats = self._stats
        stat_lines = [
            ("Congruent RT", _fmt_rt(stats["congruent_mean_rt"])),
            ("Incongruent RT", _fmt_rt(stats["incongruent_mean_rt"])),
            ("Flanker Effect", _fmt_rt(stats["flanker_effect_ms"])),
            ("Congruent Acc", f"{stats['congruent_accuracy']:.0%}"),
            ("Incongruent Acc", f"{stats['incongruent_accuracy']:.0%}"),
            ("Overall Acc", f"{stats['overall_accuracy']:.0%}"),
        ]

        for label, value in stat_lines:
            lbl = self._font_label.render(label, True, _DIM)
            surface.blit(lbl, (_STATS_X, panel_y))
            val = self._font_value.render(value, True, _ORANGE)
            surface.blit(val, (_STATS_X, panel_y + 20))
            panel_y += 56

        hint = self._font_label.render(self._strings.hint_space, True, _DIM)
        surface.blit(hint, (14, h - _FOOTER_H))
