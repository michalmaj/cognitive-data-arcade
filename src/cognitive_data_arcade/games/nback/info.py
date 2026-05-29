from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="N-Back Memory Grid",
            description_lines=[
                "Zadanie N-Back mierzy pamięć roboczą i zdolność do aktualizacji informacji.",
                "Monitoruj dwa strumienie jednocześnie: pozycję kwadratu na siatce 3x3 oraz literę.",
                "Naciśnij A gdy pozycja pasuje do tej sprzed N kroków. Naciśnij L gdy litera pasuje.",
                "Strumienie są niezależne — możesz wcisnąć oba, jeden lub żaden.",
            ],
            key_bindings=[
                ("A", "pozycja pasuje"),
                ("L", "litera pasuje"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="N-Back Memory Grid",
        description_lines=[
            "The N-Back task measures working memory and the ability to update information.",
            "Monitor two streams simultaneously: position on a 3x3 grid and a letter.",
            "Press A when the position matches the one N steps earlier. Press L for the letter.",
            "The streams are independent — you may press both, one, or neither.",
        ],
        key_bindings=[
            ("A", "position matches"),
            ("L", "letter matches"),
            ("ESC", "pause"),
        ],
    )
