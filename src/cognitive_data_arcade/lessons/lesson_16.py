"""Lesson 16 - Prediction Slider (linear regression, R², residuals, outlier influence)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Regresja liniowa dopasowuje prostą linię y = a*x + b do danych, minimalizując sumę kwadratów reszt (OLS - Ordinary Least Squares). Slope (a) mówi, jak bardzo zmienia się y gdy x rośnie o 1. Intercept (b) to wartość y gdy x = 0.",
            "Francis Galton (1886) - regresję liniową wynalazł Galton przy badaniu dziedziczenia wzrostu. Odkrył, że wzrost synów 'cofa się' w stronę średniej populacji - stąd nazwa 'regresja'. Karl Pearson sformalizował matematycznie metodę Galton w latach 90. XIX w.",
            "R² - miara dopasowania modelu. R² (R-squared) mierzy jaki procent zmienności y wyjaśnia model. R² = 1.0 to idealne dopasowanie, R² = 0.0 to brak związku. R² = 0.65 oznacza, że model wyjaśnia 65% zmienności y.",
            "Twierdzenie Gaussa-Markowa - pod standardowymi założeniami (liniowość, homoskedastyczność, brak autokorelacji, brak endogeniczności) szacownik OLS jest BLUE: Best Linear Unbiased Estimator - najlepszy liniowy nieobciążony estymator.",
            "Reszty (residuals) - błędy predykcji. Reszta = y_rzeczywiste - y_przewidywane. Dobry model ma reszty losowe, bez wzorca. Wzorzec w resztach (np. krzywizna lub lejkowanie) sugeruje, że model liniowy jest nieodpowiedni lub wariancja nie jest stała.",
            "Dystans Cooka (Cook, 1977) - formalna miara wpływu obserwacji na model. Łączy dźwignię (odległość od średniej x) z wielkością reszty. Wartości Cook's D > 1 sygnalizują obserwacje wymagające sprawdzenia. R.D. Cook wprowadził tę miarę, by móc identyfikować obserwacje diametralnie zmieniające wyniki.",
        ],
        "notes": [
            "R² nie mówi, czy model jest dobry - mówi tylko ile zmienności wyjaśnia. Wykres reszt może ujawnić problem nawet przy wysokim R².",
            "Outlier poza zakresem x (ekstrapolacja) ma ogromny wpływ - dźwignia rośnie z odległością od średniej x.",
            "Regresja OLS minimalizuje sumy kwadratów reszt, więc jest wrażliwa na outliery. Regresja odporna (robust regression, np. metoda Hubera lub Bisquare) jest alternatywą przy podejrzanych punktach.",
        ],
        "tasks": [
            "Faza A - Eksploracja: ustaw sigma = 2.0 i N = 20. Jak wygląda wykres reszt? Teraz ustaw sigma = 0.1. Jak zmienił się R²?",
            "Faza B - Gra: przejdź wszystkie 5 scenariuszy. Staraj się uzyskać wynik powyżej 350 / 500.",
            "Faza C - Sandbox: przeciągnij outlier daleko w prawo (poza dane). Jak zmienił się slope? Dlaczego punkty na krawędzi x mają większy wpływ?",
        ],
    },
    "en": {
        "theory": [
            "Linear regression fits the line y = a*x + b to data by minimizing the sum of squared residuals (OLS - Ordinary Least Squares). Slope (a) tells how much y changes when x increases by 1. Intercept (b) is the value of y when x = 0.",
            "Francis Galton (1886) - linear regression was invented by Galton when studying height inheritance. He discovered that sons' heights 'regress' toward the population mean - hence the name 'regression'. Karl Pearson formalised Galton's method mathematically in the 1890s.",
            "R² - a measure of model fit. R² (R-squared) measures what percentage of y variability is explained by the model. R² = 1.0 is a perfect fit, R² = 0.0 means no relationship. R² = 0.65 means the model explains 65% of y's variability.",
            "The Gauss-Markov theorem - under standard assumptions (linearity, homoscedasticity, no autocorrelation, no endogeneity), the OLS estimator is BLUE: Best Linear Unbiased Estimator.",
            "Residuals - prediction errors. Residual = y_actual - y_predicted. A good model has random residuals with no pattern. A pattern in residuals (e.g., curvature or funnelling) suggests the linear model is inappropriate or variance is not constant.",
            "Cook's Distance (Cook, 1977) - a formal measure of an observation's influence on the model. It combines leverage (distance from mean x) with residual magnitude. Cook's D > 1 flags observations that warrant investigation. R.D. Cook introduced this measure to identify observations that disproportionately change model results.",
        ],
        "notes": [
            "R² does not tell you if the model is good - it only tells you how much variance it explains. The residual plot can reveal problems even at high R².",
            "An outlier outside the x range (extrapolation) has enormous influence - leverage grows with distance from mean x.",
            "OLS regression minimizes squared residuals, so it is sensitive to outliers. Robust regression (e.g., Huber or Bisquare methods) is an alternative when suspicious points are present.",
        ],
        "tasks": [
            "Phase A - Explore: set sigma = 2.0 and N = 20. What does the residual plot look like? Now set sigma = 0.1. How did R² change?",
            "Phase B - Game: complete all 5 scenarios. Try to score above 350 / 500.",
            "Phase C - Sandbox: drag the outlier far to the right (beyond the data). How did slope change? Why do points at the edge of x have more influence?",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "Prediction Slider — Refleksja",
        "cards": [
            {
                "label": "Regresja",
                "color": "indigo",
                "text": "OLS minimalizuje sumę kwadratów reszt. Slope = zmiana y na jednostkę x. R² = procent wyjaśnionej zmienności — nie mówi, czy model jest dobry.",
            },
            {
                "label": "Reszty",
                "color": "orange",
                "text": "Dobry model ma reszty losowe, bez wzorca. Krzywizna lub lejkowanie na wykresie reszt to sygnał, że model liniowy jest nieodpowiedni.",
            },
            {
                "label": "Wpływ",
                "color": "green",
                "text": "Outlier daleko od średniej x (duże leverage) nieproporcjonalnie zmienia slope. Cook's D > 1 to sygnał obserwacji wymagającej sprawdzenia.",
            },
        ],
        "question": "Model regresji osiąga R²=0.85, ale wykres reszt pokazuje parabolę. Czy model jest dobry? Co zrobisz jako następny krok?",
    },
    "en": {
        "title": "Prediction Slider — Reflection",
        "cards": [
            {
                "label": "Regression",
                "color": "indigo",
                "text": "OLS minimises the sum of squared residuals. Slope = change in y per unit of x. R² = percentage of variance explained — it does not tell you whether the model is good.",
            },
            {
                "label": "Residuals",
                "color": "orange",
                "text": "A good model has random residuals with no pattern. Curvature or funnelling in the residual plot signals that the linear model is inappropriate.",
            },
            {
                "label": "Influence",
                "color": "green",
                "text": "An outlier far from the mean of x (high leverage) disproportionately shifts the slope. Cook's D > 1 flags an observation that warrants investigation.",
            },
        ],
        "question": "A regression model achieves R²=0.85, but the residual plot shows a parabola. Is the model good? What is your next step?",
    },
}
