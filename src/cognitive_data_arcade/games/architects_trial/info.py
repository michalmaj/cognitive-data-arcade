# src/cognitive_data_arcade/games/architects_trial/info.py
from __future__ import annotations
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings is not None and strings.language == "pl":
        return GameInfo(
            title="The Architect's Trial",
            description_lines=[
                "Zaprojektuj system AI dla instytucji publicznej.",
                "Podejmij 3 decyzje projektowe.",
                "Staj przed komisja etyczna.",
            ],
            key_bindings=[
                ("Klik / strzalki + ENTER", "wybor"),
                ("SPACJA", "przejdz dalej"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="The Architect's Trial",
        description_lines=[
            "Design an AI system for a public institution.",
            "Make 3 architectural decisions.",
            "Face the ethics committee.",
        ],
        key_bindings=[
            ("Click / arrows + ENTER", "choose"),
            ("SPACE", "advance"),
            ("ESC", "pause"),
        ],
    )
