# src/cognitive_data_arcade/games/emotion_classifier/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Emotion Classifier",
            description_lines=[
                "Oznaczaj slowa pozytywne (LPM) i negatywne (PPM) w zdaniach.",
                "Obserwuj jak leksykon sumuje wagi -- i gdzie sie myli.",
                "8 rund: negacja, ironia, intensywnosc. Pobij klasyfikator!",
            ],
            key_bindings=[
                ("LPM na slowie", "oznacz jako pozytywne"),
                ("PPM na slowie", "oznacz jako negatywne"),
                ("PPM na zdaniu", "podpowiedz o pulapce"),
                ("SPACJA", "zatwierdz odpowiedz"),
            ],
        )
    return GameInfo(
        title="Emotion Classifier",
        description_lines=[
            "Tag positive (LMB) and negative (RMB) words in Polish sentences.",
            "Watch the lexicon sum weights live -- and see where it fails.",
            "8 rounds: negation, irony, intensity. Beat the classifier!",
        ],
        key_bindings=[
            ("LMB on word", "tag as positive"),
            ("RMB on word", "tag as negative"),
            ("RMB on sentence", "show trap hint"),
            ("SPACE", "submit answer"),
        ],
    )
