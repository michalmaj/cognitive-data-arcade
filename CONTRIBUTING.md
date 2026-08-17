# Contributing to Cognitive Data Arcade

## Beta goals

The current stabilization target is a beta release suitable for classroom use on **2026-10-10**.

The goal is not to maximize the amount of code changed. The goal is to make Cognitive Data Arcade:

- **stable** — no P0 crashes, navigation blockers, or data-loss bugs,
- **scientifically responsible** — no unsupported norms, no diagnostic language for short behavioural tasks,
- **pedagogically useful** — concepts are explained clearly and with appropriate uncertainty,
- **transparent about local data** — students know what is stored and how to remove it,
- **easier to maintain** — launch paths, data paths, and lesson metadata are consolidated,
- **predictable to test and package** — CI passes reliably; the packaged application launches from a clean directory.

### Explicitly deferred to post-beta

These are valid improvements that will not block the beta release:

- complete migration of all lesson content to Markdown or YAML,
- typing the entire Pygame UI layer,
- eliminating every test that touches private members,
- new games or modules,
- cosmetic refactors and visual redesigns,
- generic storage abstractions with no concrete beta benefit.

If schedule pressure occurs: cut these first, never scientific correctness or privacy clarity.

---

## Quality gates

### P0 — beta blockers

The project may not be tagged as beta while any of these remain open:

- Menu and module launch paths use one canonical game construction mechanism.
- Restarting a game creates fresh gameplay state (no stale scene reuse).
- User data paths do not depend on the current working directory.
- Local data collection is clearly disclosed to the student.
- Student can understand what is stored locally and remove gameplay data.
- Cognitive dashboard does not present short-game results as diagnoses or stable personality/cognitive traits.
- Unsupported universal "norms" and pseudo-normative thresholds are removed or properly sourced and contextualized.
- High-risk educational content has passed a scientific-content audit.
- Packaged application starts correctly and can access its assets.
- Core beta smoke flows pass.
- No known P0 crash, data-loss bug, navigation blocker, or misleading scientific claim remains.

### P1 — expected for beta

Fix before the beta tag; explicitly document if deferred:

- Educational wording has been reviewed for generated/LLM-like overconfidence.
- Important educational claims have provenance or source metadata where appropriate.
- Trial logging duplication is reduced.
- Documentation matches actual application behavior.
- Ruff configuration is stronger than in alpha.
- Core non-Pygame modules have targeted static typing.
- Major touched areas have behavior-level tests rather than only private-method tests.

### P2 — defer freely

These are listed under "explicitly deferred" above.
