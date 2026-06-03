# Theory — Data Cleaning

## 1. Why Data Is Never Clean

Raw data is best understood as a **hypothesis** about what happened during an experiment. It is the product of hardware with finite precision, software with scheduling latency, participants who blink, scratch their nose, and occasionally press the wrong key, and experimenters who — despite their best intentions — sometimes mis-log a condition or leave a recording running during the break.

Cleaned data is your **best approximation** of what actually happened, constructed by applying explicit, pre-specified criteria to remove or flag observations that are implausible, impossible, or uninformative. The key word is *explicit*: every cleaning decision must be documented, because cleaning decisions are analytical decisions, and analytical decisions affect results.

The relationship between raw and cleaned data is not one of revelation — as if the "true" dataset were hidden inside the raw file waiting to be uncovered. It is one of modelling: different cleaning choices produce different datasets, and therefore different results. This is why pre-specifying cleaning criteria before looking at the data is an essential component of rigorous science.

## 2. Categories of Dirty Data

### Duplicate Rows

Hardware crashes mid-session and the experimenter restarts the recording can produce duplicate rows — the same trial_id appearing twice. Duplicates inflate the apparent sample size and bias estimates of RT distributions (because duplicated slow trials double their weight in a mean calculation). Detection: group by `trial_id` and count; any count > 1 indicates a duplicate.

### Impossible Values

Values that violate physical or logical constraints: a negative RT (`response_time_ms = -400`), a response timestamp before the stimulus (`response_time_ms = 0`), or a response key that is not in the set of valid response keys for the paradigm. These typically reflect software bugs, data corruption, or column mis-alignment during file export.

### Out-of-Range Values

Values that are technically possible but implausible given the experimental context: an RT of 50 000 ms (50 seconds) in a task that uses a 2 000 ms response window, or an RT of 15 ms in a task where the stimulus must be identified before any response can be formed. These are not errors in the strict sense — they represent real events — but they are not informative about the cognitive process under study.

### Encoding Errors

Characters or strings that should not appear in a given column: a response key recorded as `"\\n"` (a newline character that was accidentally logged), a condition label with a trailing space (`"go "` instead of `"go"`), or a Unicode replacement character where a letter should be. Encoding errors are particularly common when data from different operating systems or different programming languages are combined.

### Missing Entries

Rows where one or more cells are empty or contain a sentinel value (e.g., `NA`, `NaN`, `-1`). Missing response keys on trials where a response was expected indicate that the participant did not respond, but whether that is a timeout (response window expired) or a data-loss event must be determined from context.

### Timezone Ambiguity

Session-level timestamps that are not timezone-aware can become ambiguous when data from multiple sites is combined, or when a session spans a daylight-saving transition. This is rarely relevant for within-trial RT columns (which are relative, not absolute) but can corrupt session-ordering if analysts sort by session start time.

## 3. RT-Specific Exclusion Criteria

Reaction time distributions are right-skewed and bounded below by the irreducible minimum time for sensory processing and motor execution. Standard exclusion criteria reflect these biological constraints:

### Anticipations (RT < 100 ms)

A response occurring less than 100 ms after stimulus onset cannot have been produced by processing that stimulus. At 100 ms, light from the stimulus has barely completed its path through the visual system to primary visual cortex (V1), let alone been processed by downstream decision mechanisms. Responses this fast are **anticipatory**: the participant responded before processing was complete, either by guessing the response timing or by reacting to an unintended cue.

Including anticipatory responses in RT means would artificially lower means and inflate apparent speed. They should be excluded and counted separately (as a measure of task compliance and strategy).

### Attentional Lapses (RT > 2000–3000 ms)

Very slow responses — typically above 2 000 or 3 000 ms, depending on the paradigm — reflect attentional lapses: the participant was temporarily not engaged with the task. These responses are real, but they are not informative about the cognitive process under study (the mechanism of interest operates on a timescale of hundreds of milliseconds, not seconds). Including them inflates RT means and inflates variance.

The exact upper cutoff varies by paradigm and researcher convention. Ratcliff (1993) reviewed multiple trimming strategies; Ulrich and Miller (1994) showed that different trimming methods produce systematically different RT mean estimates, making the choice of cutoff a methodological decision that must be reported.

### Timeout Trials

Trials on which no response was recorded within the response window (e.g., `response_time_ms` is missing or flagged as timeout) are a distinct category. They are not slow responses — they are absent responses, and they carry different information:

- A high timeout rate may indicate task difficulty, participant confusion, or a poorly calibrated response window.
- Timeouts must be reported separately from the RT distribution.
- In accuracy analyses, timeouts are typically coded as incorrect, but they should be distinguished from commission errors (incorrect responses that were made).

### The Three-Category Rule

Every trial falls into exactly one of three categories: (1) valid response — included in RT analysis; (2) excluded response — response was made but excluded by pre-specified criteria; (3) absent response — no response was made (timeout). Conflating these categories produces uninterpretable results.

## 4. Documenting Cleaning Decisions

A **cleaning log** records every decision made during data cleaning:

- What criterion was applied
- How many trials were excluded by that criterion
- What percentage of all trials that represents
- In which conditions exclusions occurred (to detect condition-specific data quality problems)

