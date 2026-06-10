from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TaskResult:
    rt_ms: list[float]
    correct: list[bool]
    condition: list[str]

    def __post_init__(self) -> None:
        n = len(self.rt_ms)
        if len(self.correct) != n or len(self.condition) != n:
            raise ValueError(
                f"TaskResult lists must all have the same length: "
                f"rt_ms={n}, correct={len(self.correct)}, condition={len(self.condition)}"
            )


@dataclass
class DashboardSession:
    rt:      TaskResult | None = None
    stroop:  TaskResult | None = None
    flanker: TaskResult | None = None
    gonogo:  TaskResult | None = None
    synthetic: bool = False

    def is_complete(self) -> bool:
        return all(x is not None for x in (self.rt, self.stroop, self.flanker, self.gonogo))
