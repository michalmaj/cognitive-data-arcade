import pygame

from cognitive_data_arcade.engine.game_loop import GameLoop
from cognitive_data_arcade.engine.scene import Scene


class _OneFrameScene(Scene):
    """Exits immediately after the first update call."""

    def __init__(self) -> None:
        self._done = False

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt_ms: float) -> None:
        self._done = True

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def is_done(self) -> bool:
        return self._done


def test_game_loop_runs_one_frame_and_exits() -> None:
    loop = GameLoop(_OneFrameScene(), width=320, height=240)
    loop.run()  # must return without hanging
