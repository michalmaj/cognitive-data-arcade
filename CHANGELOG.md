# Changelog

All notable changes to Cognitive Data Arcade are documented here.

## [v1.0.0a] — 2026-06-29

Student-Ready Alpha — onboarding flow, profile data stats, home-prompt system, and pre-release hardening.

### Added

- **OnboardingScene** — first-launch screen (triggered when `onboarding_done == False`) collects alias and preferred language (PL/EN); TAB toggles language, ENTER or button submits, ESC-safe; profile saved and `onboarding_done` set before routing to TitleScene
- **"Moje dane / My Data" stats card** — new section in `ProfileScene` showing sessions recorded, data points logged, active days (counted from CSV files in `data/generated/`), and quiz accuracy percentage; backed by `ui/data_stats.py` (`compute_data_stats`, `compute_quiz_accuracy`) using stdlib `csv` only
- **LogoutConfirmScene** — reached via "Wyloguj / Log out" link in ProfileScene; ENTER deletes profile JSON + generated data and routes to OnboardingScene; ESC returns to a fresh ProfileScene (avoids stale scene routing)
- **HOME_PROMPTS** — `data/home_prompts.py` contains bilingual (PL/EN) per-module study prompts (6 modules) grounded in real game names (RT Lab, N-Back, Distribution Playground, etc.)
- **"Co zrobić przed kolejnymi zajęciami?" button** — orange border button at the bottom of `ModuleCompleteScene`; opens a full-screen overlay with the module-specific HOME_PROMPT; ESC closes overlay first, then menu

### Fixed

- **`ModuleCompleteScene` unreachable** — `_refresh_and_check_complete()` was defined but never called; now called in `ModuleRunnerScene.__init__` (when no pending quiz) and in `update()` after a quiz-less lesson completes
- **Corrupted `profile.json` crash** — `ProfileManager.load()` now wraps `json.loads()` in `try/except (json.JSONDecodeError, OSError)` and recovers with a fresh profile instead of raising
- **Version string** — `pyproject.toml` corrected from `0.0.1` to `1.0.0a0`; description updated to "31 data science games"
- **ProfileScene lesson dots** — grid was capped at 30 dots; corrected to show all 31 lessons using explicit list `[1,2,3,4] + list(range(6,33))`
- **OnboardingScene game count** — tagline showed `32 gier`; corrected to `31`
- **Level title emoji rendering** — `🌱 📊 🧠 ⚡` in level strings rendered as tofu boxes in Space Grotesk TTF; emoji removed from all EN and PL `level_*` strings in `i18n.py`; `ProfileScene` avatar now shows two-letter initials (e.g. `SD` for "Siewca Danych")
- **Polish diacritics in OnboardingScene** — `"Jezyk"` → `"Język"`, `"zmien jezyk"` → `"zmień język"`, `"wysylamy"` → `"wysyłamy"`

---

## [v0.10.0] — 2026-06-28

Learning Content — post-session reflection screens for all 32 lessons and an expanded daily challenge bank.

### Added

- **Reflection scenes** — `ReflectionScene` displays 3 concept cards (label + short text) and a reflection question after completing any content lesson; triggered automatically by `SessionSummaryScene._maybe_reflection()` for all 23 task names across modules 1–6; L03 Event Log Detective exits directly to reflection on ESC
- **REFLECTION dicts** — bilingual (`pl`/`en`) content added to 19 lesson files: `lesson_01`, `lesson_03`, `lesson_04`, `lesson_06`, `lesson_13`–`lesson_32`; each dict has a title, three cards (indigo/orange/green), and a reflection question grounded in lesson content
- **Daily challenge bank** — expanded from 20 to 62 questions across 6 modules: Data Basics (dc021–dc027), Cognitive Experiments (dc028–dc034), Statistics (dc035–dc041), Machine Learning (dc042–dc048), NLP (dc049–dc055), Networks & Ethics (dc056–dc062)
- **`tests/test_reflection_scene.py`** — 6 unit tests for `ReflectionScene` (construct, draw PL/EN, ESC/mouse events, next_scene routing)
- **`tests/test_reflection_content.py`** — parametrized structural test verifying all 19 `REFLECTION` dicts have the correct shape
- **`tests/test_session_summary.py`** — routing tests confirming `SessionSummaryScene` returns `ReflectionScene` for lesson task names and `LessonMenuScene` for arcade-only task names

