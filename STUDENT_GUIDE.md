# Student Guide — Cognitive Data Arcade

This guide walks you through the full learning cycle of the project:

**play a game → data appears → analyse it → interpret the result → think about what it means**

You don't need to know Python before starting. You do need to be curious.

---

## What is this project?

Cognitive Data Arcade is a collection of interactive experiments built in Python. Each experiment asks you to do something — react, decide, classify, build — and records what you did. You then open that data in Python and analyse it the same way a researcher would.

The point is not to play games. The point is to experience the full data science pipeline on data that came from you.

---

## Setup

```bash
git clone https://github.com/michalmaj/cognitive-data-arcade.git
cd cognitive-data-arcade
uv sync
```

Run the arcade:

```bash
uv run cognitive-data-arcade
```

A window opens with a list of 31 games. Navigate with the arrow keys. Press **Enter** to start.

---

## First lab: Reaction Time

Start with **Reaction Time Lab** (lesson 2 in the menu). It is the shortest path to the full cycle.

### What you will do

The game shows a circle on screen after a random delay. Press **Space** as fast as you can. After 20 trials the session ends and shows you a summary.

Run it at least twice — once normally, once while deliberately distracted (look away, tap your foot, count backwards). You will see the difference in the data.

### Where is your data?

After each session, a CSV file appears in:

```
data/generated/reaction_time/
```

The filename is a timestamp, e.g. `20260527_161352.csv`. Open it in any text editor to see the raw rows.

Each row is one trial:

```
participant_id, session_id, trial_id, task_name, condition,
stimulus, expected_response, actual_response, correct,
reaction_time_ms, timestamp, distractor_count
```

The columns that matter most for your first analysis: `correct`, `reaction_time_ms`, `condition`.

### First analysis

Open a Python session (or a notebook) in the project directory:

```bash
uv run python
```

```python
import pandas as pd
from pathlib import Path

# Load your most recent session
files = sorted(Path("data/generated/reaction_time").glob("*.csv"))
df = pd.read_csv(files[-1])

# How many trials?
print(len(df))

# How many correct?
print(df["correct"].value_counts())

# Mean reaction time on correct trials
correct = df[df["correct"]]
print(correct["reaction_time_ms"].describe().round(1))
```

### What to look for

A typical result for a focused adult: **200–350 ms** median, low standard deviation.

If your median is above 450 ms, something slowed you down — distraction, uncertainty, or fatigue.

If your standard deviation is very high (> 150 ms), your responses were inconsistent — which itself is a finding.

### Simple comparison

If you ran two sessions (focused vs. distracted):

```python
files = sorted(Path("data/generated/reaction_time").glob("*.csv"))

session_a = pd.read_csv(files[-2])   # earlier session
session_b = pd.read_csv(files[-1])   # later session

for label, s in [("Session A", session_a), ("Session B", session_b)]:
    correct = s[s["correct"]]
    print(f"{label}: median RT = {correct['reaction_time_ms'].median():.0f} ms, "
          f"accuracy = {s['correct'].mean():.1%}")
```

### Interpret the result

Do not just report the numbers. Ask:

- Is the difference between sessions real, or within normal variation?
- How many trials did you run? Is 20 enough to draw conclusions?
- What else could explain the difference besides distraction?
- If you ran the same session again right now, would you get the same result?

These questions are what data science is actually about.

---

## What data do games generate?

Six games log CSV files to `data/generated/`. Here are the exact columns for each.

### Reaction Time Lab → `data/generated/reaction_time/`

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | string | Device UUID — same across all your sessions |
| `session_id` | string | Timestamp string, unique per session |
| `trial_id` | int | Trial number within the session (1-based) |
| `task_name` | string | Always `reaction_time` |
| `condition` | string | `focused` or `distracted` |
| `stimulus` | string | Shape shown (`circle`) |
| `expected_response` | string | Key that should be pressed |
| `actual_response` | string | Key that was pressed (empty if timeout) |
| `correct` | bool | `True` if responded within the time limit |
| `reaction_time_ms` | float | Time from stimulus to keypress in milliseconds |
| `timestamp` | string | ISO 8601 wall-clock time of the trial |
| `distractor_count` | int | Number of distractors shown in distracted mode |

Key columns for analysis: `correct`, `reaction_time_ms`, `condition`.

---

### Stroop Challenge → `data/generated/stroop/`

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | string | Device UUID |
| `session_id` | string | Session timestamp |
| `trial_id` | int | Trial number |
| `task_name` | string | Always `stroop` |
| `condition` | string | `congruent` (ink matches word) or `incongruent` (mismatch) |
| `stimulus` | string | The word shown (e.g. `RED`) |
| `ink_color` | string | Actual ink colour (e.g. `blue`) |
| `word_color` | string | Colour named by the word |
| `expected_response` | string | Correct ink colour name |
| `actual_response` | string | Key pressed |
| `correct` | bool | Whether response was correct |
| `reaction_time_ms` | float | Reaction time in ms |
| `timestamp` | string | ISO 8601 trial time |

Key question: is `reaction_time_ms` higher on `incongruent` trials? That is the Stroop effect.

