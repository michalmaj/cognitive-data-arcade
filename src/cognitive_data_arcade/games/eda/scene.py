# src/cognitive_data_arcade/games/eda/scene.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.games.eda.simulator import simulate
from cognitive_data_arcade.games.eda.ui_controls import ControlPanel
from cognitive_data_arcade.games.eda.ui_results import ChartPanel, ResultsPanel

_BG = (15, 15, 35)


class EDAScene(Scene):
    def __init__(self) -> None:
        self._controls = ControlPanel()
        self._charts = ChartPanel()
        self._results = ResultsPanel()

    def handle_event(self, event: pygame.event.Event) -> None:
        action = self._controls.handle_event(event)
        if action == "generate":
            params = self._controls.get_params()
            threshold = self._controls.get_hypothesis_threshold()
            result = simulate(**params)
            self._charts.update(result)
            self._results.update(result, threshold)

    def update(self, dt_ms: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        self._controls.draw(surface)
        self._charts.draw(surface, x=360, y=30)
        self._results.draw(surface, x=360, y=270)

    def is_done(self) -> bool:
        return False
