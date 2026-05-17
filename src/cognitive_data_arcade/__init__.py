"""Cognitive Data Arcade package."""

from cognitive_data_arcade.engine.game_loop import GameLoop
from cognitive_data_arcade.ui.menu import LessonMenuScene


def main() -> None:
    GameLoop(LessonMenuScene()).run()
