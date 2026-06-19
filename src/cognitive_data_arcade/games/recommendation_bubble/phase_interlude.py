from __future__ import annotations
import pygame
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.recommendation_bubble.game_state import GameState

class PhaseInterludeScene(Scene):
    def __init__(self, state: GameState, next_act: str) -> None:
        self._state = state
        self._next_act = next_act
        self._done = False
        self._next: Scene | None = None
    def handle_event(self, event: pygame.event.Event) -> None: pass
    def update(self, dt_ms: float = 0.0) -> None: pass
    def draw(self, surface: pygame.Surface) -> None: surface.fill((12, 12, 20))
    def is_done(self) -> bool: return self._done
    def next_scene(self) -> Scene | None: return self._next
