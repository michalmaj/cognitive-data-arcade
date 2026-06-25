"""Lesson 20 - Anomaly Alert (anomaly detection in data visualisations)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Anomalia (outlier) to obserwacja znacznie odbiegająca od wzorca reszty danych. Może być błędem pomiaru, zdarzeniem losowym lub prawdziwym, rzadkim zjawiskiem - każdy przypadek wymaga oceny kontekstowej.",
            "Klasyczna reguła 3 sigma: w rozkładzie normalnym ponad 99.7% obserwacji leży w zakresie plus minus 3 odchylenia standardowego od średniej. Punkt poza tym zakresem jest podejrzany. W seriach czasowych EEG takie skoki to często artefakty sprzętowe (ruch mięśni, poruszenie elektrody).",
            "Kryterium Tukeya dla boxplota: outlier to punkt leżący dalej niż 1.5 x IQR (rozstęp międzykwartylowy) od krawędzi pudełka. To standardowa definicja używana przez matplotlib i większość narzędzi statystycznych. Przy skośnych rozkładach reguła 3 sigma daje za mało flag, kryterium Tukeya działa poprawniej.",
            "Izolacyjny las (Isolation Forest, Liu i in., 2008) - algorytm anomalii oparty na losowych drzewach decyzyjnych. Anomalia jest przez algorytm 'izolowana' przy mniejszej liczbie podziałów niż normalna obserwacja. Idea: rzadkie wartości leżą daleko od pozostałych, więc łatwo je odizolować.",
            "W przestrzeni 2D (scatter) anomalię oblicza się jako odległość euklidesową od centroidu grupy podzieloną przez odchylenie standardowe odległości. Punkty powyżej 2.5 sigma to anomalie - mogą wskazywać na uczestników badania z wyjątkowym profilem poznawczym.",
            "Odległość Mahalanobisa - rozszerzenie odległości euklidesowej, które uwzględnia korelacje między zmiennymi. Punkt może być blisko centroidu w każdej zmiennej z osobna, ale daleko w sensie Mahalanobisa, jeśli kombinacja wartości jest mało prawdopodobna. Stosowana w wielowymiarowej detekcji anomalii EEG.",
        ],
        "notes": [
            "Nie każda anomalia to błąd - outlier w badaniu kognitywnym może oznaczać uczestnika z wyjątkowymi zdolnościami, zmęczeniem lub inną strategią. Zawsze warto sprawdzić kontekst przed usunięciem punktu z analizy.",
            "Heatmapy korelacji EEG: anomalna komórka to potencjalny sygnał biologiczny. Przed wyciągnięciem wniosków warto sprawdzić, czy wzorzec pojawia się konsekwentnie w wielu sesjach i uczestnikach.",
        ],
        "tasks": [
            "Zagraj w Anomaly Alert - w której rundzie najtrudniej było odróżnić anomalię od normalnego punktu? Co sprawiło, że była trudna?",
            "Porównaj reguły wykrywania w rundach 1 (3 sigma) i 5 (Tukey IQR). Kiedy reguła 3 sigma zawodzi przy skośnych rozkładach?",
            "W scenariuszu z heatmapą EEG: czy anomalne komórki powinny być usuwane automatycznie? Jakie argumenty przemawiają za ręczną inspekcją każdego przypadku?",
        ],
    },
    "en": {
        "theory": [
            "An anomaly (outlier) is an observation that deviates significantly from the pattern of the rest of the data. It may be a measurement error, a random event, or a genuine rare phenomenon - each case requires contextual judgement.",
            "The classic 3-sigma rule: in a normal distribution, over 99.7% of observations fall within plus or minus 3 standard deviations of the mean. A point outside this range is suspicious. In EEG time series, such spikes are typically hardware artefacts (muscle movement, electrode displacement).",
            "Tukey's criterion for box plots: an outlier is a point further than 1.5 x IQR (interquartile range) from the box edge. This is the standard definition used by matplotlib and most statistical tools. For skewed distributions the 3-sigma rule produces too few flags, whereas Tukey's criterion performs more reliably.",
            "Isolation Forest (Liu et al., 2008) - an anomaly detection algorithm based on random decision trees. An anomaly is 'isolated' by the algorithm in fewer splits than a normal observation. The intuition: rare values lie far from others, so they are easy to isolate.",
            "In 2D scatter space, an outlier is calculated as the Euclidean distance from the group centroid divided by the standard deviation of distances. Points above 2.5 sigma are anomalies - they may indicate participants with an exceptional cognitive profile.",
            "Mahalanobis distance - an extension of Euclidean distance that accounts for correlations among variables. A point may be close to the centroid in each variable individually but far in the Mahalanobis sense if the combination of values is unlikely. Used in multi-dimensional EEG anomaly detection.",
        ],
        "notes": [
            "Not every anomaly is an error - an outlier in a cognitive study may indicate a participant with exceptional ability, fatigue, or a different strategy. Context should always be checked before removing a point from analysis.",
            "EEG correlation heatmaps: an anomalous cell is a potential biological signal. Before drawing conclusions, it is worth checking whether the pattern appears consistently across multiple sessions and participants.",
        ],
        "tasks": [
            "Play Anomaly Alert - in which round was it hardest to distinguish an anomaly from a normal point? What made it difficult?",
            "Compare detection rules in rounds 1 (3-sigma) and 5 (Tukey IQR). When does the 3-sigma rule fail for skewed distributions?",
            "In the EEG heatmap scenario: should anomalous cells be removed automatically? What arguments support manual inspection of each case?",
        ],
    },
}
