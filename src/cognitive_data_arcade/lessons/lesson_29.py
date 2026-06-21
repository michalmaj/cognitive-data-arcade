# src/cognitive_data_arcade/lessons/lesson_29.py
"""Lesson 29 - Recommendation Bubble (filter bubbles and recommendation algorithms)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Algorytmy rekomendacji optymalizują zaangażowanie (engagement): "
            "lajki, kliknięcia, czas oglądania. Nie mają wbudowanego celu "
            "'pokazuj różnorodne treści' - chyba że ktoś to jawnie zaprojektuje. "
            "Użytkownik, który klika głównie sport, dostaje więcej sportu - bo to "
            "maksymalizuje jego zaangażowanie.",
            "Bańka informacyjna (filter bubble) powstaje z trzech elementów: "
            "preferencji użytkownika (co klikasz), profilu zbudowanego przez algorytm "
            "(jak interpretuje te kliknięcia) i pętli sprzężenia zwrotnego "
            "(nowe treści wzmacniają stary profil). Każdy element z osobna jest neutralny - "
            "razem tworzą samowzmacniający się mechanizm.",
            "Kurator (moderator, edytor) może ręcznie korygować kolejkę rekomendacji. "
            "Ale kurator widzi tylko lokalną próbkę - algorytm działa w skali milionów. "
            "Nawet jeśli kurator zdywersyfikuje 5 slotów, algorytm w następnej chwili "
            "wygeneruje kolejkę z powrotem zdominowaną przez kategorie o najwyższym CTR.",
            "Systemowe rozwiązania to nie 'zatrudnij więcej kuratorów', ale zmiana "
            "funkcji celu algorytmu: np. diversity-aware ranking, exposure diversity, "
            "minimum floor dla kategorii mniejszościowych. "
            "Przykład: YouTube w 2019 zmodyfikował rekomendacje, żeby ograniczyć "
            "zasięg treści borderline - ale to wymagało świadomej decyzji inżynierskiej.",
        ],
        "notes": [
            "Eli Pariser skuł termin 'filter bubble' w 2011 (książka 'The Filter Bubble'). "
            "Jego teza: algorytmy budują spersonalizowane bańki, które ukrywają "
            "niewygodne informacje. Krytycy: bańki istniały przed algorytmami "
            "(czytamy gazety bliskie naszym poglądom). Różnica: algorytmy skalują się "
            "do miliardów użytkowników i są niewidoczne.",
            "Badania Huszara i in. (Twitter/X, 2022) pokazały, że algorytmiczna "
            "oś czasu wzmacnia treść polityczną bardziej niż chronologiczna. "
            "Efekt jest asymetryczny: wzmocnienie jest silniejsze dla jednej ze "
            "stron sceny politycznej w większości badanych krajów. "
            "To przykład tego, że brak zamierzonych stronniczości != brak efektów stronniczości.",
        ],
        "tasks": [
            "Porównaj swój wynik z Aktu 1 (diversity użytkownika) z wynikiem z Aktu 3 "
            "(diversity algorytmu). O ile pkt różniły się od siebie? "
            "Co to mówi o tym, jak bardzo algorytm amplifikuje preferencje?",
            "Zastanów się: co musiałby zrobić algorytm rekomendacji, żeby utrzymać "
            "diversity Act 2 (poziom kuratora)? Jak zmieniłaby się funkcja celu? "
            "Jakie uboczne efekty mogłyby pojawić się dla zaangażowania platformy?",
            "Znajdź jeden realny przykład systemu rekomendacji, który celowo "
            "wprowadził mechanizm zwiększający różnorodność. "
            "Co było motywacją - etyka, regulacje, czy biznes?",
        ],
    },
    "en": {
        "theory": [
            "Recommendation algorithms optimize for engagement: likes, clicks, watch time. "
            "They have no built-in goal of 'show diverse content' unless someone explicitly "
            "designs that in. A user who mostly clicks sports gets more sports - because "
            "that maximizes their engagement.",
            "A filter bubble arises from three elements: user preferences (what you click), "
            "the profile built by the algorithm (how it interprets those clicks), and a "
            "feedback loop (new content reinforces the old profile). Each element alone is "
            "neutral - together they form a self-reinforcing mechanism.",
            "A curator (moderator, editor) can manually adjust the recommendation queue. "
            "But the curator sees only a local sample - the algorithm operates at scale. "
            "Even if the curator diversifies 5 slots, the algorithm will immediately "
            "regenerate a queue dominated by the highest-CTR category.",
            "Systemic solutions are not 'hire more curators' but changing the algorithm's "
            "objective function: e.g., diversity-aware ranking, exposure diversity, "
            "minimum floors for minority categories. "
            "Example: YouTube in 2019 modified recommendations to limit borderline content - "
            "but this required a deliberate engineering decision.",
        ],
        "notes": [
            "Eli Pariser coined 'filter bubble' in 2011 (book: 'The Filter Bubble'). "
            "His thesis: algorithms build personalized bubbles that hide uncomfortable "
            "information. Critics: bubbles existed before algorithms (we read newspapers "
            "close to our views). Difference: algorithms scale to billions and are invisible.",
            "Research by Huszar et al. (Twitter/X, 2022) showed that algorithmic timelines "
            "amplify political content more than chronological ones. The effect is asymmetric: "
            "amplification is stronger for one side in most studied countries. "
            "This is an example of: absence of intended bias != absence of bias in effects.",
        ],
        "tasks": [
            "Compare your Act 1 diversity (user) with Act 3 diversity (algorithm). "
            "By how many points did they differ? "
            "What does this say about how much the algorithm amplifies preferences?",
            "Think: what would a recommendation algorithm need to do to maintain "
            "the Act 2 diversity level (curator level)? How would the objective function "
            "change? What side effects might appear for platform engagement?",
            "Find one real-world example of a recommendation system that deliberately "
            "introduced a mechanism to increase diversity. "
            "Was the motivation ethics, regulation, or business?",
        ],
    },
}
