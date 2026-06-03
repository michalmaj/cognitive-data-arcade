# Theory — Working Memory and the N-Back Paradigm

## 1. Historical Background

The concept of a limited-capacity short-term memory system that actively maintains and manipulates information has been central to cognitive psychology since William James's distinction between primary and secondary memory in 1890. The formal n-back task was introduced by **Wayne Kirchner** (1958) in a study of short-term memory load in air traffic controllers. Kirchner's key insight was that by varying n — the number of steps back to compare — he could systematically vary memory load without changing the stimuli themselves.

The paradigm remained a laboratory curiosity for several decades until the emergence of neuroimaging in the 1990s made it a workhorse of cognitive neuroscience. Its appeal for fMRI researchers is that it parametrically manipulates working memory load: n=0 (matching to a fixed target), n=1, n=2, and n=3 produce predictably graded increases in dorsolateral prefrontal cortex (dlPFC) activation. The n-back is now one of the most cited experimental paradigms in cognitive neuroscience.

The task re-entered public awareness through a 2008 *PNAS* paper by **Susanne Jaeggi** and colleagues, who claimed that training on dual n-back improved fluid intelligence — a claim that triggered one of the most active debates in cognitive training research over the following decade.

## 2. Baddeley's Model of Working Memory

Working memory (WM) is the cognitive system responsible for the active maintenance and manipulation of a limited amount of information over short time periods in service of ongoing tasks. It is distinct from short-term memory in that it is not passive storage but an active workspace.

The most influential account is **Baddeley's multicomponent model** (Baddeley & Hitch, 1974; revised in Baddeley, 2000):

| Component | Function | Capacity | N-back role |
|---|---|---|---|
| Phonological loop | Stores and rehearses verbal/acoustic information | ~2 s of speech | Letter tracking in dual n-back |
| Visuospatial sketchpad | Stores and manipulates visual and spatial information | ~3–4 objects | Position tracking in n-back |
| Central executive | Attentional control; coordinates slave systems; updates and inhibits WM contents | Limited | Primary locus of n-back load |
| Episodic buffer | Integrates information across slave systems and long-term memory into coherent episodes | ~4 chunks | Binding of sequence context |

The **phonological loop** has two subcomponents: a phonological store (passive acoustic trace that decays in ~2 seconds) and an articulatory rehearsal process (inner speech that refreshes the trace). Words that are phonologically similar (cat, bat, mat) are harder to remember than phonologically distinct words — the **phonological similarity effect** — because similar traces interfere in the store.

The **central executive** is the most important component for n-back performance. It performs three key operations: *updating* (replacing old WM contents with new information), *inhibiting* (suppressing irrelevant or outdated information), and *shifting* (switching attention between task sets). All three are heavily taxed by the n-back.

## 3. The N-Back Paradigm: Mechanics

In the standard n-back task:

1. A sequence of stimuli is presented one at a time.
2. At each step, the participant decides: **does this stimulus match the one from n steps ago?**
3. If yes, respond (press a key). If no, withhold.

The three simultaneous cognitive operations required:

- **Identify** the current stimulus (perceptual processing)
- **Compare** it to the item held in memory at position n
- **Update** the memory buffer: discard the stimulus from position n+1 steps ago, shift all remaining items back by one position, and add the new stimulus to position 1

The update operation is the bottleneck. At n=1, you maintain one item and update continuously — easy for most adults. At n=2, you maintain a two-item buffer and update after each stimulus — moderately demanding. At n=3, the buffer holds three items and the update operation must proceed without losing track of the ordering — highly demanding for most adults.

**Why difficulty grows non-linearly:** each increment of n adds one more item to the buffer *and* one more update operation at each step. The combinatorial load grows rapidly. Additionally, longer buffers increase proactive interference — items from earlier trials interfere with recall of items from n steps ago.

## 4. Typical Performance Benchmarks

| N level | Typical accuracy (healthy adults) | Typical d' |
|---|---|---|
| 0-Back (match to target) | >95% | >3.0 |
| 1-Back | 85–95% | 2.0–3.0 |
| 2-Back | 70–85% | 1.5–2.5 |
| 3-Back | 50–70% | 0.8–1.5 |
| 4-Back | 40–55% | 0.3–0.8 |

