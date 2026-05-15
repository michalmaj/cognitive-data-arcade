# Cognitive Data Arcade

**Cognitive Data Arcade** is an interactive educational repository for teaching **Big Data, Data Science, and Machine Learning in the context of Cognitive Science**.

The project combines:

* interactive mini-games built with **Pygame**,
* behavioral data collection,
* Markdown-based theory materials,
* Markdown-based student tasks,
* reproducible Python data analysis,
* small open or synthetic datasets,
* a 30-class course structure designed for 90-minute sessions.

The core idea is simple:

> Students do not only analyze data. They generate, inspect, clean, model, and interpret data produced by cognitive and behavioral tasks.

Instead of treating Big Data as an abstract infrastructure topic, this repository presents it as a practical way to study attention, reaction time, inhibition, memory, language, decision-making, social behavior, recommendation systems, and ethical issues in AI.

---

## Project Status

This repository is currently planned as an educational and research-oriented teaching project.

The first implementation goal is a small but complete MVP containing:

1. a Pygame launcher,
2. a consistent lesson structure,
3. one or more playable cognitive mini-games,
4. local CSV data logging,
5. basic data analysis scripts,
6. Markdown theory and task files,
7. tests for the data logging and analysis utilities.

The project should grow gradually. It is more important to build a clean, maintainable foundation than to implement all 30 lessons immediately.

---

## Educational Goal

This repository is designed for students of **Cognitive Science**, but it can also be used by students interested in psychology, data science, human-computer interaction, AI, social computing, and digital behavior analysis.

The course should help students understand:

* what Big Data means in the context of human behavior,
* how behavioral data can be generated and collected,
* how raw logs become structured datasets,
* how to clean and validate messy data,
* how to use Python for exploratory data analysis,
* how to interpret reaction time, accuracy, error patterns, and behavioral traces,
* how to apply basic statistics and machine learning,
* how text, networks, and recommender systems can be analyzed,
* why privacy, bias, fairness, consent, and interpretation matter.

The course is intentionally practical. Students should learn by playing, collecting data, analyzing results, and discussing the meaning and limitations of their findings.

---

## Teaching Philosophy

This repository follows a learning-by-doing model:

```text
cognitive concept -> interactive task -> generated data -> analysis -> interpretation -> ethical reflection
```

Every lesson should connect a technical data science topic with a cognitive science question.

Examples:

* Reaction time is not just a number. It is a behavioral measure.
* Missing values are not just technical errors. They may reflect participant dropout, fatigue, confusion, or interface problems.
* A classifier is not only a prediction tool. It can also introduce bias or hide poor assumptions.
* A recommendation system is not just an algorithm. It can shape attention, preferences, and behavior.

The repository should avoid dry, isolated exercises such as generic sales tables unless they are explicitly used as contrast examples.

---

## Why Pygame?

Pygame is used because it allows the project to create simple, accessible, interactive experiments and mini-games in Python.

In this project, Pygame is responsible for:

* displaying stimuli,
* collecting keyboard and mouse responses,
* measuring reaction times,
* creating simple game-like feedback,
* making classes more engaging,
* generating behavioral data.

Pygame should **not** be used as a replacement for proper data analysis tools.

Data analysis should be performed with standard Python libraries such as:

* Pandas,
* NumPy,
* Matplotlib,
* scikit-learn,
* NetworkX,
* optional NLP libraries.

The intended architecture is:

```text
Pygame -> interaction and data generation
CSV/JSON -> stored behavioral logs
Python analysis scripts -> statistics, visualization, ML, interpretation
Markdown -> theory, tasks, reflection questions
```

---

## Repository Structure

Recommended structure:

