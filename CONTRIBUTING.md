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
