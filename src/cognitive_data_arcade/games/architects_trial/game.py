# src/cognitive_data_arcade/games/architects_trial/game.py
from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.architects_trial.game_state import GameState


class ArchitectsTrialScene(Scene):
    def __init__(self) -> None:
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
                if nxt is not None:
                    self._next = nxt
                # else: self._next stays None; PausableGame will route back to menu
            else:
                self._current = nxt

    def draw(self, surface: pygame.Surface) -> None:
        self._current.draw(surface)

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
