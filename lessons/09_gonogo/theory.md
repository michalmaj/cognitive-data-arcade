# Theory — Response Inhibition and the Go/No-Go Paradigm

## 1. Historical Background

The scientific measurement of response inhibition has roots in one of the oldest experiments in cognitive psychology. **Franciscus Donders** (1868) described his "C-reaction" — a condition in which a participant had to respond to one of two stimuli and withhold a response to the other. Donders noticed that this selective response required more time than a simple reaction, and he attributed the difference to the time required for stimulus discrimination and response selection. This was the conceptual ancestor of the modern Go/No-Go task.

The Go/No-Go paradigm was formalised as a laboratory measure of **response inhibition** during the 1970s and became widely used in neuropsychology during the 1980s and 1990s. It is now one of the most frequently used tasks in cognitive neuroscience, clinical neuropsychology, and developmental research. Its appeal lies in its simplicity: one button, two stimulus types, a clear measure of the failure to inhibit (the commission error).

## 2. Task Structure

In each trial of the Go/No-Go task, a single stimulus appears on screen. The participant must:

- Press a key **as fast as possible** when a Go stimulus appears (e.g., a green circle, a letter X, an upward arrow).
- **Withhold** any key press when a No-Go stimulus appears (e.g., a red circle, a letter K, a downward arrow).

The cognitive challenge arises from the asymmetry between Go and No-Go trials. Because Go trials are more frequent (typically 70–80% of all trials), participants develop a **prepotent response** — a strong, habitual tendency to press the key whenever any stimulus appears. The No-Go stimulus must interrupt this automatic tendency at the moment it is most active.

This is why correct inhibition on No-Go trials is not simply the absence of movement. It is an active suppression of a motor response that has already been partially prepared. The neural and computational resources required for this suppression are the subject of decades of research.

## 3. Go Ratio and Prepotency

The **Go ratio** is the proportion of Go trials relative to total trials. It is the primary determinant of task difficulty:

| Go Ratio | No-Go Proportion | Prepotency | Typical Commission Error Rate |
|---|---|---|---|
| 50% | 50% | Low | ~5% |
| 70% | 30% | Moderate | ~8–12% |
| 75% | 25% | High | ~10–15% |
| 80% | 20% | Very high | ~15–20% |
| 90% | 10% | Extreme | ~25–35% |

In this application:
- **Easy:** 80% Go (higher number of trials in sequence, 1.2 s response window)
- **Medium:** 75% Go (standard, 1.0 s response window)
- **Hard:** 60% Go (less prepotency, but shorter response window 0.7 s; time pressure compensates)

A higher Go ratio increases prepotency and therefore increases commission errors. This is the operational definition of inhibitory load: the greater the automaticity of the Go response, the greater the cognitive work required to stop it.

## 4. Two Types of Error

The Go/No-Go task generates two distinct types of error, each measuring a different cognitive process:

**Commission errors (false alarms):** The participant presses the key on a No-Go trial. This is a failure of inhibitory control. It indicates that the prepotent Go response was initiated but not suppressed in time. Commission errors are the primary outcome measure of the task — they index the capacity for **response inhibition**.

**Omission errors (misses):** The participant fails to press the key on a Go trial. This is not a failure of inhibition but typically a failure of **sustained attention** — the participant was not alert enough to detect the Go stimulus within the response window, or responded too slowly. High miss rates usually indicate fatigue, inattention, or a highly conservative response strategy.

The distinction is clinically important. A participant with many commission errors but few misses is impulsive. A participant with few commission errors but many misses may be overcontrolling (excessively cautious) or inattentive.

## 5. Signal Detection Theory and d'

Raw accuracy and error counts are influenced by **response bias** — the participant's general tendency to press or not press, regardless of the stimulus. A participant who never presses the key will have zero commission errors but also many misses. A participant who always presses will have zero misses but many commission errors. Neither extreme is good performance — both reflect a failure to discriminate Go from No-Go.

**Signal Detection Theory (SDT)** provides a bias-free measure of discriminability: **d' (d-prime)**.

The formula is:

```
d' = Z(hit rate) - Z(false alarm rate)
```

Where:
- **Hit rate** = (number of Go trials with a response) / (total number of Go trials)
- **False alarm rate** = (number of No-Go trials with a response) / (total number of No-Go trials)
- **Z(p)** is the inverse of the normal cumulative distribution — the z-score corresponding to probability p

### Interpreting d'

| d' value | Interpretation |
|---|---|
| 0.0 | No discrimination — chance performance |
| 1.0 | Weak discrimination |
| 2.0 | Good discrimination (typical healthy adult) |
| 2.5–3.5 | Strong discrimination |
| > 4.0 | Near-perfect discrimination |

A worked example: suppose a participant responds on 92% of Go trials (hit rate = 0.92) and on 8% of No-Go trials (false alarm rate = 0.08). From a z-table: Z(0.92) ≈ 1.41, Z(0.08) ≈ −1.41. Therefore d' = 1.41 − (−1.41) = 2.82 — strong discrimination.

A simplified z-score table for common values:

| p | Z(p) |
|---|---|
| 0.01 | −2.33 |
| 0.05 | −1.64 |
| 0.10 | −1.28 |
| 0.20 | −0.84 |
| 0.30 | −0.52 |
| 0.40 | −0.25 |
| 0.50 | 0.00 |
| 0.60 | 0.25 |
| 0.70 | 0.52 |
| 0.80 | 0.84 |
| 0.90 | 1.28 |
| 0.95 | 1.64 |
| 0.99 | 2.33 |

