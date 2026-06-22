"""Lesson 15 - Hypothesis Arena (p-value, effect size, power)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Wartość p - co to właściwie znaczy? p-value to prawdopodobieństwo uzyskania co najmniej tak ekstremalnych danych, zakładając że H0 jest prawdziwa. p < 0.05 nie znaczy że efekt jest duży ani ważny - mówi tylko że wynik jest mało prawdopodobny przy braku efektu.",
            "Próg p=0.05 wynalazł R.A. Fisher w 1925 roku - był w dużej mierze arbitralny. Fisher napisał: 'Wygodnie jest przyjąć... szansę 1 do 20 jako granicę' (Statistical Methods for Research Workers, 1925). Nigdy nie zamierzał, by ten próg był używany mechanicznie zamiast naukowego osądu.",
            "Istotność statystyczna nie jest równoznaczna z istotnością praktyczną. Przy dużym N nawet trywialny efekt (Cohen's d = 0.05) daje p < 0.001. Warto zawsze pytać: 'Jak duży jest ten efekt?' - nie tylko 'Czy jest istotny?'",
            "Cohen's d - miara wielkości efektu. Cohen's d = (M1 - M2) / s_pooled. Skala: pomijalny d < 0.10, mały 0.10-0.30, średni 0.30-0.50, duży 0.50-0.80, bardzo duży >= 0.80. Efekt d = 0.20 jest realny, ale może być bez znaczenia praktycznego.",
            "Moc testu i planowanie próby. Moc (1 - beta) to prawdopodobieństwo wykrycia efektu gdy on istnieje. Standardem jest moc 0.80. Zbyt małe N - pomijamy prawdziwe efekty (błąd II rodzaju). Zbyt duże N - wykrywamy trywialne efekty i wyciągamy mylące wnioski.",
            "Kryzys mocy w psychologii - Ioannidis (2005) oszacował, że ponad połowa opublikowanych wyników badań biomedycznych to fałszywe pozytywy. Badanie Cohena (1962) przejrzało 70 artykułów w Journal of Abnormal and Social Psychology i stwierdziło, że mediana mocy wynosiła zaledwie 0.46 - tzn. w połowie prób badacze nie byli w stanie wykryć efektów, które faktycznie szukali.",
        ],
        "notes": [
            "Raportowanie rozmiaru efektu (d, eta^2, r) obok p-value jest standardem - same p-values są niewystarczające.",
            "Przed badaniem warto oszacować potrzebne N na podstawie oczekiwanego d i docelowej mocy (80%). Pakiety G*Power (darmowy) lub pwr (R) automatyzują te obliczenia.",
            "p >= 0.05 nie znaczy 'brak efektu' - może znaczyć 'za mała próba by go wykryć'. Nieistotny wynik bez obliczenia mocy to wynik niekonkluzywny, nie negatywny.",
        ],
        "tasks": [
            "Faza A - Eksploracja: ustaw d = 0.10 i przesuwaj N od 10 do 500. Kiedy pojawia sie p < 0.05? Co to mówi o pułapce małych efektów przy dużym N?",
            "Faza B - Eksperyment: przejdź wszystkie 6 scenariuszy. Dobierz N tak, żeby moc była >= 80% dla każdego scenariusza.",
            "Faza C - Sandbox: ustaw d = 0.20 i alfa = 0.05. Ile N potrzeba do mocy 80%? Jak zmienia sie macierz błędów?",
        ],
    },
    "en": {
        "theory": [
            "What does p-value actually mean? The p-value is the probability of observing data at least as extreme as the obtained results, assuming H0 is true. p < 0.05 does not mean the effect is large or important - it only means the result would be unlikely if there were no effect.",
            "The p=0.05 threshold was introduced by R.A. Fisher in 1925 - it was largely arbitrary. Fisher wrote: 'It is convenient to take... the 1 in 20 chance as a limit' (Statistical Methods for Research Workers, 1925). He never intended this threshold to be used mechanically in place of scientific judgement.",
            "Statistical significance is not the same as practical significance. With large N, even a trivial effect (Cohen's d = 0.05) yields p < 0.001. The relevant question is always: 'How large is this effect?' - not just 'Is it significant?'",
            "Cohen's d - effect size measure. Cohen's d = (M1 - M2) / s_pooled. Scale: negligible d < 0.10, small 0.10-0.30, medium 0.30-0.50, large 0.50-0.80, very large >= 0.80. d = 0.20 is a real effect, but may be practically meaningless.",
            "Statistical power and sample planning. Power (1 - beta) is the probability of detecting an effect when it truly exists. The standard is 80% power. Too small N - real effects are missed (Type II error). Too large N - trivial effects are detected, leading to misleading conclusions.",
            "The power crisis in psychology - Ioannidis (2005) estimated that more than half of published biomedical findings are false positives. Cohen's (1962) review of 70 articles in the Journal of Abnormal and Social Psychology found that median power was only 0.46 - meaning half the time researchers could not detect the very effects they were looking for.",
        ],
        "notes": [
            "Reporting effect size (d, eta^2, r) alongside p-value is standard - p alone is insufficient.",
            "Before a study, estimating the required N based on expected d and target power (80%) is worthwhile. Free tools such as G*Power or the R package pwr automate these calculations.",
            "p >= 0.05 does not mean 'no effect' - it may mean 'sample too small to detect it'. An non-significant result without power analysis is inconclusive, not negative.",
        ],
        "tasks": [
            "Phase A - Explore: set d = 0.10 and move N from 10 to 500. When does p < 0.05 appear? What does this reveal about the trap of small effects with large N?",
            "Phase B - Experiment: run all 6 scenarios. Choose N to achieve >= 80% power for each scenario.",
            "Phase C - Sandbox: set d = 0.20 and alpha = 0.05. How much N is needed for 80% power? How does the error matrix change?",
        ],
    },
}
