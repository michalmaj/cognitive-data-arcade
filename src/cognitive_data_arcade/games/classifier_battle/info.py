from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Classifier Battle",
            description_lines=[
                "Narysuj granicę między klasami punktów na wykresie.",
                "Porównaj swoją dokładność z KNN, regresją logistyczną i drzewem.",
                "5 rund — od prostych chmur po splecione półksiężyce.",
            ],
            key_bindings=[
                ("LPM + przeciągnij", "narysuj granicę"),
                ("PPM na ekranie", "podpowiedź o danych"),
            ],
        )
    return GameInfo(
        title="Classifier Battle",
        description_lines=[
            "Draw a decision boundary between two classes of points.",
            "Compare your accuracy against KNN, logistic regression, and decision tree.",
            "5 rounds — from simple blobs to interleaved moons.",
        ],
        key_bindings=[
            ("LMB + drag", "draw boundary"),
            ("RMB on canvas", "dataset hint"),
        ],
    )
