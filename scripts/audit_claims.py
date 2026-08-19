#!/usr/bin/env python3
"""Educational claim audit — flags risky wording for manual review.

This is a human-review aid, not an automated fact-checker.
False positives are expected and acceptable; a human must decide whether
each finding is genuinely problematic in context.

Usage:
    uv run python scripts/audit_claims.py [--strict] [paths ...]

Without --strict (default): prints findings, exits 0.  Safe for CI.
With --strict: exits 1 when any findings exist.  Suitable for pre-commit.

If no paths are given, scans:
  - lessons/   (Markdown theory, tasks, notes)
  - src/cognitive_data_arcade/lessons/   (Python lesson content modules)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Rule:
    """One flagging rule."""

    name: str
    pattern: str
    note: str


RULES: list[Rule] = [
    # ---------- normative / threshold language ----------
    Rule(
        name="NORMATIVE",
        pattern=(
            r"is\s+normal\b"
            r"|within\s+(the\s+)?(5|10|15|20|25|30)[\-–]\d+\s*%\s*norm"
            r"|\bnormal\s+range\b"
            r"|\bnorma\b"  # Polish
            r"|\bw\s+normie\b"  # Polish "within the norm"
            r"|\bto\s+norma\b"  # Polish "X to norma"
            r"|mieści\s+się\s+w\s+norm"  # Polish
        ),
        note=(
            "Verify this threshold/range is explicitly qualified as task- and "
            "population-specific, not a universal diagnostic norm."
        ),
    ),
    # ---------- absolute claims ----------
    Rule(
        name="ABSOLUTE",
        pattern=r"\b(always|never|zawsze|nigdy)\b",
        note=(
            "Check whether this absolute claim is genuinely unconditional or "
            "should be qualified with a scope/context."
        ),
    ),
    # ---------- gold standard ----------
    Rule(
        name="GOLD_STANDARD",
        pattern=r"\b(gold\s+standard|złoty\s+standard)\b",
        note=(
            "'Gold standard' requires a matching source, protocol, and population. "
            "Prefer describing the actual evidence base."
        ),
    ),
    # ---------- diagnostic / clinical label ----------
    Rule(
        name="DIAGNOSIS",
        pattern=(
            r"\bdiagnos(is|e[sd]?|ing)\b"
            r"|\brozpoznanie\s+kliniczne\b"  # Polish "clinical diagnosis"
            r"|\bdiagnozuje\b"  # Polish "diagnoses"
        ),
        note=(
            "Task performance should not be presented as clinical diagnosis. "
            "Prefer 'associated with', 'studied in', or 'used to assess' language."
        ),
    ),
    # ---------- method-dominance / state-of-the-art ----------
    Rule(
        name="DOMINANCE",
        pattern=(
            r"\b(dominates?\s+modern"
            r"|state[\s\-]of[\s\-]the[\s\-]art"
            r"|always\s+better"
            r"|universally\s+superior"
            r"|najlepszy\s+ze\s+wszystkich)\b"
        ),
        note=(
            "Method-dominance claims require time, context, and reference. "
            "Prefer describing scope and conditions."
        ),
    ),
    # ---------- trait/personality conclusions from task performance ----------
    Rule(
        name="TRAIT_CONCLUSION",
        pattern=(
            r"\b(indicates?\s+impulsiv"
            r"|you\s+are\s+impulsiv"
            r"|potwierdza\s+impulsywn"
            r"|oznacza\s+(że\s+jesteś\s+)?impulsywn"
            r"|potwierdza\s+cechę)\b"
        ),
        note=(
            "A task session error rate indexes situational inhibitory performance, "
            "not a stable personality trait. Verify the phrasing preserves this distinction."
        ),
    ),
    # ---------- physiologically impossible ----------
    Rule(
        name="PHYSIOLOGICAL",
        pattern=r"\bphysiologically\s+impossible\b",
        note=(
            "Physiological impossibility claims require a precise biological source. "
            "Prefer 'implausibly fast for genuine stimulus processing'."
        ),
    ),
    # ---------- percentage presented as a norm ----------
    Rule(
        name="PERCENTAGE_NORM",
        pattern=(
            r"\d+\s*%\s+(is\s+(normal|the\s+norm|diagnostic)"
            r"|wynosi\s+normę"
            r"|to\s+norma)"
        ),
        note=(
            "A percentage stated as 'normal' needs its source, task protocol, "
            "and population scope made explicit."
        ),
    ),
    # ---------- RT threshold presented as physiological law ----------
    Rule(
        name="RT_THRESHOLD",
        pattern=(
            r"\b(1[56789]\d|[2-9]\d{2})\s*ms\s+(is\s+(too\s+)?(fast|slow)|to\s+(za\s+)?(szybko|wolno))\b"
            r"|\bponiżej\s+\d+\s*ms\s+niemożliw"  # Polish "below X ms impossible"
            r"|\bbelow\s+\d+\s*ms\s+(is\s+)?impossible"
        ),
        note=(
            "RT cutoffs are analytic conventions, not physiological laws. "
            "Prefer 'implausible for genuine stimulus processing in this task'."
        ),
    ),
]

_COMPILED: list[tuple[Rule, re.Pattern[str]]] = [
    (rule, re.compile(rule.pattern, re.IGNORECASE)) for rule in RULES
]


# ---------------------------------------------------------------------------
# Finding
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    path: Path
    line_num: int
    line: str
    rule: Rule

    def format(self, root: Path) -> str:
        try:
            rel = self.path.relative_to(root)
        except ValueError:
            rel = self.path
        snippet = self.line.strip()[:120]
        return f"{rel}:{self.line_num}: [{self.rule.name}]\n  {snippet}\n  → {self.rule.note}"


# ---------------------------------------------------------------------------
# File selection
# ---------------------------------------------------------------------------


def _is_lesson_py(path: Path) -> bool:
    return (
        path.suffix == ".py" and path.parent.name == "lessons" and path.stem.startswith("lesson_")
    )


def _is_lesson_md(path: Path) -> bool:
    return path.suffix == ".md" and path.stat().st_size > 0


def _should_scan(path: Path) -> bool:
    return _is_lesson_py(path) or _is_lesson_md(path)


def collect_paths(roots: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for root in roots:
        if root.is_file():
            if _should_scan(root):
                paths.append(root)
        elif root.is_dir():
            for child in sorted(root.rglob("*")):
                if child.is_file() and _should_scan(child):
                    paths.append(child)
    return sorted(set(paths))


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------


def scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return findings

    for line_num, line in enumerate(text.splitlines(), start=1):
        # Skip comment lines in Python (they describe structure, not student-facing content)
        stripped = line.lstrip()
        if _is_lesson_py(path) and stripped.startswith("#"):
            continue
        for rule, compiled in _COMPILED:
            if compiled.search(line):
                findings.append(Finding(path=path, line_num=line_num, line=line, rule=rule))
    return findings


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any findings exist (default: always exit 0).",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Files or directories to scan (default: lessons/ and src/.../lessons/).",
    )
    args = parser.parse_args(argv)

    scan_roots: list[Path] = args.paths or [
        ROOT / "lessons",
        ROOT / "src" / "cognitive_data_arcade" / "lessons",
    ]

    paths = collect_paths(scan_roots)
    all_findings: list[Finding] = []
    for path in paths:
        all_findings.extend(scan_file(path))

    if not all_findings:
        print("audit_claims: no findings.")
        return 0

    print(f"audit_claims: {len(all_findings)} finding(s) — manual review required.\n")
    for finding in all_findings:
        print(finding.format(ROOT))
        print()

    if args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
