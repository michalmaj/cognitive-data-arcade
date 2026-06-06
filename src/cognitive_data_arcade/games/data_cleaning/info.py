# src/cognitive_data_arcade/games/data_cleaning/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Data Quality Lab",
            description_lines=[
                "Masz dane z eksperymentu behawioralnego. Znajdz i popraw bledy w zbiorze.",
                "Wybierz poziom trudnosci, przegladaj wiersze i zaznaczaj te z bledami.",
                "W fazie poprawy wpisz poprawne wartosci dla zaznaczonych wierszy.",
            ],
            key_bindings=[
                ("1 / 2 / 3", "poziom trudnosci"),
                ("LEWO / PRAWO", "zmien poziom"),
                ("ENTER", "start / zatwierdz"),
                ("SPACJA", "flaguj wiersz"),
                ("H", "pokaz/ukryj wskazowki (Medium)"),
                ("L", "legenda kolumn"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Data Quality Lab",
        description_lines=[
            "You have data from a behavioural experiment. Find and fix errors in the dataset.",
            "Choose a difficulty level, browse rows and flag those with errors.",
            "In the fix phase, type in the correct values for the flagged rows.",
        ],
        key_bindings=[
            ("1 / 2 / 3", "difficulty level"),
            ("LEFT / RIGHT", "change level"),
            ("ENTER", "start / confirm"),
            ("SPACE", "flag row"),
            ("H", "show/hide hints (Medium)"),
            ("L", "column legend"),
            ("ESC", "pause"),
        ],
    )
