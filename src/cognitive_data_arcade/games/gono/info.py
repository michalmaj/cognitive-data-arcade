from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Go/No-Go Guard",
            description_lines=[
                "Zadanie Go/No-Go mierzy kontrolę impulsów i zdolność hamowania odpowiedzi.",
                "Zielony krąg = Go — naciśnij SPACJĘ jak najszybciej.",
                "Czerwony krąg = No-Go — powstrzymaj się od naciśnięcia SPACJI.",
                "Wskaźnik d-prime mierzy zdolność rozróżniania sygnałów od szumów.",
            ],
            key_bindings=[
                ("SPACJA", "Go — zielony krąg"),
                ("(nic)", "No-Go — czerwony krąg"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Go/No-Go Guard",
        description_lines=[
            "The Go/No-Go task measures impulse control and response inhibition.",
            "Green circle = Go — press SPACE as fast as possible.",
            "Red circle = No-Go — withhold your response.",
            "Your d-prime score measures your ability to discriminate signal from noise.",
        ],
        key_bindings=[
            ("SPACE", "Go — green circle"),
            ("(none)", "No-Go — red circle"),
            ("ESC", "pause"),
        ],
    )
