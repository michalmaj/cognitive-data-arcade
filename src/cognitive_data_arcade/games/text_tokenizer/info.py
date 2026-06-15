from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Text Tokenizer Lab",
            description_lines=[
                "Eksploruj przetwarzanie tekstu krok po kroku.",
                "Przeglad tokenizacji, n-gramow i czestosci slow.",
                "Zmieniaj ustawienia i obserwuj wyniki w czasie rzeczywistym.",
            ],
            key_bindings=[
                ("LEWO / PRAWO", "zmien faze"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Text Tokenizer Lab",
        description_lines=[
            "Explore text preprocessing step by step.",
            "Browse tokenization, n-grams and word frequency.",
            "Adjust settings and observe results in real time.",
        ],
        key_bindings=[
            ("LEFT / RIGHT", "change phase"),
            ("ESC", "pause"),
        ],
    )
