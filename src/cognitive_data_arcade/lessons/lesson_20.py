# src/cognitive_data_arcade/lessons/lesson_20.py
"""Lesson 20 - Anomaly Alert (anomaly detection in data visualisations)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Anomalia (outlier) to obserwacja znacznie odbiegająca od wzorca reszty danych. "
            "Może być błędem pomiaru, zdarzeniem losowym lub prawdziwym, rzadkim zjawiskiem - "
            "każdy przypadek wymaga oceny kontekstowej.",
            "Klasyczna reguła 3 sigma: w rozkładzie normalnym ponad 99.7% obserwacji leży w zakresie "
            "plus minus 3 odchylenia standardowego od średniej. Punkt poza tym zakresem jest podejrzany. "
            "W seriach czasowych takie skoki to często artefakty sprzętowe.",
            "Kryterium Tukeya dla boxplota: outlier to punkt leżący dalej niż "
            "1.5 x IQR (rozstęp międzykwartylowy) od krawędzi pudełka. "
            "To standardowa definicja używana przez matplotlib i większość narzędzi statystycznych.",
            "W przestrzeni 2D (scatter) outlier oblicza się jako odległość euklidesową od centroidu grupy "
            "podzieloną przez odchylenie standardowe odległości. Punkty powyżej 2.5 sigma to anomalie - "
            "mogą wskazywać na uczestników badania z wyjątkowym profilem poznawczym.",
        ],
        "notes": [
            "Nie każda anomalia to błąd! Outlier w badaniu kognitywnym może oznaczać "
            "uczestnika z wyjątkowymi zdolnościami, zmęczeniem lub inną strategią. "
            "Zawsze sprawdź kontekst przed usunięciem punktu z analizy.",
            "Heatmapy korelacji EEG: anomalna komórka to potencjalny sygnał biologiczny. "
            "Przed wyciągnięciem wniosków sprawdź, czy wzorzec pojawia się konsekwentnie "
            "w wielu sesjach i uczestnikach.",
        ],
        "tasks": [
            "Zagraj w Anomaly Alert - w której rundzie najtrudniej było odróżnić "
            "anomalię od normalnego punktu? Co sprawiło, że była trudna?",
            "Porównaj reguły wykrywania w rundach 1 (3 sigma) i 5 (Tukey IQR). "
            "Kiedy reguła 3 sigma zawodzi przy skośnych rozkładach?",
            "Wyobraź sobie, że jesteś badaczem EEG. Czy usunąłbyś anomalne komórki "
            "z macierzy korelacji automatycznie? Uzasadnij odpowiedź.",
        ],
    },
    "en": {
        "theory": [
            "An anomaly (outlier) is an observation that deviates significantly from the pattern "
            "of the rest of the data. It may be a measurement error, a random event, or a genuine "
            "rare phenomenon - each case requires contextual judgement.",
            "The classic 3-sigma rule: in a normal distribution, over 99.7% of observations fall within "
            "plus or minus 3 standard deviations of the mean. A point outside this range is suspicious. "
            "In time series, such spikes are often hardware artefacts.",
            "Tukey's criterion for box plots: an outlier is a point further than "
            "1.5 times IQR (interquartile range) from the box edge. "
            "This is the standard definition used by matplotlib and most statistical tools.",
            "In 2D scatter space, an outlier is the Euclidean distance from the group centroid "
            "divided by the standard deviation of distances. Points above 2.5 sigma are anomalies - "
            "they may indicate participants with an exceptional cognitive profile.",
        ],
        "notes": [
            "Not every anomaly is an error! An outlier in a cognitive study may indicate "
            "a participant with exceptional ability, fatigue, or a different strategy. "
            "Always check context before removing a point from the analysis.",
            "EEG correlation heatmaps: an anomalous cell is a potential biological signal. "
            "Before drawing conclusions, check whether the pattern appears consistently "
            "across multiple sessions and participants.",
        ],
        "tasks": [
            "Play Anomaly Alert - in which round was it hardest to distinguish "
            "an anomaly from a normal point? What made it difficult?",
            "Compare detection rules in rounds 1 (3-sigma) and 5 (Tukey IQR). "
            "When does the 3-sigma rule fail for skewed distributions?",
            "Imagine you are an EEG researcher. Would you remove anomalous cells "
            "from the correlation matrix automatically? Justify your answer.",
        ],
    },
}
