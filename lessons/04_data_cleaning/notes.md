# Instructor Notes — Data Cleaning

## Timing Guide

| Activity | Time | Notes |
|---|---|---|
| Theory reading (self-paced) | 25–30 min | Assign before class; emphasise Sections 3 and 6 (exclusion criteria and reproducible cleaning) |
| Task 1–3 (counting and finding outliers) | 15–20 min | Students work with the same CSV file from Lesson 03 |
| Task 4 (Python snippet) | 10 min | Optional; demonstrate live if most students lack Python experience |
| Discussion | 20–25 min | See question guidance below |
| **Total** | **~70–85 min** | |

## Expected Observations During Tasks

Students inspecting the CSV from a typical short game session (20–40 trials) may find zero outliers, which is an expected and valid outcome. If no outliers are found, guide students to reason about what the exclusion rate would be (0%) and what that implies (clean session, compliant participant). This is a useful contrast with the typical assumption that "cleaning always finds something."

For students who played an unusually long or inattentive session, slow trials above 2 000 ms may appear. These are the most instructive cases — ask those students to share their data with the class.

The Python snippet task is the most technically demanding. If the majority of students have no Python experience, run the code live as a demonstration, with students following along by reading the output rather than writing code themselves.

## Discussion Question Guidance

**Question 1 — Why can't you just delete outlier rows in Excel?**
Key points to surface: (1) the deletion is not recorded anywhere — you cannot reproduce what was deleted; (2) the raw file is modified permanently, and you cannot go back; (3) your script colleague cannot verify your work. The contrast with a documented Python script should be made explicit: the script is the audit trail.

**Question 2 — Is a timeout the same as a very slow response?**
Expected answer: no. A timeout means the participant did not respond within the window — this could mean they were distracted, confused about the task, or experienced a technical failure. A slow response (e.g., 1 800 ms) means they responded, just slowly. These carry different information about cognitive processing. Students sometimes conflate them because both are "bad" outcomes; push them to distinguish the mechanism.

**Question 3 — If pre-registration is so important, why don't all researchers do it?**
Expect a range of answers: lack of awareness, additional time cost, concern that reviewers will penalise exploratory work, cultural norms in some subfields. The important point is that pre-registration is not about distrusting researchers — it is about creating a paper trail that makes results more trustworthy to readers, including future replicators.

## Common Misconceptions

- **"Cleaning means removing all trials where the participant made an error."** Incorrect responses are valid data for accuracy analyses. Error trials should not be excluded from accuracy counts; they may be excluded from RT analyses (if the research question is about correct-response speed only), but this must be stated explicitly.
- **"The more you clean, the better your data."** Aggressive cleaning reduces variance and can artificially reduce the apparent RT distribution. Cleaning should be motivated by principled criteria, not by a desire to obtain cleaner-looking results.
- **"If you clean the same way as other people in your lab, you don't need to write it down."** Lab conventions are not public. A reader of a published paper has no access to lab conventions. Every paper needs its own cleaning report.
- **"Python is required for reproducible cleaning."** Any scripting language works: R, MATLAB, Julia. The essential requirement is that the pipeline is a script, not a manual sequence of clicks.

## Connection to Following Lessons

Lesson 05 onwards introduces inferential statistics on RT data. Before those lessons, students should understand that the numbers they feed into statistical tests are the output of cleaning decisions. A statistically significant Stroop effect is only meaningful if the analyst can demonstrate that the cleaning choices did not create or destroy the effect. This lesson is the foundation for that critical perspective.
