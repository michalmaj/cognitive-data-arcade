"""Lesson 03 — Event Logs and Data Formats."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Log zdarzeń to opatrzony znacznikiem czasu rejestr dyskretnych zdarzeń podczas eksperymentu: pojawienie się bodźca, naciśnięcie klawisza, dostarczenie informacji zwrotnej. Każdy eksperyment behawioralny generuje taki log — Donders robił to ręcznie w 1868 roku; dziś robimy to automatycznie z precyzją milisekundową.",
            "Popularne formaty danych: CSV/TSV (płaskie, czytelne dla człowieka, otwieralne wszędzie), JSON (hierarchiczny, obsługuje zagnieżdżone metadane), HDF5 (binarny, wydajny dla dużych sygnałów jak EEG), EDF/BDF (standard klinicznego EEG). Wybór formatu to kompromis między czytelnością, rozmiarem i zdolnością do reprezentowania struktury.",
            "Anatomia logu behawioralnego: participant_id, session_id, trial_id, condition, stimulus_onset_ms, response_time_ms, response_key, correct. Każda kolumna służy celowi — trial_id umożliwia analizę efektów kolejności, stimulus_onset_ms pozwala na wyrównanie z sygnałami fizjologicznymi, correct jest potrzebny do kryteriów wykluczenia.",
            "Problem wyrównania czasowego: komputer bodźców i wzmacniacz EEG mają oddzielne zegary. Niezesynchronizowany dryf 20 ms między nimi zniszczyłby wszystkie analizy ERP. Rozwiązaniem są wyzwalacze TTL — impuls elektryczny wysyłany jednocześnie z bodźcem trafia do strumienia danych EEG jako wspólny punkt odniesienia.",
            "Częstotliwości próbkowania i precyzja: EEG przy 1000 Hz rejestruje co 1 ms — wystarczająco do rozróżnienia P100 od N200. Standardowe odpytywanie klawiatury USB odbywa się co 8 ms. To jest Twoja granica precyzji: efekt RT o wartości 10 ms jest nieinterpretowalny na konsumenckim sprzęcie klawiatury.",
            "Standard BIDS (Gorgolewski i in., 2016) określa ujednolicony układ katalogów i pliki pomocnicze JSON dla zbiorów danych neuroobrazowania. OpenNeuro przechowuje tysiące zbiorów danych w formacie BIDS do swobodnego pobrania. Kryzys replikacji był częściowo napędzany przez brak takich standardów — różne laboratoria, różne nazwy kolumn, niemożliwa do zreplikowania analiza.",
        ],
        "notes": [
            "Czytelność kontra rozmiar — CSV otwiera się w Excelu, ale plik CSV z 10 milionami wierszy zawiesi Twój laptop. HDF5 jest nieczytelny dla człowieka, ale obsługuje terabajty bez utraty wydajności. Dobry format to taki, który pasuje do rozmiaru i struktury Twoich danych.",
            "RT wewnątrz urządzenia kontra między urządzeniami — RT obliczony na jednym komputerze (czas upływający od bodźca do odpowiedzi na tej samej maszynie) jest wewnętrznie spójny. Problem pojawia się tylko przy wyrównywaniu logów z dwóch różnych systemów, np. logu behawioralnego i EEG.",
            "BIDS to dla Ciebie, nie tylko dla innych — standaryzacja przynosi korzyść samemu badaczowi. Zbiór danych, który nie może być ponownie analizowany dwa lata po zebraniu, ponieważ zapomniałeś, co oznaczają kolumny, ma ograniczoną wartość naukową.",
        ],
        "tasks": [
            "Otwórz plik CSV z data/generated/ i zidentyfikuj każdą z ośmiu standardowych kolumn. Dla każdej kolumny napisz jedno zdanie wyjaśniające jej cel analityczny.",
            "Znajdź kolumnę zawierającą czas reakcji w milisekundach. Zapisz wartość minimalną i maksymalną. Sprawdź, czy participant_id jest identyczne we wszystkich wierszach.",
            "Odejmij pierwszy stimulus_onset_ms od ostatniego i przelicz na sekundy — to przybliżony czas trwania sesji. Oblicz interwał między dwiema kolejnymi próbami.",
        ],
    },
    "en": {
        "theory": [
            "An event log is a timestamped record of discrete events during an experiment: stimulus onset, keypress, feedback delivery. Every behavioural experiment produces one — Donders did it by hand in 1868; today we do it automatically with millisecond precision.",
            "Common data formats: CSV/TSV (flat, human-readable, opens anywhere), JSON (hierarchical, supports nested metadata), HDF5 (binary, efficient for large signals like EEG), EDF/BDF (clinical EEG standard). Format choice is a trade-off between readability, file size, and the ability to represent structure.",
            "Anatomy of a behavioural log: participant_id, session_id, trial_id, condition, stimulus_onset_ms, response_time_ms, response_key, correct. Each column has a purpose — trial_id enables order-effect analysis, stimulus_onset_ms allows alignment with physiological signals, correct is needed for exclusion criteria.",
            "The time-alignment problem: the stimulus computer and the EEG amplifier have separate clocks. An unsynchronised 20 ms drift between them would destroy all ERP analyses. The solution is TTL triggers — an electrical pulse sent simultaneously with the stimulus arrives in the EEG data stream as a shared reference point.",
            "Sampling rates and precision: EEG at 1000 Hz records every 1 ms — enough to separate P100 from N200. Standard USB keyboard polling occurs every 8 ms. That is your precision floor: a 10 ms RT effect is uninterpretable with consumer keyboard hardware.",
            "The BIDS standard (Gorgolewski et al., 2016) specifies a unified directory layout and JSON sidecar files for neuroimaging datasets. OpenNeuro hosts thousands of BIDS-formatted datasets for free download. The replication crisis was partly driven by the absence of such standards — different labs, different column names, unreproducible analyses.",
        ],
        "notes": [
            "Readability vs. size — CSV opens in Excel, but a CSV with 10 million rows will freeze your laptop. HDF5 is not human-readable but handles terabytes without performance loss. A good format is one that matches the size and structure of your data.",
            "Within-device RT vs. cross-device alignment — RT computed on one computer (elapsed time from stimulus to response on the same machine) is internally consistent. The problem only arises when aligning logs from two different systems, e.g., a behavioural log and EEG.",
            "BIDS is for you, not just for others — standardisation benefits the researcher themselves. A dataset that cannot be re-analysed two years after collection because you forgot what the columns mean has limited scientific value.",
        ],
        "tasks": [
            "Open a CSV from data/generated/ and identify each of the eight standard columns. For each column, write one sentence explaining its analytical purpose.",
            "Find the column containing reaction time in milliseconds. Record the minimum and maximum values. Check that participant_id is identical across all rows.",
            "Subtract the first stimulus_onset_ms from the last and convert to seconds — that is the approximate session duration. Calculate the inter-trial interval between two consecutive trials.",
        ],
    },
}