```text
cognitive-data-arcade/
  README.md
  README.pl.md
  LICENSE
  LICENSE-CONTENT.md
  pyproject.toml
  uv.lock

  src/
    cognitive_data_arcade/
      __init__.py
      main.py

      engine/
        __init__.py
        scene.py
        game_loop.py
        events.py
        storage.py
        timing.py
        assets.py

      ui/
        __init__.py
        menu.py
        buttons.py
        text_panel.py
        charts.py

      games/
        __init__.py
        reaction_time/
          __init__.py
          game.py
          config.py
        stroop/
          __init__.py
          game.py
          config.py
        flanker/
          __init__.py
          game.py
          config.py
        go_no_go/
          __init__.py
          game.py
          config.py
        n_back/
          __init__.py
          game.py
          config.py

      analytics/
        __init__.py
        load_data.py
        cleaning.py
        descriptive_stats.py
        visualization.py
        ml.py
        nlp.py
        graphs.py
        reports.py

  lessons/
    01_big_data_in_cognitive_science/
      README.md
      theory.md
      tasks.md
      instructor_notes.md
      lesson_config.json

    02_reaction_time_data/
      README.md
      theory.md
      tasks.md
      instructor_notes.md
      lesson_config.json

    03_event_logs_and_data_formats/
      README.md
      theory.md
      tasks.md
      instructor_notes.md
      lesson_config.json

  data/
    README.md
    samples/
    synthetic/
    generated/
      .gitkeep
    external/
      .gitkeep
    licenses/

  scripts/
    generate_synthetic_data.py
    download_datasets.py
    export_class_report.py

  tests/
    test_storage.py
    test_timing.py
    test_descriptive_stats.py
    test_data_validation.py

  docs/
    course_plan.md
    datasets.md
    assessment.md
    setup.md
    architecture.md
```

---

## Course Format

The course is designed as **30 classes**, each lasting **90 minutes**.

Each class should include:

1. a short conceptual introduction,
2. a Markdown theory section,
3. a Pygame activity or mini-game,
4. generated or provided data,
5. a guided analysis task,
6. interpretation questions,
7. a short reflection or exit ticket.

Recommended 90-minute structure:

```text
00-10 min  Introduction and demonstration
10-25 min  Theory reading and discussion
25-45 min  Interactive activity / game / data generation
45-70 min  Data analysis task
70-85 min  Interpretation and discussion
85-90 min  Exit ticket
```

---

## Lesson Structure

Each lesson should follow a consistent structure.

Example:

```text
lessons/07_stroop_challenge/
  README.md
  theory.md
  tasks.md
  instructor_notes.md
  lesson_config.json
```

### `README.md`

Short overview of the lesson.

Should include:

* lesson title,
* learning goals,
* required game or dataset,
* expected outputs,
* estimated time.

### `theory.md`

Student-facing theoretical explanation.

Should include:

* cognitive science background,
* data science concept,
* key terms,
* simple examples,
* common mistakes,
* interpretation guidance.

### `tasks.md`

Student-facing practical tasks.

Should include:

* step-by-step instructions,
* commands to run,
* questions to answer,
* plots or statistics to produce,
* short written interpretation task.

### `instructor_notes.md`

Teacher-facing notes.

Should include:

* timing suggestions,
* expected student difficulties,
* optional discussion points,
* suggested answers,
* possible extensions.

### `lesson_config.json`

Machine-readable lesson configuration used by the launcher.

Example:

```json
{
  "id": "07_stroop_challenge",
  "title": "Stroop Challenge",
  "module": "Cognitive Experiments as Data Sources",
  "game": "stroop",
  "estimated_minutes": 90,
  "outputs": [
    "data/generated/stroop_runs/*.csv"
  ],
  "analysis_script": "src/cognitive_data_arcade/analytics/descriptive_stats.py"
}
```

---

## Proposed 30-Class Course Plan

### Module 1: Human Data and Data Foundations

| Class | Topic                                    | Interactive Activity    |
| ----: | ---------------------------------------- | ----------------------- |
|    01 | Big Data in Cognitive Science            | Big Data Map            |
|    02 | Behavioral Data and Reaction Time        | Reaction Time Lab       |
|    03 | Event Logs, CSV, JSON, and Data Formats  | Event Logger Game       |
|    04 | Data Cleaning                            | Data Cleaning Dungeon   |
|    05 | Missing Values, Duplicates, and Outliers | Missing Values Hospital |
|    06 | Exploratory Data Analysis                | Chart Builder Arcade    |

### Module 2: Cognitive Experiments as Data Sources

| Class | Topic                                    | Interactive Activity |
| ----: | ---------------------------------------- | -------------------- |
|    07 | Stroop Effect and Cognitive Interference | Stroop Challenge     |
|    08 | Flanker Task and Attention Control       | Flanker Arena        |
|    09 | Go/No-Go and Response Inhibition         | Go/No-Go Guard       |
|    10 | Working Memory                           | N-Back Memory Grid   |
|    11 | Visual Search                            | Visual Search Lab    |
|    12 | Comparing Cognitive Tasks                | Cognitive Dashboard  |

### Module 3: Statistics and Machine Learning

