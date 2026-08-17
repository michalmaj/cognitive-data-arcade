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

---

## Commit conventions

### Prefixes

Use one of these conventional prefixes on every commit:

```
test:      add or update tests
fix:       correct a bug
feat:      add new behavior
refactor:  restructure without intended behavior change
content:   change educational text or lesson copy
docs:      update documentation
tooling:   add or update a developer tool or script
build:     change build or packaging configuration
ci:        change CI/CD configuration
typing:    add or improve type annotations
style:     formatting only (usually from ruff)
chore:     maintenance (gitignore, version bump, etc.)
release:   release preparation
```

### Granularity

Aim for **4–10 meaningful commits per normal PR**. Each commit should be:

- understandable on its own,
- reviewable in isolation,
- reversible with `git revert`,
- usable by `git bisect`.

For behavioral changes, prefer this sequence:

```
test:     reproduce or capture current behavior
refactor: prepare structure without intended behavior change
fix/feat: implement the behavior
test:     cover edge cases and regression
docs:     synchronize documentation
```

### What to avoid

```
fix stuff
oops
fix typo
actually fix
more cleanup
```

Do not squash a well-structured test/refactor/fix/docs sequence into one giant commit.

### PR scope

One PR should solve **one coherent problem**. Examples of good scope:

- consolidate launch paths,
- centralize application paths,
- correct dashboard interpretation language,
- audit a set of related lessons.

Do not combine architectural refactors, lesson rewrites, and UI fixes in one PR.
