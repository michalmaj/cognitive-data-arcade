from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.feature_hunter.phase_a import PhaseAScene


class FeatHunterScene(Scene):
    """Sequential carousel: Phase A -> Phase B -> Phase C -> Phase A (replay)."""

    def __init__(self, pm=None, strings=None) -> None:
        self._pm = pm
        self._strings = strings
        self._phases_completed: int = 0
        self._next_cache: Scene | None = None
        self._current: Scene = PhaseAScene()

    def handle_event(self, event: pygame.event.Event) -> None:
        self._current.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        self._current.update(dt_ms)
        if self._current.is_done():
            nxt = self._current.next_scene()
            if nxt is not None:
                self._phases_completed += 1
                self._current = nxt

    def draw(self, surface: pygame.Surface) -> None:
        self._current.draw(surface)

    def is_done(self) -> bool:
        return self._current.is_done() and self._current.next_scene() is None

    def next_scene(self) -> Scene | None:
        if self.is_done():
            if self._next_cache is None:
                self._next_cache = self._build_next_scene()
            return self._next_cache
        return None

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        ap = min(100, 50 + self._phases_completed * 15)
        session = SessionResult(
            task_name="feature_hunter",
            participant_id=self._pm.load().device_uuid,
            session_id="feat_hunter_session",
            total_trials=3,
            correct_trials=min(3, self._phases_completed),
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
