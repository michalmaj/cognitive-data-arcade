"""Lesson 06 - Exploratory Data Analysis."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Eksploracyjna analiza danych (EDA, Tukey 1977) to badanie struktury danych przed testowaniem hipotez. Cel: wykrywanie anomalii, rozumienie rozkładów i znajdowanie wzorców. EDA generuje hipotezy - nie testuje ich.",
            "Mediana to preferowana miara centralna dla RT, bo jest odporna na wartości skrajne. SD opisuje rozrzut, ale jest wrażliwe na wartości odstające. IQR (Q3 - Q1) jest odporny na ogon rozkładu. Skośność surowego RT jest prawie zawsze dodatnia.",
            "Podstawowe wizualizacje RT to histogram (pełny kształt rozkładu), wykres pudełkowy (mediana, IQR, wartości odstające), wykres skrzypcowy (kształt + statystyki) i wykres Q-Q (odchylenie od normalności). Każdy ujawnia coś innego - żaden nie wystarcza sam.",
            "Kwartet Anscombe'a (1973): cztery zbiory danych o identycznych średnich, wariancjach i korelacjach, ale zupełnie różnych wykresach rozrzutu. Korelacja bez wykresu rozrzutu jest niekompletna.",
            "Datasaurus Dozen (Matejka i Fitzmaurice, CHI 2017) - 12 zbiorów danych o identycznych statystykach opisowych (średnia, SD, korelacja) ale całkowicie różnych kształtach, w tym dinozaur. Rozszerza pomysł Anscombe'a i ukazuje, że samo describe() pandas może całkowicie ominąć strukturę danych.",
            "Florence Nightingale (1858) stworzyła diagramy biegunowe obszarowe, aby zilustrować przyczyny śmiertelności podczas wojny krymskiej. Wizualizacja przekonała brytyjski parlament do poprawy warunków sanitarnych w szpitalach polowych - jeden z pierwszych historycznych przykładów użycia wizualizacji danych do podjęcia decyzji politycznych.",
            "Przepływ pracy EDA: (1) wczytaj i sprawdź wymiary/typy, (2) policz braki, (3) oblicz describe(), (4) narysuj rozkłady według warunków, (5) porównaj warunki ze słupkami błędów, (6) sprawdź trendy czasowe. Dopiero potem formułuj hipotezę.",
            "Jeśli podczas EDA rozkłady RT dla warunku niezgodnego i zgodnego prawie sie nie nakładają, efekt Stroopa jest duży i niezawodny. d Cohena wyraża różnicę w jednostkach SD - efekt poniżej d = 0,2 jest trywialny nawet przy p < 0,001.",
        ],
        "notes": [
            "Różnica dwóch liczb bez kontekstu rozkładu jest niejednoznaczna. Te same wartości średnich RT mogą opisywać całkowicie inną sytuację zależnie od kształtu rozkładu - warto zawsze porównywać histogramy, nie tylko tabele statystyk.",
            "Wykres Q-Q dla RT prawie zawsze odchyla sie od linii w prawym górnym rogu - to prawy ogon rozkładu RT. Transformacja logarytmiczna lub test nieparametryczny jest naturalną odpowiedzią na to odchylenie.",
            "Wynik EDA, który nie był preregistrowany, jest eksploracyjny, nie konfirmacyjny. HARKing (hypothesizing after results are known) prowadzi do nadmiernej liczby fałszywie pozytywnych wyników.",
        ],
        "tasks": [
            "Wczytaj plik CSV sesji Stroopa. Oblicz mean, median, SD i skewness osobno dla każdego warunku. Który warunek ma największą skośność i dlaczego?",
            "Narysuj histogram RT dla każdego warunku z zaznaczoną średnią i medianą. Czy rozkład jest prawostronnie skośny? Czy średnia leży na prawo od mediany?",
            "Narysuj wykres Q-Q dla RT. Czy dane są normalnie rozłożone? Co to mówi o możliwości użycia sparowanego t-testu na surowym RT?",
        ],
    },
    "en": {
        "theory": [
            "Exploratory Data Analysis (EDA, Tukey 1977) is the investigation of data structure before hypothesis testing. Goals: detect anomalies, understand distributions, find patterns. EDA generates hypotheses - it does not test them.",
            "Descriptive statistics for RT: the median is a robust measure of central tendency. Standard deviation (SD) describes spread but is sensitive to extreme values. IQR (Q3 - Q1) is resistant to the distribution's tail. Skewness for raw RT is almost always positive.",
            "Visualisations for RT: histogram (full distribution shape), box plot (median, IQR, outliers), violin plot (shape + summary statistics), Q-Q plot (departure from normality). Each reveals something different - none is sufficient alone.",
            "Anscombe's Quartet (1973): four datasets with identical means, variances, and correlations but completely different scatter plots. A correlation coefficient without a scatter plot is incomplete.",
            "Datasaurus Dozen (Matejka and Fitzmaurice, CHI 2017) - 12 datasets with identical descriptive statistics (mean, SD, correlation) but completely different shapes, including a dinosaur. It extends Anscombe's idea and shows that running pandas describe() alone can entirely miss the structure of the data.",
            "Florence Nightingale (1858) created polar area charts to illustrate the causes of mortality during the Crimean War. The visualisation persuaded the British Parliament to improve sanitary conditions in field hospitals - one of the earliest documented examples of data visualisation driving a policy decision.",
            "The EDA workflow: (1) load and check dimensions/types, (2) count missing values, (3) compute describe(), (4) plot distributions per condition, (5) compare conditions with error bars, (6) check temporal trends. Only then form a hypothesis.",
            "Stroop EDA: if the RT distributions for incongruent and congruent conditions barely overlap, the effect is large and reliable. Cohen's d expresses the difference in SD units - an effect below d = 0.2 is trivial even at p < 0.001.",
        ],
        "notes": [
            "The difference between two numbers without distributional context is ambiguous. The same mean RT values can describe entirely different situations depending on the shape of the distribution - comparing histograms rather than just summary tables is essential.",
            "A Q-Q plot for RT almost always departs from the diagonal in the upper right - that is the right tail of the RT distribution. Log transformation or a non-parametric test is the natural response to this departure.",
            "An EDA result that was not pre-registered is exploratory, not confirmatory. HARKing (hypothesizing after results are known) inflates the false-positive rate.",
        ],
        "tasks": [
            "Load a Stroop session CSV. Compute mean, median, SD, and skewness separately for each condition. Which condition has the highest skewness and why?",
            "Plot an RT histogram for each condition with the mean and median marked. Is the distribution right-skewed? Does the mean fall to the right of the median?",
            "Plot a Q-Q plot for RT. Are the data normally distributed? What does this imply about using a paired t-test on raw RT?",
        ],
    },
}
