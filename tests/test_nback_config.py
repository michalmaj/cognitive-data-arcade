from __future__ import annotations

import random

import pytest

from cognitive_data_arcade.games.nback.config import (
    LETTERS,
    NBACK_1,
    NBACK_2,
    NBACK_3,
    NBACK_ADAPTIVE,
    Trial,
    generate_block,
)


def test_generate_block_correct_length():
    rng = random.Random(42)
    block = generate_block(1, 20, 0.33, rng)
    assert len(block) == 20


def test_first_n_trials_have_no_match():
    rng = random.Random(42)
    block = generate_block(2, 20, 0.33, rng)
    assert not block[0].pos_match
    assert not block[0].let_match
    assert not block[1].pos_match
    assert not block[1].let_match


def test_target_rate_approximate():
    rng = random.Random(0)
    pos_matches = 0
    let_matches = 0
    eligible = 0
    n = 1
    for _ in range(100):
        block = generate_block(n, 20, 0.33, rng)
        for trial in block[n:]:
            eligible += 1
            if trial.pos_match:
                pos_matches += 1
            if trial.let_match:
                let_matches += 1
    pos_rate = pos_matches / eligible
    let_rate = let_matches / eligible
    assert abs(pos_rate - 0.33) < 0.10
    assert abs(let_rate - 0.33) < 0.10


def test_streams_are_independent():
    rng = random.Random(7)
    both = pos_only = let_only = neither = 0
    for _ in range(100):
        block = generate_block(1, 20, 0.33, rng)
        for t in block[1:]:
            if t.pos_match and t.let_match:
                both += 1
            elif t.pos_match:
                pos_only += 1
            elif t.let_match:
                let_only += 1
            else:
                neither += 1
    assert both > 0
    assert pos_only > 0
    assert let_only > 0
    assert neither > 0


def test_no_accidental_matches_when_not_forced():
    rng = random.Random(99)
    for _ in range(20):
        block = generate_block(1, 20, 0.0, rng)
        for t in block[1:]:
            assert not t.pos_match
            assert not t.let_match


def test_all_match_when_target_rate_1():
    rng = random.Random(3)
    block = generate_block(1, 20, 1.0, rng)
    for t in block[1:]:
        assert t.pos_match
        assert t.let_match


def test_presets_n_values():
    assert NBACK_1.n == 1
    assert NBACK_2.n == 2
    assert NBACK_3.n == 3
    assert NBACK_ADAPTIVE.n is None


def test_letters_constant():
    assert len(LETTERS) == 8
    assert all(isinstance(c, str) and len(c) == 1 for c in LETTERS)
