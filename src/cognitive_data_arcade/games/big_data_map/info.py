from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Big Data w Kognitywistyce",
            description_lines=[
                "Interaktywna sieć pojęć łącząca metody Big Data z kognitywistyką.",
                "Eksploruj sześć gałęzi: od neuroobrazowania i śledzenia wzroku po cyfrową fenotypizację.",
                "Węzły ze złotą obwódką to gry dostępne w menu lekcji — możesz je wypróbować.",
            ],
            key_bindings=[
                ("GORA / DOL", "nawigacja między węzłami"),
                ("ENTER", "rozwiń gałąź / wróć do L1"),
                ("BACKSPACE", "wróć do L1"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Big Data in Cognitive Science",
        description_lines=[
            "An interactive concept network linking Big Data methods to cognitive science.",
            "Explore six branches: from neuroimaging and eye tracking to digital phenotyping.",
            "Nodes with a gold border are games available in the lesson menu — try them out.",
        ],
        key_bindings=[
            ("UP / DOWN", "navigate between nodes"),
            ("ENTER", "expand branch / back to L1"),
            ("BACKSPACE", "back to L1"),
            ("ESC", "pause"),
        ],
    )
