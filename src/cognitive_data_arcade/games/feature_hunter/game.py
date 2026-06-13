from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.feature_hunter.phase_a import PhaseAScene


class FeatHunterScene(Scene):
    """Sequential carousel: Phase A -> Phase B -> Phase C -> Phase A (replay)."""

    def __init__(self) -> None:
        self._current: Scene = PhaseAScene()

    def handle_event(self, event: pygame.event.Event) -> None:
        self._current.handle_event(event)

    def update(self, dt_ms: float = 0.0) -> None:
        self._current.update(dt_ms)
        if self._current.is_done():
            nxt = self._current.next_scene()
            if nxt is not None:
                self._current = nxt

    def draw(self, surface: pygame.Surface) -> None:
        self._current.draw(surface)

    def is_done(self) -> bool:
        return self._current.is_done() and self._current.next_scene() is None

    def next_scene(self) -> Scene | None:
        return None
