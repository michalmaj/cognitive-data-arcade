"""Lightweight provenance metadata for educational claims in lesson modules.

Each lesson module may optionally expose a PROVENANCE dict mapping a
claim key to a Claim instance.  The lesson reader ignores this dict;
it is used only for auditing and automated testing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ClaimType = Literal["empirical", "simulation", "heuristic", "reference_range"]

VALID_TYPES: frozenset[str] = frozenset({"empirical", "simulation", "heuristic", "reference_range"})


@dataclass(frozen=True)
class Claim:
    """Metadata for a notable educational claim.

    Attributes:
        type:    Nature of the claim — see ClaimType for valid values.
        note:    Plain-English caveat or context (mandatory, non-empty).
        source:  Citation or reference string, if applicable.
        updated: ISO date (YYYY-MM-DD) when this entry was last reviewed.
    """

    type: ClaimType
    note: str
    source: str = field(default="")
    updated: str = field(default="")

    def __post_init__(self) -> None:
        if self.type not in VALID_TYPES:
            raise ValueError(f"Invalid claim type: {self.type!r}")
        if not self.note:
            raise ValueError("Claim.note must not be empty")
