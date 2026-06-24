# src/cognitive_data_arcade/games/bias_blind_spot/game.py
from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.bias_blind_spot.game_state import GameState


class BiasBlindSpotScene(Scene):
    def __init__(self, pm=None, strings=None) -> None:
        self._pm = pm
        self._strings = strings
        self._state = GameState()
        from cognitive_data_arcade.games.bias_blind_spot.phase_intro import PhaseIntroScene

        self._current: Scene = PhaseIntroScene(self._state)

    def handle_event(self, event: pygame.event.Event) -> None:
        self._current.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        if getattr(self, "_done", False):
            return
        self._current.update(dt_ms)
        if self._current.is_done():
            nxt = self._current.next_scene()
            if nxt is not None:
                self._current = nxt
            elif self._pm is not None:
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
        from cognitive_data_arcade.games.bias_blind_spot.game_state import stars_from_score
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        score_engineer = getattr(self._state, "score_engineer", 0)
        ap = min(100, score_engineer)
        stars = stars_from_score(score_engineer)
        session = SessionResult(
            task_name="bias_blind_spot",
            participant_id=self._pm.load().device_uuid,
            session_id="bias_session",
            total_trials=3,
            correct_trials=min(stars, 3),
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
