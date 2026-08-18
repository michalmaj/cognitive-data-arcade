from __future__ import annotations
import csv
import statistics
from pathlib import Path

from cognitive_data_arcade.games.you_were_the_dataset.game_state import ProfileData

REQUIRED_GAMES: dict[str, str] = {
    "reaction_time": "L02 Reaction Time Lab",
    "stroop": "L07 Stroop Challenge",
    "flanker": "L08 Flanker Arena",
    "gono": "L09 Go/No-Go Guard",
    "nback": "L10 N-Back Memory Grid",
}

# Hard-coded reference RTs (ms) for percentile computation.
# Derived from approximate population norms for simple RT.
_RT_REFERENCE = [155, 175, 190, 205, 220, 235, 250, 270, 295, 330, 380, 450, 560]


def check_prerequisites(data_dir: Path) -> dict[str, bool]:
    """Return {task_name: has_data} for each required game."""
    return {name: any((data_dir / name).glob("*.csv")) for name in REQUIRED_GAMES}


def _latest_csv(task_dir: Path) -> Path:
    return sorted(task_dir.glob("*.csv"))[-1]


def _read_rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _rt_percentile(rt_ms: float) -> int:
    """Return 0-100 percentile vs _RT_REFERENCE (higher = faster)."""
    below = sum(1 for r in _RT_REFERENCE if r > rt_ms)
    return int(below / len(_RT_REFERENCE) * 100)


def load_profile(data_dir: Path) -> ProfileData:
    """Read most recent CSV per game, compute 5 cognitive metrics."""
    # Reaction time baseline
    rt_rows = _read_rows(_latest_csv(data_dir / "reaction_time"))
    rt_times = [
        float(r["reaction_time_ms"])
        for r in rt_rows
        if r.get("correct") == "True" and float(r.get("reaction_time_ms", 0)) > 0
    ]
    rt_median = statistics.median(rt_times) if rt_times else 250.0

    # Stroop effect = median_incongruent - median_congruent
    stroop_rows = _read_rows(_latest_csv(data_dir / "stroop"))
    s_cong = [
        float(r["reaction_time_ms"])
        for r in stroop_rows
        if r.get("condition") == "congruent" and r.get("correct") == "True"
    ]
    s_incong = [
        float(r["reaction_time_ms"])
        for r in stroop_rows
        if r.get("condition") == "incongruent" and r.get("correct") == "True"
    ]
    stroop_effect = (
        (statistics.median(s_incong) - statistics.median(s_cong)) if s_cong and s_incong else 0.0
    )

    # Flanker effect = median_incongruent - median_congruent
    flanker_rows = _read_rows(_latest_csv(data_dir / "flanker"))
    f_cong = [
        float(r["reaction_time_ms"])
        for r in flanker_rows
        if r.get("condition") == "congruent" and r.get("correct") == "True"
    ]
    f_incong = [
        float(r["reaction_time_ms"])
        for r in flanker_rows
        if r.get("condition") == "incongruent" and r.get("correct") == "True"
    ]
    flanker_effect = (
        (statistics.median(f_incong) - statistics.median(f_cong)) if f_cong and f_incong else 0.0
    )

    # Go/No-Go false alarm rate
    gono_rows = _read_rows(_latest_csv(data_dir / "gono"))
    nogo_trials = [r for r in gono_rows if r.get("trial_type") == "nogo"]
    fa_count = sum(1 for r in nogo_trials if r.get("response") == "false_alarm")
    gono_fa_rate = fa_count / len(nogo_trials) if nogo_trials else 0.0

    # N-Back: max n_level where combined accuracy >= 70%
    nback_rows = _read_rows(_latest_csv(data_dir / "nback"))
    levels: dict[int, list[tuple[bool, bool]]] = {}
    for r in nback_rows:
        lvl = int(r.get("n_level", 1))
        pc = r.get("pos_correct", "False") == "True"
        lc = r.get("let_correct", "False") == "True"
        levels.setdefault(lvl, []).append((pc, lc))
    best_n = 1
    for lvl, trials in sorted(levels.items()):
        correct = sum(pc + lc for pc, lc in trials)
        total = 2 * len(trials)
        if total > 0 and correct / total >= 0.70:
            best_n = max(best_n, lvl)

    return ProfileData(
        rt_median_ms=rt_median,
        stroop_effect_ms=stroop_effect,
        flanker_effect_ms=flanker_effect,
        gono_false_alarm_rate=gono_fa_rate,
        nback_max_level=best_n,
        rt_percentile=_rt_percentile(rt_median),
    )
