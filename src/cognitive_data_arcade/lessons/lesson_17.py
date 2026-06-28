"""Lesson 17 - Feature Hunter (feature selection intuition)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Nie każda cecha danych pomaga modelowi - niektóre są szumem. Cecha-szum nie ma żadnego związku ze zmienną docelową. Dodanie jej do modelu może pogorszyć jego działanie poprzez zwiększenie szumu i ryzyko przeuczenia.",
            "Korelacja (r) mierzy siłę i kierunek związku liniowego między cechą a celem. r bliskie 1 lub -1 = silny związek. r bliskie 0 = brak związku = prawdopodobnie szum. Korelacja mierzy jednak tylko zależności liniowe.",
            "Klątwa wymiarowości (Bellman, 1961) - wraz z liczbą cech rośnie wykładniczo przestrzeń, którą model musi pokryć. Przy 10 cechach ciągłych potrzeba 10^10 próbek, by gęstość danych była taka sama jak przy 1 cesze i 10 próbkach. To dlatego selekcja cech jest ważna.",
            "Trzy podejścia do selekcji cech: (1) Filter methods - oceniają cechy niezależnie od modelu (korelacja, test chi², ANOVA). (2) Wrapper methods - testują podzbiory cech przez trenowanie modelu. (3) Embedded methods - algorytm uczy się i wybiera cechy jednocześnie (LASSO, drzewa decyzyjne).",
            "LASSO (Tibshirani, 1996) - regresja z regularyzacją L1. Minimalizuje sumę |współczynników| jako karę. Karę, która zeruje współczynniki nieistotnych cech. LASSO automatycznie usuwa cechy-szumy z modelu i daje rozwiązanie rzadkie (sparse). Stosowane m.in. w genomice do selekcji genów.",
            "Informacja wzajemna (mutual information) - miara nielinearna siły związku. Mierzy ile informacji o zmiennej docelowej zawiera cecha. W odróżnieniu od r, wykrywa związki nieliniowe i nieciągłości. Dostępna w sklearn jako mutual_info_regression/mutual_info_classif.",
        ],
        "notes": [
            "Silna korelacja |r| > 0.5 to dobry sygnał, ale sama korelacja nie wystarczy - warto sprawdzać też sens merytoryczny i możliwe zmienne ukryte.",
            "Korelacja mierzy tylko związki liniowe. Cecha może być przydatna nieliniowo nawet gdy r bliskie 0 - warto użyć wykresu rozrzutu lub informacji wzajemnej.",
            "Multikoliniowość - gdy dwie cechy są silnie skorelowane ze sobą, model nie może rozróżnić ich indywidualnych wkładów. Dodanie obu zamiast jednej nie poprawia predykcji, lecz zwiększa niestabilność współczynników.",
        ],
        "tasks": [
            "Zagraj w Feature Hunter na poziomie Easy - ile cech poprawnie zidentyfikowano jako sygnał vs. szum?",
            "Spróbuj poziomu Hard - które cechy były zaskakujące? Czy były cechy z niską korelacją, ale wizualnie wyraźnym nieliniowym wzorcem?",
            "Wypisz 3 cechy z rzeczywistego zbioru danych (np. dane RT), które mogłyby być szumem, i wyjaśnij, dlaczego ich korelacja z celem może być bliska zeru.",
        ],
    },
    "en": {
        "theory": [
            "Not every data feature helps a model - some are noise. A noise feature has no relationship with the target variable. Adding it can hurt model performance by increasing noise and the risk of overfitting.",
            "Correlation (r) measures the strength and direction of a linear relationship between a feature and the target. r near 1 or -1 = strong relationship. r near 0 = no relationship = likely noise. Correlation only measures linear dependencies.",
            "The curse of dimensionality (Bellman, 1961) - the space a model must cover grows exponentially with the number of features. With 10 continuous features, 10^10 samples are needed to maintain the same data density as 1 feature with 10 samples. This is why feature selection matters.",
            "Three approaches to feature selection: (1) Filter methods - evaluate features independently of the model (correlation, chi-square, ANOVA). (2) Wrapper methods - test feature subsets by training the model. (3) Embedded methods - the algorithm learns and selects features simultaneously (LASSO, decision trees).",
            "LASSO (Tibshirani, 1996) - regression with L1 regularisation. It penalises the sum of absolute coefficient values, zeroing out coefficients of unimportant features. LASSO automatically removes noise features and produces a sparse solution. Widely used in genomics for gene selection.",
            "Mutual information - a non-linear measure of association strength. It quantifies how much information the feature contains about the target variable. Unlike r, it detects non-linear relationships and discontinuities. Available in sklearn as mutual_info_regression/mutual_info_classif.",
        ],
        "notes": [
            "Strong correlation |r| > 0.5 is a good signal, but correlation alone is not enough - domain logic and possible hidden variables are also worth checking.",
            "Correlation only measures linear relationships. A feature can be useful non-linearly even when r is near 0 - scatter plots or mutual information are better diagnostics.",
            "Multicollinearity - when two features are strongly correlated with each other, the model cannot distinguish their individual contributions. Adding both rather than one does not improve prediction but makes coefficients unstable.",
        ],
        "tasks": [
            "Play Feature Hunter on Easy - how many features were correctly identified as signal vs. noise?",
            "Try Hard mode - which features were surprising? Were any features with low correlation but a visually clear non-linear pattern?",
            "List 3 features from a real dataset (e.g. RT data) that might be noise, and explain why their correlation with the target might be close to zero.",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "Feature Hunter — Refleksja",
        "cards": [
            {
                "label": "Sygnał vs szum",
                "color": "indigo",
                "text": "Cecha-szum nie ma związku ze zmienną docelową. Dodanie jej zwiększa wymiarowość i ryzyko przeuczenia, nie poprawiając predykcji.",
            },
            {
                "label": "Selekcja cech",
                "color": "orange",
                "text": "Filter (korelacja, ANOVA), Wrapper (testowanie podzbiorów), Embedded (LASSO zeruje współczynniki szumów automatycznie podczas trenowania).",
            },
            {
                "label": "Wymiarowość",
                "color": "green",
                "text": "Klątwa Bellmana (1961): przestrzeń rośnie wykładniczo z liczbą cech. Więcej zmiennych w modelu to nie zawsze lepszy model.",
            },
        ],
        "question": "Masz 100 cech i N=200. LASSO zostawia 8. Jak sprawdzisz, czy wybrał właściwe — i czy nie pominął cechy ważnej nieliniowo?",
    },
    "en": {
        "title": "Feature Hunter — Reflection",
        "cards": [
            {
                "label": "Signal vs noise",
                "color": "indigo",
                "text": "A noise feature has no relationship with the target variable. Adding it increases dimensionality and overfitting risk without improving prediction.",
            },
            {
                "label": "Feature selection",
                "color": "orange",
                "text": "Filter (correlation, ANOVA), Wrapper (subset testing), Embedded (LASSO automatically zeros out noise feature coefficients during training).",
            },
            {
                "label": "Dimensionality",
                "color": "green",
                "text": "Bellman's curse (1961): the feature space grows exponentially with the number of variables. More features in a model does not mean a better model.",
            },
        ],
        "question": "You have 100 features and N=200. LASSO keeps 8. How do you check whether it selected the right ones — and whether it missed a feature that matters non-linearly?",
    },
}
