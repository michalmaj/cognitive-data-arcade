from __future__ import annotations

from cognitive_data_arcade.games.cognitive_dashboard.session import (
    DashboardSession,
    TaskResult,
)


def test_task_result_stores_lists() -> None:
    r = TaskResult(rt_ms=[300.0, 250.0], correct=[True, False], condition=["simple", "simple"])
    assert r.rt_ms == [300.0, 250.0]
    assert r.correct == [True, False]


def test_dashboard_session_defaults_none() -> None:
    s = DashboardSession()
    assert s.rt is None
    assert s.stroop is None
    assert s.flanker is None
    assert s.gonogo is None
    assert s.synthetic is False


def test_dashboard_session_is_complete_false_when_missing() -> None:
    s = DashboardSession()
    assert not s.is_complete()


def test_dashboard_session_is_complete_true_when_all_filled() -> None:
    r = TaskResult(rt_ms=[300.0], correct=[True], condition=["simple"])
    s = DashboardSession(rt=r, stroop=r, flanker=r, gonogo=r)
    assert s.is_complete()


def test_dashboard_session_synthetic_flag() -> None:
    r = TaskResult(rt_ms=[300.0], correct=[True], condition=["simple"])
    s = DashboardSession(rt=r, stroop=r, flanker=r, gonogo=r, synthetic=True)
    assert s.synthetic is True


def test_dashboard_session_partially_complete_not_done() -> None:
    r = TaskResult(rt_ms=[300.0], correct=[True], condition=["simple"])
    s = DashboardSession(rt=r, stroop=r)
    assert not s.is_complete()


def test_config_constants() -> None:
    from cognitive_data_arcade.games.cognitive_dashboard.config import (
        FEEDBACK_MS,
        FIXATION_MS,
        MINI_TRIALS,
        TIMEOUT_MS,
    )
    assert MINI_TRIALS == 8
    assert FIXATION_MS == 500
    assert FEEDBACK_MS == 400
    assert TIMEOUT_MS == 3000
