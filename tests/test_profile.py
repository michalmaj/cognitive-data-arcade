from __future__ import annotations

from cognitive_data_arcade.games.cognitive_dashboard.profile import cognitive_profile
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession, TaskResult


def _make_result(
    rt_ms: list[float], conditions: list[str], correct: list[bool] | None = None
) -> TaskResult:
    if correct is None:
        correct = [True] * len(rt_ms)
    return TaskResult(rt_ms=rt_ms, correct=correct, condition=conditions)


def _full_session(
    stroop_effect_ms: float,
    flanker_effect_ms: float,
    gonogo_fa_count: int,
) -> DashboardSession:
    base_rt = 300.0
    rt = _make_result([base_rt] * 8, ["simple"] * 8)

    # rt_ms order: congruent first, then incongruent
    stroop = _make_result(
        [base_rt] * 4 + [base_rt + stroop_effect_ms] * 4,
        ["congruent"] * 4 + ["incongruent"] * 4,
    )

    flanker = _make_result(
        [base_rt] * 4 + [base_rt + flanker_effect_ms] * 4,
        ["congruent"] * 4 + ["incongruent"] * 4,
    )

    # GoNoGo: 6 go (correct) + 2 nogo; fa_count nogo trials are false alarms
    nogo_correct = [False] * gonogo_fa_count + [True] * (2 - gonogo_fa_count)
    gonogo = _make_result(
        [-1.0] * 6 + [-1.0] * 2,
        ["go"] * 6 + ["nogo"] * 2,
        correct=[True] * 6 + nogo_correct,
    )

    return DashboardSession(rt=rt, stroop=stroop, flanker=flanker, gonogo=gonogo)


def test_profile_returns_list_of_strings() -> None:
    s = _full_session(50.0, 40.0, 1)
    result = cognitive_profile(s)
    assert isinstance(result, list)
    assert all(isinstance(line, str) for line in result)
    assert len(result) >= 2


def test_profile_stroop_low_effect() -> None:
    s = _full_session(stroop_effect_ms=30.0, flanker_effect_ms=40.0, gonogo_fa_count=0)
    text = " ".join(cognitive_profile(s))
    assert "30" in text  # effect value present


def test_profile_stroop_medium_effect() -> None:
    s = _full_session(stroop_effect_ms=60.0, flanker_effect_ms=40.0, gonogo_fa_count=0)
    text = " ".join(cognitive_profile(s))
    assert "60" in text


def test_profile_stroop_high_effect() -> None:
    s = _full_session(stroop_effect_ms=90.0, flanker_effect_ms=40.0, gonogo_fa_count=0)
    text = " ".join(cognitive_profile(s))
    assert "90" in text


def test_profile_flanker_low_effect() -> None:
    s = _full_session(stroop_effect_ms=50.0, flanker_effect_ms=15.0, gonogo_fa_count=0)
    text = " ".join(cognitive_profile(s))
    assert "15" in text


def test_profile_flanker_medium_effect() -> None:
    s = _full_session(stroop_effect_ms=50.0, flanker_effect_ms=40.0, gonogo_fa_count=0)
    text = " ".join(cognitive_profile(s))
    assert "40" in text


def test_profile_flanker_high_effect() -> None:
    s = _full_session(stroop_effect_ms=50.0, flanker_effect_ms=70.0, gonogo_fa_count=0)
    text = " ".join(cognitive_profile(s))
    assert "70" in text


def test_profile_gonogo_no_fa() -> None:
    s = _full_session(stroop_effect_ms=50.0, flanker_effect_ms=40.0, gonogo_fa_count=0)
    text = " ".join(cognitive_profile(s)).lower()
    assert "0" in text
    assert "no-go" in text


def test_profile_gonogo_one_fa() -> None:
    s = _full_session(stroop_effect_ms=50.0, flanker_effect_ms=40.0, gonogo_fa_count=1)
    text = " ".join(cognitive_profile(s)).lower()
    assert "1" in text
    assert "no-go" in text


def test_profile_gonogo_many_fa() -> None:
    s = _full_session(stroop_effect_ms=50.0, flanker_effect_ms=40.0, gonogo_fa_count=2)
    text = " ".join(cognitive_profile(s)).lower()
    assert "2" in text
    assert "no-go" in text


def test_profile_closing_sentence_shows_actual_trial_count() -> None:
    s = _full_session(50.0, 40.0, 0)
    lines = cognitive_profile(s)
    closing = lines[-1]
    # Total: 8 (rt) + 8 (stroop) + 8 (flanker) + 8 (gonogo) = 32 trials
    assert "32" in closing
