from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Flanker Arena",
            description_lines=[
                "Zadanie Eriksena Flankera mierzy selektywną uwagę i hamowanie odpowiedzi.",
                "Na ekranie pojawia się pięć strzałek. Środkowa to cel — naciśnij LEWO lub PRAWO zgodnie z jej kierunkiem.",
                "Gdy flankerzy (boczne strzałki) są niezgodne z celem, czas reakcji wydłuża się. To efekt flankera.",
            ],
            key_bindings=[
                ("LEWO", "cel wskazuje lewo"),
                ("PRAWO", "cel wskazuje prawo"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Flanker Arena",
        description_lines=[
            "The Eriksen Flanker task measures selective attention and response inhibition.",
            "Five arrows appear on screen. Press LEFT or RIGHT to match the direction of the centre arrow.",
            "When flanking arrows conflict with the target, reaction time increases — the flanker effect.",
        ],
        key_bindings=[
            ("LEFT", "target points left"),
            ("RIGHT", "target points right"),
            ("ESC", "pause"),
        ],
    )
