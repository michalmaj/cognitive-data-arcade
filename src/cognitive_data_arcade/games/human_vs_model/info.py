from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Human vs Model",
            description_lines=[
                "Zmierz się z modelem jezykowym na zadaniach NLP.",
                "3 fazy: klasyfikacja, detekcja AI, uzupelnianie zdan.",
                "Pobij AI na trudnych przypadkach i zdobadz bonus!",
            ],
            key_bindings=[
                ("Klik", "wybierz odpowiedz"),
                ("SPACJA", "nastepna runda"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Human vs Model",
        description_lines=[
            "Compete against a language model on NLP tasks.",
            "3 phases: classification, AI detection, sentence completion.",
            "Beat the AI on hard cases to earn bonus points!",
        ],
        key_bindings=[
            ("Click", "select answer"),
            ("SPACE", "next round"),
            ("ESC", "pause"),
        ],
    )