| Class | Topic                              | Interactive Activity    |
| ----: | ---------------------------------- | ----------------------- |
|    13 | Distributions and Variability      | Distribution Playground |
|    14 | Correlation and Causation          | Correlation Trap        |
|    15 | Hypothesis Testing and Effect Size | Hypothesis Arena        |
|    16 | Linear Regression                  | Prediction Slider       |
|    17 | Classification                     | Classifier Battle       |
|    18 | Overfitting and Model Validation   | Overfitting Monster     |

### Module 4: Text, Language, and Semantic Data

| Class | Topic                              | Interactive Activity     |
| ----: | ---------------------------------- | ------------------------ |
|    19 | Text as Data                       | Text Tokenizer Lab       |
|    20 | Bag of Words and TF-IDF            | Word Weight Factory      |
|    21 | Sentiment and Emotion Analysis     | Emotion Classifier       |
|    22 | Embeddings and Semantic Similarity | Semantic Space Explorer  |
|    23 | Topic Modeling                     | Topic Detective          |
|    24 | Humans vs Language Models          | Human vs Model Challenge |

### Module 5: Networks, Recommenders, Ethics, and Final Project

| Class | Topic                                 | Interactive Activity     |
| ----: | ------------------------------------- | ------------------------ |
|    25 | Graphs and Social Networks            | Social Network Simulator |
|    26 | Information Spread and Misinformation | Misinformation Spread    |
|    27 | Recommendation Systems                | Recommendation Bubble    |
|    28 | Bias, Fairness, Privacy, and Consent  | Bias Detective           |
|    29 | Final Project Workshop                | Student Team Work        |
|    30 | Final Presentations                   | Cognitive Data Expo      |

---

## MVP Scope

The initial MVP should include only a small subset of the full course.

Recommended MVP:

```text
01_big_data_in_cognitive_science
02_reaction_time_data
03_event_logs_and_data_formats
04_data_cleaning
07_stroop_challenge
```

The MVP should include:

* Pygame launcher,
* Reaction Time Lab,
* Stroop Challenge,
* CSV logging utility,
* generated sample data,
* basic analysis scripts,
* theory and tasks for each MVP lesson,
* tests for data logging and basic statistics.

Do not implement all 30 lessons at once.

---

## Implementation Roadmap

### Phase 1: Foundation

* Create project structure.
* Configure Python packaging.
* Add Pygame dependency.
* Add Pandas, NumPy, Matplotlib, and pytest.
* Create the main launcher.
* Create a base `Scene` abstraction.
* Create a reusable CSV logger.
* Create a simple menu UI.

### Phase 2: First Game

Implement `Reaction Time Lab`.

Requirements:

* show random visual stimulus after a delay,
* record participant response,
* calculate reaction time in milliseconds,
* store trials in CSV,
* show summary statistics after the session.

Example output schema:

```csv
participant_id,session_id,trial_id,stimulus_type,expected_key,pressed_key,correct,reaction_time_ms,timestamp
```

### Phase 3: First Cognitive Task

Implement `Stroop Challenge`.

Requirements:

* show color words in congruent and incongruent ink colors,
* collect keyboard responses,
* record accuracy and reaction time,
* export results to CSV,
* include basic analysis comparing congruent and incongruent trials.

Example output schema:

```csv
participant_id,session_id,trial_id,word,ink_color,condition,expected_key,pressed_key,correct,reaction_time_ms,timestamp
```

### Phase 4: Lesson Materials

For each MVP lesson, add:

* `README.md`,
* `theory.md`,
* `tasks.md`,
* `instructor_notes.md`,
* `lesson_config.json`.

### Phase 5: Analysis and Reports

Add reusable analysis utilities:

* load generated CSV files,
* validate required columns,
* compute descriptive statistics,
* group data by condition,
* generate simple plots,
* export class-level summaries.

### Phase 6: Testing and Quality

Add tests for:

* CSV logging,
* timestamp generation,
* reaction time calculations,
* data schema validation,
* analysis utilities.

---

## Technical Stack

Recommended stack:

* Python 3.11 or newer,
* Pygame,
* Pandas,
* NumPy,
* Matplotlib,
* scikit-learn,
* NetworkX,
* pytest,
* Ruff,
* uv.

Optional later additions:

* Polars,
* DuckDB,
* Plotly,
* spaCy,
* sentence-transformers,
* nltk,
* TextBlob,
* Jupyter notebooks.

The project should remain beginner-friendly. Avoid unnecessary dependencies in the MVP.

---

## Installation

Recommended installation method:

```bash
uv sync
```

Run the launcher:

```bash
uv run cognitive-data-arcade
```

Alternative module execution:

```bash
uv run python -m cognitive_data_arcade
```

Run tests:

