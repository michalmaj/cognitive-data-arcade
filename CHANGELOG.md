# Changelog

All notable changes to Cognitive Data Arcade are documented here.

## [Unreleased] — v0.4.0

### Planned

- **Progress tracking** — per-lesson completed flag stored in profile; progress visible in lesson menu
- **PL/EN language toggle** — switch language in-app without restart, persists to profile
- **Settings (OptionsScene)** — music toggle and skip-intro (HowToPlay) toggle; now that audio and intros are real features, settings make sense
- **Event Log Detective — Scenario 4** — new experiment scenario (engine already supports it; pure data addition)

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
| **v0.3.0** | Content & Discovery | Diacritics fix (L29-32) · Concept network map |
| **v0.4.0** | Progress & Settings | Per-lesson progress tracking · Badges · PL/EN toggle in UI · Music/intro settings |
| **v0.5.0+** | Game quality | UX audit of individual games — to be scoped after v0.4.0 |
