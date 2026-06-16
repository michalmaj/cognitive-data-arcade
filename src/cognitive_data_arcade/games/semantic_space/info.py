from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Semantic Space Explorer",
            description_lines=[
                "Eksploruj mape semantyczna 50 polskich slow.",
                "8 misji: sasiedzi, intruz, most, analogia wektorowa.",
                "Odkryj, jak embeddingi koduja znaczenie geometrycznie.",
            ],
            key_bindings=[
                ("Klik na wezel", "zaznacz slowo"),
                ("SPACJA", "zatwierdz odpowiedz"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Semantic Space Explorer",
        description_lines=[
            "Explore a semantic map of 50 Polish words.",
            "8 missions: neighbors, odd-one-out, bridge, vector analogy.",
            "Discover how embeddings encode meaning geometrically.",
        ],
        key_bindings=[
            ("Click node", "select word"),
            ("SPACE", "submit answer"),
            ("ESC", "pause"),
        ],
    )