Accuracy below 55% at n=3 suggests performance near chance and may indicate that the participant's current WM span does not support that level. Accuracy above 90% at n=2 is a signal that the adaptive system should increase n.

The standard adaptive n-back used in research (including this application) targets **~75% accuracy**. When accuracy rises above ~85%, n is incremented. When it falls below ~65%, n is decremented. This keeps the participant in the zone of productive difficulty.

## 5. Dual N-Back

The **dual n-back** task simultaneously presents two independent stimulus streams — typically a spatial position on a grid and an auditory letter — and requires tracking both concurrently. The participant must make separate responses for each stream (position match and letter match).

Dual n-back doubles the cognitive load by engaging both the visuospatial sketchpad and the phonological loop simultaneously, in addition to the central executive overhead of managing two independent buffers. Research suggests that dual n-back load does not simply add up — the two streams interfere in the central executive, making dual n-back disproportionately harder than single n-back at the same level.

## 6. The Training Controversy

### Jaeggi et al. (2008)

Jaeggi and colleagues published a study in *PNAS* claiming that approximately 4 weeks of daily dual n-back training (approximately 30 minutes per day) produced gains in **fluid intelligence** (Gf), as measured by Raven's Progressive Matrices — a test of novel problem solving that is generally considered to have low trainability. Critically, the gains were dose-dependent: the more sessions, the larger the improvement in Gf. This was taken as evidence of *far transfer* — training on one task improving a qualitatively different ability.

The claim attracted enormous attention because fluid intelligence had long been thought to be stable across adulthood and resistant to environmental interventions.

### Replication and meta-analytic outcomes

The decade following Jaeggi et al. saw dozens of replication attempts. The results were mixed and contested:

- **Near transfer** (improvement on other WM tasks) was consistently observed. WM training reliably improves performance on tasks that are similar in structure to the trained task.
- **Far transfer** (improvement in fluid intelligence) proved elusive. Several well-powered studies (e.g., Redick et al., 2013; Shipstead et al., 2012) failed to find Gf gains using near-identical training protocols.
- **Melby-Lervåg & Hulme (2013)** conducted a meta-analysis of 23 WM training studies. Conclusion: near-transfer effects are robust and persistent; far-transfer effects are unreliable and likely to be zero or negligible.

The current scientific consensus, reflected in a 2018 consensus statement endorsed by over 70 cognitive scientists, is that:

1. WM training reliably improves performance on the trained tasks and closely related tasks.
2. WM training does not reliably improve fluid intelligence or other broad cognitive abilities.
3. Previously reported far-transfer effects were likely due to methodological artifacts (active vs. passive control groups, expectation effects, publication bias).

The Cogmed commercial training program and similar products were widely marketed on the basis of early positive results. Their clinical efficacy for ADHD and other populations remains a subject of active debate.

## 7. Why WM Capacity Matters

Despite the training controversy, individual differences in WM capacity are robustly associated with important outcomes:

- **Reading comprehension:** High-WM readers maintain more information during sentence processing, reducing garden-path errors and enabling inference generation (Kane & Engle, 2002).
- **Mathematical reasoning:** Arithmetic and algebra problem solving rely heavily on WM for maintaining intermediate results.
- **Fluid intelligence:** WM capacity is one of the strongest cognitive predictors of performance on novel reasoning tasks.
- **Mind-wandering:** Low-WM individuals show more mind-wandering during sustained tasks, which is detected as worse performance specifically on items following periods of mind-wandering (Smallwood et al., 2004).

These correlations do not imply that WM *causes* intelligence — the relationship is bidirectional and mediated by neural and genetic factors. But WM capacity provides a useful window into the cognitive architecture that underlies higher-level cognition.

## 8. Neural Basis of N-Back Performance

fMRI studies of the n-back paradigm have consistently identified a core network of brain regions:

**Bilateral dorsolateral prefrontal cortex (dlPFC):** The most reliably activated region. Activity increases monotonically with n. The dlPFC is thought to maintain and manipulate goal-relevant information against distraction. Patients with dlPFC lesions show specific impairments in n-back tasks relative to matched controls.

