"""Tests for provenance metadata in lesson modules."""

from __future__ import annotations

import importlib

import pytest

from cognitive_data_arcade.lessons.provenance import Claim, VALID_TYPES


# Lessons that must have PROVENANCE defined
REQUIRED_LESSON_NUMS = [7, 9, 10, 31]


def _load_provenance(lesson_num: int) -> dict[str, Claim] | None:
    mod = importlib.import_module(f"cognitive_data_arcade.lessons.lesson_{lesson_num:02d}")
    return getattr(mod, "PROVENANCE", None)


@pytest.mark.parametrize("lesson_num", REQUIRED_LESSON_NUMS)
def test_provenance_exists(lesson_num: int) -> None:
    prov = _load_provenance(lesson_num)
    assert prov is not None, f"lesson_{lesson_num:02d}.py is missing PROVENANCE"
    assert len(prov) > 0, f"lesson_{lesson_num:02d}.PROVENANCE is empty"


@pytest.mark.parametrize("lesson_num", REQUIRED_LESSON_NUMS)
def test_provenance_format(lesson_num: int) -> None:
    prov = _load_provenance(lesson_num)
    assert prov is not None
    for key, claim in prov.items():
        assert isinstance(claim, Claim), (
            f"lesson_{lesson_num:02d}: '{key}' must be a Claim instance, got {type(claim)}"
        )
        assert claim.type in VALID_TYPES, (
            f"lesson_{lesson_num:02d}: '{key}' has invalid type {claim.type!r}"
        )
        assert claim.note.strip(), f"lesson_{lesson_num:02d}: '{key}' has empty note"


def test_all_lessons_provenance_valid() -> None:
    """Any lesson that declares PROVENANCE must conform to the schema."""
    for lesson_num in range(1, 33):
        try:
            mod = importlib.import_module(f"cognitive_data_arcade.lessons.lesson_{lesson_num:02d}")
        except ImportError:
            continue
        prov = getattr(mod, "PROVENANCE", None)
        if prov is None:
            continue
        assert isinstance(prov, dict), f"lesson_{lesson_num:02d}.PROVENANCE must be a dict"
        for key, claim in prov.items():
            assert isinstance(claim, Claim), (
                f"lesson_{lesson_num:02d}: '{key}' must be a Claim instance"
            )
            assert claim.type in VALID_TYPES, (
                f"lesson_{lesson_num:02d}: '{key}' invalid type {claim.type!r}"
            )
            assert claim.note.strip(), f"lesson_{lesson_num:02d}: '{key}' has empty note"


def test_claim_rejects_invalid_type() -> None:
    with pytest.raises(ValueError, match="Invalid claim type"):
        Claim(type="made_up", note="some note")  # type: ignore[arg-type]


def test_claim_rejects_empty_note() -> None:
    with pytest.raises(ValueError, match="note must not be empty"):
        Claim(type="heuristic", note="")