The cleaning log is as scientifically important as the data file itself. A published result without a cleaning log cannot be independently verified, because a reader cannot know whether the reported effect depends on the cleaning choices made.

### Pre-Registration

**Pre-registration** means specifying the cleaning criteria — and all other analytical decisions — before collecting or analysing data, and depositing that specification in a time-stamped public record (e.g., on the Open Science Framework, osf.io). This separates confirmatory analyses (testing pre-specified hypotheses with pre-specified methods) from exploratory analyses (trying many cleaning approaches and reporting the one that produces the strongest result).

The distinction matters because with a typical RT dataset, varying the upper RT cutoff between 1 500 ms and 3 000 ms can meaningfully change the condition means and the statistical significance of comparisons. Without pre-registration, a researcher could — consciously or not — select the cutoff that produces the result they hoped for.

## 5. The 5–10% Rule of Thumb

If more than 5–10% of trials in a condition are excluded, the condition result is unreliable. This guideline does not come from a formal theorem but from accumulated empirical experience: at exclusion rates above 10%, the excluded trials are likely not a random sample of all trials, meaning the remaining included trials are a systematically biased subset of the intended measurement.

Exclusion rates should always be reported alongside the main results, per condition. A clean dataset with a 2% exclusion rate inspires more confidence than an identical mean RT derived from a dataset with 15% exclusion.

If exclusion rates differ substantially across conditions (e.g., 2% in the congruent condition vs. 12% in the incongruent condition), this difference is itself a finding: the incongruent condition produced qualitatively different behavioural engagement. Discarding this information by simply reporting the cleaned means would obscure an important result.

## 6. Reproducible Cleaning

A cleaning pipeline is reproducible if and only if it can be **re-run from the raw data** and produces the same cleaned output every time. This requires:

1. **A script** (Python, R, or other) that reads the raw CSV, applies all cleaning steps programmatically, and writes the cleaned CSV.
2. **No manual editing** of the raw CSV. Any manual change (deleting a row in Excel, correcting a typo by hand) is invisible to any version control system and cannot be reproduced by another researcher.
3. **Version-controlled scripts**. The cleaning script should be committed to the same repository as the data, so that any change to the cleaning logic is tracked with the same rigour as the data itself.

The Python `pandas` library provides the standard toolkit for programmatic RT data cleaning. A minimal cleaning pipeline might look like:

```python
import pandas as pd

raw = pd.read_csv("data/generated/session_001.csv")

# Exclusion 1: anticipations
mask_anticipation = raw["response_time_ms"] < 100

# Exclusion 2: lapses
mask_lapse = raw["response_time_ms"] > 2000

# Exclusion 3: timeouts (missing RT)
mask_timeout = raw["response_time_ms"].isna()

excluded = raw[mask_anticipation | mask_lapse | mask_timeout].copy()
cleaned  = raw[~(mask_anticipation | mask_lapse | mask_timeout)].copy()

print(f"Total trials: {len(raw)}")
print(f"Excluded: {len(excluded)} ({100*len(excluded)/len(raw):.1f}%)")
print(f"Included: {len(cleaned)}")

cleaned.to_csv("data/cleaned/session_001_clean.csv", index=False)
```

This script is the cleaning log: every exclusion criterion is explicit, every number is reproducible, and re-running it from the same raw input always produces the same cleaned output.

## 7. Historical Context: The Consequences of Uncleaned Data

### Ratcliff (1993)

Roger Ratcliff's 1993 paper "Methods for dealing with reaction time outliers" is the foundational reference for RT trimming methodology. Ratcliff showed that different outlier-exclusion strategies produce systematically different estimates of the underlying mean RT, and that some common practices (e.g., removing trials more than two standard deviations from the mean, computed on the full distribution) introduce bias because the mean and SD themselves are distorted by outliers. His recommendation: use fixed absolute cutoffs (e.g., 100 ms lower bound, 3 000 ms upper bound) rather than distribution-relative cutoffs computed from contaminated distributions.

### Ulrich and Miller (1994)

Rolf Ulrich and Jeff Miller extended Ratcliff's analysis to show that outlier trimming affects not just RT means but also the apparent size of experimental effects. An incongruent-minus-congruent Stroop effect measured on trimmed data can be substantially different from the effect measured on untrimmed data, even when both analyses are internally consistent. This confirms that the choice of trimming strategy is a methodological variable that must be pre-specified and reported.

### The Replication Crisis

A substantial fraction of the replication failures documented in the Open Science Collaboration's 2015 large-scale replication project (which failed to replicate 61% of cognitive and social psychology findings) involved flexible data analysis — the practice of making analytical decisions after seeing the data. Flexible cleaning criteria are one form of flexible analysis. BIDS, OSF pre-registration, and reproducible cleaning scripts are structural responses to this problem, making the "garden of forking paths" visible and auditable.

## References

- Ratcliff, R. (1993). Methods for dealing with reaction time outliers. *Psychological Bulletin*, 114(3), 510–532.
- Ulrich, R., & Miller, J. (1994). Effects of truncation on reaction time analysis. *Journal of Experimental Psychology: General*, 123(1), 34–80.
- Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.
- Open Science Framework: osf.io
- Gorgolewski, K. J., et al. (2016). The brain imaging data structure. *Scientific Data*, 3, 160044.
