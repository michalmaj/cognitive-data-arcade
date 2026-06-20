# src/cognitive_data_arcade/games/you_were_the_dataset/info.py
from __future__ import annotations
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings) -> GameInfo:
    if strings is not None and strings.language == "pl":
        return GameInfo(
            title="You Were the Dataset",
            description_lines=[
                "Faza 0: Zbierz dane z poprzednich gier.",
                "Faza 1: Wielki reveal.",
                "Fazy 2-3: Twoj kognitywny profil i AHA.",
            ],
            key_bindings=[
                ("SPACJA", "przejdz dalej"),
                ("Ctrl+D", "tryb developerski"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="You Were the Dataset",
        description_lines=[
            "Phase 0: Collect data from previous games.",
            "Phase 1: The big reveal.",
            "Phases 2-3: Your cognitive profile and AHA.",
        ],
        key_bindings=[
            ("SPACE", "advance"),
            ("Ctrl+D", "developer mode"),
            ("ESC", "pause"),
        ],
    )
