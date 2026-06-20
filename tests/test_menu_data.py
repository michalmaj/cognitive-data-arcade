from __future__ import annotations
from cognitive_data_arcade.ui.menu import _LESSON_DATA, _MODULES, _VIRTUAL_ROWS


def test_lesson_data_has_31_entries():
    assert len(_LESSON_DATA) == 31


def test_lesson_data_entries_have_required_keys():
    required = {"num", "name", "type", "desc_pl", "desc_en"}
    for d in _LESSON_DATA:
        assert required <= d.keys(), f"Missing keys in {d}"


def test_lesson_data_types_are_valid():
    valid = {"arcade", "lab", "puzzle"}
    for d in _LESSON_DATA:
        assert d["type"] in valid, f"Unknown type {d['type']!r} in {d['name']}"


def test_lesson_data_desc_non_empty():
    for d in _LESSON_DATA:
        assert d["desc_pl"].strip(), f"Empty desc_pl for {d['name']}"
        assert d["desc_en"].strip(), f"Empty desc_en for {d['name']}"


def test_modules_has_6_entries():
    assert len(_MODULES) == 6


def test_modules_cover_all_lessons():
    covered = set()
    for _, _, start, count in _MODULES:
        for i in range(start, start + count):
            covered.add(i)
    assert covered == set(range(31))


def test_virtual_rows_has_37_entries():
    assert len(_VIRTUAL_ROWS) == 37  # 6 headers + 31 items


def test_virtual_rows_item_count():
    items = [r for r in _VIRTUAL_ROWS if r[0] == "item"]
    assert len(items) == 31


def test_virtual_h_is_correct():
    from cognitive_data_arcade.ui.menu import _VIRTUAL_H
    assert _VIRTUAL_H == 6 * 32 + 31 * 36  # 1308
