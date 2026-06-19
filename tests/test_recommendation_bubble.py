import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest


def test_diversity_uniform():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        diversity, uniform_profile,
    )
    p = uniform_profile()
    assert abs(diversity(p) - 0.8) < 0.01


def test_diversity_single_category():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        diversity, CATEGORIES,
    )
    p = {cat: 0.0 for cat in CATEGORIES}
    p["SPORT"] = 1.0
    assert diversity(p) == 0.0


def test_profile_from_clicks_normalises():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        profile_from_clicks, CATEGORIES,
    )
    clicks = {cat: 0 for cat in CATEGORIES}
    clicks["SPORT"] = 8
    clicks["NAUKA"] = 2
    p = profile_from_clicks(clicks)
    assert abs(p["SPORT"] - 0.8) < 0.01
    assert abs(sum(p.values()) - 1.0) < 1e-9


def test_profile_from_clicks_empty_returns_uniform():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        profile_from_clicks, CATEGORIES, uniform_profile,
    )
    clicks = {cat: 0 for cat in CATEGORIES}
    p = profile_from_clicks(clicks)
    u = uniform_profile()
    for cat in CATEGORIES:
        assert abs(p[cat] - u[cat]) < 1e-9


def test_curated_profile_counts_slots():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        curated_profile,
    )
    slots = ["SPORT", "SPORT", "SPORT", "NAUKA", "POLITYKA", "MUZYKA"]
    p = curated_profile(slots)
    assert abs(p["SPORT"] - 0.5) < 0.01
    assert abs(sum(p.values()) - 1.0) < 1e-9


def test_generate_slots_dominated_by_heavy_category():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        generate_slots, CATEGORIES,
    )
    profile = {cat: 0.0 for cat in CATEGORIES}
    profile["SPORT"] = 1.0
    slots = generate_slots(profile, n=6, seed=42)
    assert all(s == "SPORT" for s in slots)


def test_game_state_defaults():
    from cognitive_data_arcade.games.recommendation_bubble.game_state import (
        GameState, CATEGORIES,
    )
    gs = GameState()
    assert set(gs.bubble.keys()) == set(CATEGORIES)
    assert abs(sum(gs.bubble.values()) - 1.0) < 1e-9
    assert gs.score_curator == 0
    assert gs.score_algo == 0
