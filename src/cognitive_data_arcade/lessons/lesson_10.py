"""Lesson 10 — Working Memory (N-Back Memory Grid)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "N-Back mierzy pojemność pamięci roboczej — zdolność do przechowywania i aktualizowania informacji przy jednoczesnym jej przetwarzaniu. N oznacza ile kroków wstecz trzeba porównać.",
            "Model Baddeleya — pamięć robocza składa się z pętli fonologicznej (dźwięki i słowa), szkicownika wzrokowo-przestrzennego (obrazy i lokalizacje) i centralnego wykonawcy (koordynacja). Dual N-Back angażuje pierwsze dwa składniki jednocześnie.",
            "Dlaczego N=2 jest standardem — N=1 jest za łatwe dla większości dorosłych (accuracy >90%). N=3 jest bardzo trudne (accuracy <60%). N=2 daje dobry zakres trudności i jest najlepiej zbadaną wersją.",
            "Korelacja z inteligencją płynną — wysoka pojemność pamięci roboczej koreluje z wynikami testów inteligencji płynnej (Gf), która mierzy zdolność do rozwiązywania nowych problemów.",
            "Efekt treningu — poprawa w samym zadaniu N-Back jest wyraźna. Transfer na inne zdolności poznawcze jest dyskusyjny — wyniki różnych laboratoriów są sprzeczne i debata trwa.",
        ],
        "notes": [
            "Dual N-Back podwaja obciążenie — śledzenie zarówno pozycji jak i litery angażuje oba składniki pamięci roboczej jednocześnie. Trudność rośnie nieliniowo z N.",
            "Accuracy 70–80% dla N=2 to norma — przy wyższej accuracy (>90%) system adaptacyjny podnosi N. Przy niższej (<60%) obniża. Cel to utrzymanie trudności na poziomie ~75% poprawnych.",
            "Reset pamięci na początku bloku — pierwsze N prób każdego bloku nie można ocenić (brak wcześniejszego bodźca do porównania). Wiele osób gorzej radzi sobie na początku każdego bloku.",
        ],
        "tasks": [
            "Jaki poziom N jest dla Ciebie optymalny? Przy którym N Twoja accuracy spada poniżej 70%? To przybliżona górna granica Twojej bieżącej pojemności pamięci roboczej.",
            "Porównaj accuracy dla pozycji i liter osobno. Która składowa jest trudniejsza? Czy widzisz asymetrię między szkicownikiem przestrzennym a pętlą fonologiczną?",
            "Czy Twoja accuracy jest niższa na początku każdego bloku niż w jego środku? Jak szybko 'wchodzisz w rytm'? To czas budowania bufora pamięci roboczej.",
        ],
    },
    "en": {
        "theory": [
            "N-Back measures working memory capacity — the ability to hold and update information while simultaneously processing it. N denotes how many steps back you must compare.",
            "Baddeley's model — working memory comprises the phonological loop (sounds and words), the visuospatial sketchpad (images and locations), and the central executive (coordination). Dual N-Back engages the first two components simultaneously.",
            "Why N=2 is the standard — N=1 is too easy for most adults (accuracy >90%). N=3 is very hard (accuracy <60%). N=2 gives a good difficulty range and is the best-studied version in the literature.",
            "Correlation with fluid intelligence — high working memory capacity correlates with fluid intelligence (Gf) test scores, which measure the ability to solve novel problems.",
            "Training effects — improvement on the N-Back task itself is clear. Transfer to other cognitive abilities is contested — results across laboratories are contradictory and the debate continues.",
        ],
        "notes": [
            "Dual N-Back doubles the load — tracking both position and letter engages both working memory components simultaneously. Difficulty grows non-linearly with N.",
            "Accuracy 70–80% for N=2 is normal — if accuracy is higher (>90%), the adaptive system raises N. If lower (<60%), it reduces N. The aim is to maintain difficulty at ~75% correct.",
            "Memory reset at block start — the first N trials of each block cannot be scored (no earlier stimulus to compare to). Many people perform worse at the start of each block.",
        ],
        "tasks": [
            "What N level is optimal for you? At which N does your accuracy drop below 70%? This is an approximation of your current working memory capacity limit.",
            "Compare accuracy for position and letter separately. Which component is harder? Do you see an asymmetry between the visuospatial sketchpad and the phonological loop?",
            "Is your accuracy lower at the start of each block than in the middle? How quickly do you 'find your rhythm'? This is the time needed to build up your working memory buffer.",
        ],
    },
}
