# Tasks — Missing Values and Outliers

Complete the following steps using a CSV file from a game session. Any session file works; Stroop files are recommended because they are produced automatically by the application.

## Step 1: Locate a game session file

Game session files are stored in `data/generated/`. Run the following to list available files:

```
ls data/generated/stroop/
```

If no files exist, play one session of the Stroop game (Lesson 07) and return.

## Step 2: Count timeout trials

Open Python (or a Jupyter notebook) and load the file:

```python
import pandas as pd

df = pd.read_csv("data/generated/stroop/YOUR_FILE.csv")
print(df.head())
print(df.columns.tolist())
```

Identify the column that indicates a timeout or missing response (it may be called `response`, `rt`, `timeout`, or similar). Count how many rows contain a timeout:

```python
# Adapt the condition to your actual column name
timeouts = df[df["response"].isna() | (df["rt"] == 0)]
print(f"Total trials: {len(df)}")
print(f"Timeout trials: {len(timeouts)}")
print(f"Proportion: {len(timeouts) / len(df):.1%}")
```

**Record:** How many timeouts? In which condition (congruent, neutral, incongruent) do they appear most often?

## Step 3: Calculate missing response proportion per condition

```python
condition_col = "condition"   # adapt if needed
response_col = "rt"

missing_per_condition = df.groupby(condition_col)[response_col].apply(
    lambda x: x.isna().mean()
)
print(missing_per_condition)
```

**Question:** Are timeout rates similar across conditions, or is one condition much worse? What does an unequal pattern tell you about the missingness mechanism (MCAR vs. MNAR)?

## Step 4: Compare mean and median RT

First, work with all rows (including outliers):

```python
valid = df[df["rt"].notna() & (df["rt"] > 0)]

print("=== Including all valid trials ===")
print(valid.groupby(condition_col)["rt"].agg(["mean", "median", "std"]))
```

**Record** the mean and median for each condition. Is the mean larger than the median? By how much? What does this gap tell you about the shape of the RT distribution?

## Step 5: Apply a z-score outlier rule

```python
from scipy import stats
import numpy as np

valid = valid.copy()
valid["z_rt"] = stats.zscore(valid["rt"])

before = len(valid)
clean = valid[valid["z_rt"].abs() <= 3]
after = len(clean)

print(f"Removed {before - after} trials ({(before - after) / before:.1%}) by z-score rule")
print("\n=== After z-score exclusion ===")
print(clean.groupby(condition_col)["rt"].agg(["mean", "median", "std"]))
```

**Compare** the means before and after exclusion. Did the Stroop effect (mean RT incongruent − mean RT congruent) change? By how much?

## Step 6: Apply a physiological boundary rule

```python
clean_phys = valid[(valid["rt"] >= 100) & (valid["rt"] <= 3000)]
removed = len(valid) - len(clean_phys)

print(f"Removed {removed} trials ({removed / len(valid):.1%}) by physiological boundary rule")
print("\n=== After physiological exclusion ===")
print(clean_phys.groupby(condition_col)["rt"].agg(["mean", "median", "std"]))
```

**Compare** to the z-score approach. Do the two methods agree on which trials to exclude? Which approach removes more trials? Which is better justified, and why?

## Discussion Questions

Discuss the following questions with your group or submit written answers:

1. In your dataset, are timeout trials distributed evenly across conditions? What does this imply about the missingness mechanism?
2. How much did the mean RT change when you applied the z-score exclusion? How much did the median change? Which statistic was more stable, and why?
3. A colleague argues: "I always delete any RT below 200 ms and above 2 000 ms — it works for my data." Evaluate this approach. Under what circumstances is it valid? What information is missing from this rule?
