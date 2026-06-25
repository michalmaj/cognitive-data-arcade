from __future__ import annotations

from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.engine.pause import GameInfo


def get_game_info(strings: Strings) -> GameInfo:
    if strings.language == "pl":
        return GameInfo(
            title="Social Network Simulator",
            description_lines=[
                "Zbuduj siec wezlow i krawedzi, uruchom epidemie SIR.",
                "Porownaj swoja siec z auto-generowana Random lub Scale-free.",
                "Odkryj, dlaczego huby przyspieszaja rozprzestrzenianie się.",
            ],
            key_bindings=[
                ("Klik lewy panel", "dodaj wezel lub krawedz"),
                ("Random/Scale-free", "generuj prawa siec"),
                ("Od huba/Od peryferium", "uruchom spread"),
                ("ESC", "pauza"),
            ],
        )
    return GameInfo(
        title="Social Network Simulator",
        description_lines=[
            "Build a node/edge network and launch an SIR epidemic.",
            "Compare your network with auto-generated Random or Scale-free.",
            "Discover why hubs accelerate spread.",
        ],
        key_bindings=[
            ("Click left panel", "add node or edge"),
            ("Random/Scale-free", "generate right network"),
            ("From hub/periphery", "start spread"),
            ("ESC", "pause"),
        ],
    )