**Anterior cingulate cortex (ACC):** Active during high-load n-back conditions. The ACC monitors for conflicts between competing response tendencies — relevant to the n-back when the current item is similar but not identical to the n-back item (lure trials).

**Posterior parietal cortex:** Left parietal for verbal load (phonological loop), right parietal for visuospatial load. The parietal cortex is thought to provide the workspace where WM representations are held active.

**Cerebellar contributions:** The cerebellum contributes to temporal sequencing, which is critical for maintaining the ordinal position of items in the n-back buffer.

A particularly important finding is the **load-dependent deactivation** of the **default mode network** (DMN) — a set of regions including medial prefrontal cortex, posterior cingulate cortex, and angular gyrus — that are active during rest and deactivated during cognitively demanding tasks. High n-back load produces strong DMN suppression; failure to suppress the DMN correlates with poor task performance and mind-wandering.

## 9. Lure Trials and Proactive Interference

A methodological feature of the n-back that affects performance is the **lure trial** — a trial where the stimulus matches the item from n+1 or n−1 steps ago (but not n steps ago). Lure trials are particularly error-prone because the participant must distinguish between a genuine match (n steps ago) and a near-miss (n±1 steps ago). This requires precise temporal tagging of WM representations.

The difficulty of lure trials illustrates **proactive interference**: old WM contents (items from prior positions) interfere with retrieval of the target item at position n. Proactive interference increases with n because more irrelevant items accumulate in memory.

## 10. Measuring N-Back Performance: Signal Detection Theory

N-back performance is best characterised using Signal Detection Theory (SDT), the same framework introduced in Lesson 09 (Go/No-Go Guard). Match trials are the "signal" and non-match trials are the "noise."

| SDT outcome | N-back meaning |
|---|---|
| Hit | Responded "match" on an actual match trial |
| Miss | Failed to respond on a match trial |
| False alarm | Responded "match" on a non-match trial |
| Correct rejection | Withheld response on a non-match trial |

The formula for d' (d-prime):

```
d' = Z(hit rate) - Z(false alarm rate)
```

where hit rate = hits / total match trials, and false alarm rate = false alarms / total non-match trials.

d' is the preferred measure over raw accuracy because it is independent of response bias. A participant who responds "match" to almost every stimulus will have a high hit rate but also a high false alarm rate — d' will correctly identify this as poor discrimination. A participant who almost never responds will have a low false alarm rate but also a low hit rate — d' again captures this as poor discrimination.

**Lure sensitivity:** Some researchers compute a separate d' for lure trials (stimuli matching n±1 positions ago). This measures the precision of temporal tagging — whether the participant's WM representations carry accurate ordinal information, or merely "feels familiar" without a reliable position tag.

## 11. References

- Baddeley, A. D. (2000). The episodic buffer: a new component of working memory? *Trends in Cognitive Sciences, 4*(11), 417–423.
- Baddeley, A. D., & Hitch, G. J. (1974). Working memory. In G. H. Bower (Ed.), *The Psychology of Learning and Motivation* (Vol. 8, pp. 47–89). Academic Press.
- Jaeggi, S. M., Buschkuehl, M., Jonides, J., & Perrig, W. J. (2008). Improving fluid intelligence with training on working memory. *Proceedings of the National Academy of Sciences, 105*(19), 6829–6833.
- Kane, M. J., & Engle, R. W. (2002). The role of prefrontal cortex in working-memory capacity, executive attention, and general fluid intelligence. *Psychonomic Bulletin & Review, 9*(4), 637–671.
- Kirchner, W. K. (1958). Age differences in short-term retention of rapidly changing information. *Journal of Experimental Psychology, 55*(4), 352–358.
- Melby-Lervåg, M., & Hulme, C. (2013). Is working memory training effective? A meta-analytic review. *Developmental Psychology, 49*(2), 270–291.
- Smallwood, J., Fishman, D. J., & Schooler, J. W. (2007). Counting the cost of an absent mind: mind wandering as an underrecognized influence on educational performance. *Psychonomic Bulletin & Review, 14*(2), 230–236.
