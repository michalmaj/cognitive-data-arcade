# src/cognitive_data_arcade/lessons/lesson_19.py
"""Lesson 19 - Overfitting Monster (overfitting and model validation)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Overfitting (przeuczenie) to zjawisko, gdy model zbyt dokładnie dopasowuje się do danych "
            "treningowych i źle działa na nowych danych. Model 'zapamiętuje' szum zamiast uczyć się "
            "prawdziwych wzorców.",
            "KNN z małym k (np. k=1) tworzy bardzo giętkę granicę decyzyjną - każdy punkt treningowy "
            "staje się 'wyspa'. Dokładność treningowa wynosi 100%, ale testowa spada. "
            "To klasyczny przykład overfittingu.",
            "Podział trening/test pozwala ocenić, jak dobrze model generalizuje. "
            "Zbiór testowy jest 'niewidzialny' dla modelu podczas trenowania - "
            "dopiero po wyborze modelu sprawdzamy na nim wyniki.",
            "Różnica między dokładnością treningową a testową (gap) to miara overfittingu. "
            "Mały gap oznacza, że model generalizuje. Duży gap (np. 30 pp) oznacza przeuczenie.",
        ],
        "notes": [
            "Kompromis bias-variance: zbyt prosty model (duże k w KNN) ma wysoki bias - "
            "nie doszacowuje złożoności danych. Zbyt złożony model (małe k) ma wysoką wariancję - "
            "jest wrażliwy na szum. Optymalny model leży pośrodku.",
            "Dobór hiperparametrów (jak k) powinien być oparty na zbiorze walidacyjnym, "
            "nie testowym. W praktyce używa się walidacji krzyżowej, "
            "by nie 'zużyć' zbioru testowego podczas tuningu.",
        ],
        "tasks": [
            "Zagraj w Overfitting Monster - w której rundzie najtrudniej było znaleźć sweet spot k?",
            "Porównaj dwie rundy: jedna z małym k i dużym gapem, druga z optymalnym k. "
            "Co różni te sytuacje?",
            "Wyjaśnij własnymi słowami, dlaczego KNN z k=1 zawsze osiąga 100% na danych treningowych.",
        ],
    },
    "en": {
        "theory": [
            "Overfitting occurs when a model fits training data too closely and performs poorly on new data. "
            "The model 'memorises' noise instead of learning the true pattern.",
            "KNN with small k (e.g. k=1) creates a very flexible decision boundary - "
            "each training point becomes its own 'island'. Training accuracy is 100%, but test accuracy drops. "
            "This is a classic example of overfitting.",
            "The train/test split lets us estimate how well a model generalises. "
            "The test set is 'invisible' to the model during training - "
            "only after model selection do we check performance on it.",
            "The gap between training and test accuracy measures overfitting. "
            "A small gap means the model generalises. A large gap (e.g. 30 pp) means overfitting.",
        ],
        "notes": [
            "Bias-variance tradeoff: an overly simple model (large k in KNN) has high bias - "
            "it underestimates data complexity. An overly complex model (small k) has high variance - "
            "it is sensitive to noise. The optimal model lies in between.",
            "Hyperparameter selection (like k) should use a validation set, not the test set. "
            "In practice, cross-validation is used so the test set is not 'spent' during tuning.",
        ],
        "tasks": [
            "Play Overfitting Monster - in which round was it hardest to find the sweet spot for k?",
            "Compare two rounds: one with small k and a large gap, another with optimal k. "
            "What is different about those situations?",
            "Explain in your own words why KNN with k=1 always achieves 100% training accuracy.",
        ],
    },
}
