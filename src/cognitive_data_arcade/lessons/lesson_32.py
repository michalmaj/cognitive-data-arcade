"""Lesson 32 -- The Architect's Trial (AI ethics and algorithmic decision-making)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Algorytmiczne podejmowanie decyzji (ADM) pojawia się w sytuacjach, "
            "gdy system AI zastępuje lub wspiera człowieka w decyzjach o wysokich "
            "stawkach: kto dostanie kredyt, kto trafi do więzienia, kto zostanie "
            "zatrudniony. EU AI Act (2024) definiuje 'systemy wysokiego ryzyka' "
            "i nakłada na nie obowiązek dokumentacji, audytu i nadzoru ludzkiego.",

            "Matematyczna niemożliwość: nie można jednocześnie spełnić trzech "
            "najpopularniejszych definicji sprawiedliwości algorytmicznej. "
            "Parytet demograficzny (równe wskaźniki aprobaty między grupami), "
            "równe szanse (równe TPR między grupami) i kalibracja (równe prawdopodobieństwa "
            "predykcyjne) są wzajemnie sprzeczne gdy grupy mają różne rozkłady bazowe. "
            "Wybór kryterium to decyzja polityczna, nie techniczna.",

            "EU AI Act klasyfikuje systemy AI według ryzyka. Systemy 'wysokiego ryzyka' "
            "(rekrutacja, edukacja, opieka społeczna, wymiar sprawiedliwości) muszą mieć: "
            "dokumentację techniczną, rejestr zdarzeń, mechanizm nadzoru ludzkiego, "
            "przejrzyste informowanie osób, których dotyczą decyzje. "
            "Brak compliance może skutkować karą do 30 mln EUR lub 6% obrotu.",

            "Efekt Goodharta: 'Kiedy miara staje się celem, przestaje być dobra miara' "
            "(Charles Goodhart, 1975). Klasyczne przykłady w AI: system rekrutacyjny "
            "optymalizowany pod retencję zaczyna odrzucać kandydatów ze złożonymi "
            "życiorysami; system medyczny optymalizowany pod śmiertelność wybiera "
            "pacjentów o najlepszych rokowaniach; algorytm rekomendacji optymalizowany "
            "pod engagement maksymalizuje outrage bo outrage trzyma użytkowników dłużej.",
        ],
        "notes": [
            "Cathy O'Neil 'Weapons of Math Destruction' (2016): autorka, matematyczka "
            "i była analityczka hedge-fund, opisuje jak pozornie neutralne modele "
            "matematyczne wzmacniają nierówności społeczne. Trzy cechy 'broni': "
            "nieprzejrzystość (black box), skala (miliony decyzji), destrukcyjność "
            "(dotykają najbardziej wrażliwe grupy). Przykłady: scoring kredytowy, "
            "ocena nauczycieli, rekrutacja w korporacjach.",

            "COMPAS (Correctional Offender Management Profiling for Alternative "
            "Sanctions): algorytm używany w USA do oceny ryzyka recydywy przy "
            "decyzjach o zwolnieniu warunkowym. ProPublica (2016) wykazała: "
            "algorytm błędnie klasyfikuje czarnych oskarżonych jako 'wysokie ryzyko' "
            "dwukrotnie częściej niż białych (45% vs 24% false positives). "
            "Northpointe (producent) odpowiedział: accuracy jest równa między grupami. "
            "Oba twierdzenia są matematycznie prawdziwe -- to jest właśnie impossibility theorem.",
        ],
        "tasks": [
            "Który z Twoich wyborów projektowych najbardziej zaskoczył Cię konsekwencjami? "
            "Dlaczego go podjąłeś -- co wydawało się wtedy oczywiste lub bezpieczne?",

            "Wyobraź sobie że jesteś w grupie demograficznej, która 'przegrała' na Twoim "
            "systemie. Jak czujesz się wiedząc że algorytm oceniał Cię bez Twojej wiedzy, "
            "na podstawie danych, których istnienia możesz nie być świadomy?",

            "Czy istnieje kombinacja decyzji projektowych, która zadowala wszystkich trzech "
            "sędziów komisji jednocześnie? Sprawdź to grając jeszcze raz. "
            "Co mówi wynik o naturze kompromisów w projektowaniu systemów AI?",
        ],
    },
    "en": {
        "theory": [
            "Algorithmic Decision Making (ADM) arises when an AI system replaces or "
            "assists humans in high-stakes decisions: who gets credit, who goes to prison, "
            "who gets hired. The EU AI Act (2024) defines 'high-risk systems' and imposes "
            "documentation, auditing, and human oversight requirements on them.",

            "Mathematical impossibility: you cannot simultaneously satisfy the three most "
            "popular definitions of algorithmic fairness. Demographic parity (equal approval "
            "rates across groups), equal opportunity (equal TPR across groups), and "
            "calibration (equal predictive probabilities) are mutually exclusive when groups "
            "have different base rates. Choosing a criterion is a political, not technical, "
            "decision.",

            "The EU AI Act classifies AI systems by risk level. 'High-risk' systems "
            "(recruitment, education, social services, justice) must have: technical "
            "documentation, event logs, human oversight mechanisms, and transparent "
            "notification of affected individuals. Non-compliance can result in fines up to "
            "EUR 30 million or 6% of turnover.",

            "Goodhart's Law: 'When a measure becomes a target, it ceases to be a good "
            "measure' (Charles Goodhart, 1975). Classic AI examples: a recruitment system "
            "optimized for retention starts rejecting candidates with complex CVs; a medical "
            "system optimized for mortality selects patients with the best prognoses; a "
            "recommendation algorithm optimized for engagement maximizes outrage because "
            "outrage keeps users on the platform longer.",
        ],
        "notes": [
            "Cathy O'Neil 'Weapons of Math Destruction' (2016): the author, a mathematician "
            "and former hedge-fund analyst, describes how seemingly neutral mathematical "
            "models amplify social inequalities. Three features of 'weapons': opacity "
            "(black box), scale (millions of decisions), destructiveness (disproportionately "
            "affecting vulnerable groups). Examples: credit scoring, teacher evaluation, "
            "corporate recruitment.",

            "COMPAS (Correctional Offender Management Profiling for Alternative Sanctions): "
            "an algorithm used in the US to assess recidivism risk for parole decisions. "
            "ProPublica (2016) showed: the algorithm incorrectly classifies Black defendants "
            "as 'high risk' twice as often as white defendants (45% vs 24% false positives). "
            "Northpointe (the developer) responded: accuracy is equal across groups. "
            "Both claims are mathematically true -- this is precisely the impossibility "
            "theorem in action.",
        ],
        "tasks": [
            "Which of your design choices surprised you most with its consequences? "
            "Why did you make it -- what seemed obvious or safe at the time?",

            "Imagine you belong to the demographic group that 'lost' under your system. "
            "How do you feel knowing that an algorithm evaluated you without your knowledge, "
            "based on data whose existence you may not have been aware of?",

            "Is there a combination of design decisions that satisfies all three committee "
            "judges simultaneously? Try playing again to find out. "
            "What does the result say about the nature of tradeoffs in AI system design?",
        ],
    },
}
