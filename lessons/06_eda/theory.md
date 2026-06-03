# Theory — Exploratory Data Analysis

## 1. What Is EDA and Where Did It Come From?

**Exploratory Data Analysis (EDA)** is the practice of summarizing and visualizing a dataset to understand its structure *before* specifying and testing a formal statistical model. The term was introduced by the American mathematician and statistician **John Tukey** in his 1977 book of the same name, which remains one of the most influential methodological texts in quantitative science.

Tukey's central argument was that statistical analysis typically begins at the wrong end. Researchers collect data, immediately compute a test statistic, and report a p-value — without ever looking at the raw numbers. This workflow makes it easy to miss anomalies, misinterpret patterns, and draw conclusions from artefacts rather than signal.

EDA inverts the order: look first, model second. The goals are:

1. **Detect anomalies** — outliers, impossible values, floor and ceiling effects that signal data quality issues.
2. **Understand the distribution** — is it symmetric? Skewed? Bimodal? The shape of the distribution determines which inferential tests are appropriate.
3. **Identify relationships** — are two variables correlated? Is the relationship linear or curved? Are there subgroups behaving differently?
4. **Generate hypotheses** — EDA produces candidate hypotheses for confirmatory analysis. It does not test them.

The last point is critical. Hypotheses suggested by the data cannot be properly tested with the same data. EDA is, by design, hypothesis-generating, not hypothesis-confirming. The confirmatory stage requires either a separate dataset or, ideally, pre-registration of hypotheses before data collection (Simmons et al., 2011).

## 2. Descriptive Statistics for RT Data

The first quantitative step in any EDA is computing **descriptive statistics**: numbers that summarize the distribution's shape, location, and spread.

### 2.1 Central Tendency

- **Mean (arithmetic average):** Sensitive to extreme values. Appropriate for symmetric distributions. For right-skewed RT data, the mean exceeds the median and overestimates where most responses fall.
- **Median (50th percentile):** The value that splits the distribution in half. Robust to outliers. Recommended as the primary summary for RT data.
- **Mode:** The most frequent value. Rarely reported for continuous data, but the concept maps to the peak of a kernel density estimate.

### 2.2 Spread

- **Standard deviation (SD):** The average distance of observations from the mean. Sensitive to outliers (because it uses the mean). For RT data, SD is typically 100–250 ms within a single condition.
- **Interquartile range (IQR = Q3 − Q1):** The range containing the middle 50 % of observations. Robust to outliers. Less sensitive to the heavy tail that characterizes RT distributions.
- **Range (max − min):** Maximum sensitivity to extreme values. Useful only for flagging implausible bounds.

### 2.3 Shape

- **Skewness:** A measure of asymmetry. Positive skewness means a right-extended tail (mean > median). RT distributions are almost universally **positively skewed** due to the hard lower bound at ~100 ms and the open-ended upper tail.
  - Skewness ≈ 0: approximately symmetric
  - Skewness > 1: markedly right-skewed (common for raw RT)
  - Skewness < −1: markedly left-skewed (rare for RT)
- **Kurtosis:** A measure of tail weight relative to a normal distribution. High kurtosis (leptokurtic) means a sharper peak and heavier tails. RT distributions often have excess kurtosis (kurtosis > 3 using the Pearson convention), reflecting the concentration of most responses near the mode and a non-negligible proportion of very slow responses.

A normal distribution has skewness = 0 and kurtosis = 3 (excess kurtosis = 0). RT data virtually never meets these criteria, which means that any statistical test assuming normality is technically violated for raw RT. Log-transformation or ex-Gaussian modelling are common remedies.

| Statistic | Sensitive to outliers? | Appropriate for RT? |
|---|---|---|
| Mean | Yes | Use alongside median |
| Median | No | Primary summary |
| SD | Yes | Report, but interpret cautiously |
| IQR | No | Recommended |
| Skewness | Yes | Always report for RT |
| Kurtosis | Yes | Report for shape description |

## 3. Visualizations for RT Data

Each visualization reveals a different aspect of the data. No single plot is sufficient.

### 3.1 Histogram

A histogram groups observations into bins and counts how many fall in each bin. It shows the **full shape** of the distribution: location, spread, skewness, modality (one peak or two), and the presence of outliers in the tails.

**When to use:** As the first visualization of any new variable. Always plot the RT histogram before computing a mean.

**Limitations:** Bin width matters enormously. Too wide: detail is lost. Too narrow: sampling noise dominates. Rule of thumb: start with Sturges' rule (k = 1 + log₂ n) and adjust visually.

### 3.2 Box Plot

A box plot (box-and-whisker plot) shows:
- The **median** as a horizontal line inside the box
- The **IQR** as the box height (Q1 to Q3)
- **Whiskers** extending to 1.5·IQR beyond the box edges
- **Outlier points** beyond the whiskers

Box plots are ideal for **comparing distributions across conditions** on the same axis. A single glance reveals differences in median, spread, and outlier frequency.

**Limitations:** Box plots compress all information about the distribution's shape into five numbers. Two distributions can have identical box plots but look completely different as histograms (e.g., bimodal vs. uniform).

### 3.3 Violin Plot

A violin plot combines the box plot's summary statistics with a **kernel density estimate** (KDE) of the full distribution, mirrored symmetrically. The wider the violin at any point, the more observations fall near that value.

**When to use:** When the shape of the distribution matters — for example, to detect whether the RT distribution is unimodal or whether there is a secondary mode at high RTs (possibly reflecting a lapse sub-distribution). Violin plots make the Stroop effect visible not just as a shift in median but as a shift in the entire distribution.

