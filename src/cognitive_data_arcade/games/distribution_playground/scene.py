# src/cognitive_data_arcade/games/distribution_playground/scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.distribution_playground.phase_a import PhaseAScene
from cognitive_data_arcade.games.distribution_playground.phase_b import PhaseBScene
from cognitive_data_arcade.games.distribution_playground.phase_c import PhaseCScene

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
)

_NAV_BG = (18, 18, 45)
_ACTIVE = (243, 156, 18)
_NAV_H = 48
_PHASE_NAMES = ["Eksploracja", "Zgadywanie", "Porownanie"]


class DistributionPlaygroundScene(Scene):
    def __init__(self, pm, strings) -> None:
        self._pm = pm
        self._strings = strings
        self._phase_switches: int = 0
        self._done: bool = False
        self._next: Scene | None = None
        self._phase = 1  # 1-indexed
        self._phases: list[Scene] = [PhaseAScene(), PhaseBScene(), PhaseCScene()]
        self._show_summary: bool = False
        self._summary_timer: float = 0.0
        self._session_start_ms: int = pygame.time.get_ticks()
        self._phases_visited: set = set()

    def current_phase(self) -> int:
        return self._phase

    def _active(self) -> Scene:
        return self._phases[self._phase - 1]

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._show_summary:
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self._summary_timer = 10_001
                self._done = True
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._phase = (self._phase % 3) + 1
                self._phase_switches += 1
                self._phases_visited.add(self._phase)
                return
            if event.key == pygame.K_LEFT:
                self._phase = ((self._phase - 2) % 3) + 1
                self._phase_switches += 1
                self._phases_visited.add(self._phase)
                return
            if event.key == pygame.K_q:
                self._show_summary = True
                self._summary_timer = 0.0
                return
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            adjusted = _offset_mouse_event(event, dy=-_NAV_H)
            self._active().handle_event(adjusted)
        else:
            self._active().handle_event(event)

    def update(self, dt_ms: float) -> None:
        if self._show_summary:
            self._summary_timer += dt_ms
            if self._summary_timer >= 10_000:
                self._done = True
            return
        self._active().update(dt_ms)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        if self._done and self._next is None:
            self._next = self._build_next_scene()
        return self._next

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        ap = min(100, 30 + self._phase_switches * 5)
        session = SessionResult(
            task_name="distribution_playground",
            participant_id=self._pm.load().device_uuid,
            session_id="sandbox_session",
            total_trials=3,
            correct_trials=min(3, self._phase_switches),
            avg_reaction_time_ms=0.0,
            min_reaction_time_ms=0.0,
            max_reaction_time_ms=0.0,
            arcade_points_earned=ap,
            science_points_earned=0,
        )
        profile_before = self._pm.load()
        badge_engine = BadgeEngine()
        new_badge_ids = badge_engine.evaluate(session, profile_before)
        self._pm.add_ap(ap)
        for bid in new_badge_ids:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()
        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badge_ids,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._draw_nav(surface)
        inner = pygame.Surface((1024, 768 - _NAV_H))
        inner.fill(_BG)
        phase_scene = self._active()
        phase_scene.draw(inner, offset_y=0)
        surface.blit(inner, (0, _NAV_H))
        if self._show_summary:
            self._draw_summary(surface)

    def _draw_nav(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _NAV_BG, (0, 0, 1024, _NAV_H))
        font_nav = get_font(18)
        font_sub = get_font(14)

        lbl = f"Faza {self._phase} / 3  -  {_PHASE_NAMES[self._phase - 1]}"
        tw = font_nav.size(lbl)[0]
        surface.blit(font_nav.render(lbl, True, _ACTIVE), ((1024 - tw) // 2, 8))

        surface.blit(font_nav.render("<", True, _WHITE), (20, 10))
        surface.blit(font_nav.render(">", True, _WHITE), (1024 - 36, 10))

        surface.blit(font_sub.render("LEWO / PRAWO = zmien faze", True, _DIM), (20, _NAV_H - 16))

    def _draw_summary(self, surface: pygame.Surface) -> None:
        w, h = surface.get_width(), surface.get_height()
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        panel_w, panel_h = 560, 260
        px = (w - panel_w) // 2
        py = (h - panel_h) // 2
        pygame.draw.rect(surface, (14, 14, 36), (px, py, panel_w, panel_h), border_radius=10)
        pygame.draw.rect(surface, (70, 70, 130), (px, py, panel_w, panel_h), 2, border_radius=10)

        elapsed_s = (pygame.time.get_ticks() - self._session_start_ms) // 1000
        mins, secs = divmod(elapsed_s, 60)
        visited = len(self._phases_visited)

        font_h = get_font(24)
        font_b = get_font(20)
        font_hint = get_font(14)
        lines = [
            ("Distribution Playground - Podsumowanie", font_h, (200, 200, 240)),
            (f"Czas sesji: {mins}m {secs}s", font_b, (160, 160, 200)),
            (f"Fazy odwiedzone: {visited} / 3", font_b, (160, 160, 200)),
            ("", font_b, (0, 0, 0)),
            ("Nacisnij dowolny klawisz lub kliknij", font_hint, (90, 90, 120)),
        ]
        y = py + 20
        for text, font, color in lines:
            if not text:
                y += 10
                continue
            s = font.render(text, True, color)
            surface.blit(s, (px + panel_w // 2 - s.get_width() // 2, y))
            y += font.get_height() + 8


def _offset_mouse_event(event: pygame.event.Event, dy: int) -> pygame.event.Event:
    d = dict(event.__dict__)
    if "pos" in d:
        x, y = d["pos"]
        d["pos"] = (x, y + dy)
    return pygame.event.Event(event.type, d)
