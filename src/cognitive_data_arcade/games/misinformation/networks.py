# src/cognitive_data_arcade/games/misinformation/networks.py
from __future__ import annotations

import random
from dataclasses import dataclass

from cognitive_data_arcade.games.social_network.graph import (
    Graph, generate_random, generate_scale_free,
)


@dataclass(frozen=True)
class NetworkConfig:
    label: str      # display name, ASCII-safe
    n: int          # node count
    kind: str       # "random" | "scale_free"
    seed: int       # for reproducibility
    p: float = 0.3  # Erdos-Renyi probability (kind="random" only)
    m: int = 2      # BA attachment parameter (kind="scale_free" only)


ROUNDS: list[NetworkConfig] = [
    NetworkConfig(label="LOSOWA",      n=15, kind="random",     seed=42),
    NetworkConfig(label="BEZSKALOWA",  n=20, kind="scale_free", seed=7),
    NetworkConfig(label="BEZSKALOWA+", n=25, kind="scale_free", seed=13),
]


def build_graph(cfg: NetworkConfig) -> Graph:
    """Build a reproducible Graph from a NetworkConfig without disturbing global RNG."""
    rng_state = random.getstate()
    random.seed(cfg.seed)
    if cfg.kind == "random":
        g = generate_random(cfg.n, cfg.p, panel_x=112, panel_w=800)
    else:
        g = generate_scale_free(cfg.n, cfg.m, panel_x=112, panel_w=800)
    random.setstate(rng_state)
    return g
