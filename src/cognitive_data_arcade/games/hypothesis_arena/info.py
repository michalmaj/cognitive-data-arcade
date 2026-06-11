from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Hypothesis Arena",
            description_lines=[
                "Naucz się odróżniać istotność statystyczną od praktycznej.",
                "p < 0.05 nie znaczy że efekt jest ważny!",
                "Odkryj jak rozmiar próby wpływa na wyniki testu.",
                "Zaprojektuj eksperymenty z odpowiednią mocą statystyczną.",
            ],
            key_bindings=[
                ("LEWO / PRAWO", "zmień fazę"),
                ("kółko myszy", "przewiń prawy panel"),
                ("PPM", "kontekstowa pomoc"),
            ],
        )
    return GameInfo(
        title="Hypothesis Arena",
        description_lines=[
            "Learn to distinguish statistical from practical significance.",
            "p < 0.05 does not mean the effect is important!",
            "Discover how sample size drives test results.",
            "Design experiments with adequate statistical power.",
        ],
        key_bindings=[
            ("LEFT / RIGHT", "switch phase"),
            ("mouse wheel", "scroll right panel"),
            ("RMB", "contextual help"),
        ],
    )
