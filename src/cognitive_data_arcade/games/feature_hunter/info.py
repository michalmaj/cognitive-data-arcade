from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Feature Hunter",
            description_lines=[
                "Posegreguj cechy danych: Przydatne vs Szum.",
                "Scatter plot pokazuje związek cechy z celem.",
                "Im wyraźniejszy trend, tym bardziej przydatna cecha.",
            ],
            key_bindings=[
                ("LPM + przeciągnij", "przypisz kartę do kubka"),
                ("PPM (Easy/Medium)", "podpowiedź"),
            ],
        )
    return GameInfo(
        title="Feature Hunter",
        description_lines=[
            "Sort features into Useful vs Noise bins.",
            "The scatter plot shows the feature-target relationship.",
            "A clearer trend means a more useful feature.",
        ],
        key_bindings=[
            ("LMB + drag", "assign card to bin"),
            ("RMB (Easy/Medium)", "hint"),
        ],
    )
