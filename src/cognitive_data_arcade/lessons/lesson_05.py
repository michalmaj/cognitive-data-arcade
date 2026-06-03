"""Lesson 05 — Missing Values and Outliers."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Brakujące dane (Rubin, 1976) dzielą się na trzy typy: MCAR — brak niezwiązany z żadną zmienną; MAR — brak zależy od zmiennych obserwowanych; MNAR — brak zależy od samej brakującej wartości. Typ mechanizmu decyduje o dopuszczalnej metodzie obsługi.",
            "MCAR jest rzadkie w kognitywistyce. Timeout w zadaniu RT oznacza, że uczestnik nie zdążył odpowiedzieć — a to zdarza się częściej w trudnych próbach. Brakujące RT jest więc skorelowane z trudnością próby: klasyczny MNAR.",
            "Metody obsługi braków: usuwanie wierszy (trafne tylko przy MCAR), imputacja średnią (zaniża wariancję), wielokrotna imputacja (generuje m kompletnych zbiorów i łączy wyniki metodą Rubina — złoty standard przy MAR), modele pełnej informacji (FIML).",
            "Wartość odstająca — definicja statystyczna (|z| > 3) i definicja dziedzinowa mogą się różnić. W danych RT: odpowiedź poniżej 100 ms jest fizjologicznie niemożliwa (antycypacja). Odpowiedź powyżej 3 000 ms to prawdopodobnie luka uwagowa.",
            "Rozkłady RT są prawostronnie skośne. Jedna odpowiedź 5 000 ms może zawyżyć średnią o kilkaset milisekund, nie zmieniając mediany. Mediana i ucięta średnia (trimmed mean) są odporne na wartości skrajne.",
            "Standardy APA i CONSORT wymagają raportowania liczby wykluczonych prób, kryterium wykluczenia i podziału na warunki. Przejrzyste raportowanie pozwala ocenić, czy wykluczenia nie wprowadzają systematycznego obciążenia.",
        ],
        "notes": [
            "Kluczowa intuicja: timeout to nie przypadkowy brak — to informacja o trudności próby. Usunięcie timeoutów zaniża szacunek RT w trudnym warunku i sztucznie zmniejsza efekt Stroopa.",
            "Imputacja średnią zachowuje średnią grupową, ale ściska wariancję. Każda analiza oparta na odchyleniach standardowych lub korelacjach będzie zawyżona pod względem pewności.",
            "Pytaj studentów: 'Czy próby z timeoutem są równomiernie rozłożone między warunkami?' Nierówny rozkład to sygnał MNAR i potencjalnego obciążenia przy usuwaniu wierszy.",
        ],
        "tasks": [
            "Wczytaj plik CSV sesji Stroopa. Policz próby z timeoutem łącznie i osobno dla każdego warunku. Czy rozkład jest równomierny?",
            "Oblicz średnią i medianę RT osobno dla każdego warunku. Jaka jest różnica między nimi? Co ta różnica mówi o kształcie rozkładu?",
            "Zastosuj dwie reguły wykluczenia: (a) |z| > 3, (b) RT < 100 ms lub RT > 3 000 ms. Porównaj liczbę wykluczonych prób i wartość efektu Stroopa przed i po wykluczeniu.",
        ],
    },
    "en": {
        "theory": [
            "Missing data (Rubin, 1976) falls into three types: MCAR — missingness unrelated to any variable; MAR — missingness depends on observed variables; MNAR — missingness depends on the missing value itself. The mechanism determines which remedies are valid.",
            "MCAR is rare in cognitive science. A timeout trial means the participant did not respond in time — and this happens more often on difficult trials. The missing RT is correlated with trial difficulty: a textbook case of MNAR.",
            "Handling strategies: listwise deletion (valid only under MCAR), mean imputation (underestimates variability), multiple imputation (generates m complete datasets and pools results using Rubin's rules — gold standard under MAR), full-information maximum likelihood (FIML).",
            "An outlier defined statistically (|z| > 3) and one defined by domain knowledge may differ. In RT data: any response below 100 ms is physiologically impossible (anticipatory). Responses above 3 000 ms likely reflect attentional lapses.",
            "RT distributions are right-skewed. A single 5 000 ms response can shift the mean by hundreds of milliseconds while leaving the median unchanged. The median and trimmed mean are resistant to extreme values.",
            "APA and CONSORT standards require reporting the number of excluded trials, the exclusion criterion, and a condition-by-condition breakdown. Transparent reporting allows readers to assess whether exclusions introduce systematic bias.",
        ],
        "notes": [
            "Key intuition: a timeout is not a random gap — it carries information about trial difficulty. Removing timeouts biases the RT estimate in the hard condition downward and artificially shrinks the Stroop effect.",
            "Mean imputation preserves the group mean but compresses variance. Any analysis relying on standard deviations or correlations will produce overconfident estimates.",
            "Ask students: 'Are timeout trials distributed evenly across conditions?' An uneven distribution is a signal of MNAR and potential bias from listwise deletion.",
        ],
        "tasks": [
            "Load a Stroop session CSV. Count timeout trials in total and separately per condition. Is the distribution even across conditions?",
            "Compute the mean and median RT for each condition. How large is the gap between them? What does it tell you about the shape of the RT distribution?",
            "Apply two exclusion rules: (a) |z| > 3, (b) RT < 100 ms or RT > 3 000 ms. Compare the number of excluded trials and the Stroop effect before and after exclusion.",
        ],
    },
}
