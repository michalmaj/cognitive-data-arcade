# src/cognitive_data_arcade/lessons/lesson_29.py
"""Lesson 29 - Recommendation Bubble (filter bubbles and recommendation algorithms)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Algorytmy rekomendacji optymalizuja zaangazowanie (engagement): lajki, klikniecia, czas ogladania. Nie maja wbudowanego celu 'pokazuj roznorodne tresci' - chyba ze ktos to jawnie zaprojektuje. Uzytkownik, ktory klika glownie sport, dostaje wiecej sportu - bo to maksymalizuje jego zaangazowanie.",
            "Filtrowanie kolaboratywne (collaborative filtering) zostalo opisane przez Goldberga i in. (1992) w systemie Tapestry w Xerox PARC - pierwszym systemie rekomendacji opartym na ocenach innych uzytkownikow. GroupLens (1994) zastosowal CF do rekomendacji artykulow Usenet. Termin 'collaborative filtering' pochodzi wlasnie z tamtego artykulu. Netflix Prize (2006-2009, nagroda 1 milion dolarow) przyspieszyl rozwoj algorytmow hybrydowych: zwyciezca BellKor Pragmatic Chaos uzywal zespolu 107 modeli.",
            "Banku informacyjna (filter bubble) powstaje z trzech elementow: preferencji uzytkownika (co sie klika), profilu zbudowanego przez algorytm (jak interpretuje te klikniecia) i petli sprzezenia zwrotnego (nowe tresci wzmacniaja stary profil). Kazdy element z osobna jest neutralny - razem tworza samowzmacniajacy sie mechanizm.",
            "Rozroznienie: banku informacyjna (filter bubble) vs komora echa (echo chamber). Sunstein (2017, 'Republic') rozroznia: banku informacyjna jest pasywna i algorytmiczna - uzytkownik nie wybiera jej swiadomie. Komora echa jest aktywna i spoleczna - uzytkownik samodzielnie eliminuje odmieniajace glosy. Oba mechanizmy moga wspoldzialac, ale moga rowniez wystepowac niezaleznie.",
            "Kurator (moderator, edytor) moze recznie korygowac kolejke rekomendacji. Ale kurator widzi tylko lokalna probke - algorytm dziala w skali milionow. Nawet jesli kurator zdywersyfikuje 5 slotow, algorytm w nastepnej chwili wygeneruje kolejke z powrotem zdominowana przez kategorie o najwyzszym CTR.",
            "Systemowe rozwiazania to nie 'zatrudnij wiecej kuratorow', ale zmiana funkcji celu algorytmu: np. diversity-aware ranking, exposure diversity, minimum floor dla kategorii mniejszosciowych. Przyklad: YouTube w 2019 zmodyfikowal rekomendacje, zeby ograniczyc zasieg tresci borderline - ale to wymagalo swiadomej decyzji inzynierskiej.",
        ],
        "notes": [
            "Eli Pariser skul termin 'filter bubble' w 2011 (ksiazka 'The Filter Bubble'). Jego teza: algorytmy buduja spersonalizowane banki, ktore ukrywaja niewygodne informacje. Krytycy: banki istnialy przed algorytmami (czytamy gazety bliskie naszym poglandom). Roznica: algorytmy skaluja sie do miliardow uzytkownikow i sa niewidoczne.",
            "Badania Huszara i in. (Twitter/X, 2022) pokazaly, ze algorytmiczna os czasu wzmacnia tresc polityczna bardziej niz chronologiczna. Efekt jest asymetryczny: wzmocnienie jest silniejsze dla jednej ze stron sceny politycznej w wiekszosci badanych krajow. To przyklad: brak zamierzonych stronniczosci != brak efektow stronniczosci.",
        ],
        "tasks": [
            "Porownaj wynik z Aktu 1 (diversity uzytkownika) z wynikiem z Aktu 3 (diversity algorytmu). O ile pkt roznia sie od siebie? Co to mowi o tym, jak bardzo algorytm amplifikuje preferencje?",
            "Co musialby zrobic algorytm rekomendacji, zeby utrzymac diversity Aktu 2 (poziom kuratora)? Jak zmienilaby sie funkcja celu? Jakie uboczne efekty moglby pojawic sie dla zaangazowania platformy?",
            "Znajdz jeden realny przyklad systemu rekomendacji, ktory celowo wprowadzil mechanizm zwiekszajacy roznorodnosc. Co bylo motywacja - etyka, regulacje, czy biznes?",
        ],
    },
    "en": {
        "theory": [
            "Recommendation algorithms optimize for engagement: likes, clicks, watch time. They have no built-in goal of 'show diverse content' unless someone explicitly designs that in. A user who mostly clicks sports gets more sports - because that maximizes their engagement.",
            "Collaborative filtering was described by Goldberg et al. (1992) in the Tapestry system at Xerox PARC - the first recommendation system based on ratings from other users. GroupLens (1994) applied CF to Usenet article recommendations. The term 'collaborative filtering' itself comes from that paper. The Netflix Prize (2006-2009, $1 million award) accelerated hybrid algorithm development: winner BellKor Pragmatic Chaos used an ensemble of 107 models.",
            "A filter bubble arises from three elements: user preferences (what is clicked), the profile built by the algorithm (how it interprets those clicks), and a feedback loop (new content reinforces the old profile). Each element alone is neutral - together they form a self-reinforcing mechanism.",
            "Distinction: filter bubble vs echo chamber. Sunstein (2017, 'Republic') differentiates: a filter bubble is passive and algorithmic - the user does not consciously choose it. An echo chamber is active and social - the user self-selects out of dissenting voices. Both mechanisms can co-occur but also arise independently.",
            "A curator (moderator, editor) can manually adjust the recommendation queue. But the curator sees only a local sample - the algorithm operates at millions-scale. Even if the curator diversifies 5 slots, the algorithm will immediately regenerate a queue dominated by the highest-CTR category.",
            "Systemic solutions are not 'hire more curators' but changing the algorithm's objective function: e.g., diversity-aware ranking, exposure diversity, minimum floors for minority categories. Example: YouTube in 2019 modified recommendations to limit borderline content - but this required a deliberate engineering decision.",
        ],
        "notes": [
            "Eli Pariser coined 'filter bubble' in 2011 (book: 'The Filter Bubble'). His thesis: algorithms build personalized bubbles that hide uncomfortable information. Critics: bubbles existed before algorithms (we read newspapers close to our views). Difference: algorithms scale to billions and are invisible.",
            "Research by Huszar et al. (Twitter/X, 2022) showed that algorithmic timelines amplify political content more than chronological ones. The effect is asymmetric: amplification is stronger for one side in most studied countries. This is an example of: absence of intended bias != absence of bias in effects.",
        ],
        "tasks": [
            "Compare the Act 1 diversity (user) with Act 3 diversity (algorithm). By how many points did they differ? What does this say about how much the algorithm amplifies preferences?",
            "What would a recommendation algorithm need to do to maintain the Act 2 diversity level (curator level)? How would the objective function change? What side effects might appear for platform engagement?",
            "Find one real-world example of a recommendation system that deliberately introduced a mechanism to increase diversity. Was the motivation ethics, regulation, or business?",
        ],
    },
}