```bash
uv run pytest
```

Run linting:

```bash
uv run ruff check .
```

Format code:

```bash
uv run ruff format .
```

---

## Data Policy

This project should use three types of data.

### 1. Generated Local Data

Generated by students while using Pygame tasks.

Stored in:

```text
data/generated/
```

These files should usually be ignored by Git, except for `.gitkeep` or carefully anonymized examples.

### 2. Synthetic Data

Generated by scripts and safe to include in the repository.

Stored in:

```text
data/synthetic/
```

Synthetic data should be clearly marked as synthetic.

### 3. External Open Data

Downloaded using scripts, not committed directly unless the license explicitly allows redistribution.

Stored in:

```text
data/external/
```

Every external dataset must have:

* source URL,
* license information,
* citation if required,
* description of allowed use,
* download script if possible.

Dataset documentation should be placed in:

```text
data/README.md
data/licenses/
```

---

## Licensing Recommendation

Recommended licensing model:

* source code: MIT License,
* educational content: Creative Commons Attribution 4.0 International,
* synthetic datasets: CC0 or equivalent,
* external datasets: original licenses preserved.

Suggested files:

```text
LICENSE
LICENSE-CONTENT.md
data/licenses/
```

The repository should never silently mix incompatible data licenses.

---

## Coding Guidelines

General rules:

* Use English for code, comments, docstrings, filenames, commit messages, and GitHub-facing materials.
* Keep functions small and readable.
* Prefer explicit names over clever abbreviations.
* Separate game logic from data logging.
* Separate data analysis from Pygame rendering.
* Avoid putting large analysis logic inside game files.
* Keep the MVP simple.

Recommended style:

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrialResult:
    participant_id: str
    session_id: str
    trial_id: int
    correct: bool
    reaction_time_ms: float
```

Avoid global mutable state where possible.

---

## Pygame Design Guidelines

Each game should have:

* a clear entry point,
* a configuration file,
* a small number of screens or scenes,
* deterministic data schema,
* clear instructions for students,
* an end-of-session summary.

Each game should avoid:

* overly complex graphics,
* unnecessary animations,
* hidden rules,
* complicated installation requirements,
* hardcoded absolute paths,
* storing student-identifying information by default.

The project should be playful, but the data should remain clean and useful.

---

## Data Logging Guidelines

Every generated dataset should include enough metadata to support later analysis.

Recommended fields:

```text
participant_id
session_id
trial_id
task_name
condition
stimulus
expected_response
actual_response
correct
reaction_time_ms
timestamp
```

Do not collect personal data unless explicitly needed for a controlled teaching scenario.

For normal classroom use, prefer anonymous participant IDs such as:

```text
participant_001
participant_002
```

or local random IDs.

---

## Example Lesson: Stroop Challenge

### Cognitive Concept

The Stroop task demonstrates cognitive interference. Participants must respond to the ink color of a word while ignoring the word meaning.

Example:

```text
Word: RED
Ink color: blue
Correct response: blue
Condition: incongruent
```

### Data Science Concept

Students compare reaction times and accuracy between congruent and incongruent trials.

### Possible Student Tasks

1. Play the Stroop Challenge.
2. Complete at least 60 trials.
3. Export the results to CSV.
4. Load the CSV file with Pandas.
5. Compute mean reaction time per condition.
6. Compute accuracy per condition.
7. Create a boxplot of reaction times.
8. Interpret whether the data shows a Stroop effect.
9. Discuss possible sources of noise.
10. Reflect on whether a larger dataset would make the conclusion stronger.

---

## Example Analysis Snippet

```python
from pathlib import Path

import pandas as pd


