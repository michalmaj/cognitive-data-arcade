# src/cognitive_data_arcade/games/misinformation/game.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.misinformation.phase_intro import PhaseIntroScene


class MisinformationScene(Scene):
    """Top-level scene: delegates to the currently active phase."""

    def __init__(self, pm=None, strings=None) -> None:
        self._pm = pm
        self._strings = strings
        self._current: Scene = PhaseIntroScene()

    def handle_event(self, event: pygame.event.Event) -> None:
        self._current.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        if hasattr(self, "_done") and self._done:
            return
        self._current.update(dt_ms)
        if self._current.is_done():
            nxt = self._current.next_scene()
            if nxt is not None:
                self._current = nxt
            elif self._pm is not None:
                # PhaseResultScene -> Menu: wire SessionSummaryScene
                self._done = True
                self._next = self._build_next_scene()

    def draw(self, surface: pygame.Surface) -> None:
        self._current.draw(surface)

    def is_done(self) -> bool:
        if getattr(self, "_done", False):
            return True
        return self._current.is_done() and self._current.next_scene() is None

    def next_scene(self) -> Scene | None:
        return getattr(self, "_next", None)

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        # Pull scores from PhaseResultScene if it's the current scene
        scores: list[int] = []
        if hasattr(self._current, "_scores"):
            scores = list(self._current._scores)
        total = sum(scores)
        ap = min(100, total // 7)
        n_pairs = max(1, len(scores) // 2)
        correct = sum(1 for i in range(len(scores) // 2) if scores[i * 2 + 1] > 50)
        session = SessionResult(
            task_name="misinformation_spread",
            participant_id=self._pm.load().device_uuid,
            session_id="misinfo_session",
            total_trials=n_pairs,
            correct_trials=min(correct, n_pairs),
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
