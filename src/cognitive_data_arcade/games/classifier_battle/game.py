from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.classifier_battle.phase_intro import PhaseIntroScene


class ClassifierBattleScene(Scene):
    """Top-level scene: delegates to whichever phase is active."""

    def __init__(self, pm=None, strings=None) -> None:
        self._pm = pm
        self._strings = strings
        self._current: Scene = PhaseIntroScene()

    def handle_event(self, event: pygame.event.Event) -> None:
        self._current.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        self._current.update(dt_ms)
        if self._current.is_done():
            nxt = self._current.next_scene()
            if nxt is not None:
                from cognitive_data_arcade.games.classifier_battle.phase_session_result import (
                    PhaseSessionResultScene,
                )

                if isinstance(nxt, PhaseSessionResultScene):
                    nxt._pm = self._pm
                    nxt._strings = self._strings
                self._current = nxt

    def draw(self, surface: pygame.Surface) -> None:
        self._current.draw(surface)

    def is_done(self) -> bool:
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        if isinstance(self._current, SessionSummaryScene):
            return False
        return self._current.is_done() and self._current.next_scene() is None

    def next_scene(self) -> Scene | None:
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        if isinstance(self._current, SessionSummaryScene) and self._current.is_done():
            return self._current.next_scene()
        return None
