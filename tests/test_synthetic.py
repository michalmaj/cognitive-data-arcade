from __future__ import annotations

from cognitive_data_arcade.games.cognitive_dashboard.config import (
    MINI_TRIALS,
    SYNTHETIC_PARAMS,
    generate_synthetic,
)
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession


def test_generate_synthetic_returns_complete_session() -> None:
    s = generate_synthetic()
    assert isinstance(s, DashboardSession)
    assert s.is_complete()
    assert s.synthetic is True


def test_generate_synthetic_trial_counts() -> None:
    s = generate_synthetic()
    assert len(s.rt.rt_ms) == MINI_TRIALS
    assert len(s.stroop.rt_ms) == MINI_TRIALS
    assert len(s.flanker.rt_ms) == MINI_TRIALS
    assert len(s.gonogo.rt_ms) == MINI_TRIALS


def test_generate_synthetic_rt_in_range() -> None:
    s = generate_synthetic()
    lo = SYNTHETIC_PARAMS["rt"]["simple"]["lo"]
    hi = SYNTHETIC_PARAMS["rt"]["simple"]["hi"]
    for rt in s.rt.rt_ms:
        assert lo <= rt <= hi, f"RT {rt} out of range [{lo}, {hi}]"


def test_generate_synthetic_stroop_conditions_balanced() -> None:
    s = generate_synthetic()
    congs = s.stroop.condition.count("congruent")
    incongs = s.stroop.condition.count("incongruent")
    assert congs == MINI_TRIALS // 2
    assert incongs == MINI_TRIALS // 2


def test_generate_synthetic_flanker_conditions_balanced() -> None:
    s = generate_synthetic()
    assert s.flanker.condition.count("congruent") == MINI_TRIALS // 2
    assert s.flanker.condition.count("incongruent") == MINI_TRIALS // 2


def test_generate_synthetic_gonogo_counts() -> None:
    s = generate_synthetic()
    go_count = s.gonogo.condition.count("go")
    nogo_count = s.gonogo.condition.count("nogo")
    assert go_count == MINI_TRIALS - 2
    assert nogo_count == 2


def test_generate_synthetic_rt_all_correct() -> None:
    s = generate_synthetic()
    assert all(s.rt.correct)


def test_generate_synthetic_stroop_all_correct() -> None:
    s = generate_synthetic()
    assert all(s.stroop.correct)


def test_generate_synthetic_flanker_all_correct() -> None:
    s = generate_synthetic()
    assert all(s.flanker.correct)
