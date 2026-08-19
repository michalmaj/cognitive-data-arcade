# src/cognitive_data_arcade/games/bias_blind_spot/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Bias Blind Spot",
            description_lines=[
                "Akt 1: Analizuj decyzje algorytmu kredytowego.",
                "Akt 2: Usuwaj cechy -- obserwuj bias i dokladnosc.",
                "Akt 3: Wybierz kryterium sprawiedliwosci.",
            ],
            key_bindings=[
                ("Klik na karty/panele", "wybor"),
                ("SPACJA", "przejdz dalej"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Bias Blind Spot",
        description_lines=[
            "Act 1: Analyse credit algorithm decisions.",
            "Act 2: Remove features -- watch bias and accuracy.",
            "Act 3: Choose a fairness criterion.",
        ],
        key_bindings=[
            ("Click cards/panels", "choose"),
            ("SPACE", "advance"),
            ("ESC", "pause"),
        ],
    )
