"""Lesson 18 - Classifier Battle (decision boundaries and classifier intuition)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Klasyfikator to algorytm, który przypisuje każdemu punktowi danych jedną z predefiniowanych klas. Granica decyzyjna to linia (lub hiperpowierzchnia), która dzieli przestrzeń cech na obszary odpowiadające różnym klasom.",
            "Perceptron (Rosenblatt, 1958) - pierwszy uczący sie klasyfikator. Frank Rosenblatt zbudował go w Cornell University, a New York Times napisał: 'Navy Device Learns By Doing'. Minsky i Papert (1969) wykazali, że perceptron nie może rozwiązać problemu XOR - co wywołało pierwszy 'zimny sezon' w badaniach nad sieciami neuronowymi.",
            "Klasyfikator liniowy (np. regresja logistyczna) zakłada, że klasy można rozdzielić prostą linią. Działa świetnie gdy dane są liniowo separowalne, ale zawodzi na kształtach takich jak półksiężyce czy koncentryczne kółka.",
            "KNN (K najbliższych sąsiadów) klasyfikuje punkt na podstawie klas jego k najbliższych sąsiadów. Może tworzyć bardzo giętkie, nieliniowe granice - jest mocniejszy od regresji logistycznej na skomplikowanych danych.",
            "SVM (Vapnik i Cortes, 1995) - Support Vector Machine szuka granicy decyzyjnej z maksymalnym marginesem. Formalnie dowodzi sie, że granica o największym marginesie daje najlepszą generalizację. SVM z jądrem (kernel trick) pozwala oddzielać klasy nieliniowo bez obliczania cech w wysokowymiarowej przestrzeni wprost.",
            "Drzewo decyzyjne dzieli przestrzeń seriami prostopadłych cięć. Łatwo interpretować jego decyzje, ale przy dużej głębokości skłonne do overfittingu.",
        ],
        "notes": [
            "Overfitting to zjawisko, gdy model zbyt dokładnie dopasowuje sie do danych treningowych i źle generalizuje. Zbyt giętka granica decyzyjna może być symptomem overfittingu.",
            "Twierdzenie No Free Lunch (Wolpert, 1996) - żaden pojedynczy klasyfikator nie przewyższa wszystkich innych we wszystkich możliwych zbiorach danych. Wybór klasyfikatora powinien opierać sie na właściwościach konkretnych danych i zadania.",
            "Walidacja krzyżowa (cross-validation) ocenia model na różnych podzbiorach danych, dając bardziej wiarygodny obraz rzeczywistej dokładności niż jednorazowy podział na trening/test.",
        ],
        "tasks": [
            "Zagraj w Classifier Battle - w której rundzie najtrudniej było narysować granicę? Dlaczego kształt danych wpływa na wybór klasyfikatora?",
            "Porównaj wyniki człowieka z KNN: kiedy granica ręczna okazała sie lepsza, a kiedy KNN był skuteczniejszy?",
            "Wyjaśnij, dlaczego klasyfikator liniowy nie radzi sobie z danymi w kształcie koncentrycznych kółek.",
        ],
    },
    "en": {
        "theory": [
            "A classifier is an algorithm that assigns each data point to one of several predefined classes. A decision boundary is the line (or hyperplane) that divides the feature space into regions for each class.",
            "The Perceptron (Rosenblatt, 1958) - the first learning classifier. Frank Rosenblatt built it at Cornell University, and the New York Times wrote: 'Navy Device Learns By Doing'. Minsky and Papert (1969) showed that a single-layer perceptron cannot solve the XOR problem - triggering the first 'AI winter' in neural network research.",
            "A linear classifier (e.g. logistic regression) assumes classes can be separated by a straight line. It works well when data is linearly separable but fails on shapes like moons or concentric circles.",
            "KNN (K-Nearest Neighbours) classifies a point based on the classes of its k closest neighbours. It can form very flexible, non-linear boundaries and is stronger than logistic regression on complex data.",
            "SVM (Vapnik and Cortes, 1995) - Support Vector Machine finds the decision boundary with maximum margin. It can be formally proven that a maximum-margin boundary gives the best generalisation. SVM with a kernel (kernel trick) allows non-linear class separation without explicitly computing features in a high-dimensional space.",
            "A decision tree splits the feature space with perpendicular cuts. Its decisions are easy to interpret, but deep trees are prone to overfitting.",
        ],
        "notes": [
            "Overfitting occurs when a model fits training data too closely and generalises poorly. An overly flexible decision boundary can be a symptom of overfitting.",
            "The No Free Lunch theorem (Wolpert, 1996) - no single classifier outperforms all others across all possible datasets. Classifier selection should be based on the specific properties of the data and task.",
            "Cross-validation evaluates a model on different data subsets, giving a more reliable accuracy estimate than a single train/test split.",
        ],
        "tasks": [
            "Play Classifier Battle - in which round was it hardest to draw a boundary? Why does the shape of the data influence classifier choice?",
            "Compare the human results against KNN: when was a hand-drawn boundary better, and when was KNN more effective?",
            "Explain why a linear classifier fails on concentric-circle-shaped data.",
        ],
    },
}
