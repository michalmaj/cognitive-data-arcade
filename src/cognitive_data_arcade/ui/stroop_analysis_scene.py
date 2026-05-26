from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.scene import Scene

_BG = (10, 10, 20)
_WHITE = (240, 240, 240)
_ORANGE = (243, 156, 18)
_DIM = (100, 100, 150)
_GREEN = (39, 174, 96)
_RED = (231, 76, 60)
_BORDER = (42, 42, 80)
_CHART_X = 10
_CHART_Y = 45
_STATS_X = 710
_FOOTER_H = 30


class StroopAnalysisScene(Scene):
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
        self._font_value = pygame.font.SysFont(None, 32)
        self._font_badge = pygame.font.SysFont(None, 28)
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

        title = self._font_title.render(
            self._strings.stroop_analysis_title, True, _WHITE
        )
        surface.blit(title, (14, 10))
        surface.blit(self._chart, (_CHART_X, _CHART_Y))

        # Per-condition rows
        panel_y = _CHART_Y + 10
        cond_items = [
            ("Congruent", self._stats["avg_rt_congruent"], _GREEN),
            ("Neutral", self._stats["avg_rt_neutral"], (80, 80, 192)),
            ("Incongruent", self._stats["avg_rt_incongruent"], _RED),
        ]
        for label, value, color in cond_items:
            lbl = self._font_label.render(label, True, _DIM)
            surface.blit(lbl, (_STATS_X, panel_y))
            val = self._font_value.render(f"{value:.0f} ms", True, color)
            surface.blit(val, (_STATS_X, panel_y + 20))
            panel_y += 56

        pygame.draw.line(surface, _BORDER, (_STATS_X, panel_y), (w - 10, panel_y))
        panel_y += 12

        # Facilitation / Interference
        delta_items = [
            (self._strings.label_facilitation, self._stats["facilitation_ms"]),
            (self._strings.label_interference, self._stats["interference_ms"]),
        ]
        for label, value in delta_items:
            sign = "+" if value >= 0 else ""
            lbl = self._font_label.render(label, True, _DIM)
            surface.blit(lbl, (_STATS_X, panel_y))
            val_color = _GREEN if value < 0 else _RED
            val = self._font_value.render(f"{sign}{value:.0f} ms", True, val_color)
            surface.blit(val, (_STATS_X, panel_y + 20))
            panel_y += 56

        # Stroop Effect badge
        effect = self._stats["stroop_effect_ms"]
        sign = "+" if effect >= 0 else ""
        badge_text = f"{self._strings.label_stroop_effect}  {sign}{effect:.0f} ms"
        badge_surf = self._font_badge.render(badge_text, True, _ORANGE)
        bw = badge_surf.get_width() + 24
        bh = badge_surf.get_height() + 16
        badge_y = panel_y + 12
        pygame.draw.rect(
            surface, (26, 26, 46), (_STATS_X - 4, badge_y, bw, bh), border_radius=6
        )
        pygame.draw.rect(
            surface, _ORANGE, (_STATS_X - 4, badge_y, bw, bh), 1, border_radius=6
        )
        surface.blit(badge_surf, (_STATS_X + 8, badge_y + 8))

        hint = self._font_hint.render("ESC  back", True, _DIM)
        surface.blit(hint, (14, h - _FOOTER_H))
