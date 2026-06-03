# Instructor Notes — Missing Values and Outliers

## Timing Guide

| Activity | Time | Notes |
|---|---|---|
| Theory reading (self-paced) | 30–35 min | Assign before class if possible |
| Task exercises | 20–25 min | Pairs work well for the calculation steps |
| Discussion | 20 min | See question guidance below |
| **Total** | **~70–80 min** | |

## Core Concept to Reinforce

The single most important concept in this lesson is that **missingness is itself data**. Students raised on clean spreadsheet exercises often treat NaN cells as accidents to be swept away. The MNAR example — timeouts occurring on hard trials — should make the stakes concrete.

Use the following sequence:

1. Ask: "If a student doesn't answer question 7 on an exam, does that tell you something?"
2. Most students answer yes: it was probably hard, or the student ran out of time.
3. Now ask: "If you delete that question from your grade analysis, are you accurately representing what happened?"
4. This maps directly to timeout trials in the Stroop task.

## Discussion Question Guidance

**Question 1 — Is a Stroop timeout trial MCAR, MAR, or MNAR?**
Expected answer: MNAR. The timeout is most likely on incongruent trials, which are by definition more difficult. The missing RT is correlated with the difficulty of that specific trial — and difficulty is the unobserved variable we care about. Listwise deletion therefore underestimates the mean RT in the incongruent condition, artificially shrinking the Stroop effect.

**Question 2 — A response of 85 ms: is it an outlier?**
This is a trick question with a clear answer. 85 ms is physiologically impossible as a genuine reaction to a visual stimulus (minimum processing time is ~100 ms). The correct treatment is exclusion regardless of the z-score, regardless of the sample mean, regardless of whether it is statistically unusual. This demonstrates that domain knowledge overrides statistics.

**Question 3 — Should you always exclude outliers?**
No. The decision depends on the research question. If you are studying the full distribution of responses (including lapses), excluding outliers removes the phenomenon of interest. If you are estimating the mode of the RT distribution under optimal attention, excluding lapses is justified. The key is to state the criterion, justify it, and check whether exclusion rates differ across conditions.

## Common Misconceptions

- **"More data is always better, so never exclude anything."** Counter: including physiologically impossible values degrades the estimate of the quantity you actually want to measure. Inclusion decisions should be principled, not maximalist.
- **"Imputing with the mean is safe because it preserves the mean."** Counter: it preserves the group mean but systematically underestimates variance and covariance. For any analysis that uses standard errors, confidence intervals, or correlations, mean imputation introduces systematic distortion.
- **"If the p-value doesn't change much, the outlier wasn't important."** Counter: p-values are influenced by sample size. In large datasets, an outlier may not cross the significance threshold but may shift the effect size estimate substantially. Report effect sizes, not just p-values.

## Key Numbers to Remember

Provide these as a reference card or write on the board:

- RT < 100 ms → exclude (physiologically impossible)
- RT > 3 000 ms → typically exclude (attentional lapse)
- Missingness rate > 10 % → multiple imputation or model-based methods; justify any simpler approach
- Condition-specific exclusion rates differing by > 2–3 % → investigate before proceeding

## Connection to Following Lessons

Lesson 06 (EDA) builds directly on the cleaned dataset. Instructors should encourage students to complete the exclusion/cleaning steps in Lesson 05 Tasks *before* the EDA session, so that Lesson 06 can begin with analysis-ready data. The contrast between raw and cleaned histograms is one of the most visually effective demonstrations in the course.
