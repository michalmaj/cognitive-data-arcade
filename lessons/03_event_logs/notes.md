# Instructor Notes — Event Logs and Data Formats

## Timing Guide

| Activity | Time | Notes |
|---|---|---|
| Theory reading (self-paced) | 25–30 min | Assign before class; students who are unfamiliar with CSV should spend extra time on Section 3 |
| CSV inspection tasks | 15–20 min | Students open real game output files; see Tasks for step-by-step instructions |
| Observation recording | 5 min | |
| Discussion | 20–25 min | See question guidance below |
| **Total** | **~65–80 min** | No game in this lesson; adjust pacing accordingly |

## Expected Observations During Tasks

Students will open a CSV from `data/generated/`. The file should have eight standard columns. Most students will immediately recognise `response_time_ms` as RT, but some will confuse it with `stimulus_onset_ms`. Use this confusion productively: ask them what the difference between the two columns means conceptually.

Students doing the timestamp arithmetic task (Step 5 in Tasks) should find that consecutive `stimulus_onset_ms` values differ by the inter-trial interval. Across a full session, they can calculate the approximate session duration. This concretises the abstract idea of "millisecond-precision logging."

## Discussion Question Guidance

**Question 1 — Why does CSV not store the participant's age?**
Expected answers: age is session-level metadata, not trial-level data. It should be stored in a separate participants file and joined by `participant_id`. Key concept: the unit of analysis determines the unit of storage. This is a gentle introduction to relational data structure without using that term.

**Question 2 — If two computers have slightly different clocks, what happens to the RT measurement?**
Expected answers: the RT column itself is unaffected if RT is computed on a single computer (as elapsed time from stimulus onset to response on the same machine). The problem arises only when aligning data from two different recording systems (e.g., behavioural log and EEG). Surface the distinction between within-device RT (internally consistent) and cross-device alignment (requires synchronisation).

**Question 3 — Why does BIDS matter if you never share your data?**
Expected answers range from "it doesn't" to "it forces you to document your data in a way that future-you will understand." Push students toward the second answer. The strongest argument is that standardisation benefits the researcher themselves: a dataset you cannot re-analyse two years later has limited value.

## Common Misconceptions

- **"CSV is the best format because it opens in Excel."** True that readability is valuable. But ask: what happens to a 5 GB CSV in Excel? What about nested data (participant metadata + trial data)? Readability is one dimension of format quality, not the only one.
- **"Reaction time is already in the CSV, so timing precision doesn't matter."** RT in the CSV is the software-computed difference between two timestamps on the same machine. The concern is that the timestamp itself may be delayed by OS scheduling. A 10 ms polling interval means the logged RT could be up to 10 ms higher than the true RT.
- **"EDF is an old format and probably obsolete."** EDF dates to 1992 and is still the dominant EEG exchange format in clinical settings worldwide. Age does not equal obsolescence in data formats; adoption and ecosystem matter more than novelty.
- **"Open data means anyone can use it for anything."** OpenNeuro datasets are freely downloadable but carry licences. More importantly, re-identification of participants from neuroimaging data is a real risk; open sharing comes with ethical responsibilities.

## Connection to Following Lessons

Lesson 04 (Data Cleaning) follows directly. The CSV files students inspect in this lesson's tasks are the same files they will clean in Lesson 04. Encourage students to keep their notes from the CSV inspection task — they will be useful when computing exclusion rates.

The `stimulus_onset_ms` column, which often puzzles students in this lesson, becomes critical context for Lesson 04's discussion of why timeout trials (no response within the window) are fundamentally different from slow responses.
