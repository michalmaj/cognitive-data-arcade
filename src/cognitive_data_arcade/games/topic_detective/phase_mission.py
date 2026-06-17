from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.topic_detective.missions import Mission


class PhaseMissionScene(Scene):
    def __init__(
        self,
        missions: list[Mission],
        round_idx: int,
        session_score: int,
        round_results: list[dict],
    ) -> None:
        self._missions = missions
        self._round_idx = round_idx
        self._session_score = session_score
        self._round_results = round_results
        self._done = False
        self._next = None

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> "Scene | None":
        return self._next
