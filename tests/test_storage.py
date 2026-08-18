import csv
from dataclasses import dataclass
from pathlib import Path

import pytest

from cognitive_data_arcade.engine.storage import CSVLogger, TrialResult, write_trial


def _trial(**kwargs) -> TrialResult:
    defaults = dict(
        participant_id="p01",
        session_id="s01",
        trial_id=1,
        task_name="reaction_time",
        condition="simple",
        stimulus="circle",
        expected_response="space",
        actual_response="space",
        correct=True,
        reaction_time_ms=312.5,
        timestamp="2026-05-17T10:00:00",
    )
    return TrialResult(**{**defaults, **kwargs})


def test_log_creates_csv_with_correct_headers(tmp_path: Path) -> None:
    logger = CSVLogger(tmp_path)
    logger.log_trial(_trial())

    csv_file = tmp_path / "reaction_time" / "s01.csv"
    assert csv_file.exists()
    with csv_file.open() as f:
        headers = csv.DictReader(f).fieldnames
    assert headers == [
        "participant_id",
        "session_id",
        "trial_id",
        "task_name",
        "condition",
        "stimulus",
        "expected_response",
        "actual_response",
        "correct",
        "reaction_time_ms",
        "timestamp",
    ]


def test_log_appends_multiple_trials(tmp_path: Path) -> None:
    logger = CSVLogger(tmp_path)
    for i in range(1, 4):
        logger.log_trial(_trial(trial_id=i))

    csv_file = tmp_path / "reaction_time" / "s01.csv"
    with csv_file.open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 3
    assert [int(r["trial_id"]) for r in rows] == [1, 2, 3]


def test_log_separates_tasks_into_subdirectories(tmp_path: Path) -> None:
    logger = CSVLogger(tmp_path)
    logger.log_trial(_trial(task_name="reaction_time"))
    logger.log_trial(_trial(task_name="stroop"))

    assert (tmp_path / "reaction_time" / "s01.csv").exists()
    assert (tmp_path / "stroop" / "s01.csv").exists()


def test_log_separates_sessions(tmp_path: Path) -> None:
    logger = CSVLogger(tmp_path)
    logger.log_trial(_trial(session_id="s01"))
    logger.log_trial(_trial(session_id="s02"))

    assert (tmp_path / "reaction_time" / "s01.csv").exists()
    assert (tmp_path / "reaction_time" / "s02.csv").exists()


# ── write_trial: standalone function ─────────────────────────────────────────


@dataclass(frozen=True)
class _CustomRecord:
    participant_id: str
    task_name: str
    extra_field: int


def test_write_trial_creates_file_and_header(tmp_path: Path) -> None:
    path = tmp_path / "task" / "s01.csv"
    rec = _CustomRecord(participant_id="p1", task_name="custom", extra_field=42)
    write_trial(path, rec)

    assert path.exists()
    with path.open() as f:
        rows = list(csv.DictReader(f))
    assert rows == [{"participant_id": "p1", "task_name": "custom", "extra_field": "42"}]


def test_write_trial_appends_without_duplicate_header(tmp_path: Path) -> None:
    path = tmp_path / "task" / "s01.csv"
    rec = _CustomRecord(participant_id="p1", task_name="custom", extra_field=1)
    write_trial(path, rec)
    write_trial(path, _CustomRecord(participant_id="p1", task_name="custom", extra_field=2))

    with path.open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert rows[0]["extra_field"] == "1"
    assert rows[1]["extra_field"] == "2"


def test_write_trial_creates_parent_dirs(tmp_path: Path) -> None:
    path = tmp_path / "deep" / "nested" / "dir" / "file.csv"
    write_trial(path, _CustomRecord(participant_id="p1", task_name="t", extra_field=0))
    assert path.exists()


# ── CSV schema compatibility: all 6 game _TrialRecord schemas ─────────────────
# These tests verify that the schemas written by write_trial remain readable
# and contain the expected canonical columns.

_CANONICAL_COLS = {
    "participant_id",
    "session_id",
    "trial_id",
    "task_name",
    "correct",
    "reaction_time_ms",
    "timestamp",
}

# N-back uses a fundamentally different dual-response schema:
# pos_correct/let_correct instead of correct, rt_a_ms/rt_l_ms instead of
# reaction_time_ms, and no timestamp column.  This is intentional.
_NBACK_EXPECTED_COLS = {
    "participant_id",
    "session_id",
    "trial_id",
    "task_name",
    "pos_correct",
    "let_correct",
    "rt_a_ms",
    "rt_l_ms",
}

# Visual search uses rt_ms (not reaction_time_ms) and mode (not task_name).
_VISUAL_SEARCH_EXPECTED_COLS = {
    "participant_id",
    "session_id",
    "trial_id",
    "correct",
    "rt_ms",
    "timestamp",
}


@pytest.mark.parametrize(
    "game_module, game_class, extra_kwargs",
    [
        (
            "cognitive_data_arcade.games.reaction_time.game",
            "ReactionTimeGame",
            None,
        ),
        (
            "cognitive_data_arcade.games.stroop.game",
            "StroopGame",
            None,
        ),
        (
            "cognitive_data_arcade.games.flanker.game",
            "FlankerGame",
            None,
        ),
        (
            "cognitive_data_arcade.games.gono.game",
            "GoNoGoGame",
            None,
        ),
        (
            "cognitive_data_arcade.games.nback.game",
            "NBackGame",
            None,
        ),
        (
            "cognitive_data_arcade.games.visual_search.game",
            "VisualSearchGame",
            None,
        ),
    ],
    ids=["reaction_time", "stroop", "flanker", "gono", "nback", "visual_search"],
)
def test_game_csv_contains_canonical_columns(
    tmp_path: Path, game_module: str, game_class: str, extra_kwargs
) -> None:
    """Each game writes a CSV; the file must contain the canonical core columns.

    We do not instantiate the game (too many Pygame dependencies) — instead we
    directly exercise write_trial with each game's _TrialRecord to verify the
    schema is stable and canonical columns are present.
    """
    import importlib

    mod = importlib.import_module(game_module)
    record_cls = mod._TrialRecord  # type: ignore[attr-defined]
    fields = list(record_cls.__dataclass_fields__.keys())

    # Confirm write_trial can handle this record schema without error
    path = tmp_path / f"{game_class}.csv"
    defaults = {f: 0 for f in fields}
    for f in fields:
        ann = record_cls.__dataclass_fields__[f].type
        if ann in (str, "str"):
            defaults[f] = "x"
        elif ann in (bool, "bool"):
            defaults[f] = False
        elif ann in (float, "float"):
            defaults[f] = 0.0
        elif ann in (int, "int"):
            defaults[f] = 0
        else:
            defaults[f] = None  # list / complex types — skip write check
    if any(v is None for v in defaults.values()):
        pytest.skip(f"{game_class} has non-primitive field types — schema inspection only")

    rec = record_cls(**defaults)
    write_trial(path, rec)

    with path.open() as f:
        headers = set(csv.DictReader(f).fieldnames or [])

    # Some games use purposefully different schemas; check their own expected cols.
    if game_class == "NBackGame":
        missing = _NBACK_EXPECTED_COLS - headers
    elif game_class == "VisualSearchGame":
        missing = _VISUAL_SEARCH_EXPECTED_COLS - headers
    else:
        missing = (
            _CANONICAL_COLS
            - headers
            - {"condition", "stimulus", "expected_response", "actual_response"}
        )
    assert not missing, f"{game_class} CSV missing columns: {missing}"
