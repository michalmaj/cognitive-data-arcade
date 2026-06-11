from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Correlation Trap",
            description_lines=[
                "Odkryj roznice miedzy korelacja a przyczynowoscia.",
                "Faza A: eksploruj jak wyglada r na wykresie punktowym.",
                "Faza B: wykryj ktorej korelacje sa pulapkami.",
                "Faza C: zestawiaj dowolne pary zmiennych.",
            ],
            key_bindings=[
                ("LEWO / PRAWO", "zmien faze"),
                ("PPM (prawy klik)", "kontekstowa pomoc"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Correlation Trap",
        description_lines=[
            "Discover the difference between correlation and causation.",
            "Phase A: explore what r looks like on a scatter plot.",
            "Phase B: detect which correlations are traps.",
            "Phase C: pair any two variables in the sandbox.",
        ],
        key_bindings=[
            ("LEFT / RIGHT", "change phase"),
            ("Right-click", "contextual help"),
            ("ESC", "pause"),
        ],
    )
