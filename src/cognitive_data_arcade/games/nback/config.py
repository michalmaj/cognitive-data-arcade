from __future__ import annotations

import random
from dataclasses import dataclass
from typing import NamedTuple

LETTERS = ("B", "C", "D", "F", "G", "H", "K", "T")


class Trial(NamedTuple):
    position: int   # 0-8
    letter: str     # one of LETTERS
    pos_match: bool
    let_match: bool


@dataclass(frozen=True)
class NBackConfig:
    n: int | None                          # 1, 2, 3, or None (adaptive)
    trials_per_block: int = 20
    num_blocks: int = 4                    # 80 trials total
    stimulus_ms: int = 500
    isi_ms: int = 2000                     # response window after stimulus offset
    iti_ms: int = 300                      # blank inter-trial interval
    between_blocks_ms: int = 1500          # auto-advance pause between blocks
    target_rate: float = 0.33
    adaptive_up_threshold: float = 0.80
    adaptive_down_threshold: float = 0.50
    ap_per_hit: int = 3
    ap_per_false_alarm: int = -1
    sp_dprime_bonus: int = 20
    dprime_threshold: float = 2.0


NBACK_1 = NBackConfig(n=1)
NBACK_2 = NBackConfig(n=2)
NBACK_3 = NBackConfig(n=3)
NBACK_ADAPTIVE = NBackConfig(n=None)


def generate_block(
    n: int,
    trials_per_block: int,
    target_rate: float,
    rng: random.Random,
) -> list[Trial]:
    """Generate one block of N-Back trials.

    For each trial at index i >= n, independently for position and letter:
    - With probability target_rate: force a match (set value = value[i-n]).
    - Otherwise: ensure no accidental match by adjusting to adjacent value.
    """
    positions = [rng.randint(0, 8) for _ in range(trials_per_block)]
    letters = [rng.choice(LETTERS) for _ in range(trials_per_block)]

    for i in range(n, trials_per_block):
        if rng.random() < target_rate:
            positions[i] = positions[i - n]
        elif positions[i] == positions[i - n]:
            positions[i] = (positions[i] + 1) % 9

        if rng.random() < target_rate:
            letters[i] = letters[i - n]
        elif letters[i] == letters[i - n]:
            idx = LETTERS.index(letters[i])
            letters[i] = LETTERS[(idx + 1) % len(LETTERS)]

    trials: list[Trial] = []
    for i in range(trials_per_block):
        pos_match = (i >= n) and (positions[i] == positions[i - n])
        let_match = (i >= n) and (letters[i] == letters[i - n])
        trials.append(
            Trial(
                position=positions[i],
                letter=letters[i],
                pos_match=pos_match,
                let_match=let_match,
            )
        )
    return trials
