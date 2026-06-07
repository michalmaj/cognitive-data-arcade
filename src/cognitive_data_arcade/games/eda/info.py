# src/cognitive_data_arcade/games/eda/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="EDA Sandbox",
            description_lines=[
                "Zaprojektuj symulowany eksperyment RT z dwoma warunkami.",
                "Ustaw suwaki, postaw hipoteze i kliknij GENERUJ.",
                "Obserwuj jak N, efekt i szum wplywaja na wyniki.",
            ],
            key_bindings=[
                ("LEWO / PRAWO", "zmien wartosc suwaka"),
                ("TAB", "nastepny suwak"),
                ("ENTER", "generuj dane"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="EDA Sandbox",
        description_lines=[
            "Design a simulated two-condition RT experiment.",
            "Set sliders, state a hypothesis, and click GENERATE.",
            "See how N, effect size, and noise shape the results.",
        ],
        key_bindings=[
            ("LEFT / RIGHT", "adjust slider value"),
            ("TAB", "next slider"),
            ("ENTER", "generate data"),
            ("ESC", "pause"),
        ],
    )
