# src/cognitive_data_arcade/games/architects_trial/game.py
from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.architects_trial.game_state import GameState


class ArchitectsTrialScene(Scene):
    def __init__(self, pm=None, strings=None) -> None:
        self._pm = pm
        self._strings = strings
        self._state = GameState()
        self._done = False
        self._next: Scene | None = None
        from cognitive_data_arcade.games.architects_trial.phase_intro import PhaseIntroScene

        self._current: Scene = PhaseIntroScene(self._state)

    def handle_event(self, event: pygame.event.Event) -> None:
        self._current.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        if self._done:
            return
        self._current.update(dt_ms)
        if self._current.is_done():
            nxt = self._current.next_scene()
            if nxt is None or type(nxt).__name__ == "LessonMenuScene":
                self._done = True
                if self._pm is not None:
                    self._next = self._build_next_scene()
                elif nxt is not None:
                    self._next = nxt
                # else: self._next stays None; PausableGame will route back to menu
            else:
                self._current = nxt

    def _build_next_scene(self) -> Scene:
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.games.architects_trial.game_state import compute_verdict
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        state = self._state
        ap = min(
            100,
            (state.fairness_score + state.compliance_score + state.effectiveness_score) // 3,
        )
        verdict = compute_verdict(
            state.fairness_score, state.compliance_score, state.effectiveness_score
        )
        correct = 1 if verdict == "ZATWIERDZONY" else 0
        session = SessionResult(
            task_name="architects_trial",
            participant_id=self._pm.load().device_uuid,
            session_id="trial_session",
            total_trials=1,
            correct_trials=correct,
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
        self._current.draw(surface)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
