# src/cognitive_data_arcade/games/word_weight_factory/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Word Weight Factory",
            description_lines=[
                "Obserwuj jak tekst staje sie wektorem liczb.",
                "Pipeline: Korpus -> BoW -> TF -> IDF -> TF-IDF.",
                "Zmien preprocessing i obserwuj zmiany w macierzy.",
            ],
            key_bindings=[
                ("LEWO / PRAWO", "zmien krok"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Word Weight Factory",
        description_lines=[
            "Watch text become a vector of numbers.",
            "Pipeline: Corpus -> BoW -> TF -> IDF -> TF-IDF.",
            "Change preprocessing and observe matrix changes.",
        ],
        key_bindings=[
            ("LEFT / RIGHT", "change step"),
            ("ESC", "pause"),
        ],
    )
