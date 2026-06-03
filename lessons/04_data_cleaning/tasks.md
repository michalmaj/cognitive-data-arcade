# Tasks — Data Cleaning

Complete the following steps during the lesson. Use the same CSV file you inspected in Lesson 03, or generate a new session file first (see Lesson 03, Step 1).

## Step 1: Count the trials

Open your CSV file and count the total number of data rows (excluding the header). This is your **N_total**.

- N_total: _______

## Step 2: Identify anticipations (RT < 100 ms)

Scan the `response_time_ms` column for values less than 100. In a spreadsheet application, you can use a filter (Data → Filter) to show only rows where `response_time_ms < 100`.

- Number of anticipation trials: _______
- If you found any: record the smallest RT value observed. _______ ms

## Step 3: Identify attentional lapses (RT > 2000 ms)

Apply a filter to show rows where `response_time_ms > 2000`.

- Number of lapse trials: _______
- If you found any: record the largest RT value observed. _______ ms

## Step 4: Identify timeouts (missing RT)

Apply a filter to show rows where `response_time_ms` is empty or contains `NA`/`NaN`.

- Number of timeout trials: _______

## Step 5: Calculate the exclusion rate

Fill in the table:

| Category | Count | % of N_total |
|---|---|---|
| Anticipations (< 100 ms) | | |
| Lapses (> 2000 ms) | | |
| Timeouts (no response) | | |
| **Total excluded** | | |
| **Included** | | |

Is your total exclusion rate above or below 5%? _______

## Step 6: Write a cleaning snippet in Python

Open a Python interpreter (or a new cell in a Jupyter notebook) and type the following. Replace `"your_file.csv"` with the actual path to your CSV:

```python
import pandas as pd

raw = pd.read_csv("your_file.csv")

mask_anticipation = raw["response_time_ms"] < 100
mask_lapse        = raw["response_time_ms"] > 2000
mask_timeout      = raw["response_time_ms"].isna()

excluded = raw[mask_anticipation | mask_lapse | mask_timeout]
cleaned  = raw[~(mask_anticipation | mask_lapse | mask_timeout)]

print(f"Total: {len(raw)} | Excluded: {len(excluded)} ({100*len(excluded)/len(raw):.1f}%) | Included: {len(cleaned)}")
```

Do the numbers match what you found manually in Steps 2–5?

## Discussion Questions

Discuss the following questions with your group or submit written answers as instructed:

1. **Why is it not acceptable to delete rows manually in Excel to clean a dataset?** What specifically is lost by doing it that way?
2. **Your exclusion rate is 0%. Is your data clean?** Explain what 0% exclusion rate tells you, and what it does not tell you.
3. **Imagine you found that 8% of trials are lapses in the incongruent condition, but only 1% in the congruent condition.** What does this asymmetry tell you, beyond the RT means? Should you report it?
