"""Lesson 02 — Reaction Time (RT Lab)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Czas reakcji (RT) to odstęp między bodźcem a odpowiedzią, mierzony w milisekundach. RT nie jest jedną operacją — składa się z detekcji sygnału, decyzji i wykonania motorycznego.",
            "Metoda odejmowania Dondersa (1868) — zmierz RT w dwóch warunkach różniących się jedną operacją umysłową. Różnica = koszt czasowy tej operacji. Pierwszy eksperymentalny dowód, że myślenie zajmuje mierzalny czas.",
            "Dlaczego mediana, nie średnia — rozkłady RT są skośne prawostronnie. Kilka wolnych odpowiedzi (rozproszenie, antycypacja) bardzo zawyża średnią. Mediana jest odporna na wartości skrajne.",
            "Typowe wartości — prosty RT wzrokowy: 180–250 ms. Słuchowy: 140–200 ms. Wybór RT (2 opcje): 350–500 ms. Stroop niezgodny: 700–1000 ms. Wartości rosną z wiekiem i zmęczeniem.",
            "Co zaburza RT — zmęczenie (+10–30 ms), kofeina (−10 ms), wiek (~1 ms/rok po 25. r.ż.), obciążenie poznawcze (zadanie dodatkowe wydłuża RT w obu zadaniach jednocześnie).",
        ],
        "notes": [
            "Jak czytać histogram RT — szczyt to Twój typowy czas reakcji. Ogon w prawo to wolne próby (rozproszenie). Wartości poniżej 100 ms to antycypacje, nie prawdziwe reakcje — naciśnięto przed bodźcem.",
            "Efekt ćwiczenia — RT typowo maleje przez pierwsze kilka bloków w miarę rozgrzewania się. Porównuj bloki między sobą, nie tylko całą sesję, żeby zobaczyć ten efekt.",
            "Wartości odstające — odpowiedzi > 1000 ms to prawdopodobnie rozproszenie uwagi. Odpowiedzi < 100 ms to antycypacje. Oba typy zniekształcają analizę i warto je odfiltrować.",
        ],
        "tasks": [
            "Jaki jest Twój medianowy RT? Porównaj go z wartościami typowymi (180–250 ms). Czy jesteś szybszy czy wolniejszy? Co mogło wpłynąć na Twój wynik?",
            "Porównaj swój RT w pierwszym i ostatnim bloku. Czy widzisz efekt ćwiczenia? O ile milisekund skrócił się Twój RT między początkiem a końcem sesji?",
            "Znajdź swoją najszybszą i najwolniejszą próbę. Jak duża jest ta różnica? Co mogło wpłynąć na wolną próbę — rozproszenie, zmęczenie, czy coś innego?",
        ],
    },
    "en": {
        "theory": [
            "Reaction time (RT) is the interval between a stimulus and a response, measured in milliseconds. RT is not a single operation — it comprises signal detection, decision-making, and motor execution.",
            "Donders' subtraction method (1868) — measure RT in two conditions differing by one mental operation. The difference is the time cost of that operation. The first experimental proof that thinking takes measurable time.",
            "Why median, not mean — RT distributions are right-skewed. A few slow responses (distraction, anticipation) inflate the mean greatly. The median is robust to extreme values.",
            "Typical values — simple visual RT: 180–250 ms. Auditory: 140–200 ms. Choice RT (2 options): 350–500 ms. Stroop incongruent: 700–1000 ms. Values increase with age and fatigue.",
            "What affects RT — fatigue (+10–30 ms), caffeine (−10 ms), age (~1 ms/year after 25), cognitive load (a secondary task slows RT in both tasks simultaneously).",
        ],
        "notes": [
            "How to read an RT histogram — the peak is your typical reaction time. The right tail is slow trials (distraction). Values below 100 ms are anticipations, not true reactions — the key was pressed before the stimulus.",
            "Practice effect — RT typically decreases over the first few blocks as you warm up. Compare blocks against each other, not just the whole session, to see this effect.",
            "Outliers — responses > 1000 ms are likely distraction. Responses < 100 ms are anticipations. Both distort analysis and are worth filtering out.",
        ],
        "tasks": [
            "What is your median RT? Compare it to typical values (180–250 ms). Are you faster or slower? What might have influenced your result?",
            "Compare your RT in the first and last block. Do you see a practice effect? By how many milliseconds did your RT decrease from start to finish?",
            "Find your fastest and slowest trial. How large is the difference? What might have caused the slow trial — distraction, fatigue, or something else?",
        ],
    },
}