---

## [v0.9.0] — 2026-06-26

Distribution & Instructor Tools — standalone binaries and aggregate progress reporting.

### Added

- **Standalone executables** — Nuitka `--onefile` builds for Windows, macOS, and Linux; no Python installation required on student machines
- **GitHub Actions release workflow** — triggered on `v*` tags; matrix build across all three platforms; artifacts attached automatically to GitHub Release
- **`engine/assets.py`** — `assets_dir()` helper resolves `assets/` directory in both dev mode and Nuitka frozen mode; replaces all `Path("assets")` hardcodes in `fonts.py`, `audio.py`, `badges.py`
- **`engine/lesson_registry.py`** — `lesson_available(n)` backed by a frozenset; replaces unreliable `importlib.util.find_spec()` in Nuitka onefile builds
- **`__main__.py`** — explicit entry point required by Nuitka (`from cognitive_data_arcade import main; main()`)
- **Rich profile export** — `ProfileManager.export_progress()` now writes a flat, instructor-friendly JSON with `app_version`, `completed_count`, `sp_points`, `quiz_accuracy_pct`, and per-module `module_completion` dictionary; same `X` key and filename as before
- **`tools/aggregate_progress.py`** — standalone instructor script (stdlib + optional `openpyxl`); reads all `*.json` exports from a directory and produces a CSV or Excel summary with one row per student; malformed files skipped with a warning

---

## [v0.8.0] — 2026-06-26

Streak + Daily Challenge — daily habit loop and standalone quiz mode.

### Added

- **Streak tracking** — `Profile` gains `streak_days` and `last_active_date`; `ProfileManager.touch_streak()` increments on consecutive days, resets on gap; called at game start (`ModuleRunnerScene`) and after Daily Challenge
- **Streak badges** — `streak_3` (3 dni z rzędu), `streak_7` (Tygodniowy), `streak_30` (Miesięczny); awarded automatically when threshold is first crossed; visible in ProfileScene badge gallery
- **Daily Challenge** — 20-question TOML bank (`data/daily_challenges.toml`); deterministic daily selection (`pick_daily` seeds on `date.toordinal()`); same 5 questions for all students on a given day
- **DailyChallengeScene** — 4-state flow: TITLE → QUESTION → RESULT → SUMMARY; A/B/C/D keys or mouse click; explanation shown after each answer; wrapped in `PausableGame` (ESC opens pause menu)
- **`D` key in menu** — opens Daily Challenge; streak chip `* Nd` shown in topbar when streak > 0
- **Streak row in ProfileScene** — displayed between SP total and lesson dots
- **RESULT polish** — verdict prefixed with `✓` (correct) or `✗` (wrong); question text word-wraps on long strings
- **SUMMARY badge reveal** — if a streak milestone was crossed, SUMMARY shows "Nowa odznaka! / New badge!" with the badge name
- **Tests** — `tests/test_streak.py` and `tests/test_challenge_loader.py`

---

## [v0.7.0] — 2026-06-25

Semester Platform — act narrative layer, checkpoint quizzes, syllabus overview, and full diacritics audit.

### Added

- **Act intro screens** (`ActIntroScene`) — narrative text shown once per act before the first game; skipped on repeat visits; `seen_act_intros: list[int]` in Profile
- **Checkpoint quizzes** (`QuizScene`) — 3-option quiz after each lesson (31 questions in `data/quiz_data.py`); result stored once in `quiz_results: dict[str, bool]`; wired via `pending_quiz_lesson` in `ModuleRunnerScene`
- **Act bridge texts** — motivational paragraph in `ModuleCompleteScene` connecting acts narratively (`data/act_content.py`)
- **SyllabusScene** — 2×3 grid of all 6 acts with completion status; `S` key from menu and profile screen; Polish titles, descriptions, and act-click navigation to the corresponding module
- **Progress export** — `X` key in ProfileScene exports full profile JSON to `~/cda_progress_<alias>.json`; footer layout and success toast polished

