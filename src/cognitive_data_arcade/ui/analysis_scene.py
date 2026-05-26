from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene

_BG = (10, 10, 20)
_WHITE = (240, 240, 240)
_ORANGE = (243, 156, 18)
_DIM = (100, 100, 150)

_CHART_X = 10
_CHART_Y = 45
_STATS_X = 710
_FOOTER_H = 30


class AnalysisScene(Scene):
    def __init__(
        self,
        chart_surface: pygame.Surface,
        stats: dict,
        strings: Strings,
        back_scene: Scene,
    ) -> None:
        self._chart = chart_surface
        self._stats = stats
        self._strings = strings
        self._back = back_scene
        self._done = False
        pygame.font.init()
        self._font_title = pygame.font.SysFont(None, 34)
        self._font_label = pygame.font.SysFont(None, 24)
        self._font_value = pygame.font.SysFont(None, 36)
        self._font_hint = pygame.font.SysFont(None, 24)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._done = True

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._back if self._done else None

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        w, h = surface.get_size()

        title = self._font_title.render(self._strings.analysis_title, True, _WHITE)
        surface.blit(title, (14, 10))

        surface.blit(self._chart, (_CHART_X, _CHART_Y))

        stats_items = [
            (self._strings.label_avg_rt, f"{self._stats['avg_rt']:.0f} ms"),
            (self._strings.label_median_rt, f"{self._stats['median_rt']:.0f} ms"),
            ("Min RT", f"{self._stats['min_rt']:.0f} ms"),
            (self._strings.label_accuracy, f"{self._stats['accuracy']:.0%}"),
            ("Trials", f"{self._stats['n_correct']}/{self._stats['n_trials']}"),
        ]
        panel_y = _CHART_Y + 20
        for label, value in stats_items:
            lbl = self._font_label.render(label, True, _DIM)
            surface.blit(lbl, (_STATS_X, panel_y))
            val = self._font_value.render(value, True, _ORANGE)
            surface.blit(val, (_STATS_X, panel_y + 22))
            panel_y += 70

        hint = self._font_hint.render(self._strings.analysis_hint_esc, True, _DIM)
        surface.blit(hint, (14, h - _FOOTER_H))
