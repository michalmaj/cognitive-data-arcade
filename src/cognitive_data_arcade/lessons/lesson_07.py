"""Lesson 07 — Stroop Effect (Stroop Challenge)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Efekt Stroopa (1935) — gdy kolor tuszu słowa jest niezgodny z jego znaczeniem (np. słowo CZERWONY napisane niebieskim tuszem), czas odpowiedzi rośnie. Przyczyną jest konflikt dwóch procesów poznawczych.",
            "Automatyczność czytania — czytanie jest wyuczone do tego stopnia, że nie możemy go wyłączyć. Kiedy widzisz słowo, mózg przetwarza je automatycznie, nawet gdy zadanie wymaga ignorowania jego znaczenia.",
            "Trzy warunki — zgodny (CZERWONY czerwonym tuszem): najszybszy. Neutralny (XXXXX czerwonym tuszem): pośredni. Niezgodny (NIEBIESKI czerwonym tuszem): najwolniejszy. Różnica to efekt Stroopa.",
            "Co mierzy efekt Stroopa — interference = RT(niezgodny) − RT(neutralny). Facilitation = RT(neutralny) − RT(zgodny). Oba mierzą zdolność do hamowania procesów automatycznych.",
            "Zastosowania kliniczne — zmniejszony efekt Stroopa obserwuje się w ADHD, demencji i schizofrenii. Test Stroopa jest używany w neuropsychologicznej ocenie funkcji wykonawczych.",
        ],
        "notes": [
            "RT i dokładność łącznie — ktoś odpowiadający szybko z niską dokładnością stosuje inną strategię niż ktoś wolny i dokładny. Obie miary razem dają pełny obraz zachowania.",
            "Efekt maleje przy zmęczeniu — kontrola hamowania wymaga energii. Pod koniec długiej sesji efekt Stroopa często rośnie, bo zdolność hamowania słabnie.",
            "Facilitation vs. interference — to dwa odrębne procesy. Możesz mieć duże interference (spowolnienie przez niezgodność) przy małej facilitation (przyspieszeniu przez zgodność).",
        ],
        "tasks": [
            "Oblicz swój efekt Stroopa: RT(niezgodny) − RT(zgodny). Typowe wartości to 100–300 ms. Jak wypada Twój wynik na tle tych norm?",
            "Porównaj swoje interference i facilitation osobno. Które jest większe? Co to mówi o tym, jak Twój mózg przetwarza konflikty percepcyjne?",
            "Czy Twoja dokładność spada w warunku niezgodnym? Jeśli tak — czy to błędy impulsywne (szybkie złe odpowiedzi) czy wahanie (wolne złe odpowiedzi)?",
        ],
    },
    "en": {
        "theory": [
            "The Stroop effect (1935) — when the ink colour of a word conflicts with its meaning (e.g. the word RED written in blue ink), response time increases. The cause is a conflict between two cognitive processes.",
            "Reading automaticity — reading is so well-practised that we cannot switch it off. When you see a word, the brain processes it automatically, even when the task requires ignoring its meaning.",
            "Three conditions — congruent (RED in red ink): fastest. Neutral (XXXXX in red ink): intermediate. Incongruent (BLUE in red ink): slowest. The difference is the Stroop effect.",
            "What the Stroop effect measures — interference = RT(incongruent) − RT(neutral). Facilitation = RT(neutral) − RT(congruent). Both measure the ability to suppress automatic processes.",
            "Clinical applications — a reduced Stroop effect is observed in ADHD, dementia, and schizophrenia. The Stroop test is used in neuropsychological assessment of executive functions.",
        ],
        "notes": [
            "RT and accuracy together — someone who responds quickly with low accuracy uses a different strategy than someone who is slow but accurate. Both measures together give a complete picture.",
            "Effect weakens with fatigue — inhibitory control requires energy. Towards the end of a long session, the Stroop effect often grows because inhibition capacity diminishes.",
            "Facilitation vs. interference — these are two distinct processes. You can have large interference (slowing due to incongruency) with small facilitation (speeding due to congruency).",
        ],
        "tasks": [
            "Calculate your Stroop effect: RT(incongruent) − RT(congruent). Typical values are 100–300 ms. How does your result compare to these norms?",
            "Compare your interference and facilitation separately. Which is larger? What does this say about how your brain processes perceptual conflicts?",
            "Does your accuracy drop in the incongruent condition? If so — are these impulsive errors (fast wrong answers) or hesitation errors (slow wrong answers)?",
        ],
    },
}
