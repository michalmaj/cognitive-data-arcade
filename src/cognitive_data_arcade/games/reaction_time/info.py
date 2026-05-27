from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Reaction Time Lab",
            description_lines=[
                "Prosty czas reakcji to czas między pojawieniem się bodźca a naciśnięciem klawisza.",
                "Obserwuj środkowe kółko. Gdy zaświeci — naciśnij SPACJĘ jak najszybciej.",
                "Ignoruj pozostałe kółka — to tylko rozpraszacze.",
            ],
            key_bindings=[
                ("SPACJA", "reaguj gdy zaświeci kółko"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Reaction Time Lab",
        description_lines=[
            "Simple reaction time is the time between a stimulus appearing and a key press.",
            "Watch the centre circle. When it lights up, press SPACE as fast as possible.",
            "Ignore the other circles — they are distractors.",
        ],
        key_bindings=[
            ("SPACE", "react when circle lights up"),
            ("ESC", "pause"),
        ],
    )
