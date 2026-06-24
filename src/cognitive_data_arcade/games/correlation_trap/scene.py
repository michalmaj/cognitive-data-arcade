# src/cognitive_data_arcade/games/correlation_trap/scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.correlation_trap.phase_a import PhaseAScene
from cognitive_data_arcade.games.correlation_trap.phase_b import PhaseBScene
from cognitive_data_arcade.games.correlation_trap.phase_c import PhaseCScene

from cognitive_data_arcade.engine.colors import (
    BG as _BG,
    WHITE as _WHITE,
    DIM as _DIM,
)

_NAV_BG = (18, 18, 45)
_ACTIVE = (243, 156, 18)
_NAV_H = 48

_PHASE_NAMES = ["Eksploracja", "Detekcja", "Sandbox"]


class CorrelationTrapScene(Scene):
    def __init__(self, pm, strings) -> None:
        self._pm = pm
        self._strings = strings
        self._phase_switches: int = 0
        self._done: bool = False
        self._next: Scene | None = None
        self._phase = 1
        self._phases: list[Scene] = [PhaseAScene(), PhaseBScene(), PhaseCScene()]

    def current_phase(self) -> int:
        return self._phase

    def _active(self) -> Scene:
        return self._phases[self._phase - 1]

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._phase = (self._phase % 3) + 1
                self._phase_switches += 1
                return
            if event.key == pygame.K_LEFT:
                self._phase = ((self._phase - 2) % 3) + 1
                self._phase_switches += 1
                return
            if event.key == pygame.K_q:
                self._done = True
                return
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            adjusted = _offset_mouse_event(event, dy=-_NAV_H)
            self._active().handle_event(adjusted)
        else:
            self._active().handle_event(event)

    def update(self, dt_ms: float) -> None:
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
            task_name="correlation_trap",
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


def _offset_mouse_event(event: pygame.event.Event, dy: int) -> pygame.event.Event:
    d = dict(event.__dict__)
    if "pos" in d:
        x, y = d["pos"]
        d["pos"] = (x, y + dy)
    return pygame.event.Event(event.type, d)
