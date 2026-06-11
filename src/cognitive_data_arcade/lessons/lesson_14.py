"""Lesson 14 -- Correlation & Causation."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Korelacja Pearsona (r) mierzy siłę i kierunek liniowego związku między dwiema zmiennymi. Zakres: od -1 (idealna ujemna) przez 0 (brak związku) do +1 (idealna dodatnia). r^2 (współczynnik determinacji) mówi jaki procent zmienności Y wyjaśniają X.",
            "Korelacja NIE oznacza przyczynowości. Istnieją trzy główne powody pozornej korelacji bez związku przyczynowego: 1) Zmienna ukryta (confounding) -- trzecia zmienna Z wpływa na obie. 2) Przypadek -- przy małym N łatwo o spurious correlation. 3) Trend czasowy -- obie zmienne rosną w czasie z różnych powodów.",
            "Jak ustalamy przyczynowość? Złotym standardem jest eksperyment z randomizacją (RCT): losowo przydzielamy uczestników do grup i manipulujemy zmienną X. Bez randomizacji możemy używać badań naturalnych, analizy regresji z kontrolą zmiennych ukrytych lub kryteriów Bradforda-Hilla (siła, specyficzność, koherencja, temporalność).",
            "Przykład klasyczny: spożycie lodów koreluje z liczbą utonięć (r=0.88). Pułapka -- wspólna przyczyna to pora roku. Latem ludzie jedzą więcej lodów i więcej pływają. Przykład przyczynowy: palenie papierosów i rak płuc -- potwierdzony w setkach badań kohortowych i eksperymentów na zwierzętach.",
        ],
        "notes": [
            "Przy małym N nawet duże r może być przypadkowe. Przed wyciąganiem wniosków zawsze sprawdzaj: ile mamy obserwacji? Jaki jest 95% przedział ufności dla r? Zasada: N < 30 to za mało by ufać r bez testu istotności.",
            "Siła korelacji nie informuje o mechanizmie przyczynowym. r=0.93 między sprzedażą iPhone a wskaźnikiem samobójstw w USA to trend czasowy, nie przyczynowość. Zawsze pytaj: co może być wspólną przyczyną? Czy jest tu trend czasowy? Jaki byłby wynik eksperymentu?",
            "Korelacja Pearsona zakłada liniowość związku i normalność obu zmiennych. Dla związków nieliniowych (np. odwrócone U) r ~ 0 mimo wyraźnego wzorca. Zawsze patrz na wykres punktowy -- samo r nie wystarcza!",
        ],
        "tasks": [
            "W Fazie A: ustaw r=0.9, N=20 i r=0.9, N=200. Jak różni się wygląd chmury punktów? Teraz utrzymaj r=0.9, N=200 i zwiększ szum do 0.8. Jak zmieniło się wizualne wrażenie? Czy r się zmieniło?",
            "W Fazie B: przejdź przez wszystkie 8 scenariuszy. Dla każdego spurious -- znajdź zmienną ukrytą zanim klikniesz 'Poddaj się'. Dla każdego causal -- zastanów się jak można to sprawdzić eksperymentalnie.",
            "W Fazie C: znajdź 3 pary zmiennych z r > 0.7. Dla każdej zapisz: czy to przyczynowość, zmienna ukryta czy trend czasowy? Potem znajdź parę z r najbliższym 0 -- co łączy te zmienne?",
        ],
    },
    "en": {
        "theory": [
            "Pearson's r measures the strength and direction of the linear relationship between two variables. Range: from -1 (perfect negative) through 0 (no relationship) to +1 (perfect positive). r^2 (coefficient of determination) tells us what percentage of Y's variance is explained by X.",
            "Correlation does NOT imply causation. There are three main reasons for apparent correlation without a causal link: 1) Confounding variable -- a third variable Z affects both. 2) Coincidence -- with small N, spurious correlations are easy to find. 3) Time trend -- both variables increase over time for different reasons.",
            "How do we establish causation? The gold standard is a randomised controlled trial (RCT): randomly assign participants to groups and manipulate X. Without randomisation we can use natural experiments, regression analysis controlling for confounders, or Bradford-Hill criteria (strength, specificity, coherence, temporality).",
            "Classic example: ice cream consumption correlates with drownings (r=0.88). The trap -- the common cause is the season. In summer people eat more ice cream AND swim more. Causal example: smoking and lung cancer -- confirmed in hundreds of cohort studies and animal experiments.",
        ],
        "notes": [
            "With small N even a large r may be coincidental. Before drawing conclusions always check: how many observations do we have? What is the 95% confidence interval for r? Rule of thumb: N < 30 is too few to trust r without a significance test.",
            "Correlation strength does not tell us about the causal mechanism. r=0.93 between iPhone sales and the US suicide rate is a time trend, not causation. Always ask: what could be a common cause? Is there a time trend here? What would an experiment show?",
            "Pearson's r assumes linearity and normality. For non-linear relationships (e.g., inverted U), r ~ 0 despite a clear pattern. Always look at the scatter plot -- r alone is not enough!",
        ],
        "tasks": [
            "In Phase A: set r=0.9, N=20 then r=0.9, N=200. How does the point cloud look different? Keep r=0.9, N=200 and increase noise to 0.8. How did the visual impression change? Did r change?",
            "In Phase B: go through all 8 scenarios. For each spurious one -- find the hidden variable before clicking 'Give up'. For each causal one -- think about how you could test it experimentally.",
            "In Phase C: find 3 variable pairs with r > 0.7. For each, note: is this causation, a hidden variable, or a time trend? Then find the pair with r closest to 0 -- what connects those variables?",
        ],
    },
}
