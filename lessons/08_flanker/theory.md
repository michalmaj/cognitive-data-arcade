# Theory — The Flanker Effect

## 1. Historical Context

In 1974, Barbara A. Eriksen and Charles W. Eriksen published "Effects of noise letters upon the identification of a target letter in a nonsearch task" in *Perception & Psychophysics*. Their original experiment used letters, not arrows. Participants had to identify a central target letter (e.g., H or S) while ignoring flanking letters that were either compatible with the required response (e.g., HHHHH), incompatible (e.g., SSHSS), or neutral. The flanking letters reliably interfered with response selection even though participants were told they were irrelevant.

The paradigm was designed to answer a specific theoretical question: does selective attention operate at the level of individual stimuli, or does it operate over spatial regions? If attention is perfectly selective at the stimulus level, flankers should produce no interference. The finding that they do — demonstrating that attention spills over to spatially adjacent stimuli — became a cornerstone of modern attention research.

The arrow version used in computerised tasks (including Flanker Arena) was introduced for practical reasons: arrows have an unambiguous response mapping (left or right) without requiring letter-response learning, making the task accessible to broader populations including children and clinical groups.

## 2. The Task Structure

A flanker trial consists of a central target flanked by two stimuli on each side. Three conditions are standard:

| Condition | Stimulus | Typical RT (young adults) | Description |
|---|---|---|---|
| Congruent | -> -> -> -> -> | ~420 ms | Flankers point in the same direction as target |
| Neutral | -- -> -- | ~450 ms | Flankers carry no directional information |
| Incongruent | <- <- -> <- <- | ~470–500 ms | Flankers point in the opposite direction to target |

Note that the absolute RT values for the Flanker task are lower than for the Stroop task. This is because arrow-pressing is a simpler motor act than verbally naming a colour, and the flanker task allows faster responses overall. The critical measure is the difference, not the absolute values.

## 3. The Flanker Compatibility Effect

The primary measure of flanker interference is:

```
Flanker compatibility effect = RT(incongruent) - RT(congruent)
```

In healthy young adults this effect is typically **20–80 ms**. Note that this is substantially smaller than the typical Stroop interference effect (100–300 ms), reflecting the fact that reading automaticity is a stronger force than spatial response priming from flanking arrows.

A neutral condition can separate the effect into components analogous to the Stroop design:

```
Interference = RT(incongruent) - RT(neutral)
Facilitation = RT(neutral)     - RT(congruent)
```

For the flanker task, facilitation tends to be smaller relative to interference than in the Stroop task.

## 4. Why Flanker Interference Occurs: The Spotlight Model

Eriksen and St. James (1986) proposed the **attentional spotlight model**: visual attention has a limited focus that can be expanded or contracted, but cannot be perfectly zeroed in on a single point. When the display is presented, attention is directed toward the centre where the target appears. However, the spotlight is not a perfect circle — it has soft edges that extend into the surrounding area where the flankers are located.

Because the flankers fall within the broader spatial focus of attention, they are partially processed. The directional information in an incongruent flanker (e.g., left-pointing arrows) activates the competing response (left hand), creating response conflict. Before the correct response (right hand) can be selected, the conflict must be detected and resolved — this takes time, producing the RT increase.

The model makes a testable prediction: as the distance between the target and flankers increases, the interference effect should decrease — because more distant flankers fall further outside the edge of the attentional spotlight. This prediction has been repeatedly confirmed (Eriksen & Eriksen, 1974; Eriksen & St. James, 1986).

## 5. Neural Correlates: ACC and the N2 Component

**Anterior cingulate cortex (ACC):** The ACC plays a central role in conflict monitoring. When incongruent flankers activate a competing response, the ACC detects the conflict and signals prefrontal cortex to increase cognitive control. ACC activation scales with the degree of response conflict.

**The N2 ERP component:** In electroencephalography (EEG), the N2 is a negative-going waveform peaking approximately 200–350 ms after stimulus onset, maximal over frontocentral scalp regions. Incongruent flankers produce larger N2 amplitudes than congruent flankers. The N2 is widely interpreted as a neural marker of conflict detection — its latency tells us when conflict is registered, and its amplitude reflects how much conflict is present.

**The P3 component:** Following the N2, the P3 (peaking ~300–600 ms) reflects response selection and decision updating. Incongruent conditions produce delayed P3 peaks, consistent with the additional time required to resolve the flanker conflict before committing to a response.

## 6. The Gratton Effect: Sequential Adaptation of Cognitive Control

One of the most important discoveries made with the flanker task is the **Gratton effect** (Gratton, Coles, & Donchin, 1992), also called the sequential compatibility effect. The finding: the size of the flanker compatibility effect depends on what happened on the previous trial.

Specifically:
- After a congruent trial (CC), the compatibility effect on the next trial is **larger**.
- After an incongruent trial (CI), the compatibility effect on the next trial is **smaller**.

This occurs because experiencing conflict on an incongruent trial up-regulates cognitive control — the attentional spotlight is narrowed, flanker processing is suppressed, and the next trial consequently shows less interference. After a congruent trial, there is less need to maintain high control, so the spotlight widens again.

The Gratton effect demonstrates that cognitive control is not a fixed setting — it is dynamically adjusted on a trial-by-trial basis in response to recent conflict history. This has implications for understanding how the brain learns to manage competing information in real time.

