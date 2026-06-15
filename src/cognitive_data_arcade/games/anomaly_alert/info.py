# src/cognitive_data_arcade/games/anomaly_alert/info.py
from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Anomaly Alert",
            description_lines=[
                "Kliknij na podejrzane punkty danych w 6 typach wykresow.",
                "Za trafienie +20 pkt, za falszywy alarm -5 pkt.",
                "6 rund -- od prostych skokow po subtelne anomalie w macierzy EEG.",
            ],
            key_bindings=[
                ("LPM na wykresie", "zaznacz / odznacz punkt"),
                ("PPM na wykresie", "podpowiedz o typie wykresu"),
                ("Enter / Zatwierdz", "potwierdz wybor"),
            ],
        )
    return GameInfo(
        title="Anomaly Alert",
        description_lines=[
            "Click suspicious data points across 6 chart types.",
            "Hit: +20 pts, False alarm: -5 pts, Time bonus: +10 pts.",
            "6 rounds -- from obvious spikes to subtle EEG matrix anomalies.",
        ],
        key_bindings=[
            ("LMB on chart", "select / deselect point"),
            ("RMB on chart", "chart type hint"),
            ("Enter / Confirm", "submit selection"),
        ],
    )