### Fixed

- **Polish diacritics** — comprehensive audit: `i18n.py`, `act_content.py`, `quiz_data.py` (P1); 26 lesson files (P2); 27 game files (P3); residual cleanup (P4) — ą/ę/ś/ź/ż/ó/ń/ł/ć now consistent throughout
- `SyllabusScene` back-scene creates a fresh `LessonMenuScene` to avoid stale state
- Pygame mixer segfault in CI caused by stale `Sound` objects on re-import

---

## [v0.6.0] — 2026-06-24

Game Quality Audit — UX review of all 31 games: feedback, session results, and HowToPlay wiring.

### Added

- **SessionResult wiring** — `SessionResult` → `BadgeEngine` → `SessionSummaryScene` wired for all 26 games that were missing it; sandbox games get Q-key exit with exploration-depth score; phase-delegation and phase-carousel games get correct routing
- **Per-decision feedback and session summary overlays** — L10 N-Back: 600 ms OK/X overlay after each trial; L24 Semantic Space: 1.5 s feedback screen between missions; L01/L06/L13/L21/L22/L27: Q-key summary overlay with stats then auto-exit; L18/L19: verdict line on PhaseRoundResultScene; L29: diversity verdict; L31: synthesis sentence based on cognitive profile
- **HowToPlay wiring** — `make_how_to_play()` wired for 10 games that were missing the intro screen
- **Reset progress dialog** — ProfileScene shows a confirmation dialog before wiping completed lessons and arcade points

### Fixed

- **L04 Data Quality Lab** — critical bug that blocked game completion; `SessionResult` and `HowToPlayScene` now wired correctly

---

## [v0.5.0] — 2026-06-23

Data & Gamification — Cognitive Dashboard wired to real data, module completion badges, sequential learning mode.

### Added

- **Cognitive Dashboard wiring** — L12 (`CognitiveDashboardModeScene`) reads real CSV files logged by RT Lab, Stroop, Flanker, GoNoGo, N-Back; cross-task profile with per-game mean RT, accuracy, and what-if sliders now show actual student data instead of placeholders
- **Module completion badges** — 6 PNG badge icons (one per module) + 2 special badges (first lesson, all 31 done); `ModuleBadge` dataclass and `_MODULE_BADGES` registry in `engine/badges.py`; `earned_badges()` and `module_complete()` helpers; badge icon shown in sidebar header when module is done
- **Session achievement badges with PNG icons** — existing 5 `Badge` types (quick reflex, sharpshooter, high accuracy, clean data, first game) now display MIT-licensed Tabler Icons PNG in `ProfileScene` instead of emoji
- **Profile gallery** — `ProfileScene` shows two rows: session achievement cards and an 8-slot module badge strip; earned badges bright, unearned dimmed with `BLEND_RGBA_MULT`
- **Sequential learning mode** — clicking a module header opens `ModuleRunnerScene`: horizontal stepper (circles + connecting lines), lesson card with equal **Teoria** / **Zagraj** buttons, step auto-advances after completing a lesson, soft recommendation (no hard locks)
- **ModuleCompleteScene** — badge glow reveal, lesson count stats, next-module routing (`Moduł N+1 →`) or back to menu for the last module; calls `clear_current_module()` on init
- **`current_module_idx`** field on `Profile` — persists which module the student is running through; `set_current_module()` / `clear_current_module()` on `ProfileManager`
- **Topbar continuation hint** — when `current_module_idx` is set, `LessonMenuScene` topbar shows `"Kontynuuj: <ModuleName>"` in indigo
- **Module header affordance** — headers have subtle background, brighter label, stronger hover, and an indigo `> Start` pill button to signal interactivity
- **Mouse click in runner** — stepper circles and mini-bar cells are clickable (in addition to arrow keys)
- **`game_launcher.py`** — `game_factory_for()` and `game_factory_for_with_back()` extracted from `LessonMenuScene` to a standalone module; runner reuses it without circular imports

