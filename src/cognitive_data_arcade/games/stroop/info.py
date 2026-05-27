from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Wyzwanie Stroopa",
            description_lines=[
                "Efekt Stroopa to klasyczny fenomen psychologiczny odkryty w 1935 roku.",
                "Słowo pojawi się w kolorowym tuszu. Nazwij kolor TUSZU — ignoruj znaczenie słowa.",
                "Gdy kolor i słowo są niezgodne, czas reakcji wzrasta. To właśnie efekt Stroopa.",
            ],
            key_bindings=[
                ("R", "Czerwony"),
                ("G", "Zielony"),
                ("B", "Niebieski"),
                ("Y", "Żółty"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Stroop Challenge",
        description_lines=[
            "The Stroop effect is a classic psychological phenomenon discovered in 1935.",
            "A word appears in coloured ink. Name the INK COLOUR — ignore what the word says.",
            "When colour and word conflict, reaction time increases — the Stroop effect.",
        ],
        key_bindings=[
            ("R", "Red"),
            ("G", "Green"),
            ("B", "Blue"),
            ("Y", "Yellow"),
            ("ESC", "pause"),
        ],
    )
