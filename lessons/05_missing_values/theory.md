# Theory — Missing Values and Outliers

## 1. Why Missing Data Is Not a Minor Inconvenience

Every empirical dataset contains gaps. A participant fails to respond in time; a sensor loses signal for three seconds; a questionnaire item is left blank. The temptation is to delete these rows and move on. But missing data are not random noise — they carry information about the data-generating process. The pattern of missingness, not just its quantity, determines how much damage it inflicts on statistical conclusions.

Donald Rubin (1976) formalized this insight by introducing a taxonomy of three missingness mechanisms that remains the standard reference for quantitative researchers across all empirical sciences.

## 2. Rubin's Taxonomy: MCAR, MAR, MNAR

### 2.1 Missing Completely At Random (MCAR)

A value is **MCAR** when the probability of it being missing is unrelated to any variable in the dataset — observed or unobserved. Formally, if *R* is the binary indicator of missingness and *Y* is the full data matrix:

> P(R | Y) = P(R)

In practice, MCAR is equivalent to saying that the missing rows are a simple random sample of all rows. If this holds, listwise deletion (removing all rows with any missing value) produces unbiased estimates. The only cost is reduced statistical power.

**Example:** A lab fire destroys a randomly selected 10 % of response sheets. The damage is purely physical and unrelated to participant behaviour. This is MCAR.

**How to test for MCAR:** Little's MCAR test (1988) compares the observed means of variables across patterns of missingness using a chi-square statistic. A non-significant result is consistent with (but does not prove) MCAR.

### 2.2 Missing At Random (MAR)

A value is **MAR** when the probability of missingness depends on *observed* variables, but not on the missing value itself. Formally:

> P(R | Y) = P(R | Y_obs)

The label is misleading: the data are not random in the everyday sense. The term means that missingness is explainable once you condition on what you can see.

**Example:** Older participants are more likely to skip the final questionnaire page (perhaps due to fatigue). Age is observed. If we control for age, the remaining missingness is unrelated to the questionnaire answers. This is MAR.

Under MAR, listwise deletion is biased, but maximum likelihood estimation and multiple imputation — both of which exploit the observed data structure — produce valid inferences (Schafer & Graham, 2002).

### 2.3 Missing Not At Random (MNAR)

A value is **MNAR** when the probability of missingness depends on the *missing value itself*, even after conditioning on all observed variables. Formally:

> P(R | Y) ≠ P(R | Y_obs)

This is the most dangerous mechanism because no purely statistical remedy exists. Bias can only be reduced by modelling the missingness process explicitly or by collecting additional data.

**Example:** A patient drops out of a clinical trial because their symptoms have worsened — the very outcome being measured is causing the dropout. This is MNAR.

### 2.4 Summary Table

| Mechanism | Missingness depends on | Listwise deletion | Imputation |
|---|---|---|---|
| MCAR | Nothing | Unbiased (power loss only) | Acceptable |
| MAR | Observed variables | Biased | Valid |
| MNAR | The missing value itself | Biased | Biased |

## 3. MCAR Is Rare in Cognitive Science

The MCAR assumption is rarely satisfied in behavioural and cognitive research. Consider the most common form of missing data in reaction-time (RT) paradigms: the **timeout trial**.

When a participant fails to respond within the response window (typically 2 000–3 000 ms), the trial is recorded as a timeout. Is this missing response unrelated to anything? No. Timeouts occur predominantly on **difficult** trials — incongruent Stroop items, high-load working memory probes, ambiguous stimuli. The missing RT is correlated with the latent difficulty of the trial, which is unobserved but real. This is textbook **MNAR**.

The consequence is serious: if you simply delete timeout trials and average the remaining RTs, your estimate of mean RT in the hard condition is biased *downward* — you have removed precisely the slowest responses. The measured Stroop effect shrinks artificially.

