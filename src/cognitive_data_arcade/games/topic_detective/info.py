from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Topic Detective",
            description_lines=[
                "Odkryj ukryte tematy w dokumentach tekstowych.",
                "8 misji: nazwij temat, przypisz dokument, znajdz intruza.",
                "Naucz sie jak LDA koduje tematy jako rozklady slow.",
            ],
            key_bindings=[
                ("Klik", "wybierz odpowiedz"),
                ("SPACJA", "zatwierdz odpowiedz"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Topic Detective",
        description_lines=[
            "Uncover hidden topics in text documents.",
            "8 missions: name topic, assign document, find intruder.",
            "Learn how LDA encodes topics as word distributions.",
        ],
        key_bindings=[
            ("Click", "select answer"),
            ("SPACE", "submit answer"),
            ("ESC", "pause"),
        ],
    )
