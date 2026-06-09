from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Visual Search Lab",
            description_lines=[
                "Wcielasz się w badacza prowadzącego klasyczny eksperyment przeszukiwania wzrokowego.",
                "W bloku 1 szukasz celu wśród różnych dystraktorów (efekt pop-out).",
                "W bloku 2 cel dzieli cechy z dystraktorami — musisz przejrzeć każdy element.",
                "Sprawdź jak liczba elementów wpływa na czas reakcji w obu warunkach!",
            ],
            key_bindings=[
                ("F", "brak targetu"),
                ("J", "target obecny"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Visual Search Lab",
        description_lines=[
            "Play a researcher running a classic visual search experiment.",
            "Block 1: find the target among different distractors (pop-out search).",
            "Block 2: the target shares features with distractors — scan each item.",
            "Observe how set size affects RT differently in each condition!",
        ],
        key_bindings=[
            ("F", "target absent"),
            ("J", "target present"),
            ("ESC", "pause"),
        ],
    )
