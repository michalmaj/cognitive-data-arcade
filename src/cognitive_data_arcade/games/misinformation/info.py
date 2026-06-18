# src/cognitive_data_arcade/games/misinformation/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Misinformation Spread",
            description_lines=[
                "Zagraj jako Spreader: zaraz siec dezinformacja.",
                "Potem jako Fact-Checker: zatrzymaj epidemie klikanem.",
                "Odkryj, czemu sianie jest latwe, a leczenie trudne.",
            ],
            key_bindings=[
                ("Klik na wezel", "zaraz (Spreader) lub wylecz (Fact-Checker)"),
                ("SPACJA", "pomin ekran przejscia"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Misinformation Spread",
        description_lines=[
            "Play as Spreader: infect the network with misinformation.",
            "Then as Fact-Checker: stop the epidemic by clicking.",
            "Discover why spreading is easy and fact-checking is hard.",
        ],
        key_bindings=[
            ("Click node", "infect (Spreader) or cure (Fact-Checker)"),
            ("SPACE", "skip interlude"),
            ("ESC", "pause"),
        ],
    )
