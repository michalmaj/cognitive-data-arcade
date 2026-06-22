"""Lesson 02 - Reaction Time (RT Lab)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Czas reakcji (RT) to odstęp między bodźcem a odpowiedzią, mierzony w milisekundach. RT nie jest jedną operacją - składa się z detekcji sygnału, decyzji i wykonania motorycznego.",
            "Metoda odejmowania Dondersa (1868) - zmierz RT w dwóch warunkach różniących się jedną operacją umysłową. Różnica = koszt czasowy tej operacji. Pierwszy eksperymentalny dowód, że myślenie zajmuje mierzalny czas.",
            "Dlaczego mediana, nie średnia - rozkłady RT są skośne prawostronnie. Kilka wolnych odpowiedzi (rozproszenie, antycypacja) bardzo zawyża średnią. Mediana jest odporna na wartości skrajne.",
            "Typowe wartości - prosty RT wzrokowy: 180-250 ms. Słuchowy: 140-200 ms. Wybór RT (2 opcje): 350-500 ms. Stroop niezgodny: 700-1000 ms. Wartości rosną z wiekiem i zmęczeniem.",
            "Co zaburza RT - zmęczenie (+10-30 ms), kofeina (-10 ms), wiek (~1 ms/rok po 25. r.ż.), obciążenie poznawcze (zadanie dodatkowe wydłuża RT w obu zadaniach jednocześnie).",
            "Kierowcy Formuły 1 reagują w okolicach 200 ms - to i tak wolniej niż mimowolne mruganie okiem (100-150 ms). Mózg nie przetwarza wzroku tak szybko jak odruchy rdzeniowe, bo sygnał musi dotrzeć do kory wzrokowej w płacie potylicznym i wrócić do kory ruchowej.",
            "Hermann von Helmholtz zmierzył w 1850 roku prędkość impulsu nerwowego na nerwie żaby i uzyskał 30-70 m/s. Wynik był zaskakujący - spodziewano się prędkości bliskiej światłu. To był pierwszy eksperymentalny dowód, że myślenie i percepcja mają fizyczne ograniczenia czasowe.",
            "Prawo Hicka-Hymana (1952) - RT rośnie logarytmicznie z liczbą możliwych opcji odpowiedzi. Wybór spośród 2 opcji zajmuje ok. 350 ms, spośród 4 opcji - ok. 450 ms, spośród 8 opcji - ok. 500 ms. To dlatego proste interfejsy są szybsze w obsłudze.",
        ],
        "notes": [
            "Jak czytać histogram RT - szczyt to typowy czas reakcji. Ogon w prawo to wolne próby (rozproszenie). Wartości poniżej 100 ms to antycypacje, nie prawdziwe reakcje - naciśnięto przed bodźcem.",
            "Efekt ćwiczenia - RT typowo maleje przez pierwsze kilka bloków w miarę rozgrzewania się. Porównuj bloki między sobą, nie tylko całą sesję, żeby zobaczyć ten efekt.",
            "Wartości odstające - odpowiedzi > 1000 ms to prawdopodobnie rozproszenie uwagi. Odpowiedzi < 100 ms to antycypacje. Oba typy zniekształcają analizę i warto je odfiltrować.",
            "Bardzo wolne próby (> 800 ms) to prawie zawsze zjawisko uwagowego 'odpływu' - przez ułamek sekundy uwaga była skupiona na czymś innym. To nie błąd pomiaru, lecz właściwość układu uwagi.",
        ],
        "tasks": [
            "Jaki jest medianowy RT? Porównaj go z wartościami typowymi (180-250 ms). Czy wynik mieści się w normie i co mogło na niego wpłynąć?",
            "Porównaj RT w pierwszym i ostatnim bloku. Czy widoczny jest efekt ćwiczenia? O ile milisekund zmienił się RT między początkiem a końcem sesji?",
            "Znajdź najszybszą i najwolniejszą próbę. Jak duża jest ta różnica? Co mogło wpłynąć na wolną próbę - rozproszenie, zmęczenie, czy antycypacja?",
        ],
    },
    "en": {
        "theory": [
            "Reaction time (RT) is the interval between a stimulus and a response, measured in milliseconds. RT is not a single operation - it comprises signal detection, decision-making, and motor execution.",
            "Donders' subtraction method (1868) - measure RT in two conditions differing by one mental operation. The difference is the time cost of that operation. The first experimental proof that thinking takes measurable time.",
            "Why median, not mean - RT distributions are right-skewed. A few slow responses (distraction, anticipation) inflate the mean greatly. The median is robust to extreme values.",
            "Typical values - simple visual RT: 180-250 ms. Auditory: 140-200 ms. Choice RT (2 options): 350-500 ms. Stroop incongruent: 700-1000 ms. Values increase with age and fatigue.",
            "What affects RT - fatigue (+10-30 ms), caffeine (-10 ms), age (~1 ms/year after 25), cognitive load (a secondary task slows RT in both tasks simultaneously).",
            "Formula 1 drivers react in around 200 ms - still slower than an involuntary eye blink (100-150 ms). The brain does not process vision as fast as spinal reflexes, because the signal must reach the visual cortex in the occipital lobe and return to the motor cortex.",
            "Hermann von Helmholtz measured the speed of a nerve impulse in a frog nerve in 1850 and obtained 30-70 m/s. The result was surprising - speeds close to that of light had been expected. This was the first experimental proof that thinking and perception have physical time limits.",
            "Hick-Hyman law (1952) - RT grows logarithmically with the number of possible response options. Choosing between 2 options takes about 350 ms, 4 options about 450 ms, 8 options about 500 ms. This is why simple interfaces are faster to use.",
        ],
        "notes": [
            "How to read an RT histogram - the peak is the typical reaction time. The right tail is slow trials (distraction). Values below 100 ms are anticipations, not true reactions - the key was pressed before the stimulus.",
            "Practice effect - RT typically decreases over the first few blocks as you warm up. Compare blocks against each other, not just the whole session, to see this effect.",
            "Outliers - responses > 1000 ms are likely distraction. Responses < 100 ms are anticipations. Both distort analysis and are worth filtering out.",
            "Very slow trials (> 800 ms) are almost always attentional 'drift' - for a fraction of a second attention was focused on something else. This is not a measurement error, but a property of the attention system.",
        ],
        "tasks": [
            "What is the median RT? Compare it to typical values (180-250 ms). Does the result fall within the normal range and what might have influenced it?",
            "Compare RT in the first and last block. Is a practice effect visible? By how many milliseconds did RT change from the start to the end of the session?",
            "Find the fastest and slowest trial. How large is the difference? What might have caused the slow trial - distraction, fatigue, or anticipation?",
        ],
    },
}
