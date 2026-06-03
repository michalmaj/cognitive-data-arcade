# Instructor Notes — Exploratory Data Analysis

## Timing Guide

| Activity | Time | Notes |
|---|---|---|
| Theory reading (self-paced) | 25–30 min | Assign before class if possible |
| Task exercises | 25–30 min | Demonstrate Step 1–3 live, then let students work |
| Discussion | 20 min | See question guidance below |
| **Total** | **~70–80 min** | |

## Pedagogical Purpose

EDA is a difficult topic to motivate for beginners because it looks like "just looking at the data." The key is to show that looking reveals things that numbers conceal.

**Recommended opening:** Before showing any theory, ask students: "You ran a Stroop experiment. Mean RT for incongruent is 620 ms and for congruent it is 540 ms. Is that a real difference?" Most students will say yes. Then show two scenarios:
- Scenario A: the distributions barely overlap — the difference is real.
- Scenario B: the SD in each condition is 400 ms and the distributions are nearly identical — the means differ because of three extreme outliers.

Both scenarios have exactly the same means. This motivates EDA.

## Discussion Question Guidance

**Question 1 — What does a histogram of RT tell you that the mean doesn't?**
Key points: the shape (skewness, bimodality), the spread, the presence and location of outliers, floor effects (many responses clustered near the minimum), ceiling effects (many responses near the upper bound). A mean of 580 ms could describe a tight unimodal distribution or a bimodal distribution with one cluster at 400 ms and another at 760 ms. You cannot distinguish these from the mean alone.

**Question 2 — Anscombe's Quartet: is this a real problem in cognitive science?**
Yes. The canonical example: two research groups each compute the correlation between working memory capacity and academic achievement as r = 0.45. Group A's scatter plot shows a clean linear relationship. Group B's scatter plot shows a curvilinear relationship — the correlation is driven by a ceiling effect at high working memory capacity. The same r, completely different implications. Encourage students to always plot before computing r.

**Question 3 — If your EDA reveals a pattern you did not pre-register, what should you do?**
This is the critical link to open science. A result that emerges from EDA is **exploratory** — it may be a real effect or it may be noise. The honest approach is to:
1. Report it as exploratory and clearly label it as such.
2. Collect new data to test the hypothesis in a pre-registered confirmatory study.
3. Do NOT reframe an exploratory finding as confirmatory after the fact (this is called HARKing — Hypothesizing After Results are Known).

## Common Misconceptions

- **"EDA is just computing descriptive statistics."** EDA is primarily visual. A table of means tells you almost nothing compared to the histogram, violin plot, and condition comparison plot together.
- **"The Q-Q plot passed, so the data are normal."** No test confirms normality; tests can only reject it. A Q-Q plot that looks approximately straight means the normality assumption is *not obviously violated* at this sample size — not that the data are normal. With small samples, non-normal distributions can produce straight Q-Q plots.
- **"My histogram looks bell-shaped, so t-test is fine."** RT distributions are not normal even when they look roughly bell-shaped. The right tail is always longer than the left. Log-transformation is recommended for parametric analyses.

## Connecting to Practice

The EDA workflow in Section 5 of the theory (load → missing → describe → distributions → condition comparison → time trends → individual differences) should be presented as a **repeatable checklist** that students apply to every new dataset. Consider creating a printed checklist card for the lab.

Link to Lesson 05: students who completed the missing-data cleaning tasks in Lesson 05 should have a cleaned CSV ready. This lesson's tasks work best on cleaned data. If they haven't done Lesson 05 yet, they will observe more extreme outliers in their histograms — which is itself a teaching opportunity.
