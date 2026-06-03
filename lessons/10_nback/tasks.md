# Tasks — Working Memory: N-Back Memory Grid

Complete the following steps during the lesson. Record your data in a notebook or shared document as directed by your instructor.

## Step 1: Launch the application

Open a terminal in the project directory and run:

```
uv run cognitive-data-arcade
```

## Step 2: Open Lesson 10

Navigate to **Lesson 10 — N-Back Memory Grid** using the arrow keys and press **ENTER**.

Read the introduction slides to understand the task rules before starting. Pay particular attention to the explanation of what "matching n steps ago" means in practice.

## Step 3: Play at 1-Back

Select **1-Back** from the session menu. Complete one full session.

Rules:
- A stimulus appears in a grid position (and/or a letter is shown or spoken).
- Press **SPACE** (or the designated match key) if the current stimulus matches the one from **1 step ago**.
- Do nothing if it does not match.

At the end of the session, note the following values from the results screen:

| Metric (1-Back) | Your value |
|---|---|
| Total match trials (Go) | |
| Total non-match trials (No-Go) | |
| Correct matches (hits) | |
| Missed matches (misses) | |
| Incorrect matches (false alarms) | |
| Correct non-matches (correct rejections) | |
| Mean RT on match trials (ms) | |

## Step 4: Play at 2-Back

Return to the session menu and select **2-Back**. Complete one full session. Record the same metrics as in Step 3 in a second row.

| Metric (2-Back) | Your value |
|---|---|
| Total match trials | |
| Total non-match trials | |
| Correct matches (hits) | |
| Missed matches (misses) | |
| Incorrect matches (false alarms) | |
| Correct non-matches (correct rejections) | |
| Mean RT on match trials (ms) | |

## Step 5: Calculate d' for 1-Back and 2-Back

For each level, compute:

```
Hit rate = Correct matches / Total match trials
False alarm rate = False alarms / Total non-match trials
d' = Z(hit rate) - Z(false alarm rate)
```

Use the z-score table in theory.md. Fill in the comparison table:

| N level | Hit rate | FA rate | d' |
|---|---|---|---|
| 1-Back | | | |
| 2-Back | | | |

How did d' change from 1-Back to 2-Back? By how much?

## Step 6: Play Adaptive mode

Select **Adaptive** from the session menu. Play at least two consecutive sessions without closing the application between them.

The system adjusts n dynamically based on your accuracy:
- If your accuracy exceeds ~85%, n increases by 1.
- If your accuracy falls below ~65%, n decreases by 1.
- Target is approximately 75% accuracy.

Record:
- Starting n level at the beginning of session 1
- Final n level at the end of session 1
- Final n level at the end of session 2
- Did n go up, down, or stay stable?

## Step 7: Reflection questions

Write brief answers to the following — these may be used for the group discussion:

1. At which n level did performance feel qualitatively different (not just harder, but a different kind of task)? Can you describe what changed?
2. Did your hit rate or false alarm rate change more between 1-Back and 2-Back? What does this suggest about which type of error becomes harder to control at higher n?
3. After two Adaptive sessions, at what n level did the system stabilise? Do you think this reflects your true WM capacity or is it influenced by other factors (fatigue, familiarity with the task, motivation)?
4. If a researcher claimed that playing 30 minutes of n-back daily for 4 weeks would raise your IQ by 5 points, what would you need to see before believing this claim? List at least three specific methodological requirements.
5. Compare your mean RT on match trials in 1-Back versus 2-Back. Why is RT slower at 2-Back even on correct trials?

## Discussion Questions

Bring your d' values and Adaptive session levels to the group discussion:

1. **What is working memory, and why is it different from "just having a good memory"?** Use Baddeley's model to answer.
2. **The Jaeggi (2008) claim: why did it fail to replicate?** What methodological factors explain the discrepancy between the original result and subsequent meta-analyses?
3. **Individual differences:** Did different students in your group stabilise at different Adaptive levels? What factors (other than WM capacity) might account for the variation?
