# src/cognitive_data_arcade/lessons/lesson_29.py
"""Lesson 29 -- Recommendation Bubble (filter bubbles and recommendation algorithms)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Algorytmy rekomendacji optymalizuja zaangazowanie (engagement): "
            "lajki, klikniecia, czas ogladania. Nie maja wbudowanego celu "
            "'pokazuj roznorodne tresci' -- chyba ze ktos to jawnie zaprojektuje. "
            "Uzytkownik, ktory klika glownie sport, dostaje wiecej sportu -- bo to "
            "maksymalizuje jego zaangazowanie.",
            "Banka informacyjna (filter bubble) powstaje z trzech elementow: "
            "preferencji uzytkownika (co klikasz), profilu zbudowanego przez algorytm "
            "(jak interpretujesz te klikniecia) i petli sprzezenia zwrotnego "
            "(nowe tresci wzmacniaja stary profil). Kazdy element z osobna jest neutralny -- "
            "razem tworza samowzmacniajacy sie mechanizm.",
            "Kurator (moderator, edytor) moze recznie korygowac kolejke rekomendacji. "
            "Ale kurator widzi tylko lokalna probke -- algorytm dziala w skali milionow. "
            "Nawet jesli kurator zdywersyfikuje 5 slotow, algorytm w nastepnej chwili "
            "wygeneruje kolejke z powrotem zdominowana przez kategorie o najwyzszym CTR.",
            "Systemowe rozwiazania to nie 'zatrudnij wiecej kuratorow', ale zmiana "
            "funkcji celu algorytmu: np. diversity-aware ranking, exposure diversity, "
            "minimum floor dla kategorii mniejszosciowych. "
            "Przyklad: YouTube w 2019 zmodyfikowal rekomendacje, zeby ograniczyc "
            "zasieg tresci borderline -- ale to wymagalo swiadomej decyzji inzynierskiej.",
        ],
        "notes": [
            "Eli Pariser skul termin 'filter bubble' w 2011 (ksiazka 'The Filter Bubble'). "
            "Jego teza: algorytmy buduja spersonalizowane buble, ktore ukrywaja "
            "niewygodne informacje. Krytycy: buble istnialy przed algorytmami "
            "(czytamy gazety bliskie naszym poglandom). Roznica: algorytmy skaluja sie "
            "do miliardow uzytkownikow i sa niewidoczne.",
            "Badania Huszara i in. (Twitter/X, 2022) pokazaly, ze algorytmiczna "
            "os czasu wzmacnia tresc polityczna bardziej niz chronologiczna. "
            "Efekt jest asymetryczny: wzmocnienie jest silniejsze dla jednej ze "
            "stron sceny politycznej w wiekszosci badanych krajow. "
            "To przyklad tego, ze brak zamierzonych stronniczosci != brak efektow stronniczosci.",
        ],
        "tasks": [
            "Porownaj swoj wynik z Aktu 1 (diversity uzytkownika) z wynikiem z Aktu 3 "
            "(diversity algorytmu). O ile pkt roznialy sie od siebie? "
            "Co to mowi o tym, jak bardzo algorytm amplifikuje preferencje?",
            "Zastanow sie: co musialby zrobic algorytm rekomendacji, zeby utrzymac "
            "diversity Act 2 (poziom kuratora)? Jak zmienilaby sie funkcja celu? "
            "Jakie uboczne efekty moglyby pojawic sie dla zaangazowania platformy?",
            "Znajdz jeden realny przyklad systemu rekomendacji, ktory celowo "
            "wprowadzil mechanizm zwiekszajacy roznorodnosc. "
            "Co bylo motywacja -- etyka, regulacje, czy biznes?",
        ],
    },
    "en": {
        "theory": [
            "Recommendation algorithms optimize for engagement: likes, clicks, watch time. "
            "They have no built-in goal of 'show diverse content' unless someone explicitly "
            "designs that in. A user who mostly clicks sports gets more sports -- because "
            "that maximizes their engagement.",
            "A filter bubble arises from three elements: user preferences (what you click), "
            "the profile built by the algorithm (how it interprets those clicks), and a "
            "feedback loop (new content reinforces the old profile). Each element alone is "
            "neutral -- together they form a self-reinforcing mechanism.",
            "A curator (moderator, editor) can manually adjust the recommendation queue. "
            "But the curator sees only a local sample -- the algorithm operates at scale. "
            "Even if the curator diversifies 5 slots, the algorithm will immediately "
            "regenerate a queue dominated by the highest-CTR category.",
            "Systemic solutions are not 'hire more curators' but changing the algorithm's "
            "objective function: e.g., diversity-aware ranking, exposure diversity, "
            "minimum floors for minority categories. "
            "Example: YouTube in 2019 modified recommendations to limit borderline content -- "
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
