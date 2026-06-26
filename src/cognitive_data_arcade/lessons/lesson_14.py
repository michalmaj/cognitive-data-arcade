"""Lesson 14 - Correlation & Causation."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Korelacja Pearsona (r) mierzy siłę i kierunek liniowego związku między dwiema zmiennymi. Zakres: od -1 (idealna ujemna) przez 0 (brak związku) do +1 (idealna dodatnia). r^2 (współczynnik determinacji) mówi, jaki procent zmienności Y wyjaśnia X.",
            "Karl Pearson (1896) - wzór na r wprowadził Pearson na podstawie wcześniejszych prac Galtona nad dziedziczeniem cech. Galton odkrył, że wzrost dorosłych synów 'cofa się' w stronę średniej populacji - to zjawisko regresji do średniej. Pearson sformalizował ten pomysł w miarę korelacji.",
            "Korelacja NIE oznacza przyczynowości. Trzy główne powody pozornej korelacji bez związku przyczynowego: 1) Zmienna ukryta (confounding) - trzecia zmienna Z wpływa na obie. 2) Przypadek - przy małym N łatwo o spurious correlation. 3) Trend czasowy - obie zmienne rosną w czasie z różnych powodów.",
            "Spurious Correlations - Tyler Vigen (2015) stworzył stronę internetową, na której automatycznie wyszukuje korelacje między przypadkowymi zmiennymi z danych rządowych USA. Spożycie sera na głowę koreluje ze śmiercią przez zaplątanie w pościel (r=0.947). Strona stała się podręcznikowym przykładem korelacji spuriousowych.",
            "Jak ustalamy przyczynowość? Złotym standardem jest eksperyment z randomizacją (RCT). Bez randomizacji używa się badań naturalnych, regresji z kontrolą zmiennych ukrytych lub kryteriów Bradforda-Hilla (1965) - 9 kryteriów opracowanych po epidemiologicznych badaniach nad związkiem palenia z rakiem płuca.",
            "Klasyczna korelacja pozorna: spożycie lodów koreluje z liczbą utonięć (r=0.88), bo wspólna przyczyna to pora roku. Korelacja przyczynowa: palenie papierosów i rak płuca, potwierdzone w setkach badań kohortowych i eksperymentów na zwierzętach.",
        ],
        "notes": [
            "Przy małym N nawet duże r może być przypadkowe. Przed wyciąganiem wniosków warto sprawdzić: ile obserwacji? Jaki jest 95% przedział ufności dla r? Przy N < 30 r bez testu istotności jest mało wiarygodne.",
            "Siła korelacji nie informuje o mechanizmie przyczynowym. r=0.93 między sprzedażą iPhone a wskaźnikiem samobójstw w USA to trend czasowy, nie przyczynowość. Warto pytać: co może być wspólną przyczyną? Czy jest trend czasowy? Co pokazałby eksperyment?",
            "Korelacja Pearsona zakłada liniowość związku i normalność obu zmiennych. Dla związków nieliniowych (np. odwrócone U) r wynosi ok. 0 mimo wyraźnego wzorca. Zawsze warto patrzeć na wykres punktowy - samo r nie wystarcza.",
        ],
        "tasks": [
            "W Fazie A: ustaw r=0.9, N=20 i r=0.9, N=200. Jak różni się wygląd chmury punktów? Teraz utrzymaj r=0.9, N=200 i zwiększ szum do 0.8. Jak zmieniło się wizualne wrażenie? Czy r się zmieniło?",
            "W Fazie B: przejdź przez wszystkie 8 scenariuszy. Dla każdego spurious - znajdź zmienną ukrytą zanim klikniesz 'Poddaj się'. Dla każdego causal - zastanów się jak można to sprawdzić eksperymentalnie.",
            "W Fazie C: znajdź 3 pary zmiennych z r > 0.7. Dla każdej zapisz: czy to przyczynowość, zmienna ukryta czy trend czasowy? Potem znajdź parę z r najbliższym 0 - co łączy te zmienne?",
        ],
    },
    "en": {
        "theory": [
            "Pearson's r measures the strength and direction of the linear relationship between two variables. Range: from -1 (perfect negative) through 0 (no relationship) to +1 (perfect positive). r^2 (coefficient of determination) tells us what percentage of Y's variance is explained by X.",
            "Karl Pearson (1896) - Pearson formalised the correlation formula based on Galton's earlier work on inheritance. Galton had discovered that adult sons' heights 'regress' towards the population mean - the phenomenon of regression to the mean. Pearson formalised this idea into a measure of correlation.",
            "Correlation does NOT imply causation. Three main reasons for apparent correlation without a causal link: 1) Confounding variable - a third variable Z affects both. 2) Coincidence - with small N, spurious correlations are easy to find. 3) Time trend - both variables increase over time for different reasons.",
            "Spurious Correlations - Tyler Vigen (2015) built a website that automatically searches for correlations among random variables in US government data. Per capita cheese consumption correlates with deaths by bedsheet tangling (r=0.947). The site has become a textbook example of spurious correlation.",
            "How do we establish causation? The gold standard is a randomised controlled trial (RCT). Without randomisation, natural experiments, regression controlling for confounders, or Bradford-Hill criteria (1965) are used - 9 criteria developed after epidemiological studies of smoking and lung cancer.",
            "Classic spurious correlation: ice cream consumption correlates with drownings (r=0.88), because the common cause is the season. Causal example: smoking and lung cancer - confirmed in hundreds of cohort studies and animal experiments.",
        ],
        "notes": [
            "With small N even a large r may be coincidental. Before drawing conclusions, it is worth checking: how many observations? What is the 95% confidence interval for r? At N < 30, r without a significance test is unreliable.",
            "Correlation strength does not tell us about the causal mechanism. r=0.93 between iPhone sales and the US suicide rate is a time trend, not causation. Useful questions: what could be a common cause? Is there a time trend? What would an experiment show?",
            "Pearson's r assumes linearity and normality. For non-linear relationships (e.g., inverted U), r is approximately 0 despite a clear pattern. Looking at the scatter plot is always worthwhile - r alone is not enough.",
        ],
        "tasks": [
            "In Phase A: set r=0.9, N=20 then r=0.9, N=200. How does the point cloud look different? Keep r=0.9, N=200 and increase noise to 0.8. How did the visual impression change? Did r change?",
            "In Phase B: go through all 8 scenarios. For each spurious one - find the hidden variable before clicking 'Give up'. For each causal one - think about how it could be tested experimentally.",
            "In Phase C: find 3 variable pairs with r > 0.7. For each, note: is this causation, a hidden variable, or a time trend? Then find the pair with r closest to 0 - what connects those variables?",
        ],
    },
}
