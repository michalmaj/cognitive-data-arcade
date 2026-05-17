import csv
from pathlib import Path

from cognitive_data_arcade.engine.storage import CSVLogger, TrialResult


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