---

### Flanker Arena → `data/generated/flanker/`

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | string | Device UUID |
| `session_id` | string | Session timestamp |
| `trial_id` | int | Trial number |
| `task_name` | string | Always `flanker` |
| `condition` | string | `congruent` or `incongruent` |
| `target_direction` | string | `left` or `right` — the correct answer |
| `correct` | bool | Whether response matched target direction |
| `reaction_time_ms` | float | Reaction time in ms |
| `timestamp` | string | ISO 8601 trial time |

Key question: compare mean RT and accuracy between `congruent` and `incongruent` conditions.

---

### Go/No-Go Guard → `data/generated/gono/`

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | string | Device UUID |
| `session_id` | string | Session timestamp |
| `trial_id` | int | Trial number |
| `task_name` | string | Always `go_no_go` |
| `trial_type` | string | `go` (respond) or `nogo` (withhold) |
| `response` | string | `hit`, `miss`, `false_alarm`, or `correct_rejection` |
| `correct` | bool | Whether the response was appropriate |
| `reaction_time_ms` | float | RT in ms; `0.0` if no response was made |
| `timestamp` | string | ISO 8601 trial time |

Key question: what is your false alarm rate (pressing on `nogo` trials)? That measures impulse control.

---

### N-Back Memory Grid → `data/generated/nback/`

| Column | Type | Description |
|--------|------|-------------|
| `task_name` | string | Always `n_back` |
| `participant_id` | string | Device UUID |
| `session_id` | string | Session timestamp |
| `trial_id` | int | Trial number |
| `block_id` | int | Block number |
| `n_level` | int | N-back level played (1, 2, or 3) |
| `position` | int | Grid position shown (0–8) |
| `letter` | string | Letter shown |
| `pos_match` | bool | Whether position matches N steps back |
| `let_match` | bool | Whether letter matches N steps back |
| `key_a_pressed` | bool | Whether the position-match key was pressed |
| `key_l_pressed` | bool | Whether the letter-match key was pressed |
| `pos_correct` | bool | Correct response for position match |
| `let_correct` | bool | Correct response for letter match |
| `rt_a_ms` | float | Reaction time for the A key (ms) |
| `rt_l_ms` | float | Reaction time for the L key (ms) |

Key question: how does accuracy (`pos_correct`, `let_correct`) change as `n_level` increases?

---

### Visual Search Lab → `data/generated/visual_search/`

| Column | Type | Description |
|--------|------|-------------|
| `participant_id` | string | Device UUID |
| `session_id` | string | Session timestamp |
| `trial_id` | int | Trial number |
| `mode` | string | Search type (`feature` or `conjunction`) |
| `condition` | string | Trial condition |
| `set_size` | int | Number of items on screen |
| `target_present` | bool | Whether the target was actually present |
| `response` | string | `present`, `absent`, or `timeout` |
| `correct` | bool | Whether response matched target presence |
| `rt_ms` | float | Reaction time in ms (`NaN` on timeout) |
| `timestamp` | string | ISO 8601 trial time |

Key question: does `rt_ms` grow with `set_size` in conjunction search but not in feature search? That is the slope-of-the-search-function.

---

## Module guide

The arcade is organised into 6 modules. You can play in any order, but the modules build on each other conceptually.

### Module 1 — Data & Cognition Basics (lessons 1–6)

**Goal:** Understand what data science data looks like before running any statistics.

- **L01 Big Data Map** — overview of how all 31 lessons connect. Start here if you want to understand the big picture.
- **L02 Reaction Time Lab** — your first CSV file. See "First lab" above.
- **L03 Event Log Detective** — puzzle: read and interpret a messy experiment log. No CSV produced; all analysis is in-game.
- **L04 Data Quality Lab** — detect missing values, outliers, encoding errors in a raw dataset.
- **L06 EDA Sandbox** — design and run a mini experiment; explore the data live before any modelling.

**After this module:** You should be able to load a CSV with pandas, compute basic statistics, and explain what each column means.

---

### Module 2 — Cognitive Science (lessons 7–12)

**Goal:** Run the classic experiments of cognitive psychology on yourself and read the numbers they produce.

- **L07 Stroop Challenge** — cognitive interference; logs `stroop/` CSV.
- **L08 Flanker Arena** — selective attention; logs `flanker/` CSV.
- **L09 Go/No-Go Guard** — inhibitory control; logs `gono/` CSV.
- **L10 N-Back Memory Grid** — working memory load; logs `nback/` CSV.
- **L11 Visual Search Lab** — feature vs. conjunction search; logs `visual_search/` CSV.
- **L12 Cognitive Dashboard** — reads all five CSVs above and shows your cross-task profile. **Play the five games first, then open this.**

**After this module:** You will have five CSV datasets from your own cognitive sessions. The Cognitive Dashboard reads them automatically.

---

### Module 3 — Statistics (lessons 13–16)

**Goal:** Connect the distributions and numbers you saw in modules 1–2 to formal statistical tools.

