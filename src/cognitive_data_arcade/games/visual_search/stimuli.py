from __future__ import annotations

import random
from dataclasses import dataclass

import pygame

_LETTER_SIZE = 38
_SHAPE_RADIUS = 18
_JITTER = 8

# (cols, rows, spacing_px)
GRID_PARAMS: dict[int, tuple[int, int, int]] = {
    8:  (4, 2, 90),
    16: (4, 4, 80),
    24: (6, 4, 75),
}

_COLOR_ORANGE = (230, 126, 34)
_COLOR_BLUE   = (52, 152, 219)
_COLOR_LETTER = (230, 230, 230)

_TARGET_KIND: dict[tuple[str, str], str] = {
    ("letters", "feature"):     "X",
    ("letters", "conjunction"): "T",
    ("shapes",  "feature"):     "circle_orange",
    ("shapes",  "conjunction"): "circle_orange",
}
_DISTRACTOR_POOL: dict[tuple[str, str], list[str]] = {
    ("letters", "feature"):     ["O"],
    ("letters", "conjunction"): ["L"],
    ("shapes",  "feature"):     ["circle_blue"],
    ("shapes",  "conjunction"): ["circle_blue", "square_orange"],
}


@dataclass
class Item:
    x: float
    y: float
    is_target: bool
    kind: str  # "X","O","T","L" | "circle_orange","circle_blue","square_orange"


def _grid_positions(
    set_size: int, screen_w: int, screen_h: int, rng: random.Random
) -> list[tuple[float, float]]:
    if set_size not in GRID_PARAMS:
        raise ValueError(f"Unsupported set_size {set_size!r}; valid: {sorted(GRID_PARAMS)}")
    cols, rows, spacing = GRID_PARAMS[set_size]
    total_w = (cols - 1) * spacing
    total_h = (rows - 1) * spacing
    ox = (screen_w - total_w) / 2
    oy = (screen_h - total_h) / 2
    positions: list[tuple[float, float]] = []
    for r in range(rows):
        for c in range(cols):
            x = ox + c * spacing + rng.uniform(-_JITTER, _JITTER)
            y = oy + r * spacing + rng.uniform(-_JITTER, _JITTER)
            positions.append((x, y))
    rng.shuffle(positions)
    return positions


def generate_items(
    mode: str,
    condition: str,
    target_present: bool,
    set_size: int,
    rng: random.Random,
    screen_w: int = 1024,
    screen_h: int = 768,
) -> list[Item]:
    valid_modes = {"letters", "shapes"}
    valid_conditions = {"feature", "conjunction"}
    if mode not in valid_modes:
        raise ValueError(f"mode must be one of {valid_modes}, got {mode!r}")
    if condition not in valid_conditions:
        raise ValueError(f"condition must be one of {valid_conditions}, got {condition!r}")
    key = (mode, condition)
    target_kind = _TARGET_KIND[key]
    distractor_pool = _DISTRACTOR_POOL[key]

    positions = _grid_positions(set_size, screen_w, screen_h, rng)
    items: list[Item] = []

    if target_present:
        tx, ty = positions[0]
        items.append(Item(x=tx, y=ty, is_target=True, kind=target_kind))
        distractor_positions = positions[1:]
    else:
        distractor_positions = positions

    for x, y in distractor_positions:
        kind = rng.choice(distractor_pool)
        items.append(Item(x=x, y=y, is_target=False, kind=kind))

    return items


def draw_item(
    surface: pygame.Surface,
    item: Item,
    font: pygame.font.Font,
) -> None:
    cx, cy = int(item.x), int(item.y)
    if item.kind in ("X", "O", "T", "L"):
        text = font.render(item.kind, True, _COLOR_LETTER)
        surface.blit(text, (cx - text.get_width() // 2, cy - text.get_height() // 2))
    elif item.kind == "circle_orange":
        pygame.draw.circle(surface, _COLOR_ORANGE, (cx, cy), _SHAPE_RADIUS)
    elif item.kind == "circle_blue":
        pygame.draw.circle(surface, _COLOR_BLUE, (cx, cy), _SHAPE_RADIUS)
    elif item.kind == "square_orange":
        half = _SHAPE_RADIUS
        pygame.draw.rect(surface, _COLOR_ORANGE, (cx - half, cy - half, half * 2, half * 2))
    else:
        raise ValueError(f"Unknown item kind: {item.kind!r}")
