from __future__ import annotations

import random
from typing import List

import pygame
import pytest

from cognitive_data_arcade.games.visual_search.stimuli import (
    Item,
    generate_items,
    draw_item,
    GRID_PARAMS,
)


@pytest.fixture(autouse=True)
def pg() -> None:
    pygame.init()
    yield
    pygame.quit()


def _rng() -> random.Random:
    return random.Random(42)


def test_grid_params_set_sizes() -> None:
    assert set(GRID_PARAMS.keys()) == {8, 16, 24}


def test_generate_items_correct_count() -> None:
    for set_size in (8, 16, 24):
        items = generate_items("letters", "feature", True, set_size, _rng())
        assert len(items) == set_size, f"set_size={set_size}: got {len(items)}"


def test_generate_items_one_target_when_present() -> None:
    items = generate_items("letters", "feature", True, 8, _rng())
    targets = [i for i in items if i.is_target]
    assert len(targets) == 1


def test_generate_items_no_target_when_absent() -> None:
    items = generate_items("letters", "feature", False, 8, _rng())
    targets = [i for i in items if i.is_target]
    assert len(targets) == 0


def test_letters_feature_target_is_X() -> None:
    items = generate_items("letters", "feature", True, 8, _rng())
    target = next(i for i in items if i.is_target)
    assert target.kind == "X"


def test_letters_feature_distractors_are_O() -> None:
    items = generate_items("letters", "feature", True, 8, _rng())
    distractors = [i for i in items if not i.is_target]
    assert all(i.kind == "O" for i in distractors)


def test_letters_conjunction_target_is_T() -> None:
    items = generate_items("letters", "conjunction", True, 8, _rng())
    target = next(i for i in items if i.is_target)
    assert target.kind == "T"


def test_letters_conjunction_distractors_are_L() -> None:
    items = generate_items("letters", "conjunction", True, 8, _rng())
    distractors = [i for i in items if not i.is_target]
    assert all(i.kind == "L" for i in distractors)


def test_shapes_feature_target_is_orange_circle() -> None:
    items = generate_items("shapes", "feature", True, 8, _rng())
    target = next(i for i in items if i.is_target)
    assert target.kind == "circle_orange"


def test_shapes_feature_distractors_are_blue_circles() -> None:
    items = generate_items("shapes", "feature", True, 8, _rng())
    distractors = [i for i in items if not i.is_target]
    assert all(i.kind == "circle_blue" for i in distractors)


def test_shapes_conjunction_distractors_mixed() -> None:
    items = generate_items("shapes", "conjunction", True, 16, _rng())
    distractors = [i for i in items if not i.is_target]
    kinds = {i.kind for i in distractors}
    assert "circle_blue" in kinds
    assert "square_orange" in kinds


def test_no_item_overlap() -> None:
    items = generate_items("letters", "feature", True, 24, _rng())
    for i, a in enumerate(items):
        for b in items[i + 1:]:
            dist = ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5
            assert dist > 30, f"Items overlap: {a} vs {b}"


def test_draw_item_no_crash() -> None:
    surface = pygame.Surface((1024, 768))
    font = pygame.font.SysFont(None, 40)
    items = generate_items("letters", "feature", True, 8, _rng())
    for item in items:
        draw_item(surface, item, font)
    items_s = generate_items("shapes", "conjunction", True, 8, _rng())
    for item in items_s:
        draw_item(surface, item, font)
