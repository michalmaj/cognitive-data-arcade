"""Lesson 05 - Missing Values and Outliers."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Brakujące dane (Rubin, 1976) dzielą sie na trzy typy: MCAR - brak niezwiązany z żadną zmienną; MAR - brak zależy od zmiennych obserwowanych; MNAR - brak zależy od samej brakującej wartości. Typ mechanizmu decyduje o dopuszczalnej metodzie obsługi.",
            "MCAR jest rzadkie w kognitywistyce. Timeout w zadaniu RT oznacza, że uczestnik nie zdążył odpowiedzieć - a to zdarza sie częściej w trudnych próbach. Brakujące RT jest więc skorelowane z trudnością próby: klasyczny MNAR.",
            "Wielokrotna imputacja - metodę opracował Donald Rubin w monografii z 1987 roku ('Multiple Imputation for Nonresponse in Surveys'). Algorytm generuje m (typowo 20-100) kompletnych zbiorów przez losowanie z rozkładu posteriori brakujących wartości, analizuje każdy osobno i łączy wyniki regułami Rubina. Pozwala na poprawne propagowanie niepewności.",
            "Algorytm MICE (Multiple Imputation by Chained Equations) - van Buuren i Groothuis-Oudshoorn, 2011. Każda zmienna z brakami jest imputowana osobno za pomocą modelu regresji na pozostałych zmiennych. Pakiet R 'mice' ma ponad 500 000 pobrań miesięcznie i stał sie de facto standardem w naukach społecznych.",
            "Metody obsługi braków: usuwanie wierszy (trafne tylko przy MCAR), imputacja średnią (zaniża wariancję), wielokrotna imputacja (złoty standard przy MAR), modele pełnej informacji (FIML - Full Information Maximum Likelihood).",
            "Wykres pudełkowy Tukeya (1977) - John Tukey zdefiniował wartości odstające jako punkty poza 1.5 x IQR (rozstęp ćwiartkowy). Opublikował to w 'Exploratory Data Analysis'. Definicja 1.5 x IQR nie ma podstaw probabilistycznych - Tukey dobrał ją empirycznie, bo dawała rozsądne wyniki na wielu zbiorach danych.",
            "Wartość odstająca - definicja statystyczna (|z| > 3) i definicja dziedzinowa mogą sie różnić. W danych RT: odpowiedź poniżej 100 ms jest fizjologicznie niemożliwa (antycypacja). Odpowiedź powyżej 3 000 ms to prawdopodobnie luka uwagowa.",
            "Winsoryzacja (ang. winsorizing) - alternatywa dla usuwania wartości skrajnych: zastąpienie wartości powyżej p-tego percentyla wartością na tym percentylu zamiast ich usuwania. Nazwa pochodzi od Charlesa Winsora - biometrycy z Harvardu, który popularyzował metodę w latach 40. XX w. Winsoryzacja zachowuje n (liczbę prób) przy ograniczeniu wpływu wartości ekstremalnych.",
            "Rozkłady RT są prawostronnie skośne. Jedna odpowiedź 5 000 ms może zawyżyć średnią o kilkaset milisekund, nie zmieniając mediany. Mediana i ucięta średnia (trimmed mean) są odporne na wartości skrajne.",
            "Standardy APA i CONSORT wymagają raportowania liczby wykluczonych prób, kryterium wykluczenia i podziału na warunki. Przejrzyste raportowanie pozwala ocenić, czy wykluczenia nie wprowadzają systematycznego obciążenia.",
        ],
        "notes": [
            "Timeout to nie przypadkowy brak, ale informacja o trudności próby. Usunięcie timeoutów zaniża szacunek RT w trudnym warunku i sztucznie zmniejsza efekt Stroopa.",
            "Imputacja średnią zachowuje średnią grupową, ale ściska wariancję. Każda analiza oparta na odchyleniach standardowych lub korelacjach da zawyżone wyniki pod względem pewności statystycznej.",
            "Nierówny rozkład prób z timeoutem między warunkami to sygnał MNAR. Warto sprawdzić proporcje timeoutów osobno dla każdego warunku przed wyborem metody obsługi braków.",
            "Winsoryzacja a usuwanie wartości skrajnych - winsoryzacja zachowuje pełną liczebność próby i jest mniej podatna na wpływ progu decyzji niż twarde wykluczenie. Zmienia jednak rozkład w sposób subtelny, co może być ważne przy analizach opartych na skośności.",
        ],
        "tasks": [
            "Wczytaj plik CSV sesji Stroopa. Policz próby z timeoutem łącznie i osobno dla każdego warunku. Czy rozkład jest równomierny?",
            "Oblicz średnią i medianę RT osobno dla każdego warunku. Jaka jest różnica między nimi? Co ta różnica mówi o kształcie rozkładu?",
            "Zastosuj dwie reguły wykluczenia: (a) |z| > 3, (b) RT < 100 ms lub RT > 3 000 ms. Porównaj liczbę wykluczonych prób i wartość efektu Stroopa przed i po wykluczeniu.",
        ],
    },
    "en": {
        "theory": [
            "Missing data (Rubin, 1976) falls into three types: MCAR - missingness unrelated to any variable; MAR - missingness depends on observed variables; MNAR - missingness depends on the missing value itself. The mechanism determines which remedies are valid.",
            "MCAR is rare in cognitive science. A timeout trial means the participant did not respond in time - and this happens more often on difficult trials. The missing RT is correlated with trial difficulty: a textbook case of MNAR.",
            "Multiple imputation - the method was developed by Donald Rubin in his 1987 monograph ('Multiple Imputation for Nonresponse in Surveys'). The algorithm generates m (typically 20-100) complete datasets by sampling from the posterior distribution of missing values, analyses each separately, and combines results using Rubin's rules. This allows for correct propagation of uncertainty.",
            "The MICE algorithm (Multiple Imputation by Chained Equations) - van Buuren and Groothuis-Oudshoorn, 2011. Each variable with missingness is imputed separately using a regression model on the remaining variables. The R package 'mice' has over 500,000 monthly downloads and has become the de facto standard in social sciences.",
            "Handling strategies: listwise deletion (valid only under MCAR), mean imputation (underestimates variability), multiple imputation (gold standard under MAR), full-information maximum likelihood (FIML).",
            "Tukey's boxplot (1977) - John Tukey defined outliers as points beyond 1.5 x IQR (interquartile range). He published this in 'Exploratory Data Analysis'. The 1.5 x IQR threshold has no probabilistic derivation - Tukey selected it empirically because it produced reasonable results across many datasets.",
            "An outlier defined statistically (|z| > 3) and one defined by domain knowledge may differ. In RT data: any response below 100 ms is physiologically impossible (anticipatory). Responses above 3 000 ms likely reflect attentional lapses.",
            "Winsorizing - an alternative to removing extreme values: replacing values above the p-th percentile with the value at that percentile rather than deleting them. Named after Charles Winsor, a Harvard biometrician who popularised the method in the 1940s. Winsorizing preserves n (trial count) while limiting the influence of extreme observations.",
            "RT distributions are right-skewed. A single 5 000 ms response can shift the mean by hundreds of milliseconds while leaving the median unchanged. The median and trimmed mean are resistant to extreme values.",
            "APA and CONSORT standards require reporting the number of excluded trials, the exclusion criterion, and a condition-by-condition breakdown. Transparent reporting allows readers to assess whether exclusions introduce systematic bias.",
        ],
        "notes": [
            "A timeout is not a random gap - it carries information about trial difficulty. Removing timeouts biases the RT estimate in the hard condition downward and artificially shrinks the Stroop effect.",
            "Mean imputation preserves the group mean but compresses variance. Any analysis relying on standard deviations or correlations will produce overconfident statistical estimates.",
            "An uneven distribution of timeout trials across conditions is a signal of MNAR. Checking timeout proportions per condition before choosing a missing-data remedy is essential.",
            "Winsorizing vs. outlier removal - winsorizing preserves the full sample size and is less sensitive to the choice of threshold than hard exclusion. It does change the distribution in a subtle way, which may matter for analyses based on skewness.",
        ],
        "tasks": [
            "Load a Stroop session CSV. Count timeout trials in total and separately per condition. Is the distribution even across conditions?",
            "Compute the mean and median RT for each condition. How large is the gap between them? What does it tell you about the shape of the RT distribution?",
            "Apply two exclusion rules: (a) |z| > 3, (b) RT < 100 ms or RT > 3 000 ms. Compare the number of excluded trials and the Stroop effect before and after exclusion.",
        ],
    },
}
