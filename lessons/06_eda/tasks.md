# Tasks — Exploratory Data Analysis

Complete the following steps using a Stroop session CSV from `data/generated/stroop/`. If you have already cleaned the data in Lesson 05, use the cleaned version.

## Step 1: Load and inspect the dataset

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data/generated/stroop/YOUR_FILE.csv")

print("Shape:", df.shape)
print("\nColumn types:")
print(df.dtypes)
print("\nFirst 5 rows:")
print(df.head())
print("\nLast 5 rows:")
print(df.tail())
```

**Record:** How many rows and columns? Does the number of rows match the expected number of trials? Are there any columns with unexpected types?

## Step 2: Compute descriptive statistics

```python
print(df.describe())
```

Inspect the output carefully:
- Does the minimum RT look plausible (should be above 100 ms)?
- Does the maximum RT look plausible (should be below ~3 000 ms)?
- What is the mean RT overall?

Now compute condition-specific statistics:

```python
condition_col = "condition"   # adapt to your actual column name
rt_col = "rt"

stats = df.groupby(condition_col)[rt_col].agg(
    count="count",
    mean="mean",
    median="median",
    std="std",
    q25=lambda x: x.quantile(0.25),
    q75=lambda x: x.quantile(0.75),
    skewness=lambda x: x.skew(),
)
print(stats.round(1))
```

**Record:** Which condition has the highest mean? The highest median? Are mean and median similar, or does the mean exceed the median substantially? What does the skewness value tell you?

## Step 3: Plot the RT distribution

```python
import matplotlib.pyplot as plt

conditions = df[condition_col].unique()
fig, axes = plt.subplots(1, len(conditions), figsize=(12, 4), sharey=True)

for ax, cond in zip(axes, sorted(conditions)):
    data = df[df[condition_col] == cond][rt_col].dropna()
    ax.hist(data, bins=30, edgecolor="black", color="steelblue", alpha=0.7)
    ax.axvline(data.mean(), color="red", linestyle="--", label=f"Mean={data.mean():.0f}")
    ax.axvline(data.median(), color="green", linestyle="-", label=f"Median={data.median():.0f}")
    ax.set_title(cond)
    ax.set_xlabel("RT (ms)")
    ax.legend(fontsize=8)

axes[0].set_ylabel("Count")
plt.tight_layout()
plt.savefig("eda_histograms.png", dpi=150)
plt.show()
```

**Observe:** Is the distribution right-skewed (long right tail)? Is the mean (red dashed) to the right of the median (green solid)? Does the shape differ across conditions?

## Step 4: Plot a box plot and violin plot

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

# Box plot
df.boxplot(column=rt_col, by=condition_col, ax=axes[0])
axes[0].set_title("Box plot")
axes[0].set_xlabel("Condition")
axes[0].set_ylabel("RT (ms)")

# Violin plot (requires matplotlib >= 3.7 or seaborn)
try:
    import seaborn as sns
    sns.violinplot(data=df, x=condition_col, y=rt_col, ax=axes[1], inner="box")
    axes[1].set_title("Violin plot")
except ImportError:
    axes[1].text(0.5, 0.5, "Install seaborn for violin plot", ha="center", va="center")

plt.tight_layout()
plt.savefig("eda_boxviolin.png", dpi=150)
plt.show()
```

**Observe:** Are the medians in the expected order (congruent < neutral < incongruent)? Do the boxes overlap? Are there outlier points visible beyond the whiskers?

## Step 5: Check for normality with a Q-Q plot

```python
from scipy import stats

valid_rt = df[rt_col].dropna()
fig, ax = plt.subplots(figsize=(5, 5))
stats.probplot(valid_rt, dist="norm", plot=ax)
ax.set_title("Q-Q plot — all conditions combined")
plt.tight_layout()
plt.savefig("eda_qqplot.png", dpi=150)
plt.show()
```

**Observe:** Do the points fall on the diagonal line, or do they curve away from it in the upper right (which indicates right skew — the long RT tail)? What does this tell you about using a standard t-test on raw RT?

## Step 6: Compare conditions and compute the Stroop effect

```python
condition_means = df.groupby(condition_col)[rt_col].mean()
print("Condition means:")
print(condition_means.round(1))

if "incongruent" in condition_means and "congruent" in condition_means:
    stroop_effect = condition_means["incongruent"] - condition_means["congruent"]
    print(f"\nStroop effect (mean): {stroop_effect:.1f} ms")

condition_medians = df.groupby(condition_col)[rt_col].median()
if "incongruent" in condition_medians and "congruent" in condition_medians:
    stroop_median_effect = condition_medians["incongruent"] - condition_medians["congruent"]
    print(f"Stroop effect (median): {stroop_median_effect:.1f} ms")
```

**Compare:** Is the Stroop effect larger when computed from means or from medians? Which do you trust more, and why?

## Discussion Questions

1. Look at your histograms from Step 3. Is the RT distribution in the incongruent condition simply shifted to the right relative to congruent, or does it also have a different shape? What would it mean if the shape were different?
2. Your Q-Q plot showed a departure from normality. Does this mean you cannot analyse the data statistically? What alternatives exist?
3. Based on your EDA, formulate one specific, testable hypothesis about the Stroop effect in your data. Make sure the hypothesis is stated *before* you run any inferential test.
