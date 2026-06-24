# src/cognitive_data_arcade/games/you_were_the_dataset/game.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.you_were_the_dataset.game_state import GameState
from cognitive_data_arcade.games.you_were_the_dataset.profile_loader import check_prerequisites


class YouWereTheDatasetScene(Scene):
    def __init__(self, pm, strings) -> None:
        self._pm = pm
        self._strings = strings
        self._state = GameState()
        # Store pm/strings on state so PhaseResultScene can use them for replay
        self._state._pm = pm  # type: ignore[attr-defined]
        self._state._strings = strings  # type: ignore[attr-defined]

        self._done = False
        self._next: Scene | None = None

        factories = self._build_game_factories()
        prereqs = check_prerequisites()
        if all(prereqs.values()):
            from cognitive_data_arcade.games.you_were_the_dataset.phase_reveal import (
                PhaseRevealScene,
            )

            self._current: Scene = PhaseRevealScene(self._state)
        else:
            from cognitive_data_arcade.games.you_were_the_dataset.phase_prerequisite import (
                PhasePrerequisiteScene,
            )

            self._current = PhasePrerequisiteScene(self._state, factories)

    def _build_game_factories(self) -> dict:
        pm, strings = self._pm, self._strings
        factories: dict = {}
        if pm is None or strings is None:
            return factories  # test / synthetic mode — no factories needed

        def _make_rt():
            from cognitive_data_arcade.ui.session_picker import SessionPickerScene
            from pathlib import Path

            return SessionPickerScene(Path("data") / "generated" / "reaction_time", strings, pm)

        def _make_stroop():
            from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene

            return StroopLevelScene(pm, strings)

        def _make_flanker():
            from cognitive_data_arcade.ui.flanker_level_scene import FlankerLevelScene

            return FlankerLevelScene(pm, strings)

        def _make_gono():
            from cognitive_data_arcade.ui.gono_level_scene import GoNoGoLevelScene

            return GoNoGoLevelScene(pm, strings)

        def _make_nback():
            from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene

            return NBackLevelScene(pm, strings)

        factories["reaction_time"] = _make_rt
        factories["stroop"] = _make_stroop
        factories["flanker"] = _make_flanker
        factories["gono"] = _make_gono
        factories["nback"] = _make_nback
        return factories

    def handle_event(self, event: pygame.event.Event) -> None:
        self._current.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        if self._done:
            return
        self._current.update(dt_ms)
        if self._current.is_done():
            nxt = self._current.next_scene()
            if nxt is None or type(nxt).__name__ == "LessonMenuScene":
                # Phase chain ended (Menu clicked) — wire to SessionSummaryScene.
                # Detect LessonMenuScene by name to handle nested coordinators
                # (Replay creates a new YouWereTheDatasetScene as self._current;
                # when that inner instance finishes with Menu it returns LessonMenuScene).
                self._done = True
                if self._pm is not None and self._strings is not None:
                    self._next = self._build_next_scene()
                elif nxt is not None:
                    self._next = nxt
            else:
                self._current = nxt

    def _build_next_scene(self) -> "Scene":
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        p = self._state.profile
        if p is None:
            ap = 50
        elif getattr(p, "is_synthetic", True):
            ap = 75
        else:
            ap = 100
        rt_med = getattr(p, "rt_median_ms", 0.0) if p is not None else 0.0
        session = SessionResult(
            task_name="you_were_the_dataset",
            participant_id=self._pm.load().device_uuid,
            session_id="ytd_session",
            total_trials=5,
            correct_trials=5 if p is not None else 0,
            avg_reaction_time_ms=rt_med,
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
