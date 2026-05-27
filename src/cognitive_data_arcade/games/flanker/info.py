from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Flanker Arena",
            description_lines=[
                "Zadanie Eriksena Flankera mierzy selektywną uwagę i hamowanie odpowiedzi.",
                "Na ekranie pojawia się pięć strzałek. Środkowa to cel — naciśnij ← lub → zgodnie z jej kierunkiem.",
                "Gdy flankerzy (boczne strzałki) są niezgodne z celem, czas reakcji wydłuża się. To efekt flankera.",
            ],
            key_bindings=[
                ("←", "cel wskazuje lewo"),
                ("→", "cel wskazuje prawo"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Flanker Arena",
        description_lines=[
            "The Eriksen Flanker task measures selective attention and response inhibition.",
            "Five arrows appear on screen. Press ← or → to match the direction of the centre arrow.",
            "When flanking arrows conflict with the target, reaction time increases — the flanker effect.",
        ],
        key_bindings=[
            ("←", "target points left"),
            ("→", "target points right"),
            ("ESC", "pause"),
        ],
    )