def summarize_stroop_results(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    correct_trials = df[df["correct"]]

    return (
        correct_trials
        .groupby("condition")["reaction_time_ms"]
        .agg(["count", "mean", "median", "std"])
        .reset_index()
    )
```

---

## Assessment Ideas

Suggested grading components:

| Component                    | Weight |
| ---------------------------- | -----: |
| Weekly tasks                 |    30% |
| Data analysis reports        |    25% |
| Final project                |    30% |
| Participation and reflection |    15% |

Final project options:

1. Analyze data generated by one of the cognitive games.
2. Create a new mini-game that generates behavioral data.
3. Extend an existing game with a new experimental condition.
4. Analyze text, social network, or recommendation data.
5. Compare human behavior with model predictions.
6. Investigate bias or fairness in a simple dataset.

---

## Final Project Requirements

A final project should include:

* research question,
* dataset description,
* analysis plan,
* code,
* visualizations,
* interpretation,
* limitations,
* ethical reflection.

Optional technical extension:

* implement a new Pygame mini-game,
* add a new lesson folder,
* add tests for the new functionality,
* create a short demo video or screenshots.

---

## AI Agent Collaboration Guidelines

This repository may be developed with the help of coding agents such as Claude Code, Codex, or similar tools.

Agents should follow these rules:

1. Do not implement all 30 lessons at once.
2. Start with the project foundation and MVP.
3. Keep the architecture simple and explicit.
4. Prefer small, reviewable changes.
5. Add tests for reusable utilities.
6. Keep Pygame code separate from analysis code.
7. Keep generated data out of Git unless it is synthetic or intentionally included.
8. Use English for code and GitHub-facing materials.
9. Do not introduce heavy dependencies without a clear reason.
10. Preserve the educational structure: theory, task, game, data, analysis, interpretation.

Recommended first agent task:

```text
Create the initial Python project structure for Cognitive Data Arcade using uv.
Add a Pygame launcher with a simple menu, a placeholder lesson list, and a clean package layout.
Do not implement all games yet. Include pytest and Ruff configuration.
```

Recommended second agent task:

```text
Implement the Reaction Time Lab as the first playable Pygame mini-game.
The game should show instructions, run a configurable number of trials, measure reaction time, save results to CSV, and display a summary screen.
Add tests for CSV logging and data schema validation.
```

Recommended third agent task:

```text
Add lesson materials for 01_big_data_in_cognitive_science and 02_reaction_time_data.
Each lesson should include README.md, theory.md, tasks.md, instructor_notes.md, and lesson_config.json.
Keep the language clear and student-friendly.
```

---

## Suggested Commit Strategy

Use small, meaningful commits.

Examples:

```text
chore: initialize uv python project
chore: add ruff and pytest configuration
feat: add pygame launcher skeleton
feat: implement reusable csv logger
feat: add reaction time lab prototype
test: add csv logger tests
docs: add lesson structure documentation
docs: add first reaction time lesson materials
```

---

## Suggested Branch Strategy

Recommended branches:

```text
main
feature/project-setup
feature/pygame-launcher
feature/reaction-time-lab
feature/stroop-challenge
feature/lesson-materials
feature/data-analysis-utils
```

Each feature branch should be small enough to review comfortably.

---

## Pull Request Template

Recommended `.github/pull_request_template.md`:

```markdown
## Summary

Describe what this PR changes.

## Scope

- [ ] Code
- [ ] Lesson materials
- [ ] Data
- [ ] Tests
- [ ] Documentation

## Validation

Commands run:

- [ ] `uv run pytest`
- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`

## Screenshots or Demo

Add screenshots or short notes if this PR changes a Pygame screen.

## Notes

Mention limitations, follow-up tasks, or design decisions.
```

---

## Initial Development Checklist

* [ ] Create repository.
* [ ] Add README.md.
* [ ] Add MIT license for code.
* [ ] Add content license file.
* [ ] Initialize uv project.
* [ ] Add package structure.
* [ ] Add Pygame dependency.
* [ ] Add Pandas, NumPy, Matplotlib.
* [ ] Add pytest and Ruff.
* [ ] Create Pygame launcher.
* [ ] Create placeholder lesson menu.
* [ ] Add CSV logging utility.
* [ ] Add Reaction Time Lab.
* [ ] Add Stroop Challenge.
* [ ] Add first lesson materials.
* [ ] Add generated data policy.
* [ ] Add tests.
* [ ] Add GitHub Actions CI.

---

## Long-Term Vision

The long-term goal is to create a complete, interactive, open educational repository for teaching Big Data through the lens of Cognitive Science.

The repository should eventually support:

* 30 structured lessons,
* multiple cognitive mini-games,
* local behavioral data collection,
* reproducible analysis scripts,
* optional notebooks,
* synthetic and open datasets,
* teacher notes,
* student project templates,
* final project examples,
* classroom-friendly setup instructions.

The ideal student experience:

> I play a cognitive task, generate my own data, analyze it with Python, compare it with others, discover patterns, question the interpretation, and understand why data about humans must be handled carefully.

---

## Working Title

Current working title:

```text
Cognitive Data Arcade
```

Alternative names:

```text
Cog Big Data Lab
Mind Data Playground
Cognitive Data Playground
Human Data Arcade
```

The preferred name is **Cognitive Data Arcade**, because it clearly communicates the combination of cognitive science, data analysis, and interactive mini-games.