A similar logic applies to:
- **EEG artefact rejection:** Noisy epochs are more likely during blinks and movement, which co-occur with certain cognitive states.
- **Dropout in longitudinal studies:** Participants who leave a multi-week study are often those with the worst outcomes.
- **Self-report questionnaires:** Items about sensitive topics (drug use, depression severity) are more often skipped by those most affected.

## 4. Handling Missing Data

### 4.1 Listwise Deletion (Complete Case Analysis)

Delete all observations with any missing value. Simple and transparent. Valid only under MCAR. Under MAR or MNAR, it introduces bias proportional to the rate of missingness and the strength of the correlation between missingness and outcome.

**When acceptable:** Missingness rate is low (< 5 %), mechanism is plausibly MCAR, and a note is included in the methods section.

### 4.2 Mean and Median Imputation

Replace each missing value with the column mean (or median). Preserves the sample size but artificially reduces variability — the imputed distribution has a spike at the mean, compressing standard deviations and correlations. This produces overconfident (too narrow) confidence intervals.

**Verdict:** Discouraged for inferential analysis. Acceptable only for exploratory tables where distributional shape is not the object of inference.

### 4.3 Multiple Imputation (MI)

Multiple imputation (Rubin, 1987; van Buuren, 2018) generates *m* complete datasets by drawing plausible values from the posterior predictive distribution of the missing data given the observed data. Each dataset is analysed separately, and the results are pooled using Rubin's rules. This propagates the uncertainty about the missing values into the final estimate.

**Steps:**
1. Create *m* imputed datasets (typically *m* = 20–100 for high missingness rates).
2. Fit the model of interest on each dataset.
3. Pool parameter estimates: the point estimate is the mean across *m* estimates; the standard error incorporates both within-imputation and between-imputation variance.

**Valid under:** MAR (and, with sensitivity analysis, MNAR).

Software: `mice` (R), `IterativeImputer` (scikit-learn), Amelia II (R), fancyimpute (Python).

### 4.4 Model-Based Approaches

Full-information maximum likelihood (FIML) and Bayesian models use all available data by maximizing the likelihood over the observed data pattern, marginalizing over the missing values. These are theoretically equivalent to multiple imputation under MAR and are the default in many structural equation modelling packages.

## 5. Outliers: Two Definitions in Tension

An **outlier** is an observation that is extreme relative to the rest of the data. But "extreme" can mean two different things:

