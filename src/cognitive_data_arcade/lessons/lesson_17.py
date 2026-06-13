"""Lesson 17 -- Feature Hunter (feature selection intuition)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Nie każda cecha danych pomaga modelowi — niektóre są szumem. Cecha-szum nie ma żadnego związku ze zmienną docelową. Dodanie jej do modelu może pogorszyć jego działanie.",
            "Korelacja (r) mierzy siłę i kierunek związku liniowego między cechą a celem. r bliskie 1 lub -1 = silny związek. r bliskie 0 = brak związku = prawdopodobnie szum.",
            "Selekcja cech (feature selection) to wybór podzbioru cech, które najlepiej przewidują wynik. Mniej cech — prostszy model, mniejsze ryzyko przeuczenia (overfitting).",
            "Scatter plot to Twój najlepszy przyjaciel przy selekcji cech. Szukaj wizualnego trendu: jeśli punkty idą w górę lub w dół względem osi X — cecha jest przydatna.",
        ],
        "notes": [
            "Silna korelacja |r| > 0.5 to dobry sygnał, ale sama korelacja nie wystarczy — sprawdzaj też sens merytoryczny.",
            "Korelacja mierzy tylko związki liniowe. Cecha może być przydatna nieliniowo nawet gdy r bliskie 0.",
        ],
        "tasks": [
            "Zagraj w Feature Hunter na poziomie Easy — ile cech poprawnie zidentyfikowałeś?",
            "Spróbuj poziomu Hard — które cechy cię zaskoczyły? Dlaczego?",
            "Wypisz 3 cechy ze swojego własnego zbioru danych, które mogłyby być szumem, i wyjaśnij dlaczego.",
        ],
    },
    "en": {
        "theory": [
            "Not every data feature helps a model — some are noise. A noise feature has no relationship with the target variable. Adding it can hurt model performance.",
            "Correlation (r) measures the strength and direction of a linear relationship between a feature and the target. r near 1 or -1 = strong relationship. r near 0 = no relationship = likely noise.",
            "Feature selection is the process of choosing a subset of features that best predict the outcome. Fewer features means a simpler model and lower risk of overfitting.",
            "A scatter plot is your best friend for feature selection. Look for a visual trend: if points go up or down along the X axis — the feature is useful.",
        ],
        "notes": [
            "Strong correlation |r| > 0.5 is a good signal, but correlation alone is not enough — also check domain logic.",
            "Correlation only measures linear relationships. A feature can be useful in a non-linear way even when r is near 0.",
        ],
        "tasks": [
            "Play Feature Hunter on Easy — how many features did you correctly identify?",
            "Try Hard mode — which features surprised you, and why?",
            "List 3 features from your own dataset that might be noise and explain why.",
        ],
    },
}