**Note:** If hit rate = 1.00 or false alarm rate = 0.00, the z-score is undefined (infinite). In practice, researchers apply a correction: replace 0 with 0.5/(n) and replace 1 with (n − 0.5)/n, where n is the number of trials of that type (Macmillan & Creelman, 2005).

## 6. Neural Correlates of Inhibitory Control

Response inhibition is not a unitary process implemented in a single brain region. Multiple prefrontal and subcortical circuits contribute:

**Right inferior frontal gyrus (rIFG):** Considered the primary "brake" for motor responses. Lesions to the rIFG in humans (e.g., from stroke) produce elevated commission errors on Go/No-Go and Stop-Signal tasks. Transcranial magnetic stimulation (TMS) disruption of rIFG also impairs inhibitory performance in healthy participants (Aron & Poldrack, 2006).

**Right prefrontal cortex (rPFC) more broadly:** fMRI studies consistently show right-lateralised prefrontal activation during successful No-Go trials compared to Go trials.

**Subthalamic nucleus (STN):** A deep-brain structure in the basal ganglia. The "hyperdirect pathway" from rIFG to STN is thought to mediate rapid, global stopping of motor programs — a kind of emergency brake.

**ERP components:** The N2 component (a negative deflection ~200–300 ms after No-Go stimulus) is larger on No-Go than Go trials and reflects the inhibitory process. The P3 component (~300–500 ms) on No-Go trials reflects the outcome of inhibitory processing.

## 7. Developmental Changes in Inhibitory Control

Response inhibition shows a protracted developmental course. Children aged 6–8 have commission error rates of 30–40% even at standard Go ratios. Performance improves substantially between ages 8 and 12, and continues to improve — though more slowly — through adolescence and into young adulthood.

| Age group | Typical commission error rate (75% Go) |
|---|---|
| 6–8 years | 30–40% |
| 9–11 years | 20–28% |
| 12–14 years | 12–18% |
| 15–17 years | 8–12% |
| Young adults (18–25) | 5–12% |
| Older adults (60+) | 10–18% |

The late development of inhibitory control parallels the prolonged maturation of the prefrontal cortex, which is not fully myelinated until approximately age 25. Older adults show a partial return of elevated commission errors, consistent with age-related prefrontal decline.

## 8. Clinical Applications

The Go/No-Go task is a standard tool in clinical neuropsychology:

**ADHD:** Children and adults with ADHD show significantly elevated commission error rates and reduced d', reflecting impaired inhibitory control. The Go/No-Go task is included in the CANTAB (Cambridge Neuropsychological Test Automated Battery) and similar computerised assessment batteries. It has been used to monitor medication effects — methylphenidate (Ritalin) reliably reduces commission errors in ADHD populations (Heaton et al., 2004).

**Frontal lobe lesions:** Patients with damage to the prefrontal cortex — from stroke, tumour, or traumatic brain injury — show elevated commission errors even when general intelligence and reaction time are unimpaired. The Go/No-Go task thus provides a specific measure of frontal executive function beyond general processing speed.

**Substance use and impulsivity:** Go/No-Go performance correlates with self-reported impulsivity and with risk-taking behaviour. Participants who score high on trait impulsivity measures (e.g., the Barratt Impulsiveness Scale) tend to have higher commission error rates.

## 9. The Stop-Signal Task: A Related Paradigm

The **Stop-Signal Task (SST)** is closely related to the Go/No-Go task but measures a conceptually distinct process:

In the SST, every trial begins as a Go trial — the participant prepares and begins to execute a response. On a subset of trials, a **stop signal** (a beep, a flash) occurs shortly after the Go stimulus. The participant must cancel the response that is already in progress. The delay between Go and Stop signals is varied so that stopping succeeds approximately 50% of the time.

From SST data, researchers estimate the **Stop-Signal Reaction Time (SSRT)** — the latency of the covert stopping process. The theoretical framework is the **horse-race model** (Logan & Cowan, 1984): the Go process and the Stop process race against each other; the one that finishes first determines the outcome.

| Feature | Go/No-Go | Stop-Signal Task |
|---|---|---|
| Response preparation | Partial | Full, already initiated |
| Stop signal timing | Simultaneous with stimulus | Delayed after Go stimulus |
| Primary measure | Commission error rate, d' | Stop-Signal Reaction Time (SSRT) |
| Type of inhibition | Proactive (anticipatory) | Reactive (after initiation) |

Both tasks recruit rIFG, but the SST more cleanly isolates the reactive stopping process (Verbruggen & Logan, 2008).

## 10. References

- Aron, A. R., & Poldrack, R. A. (2006). Cortical and subcortical contributions to stop signal response inhibition: role of the subthalamic nucleus. *Journal of Neuroscience, 26*(9), 2424–2433.
- Donders, F. C. (1868/1969). On the speed of mental processes. *Acta Psychologica, 30*, 412–431. (Translated by W. G. Koster)
- Heaton, S. C., Avila, M. T., Bailey, A. A., & Thaker, G. K. (2004). Specific working memory and executive function deficits in schizophrenia and related conditions. *Neuropsychology, 18*(4), 651–660.
- Logan, G. D., & Cowan, W. B. (1984). On the ability to inhibit thought and action: a theory of an act of control. *Psychological Review, 91*(3), 295–327.
- Macmillan, N. A., & Creelman, C. D. (2005). *Detection Theory: A User's Guide* (2nd ed.). Lawrence Erlbaum Associates.
- Verbruggen, F., & Logan, G. D. (2008). Response inhibition in the stop-signal paradigm. *Trends in Cognitive Sciences, 12*(11), 418–424.
