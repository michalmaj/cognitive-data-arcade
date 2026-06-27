"""Lesson 03 - Event Logs and Data Formats."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Log zdarzeń to opatrzony znacznikiem czasu rejestr dyskretnych zdarzeń podczas eksperymentu: pojawienie się bodźca, naciśniecie klawisza, dostarczenie informacji zwrotnej. Każdy eksperyment behawioralny generuje taki log - Donders robił to ręcznie w 1868 roku; dziś robi się to automatycznie z precyzją milisekundową.",
            "Chronoskop Hippa (ok. 1843) - pierwsze urządzenie do pomiaru czasu reakcji z dokładnością do 1/1000 sekundy. Donders użył go w badaniach z 1868 roku, które zapoczątkowały chronometrię umysłową. Wcześniej pomiar czasu trwania prostych operacji umysłowych był technicznie niemożliwy.",
            "Popularne formaty danych: CSV/TSV (płaskie, czytelne dla człowieka, otwieralne wszędzie), JSON (hierarchiczny, obsługuje zagnieżdżone metadane), HDF5 (binarny, wydajny dla dużych sygnałów jak EEG), EDF/BDF (standard klinicznego EEG). Wybór formatu to kompromis między czytelnością, rozmiarem i zdolnością do reprezentowania struktury.",
            "Historia formatu CSV - format sięga roku 1972, gdy IBM używał go na komputerach mainframe. Standard RFC 4180 oficjalnie opisujący CSV powstał dopiero w 2005 roku - przez ponad 30 lat format ten był powszechnie stosowany bez żadnej formalnej specyfikacji.",
            "Anatomia logu behawioralnego: participant_id, session_id, trial_id, condition, stimulus_onset_ms, response_time_ms, response_key, correct. Każda kolumna służy celowi - trial_id umożliwia analizę efektów kolejności, stimulus_onset_ms pozwala na wyrównanie z sygnałami fizjologicznymi, correct jest potrzebny do kryteriów wykluczenia.",
            "Problem wyrównania czasowego: komputer bodźców i wzmacniacz EEG mają oddzielne zegary. Niezesynchronizowany dryf 20 ms między nimi zniszczyłby wszystkie analizy ERP. Rozwiązaniem są wyzwalacze TTL - impuls elektryczny wysyłany jednocześnie z bodźcem trafia do strumienia danych EEG jako wspólny punkt odniesienia.",
            "Częstotliwości próbkowania i precyzja: EEG przy 1000 Hz rejestruje co 1 ms - wystarczająco do rozróżnienia P100 od N200. Standardowe odpytywanie klawiatury USB odbywa się co 8 ms. To jest granica precyzji pomiaru RT na typowym sprzęcie konsumenckim - efekt o wielkości 10 ms jest statystycznie nieinterpretowalny.",
            "Rozmiary plików EEG - godzinna sesja przy 256 kanałach i 2048 Hz generuje ok. 900 MB surowych danych. Format EDF+ (European Data Format) kompresuje te dane do ok. 150 MB. Baza danych PhysioNet zawiera ponad 100 TB danych elektrofizjologicznych dostępnych publicznie i bezpłatnie.",
            "Standard BIDS (Gorgolewski i in., 2016) określa ujednolicony układ katalogów i pliki pomocnicze JSON dla zbiorów danych neuroobrazowania. OpenNeuro przechowuje tysiące zbiorów danych w formacie BIDS do swobodnego pobrania. Kryzys replikacji był częściowo napędzany przez brak takich standardów - różne laboratoria, różne nazwy kolumn, niemożliwa do zreplikowania analiza.",
        ],
        "notes": [
            "Czytelność kontra rozmiar - CSV otwiera się w Excelu, ale plik CSV z 10 milionami wierszy zablokuje komputer. HDF5 jest nieczytelny dla człowieka, ale obsługuje terabajty bez utraty wydajności. Dobry format to taki, który pasuje do rozmiaru i struktury danych.",
            "RT wewnątrz urządzenia kontra między urządzeniami - RT obliczony na jednym komputerze (czas upływający od bodźca do odpowiedzi na tej samej maszynie) jest wewnętrznie spójny. Problem pojawia się tylko przy wyrównywaniu logów z dwóch różnych systemów, np. logu behawioralnego i EEG.",
            "Kryzys replikacji a dokumentacja - Open Science Collaboration (2015) podjęła próbę replikacji 100 opublikowanych badań psychologicznych. Tylko 36% dało wyniki spójne z oryginałem. Część niepowodzeń wynikała z niedokładnej dokumentacji procedury - brak opisów skryptów analizy, różne nazwy zmiennych w różnych publikacjach.",
            "BIDS jest korzystny przede wszystkim dla samego badacza - standaryzacja przynosi korzyść własną. Zbiór danych, który nie może być ponownie analizowany dwa lata po zebraniu z powodu braku opisu kolumn, ma ograniczoną wartość naukową.",
        ],
        "tasks": [
            "Otwórz plik CSV z data/generated/ i zidentyfikuj każdą z ośmiu standardowych kolumn. Dla każdej kolumny napisz jedno zdanie wyjaśniające jej cel analityczny.",
            "Znajdź kolumnę zawierającą czas reakcji w milisekundach. Zapisz wartość minimalną i maksymalną. Sprawdź, czy participant_id jest identyczne we wszystkich wierszach.",
            "Odejmij pierwszy stimulus_onset_ms od ostatniego i przelicz na sekundy - to przybliżony czas trwania sesji. Oblicz średni interwał między dwiema kolejnymi próbami.",
        ],
    },
    "en": {
        "theory": [
            "An event log is a timestamped record of discrete events during an experiment: stimulus onset, keypress, feedback delivery. Every behavioural experiment produces one - Donders did it by hand in 1868; today it is done automatically with millisecond precision.",
            "The Hipp chronoscope (c. 1843) - the first device capable of measuring reaction time to 1/1000 of a second. Donders used it in the 1868 studies that launched mental chronometry. Before this instrument, measuring the duration of simple mental operations was technically impossible.",
            "Common data formats: CSV/TSV (flat, human-readable, opens anywhere), JSON (hierarchical, supports nested metadata), HDF5 (binary, efficient for large signals like EEG), EDF/BDF (clinical EEG standard). Format choice is a trade-off between readability, file size, and the ability to represent structure.",
            "The history of CSV - the format dates to 1972, when IBM used it on mainframe computers. The RFC 4180 standard formally describing CSV was not published until 2005 - for over 30 years the format was in widespread use without any formal specification.",
            "Anatomy of a behavioural log: participant_id, session_id, trial_id, condition, stimulus_onset_ms, response_time_ms, response_key, correct. Each column has a purpose - trial_id enables order-effect analysis, stimulus_onset_ms allows alignment with physiological signals, correct is needed for exclusion criteria.",
            "The time-alignment problem: the stimulus computer and the EEG amplifier have separate clocks. An unsynchronised 20 ms drift between them would destroy all ERP analyses. The solution is TTL triggers - an electrical pulse sent simultaneously with the stimulus arrives in the EEG data stream as a shared reference point.",
            "Sampling rates and precision: EEG at 1000 Hz records every 1 ms - enough to separate P100 from N200. Standard USB keyboard polling occurs every 8 ms. That is the precision floor for RT measurement on typical consumer hardware - a 10 ms effect is statistically uninterpretable.",
            "EEG file sizes - a one-hour session at 256 channels and 2048 Hz generates approximately 900 MB of raw data. The EDF+ (European Data Format) standard compresses this to around 150 MB. The PhysioNet database holds over 100 TB of electrophysiological data available for free public download.",
            "The BIDS standard (Gorgolewski et al., 2016) specifies a unified directory layout and JSON sidecar files for neuroimaging datasets. OpenNeuro hosts thousands of BIDS-formatted datasets for free download. The replication crisis was partly driven by the absence of such standards - different labs, different column names, unreproducible analyses.",
        ],
        "notes": [
            "Readability vs. size - CSV opens in Excel, but a CSV with 10 million rows will freeze the computer. HDF5 is not human-readable but handles terabytes without performance loss. A good format is one that matches the size and structure of the data.",
            "Within-device RT vs. cross-device alignment - RT computed on one computer (elapsed time from stimulus to response on the same machine) is internally consistent. The problem only arises when aligning logs from two different systems, e.g., a behavioural log and EEG.",
            "The replication crisis and documentation - the Open Science Collaboration (2015) attempted to replicate 100 published psychology studies. Only 36% yielded results consistent with the original. Part of the failure rate stemmed from inadequate procedure documentation - missing analysis scripts, inconsistent variable names across publications.",
            "BIDS primarily benefits the researcher themselves - standardisation carries its own reward. A dataset that cannot be re-analysed two years after collection because column names were not documented has limited scientific value.",
        ],
        "tasks": [
            "Open a CSV from data/generated/ and identify each of the eight standard columns. For each column, write one sentence explaining its analytical purpose.",
            "Find the column containing reaction time in milliseconds. Record the minimum and maximum values. Check that participant_id is identical across all rows.",
            "Subtract the first stimulus_onset_ms from the last and convert to seconds - that is the approximate session duration. Calculate the mean inter-trial interval between two consecutive trials.",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "Event Log Detective — Refleksja",
        "cards": [
            {
                "label": "Format",
                "color": "indigo",
                "text": "Event logi to sekwencje zdarzeń z timestampem — zupełnie inaczej niż tabele z jednym wierszem na obserwację.",
            },
            {
                "label": "Standard",
                "color": "orange",
                "text": "BIDS porządkuje pliki tak, żeby każde laboratorium mogło czytać Twoje dane bez dodatkowych instrukcji.",
            },
            {
                "label": "Pułapka",
                "color": "green",
                "text": "Kolejność wierszy w CSV bywa przypadkowa. W logu zdarzeń kolejność to dane — jej utrata niszczy sens pliku.",
            },
        ],
        "question": "Jakie zdarzenia generuje Twoja aplikacja mobilna? Czy można z nich odtworzyć sesję użytkownika?",
    },
    "en": {
        "title": "Event Log Detective — Reflection",
        "cards": [
            {
                "label": "Format",
                "color": "indigo",
                "text": "Event logs are sequences of timestamped events — completely different from tables with one row per observation.",
            },
            {
                "label": "Standard",
                "color": "orange",
                "text": "BIDS organises files so any lab in the world can read your data without extra instructions.",
            },
            {
                "label": "Pitfall",
                "color": "green",
                "text": "Row order in a CSV can be arbitrary. In an event log, order is data — losing it destroys meaning.",
            },
        ],
        "question": "What events does your mobile app generate? Could you reconstruct a user session from them?",
    },
}
