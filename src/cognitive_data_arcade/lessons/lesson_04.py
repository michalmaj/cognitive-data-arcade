"""Lesson 04+05 — Data Quality Lab (Data Cleaning + Missing Values and Outliers)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Surowe dane to hipoteza o tym, co się wydarzyło. Są produktem sprzętu o skończonej precyzji, oprogramowania z opóźnieniami i uczestników, którzy mrugają i naciskają złe klawisze. Wyczyszczone dane to Twoje najlepsze przybliżenie rzeczywistości — skonstruowane przez zastosowanie jawnych, udokumentowanych kryteriów.",
            "Kategorie brudnych danych: zduplikowane wiersze (awaria i restart sesji), wartości niemożliwe (RT = -400 ms), wartości poza zakresem (RT = 50000 ms), błędy kodowania (klawisz odpowiedzi jako '\\\\n'), brakujące wpisy, niejednoznaczność strefy czasowej. Każda wymaga innego podejścia do wykrycia i obsługi.",
            "Kryteria wykluczenia RT: odpowiedzi < 100 ms to antycypacje — mózg nie zdążył przetworzyć bodźca. Odpowiedzi > 2000-3000 ms to przerwy uwagi. Próby bez odpowiedzi (timeout) to trzecia kategoria — nie wolne odpowiedzi, ale nieobecne. Nigdy nie mieszaj tych trzech kategorii.",
            "Dziennik czyszczenia dokumentuje każdą decyzję: jakie kryterium, ile prób wykluczono, ile procent całości, w jakich warunkach. Prerejestracja na OSF (osf.io) ustala kryteria przed zobaczeniem danych — uniemożliwia wybieranie progu, który daje pożądany wynik (p-hacking).",
            "Reguła 5-10%: jeśli więcej niż 5-10% prób w warunku jest wykluczonych, wynik jest niepewny. Asymetryczne wskaźniki wykluczenia (2% w warunku zgodnym vs. 12% w niezgodnym) są same w sobie odkryciem — wskazują na jakościowo różne zaangażowanie uczestnika.",
            "Odtwarzalne czyszczenie oznacza skrypt, który można uruchomić ponownie z surowych danych i zawsze daje ten sam wynik. Ręczna edycja CSV w Excelu jest niewidoczna dla kontroli wersji i niemożliwa do odtworzenia. Skrypt Python z pandas to ścieżka audytu.",
            "Brakujące dane (Rubin, 1976) dzielą się na trzy typy: MCAR — brak niezwiązany z żadną zmienną; MAR — brak zależy od zmiennych obserwowanych; MNAR — brak zależy od samej brakującej wartości. Typ mechanizmu decyduje o dopuszczalnej metodzie obsługi.",
            "MCAR jest rzadkie w kognitywistyce. Timeout w zadaniu RT oznacza, że uczestnik nie zdążył odpowiedzieć — a to zdarza się częściej w trudnych próbach. Brakujące RT jest więc skorelowane z trudnością próby: klasyczny MNAR.",
            "Metody obsługi braków: usuwanie wierszy (trafne tylko przy MCAR), imputacja średnią (zaniża wariancję), wielokrotna imputacja (generuje m kompletnych zbiorów i łączy wyniki metodą Rubina — złoty standard przy MAR), modele pełnej informacji (FIML).",
            "Wartość odstająca — definicja statystyczna (|z| > 3) i definicja dziedzinowa mogą się różnić. W danych RT: odpowiedź poniżej 100 ms jest fizjologicznie niemożliwa (antycypacja). Odpowiedź powyżej 3 000 ms to prawdopodobnie luka uwagowa.",
            "Rozkłady RT są prawostronnie skośne. Jedna odpowiedź 5 000 ms może zawyżyć średnią o kilkaset milisekund, nie zmieniając mediany. Mediana i ucięta średnia (trimmed mean) są odporne na wartości skrajne.",
            "Standardy APA i CONSORT wymagają raportowania liczby wykluczonych prób, kryterium wykluczenia i podziału na warunki. Przejrzyste raportowanie pozwala ocenić, czy wykluczenia nie wprowadzają systematycznego obciążenia.",
        ],
        "notes": [
            "Błąd kontra wykluczona próba — nieprawidłowe odpowiedzi to prawidłowe dane dla analiz dokładności. Nie wykluczaj ich z liczników dokładności. Możesz wykluczyć błędne odpowiedzi z analiz RT, jeśli interesuje Cię tylko szybkość prawidłowych odpowiedzi — ale musisz to jawnie stwierdzić.",
            "Agresywne czyszczenie to też problem — usuwanie zbyt wielu prób redukuje wariancję i może sztucznie zmienić rozkład RT. Czyszczenie motywowane zasadami biologicznymi (antycypacje, przerwy) różni się od czyszczenia motywowanego chęcią uzyskania lepszych wyników.",
            "Wskaźnik wykluczenia 0% nie oznacza, że dane są idealne — oznacza, że sesja była krótka i uczestnik był skupiony. Sesje z 0% wykluczeniem są wiarygodne; sesje z 15% wykluczeniem w jednym warunku wymagają wyjaśnienia.",
            "Kluczowa intuicja: timeout to nie przypadkowy brak — to informacja o trudności próby. Usunięcie timeoutów zaniża szacunek RT w trudnym warunku i sztucznie zmniejsza efekt Stroopa.",
            "Imputacja średnią zachowuje średnią grupową, ale ściska wariancję. Każda analiza oparta na odchyleniach standardowych lub korelacjach będzie zawyżona pod względem pewności.",
            "Pytaj studentów: 'Czy próby z timeoutem są równomiernie rozłożone między warunkami?' Nierówny rozkład to sygnał MNAR i potencjalnego obciążenia przy usuwaniu wierszy.",
        ],
        "tasks": [
            "Otwórz plik CSV z data/generated/ i policz łączną liczbę prób. Następnie zastosuj filtry, aby znaleźć: (1) próby z RT < 100 ms, (2) próby z RT > 2000 ms, (3) próby z brakującym RT.",
            "Wypełnij tabelę wykluczeń: liczba i procent dla każdej kategorii. Oblicz łączny wskaźnik wykluczenia. Czy jest powyżej, czy poniżej 5%?",
            "Wpisz w Pythonie: załaduj CSV przez pandas, zastosuj trzy maski (mask_anticipation, mask_lapse, mask_timeout) i wydrukuj: Razem / Wykluczone (%) / Wlaczone. Sprawdź, czy liczby zgadzają się z ręcznym liczeniem.",
            "Wczytaj plik CSV sesji Stroopa. Policz próby z timeoutem łącznie i osobno dla każdego warunku. Czy rozkład jest równomierny?",
            "Oblicz średnią i medianę RT osobno dla każdego warunku. Jaka jest różnica między nimi? Co ta różnica mówi o kształcie rozkładu?",
            "Zastosuj dwie reguły wykluczenia: (a) |z| > 3, (b) RT < 100 ms lub RT > 3 000 ms. Porównaj liczbę wykluczonych prób i wartość efektu Stroopa przed i po wykluczeniu.",
        ],
    },
    "en": {
        "theory": [
            "Raw data is a hypothesis about what happened. It is the product of hardware with finite precision, software with scheduling latency, and participants who blink and press the wrong key. Cleaned data is your best approximation of reality — constructed by applying explicit, documented criteria.",
            "Categories of dirty data: duplicate rows (session crash and restart), impossible values (RT = -400 ms), out-of-range values (RT = 50000 ms), encoding errors (response key as '\\\\n'), missing entries, timezone ambiguity. Each requires a different approach to detection and handling.",
            "RT exclusion criteria: responses < 100 ms are anticipations — the brain had not yet processed the stimulus. Responses > 2000–3000 ms are attentional lapses. Trials with no response (timeout) are a third category — not slow responses, but absent ones. Never conflate these three categories.",
            "A cleaning log documents every decision: what criterion, how many trials excluded, what percentage of total, in which conditions. Pre-registration on OSF (osf.io) fixes criteria before seeing the data — it prevents choosing the threshold that produces the desired result (p-hacking).",
            "The 5–10% rule of thumb: if more than 5–10% of trials in a condition are excluded, the result is unreliable. Asymmetric exclusion rates (2% in congruent vs. 12% in incongruent) are themselves a finding — they indicate qualitatively different participant engagement.",
            "Reproducible cleaning means a script that can be re-run from raw data and always produces the same output. Manual CSV editing in Excel is invisible to version control and cannot be reproduced. A Python pandas script is the audit trail.",
            "Missing data (Rubin, 1976) falls into three types: MCAR — missingness unrelated to any variable; MAR — missingness depends on observed variables; MNAR — missingness depends on the missing value itself. The mechanism determines which remedies are valid.",
            "MCAR is rare in cognitive science. A timeout trial means the participant did not respond in time — and this happens more often on difficult trials. The missing RT is correlated with trial difficulty: a textbook case of MNAR.",
            "Handling strategies: listwise deletion (valid only under MCAR), mean imputation (underestimates variability), multiple imputation (generates m complete datasets and pools results using Rubin's rules — gold standard under MAR), full-information maximum likelihood (FIML).",
            "An outlier defined statistically (|z| > 3) and one defined by domain knowledge may differ. In RT data: any response below 100 ms is physiologically impossible (anticipatory). Responses above 3 000 ms likely reflect attentional lapses.",
            "RT distributions are right-skewed. A single 5 000 ms response can shift the mean by hundreds of milliseconds while leaving the median unchanged. The median and trimmed mean are resistant to extreme values.",
            "APA and CONSORT standards require reporting the number of excluded trials, the exclusion criterion, and a condition-by-condition breakdown. Transparent reporting allows readers to assess whether exclusions introduce systematic bias.",
        ],
        "notes": [
            "Error vs. excluded trial — incorrect responses are valid data for accuracy analyses. Do not exclude them from accuracy counts. You may exclude incorrect responses from RT analyses if you are only interested in correct-response speed — but you must state this explicitly.",
            "Aggressive cleaning is also a problem — removing too many trials reduces variance and can artificially shift the RT distribution. Cleaning motivated by biological principles (anticipations, lapses) is different from cleaning motivated by a desire for better-looking results.",
            "An exclusion rate of 0% does not mean the data are perfect — it means the session was short and the participant was focused. Sessions with 0% exclusion are credible; sessions with 15% exclusion in one condition require explanation.",
            "Key intuition: a timeout is not a random gap — it carries information about trial difficulty. Removing timeouts biases the RT estimate in the hard condition downward and artificially shrinks the Stroop effect.",
            "Mean imputation preserves the group mean but compresses variance. Any analysis relying on standard deviations or correlations will produce overconfident estimates.",
            "Ask students: 'Are timeout trials distributed evenly across conditions?' An uneven distribution is a signal of MNAR and potential bias from listwise deletion.",
        ],
        "tasks": [
            "Open a CSV from data/generated/ and count the total number of trials. Then apply filters to find: (1) trials with RT < 100 ms, (2) trials with RT > 2000 ms, (3) trials with missing RT.",
            "Fill in the exclusion table: count and percentage for each category. Calculate the total exclusion rate. Is it above or below 5%?",
            "In Python: load the CSV via pandas, apply three masks (mask_anticipation, mask_lapse, mask_timeout) and print: Total / Excluded (%) / Included. Check that the numbers match your manual count.",
            "Load a Stroop session CSV. Count timeout trials in total and separately per condition. Is the distribution even across conditions?",
            "Compute the mean and median RT for each condition. How large is the gap between them? What does it tell you about the shape of the RT distribution?",
            "Apply two exclusion rules: (a) |z| > 3, (b) RT < 100 ms or RT > 3 000 ms. Compare the number of excluded trials and the Stroop effect before and after exclusion.",
        ],
    },
}
