"""Lesson 16 -- Prediction Slider (linear regression, R², residuals, outlier influence)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Regresja liniowa — co to jest? Regresja liniowa dopasowuje prostą linię y = a*x + b do danych, minimalizując sumę kwadratów reszt (OLS). Slope (a) mówi jak bardzo zmienia się y gdy x rośnie o 1. Intercept (b) to wartość y gdy x = 0.",
            "R² — miara dopasowania modelu. R² (R-squared) mierzy jaki procent zmienności y jest wyjaśniony przez model. R² = 1.0 to idealne dopasowanie, R² = 0.0 to brak związku. R² = 0.65 znaczy że model wyjaśnia 65% zmienności y.",
            "Reszty (residuals) — błędy predykcji. Reszta = y_rzeczywiste - y_przewidywane. Dobry model ma reszty losowe, bez wzorca. Wzorzec w resztach (np. krzywizna) sugeruje że model liniowy jest nieodpowiedni.",
            "Wpływ outlierów i dźwignia (leverage). Punkty daleko od średniej x mają duży wpływ na nachylenie linii — to tzw. dźwignia (leverage). Jeden outlier z dużą dźwignią może drastycznie zmienić slope i R². Zawsze sprawdzaj wykres rozproszenia przed interpretacją modelu.",
        ],
        "notes": [
            "R² nie mówi czy model jest dobry — mówi tylko ile zmienności wyjaśnia. Sprawdzaj zawsze wykres reszt.",
            "Outlier poza zakresem x (ekstrapolacja) ma ogromny wpływ — dźwignia rośnie z odległością od średniej x.",
            "Regresja OLS minimalizuje sumy kwadratów reszt, więc jest wrażliwa na outliery. Rozważ regresję odporną (robust regression) jeśli masz podejrzane punkty.",
        ],
        "tasks": [
            "Faza A — Eksploracja: ustaw sigma = 2.0 i N = 20. Jak wygląda wykres reszt? Teraz ustaw sigma = 0.1. Jak zmienił się R²?",
            "Faza B — Gra: przejdź wszystkie 5 scenariuszy. Staraj się uzyskać wynik powyżej 350 / 500.",
            "Faza C — Sandbox: przeciągnij outlier daleko w prawo (poza dane). Jak zmienił się slope? Dlaczego punkty na krawędzi x mają większy wpływ?",
        ],
    },
    "en": {
        "theory": [
            "Linear regression — what is it? Linear regression fits the line y = a*x + b to data by minimizing the sum of squared residuals (OLS). Slope (a) tells how much y changes when x increases by 1. Intercept (b) is the value of y when x = 0.",
            "R² — a measure of model fit. R² (R-squared) measures what percentage of y variability is explained by the model. R² = 1.0 is a perfect fit, R² = 0.0 means no relationship. R² = 0.65 means the model explains 65% of y's variability.",
            "Residuals — prediction errors. Residual = y_actual - y_predicted. A good model has random residuals with no pattern. A pattern in residuals (e.g., curvature) suggests the linear model is inappropriate.",
            "Outlier influence and leverage. Points far from the mean x have a large effect on the slope — this is called leverage. A single high-leverage outlier can drastically change slope and R². Always check the scatter plot before interpreting a model.",
        ],
        "notes": [
            "R² does not tell you if the model is good — it only tells you how much variance it explains. Always check the residual plot.",
            "An outlier outside the x range (extrapolation) has enormous influence — leverage grows with distance from mean x.",
            "OLS regression minimizes squared residuals, so it is sensitive to outliers. Consider robust regression if you have suspicious points.",
        ],
        "tasks": [
            "Phase A — Explore: set sigma = 2.0 and N = 20. What does the residual plot look like? Now set sigma = 0.1. How did R² change?",
            "Phase B — Game: complete all 5 scenarios. Try to score above 350 / 500.",
            "Phase C — Sandbox: drag the outlier far to the right (beyond the data). How did slope change? Why do points at the edge of x have more influence?",
        ],
    },
}
