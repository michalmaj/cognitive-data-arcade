# Cognitive Data Arcade

[![CI](https://github.com/michalmaj/cognitive-data-arcade/actions/workflows/ci.yml/badge.svg)](https://github.com/michalmaj/cognitive-data-arcade/actions/workflows/ci.yml)

Interactive mini-games that teach **Big Data, Data Science, and Machine Learning through Cognitive Science**. Students don't just analyse data — they generate it by playing behavioural tasks, then inspect, clean, model, and interpret their own results.

```
game → data → analysis → interpretation → reflection
```

## Download

Pre-built binaries for Windows, macOS, and Linux — no Python required:

**[→ Latest release](https://github.com/michalmaj/cognitive-data-arcade/releases/latest)**

See [SETUP.md](SETUP.md) for installation instructions.

## Quick start (from source)

```bash
uv sync
uv run cognitive-data-arcade
```

Requires Python 3.12+, a display, and no other setup.

## Game status

31 games across 6 modules. Status as a course element — not just whether the code runs.

| # | Game | Topic / concept | Gameplay | Data logging | Analysis | Student material | Tests | Notes |
|--:|------|-----------------|:--------:|:------------:|:--------:|:----------------:|:-----:|-------|
| 1 | Big Data in Cognitive Science | Big data, behaviour at scale | ✅ | ⚪ | ⚪ | ✅ | ✅ | Concept network |
| 2 | Reaction Time Lab | RT measurement | ✅ | ✅ | ✅ | ✅ | ✅ | CSV + analysis scene |
| 3 | Event Log Detective | Event logs, data formats | ✅ | ⚪ | ⚪ | ✅ | ✅ | Puzzle levels |
| 4 | Data Quality Lab | Data cleaning, outliers | ✅ | ⚪ | ⚪ | ✅ | ✅ | Interactive table |
| 5 | EDA Sandbox | Exploratory data analysis | ✅ | ⚪ | ⚪ | ✅ | ✅ | Parameter simulation |
| 6 | Stroop Challenge | Cognitive interference | ✅ | ✅ | ✅ | ✅ | ✅ | CSV + analysis scene |
| 7 | Flanker Arena | Attention control | ✅ | ✅ | ✅ | ✅ | ✅ | CSV + analysis scene |
| 8 | Go/No-Go Guard | Response inhibition | ✅ | ✅ | ✅ | ✅ | ✅ | CSV + analysis scene |
| 9 | N-Back Memory Grid | Working memory | ✅ | ✅ | ✅ | ✅ | ✅ | CSV + analysis scene |
| 10 | Visual Search Lab | Visual attention | ✅ | ✅ | ✅ | ✅ | ✅ | CSV + analysis scene |
| 11 | Cognitive Dashboard | Performance aggregation | ✅ | ⚪ | ✅ | ✅ | ✅ | Reads prior sessions |
| 12 | Distribution Playground | Probability distributions | ✅ | ⚪ | ⚪ | ✅ | ✅ | 3-phase sandbox |
| 13 | Correlation Trap | Correlation vs. causation | ✅ | ⚪ | ⚪ | ✅ | ✅ | 3-phase explorer |
| 14 | Hypothesis Arena | Statistical testing | ✅ | ⚪ | ⚪ | ✅ | ✅ | 3-phase sandbox |
| 15 | Prediction Slider | Regression, forecasting | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 16 | Feature Hunter | Feature selection | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 17 | Classifier Battle | Classification | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 18 | Overfitting Monster | Overfitting, validation | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 19 | Anomaly Alert | Anomaly detection | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 20 | Text Tokenizer | NLP tokenisation | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 21 | Word Weight Factory | TF-IDF | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 22 | Emotion Classifier | Sentiment analysis | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 23 | Semantic Space Explorer | Word embeddings | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 24 | Topic Detective | Topic modelling (LDA) | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 25 | Human vs Model | Human–AI comparison | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 26 | Social Network Simulator | Network dynamics, SIR | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 27 | Misinformation Spread | Information virality | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 28 | Recommendation Bubble | Filter bubbles | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 29 | Bias Blind Spot | Algorithmic bias | ✅ | ⚪ | ⚪ | ✅ | ✅ | |
| 30 | The Architect's Trial | Research design, ethics | ✅ | ⚪ | ⚪ | ✅ | ✅ | Final narrative challenge |
| 31 | You Were the Dataset | Personal data reflection | ✅ | ⚪ | ✅ | ✅ | ✅ | Reads all prior sessions |

**Legend:** ✅ Ready · 🟡 Partial · ❌ Missing · ⚪ N/A (not applicable by design)

## Development

```bash
uv run pytest          # 1188 tests
uv run ruff check .    # lint
uv run ruff format .   # format
```

CI runs on every push and pull request (GitHub Actions).

## Stack

Python 3.12 · Pygame · Pandas · NumPy · Matplotlib · scikit-learn · uv · Ruff · pytest
