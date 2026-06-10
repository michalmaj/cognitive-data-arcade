# src/cognitive_data_arcade/games/cognitive_dashboard/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Cognitive Dashboard",
            description_lines=[
                "Porownaj swoja wydajnosc w 4 klasycznych zadaniach poznawczych.",
                "Zagraj w kazde zadanie (8 prob) lub wygeneruj dane syntetyczne.",
                "Na koncu zobaczysz swoj profil poznawczy.",
            ],
            key_bindings=[
                ("strzalki + ENTER", "wybierz i zagraj zadanie"),
                ("S", "dane syntetyczne"),
                ("ESC", "menu"),
            ],
        )
    return GameInfo(
        title="Cognitive Dashboard",
        description_lines=[
            "Compare your performance across 4 classic cognitive tasks.",
            "Play each task (8 trials) or generate synthetic data.",
            "At the end you will see your cognitive profile.",
        ],
        key_bindings=[
            ("arrows + ENTER", "select and play task"),
            ("S", "synthetic data"),
            ("ESC", "menu"),
        ],
    )