- **Statistical outlier:** An observation that falls far from the bulk of the distribution, typically defined as a z-score |z| > 3 or as a value beyond Q1 − 1.5·IQR or Q3 + 1.5·IQR (Tukey's fence).
- **Theoretical outlier:** An observation that is implausible given domain knowledge, regardless of its statistical distance from the sample mean.

These two definitions can conflict. A response time of 850 ms might be entirely normal for a Stroop task (no statistical outlier) but be the fastest a particular participant has ever responded, suggesting an anticipatory response. Conversely, a response of 2 800 ms may not exceed the z-score threshold in a sluggish participant, yet represent an attentional lapse.

**Domain knowledge must take precedence.** Statistics can flag candidates; only expertise can decide.

## 6. Outliers in Reaction-Time Data

RT distributions have well-established physiological constraints that define hard boundaries:

### 6.1 Lower Bound: Anticipatory Responses

The minimum time required for a visual stimulus to be detected, processed, and a motor response initiated is approximately **100 ms**. This reflects:
- ~40–60 ms for retinal transduction and early visual cortex processing
- ~20–40 ms for motor command transmission and muscle activation

Any response faster than 100 ms was produced *before* the stimulus could have been fully processed. These are **anticipatory responses** — the participant pressed the key in expectation, not reaction. They should be excluded regardless of condition.

### 6.2 Upper Bound: Attentional Lapses

There is no fixed upper bound, but responses slower than **3 000 ms** (and sometimes 2 000 ms in fast-paced tasks) typically reflect moments when the participant's attention was elsewhere — a sneeze, a phone notification, a moment of mind-wandering. These extreme values are better modelled as a mixture component (lapse process) than as genuine task performance.

Ratcliff (1993) analysed several trimming strategies and found that removing responses below 200 ms and above 3 000 ms, combined with a 2.5 % trimming from each tail of the remaining distribution, balances bias and efficiency for most RT paradigms.

### 6.3 Effect of Outliers on the Mean

RT distributions are **right-skewed**: there is a hard lower bound but an extended upper tail. In a right-skewed distribution, the mean exceeds the median, and a single extreme value can shift the mean substantially.

**Example calculation:**

| Trial | RT (ms) |
|---|---|
| 1 | 450 |
| 2 | 510 |
| 3 | 490 |
| 4 | 530 |
| 5 | 5 200 |

Mean without trial 5: 495 ms. Mean with trial 5: 1 236 ms. Median with trial 5: 510 ms.

The single 5 200 ms lapse inflates the mean by 741 ms — larger than any genuine Stroop effect. The median is unaffected.

| Statistic | Resistant to outliers? |
|---|---|
| Mean | No |
| Median | Yes |
| Trimmed mean (2.5 %) | Partially |
| Standard deviation | No |
| IQR | Yes |

### 6.4 The Trimmed Mean

The **trimmed mean** discards a fixed percentage of observations from each tail before averaging the remainder. A 10 % trimmed mean removes the lowest 10 % and highest 10 % of values. It is more resistant to outliers than the full mean and more efficient (uses more data) than the median.

Wilcox (2005) recommends the 20 % trimmed mean for RT data as a robust estimator that retains sensitivity to genuine treatment effects while suppressing lapse contamination.

## 7. Reporting Standards

The **APA Publication Manual** (7th ed.) and **CONSORT** (for clinical trials) both require explicit reporting of data exclusions. The key elements are:

1. **N excluded per criterion** — how many observations were removed at each step.
2. **Reason for exclusion** — the criterion used (e.g., RT < 100 ms, accuracy < 50 %).
3. **Condition breakdown** — were exclusions distributed evenly across conditions? Uneven exclusion rates can introduce bias.
4. **Missing data mechanism** — what mechanism was assumed (MCAR, MAR) and why.
5. **Method used** — listwise deletion, imputation method, software package.

A transparent report might read: *"Trials with RT < 100 ms (N = 12, 0.4 % of total) and RT > 3 000 ms (N = 8, 0.3 %) were excluded prior to analysis. An additional three participants (N = 186 trials, 6.2 %) were excluded due to overall accuracy below 60 %. Missing data were not imputed; complete-case analysis was used, which is valid under the assumption that exclusions were MCAR with respect to condition."*

## 8. Practical Checklist

Before submitting any analysis involving missing data or outlier removal:

- [ ] Report the total number of missing/excluded observations and the percentage of the total.
- [ ] Justify the exclusion criteria (cite a reference or provide a physiological rationale).
- [ ] Check whether exclusion rates differ across experimental conditions.
- [ ] State the assumed missingness mechanism and provide a justification or reference.
- [ ] Report results both with and without outlier exclusion as a sensitivity analysis.

## References

- Rubin, D. B. (1976). Inference and missing data. *Biometrika, 63*(3), 581–592.
- Schafer, J. L., & Graham, J. W. (2002). Missing data: Our view of the state of the art. *Psychological Methods, 7*(2), 147–177.
- Ratcliff, R. (1993). Methods for dealing with reaction time outliers. *Psychological Bulletin, 114*(3), 510–532.
- van Buuren, S. (2018). *Flexible Imputation of Missing Data* (2nd ed.). CRC Press. [Open access: https://stefvanbuuren.name/fimd/]
- Little, R. J. A. (1988). A test of missing completely at random for multivariate data with missing values. *Journal of the American Statistical Association, 83*(404), 1198–1202.
- Wilcox, R. R. (2005). *Introduction to Robust Estimation and Hypothesis Testing* (2nd ed.). Academic Press.
