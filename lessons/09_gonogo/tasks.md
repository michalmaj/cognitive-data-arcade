# Tasks — Response Inhibition: Go/No-Go Guard

Complete the following steps during the lesson. Record your data in a notebook or shared document as directed by your instructor.

## Step 1: Launch the application

Open a terminal in the project directory and run:

```
uv run cognitive-data-arcade
```

## Step 2: Open Lesson 09

Navigate to **Lesson 09 — Go/No-Go Guard** using the arrow keys and press **ENTER**.

Read the introduction slides (use the arrow keys or SPACE to advance). Pay attention to the distinction between Go and No-Go stimuli for the current session.

## Step 3: Play at Medium difficulty

Select **Standard session, Medium difficulty** from the session menu. This gives you approximately 80 trials with 75% Go stimuli and a 1.0-second response window.

- Press **SPACE** when you see the Go stimulus.
- Do **not** press anything when you see the No-Go stimulus.

At the end of the session, note down the following values shown on the results screen:

| Metric | Your value |
|---|---|
| Total Go trials | |
| Total No-Go trials | |
| Correct Go responses (hits) | |
| Missed Go responses (misses) | |
| No-Go responses (commission errors / false alarms) | |
| Correct No-Go suppressions (correct rejections) | |
| Mean RT on Go trials (ms) | |

## Step 4: Calculate hit rate and false alarm rate

Using your data from Step 3:

```
Hit rate = Correct Go responses / Total Go trials
False alarm rate = Commission errors / Total No-Go trials
```

Write both values as decimals (e.g., 0.88, not 88%).

## Step 5: Calculate d'

Use the z-score table in theory.md to look up Z(hit rate) and Z(false alarm rate).

```
d' = Z(hit rate) - Z(false alarm rate)
```

Record your d'. Compare with the interpretation table in theory.md — what does your d' indicate about your Go/No-Go discrimination?

## Step 6: Play at Hard difficulty

Return to the session menu and select **Hard difficulty** (60% Go, 0.7-second response window). Complete the full session.

After the session, record the same metrics as in Step 3. Calculate commission error rate (false alarm rate) and d' for this session.

**Comparison questions:**
- Did your commission error rate go up, down, or stay the same compared to Medium?
- Did your d' change? In which direction?
- Did your mean RT on Go trials change? Why might that happen?

## Step 7: Reflection questions

Write brief answers to the following — these may be used as the basis for the group discussion:

1. Were your commission errors spread evenly across the session, or did they cluster towards the end? What might this suggest about inhibitory fatigue?
2. If a classmate had a 90% hit rate and a 20% false alarm rate, and you had an 80% hit rate and a 5% false alarm rate — who has the higher d'? Calculate both and compare.
3. A patient with a frontal lobe lesion shows many commission errors but a normal RT on Go trials. What does this pattern tell us about the neural dissociation between response speed and response inhibition?
4. The Go/No-Go task and the Stroop task (if you have done Lesson 07) are both used to measure "executive function." Based on your experience with both, what is similar and what is different about the cognitive demands they place on you?

## Discussion Questions

Bring your calculated d' values and commission error rates to the group discussion:

1. **What distinguishes a commission error from an omission error?** Which one worries a clinician more in the context of ADHD, and why?
2. **Two students both get 85% accuracy. Can one be impulsive and the other inattentive?** Construct a concrete example using hit rates and false alarm rates.
3. **Why does response inhibition continue to develop until age 25?** What brain structure is involved and why does its maturation take so long?
