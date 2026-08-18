"""Tests ensuring dashboard interpretations are session observations, not diagnoses.

These tests enforce the semantic rule:
    task/session result ≠ stable human trait ≠ diagnosis
"""

from __future__ import annotations

import re

import pytest

from cognitive_data_arcade.games.cognitive_dashboard.dashboard_scene import CognitiveDashboardScene
from cognitive_data_arcade.games.cognitive_dashboard.profile import cognitive_profile
from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession, TaskResult

# ── Forbidden patterns ─────────────────────────────────────────────────────
# These appear in diagnostic/normative claims that must not occur in output.
_FORBIDDEN = [
    "norma",  # unsupported normative comparison
    "tendencja do impulsywności",  # diagnosis
    "impulsywności",  # diagnosis synonym
    "odporność na interferencję",  # trait label
    "selektywna uwaga",  # trait label
    "hamowanie impulsów",  # trait label
    "bezbłędne",  # perfection claim
    "bardzo dobra",  # normative judgment
    "bardzo szybki",  # normative judgment
    "przeciętny",  # normative average (without session scope)
]


# ── Fixtures ───────────────────────────────────────────────────────────────


@pytest.fixture()
def session() -> DashboardSession:
    """Complete DashboardSession with known values for assertion."""
    # rt_ms order must match condition order: first 4 congruent (fast), then 4 incongruent (slow)
    # stroop effect: mean([340..355]) - mean([280..295]) = 347.5 - 287.5 = +60 ms
    stroop = TaskResult(
        rt_ms=[280.0, 285.0, 290.0, 295.0, 340.0, 345.0, 350.0, 355.0],
        correct=[True] * 8,
        condition=["congruent"] * 4 + ["incongruent"] * 4,
    )
    # flanker effect: mean([320..335]) - mean([270..285]) = 327.5 - 277.5 = +50 ms
    flanker = TaskResult(
        rt_ms=[270.0, 275.0, 280.0, 285.0, 320.0, 325.0, 330.0, 335.0],
        correct=[True] * 8,
        condition=["congruent"] * 4 + ["incongruent"] * 4,
    )
    # 2 go hits, 1 correct rejection, 1 false alarm
    gonogo = TaskResult(
        rt_ms=[300.0, 0.0, 310.0, 0.0],
        correct=[True, True, True, False],
        condition=["go", "nogo", "go", "nogo"],
    )
    rt = TaskResult(
        rt_ms=[250.0, 300.0, 280.0, 320.0, 0.0],
        correct=[True, True, True, True, False],
        condition=["simple"] * 5,
    )
    return DashboardSession(rt=rt, stroop=stroop, flanker=flanker, gonogo=gonogo)


# ── cognitive_profile() — content requirements ────────────────────────────


def test_no_forbidden_patterns_in_profile(session: DashboardSession) -> None:
    text = " ".join(cognitive_profile(session)).lower()
    for pattern in _FORBIDDEN:
        assert pattern not in text, f"Forbidden diagnostic pattern in profile: {pattern!r}"


def test_profile_contains_reaction_time_ms_value(session: DashboardSession) -> None:
    text = " ".join(cognitive_profile(session))
    # mean of valid RT trials: (250+300+280+320)/4 = 287.5 ms
    assert re.search(r"28[0-9]|29[0-9]", text), "RT mean (ms) not found in profile output"


def test_profile_shows_stroop_effect_in_ms(session: DashboardSession) -> None:
    text = " ".join(cognitive_profile(session))
    # Stroop effect: mean(incong) - mean(cong) = 347.5 - 287.5 = 60 ms
    assert "60" in text or "+60" in text, "Stroop effect value (ms) not found in profile output"


def test_profile_shows_false_alarm_count(session: DashboardSession) -> None:
    text = " ".join(cognitive_profile(session)).lower()
    # 1 false alarm out of 2 no-go trials
    assert "1" in text, "False alarm count not found in profile output"
    assert "no-go" in text or "nogo" in text, "No-go condition label not found in profile output"


def test_profile_shows_trial_count(session: DashboardSession) -> None:
    text = " ".join(cognitive_profile(session))
    # Should mention some trial count (n=X or "X prób")
    assert re.search(r"n=\d+|\d+\s*prób", text), "Trial count not found in profile output"


def test_profile_does_not_hardcode_8_trials(session: DashboardSession) -> None:
    """The old disclaimer 'to tylko 8 prób' hardcoded a fixed count."""
    text = " ".join(cognitive_profile(session))
    assert "tylko 8 prób" not in text, "Hardcoded '8 prób' disclaimer still present"


# ── _hypothetical_profile() — same requirements ───────────────────────────


def test_no_forbidden_patterns_in_hypothetical_profile() -> None:
    lines = CognitiveDashboardScene._hypothetical_profile(60.0, 40.0, 1)
    text = " ".join(lines).lower()
    for pattern in _FORBIDDEN:
        assert pattern not in text, (
            f"Forbidden diagnostic pattern in hypothetical profile: {pattern!r}"
        )


def test_hypothetical_profile_shows_stroop_value() -> None:
    lines = CognitiveDashboardScene._hypothetical_profile(60.0, 40.0, 1)
    text = " ".join(lines)
    assert "60" in text, "Stroop effect value not shown in hypothetical profile"


def test_hypothetical_profile_shows_flanker_value() -> None:
    lines = CognitiveDashboardScene._hypothetical_profile(60.0, 40.0, 1)
    text = " ".join(lines)
    assert "40" in text, "Flanker effect value not shown in hypothetical profile"


def test_hypothetical_profile_shows_fa_count() -> None:
    lines = CognitiveDashboardScene._hypothetical_profile(60.0, 40.0, 2)
    text = " ".join(lines)
    assert "2" in text, "False alarm count not shown in hypothetical profile"