---

## [v0.4.0] — 2026-06-23

Progress & Settings — progress tracking, OptionsScene wiring, ELD Scenario 4.

### Added

- **Progress tracking** — `complete_lesson()` called on game launch; `_completed` cache in `LessonMenuScene`; green dot in sidebar (5px), type-colored dot when not done (4px); `X / 31` counter in topbar (green when at least one done)
- **Skip-intro wiring** — `make_how_to_play()` helper reads `profile.seen_intro`; Options → Tutorial OFF skips `HowToPlayScene` in all 6 wired games (BigDataMap, RT Lab, EDA, Stroop, Flanker, GoNoGo)
- **ELD Scenario 4** — A/B Test: Online Experiment; 6 decisions covering sample size calculation, test duration (weekly seasonality), primary metric, traffic split, multiple comparisons, and pre-registration

### Already present (confirmed in v0.4.0 review)

- **PL/EN language toggle** — K_l in menu, persists to profile, restores on startup
- **OptionsScene** — music + SFX volume sliders and toggles, fullscreen toggle, Tutorial toggle (now wired)

---

## [v0.3.0] — 2026-06-23

Content & Discovery — diacritics fix and interactive concept network.

### Added

- **Concept network** (`L01 Big Data Map`) — redesigned as an interactive graph linking all 31 lessons across 6 modules; ~77 cross-module edges with PL/EN rationale per connection; sequential display numbers 1-31; connected-node highlighting; zoom (scroll wheel) + reset (R)
- **ConceptDetailScene** — full-screen detail panel opened on double-click or ENTER; shows description, up to 5 logical connections with reasons; BACKSPACE returns to network, ESC shows pause menu
- **DISPLAY_NUM** mapping — circles show sequential 1-31 (lesson file numbers skip 5, end at 32)
- **EDGE_REASONS** dict — ~77 canonical edges with PL+EN explanation driving both graph rendering and the detail panel

### Fixed

