# src/cognitive_data_arcade/games/distribution_playground/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Distribution Playground",
            description_lines=[
                "Eksploruj trzy rodziny rozkladow statystycznych.",
                "Faza A: swobodna eksploracja parametrow.",
                "Faza B: odgadnij ukryty rozklad.",
                "Faza C: porownaj dwa rozklady side-by-side.",
            ],
            key_bindings=[
                ("LEWO / PRAWO", "zmien faze"),
                ("PPM (prawy klik)", "kontekstowa pomoc"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Distribution Playground",
        description_lines=[
            "Explore three statistical distribution families.",
            "Phase A: free parameter exploration.",
            "Phase B: guess the hidden distribution.",
            "Phase C: compare two distributions side-by-side.",
        ],
        key_bindings=[
            ("LEFT / RIGHT", "change phase"),
            ("Right-click", "contextual help"),
            ("ESC", "pause"),
        ],
    )
