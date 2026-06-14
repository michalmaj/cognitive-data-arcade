# src/cognitive_data_arcade/games/overfitting_monster/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Overfitting Monster",
            description_lines=[
                "Dobierz k dla KNN i podział trening/test, by model dobrze generalizował.",
                "Obserwuj na żywo gap między dokładnością treningową a testową.",
                "5 rund — od czystych chmur po zaszumione półksiężyce.",
            ],
            key_bindings=[
                ("Suwak split", "podział danych trening/test"),
                ("Suwak k", "liczba sąsiadów KNN"),
                ("PPM na ekranie", "podpowiedź o scenariuszu"),
            ],
        )
    return GameInfo(
        title="Overfitting Monster",
        description_lines=[
            "Pick KNN k and train/test split so the model generalises well.",
            "Watch the live train-test accuracy gap and avoid overfitting.",
            "5 rounds — from clean blobs to noisy moons.",
        ],
        key_bindings=[
            ("Split slider", "train/test data split"),
            ("k slider", "KNN neighbours"),
            ("RMB on screen", "dataset hint"),
        ],
    )