- **Polish diacritics** — lessons 29-32 (Recommendation Bubble, Bias Blind Spot, You Were the Dataset, Architect's Trial) rewritten with correct ą/ę/ś/ź/ż/ó/ń/ł/ć in Polish content
- Concept network node labels no longer overlap circles (two-pass drawing)
- Zoom centres on canvas centre for predictable behaviour; R key resets zoom
- BACKSPACE from detail panel goes to network directly (not HowToPlay screen)

---

## [v0.2.0] — 2026-06-21

UX consistency pass across the entire app.

### Added

- New lesson menu: sidebar + panel layout, indigo palette (`#6366f1` / `#0d0f1a`)
- Centralized color palette in `engine/colors.py` (130 files migrated)
- Space Grotesk Regular + Medium as the primary typeface (replaces Inter and SysFont)
- Keyboard and mouse hints added to all interactive game phases
- Lesson reader: mouse click on Teoria / Notatki / Zadania tabs
- Lesson reader: TOC dropdown overlay (T key or hamburger button) with section navigation and hover highlight
- Expanded lesson content for all 31 games — 2-4 new theory slides per lesson with named researchers, dates, and quantitative facts
- README status table, STUDENT_GUIDE, GitHub PR template and issue templates, CI badge
- Polish diacritics audit and em-dash → hyphen pass across all lesson text

### Fixed

- Standardized game resolution to 1024×768 across all 64 game files
- Correct lesson count label and row order for lessons 30-31
- TOC dropdown: pixel-based text truncation with "…" (replaces 48-char limit)

---

## [v0.1.0] — 2026-06-21

First complete release: 31 playable games, full CI, analysis scenes.

### Games (by module)

**Module 1 — Data & Cognition Basics**
- L01 Big Data Map — interactive concept overview
- L02 Reaction Time Lab — chronometric measurement, CSV logging
- L03 Event Log Detective — data parsing puzzle
- L04 Data Quality Lab — missing values, outliers, cleaning
- L06 EDA Sandbox — interactive RT experiment designer with live charts

**Module 2 — Cognitive Science**
- L07 Stroop Challenge — interference effect arcade game
- L08 Flanker Task — executive attention, congruent/incongruent trials
- L09 Go/No-Go — inhibitory control, false-alarm tracking
- L10 N-Back — working memory load levels
- L11 Visual Search Lab — feature vs conjunction search
- L12 Cognitive Dashboard — cross-task profile with what-if sliders

**Module 3 — Statistics**
- L13 Distribution Playground — shape, parameters, CLT
- L14 Correlation Trap — causation fallacies, Pearson r
- L15 Hypothesis Arena — p-values, effect size, statistical power
- L16 Prediction Slider — linear regression, Cook's distance

**Module 4 — Machine Learning**
- L17 Feature Hunter — drag-and-drop feature selection game
- L18 Classifier Battle — perceptron, SVM, decision tree comparison
- L19 Overfitting Monster — bias-variance tradeoff sandbox
- L20 Anomaly Alert — Isolation Forest, Mahalanobis distance

**Module 5 — Natural Language Processing**
- L21 Text Tokenizer Lab — Zipf's law, BPE, corpus statistics
- L22 Word Weight Factory — BoW / TF-IDF pipeline sandbox
- L23 Emotion Classifier — sentiment analysis with VADER
- L24 Semantic Space Explorer — word embeddings, cosine similarity
- L25 Topic Detective — LDA topic modeling missions
- L26 Human vs Model Challenge — negation, sarcasm, Winograd schemas

**Module 6 — Networks & Ethics**
- L27 Social Network Simulator — SIR epidemic on random/scale-free graphs
- L28 Misinformation Spread — spreader vs fact-checker asymmetry
- L29 Recommendation Bubble — filter bubble mechanics, diversity scoring
- L30 Bias Blind Spot — proxy features, fairness impossibility theorem
- L31 You Were the Dataset — behavioural data, Hawthorne effect, GDPR
- L32 The Architect's Trial — AI ethics decision game (Goodhart's law, EU AI Act)

### Infrastructure

- `uv` + `pyproject.toml` project setup
- GitHub Actions CI (lint + 1200 tests on push/PR)
- `engine/` shared subsystems: fonts, colors, audio, scrollbar, i18n, PausableGame
- `SessionSummaryScene` for arcade games, phase-result screens for lab games
- CSV logging for RT, Stroop, Flanker, Go/No-Go, N-Back

---

## Roadmap

| Version | Theme | Key deliverables |
|---------|-------|-----------------|
| **v0.3.0** ✅ | Content & Discovery | Diacritics fix (L29-32) · Concept network map |
| **v0.4.0** ✅ | Progress & Settings | Progress tracking · Skip-intro wiring · ELD Scenario 4 |
| **v0.5.0** ✅ | Data & Gamification | Cognitive Dashboard wiring (real CSV) · Badges · Sequential learning mode |
| **v0.6.0** ✅ | Game quality | SessionResult + HowToPlay wiring for all 31 games · Per-decision feedback overlays · Reset progress |
| **v0.7.0** ✅ | Semester Platform | Act intros · Checkpoint quizzes · SyllabusScene · Progress export · Diacritics audit |
| **v0.8.0** ✅ | Streak + Daily | Streak tracking · Daily Challenge scene · 20-question bank · Streak badges |
| **v0.9.0** ✅ | Distribution & Instructor | Standalone exe (Win/Mac/Linux) · GitHub Releases · Rich profile export · Instructor aggregator script |
| **v0.10.0** ✅ | Content completion | Lesson content for all 31 lessons · 60+ daily challenge questions · Analysis scenes (ML/NLP) · Quiz audit |
| **v1.0.0a** ✅ | Student-Ready Alpha | Onboarding flow · Profile data stats · Home prompts · Pre-release hardening |
| **v1.0.0** | Release | October 2026 · student assessment target |
