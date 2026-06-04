from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Event Log Detective",
            description_lines=[
                "Wejdz w role eksperymentatora i skonfiguruj badanie naukowe.",
                "Podejmij decyzje dotyczace formatow danych, nazewnictwa plikow i struktury.",
                "Raport pokazuje konsekwencje kazdego wyboru.",
                "Easy = poglad konsekwencji, Medium = wskazowka, Hard = brak pomocy.",
            ],
            key_bindings=[
                ("UP/DOWN", "nawigacja"),
                ("ENTER", "otworz / potwierdz"),
                ("1-4", "wybierz opcje"),
                ("H", "wskazowka (Medium)"),
                ("BACKSPACE", "wroc do mapy"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Event Log Detective",
        description_lines=[
            "Step into the role of an experimenter and configure a scientific study.",
            "Make decisions about data formats, file naming, and data structure.",
            "The report shows the consequences of every choice.",
            "Easy = consequence preview, Medium = hint available, Hard = no help.",
        ],
        key_bindings=[
            ("UP/DOWN", "navigate"),
            ("ENTER", "open / confirm"),
            ("1-4", "select option"),
            ("H", "hint (Medium)"),
            ("BACKSPACE", "back to map"),
            ("ESC", "pause"),
        ],
    )
