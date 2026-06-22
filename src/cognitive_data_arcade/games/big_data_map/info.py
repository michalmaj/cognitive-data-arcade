from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Siec Pojec",
            description_lines=[
                "Interaktywna siec pojec laczaca wszystkie 31 lekcji kursu.",
                "Nawiguj strzalkami lub mysza. ENTER otwiera wybrana lekcje.",
                "Krawedzie lacza lekcje dzielace wspolne pojecia.",
            ],
            key_bindings=[
                ("LEWO / PRAWO", "poprzednia / nastepna lekcja"),
                ("ENTER", "otworz lekcje w czytniku"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Concept Network",
        description_lines=[
            "An interactive concept network linking all 31 course lessons.",
            "Navigate with arrow keys or mouse. ENTER opens the selected lesson.",
            "Edges connect lessons that share common concepts.",
        ],
        key_bindings=[
            ("LEFT / RIGHT", "previous / next lesson"),
            ("ENTER", "open lesson in reader"),
            ("ESC", "pause"),
        ],
    )
