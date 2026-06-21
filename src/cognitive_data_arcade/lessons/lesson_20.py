# src/cognitive_data_arcade/lessons/lesson_20.py
"""Lesson 20 - Anomaly Alert (anomaly detection in data visualisations)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Anomalia (outlier) to obserwacja znacznie odbiegajaca od wzorca reszty danych. "
            "Moze byc bledem pomiaru, zdarzeniem losowym lub prawdziwym, rzadkim zjawiskiem -- "
            "kazdy przypadek wymaga oceny kontekstowej.",
            "Klasyczna regula 3 sigma: w rozkladzie normalnym ponad 99.7% obserwacji lezy w zakresie "
            "plus minus 3 odchylenia standardowego od sredniej. Punkt poza tym zakresem jest podejrzany. "
            "W seriach czasowych takie skoki to czesto artefakty sprzętowe.",
            "Kryterium Tukeya dla boxplota: outlier to punkt lezacy dalej niz "
            "1.5 x IQR (rozstep miedzikwartylowy) od krawedzi pudelka. "
            "To standardowa definicja uzywana przez matplotlib i wiekszosc narzedzi statystycznych.",
            "W przestrzeni 2D (scatter) outlier oblicza sie jako odleglosc euklidesowa od centroidu grupy "
            "podzielona przez odchylenie standardowe odleglosci. Punkty powyzej 2.5 sigma to anomalie -- "
            "moga wskazywac na uczestnikow badania z wyjatkowym profilem poznawczym.",
        ],
        "notes": [
            "Nie kazda anomalia to blad! Outlier w badaniu kognitywnym moze oznaczac "
            "uczestnika z wyjatkowymi zdolnosciami, zmeczeniem lub inna strategia. "
            "Zawsze sprawdz kontekst przed usunieciem punktu z analizy.",
            "Heatmapy korelacji EEG: anomalna komorka to potencjalny sygnal biologiczny. "
            "Przed wyciagnieciem wnioskow sprawdz, czy wzorzec pojawia sie konsekwentnie "
            "w wielu sesjach i uczestnikach.",
        ],
        "tasks": [
            "Zagraj w Anomaly Alert -- w ktorej rundzie najtrudniej bylo odroznic "
            "anomalie od normalnego punktu? Co sprawilo, ze byla trudna?",
            "Porownaj reguly wykrywania w rundach 1 (3 sigma) i 5 (Tukey IQR). "
            "Kiedy regula 3 sigma zawodzi przy skosnych rozkladach?",
            "Wyobraz sobie, ze jestes badaczem EEG. Czy usunałbyś anomalne komorki "
            "z macierzy korelacji automatycznie? Uzasadnij odpowiedz.",
        ],
    },
    "en": {
        "theory": [
            "An anomaly (outlier) is an observation that deviates significantly from the pattern "
            "of the rest of the data. It may be a measurement error, a random event, or a genuine "
            "rare phenomenon -- each case requires contextual judgement.",
            "The classic 3-sigma rule: in a normal distribution, over 99.7% of observations fall within "
            "plus or minus 3 standard deviations of the mean. A point outside this range is suspicious. "
            "In time series, such spikes are often hardware artefacts.",
            "Tukey's criterion for box plots: an outlier is a point further than "
            "1.5 times IQR (interquartile range) from the box edge. "
            "This is the standard definition used by matplotlib and most statistical tools.",
            "In 2D scatter space, an outlier is the Euclidean distance from the group centroid "
            "divided by the standard deviation of distances. Points above 2.5 sigma are anomalies -- "
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
            "Play Anomaly Alert -- in which round was it hardest to distinguish "
            "an anomaly from a normal point? What made it difficult?",
            "Compare detection rules in rounds 1 (3-sigma) and 5 (Tukey IQR). "
            "When does the 3-sigma rule fail for skewed distributions?",
            "Imagine you are an EEG researcher. Would you remove anomalous cells "
            "from the correlation matrix automatically? Justify your answer.",
        ],
    },
}
