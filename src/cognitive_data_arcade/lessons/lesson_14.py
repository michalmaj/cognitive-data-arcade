"""Lesson 14 -- Correlation & Causation."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Korelacja Pearsona (r) mierzy sile i kierunek liniowego zwiazku miedzy dwiema zmiennymi. Zakres: od -1 (idealna ujemna) przez 0 (brak zwiazku) do +1 (idealna dodatnia). r^2 (wspolczynnik determinacji) mowi jaki procent zmiennosci Y wyjasnaja X.",
            "Korelacja NIE oznacza przyczynowosci. Istnieja trzy glowne powody pozornej korelacji bez zwiazku przyczynowego: 1) Zmienna ukryta (confounding) -- trzecia zmienna Z wplywa na obie. 2) Przypadek -- przy malym N latwo o spurious correlation. 3) Trend czasowy -- obie zmienne rosna w czasie z roznych powodow.",
            "Jak ustalamy przyczynowos c? Zlotym standardem jest eksperyment z randomizacja (RCT): losowo przydzielamy uczestnikow do grup i manipulujemy zmienna X. Bez randomizacji mozemy uzywac badan naturalnych, analizy regresji z kontrola zmiennych ukrytych lub kryteriow Bradforda-Hilla (sila, specyficznosc, koherencja, temporalnosc).",
            "Przyklad klasyczny: spozycie lodow koreluje z liczba utoniec (r=0.88). Pulapka -- wspolna przyczyna to pora roku. Latem ludzie jada wiecej lodow i wiecej plywa. Przyklad przyczynowy: palenie papierosow i rak pluc -- potwierdzony w setkach badan kohortowych i eksperymentow na zwierzetach.",
        ],
        "notes": [
            "Przy malym N nawet duze r moze byc przypadkowe. Przed wyciaganiem wnioskow zawsze sprawdzaj: ile mamy obserwacji? Jaki jest 95% przedzial ufnosci dla r? Zasada: N < 30 to za malo by ufac r bez testu istotnosci.",
            "Sila korelacji nie informuje o mechanizmie przyczynowym. r=0.93 miedzy sprzedaza iPhone a wskaznikiem samobojstw w USA to trend czasowy, nie przyczynowosc. Zawsze pytaj: co moze byc wspolna przyczyna? Czy jest tu trend czasowy? Jaki bylby wynik eksperymentu?",
            "Korelacja Pearsona zaklada liniowosc zwiazku i normalnosc obu zmiennych. Dla zwiazkow nieliniowych (np. odwrocone U) r ~ 0 mimo wyraznego wzorca. Zawsze patrz na wykres punktowy -- samo r nie wystarcza!",
        ],
        "tasks": [
            "W Fazie A: ustaw r=0.9, N=20 i r=0.9, N=200. Jak rozni sie wyglad chmury punktow? Teraz utrzymaj r=0.9, N=200 i zwieksz szum do 0.8. Jak zmienilo sie wizualne wrazenie? Czy r sie zmienilo?",
            "W Fazie B: przejdz przez wszystkie 8 scenariuszy. Dla kazdego spurious -- znajdz zmienna ukryta zanim klikniesz 'Poddaj sie'. Dla kazdego causal -- zastanow sie jak mozna to sprawdzic eksperymentalnie.",
            "W Fazie C: znajdz 3 pary zmiennych z r > 0.7. Dla kazdej zapisz: czy to przyczynowosc, zmienna ukryta czy trend czasowy? Potem znajdz pare z r najblizszym 0 -- co laczy te zmienne?",
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
