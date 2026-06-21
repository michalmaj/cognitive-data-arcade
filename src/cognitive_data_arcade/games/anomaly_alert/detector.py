from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Element:
    x_px: float  # pixel x in the rendered chart surface (pygame coords)
    y_px: float  # pixel y in the rendered chart surface (pygame coords)
    w_px: float  # 0 for point elements; > 0 for rectangular elements
    h_px: float  # 0 for point elements; > 0 for rectangular elements
    is_anomaly: bool
    label: str


def compute_round_score(found: int, false_alarms: int, time_bonus: int) -> int:
    return max(0, found * 20 - false_alarms * 5 + time_bonus)


def find_clicked_element(elements: list[Element], click_pos: tuple[int, int]) -> int | None:
    cx, cy = click_pos
    for i, el in enumerate(elements):
        if el.w_px == 0.0 and el.h_px == 0.0:
            if math.hypot(cx - el.x_px, cy - el.y_px) < 14:
                return i
        else:
            if el.x_px <= cx <= el.x_px + el.w_px and el.y_px <= cy <= el.y_px + el.h_px:
                return i
    return None
