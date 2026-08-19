# src/cognitive_data_arcade/games/recommendation_bubble/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Recommendation Bubble",
            description_lines=[
                "Zagraj jako uzytkownik, kurator i algorytm.",
                "Obserwuj, jak preferencje staja się banka informacyjna.",
                "Algorytm nie jest zly -- optymalizuje to, o co go prosisz.",
            ],
            key_bindings=[
                ("Klik na pasek / kafelek", "konsumuj / zamieniaj / rekomenduj"),
                ("SPACJA", "pomin ekran przejscia"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Recommendation Bubble",
        description_lines=[
            "Play as user, curator and algorithm.",
            "Watch how preferences become a filter bubble.",
            "The algorithm is not evil -- it optimizes what you ask for.",
        ],
        key_bindings=[
            ("Click bar / tile", "consume / swap / recommend"),
            ("SPACE", "skip interlude"),
            ("ESC", "pause"),
        ],
    )
