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

## What next?

The arcade is designed so that each game adds one more concept. After Reaction Time Lab, the natural next steps are:

- **Stroop Challenge** (lesson 6) — same measurement, but now there is a cognitive manipulation. Compare your RT under interference with your baseline from this lab.
- **Flanker Arena** (lesson 7) — attention control under conflicting signals.
- **Cognitive Dashboard** (lesson 11) — look at all your sessions together in one place.

Each of those games saves data in the same format. You can combine sessions across games once you understand what each column means.

---

## How to read the in-game theory

Every game has a theory screen. Press **T** in the menu to open it before playing. It explains the cognitive concept behind the task in plain language.

Read it before playing, not after. The theory changes what you notice during the game.

---

## A note on your own data

The data this project generates is about you. Your reaction times, your accuracy, your decisions. That makes it more interesting to analyse — and also a reason to think carefully about what conclusions are valid.

A single session of 20 trials is not a scientific study. It is a starting point. The goal is to understand the pipeline, not to diagnose yourself.
