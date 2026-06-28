# src/cognitive_data_arcade/lessons/lesson_29.py
"""Lesson 29 - Recommendation Bubble (filter bubbles and recommendation algorithms)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Algorytmy rekomendacji optymalizują zaangażowanie (engagement): lajki, kliknięcia, czas oglądania. Nie mają wbudowanego celu 'pokazuj różnorodne treści' - chyba że ktoś to jawnie zaprojektuje. Użytkownik, który klika głównie sport, dostaje więcej sportu - bo to maksymalizuje jego zaangażowanie.",
            "Filtrowanie kolaboratywne (collaborative filtering) zostało opisane przez Goldberga i in. (1992) w systemie Tapestry w Xerox PARC - pierwszym systemie rekomendacji opartym na ocenach innych użytkowników. GroupLens (1994) zastosował CF do rekomendacji artykułów Usenet. Termin 'collaborative filtering' pochodzi właśnie z tamtego artykułu. Netflix Prize (2006-2009, nagroda 1 milion dolarów) przyspieszył rozwój algorytmów hybrydowych: zwycięzca BellKor Pragmatic Chaos używał zespołu 107 modeli.",
            "Bańka informacyjna (filter bubble) powstaje z trzech elementów: preferencji użytkownika (co się klika), profilu zbudowanego przez algorytm (jak interpretuje te kliknięcia) i pętli sprzężenia zwrotnego (nowe treści wzmacniają stary profil). Każdy element z osobna jest neutralny - razem tworzą samowzmacniający się mechanizm.",
            "Rozróżnienie: bańka informacyjna (filter bubble) vs komora echa (echo chamber). Sunstein (2017, 'Republic') rozróżnia: bańka informacyjna jest pasywna i algorytmiczna - użytkownik nie wybiera jej świadomie. Komora echa jest aktywna i społeczna - użytkownik samodzielnie eliminuje odmienne głosy. Oba mechanizmy mogą współdziałać, ale mogą również występować niezależnie.",
            "Kurator (moderator, edytor) może ręcznie korygować kolejkę rekomendacji. Ale kurator widzi tylko lokalną próbkę - algorytm działa w skali milionów. Nawet jeśli kurator zdywersyfikuje 5 slotów, algorytm w następnej chwili wygeneruje kolejkę zdominowaną przez kategorie o najwyższym CTR.",
            "Systemowe rozwiązania to nie 'zatrudnij więcej kuratorów', ale zmiana funkcji celu algorytmu: np. diversity-aware ranking, exposure diversity, minimum floor dla kategorii mniejszościowych. Przykład: YouTube w 2019 zmodyfikował rekomendacje, żeby ograniczyć zasięg treści borderline - ale to wymagało świadomej decyzji inżynierskiej.",
        ],
        "notes": [
            "Eli Pariser skuł termin 'filter bubble' w 2011 (książka 'The Filter Bubble'). Jego teza: algorytmy budują spersonalizowane bańki, które ukrywają niewygodne informacje. Krytycy: bańki istniały przed algorytmami (czytamy gazety bliskie naszym poglądom). Różnica: algorytmy skalują się do miliardów użytkowników i są niewidoczne.",
            "Badania Huszara i in. (Twitter/X, 2022) pokazały, że algorytmiczna oś czasu wzmacnia treść polityczną bardziej niż chronologiczna. Efekt jest asymetryczny: wzmocnienie jest silniejsze dla jednej ze stron sceny politycznej w większości badanych krajów. To przykład: brak zamierzonych stronniczości != brak efektów stronniczości.",
        ],
        "tasks": [
            "Porównaj wynik z Aktu 1 (diversity użytkownika) z wynikiem z Aktu 3 (diversity algorytmu). O ile pkt różnią się od siebie? Co to mówi o tym, jak bardzo algorytm amplifikuje preferencje?",
            "Co musiałby zrobić algorytm rekomendacji, żeby utrzymać diversity Aktu 2 (poziom kuratora)? Jak zmieniłaby się funkcja celu? Jakie uboczne efekty mogłyby pojawić się dla zaangażowania platformy?",
            "Znajdź jeden realny przykład systemu rekomendacji, który celowo wprowadził mechanizm zwiększający różnorodność. Co było motywacją - etyka, regulacje, czy biznes?",
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

REFLECTION = {
    "pl": {
        "title": "Recommendation Bubble — Refleksja",
        "cards": [
            {
                "label": "Filtrowanie kolaboratywne",
                "color": "indigo",
                "text": "Goldberg (1992): rekomenduj na podstawie ocen podobnych użytkowników. Netflix Prize (2009, 1M$): zwycięzca BellKor używał 107 modeli. Optymalizacja: engagement — nie różnorodność treści.",
            },
            {
                "label": "Bańka vs komora echa",
                "color": "orange",
                "text": "Sunstein (2017): bańka informacyjna = pasywna, algorytmiczna. Komora echa = aktywna, społeczna — sam eliminujesz odmienne głosy. Oba mechanizmy mogą współwystępować, ale są od siebie niezależne.",
            },
            {
                "label": "Diversity-aware ranking",
                "color": "green",
                "text": "Zmiana funkcji celu: minimum floor dla kategorii mniejszościowych, exposure diversity. YouTube (2019): ograniczenie zasięgu treści borderline wymagało świadomej decyzji inżynierskiej — algorytm sam się nie 'naprawił'.",
            },
        ],
        "question": "Użytkownik ogląda tylko sport. Algorytm optymalizuje engagement. Po 2 tygodniach: 98% sportu w feedzie. Jak zaprojektujesz metrykę mierzącą jednocześnie engagement i różnorodność — i co poświęcasz w kompromisie?",
    },
    "en": {
        "title": "Recommendation Bubble — Reflection",
        "cards": [
            {
                "label": "Collaborative filtering",
                "color": "indigo",
                "text": "Goldberg (1992): recommend based on ratings from similar users. Netflix Prize (2009, $1M): winner BellKor used 107 models. Optimisation target: engagement — not content diversity.",
            },
            {
                "label": "Bubble vs echo chamber",
                "color": "orange",
                "text": "Sunstein (2017): filter bubble = passive, algorithmic. Echo chamber = active, social — you yourself eliminate dissenting voices. Both mechanisms can coexist but are independent of each other.",
            },
            {
                "label": "Diversity-aware ranking",
                "color": "green",
                "text": "Changing the objective function: minimum floor for minority categories, exposure diversity. YouTube (2019): limiting reach of borderline content required a conscious engineering decision — the algorithm did not 'fix itself'.",
            },
        ],
        "question": "A user watches only sport. The algorithm optimises engagement. After 2 weeks: 98% sport in the feed. How would you design a metric that measures both engagement and diversity — and what do you sacrifice in the trade-off?",
    },
}
