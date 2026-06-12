from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Prediction Slider",
            description_lines=[
                "Naucz się przewidywać wartości na podstawie regresji liniowej.",
                "Ustaw predykcje Y dla zadanych X — sprawdź jak blisko jesteś!",
                "Odkryj jak outlier może całkowicie zmienić linię regresji.",
                "Zrozum czym jest R² i reszty (residuals).",
            ],
            key_bindings=[
                ("LEWO / PRAWO", "zmień fazę"),
                ("PPM (faza C)", "pokaż/ukryj linię bazową"),
            ],
        )
    return GameInfo(
        title="Prediction Slider",
        description_lines=[
            "Learn to predict values using linear regression.",
            "Set Y predictions for given X values — see how close you are!",
            "Discover how a single outlier can tilt the regression line.",
            "Understand R² and residuals.",
        ],
        key_bindings=[
            ("LEFT / RIGHT", "switch phase"),
            ("RMB (phase C)", "show/hide baseline"),
        ],
    )
