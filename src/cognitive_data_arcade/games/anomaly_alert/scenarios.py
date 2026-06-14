# src/cognitive_data_arcade/games/anomaly_alert/scenarios.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name_pl: str
    chart_type: str   # timeseries | barchart | scatter | histogram | boxplot | heatmap
    n_anomalies: int
    hint_pl: str      # right-click popup text
    insight_pl: str   # post-round explanation


SCENARIOS: list[Scenario] = [
    Scenario(
        name_pl="Tętno sportowca",
        chart_type="timeseries",
        n_anomalies=2,
        hint_pl=(
            "Szukaj gwałtownych skoków lub spadków tętna, które wyraźnie odstają od "
            "normalnego rytmu. Anomalie przekraczają 3 odchylenia standardowe od "
            "średniej — są jak błyskawica na tle spokojnego sygnału."
        ),
        insight_pl=(
            "Zaznaczone punkty leżą ponad 3σ od średniej tętna. W biosygnałach "
            "tak nagłe zmiany to często artefakty sprzętowe lub chwilowe "
            "zaburzenia rytmu serca — warte szczególnej uwagi diagnostycznej."
        ),
    ),
    Scenario(
        name_pl="Wyniki uczestników",
        chart_type="barchart",
        n_anomalies=2,
        hint_pl=(
            "Porównaj wysokości słupków. Szukaj uczestników, których wynik jest "
            "ponad 4× wyższy niż średnia pozostałych. Tak duże odchylenie sugeruje "
            "błąd pomiaru lub wyjątkowe warunki końcowych pomiarów."
        ),
        insight_pl=(
            "Te słupki sięgają ponad 4× średnią grupy. Mogą oznaczać błąd "
            "w zbieraniu danych, specjalną grupę lub wpływ czynników zewnętrznych. "
            "Taki wynik zawsze warto sprawdzić przed dalszą analizą."
        ),
    ),
    Scenario(
        name_pl="Czas reakcji vs dokładność",
        chart_type="scatter",
        n_anomalies=2,
        hint_pl=(
            "Obserwuj chmurę punktów w przestrzeni 2D. Anomalie to punkty "
            "leżące ponad 2.5 odchylenia standardowego od środka tej chmury. "
            "Szukaj punktów wyraźnie oderwanych od gęstego skupiska."
        ),
        insight_pl=(
            "Izolowane punkty daleko od skupiska to outliery w przestrzeni 2D. "
            "Ich odległość od środka grupy przekracza 2.5σ — mogą wskazywać "
            "na uczestników z bardzo różnym poziomem skupienia lub zmęczenia."
        ),
    ),
    Scenario(
        name_pl="Rozkład czasów odpowiedzi",
        chart_type="histogram",
        n_anomalies=2,
        hint_pl=(
            "Obserwuj kształt rozkładu. Anomalie to izolowane słupki w dalekim "
            "ogonie, oddzielone pustą przestrzenią od reszty danych. "
            "Źródło takich wartości to często zdarzenia losowe lub rozproszenia."
        ),
        insight_pl=(
            "Izolowane słupki w ogonie rozkładu wskazują na rzadkie zdarzenia — "
            "np. bardzo długi czas namysłu lub chwilowe rozproszenie uwagi. "
            "W analizie RT standardowo usuwa się wartości ponad 3σ od średniej."
        ),
    ),
    Scenario(
        name_pl="Porównanie grup",
        chart_type="boxplot",
        n_anomalies=2,
        hint_pl=(
            "Wąsy boxplota obejmują zakres do 1.5× rozstępu międzykwartylowego. "
            "Szukaj pojedynczych punktów leżących tuż poza wąsami — "
            "to klasyczne outliery według kryterium Tukeya."
        ),
        insight_pl=(
            "Punkty poza wąsami spełniają kryterium Tukeya: leżą dalej niż "
            "1.5× IQR od pudełka. Taki punkt warto zbadać — może to błąd "
            "lub uczestnik z wyjątkowym profilem poznawczym."
        ),
    ),
    Scenario(
        name_pl="Macierz EEG",
        chart_type="heatmap",
        n_anomalies=2,
        hint_pl=(
            "Każda komórka macierzy to korelacja między obszarem mózgu "
            "a warunkiem eksperymentu. Anomalia różni się od średniej "
            "swojego wiersza o ponad 2 odchylenia standardowe."
        ),
        insight_pl=(
            "Anomalne komórki mają wartości ponad 2σ od średniej wiersza — "
            "mogą świadczyć o nieoczekiwanej zależności między obszarem mózgu "
            "a warunkiem, wartej głębszej analizy źródłowej."
        ),
    ),
]
