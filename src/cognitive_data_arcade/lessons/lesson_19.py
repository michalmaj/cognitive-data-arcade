"""Lesson 19 - Overfitting Monster (overfitting and model validation)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Overfitting (przeuczenie) to zjawisko, gdy model zbyt dokładnie dopasowuje się do danych treningowych i źle działa na nowych danych. Model 'zapamiętuje' szum zamiast uczyć się prawdziwych wzorców.",
            "KNN z małym k (np. k=1) tworzy bardzo giętkę granicę decyzyjną - każdy punkt treningowy staje się 'wyspą'. Dokładność treningowa wynosi 100%, ale testowa spada. To klasyczny przykład overfittingu.",
            "Brzytwa Ockhama w uczeniu maszynowym - William z Ockham (XIV w.) sformułował zasadę: nie mnożyć bytów ponad potrzebę. W ML przekłada się to na: jeśli prostszy model wyjaśnia dane równie dobrze co złożony, prostszy jest preferowany. Regularyzacja formalizuje tę zasadę matematycznie.",
            "Regularyzacja L2 (Ridge) - Tikhonow (1963) wprowadził regularyzację do matematyki jako metodę rozwiązywania problemów niepoprawnie postawionych. W ML Ridge regression dodaje karę za duże współczynniki (suma kwadratów), zmniejszając overfitting bez zerowania cech.",
            "Podział trening/test pozwala ocenić, jak dobrze model generalizuje. Zbiór testowy jest 'niewidzialny' dla modelu podczas trenowania - dopiero po wyborze modelu sprawdza się na nim wyniki.",
            "Różnica między dokładnością treningową a testową (gap) to miara overfittingu. Mały gap oznacza, że model generalizuje. Duży gap (np. 30 pp) oznacza przeuczenie.",
        ],
        "notes": [
            "Kompromis bias-wariancja: zbyt prosty model (duże k w KNN) ma wysoki bias - nie doszacowuje złożoności danych. Zbyt złożony model (małe k) ma wysoką wariancję - jest wrażliwy na szum. Optymalny model leży pośrodku.",
            "Dobór hiperparametrów (jak k) powinien opierać się na zbiorze walidacyjnym, nie testowym. W praktyce używa się walidacji krzyżowej, by nie 'zużyć' zbioru testowego podczas tuningu.",
            "Dropout (Srivastava i in., 2014) - kluczowa technika zapobiegania overfittingowi w głębokich sieciach neuronowych: losowo 'wyłącza' ok. 50% neuronów podczas treningu. Zdobyła powszechne zastosowanie po wygraniu wielu konkursów ImageNet przez sieć AlexNet.",
        ],
        "tasks": [
            "Zagraj w Overfitting Monster - przy którym k pojawia się największy gap między dokładnością treningową a testową?",
            "Porównaj dwie rundy: jedna z małym k i dużym gapem, druga z optymalnym k. Co różni te sytuacje?",
            "Wyjaśnij, dlaczego KNN z k=1 zawsze osiąga 100% dokładności na danych treningowych.",
        ],
    },
    "en": {
        "theory": [
            "Overfitting occurs when a model fits training data too closely and performs poorly on new data. The model 'memorises' noise instead of learning the true pattern.",
            "KNN with small k (e.g. k=1) creates a very flexible decision boundary - each training point becomes its own 'island'. Training accuracy is 100%, but test accuracy drops. This is a classic example of overfitting.",
            "Occam's Razor in machine learning - William of Ockham (14th century) formulated the principle: entities should not be multiplied beyond necessity. In ML this translates to: if a simpler model explains data equally well as a complex one, the simpler one is preferred. Regularisation formalises this principle mathematically.",
            "L2 regularisation (Ridge) - Tikhonov (1963) introduced regularisation into mathematics as a method for solving ill-posed problems. In ML, Ridge regression adds a penalty on large coefficients (sum of squares), reducing overfitting without zeroing out features.",
            "The train/test split lets us estimate how well a model generalises. The test set is 'invisible' to the model during training - only after model selection is performance checked on it.",
            "The gap between training and test accuracy measures overfitting. A small gap means the model generalises. A large gap (e.g. 30 pp) means overfitting.",
        ],
        "notes": [
            "Bias-variance tradeoff: an overly simple model (large k in KNN) has high bias - it underestimates data complexity. An overly complex model (small k) has high variance - it is sensitive to noise. The optimal model lies in between.",
            "Hyperparameter selection (like k) should use a validation set, not the test set. In practice, cross-validation is used so the test set is not 'spent' during tuning.",
            "Dropout (Srivastava et al., 2014) - a key technique for preventing overfitting in deep neural networks: randomly 'switches off' approximately 50% of neurons during training. It gained widespread adoption after AlexNet won the ImageNet competition.",
        ],
        "tasks": [
            "Play Overfitting Monster - at which k does the largest gap appear between training and test accuracy?",
            "Compare two rounds: one with small k and a large gap, another with optimal k. What is different about those situations?",
            "Explain why KNN with k=1 always achieves 100% training accuracy.",
        ],
    },
}