- **L13 Distribution Playground** — change parameters of Normal, Poisson, and t distributions; watch the shape change.
- **L14 Correlation Trap** — Pearson r, causation fallacies, Anscombe's quartet.
- **L15 Hypothesis Arena** — p-values, effect size, statistical power — interactive arcade game.
- **L16 Prediction Slider** — linear regression; Cook's distance; see how one outlier moves the line.

**After this module:** You should be able to describe a distribution, run a correlation, and interpret a p-value without treating it as a verdict.

---

### Module 4 — Machine Learning (lessons 17–20)

**Goal:** Build intuition for what ML models actually do before you write any `sklearn` code.

- **L17 Feature Hunter** — drag features onto a model; see how accuracy changes.
- **L18 Classifier Battle** — perceptron, SVM, decision tree on the same data; compare decision boundaries.
- **L19 Overfitting Monster** — bias-variance trade-off sandbox; watch a model overfit in real time.
- **L20 Anomaly Alert** — Isolation Forest and Mahalanobis distance on synthetic data.

**After this module:** You should be able to explain overfitting, why a high training accuracy can be bad, and what a decision boundary is.

---

### Module 5 — Natural Language Processing (lessons 21–26)

**Goal:** Understand how text becomes numbers, and what those numbers mean for meaning.

- **L21 Text Tokenizer Lab** — Zipf's law, BPE tokenisation, vocabulary statistics.
- **L22 Word Weight Factory** — Bag-of-Words and TF-IDF pipeline, interactive.
- **L23 Emotion Classifier** — VADER sentiment analysis; test it against your own sentences.
- **L24 Semantic Space Explorer** — word embeddings, cosine similarity, analogy arithmetic.
- **L25 Topic Detective** — LDA topic modelling; what themes emerge from a corpus?
- **L26 Human vs. Model Challenge** — negation, sarcasm, Winograd schemas: where models fail.

**After this module:** You should be able to describe the bag-of-words assumption and explain why word embeddings are not the same as word definitions.

---

### Module 6 — Networks & Ethics (lessons 27–32)

**Goal:** Understand how structure shapes behaviour — and what happens when algorithms make consequential decisions.

- **L27 Social Network Simulator** — SIR epidemic model on random vs. scale-free graphs.
- **L28 Misinformation Spread** — spreader vs. fact-checker asymmetry.
- **L29 Recommendation Bubble** — filter bubble mechanics; diversity scoring.
- **L30 Bias Blind Spot** — proxy features, fairness impossibility theorem.
- **L31 You Were the Dataset** — behavioural data, Hawthorne effect, GDPR.
- **L32 The Architect's Trial** — AI ethics decision game; Goodhart's Law and the EU AI Act.

**After this module:** You should be able to explain one concrete way that an algorithm can be fair by one metric and unfair by another, and why that is not a bug.

---

## What to hand in

Each lab session or module has specific deliverables. Here is what your instructor expects.

### Per-session deliverable (each time you play a game)

For games that log data (L02, L07–L11):

1. **The CSV file** — copy it out of `data/generated/<game>/` and keep it. Filename is the session timestamp.
2. **A short analysis** (5–10 lines of Python) — at minimum: load the file, compute mean and median RT or accuracy per condition, print the result.
3. **One sentence of interpretation** — what does the number mean? Is it what you expected?

You do not need to write a report. A notebook cell with the code and one markdown cell with the interpretation is enough.

### Module deliverable

After completing all lessons in a module:

| Module | What to submit |
|--------|---------------|
| 1 — Data Basics | Load any one of your CSVs. Describe what each column means in your own words. Identify one data quality issue (even if minor). |
| 2 — Cognitive Science | Combine at least two of your cognitive CSVs. Compare your performance across tasks. Does any pattern emerge? |
| 3 — Statistics | Take your RT data from Module 2. Compute a t-test between congruent and incongruent conditions. Report the p-value, effect size, and whether the result is interpretable given your sample size. |
| 4 — Machine Learning | Use any of your CSV data as input to a scikit-learn classifier. Report training vs. test accuracy. Explain in one sentence why they differ. |
| 5 — NLP | Run VADER on five sentences you write yourself — two clearly positive, two clearly negative, one ambiguous. Report the compound score and explain where it surprised you. |
| 6 — Networks & Ethics | Pick one scenario from The Architect's Trial. Explain the trade-off you faced, what you chose, and what you would change if you had to make the same decision in a real system. |

### Export your progress

At any time, press **X** in the Profile screen to export a JSON summary of your progress. This includes completed lessons, arcade points, quiz accuracy, and per-module completion. You can share this file with your instructor as proof of completion.

---

## How to read the in-game theory

Every game has a theory screen. Press **T** in the menu to open it before playing. It explains the cognitive concept behind the task in plain language.

Read it before playing, not after. The theory changes what you notice during the game.

---

## A note on your own data

The data this project generates is about you. Your reaction times, your accuracy, your decisions. That makes it more interesting to analyse — and also a reason to think carefully about what conclusions are valid.

A single session of 20 trials is not a scientific study. It is a starting point. The goal is to understand the pipeline, not to diagnose yourself.

All data stays on your computer. The app never sends anything over the network.
