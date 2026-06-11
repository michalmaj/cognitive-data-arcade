"""Lesson 15 -- Hypothesis Arena (p-value, effect size, power)."""
from __future__ import annotations

CONTENT: dict[str, dict] = {
    "pl": {
        "theory": [
            (
                "Wartość p — co to właściwie znaczy?",
                "p-value to prawdopodobieństwo uzyskania co najmniej tak ekstremalnych danych, "
                "zakładając że H0 jest prawdziwa. p < 0.05 nie znaczy że efekt jest duży ani ważny — "
                "mówi tylko że wynik jest mało prawdopodobny przy braku efektu.",
            ),
            (
                "Istotność statystyczna != istotność praktyczna",
                "Przy dużym N nawet trywialny efekt (Cohen's d = 0.05) daje p < 0.001. "
                "Zawsze pytaj: 'Jak duży jest ten efekt?' — nie tylko 'Czy jest istotny?'",
            ),
            (
                "Cohen's d — miara wielkości efektu",
                "Cohen's d = (M1 - M2) / s_pooled. Skala: pomijalny d < 0.10, mały 0.10-0.30, "
                "średni 0.30-0.50, duży 0.50-0.80, bardzo duży >= 0.80. "
                "Efekt d = 0.20 jest realny, ale w praktyce może być bez znaczenia.",
            ),
            (
                "Moc testu i planowanie próby",
                "Moc (1 - beta) to prawdopodobieństwo wykrycia efektu gdy on istnieje. "
                "Standardem jest moc 0.80. Zbyt małe N -> przeoczasz prawdziwe efekty (błąd II rodzaju). "
                "Zbyt duże N -> wykrywasz trywialne efekty i wyciągasz mylące wnioski.",
            ),
        ],
        "notes": [
            "Zawsze raportuj rozmiar efektu (d, eta^2, r) obok p-value — same p-values są niewystarczające.",
            "Przed badaniem oszacuj potrzebne N na podstawie oczekiwanego d i docelowej mocy (80%).",
            "p >= 0.05 nie znaczy 'brak efektu' — może znaczyć 'za mała próba by go wykryć'.",
        ],
        "tasks": [
            "Faza A — Eksploracja: ustaw d = 0.10 i przesuwaj N od 10 do 500. Kiedy pojawia się p < 0.05? Co to mówi o pułapce?",
            "Faza B — Eksperyment: przejdź wszystkie 6 scenariuszy. Dobierz N tak, żeby moc była >= 80% dla każdego.",
            "Faza C — Sandbox: ustaw d = 0.20 i alfa = 0.05. Ile N potrzebujesz do mocy 80%? Jak zmienia się macierz błędów?",
        ],
    },
    "en": {
        "theory": [
            (
                "What does p-value actually mean?",
                "The p-value is the probability of observing data at least as extreme as yours, "
                "assuming H0 is true. p < 0.05 does not mean the effect is large or important — "
                "it only means the result would be unlikely if there were no effect.",
            ),
            (
                "Statistical significance != practical significance",
                "With large N, even a trivial effect (Cohen's d = 0.05) yields p < 0.001. "
                "Always ask: 'How large is this effect?' — not just 'Is it significant?'",
            ),
            (
                "Cohen's d — effect size measure",
                "Cohen's d = (M1 - M2) / s_pooled. Scale: negligible d < 0.10, small 0.10-0.30, "
                "medium 0.30-0.50, large 0.50-0.80, very large >= 0.80. "
                "d = 0.20 is a real effect, but may be practically meaningless.",
            ),
            (
                "Statistical power and sample planning",
                "Power (1 - beta) is the probability of detecting an effect when it truly exists. "
                "The standard is 80% power. Too small N -> you miss real effects (Type II error). "
                "Too large N -> you detect trivial effects and draw misleading conclusions.",
            ),
        ],
        "notes": [
            "Always report effect size (d, eta^2, r) alongside p-value — p alone is insufficient.",
            "Before a study, calculate the N needed based on expected d and target power (80%).",
            "p >= 0.05 does not mean 'no effect' — it may mean 'sample too small to detect it'.",
        ],
        "tasks": [
            "Phase A — Explore: set d = 0.10 and move N from 10 to 500. When does p < 0.05 appear? What does this reveal about the trap?",
            "Phase B — Experiment: run all 6 scenarios. Choose N to achieve >= 80% power for each.",
            "Phase C — Sandbox: set d = 0.20 and alpha = 0.05. How much N do you need for 80% power? How does the error matrix change?",
        ],
    },
}
