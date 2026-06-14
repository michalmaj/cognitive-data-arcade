"""Lesson 18 — Classifier Battle (decision boundaries and classifier intuition)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Klasyfikator to algorytm, który przypisuje każdemu punktowi danych jedną z predefiniowanych klas. "
            "Granica decyzyjna to linia (lub hiperpowierzchnia), która dzieli przestrzeń cech na obszary odpowiadające różnym klasom.",
            "Klasyfikator liniowy (np. regresja logistyczna) zakłada, że klasy można rozdzielić prostą linią. "
            "Działa świetnie, gdy dane są liniowo separowalne, ale zawodzi na kształtach takich jak półksiężyce czy koncentryczne kółka.",
            "KNN (K najbliższych sąsiadów) klasyfikuje punkt na podstawie klas jego k najbliższych sąsiadów. "
            "Może tworzyć bardzo giętkie, nieliniowe granice — jest mocniejszy od regresji logistycznej na skomplikowanych danych.",
            "Drzewo decyzyjne dzieli przestrzeń seriami prostopadłych cięć. "
            "Łatwo interpretować jego decyzje, ale przy dużej głębokości skłonne do overfittingu.",
        ],
        "notes": [
            "Overfitting to zjawisko, gdy model zbyt dokładnie dopasowuje się do danych treningowych i źle generalizuje. "
            "Zbyt giętka granica decyzyjna może być symptomem overfittingu.",
            "Walidacja krzyżowa (cross-validation) ocenia model na różnych podzbiorach danych, "
            "dając bardziej wiarygodny obraz rzeczywistej dokładności niż jednorazowy podział na trening/test.",
        ],
        "tasks": [
            "Zagraj w Classifier Battle — w której rundzie najtrudniej było Ci narysować granicę? Dlaczego?",
            "Porównaj swoje wyniki z KNN: kiedy Ty wygrywasz, a kiedy KNN był lepszy?",
            "Wyjaśnij własnymi słowami, dlaczego klasyfikator liniowy nie radzi sobie z danymi w kształcie kółek.",
        ],
    },
    "en": {
        "theory": [
            "A classifier is an algorithm that assigns each data point to one of several predefined classes. "
            "A decision boundary is the line (or hyperplane) that divides the feature space into regions for each class.",
            "A linear classifier (e.g. logistic regression) assumes classes can be separated by a straight line. "
            "It works well when data is linearly separable but fails on shapes like moons or concentric circles.",
            "KNN (K-Nearest Neighbours) classifies a point based on the classes of its k closest neighbours. "
            "It can form very flexible, non-linear boundaries and is stronger than logistic regression on complex data.",
            "A decision tree splits the feature space with perpendicular cuts. "
            "Its decisions are easy to interpret, but deep trees are prone to overfitting.",
        ],
        "notes": [
            "Overfitting occurs when a model fits training data too closely and generalises poorly. "
            "An overly flexible decision boundary can be a symptom of overfitting.",
            "Cross-validation evaluates a model on different data subsets, "
            "giving a more reliable accuracy estimate than a single train/test split.",
        ],
        "tasks": [
            "Play Classifier Battle — in which round was it hardest to draw a boundary, and why?",
            "Compare your results to KNN: when did you win, and when was KNN better?",
            "Explain in your own words why a linear classifier fails on circle-shaped data.",
        ],
    },
}
