# src/cognitive_data_arcade/games/architects_trial/game_state.py
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class DecisionCard:
    key: str
    label: str
    description: str
    note: str
    note_color: str          # "green" | "orange" | "red"
    fairness_delta: int
    compliance_delta: int
    effectiveness_delta: int


@dataclass
class GameState:
    domain: str = ""
    decisions: list[str] = field(default_factory=list)
    fairness_score: int = 0
    compliance_score: int = 0
    effectiveness_score: int = 0
    tribunal_response: str = ""


def compute_verdict(fairness: int, compliance: int, effectiveness: int) -> str:
    if fairness <= 20 or compliance <= 20:
        return "ODRZUCONY"
    if fairness <= 30 or compliance <= 30 or effectiveness <= 30:
        return "ZAWIESZONY"
    if fairness >= 60 and compliance >= 60 and effectiveness >= 60:
        return "ZATWIERDZONY"
    return "ZATWIERDZONY Z ZALECENIAMI"
