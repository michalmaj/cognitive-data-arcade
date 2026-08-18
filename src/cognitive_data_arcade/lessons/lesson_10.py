"""Lesson 10 - Working Memory (N-Back Memory Grid)."""

from __future__ import annotations

from cognitive_data_arcade.lessons.provenance import Claim

PROVENANCE: dict[str, Claim] = {
    "nback_accuracy_benchmarks": Claim(
        type="reference_range",
        note=(
            "N=1 >90%, N=2 70-80%, N=3 <60% accuracy presented as orientation norms. "
            "These figures are approximate; they vary with stimulus type (letter vs. "
            "spatial), presentation rate, adaptive vs. fixed design, and individual WM capacity."
        ),
        source="Kane & Engle (2002); Melby-Lervag & Hulme (2013)",
        updated="2026-08-18",
    ),
    "miller_seven_chunks": Claim(
        type="empirical",
        note=(
            "Miller (1956) '7 plus or minus 2' is a widely cited finding but applies "
            "to span under rehearsal conditions. Cowan (2001) revision to ~4 chunks "
            "is better supported by modern WM research."
        ),
        source="Miller (1956), Psychological Review; Cowan (2001), Behavioral and Brain Sciences",
        updated="2026-08-18",
    ),
    "training_controversy_consensus": Claim(
        type="empirical",
        note=(
            "WM training debate presented as ongoing. The current evidence balance "
            "(as of 2018 consensus statement; Melby-Lervag & Hulme, 2013 meta-analysis) "
            "favours near transfer only, with no reliable far transfer to fluid intelligence."
        ),
        source="Melby-Lervag & Hulme (2013), Developmental Psychology; Shipstead et al. (2012), Psychological Bulletin",
        updated="2026-08-18",
    ),
}

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "N-Back mierzy pojemność pamięci roboczej - zdolność do przechowywania i aktualizowania informacji przy jednoczesnym jej przetwarzaniu. N oznacza ile kroków wstecz trzeba porównać.",
            "Miller (1956) - w artykule 'The Magical Number Seven, Plus or Minus Two' George Miller wykazał, że pojemność pamięci krótkotrwałej wynosi ok. 7 elementów (plus minus 2). Cowan (2001) zrewidował tę liczbę do ok. 4 porcji informacji (chunks), gdy zapobiega się powtarzaniu. Różnica wynika z tego, że Miller liczył elementy, a Cowan - porcje po grupowaniu.",
            "Model Baddeleya - pamięć robocza składa się z pętli fonologicznej (dźwięki i słowa), szkicownika wzrokowo-przestrzennego (obrazy i lokalizacje) i centralnego wykonawcy (koordynacja). Dual N-Back angażuje pierwsze dwa składniki jednocześnie.",
            "Dlaczego N=2 jest standardem - N=1 jest za łatwe dla większości dorosłych (accuracy >90%). N=3 jest bardzo trudne (accuracy <60%). N=2 daje dobry zakres trudności i jest najlepiej zbadaną wersją.",
            "Korelacja z inteligencją płynną - wysoka pojemność pamięci roboczej koreluje z wynikami testów inteligencji płynnej (Gf), która mierzy zdolność do rozwiązywania nowych problemów.",
            "Kontrowersja treningu - Jaeggi i in. (2008) opublikowali w PNAS wyniki sugerujące, że trening Dual N-Back podnosi inteligencję płynną. Metaanaliza Shipsteada i in. (2012) w Psychological Bulletin znalazła znikomy transfer poza samym zadaniem. Debata trwa do dziś i jest jednym z najgłośniejszych sporów w kognitywistyce ostatniej dekady.",
        ],
        "notes": [
            "Dual N-Back podwaja obciążenie - śledzenie zarówno pozycji jak i litery angażuje oba składniki pamięci roboczej jednocześnie. Trudność rośnie nieliniowo z N.",
            "Accuracy 70-80% dla N=2 to norma - przy wyższej accuracy (>90%) system adaptacyjny podnosi N. Przy niższej (<60%) obniża. Cel to utrzymanie trudności na poziomie ok. 75% poprawnych.",
            "Reset pamięci na początku bloku - pierwsze N prób każdego bloku nie można ocenić (brak wcześniejszego bodźca do porównania). Wyniki na początku bloku są typowo gorsze niż w jego środku.",
        ],
        "tasks": [
            "Przy którym poziomie N accuracy spada poniżej 70%? To przybliżona górna granica bieżącej pojemności pamięci roboczej.",
            "Porównaj accuracy dla pozycji i liter osobno. Która składowa jest trudniejsza? Czy widoczna jest asymetria między szkicownikiem przestrzennym a pętlą fonologiczną?",
            "Czy accuracy jest niższa na początku każdego bloku niż w jego środku? Jak szybko następuje adaptacja? To czas potrzebny na zbudowanie bufora pamięci roboczej.",
        ],
    },
    "en": {
        "theory": [
            "N-Back measures working memory capacity - the ability to hold and update information while simultaneously processing it. N denotes how many steps back a comparison must be made.",
            "Miller (1956) - in 'The Magical Number Seven, Plus or Minus Two', George Miller showed that short-term memory capacity is approximately 7 items (plus or minus 2). Cowan (2001) revised this to approximately 4 chunks when rehearsal is prevented. The difference arises because Miller counted items while Cowan counted chunks after grouping.",
            "Baddeley's model - working memory comprises the phonological loop (sounds and words), the visuospatial sketchpad (images and locations), and the central executive (coordination). Dual N-Back engages the first two components simultaneously.",
            "Why N=2 is the standard - N=1 is too easy for most adults (accuracy >90%). N=3 is very hard (accuracy <60%). N=2 gives a good difficulty range and is the best-studied version in the literature.",
            "Correlation with fluid intelligence - high working memory capacity correlates with fluid intelligence (Gf) test scores, which measure the ability to solve novel problems.",
            "The training controversy - Jaeggi et al. (2008) published results in PNAS suggesting that Dual N-Back training raises fluid intelligence. A meta-analysis by Shipstead et al. (2012) in Psychological Bulletin found negligible transfer beyond the task itself. The debate continues and is one of the loudest disputes in cognitive science of the past decade.",
        ],
        "notes": [
            "Dual N-Back doubles the load - tracking both position and letter engages both working memory components simultaneously. Difficulty grows non-linearly with N.",
            "Accuracy 70-80% for N=2 is normal - if accuracy is higher (>90%), the adaptive system raises N. If lower (<60%), it reduces N. The aim is to maintain difficulty at approximately 75% correct.",
            "Memory reset at block start - the first N trials of each block cannot be scored (no earlier stimulus to compare to). Performance at the start of a block is typically lower than in the middle.",
        ],
        "tasks": [
            "At which N level does accuracy drop below 70%? This is an approximation of the current working memory capacity limit.",
            "Compare accuracy for position and letter separately. Which component is harder? Is there an asymmetry between the visuospatial sketchpad and the phonological loop?",
            "Is accuracy lower at the start of each block than in the middle? How quickly does adaptation occur? This is the time needed to build up the working memory buffer.",
        ],
    },
}