### 3.4 Q-Q Plot (Quantile-Quantile Plot)

A Q-Q plot compares the quantiles of the observed distribution against the quantiles of a theoretical distribution (usually the normal). If the data are normally distributed, the points fall on a straight diagonal line. Deviations from the line reveal:
- **Curved upward:** right skew (typical for RT)
- **Curved downward:** left skew
- **S-shaped:** heavy tails (excess kurtosis)

**Why it matters for RT:** Any parametric test that assumes normality (e.g., paired t-test) is technically invalid for raw RT data. The Q-Q plot makes this violation visible. Researchers should either use a transformation (log-RT), a non-parametric test, or a distribution-specific model (ex-Gaussian).

### 3.5 Scatter Plot

A scatter plot displays two variables as points in a 2D space, revealing the relationship between them. Before computing any correlation coefficient, **always plot the scatter plot** — this is the core lesson of Anscombe's Quartet (see Section 4).

**For RT data:** Scatter plots are used to examine practice effects (RT vs. trial number), speed-accuracy tradeoffs (RT vs. accuracy per block), and individual differences (participant mean RT vs. some covariate).

## 4. Anscombe's Quartet: Why Visualisation Is Not Optional

In 1973, the statistician Francis Anscombe published a paper demonstrating four datasets that are statistically identical on every standard summary measure yet look completely different when plotted:

| Dataset | Mean X | Mean Y | SD X | SD Y | Pearson r |
|---|---|---|---|---|---|
| I | 9.00 | 7.50 | 3.32 | 2.03 | 0.816 |
| II | 9.00 | 7.50 | 3.32 | 2.03 | 0.816 |
| III | 9.00 | 7.50 | 3.32 | 2.03 | 0.816 |
| IV | 9.00 | 7.50 | 3.32 | 2.03 | 0.817 |

Dataset I is approximately linear with mild noise. Dataset II follows a perfect curve — a linear model is wrong. Dataset III is a perfect line with one outlier inflating the correlation. Dataset IV consists of a vertical stack of identical X-values plus one extreme outlier that drives the entire correlation.

**The lesson is unambiguous:** A correlation coefficient of r = 0.82 does not tell you whether the relationship is linear, whether there are outliers, or whether the model is appropriate. A scatter plot tells you all of this in seconds. Reporting a correlation without a scatter plot is incomplete and potentially misleading.

This principle extends to every summary statistic. Descriptive statistics describe only what you measure; they conceal everything else.

## 5. The EDA Workflow for Cognitive Science Data

The following sequence should be applied to any new dataset before running inferential tests:

1. **Load and inspect:** `df.shape`, `df.dtypes`, `df.head()`, `df.tail()`. Confirm that the number of rows matches expectations, column types are correct, and no unexpected values appear in the first/last rows.

2. **Check for missing values:** `df.isna().sum()`. Cross-reference with Lesson 05 criteria (RT < 100 ms, RT > 3 000 ms, timeout trials).

3. **Compute `describe()`:** `df.describe()` returns count, mean, SD, min, Q1, median, Q3, max for all numeric columns. Read these carefully: the min and max alone often reveal data quality issues.

4. **Plot distributions per condition:** Plot a histogram (or violin plot) of RT separately for each experimental condition (congruent, neutral, incongruent for Stroop). Look for differences in shape, not just location.

5. **Plot condition means with error bars:** Compute the mean (or median) RT per condition with 95 % confidence intervals. This is the standard result plot — but it should be the *last* step, after the full distribution has been inspected.

6. **Plot RT over trial order:** Check for practice effects (RT decreasing over time) and fatigue effects (RT increasing late in the session). A simple scatter plot of RT vs. trial number reveals these.

7. **Examine individual differences:** If the dataset contains multiple participants, check whether the group-level pattern holds within each individual. Group means can mask heterogeneity.

Only after completing these steps should you form a specific hypothesis for confirmatory testing.

## 6. Condition Comparisons and Effect Size

The ultimate EDA goal in a Stroop paradigm is to determine whether the RT distributions in the three conditions are meaningfully different.

### 6.1 Overlapping Distributions

If the incongruent and congruent RT distributions overlap almost completely, the Stroop effect may be small or the variability may be high. Plotting both distributions as overlapping histograms or violin plots immediately reveals this. If the distributions are well-separated, the effect is large and likely reliable.

### 6.2 Cohen's d

After EDA, the first number to compute is not a p-value but an **effect size**. Cohen's d expresses the difference between two means in units of the pooled standard deviation:

> d = (M₁ − M₂) / SD_pooled

Conventional benchmarks (Cohen, 1988):

| d | Interpretation |
|---|---|
| 0.2 | Small |
| 0.5 | Medium |
| 0.8 | Large |

For within-subjects designs (which Stroop paradigms typically are), Cohen's d_z — using the standard deviation of the *difference scores* — is the appropriate variant.

Effect size is critical because, with a large enough sample, even a trivially small difference (d = 0.05, equivalent to 3 ms in a 600 ms baseline) will be statistically significant. Statistical significance answers "is the effect non-zero?"; effect size answers "is it worth caring about?". EDA cannot answer the first question but can definitively inform the second.

## References

- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- Anscombe, F. J. (1973). Graphs in statistical analysis. *The American Statistician, 27*(1), 17–21.
- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant. *Psychological Science, 22*(11), 1359–1366.
- Wickham, H. (2016). *ggplot2: Elegant Graphics for Data Analysis* (2nd ed.). Springer.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum.