## 7. The Attention Network Test (ANT)

Fan, McCandliss, Sommer, Raz, & Posner (2002, *Journal of Cognitive Neuroscience*) extended the flanker paradigm into the **Attention Network Test (ANT)**, which measures three functionally distinct attention networks:

| Network | Function | Measured by |
|---|---|---|
| Alerting | Achieving and maintaining a state of high sensitivity | RT difference between warned vs. unwarned trials |
| Orienting | Selecting information from sensory input | RT difference between valid vs. invalid spatial cues |
| Executive control | Resolving conflict | RT difference between incongruent vs. congruent flankers |

The ANT provides three separate scores from a single 20-minute task. It has been used in hundreds of studies on development (children show larger executive control scores), aging (older adults show larger executive control costs), meditation (meditators show smaller executive control costs), and clinical populations (ADHD is associated with large executive control scores).

The executive control score in the ANT is directly analogous to the flanker compatibility effect measured in Flanker Arena.

## 8. Individual Differences

**Age:** Children under 10 show substantially larger flanker effects than adults, reflecting the protracted development of inhibitory control and executive attention (Rueda et al., 2004). The compatibility effect decreases across childhood and adolescence, stabilising in young adulthood. In older adults, the effect increases again as inhibitory control declines.

**ADHD:** Individuals with ADHD show larger flanker effects than matched controls (Mullane et al., 2009, *Journal of Attention Disorders*), consistent with documented deficits in executive attention and distractor suppression.

**Practice:** Overall RT decreases with practice, but the flanker compatibility effect is more resistant to reduction than the global RT change. This asymmetry suggests that distractor suppression is qualitatively different from general response speed — you can get faster without necessarily becoming better at ignoring irrelevant information.

**Time pressure:** Under strict time limits, participants must decide before the conflict-resolution process is complete. This produces more errors on incongruent trials and can actually reduce the RT difference between conditions (while increasing the accuracy difference). This is the speed-accuracy trade-off — a fundamental constraint on cognitive performance.

## 9. Comparing Stroop and Flanker Interference

Both the Stroop task and the Flanker task measure response conflict and inhibitory control, but they differ in several important ways:

| Feature | Stroop | Flanker |
|---|---|---|
| Source of conflict | Word meaning vs. ink colour | Spatial direction of flankers vs. target |
| Typical effect size | 100–300 ms | 20–80 ms |
| Primary automaticity | Reading (highly practiced) | Spatial priming (partially automatic) |
| Clinical sensitivity | Frontal lobe, dementia | ADHD, child development |
| Key measurement | RT per condition | RT per condition + sequential effects |

The two tasks can be dissociated: some patients show impaired Stroop performance with relatively intact flanker performance, and vice versa. This suggests that while both tasks tap inhibitory control, they engage partially overlapping but distinct neural mechanisms.

## 10. Data Analysis

### Recommended analysis steps

1. Exclude trials with RT < 150 ms (too fast for genuine stimulus processing) and RT > 1500 ms (likely inattention given the task structure).
2. Compute mean RT and accuracy per condition per participant.
3. Calculate the flanker compatibility effect (RT incongruent - RT congruent).
4. Check for a speed-accuracy trade-off: if a participant is faster on incongruent trials but less accurate, they may be responding before full conflict resolution (guessing).
5. For sequential effects: code each trial as CC (previous congruent, current congruent), CI, IC, or II, and compute the compatibility effect separately for each sequence type.

### Typical published values

| Measure | Value | Source |
|---|---|---|
| Congruent RT | ~420 ms | Eriksen & Eriksen (1974); ANT norms |
| Incongruent RT | ~460–500 ms | Eriksen & Eriksen (1974); ANT norms |
| Compatibility effect | 20–80 ms | Population range |
| Effect after congruent trial | ~60–80 ms | Gratton et al. (1992) |
| Effect after incongruent trial | ~10–30 ms | Gratton et al. (1992) |

## Key References

- Eriksen, B. A., & Eriksen, C. W. (1974). Effects of noise letters upon the identification of a target letter in a nonsearch task. *Perception & Psychophysics, 16*(1), 143–149.
- Eriksen, C. W., & St. James, J. D. (1986). Visual attention within and around the field of focal attention. *Perception & Psychophysics, 40*(4), 225–240.
- Gratton, G., Coles, M. G. H., & Donchin, E. (1992). Optimizing the use of information: Strategic control of activation of responses. *Journal of Experimental Psychology: General, 121*(4), 480–506.
- Fan, J., McCandliss, B. D., Sommer, T., Raz, A., & Posner, M. I. (2002). Testing the efficiency and independence of attentional networks. *Journal of Cognitive Neuroscience, 14*(3), 340–347.
- Rueda, M. R., Fan, J., McCandliss, B. D., Halparin, J. D., Gruber, D. B., Lercari, L. P., & Posner, M. I. (2004). Development of attentional networks in childhood. *Neuropsychologia, 42*(8), 1029–1040.
- Mullane, J. C., Corkum, P. V., Klein, R. M., & McLaughlin, E. (2009). Interference control in children with and without ADHD. *Journal of Attention Disorders, 13*(2), 191–200.
