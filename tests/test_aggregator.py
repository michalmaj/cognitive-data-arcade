import json
from pathlib import Path

from tools.aggregate_progress import _parse_file, main


def _write_export(path: Path, **overrides) -> None:
    data = {
        "alias": "student01",
        "exported_at": "2026-10-01T10:00:00",
        "app_version": "0.9.0",
        "completed_lessons": [1, 2],
        "completed_count": 2,
        "arcade_points": 100,
        "sp_points": 50,
        "streak_days": 3,
        "last_active_date": "2026-10-01",
        "quiz_results": {"1": True},
        "quiz_accuracy_pct": 100,
        "badges": ["first"],
        "module_completion": {
            "1": {"done": 2, "total": 5},
            "2": {"done": 0, "total": 6},
            "3": {"done": 0, "total": 4},
            "4": {"done": 0, "total": 4},
            "5": {"done": 0, "total": 6},
            "6": {"done": 0, "total": 6},
        },
    }
    data.update(overrides)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_parse_valid_file(tmp_path):
    p = tmp_path / "s1.json"
    _write_export(p)
    row = _parse_file(p)
    assert row is not None
    assert row["alias"] == "student01"
    assert row["badges"] == "first"
    assert row["mod1_done"] == 2
    assert row["mod2_done"] == 0


def test_parse_malformed_file(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("not json", encoding="utf-8")
    row = _parse_file(p)
    assert row is None


def test_aggregate_multiple_files(tmp_path):
    _write_export(tmp_path / "s1.json", alias="alice")
    _write_export(tmp_path / "s2.json", alias="bob")
    out = tmp_path / "out.csv"
    main([str(tmp_path), "-o", str(out)])
    content = out.read_text(encoding="utf-8")
    assert "alice" in content
    assert "bob" in content


def test_aggregate_skips_malformed(tmp_path):
    _write_export(tmp_path / "s1.json", alias="alice")
    (tmp_path / "broken.json").write_text("bad", encoding="utf-8")
    out = tmp_path / "out.csv"
    main([str(tmp_path), "-o", str(out)])
    content = out.read_text(encoding="utf-8")
    assert "alice" in content
