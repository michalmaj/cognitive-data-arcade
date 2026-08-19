"""Tests for the educational claim audit script."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from scripts.audit_claims import (  # type: ignore[import]
    RULES,
    Rule,
    collect_paths,
    main,
    scan_file,
)

# ---------------------------------------------------------------------------
# Rule fixture helpers
# ---------------------------------------------------------------------------


def _rule(name: str) -> Rule:
    match = [r for r in RULES if r.name == name]
    assert match, f"No rule named {name!r}"
    return match[0]


def _write(tmp_path: Path, filename: str, content: str) -> Path:
    p = tmp_path / filename
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Unit tests: individual rules trigger on target text
# ---------------------------------------------------------------------------


class TestRuleNormative:
    def test_is_normal_en(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "FA rate of 5-15% is normal for this task.\n")
        findings = scan_file(p)
        assert any(f.rule.name == "NORMATIVE" for f in findings)

    def test_within_norm_en(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "Does the result fall within the 5-15% norm?\n")
        findings = scan_file(p)
        assert any(f.rule.name == "NORMATIVE" for f in findings)

    def test_normal_range_en(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "Does the score fall within the normal range?\n")
        findings = scan_file(p)
        assert any(f.rule.name == "NORMATIVE" for f in findings)

    def test_norma_pl(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.pl.md", "FA rate 5-15% to norma dla dorosłych.\n")
        findings = scan_file(p)
        assert any(f.rule.name == "NORMATIVE" for f in findings)

    def test_w_normie_pl(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "tasks.pl.md", "Czy wynik mieści się w normie?\n")
        findings = scan_file(p)
        assert any(f.rule.name == "NORMATIVE" for f in findings)

    def test_normal_distribution_not_flagged(self, tmp_path: Path) -> None:
        # "normal distribution" is a statistical term, not a threshold claim
        p = _write(tmp_path, "theory.md", "Assuming a normal distribution of scores.\n")
        findings = [f for f in scan_file(p) if f.rule.name == "NORMATIVE"]
        assert not findings, "normal distribution should not be flagged as a normative threshold"


class TestRuleAbsolute:
    def test_always_en(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "You should always exclude RTs below 150 ms.\n")
        assert any(f.rule.name == "ABSOLUTE" for f in scan_file(p))

    def test_never_en(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "Never use listwise deletion when MNAR.\n")
        assert any(f.rule.name == "ABSOLUTE" for f in scan_file(p))

    def test_zawsze_pl(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.pl.md", "Zawsze raportuj wskaźnik wykluczeń.\n")
        assert any(f.rule.name == "ABSOLUTE" for f in scan_file(p))

    def test_nigdy_pl(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.pl.md", "Nigdy nie używaj implikacji przyczynowej.\n")
        assert any(f.rule.name == "ABSOLUTE" for f in scan_file(p))


class TestRuleGoldStandard:
    def test_gold_standard_en(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "Multiple imputation is the gold standard.\n")
        assert any(f.rule.name == "GOLD_STANDARD" for f in scan_file(p))

    def test_zloty_standard_pl(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.pl.md", "MICE to złoty standard imputacji.\n")
        assert any(f.rule.name == "GOLD_STANDARD" for f in scan_file(p))


class TestRuleDiagnosis:
    def test_diagnosis_en(self, tmp_path: Path) -> None:
        p = _write(
            tmp_path, "theory.md", "A high commission error rate confirms a diagnosis of ADHD.\n"
        )
        assert any(f.rule.name == "DIAGNOSIS" for f in scan_file(p))

    def test_diagnoses_verb(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "The task diagnoses executive dysfunction.\n")
        assert any(f.rule.name == "DIAGNOSIS" for f in scan_file(p))

    def test_clinical_assessment_not_flagged(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "Used in clinical assessment of ADHD.\n")
        diag = [f for f in scan_file(p) if f.rule.name == "DIAGNOSIS"]
        assert not diag


class TestRuleDominance:
    def test_state_of_the_art(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "BERT is state-of-the-art in NLP.\n")
        assert any(f.rule.name == "DOMINANCE" for f in scan_file(p))

    def test_dominates_modern(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "Deep learning dominates modern AI research.\n")
        assert any(f.rule.name == "DOMINANCE" for f in scan_file(p))

    def test_always_better(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.md", "More data is always better for training.\n")
        assert any(f.rule.name in ("DOMINANCE", "ABSOLUTE") for f in scan_file(p))


class TestRulePercentageNorm:
    def test_percent_immediately_before_is_normal(self, tmp_path: Path) -> None:
        # Pattern matches when % is immediately followed by "is normal"
        p = _write(tmp_path, "theory.md", "FA rate of 5-15% is normal for this task.\n")
        assert any(f.rule.name == "PERCENTAGE_NORM" for f in scan_file(p))

    def test_percent_with_words_before_is_normal(self, tmp_path: Path) -> None:
        # When words fall between % and "is normal", NORMATIVE catches it instead
        p = _write(tmp_path, "theory.md", "A 10% false alarm rate is normal.\n")
        assert any(f.rule.name in ("NORMATIVE", "PERCENTAGE_NORM") for f in scan_file(p))

    def test_percent_to_norma_pl(self, tmp_path: Path) -> None:
        p = _write(tmp_path, "theory.pl.md", "10% fałszywych alarmów to norma.\n")
        assert any(f.rule.name in ("PERCENTAGE_NORM", "NORMATIVE") for f in scan_file(p))


class TestRulePhysiological:
    def test_physiologically_impossible(self, tmp_path: Path) -> None:
        p = _write(
            tmp_path, "notes.md", "85 ms is physiologically impossible as a genuine reaction.\n"
        )
        assert any(f.rule.name == "PHYSIOLOGICAL" for f in scan_file(p))


# ---------------------------------------------------------------------------
# File-selection tests
# ---------------------------------------------------------------------------


class TestCollectPaths:
    def test_lesson_py_included(self, tmp_path: Path) -> None:
        lessons_dir = tmp_path / "lessons"
        lessons_dir.mkdir()
        p = lessons_dir / "lesson_07.py"
        p.write_text("x = 1\n")
        assert p in collect_paths([tmp_path])

    def test_non_lesson_py_excluded(self, tmp_path: Path) -> None:
        p = tmp_path / "conftest.py"
        p.write_text("x = 1\n")
        assert p not in collect_paths([tmp_path])

    def test_md_included(self, tmp_path: Path) -> None:
        p = tmp_path / "theory.md"
        p.write_text("# Hello\n")
        assert p in collect_paths([tmp_path])

    def test_python_comment_skipped(self, tmp_path: Path) -> None:
        lessons_dir = tmp_path / "lessons"
        lessons_dir.mkdir()
        p = lessons_dir / "lesson_01.py"
        # Comment lines in Python lesson files should not be scanned
        p.write_text("# FA rate of 5-15% is normal\n")
        findings = scan_file(p)
        assert not findings, "Python comment lines should be skipped"


# ---------------------------------------------------------------------------
# main() entry-point tests
# ---------------------------------------------------------------------------


class TestMain:
    def test_clean_file_exits_zero(self, tmp_path: Path) -> None:
        p = tmp_path / "clean.md"
        p.write_text("Working memory capacity is the ability to maintain information.\n")
        code = main([str(p)])
        assert code == 0

    def test_flagged_file_exits_zero_by_default(self, tmp_path: Path) -> None:
        p = tmp_path / "risky.md"
        p.write_text("FA rate of 5-15% is normal.\n")
        code = main([str(p)])
        assert code == 0, "Without --strict, should exit 0 even with findings"

    def test_flagged_file_exits_one_with_strict(self, tmp_path: Path) -> None:
        p = tmp_path / "risky.md"
        p.write_text("FA rate of 5-15% is normal.\n")
        code = main(["--strict", str(p)])
        assert code == 1

    def test_no_findings_message(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        p = tmp_path / "clean.md"
        p.write_text("Working memory is an active workspace.\n")
        main([str(p)])
        captured = capsys.readouterr()
        assert "no findings" in captured.out

    def test_findings_count_in_output(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        p = tmp_path / "risky.md"
        p.write_text("FA rate of 5-15% is normal.\nGold standard method.\n")
        main([str(p)])
        captured = capsys.readouterr()
        assert "finding" in captured.out

    def test_finding_format_includes_rule_name(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        p = tmp_path / "risky.md"
        p.write_text("This is the gold standard approach.\n")
        main([str(p)])
        captured = capsys.readouterr()
        assert "[GOLD_STANDARD]" in captured.out
