"""Lesson 06 — Exploratory Data Analysis."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Eksploracyjna analiza danych (EDA, Tukey 1977) to badanie struktury danych przed testowaniem hipotez. Cel: wykryć anomalie, zrozumieć rozkłady, znaleźć wzorce. EDA generuje hipotezy — nie testuje ich.",
            "Statystyki opisowe dla RT: mediana jest miarą centralną odporną na wartości odstające. Odchylenie standardowe (SD) opisuje rozrzut, ale jest wrażliwe na skrajne wartości. IQR (Q3 − Q1) jest odporne na ogon rozkładu. Skośność dla surowego RT jest prawie zawsze dodatnia.",
            "Wizualizacje dla RT: histogram (pełny kształt rozkładu), wykres pudełkowy (mediana, IQR, wartości odstające), wykres skrzypcowy (kształt + statystyki), wykres Q-Q (odchylenie od normalności). Każdy ujawnia coś innego — żaden nie jest wystarczający sam w sobie.",
            "Kwartet Anscombe'a (1973): cztery zbiory danych o identycznych średnich, wariancjach i korelacjach, ale zupełnie różnych wykresach rozrzutu. Korelacja bez wykresu rozrzutu jest niekompletna.",
            "Przepływ pracy EDA: (1) wczytaj i sprawdź wymiary/typy, (2) policz braki, (3) oblicz describe(), (4) narysuj rozkłady według warunków, (5) porównaj warunki ze słupkami błędów, (6) sprawdź trendy czasowe. Dopiero potem formułuj hipotezę.",
            "Efekt Stroopa w EDA: jeśli rozkłady RT dla warunku niezgodnego i zgodnego niemal się nie nakładają, efekt jest duży i niezawodny. d Cohena wyraża różnicę w jednostkach SD — efekt poniżej d = 0,2 jest trywialny nawet przy p < 0,001.",
        ],
        "notes": [
            "Otwarcie zajęć: daj studentom dwie liczby (średnie RT dla dwóch warunków) i zapytaj, czy różnica jest realna. Potem pokaż, że te same liczby mogą opisywać zupełnie inną sytuację zależnie od kształtu rozkładu.",
            "Wykres Q-Q dla RT prawie zawsze odchyla się od linii w prawym górnym rogu — to prawy ogon rozkładu RT. Użyj tego, by wprowadzić transformację logarytmiczną i testy nieparametryczne.",
            "Wynik EDA, który nie był pre-rejestrowany, jest eksploracyjny, nie konfirmacyjny. Podkreśl różnicę: HARKing (hypothesizing after results are known) prowadzi do nadmiernej liczby fałszywie pozytywnych wyników.",
        ],
        "tasks": [
            "Wczytaj plik CSV sesji Stroopa. Oblicz mean, median, SD i skewness osobno dla każdego warunku. Który warunek ma największą skośność i dlaczego?",
            "Narysuj histogram RT dla każdego warunku z zaznaczoną średnią i medianą. Czy rozkład jest prawostronnie skośny? Czy średnia leży na prawo od mediany?",
            "Narysuj wykres Q-Q dla RT. Czy dane są normalnie rozłożone? Co to mówi o możliwości użycia sparowanego t-testu na surowym RT?",
        ],
    },
    "en": {
        "theory": [
            "Exploratory Data Analysis (EDA, Tukey 1977) is the investigation of data structure before hypothesis testing. Goals: detect anomalies, understand distributions, find patterns. EDA generates hypotheses — it does not test them.",
            "Descriptive statistics for RT: the median is a robust measure of central tendency. Standard deviation (SD) describes spread but is sensitive to extreme values. IQR (Q3 − Q1) is resistant to the distribution's tail. Skewness for raw RT is almost always positive.",
            "Visualizations for RT: histogram (full distribution shape), box plot (median, IQR, outliers), violin plot (shape + summary statistics), Q-Q plot (departure from normality). Each reveals something different — none is sufficient alone.",
            "Anscombe's Quartet (1973): four datasets with identical means, variances, and correlations but completely different scatter plots. A correlation coefficient without a scatter plot is incomplete.",
            "The EDA workflow: (1) load and check dimensions/types, (2) count missing values, (3) compute describe(), (4) plot distributions per condition, (5) compare conditions with error bars, (6) check temporal trends. Only then form a hypothesis.",
            "Stroop EDA: if the RT distributions for incongruent and congruent conditions barely overlap, the effect is large and reliable. Cohen's d expresses the difference in SD units — an effect below d = 0.2 is trivial even at p < 0.001.",
        ],
        "notes": [
            "Opening activity: give students two numbers (mean RT for two conditions) and ask whether the difference is real. Then show that the same numbers can describe a completely different situation depending on the distribution's shape.",
            "A Q-Q plot for RT almost always departs from the diagonal in the upper right — that is the right tail of the RT distribution. Use this to introduce log-transformation and non-parametric tests.",
            "An EDA result that was not pre-registered is exploratory, not confirmatory. Stress the distinction: HARKing (hypothesizing after results are known) inflates the false-positive rate.",
        ],
        "tasks": [
            "Load a Stroop session CSV. Compute mean, median, SD, and skewness separately for each condition. Which condition has the highest skewness and why?",
            "Plot an RT histogram for each condition with the mean and median marked. Is the distribution right-skewed? Does the mean fall to the right of the median?",
            "Plot a Q-Q plot for RT. Are the data normally distributed? What does this imply about using a paired t-test on raw RT?",
        ],
    },
}
