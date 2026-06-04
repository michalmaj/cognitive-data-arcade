"""Scenario definitions for the Event Log Detective mini-game.

Each scenario presents a series of data-management decisions.
Students choose an option and receive feedback on consequences.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Option:
    label_pl: str
    label_en: str
    is_correct: bool
    consequence_easy_pl: (
        str  # shown in Easy popup before confirm (empty string if correct)
    )
    consequence_easy_en: str


@dataclass(frozen=True)
class Decision:
    title_pl: str
    title_en: str
    context_pl: str  # right-panel context text (always visible)
    context_en: str
    hint_medium_pl: str  # shown when H pressed on Medium
    hint_medium_en: str
    report_pl: str  # explanation shown in final report
    report_en: str
    options: tuple[Option, ...]  # 2-4 options


@dataclass(frozen=True)
class Scenario:
    id: int
    title_pl: str
    title_en: str
    intro_pl: str
    intro_en: str
    decisions: tuple[Decision, ...]


# ---------------------------------------------------------------------------
# Scenario 1 — RT Lab (behavioural experiment, 6 decisions)
# ---------------------------------------------------------------------------

_s1_d1 = Decision(
    title_pl="Format pliku",
    title_en="File format",
    context_pl=(
        "Twój eksperyment mierzy czasy reakcji w zadaniu wyboru. "
        "Zbierasz około 6000 prób od 30 uczestników. "
        "Dane będziesz analizować w Pythonie i Excelu."
    ),
    context_en=(
        "Your experiment measures reaction times in a choice task. "
        "You collect about 6000 trials from 30 participants. "
        "You will analyse the data in Python and Excel."
    ),
    hint_medium_pl=(
        "Pomyśl o tym, co otwiera każdy psycholog bez instalowania dodatkowych narzędzi."
    ),
    hint_medium_en=(
        "Think about what every psychologist can open without installing extra tools."
    ),
    report_pl=(
        "CSV to universalny format tekstowy czytelny przez Excela, Pandas i każdy edytor. "
        "Dla danych tabelarycznych z kilkoma tysiącami wierszy nie potrzebujesz "
        "bardziej złożonego formatu."
    ),
    report_en=(
        "CSV is a universal text format readable by Excel, Pandas, and any editor. "
        "For tabular data with a few thousand rows you don't need a more complex format."
    ),
    options=(
        Option(
            label_pl="CSV",
            label_en="CSV",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="JSON",
            label_en="JSON",
            is_correct=False,
            consequence_easy_pl="JSON wprowadza zbędną złożoność — nie otwiera się w Excelu.",
            consequence_easy_en="JSON: unnecessary complexity, doesn't open in Excel.",
        ),
        Option(
            label_pl="HDF5",
            label_en="HDF5",
            is_correct=False,
            consequence_easy_pl="HDF5 to przerost formy nad treścią dla 6000 wierszy.",
            consequence_easy_en="HDF5: overkill for 6000 rows.",
        ),
        Option(
            label_pl="EDF/BDF",
            label_en="EDF/BDF",
            is_correct=False,
            consequence_easy_pl="EDF służy do sygnału EEG, nie do danych behawioralnych.",
            consequence_easy_en="EDF is for EEG signals, not behavioural data.",
        ),
    ),
)

_s1_d2 = Decision(
    title_pl="Separator kolumn",
    title_en="Separator",
    context_pl=(
        "Zapisujesz dane w formacie CSV. "
        "Musisz wybrać znak oddzielający kolumny. "
        "Plik będzie czytany przez Pandas i Excela w różnych systemach operacyjnych."
    ),
    context_en=(
        "You are saving data in CSV format. "
        "You must choose the character that separates columns. "
        "The file will be read by Pandas and Excel on various operating systems."
    ),
    hint_medium_pl=(
        "Sprawdź, który separator jest domyślnie rozpoznawany przez Pandas i angielski Excel."
    ),
    hint_medium_en=(
        "Check which separator Pandas and English-locale Excel recognise by default."
    ),
    report_pl=(
        "Przecinek i tabulator są domyślnie rozpoznawane przez Pandas (sep=',' i sep='\\t'). "
        "Średnik bywa domyślny w europejskim Excelu, ale wymaga jawnego podania w bibliotekach."
    ),
    report_en=(
        "Comma and tab are recognised by Pandas by default (sep=',' and sep='\\t'). "
        "Semicolon is the default in some European Excel locales but requires "
        "explicit configuration in libraries."
    ),
    options=(
        Option(
            label_pl="Przecinek",
            label_en="Comma",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Tabulator",
            label_en="Tab",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Średnik",
            label_en="Semicolon",
            is_correct=False,
            consequence_easy_pl=(
                "Średnik nie jest rozpoznawany przez część bibliotek — "
                "wymaga dodatkowej konfiguracji."
            ),
            consequence_easy_en=(
                "Semicolon: not recognised by some libraries — requires extra configuration."
            ),
        ),
    ),
)

_s1_d3 = Decision(
    title_pl="Kolumny do zapisania",
    title_en="Columns to save",
    context_pl=(
        "Masz dostęp do pełnego dziennika zdarzeń z 8 kolumnami: "
        "participant_id, session_id, trial_id, condition, stimulus, "
        "expected_response, actual_response, reaction_time_ms. "
        "Chcesz być szybki, ale też mieć dane gotowe do analizy."
    ),
    context_en=(
        "You have access to the full event log with 8 columns: "
        "participant_id, session_id, trial_id, condition, stimulus, "
        "expected_response, actual_response, reaction_time_ms. "
        "You want to be fast but also have data ready for analysis."
    ),
    hint_medium_pl=(
        "Zastanów się, bez których kolumn nie można porównać uczestników ani warunków."
    ),
    hint_medium_en=(
        "Think about which columns are essential to compare participants and conditions."
    ),
    report_pl=(
        "Pełny dziennik pozwala odtworzyć każdą próbę. "
        "Przy ograniczonych kolumnach tracisz informację, której nie da się odzyskać później."
    ),
    report_en=(
        "The full log lets you reconstruct every trial. "
        "With fewer columns you lose information that cannot be recovered later."
    ),
    options=(
        Option(
            label_pl="Pełny dziennik (8 kol.)",
            label_en="Full log (8 col.)",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Tylko RT",
            label_en="RT only",
            is_correct=False,
            consequence_easy_pl=(
                "Brak participant_id, condition i stimulus — prawie żadna analiza nie jest możliwa."
            ),
            consequence_easy_en=(
                "No participant_id, condition or stimulus columns — almost no analysis is possible."
            ),
        ),
        Option(
            label_pl="RT + poprawność",
            label_en="RT + correct",
            is_correct=False,
            consequence_easy_pl=(
                "Brak participant_id — niemożliwe porównanie wyników między uczestnikami."
            ),
            consequence_easy_en=(
                "No participant_id — impossible to compare results across participants."
            ),
        ),
        Option(
            label_pl="Surowe zdarzenia",
            label_en="Raw events",
            is_correct=False,
            consequence_easy_pl=(
                "Surowe zdarzenia wymagają parsowania — trudna analiza bez preprocessingu."
            ),
            consequence_easy_en=(
                "Raw events require parsing — hard to analyse without preprocessing."
            ),
        ),
    ),
)

_s1_d4 = Decision(
    title_pl="Nazwa pliku",
    title_en="File name",
    context_pl=(
        "Będziesz zbierać dane od wielu uczestników przez kilka tygodni. "
        "Pliki będą przechowywane w wspólnym folderze na dysku laboratoryjnym. "
        "Potrzebujesz nazwy, która jednoznacznie identyfikuje sesję."
    ),
    context_en=(
        "You will collect data from many participants over several weeks. "
        "Files will be stored in a shared folder on the lab drive. "
        "You need a name that uniquely identifies the session."
    ),
    hint_medium_pl=(
        "Dobra nazwa pliku powinna zawierać datę i identyfikator uczestnika."
    ),
    hint_medium_en=(
        "A good file name should include the date and participant identifier."
    ),
    report_pl=(
        "Schemat {data}_{pid}.csv pozwala natychmiast zobaczyć, "
        "kiedy i dla kogo zebrano dane, i łatwiej sortować pliki chronologicznie."
    ),
    report_en=(
        "The pattern {date}_{pid}.csv lets you immediately see "
        "when and for whom data were collected, and makes chronological sorting easy."
    ),
    options=(
        Option(
            label_pl="{data}_{pid}.csv",
            label_en="{date}_{pid}.csv",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="data.csv",
            label_en="data.csv",
            is_correct=False,
            consequence_easy_pl=(
                "Plik nadpisany przy następnym uruchomieniu — tracisz poprzednie dane."
            ),
            consequence_easy_en=("Overwritten on next run — you lose previous data."),
        ),
        Option(
            label_pl="exp_{losowy}.csv",
            label_en="exp_{random}.csv",
            is_correct=False,
            consequence_easy_pl=(
                "Losowa nazwa — nie wiadomo kto i kiedy, trudno sortować."
            ),
            consequence_easy_en=("Random name — unknown who and when, hard to sort."),
        ),
    ),
)

_s1_d5 = Decision(
    title_pl="RT < 100 ms",
    title_en="RT < 100 ms",
    context_pl=(
        "Po zebraniu danych zauważysz, że kilka prób ma czas reakcji poniżej 100 ms. "
        "To prawdopodobnie antycypacje lub artefakty sprzętowe. "
        "Musisz zdecydować, co zrobić z tymi obserwacjami."
    ),
    context_en=(
        "After collecting data you notice that some trials have reaction times below 100 ms. "
        "These are likely anticipations or hardware artefacts. "
        "You must decide what to do with these observations."
    ),
    hint_medium_pl=("Pomyśl, jak zachować ślad po każdej decyzji dotyczącej danych."),
    hint_medium_en=("Think about how to preserve a trace of every data decision."),
    report_pl=(
        "Oznaczenie flagą zachowuje dane i zostawia ślad audytowy. "
        "Możesz później wykluczyć flagowane próby albo zbadać ich rozkład."
    ),
    report_en=(
        "Flagging preserves the data and leaves an audit trail. "
        "You can later exclude flagged trials or examine their distribution."
    ),
    options=(
        Option(
            label_pl="Oznacz flagą",
            label_en="Flag it",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Usuń wiersz",
            label_en="Delete row",
            is_correct=False,
            consequence_easy_pl=(
                "Utrata danych bez śladu — nie wiesz ile prób usunięto."
            ),
            consequence_easy_en=(
                "Data loss without trace — you don't know how many trials were removed."
            ),
        ),
        Option(
            label_pl="Zostaw bez zmian",
            label_en="Keep as-is",
            is_correct=False,
            consequence_easy_pl=(
                "Zachowujesz skontaminowane dane — zniekształca średnie RT."
            ),
            consequence_easy_en=("You keep contaminated data — distorts mean RT."),
        ),
    ),
)

_s1_d6 = Decision(
    title_pl="Brak odpowiedzi",
    title_en="Missing response",
    context_pl=(
        "Uczestnik nie odpowiedział na próbę przed upłynięciem czasu. "
        "Pole actual_response i reaction_time_ms są puste. "
        "Musisz ustalić, jaką wartość zapisać w CSV."
    ),
    context_en=(
        "The participant did not respond to a trial before the timeout. "
        "The actual_response and reaction_time_ms fields are empty. "
        "You need to decide what value to write in the CSV."
    ),
    hint_medium_pl=(
        "Sprawdź, która wartość Pandas interpretuje jako brak liczby (a nie tekst)."
    ),
    hint_medium_en=(
        "Check which value Pandas interprets as a missing number (not as text)."
    ),
    report_pl=(
        "NaN jest standardem w Pandas dla brakujących wartości numerycznych. "
        "Pusty string jest czytany jako tekst, NULL nie jest rozpoznawany wszędzie, "
        "a -1 mógłby być pomylony z prawdziwym RT bez dokumentacji."
    ),
    report_en=(
        "NaN is the Pandas standard for missing numeric values. "
        "Empty string is read as text, NULL is not recognised by all Python libraries, "
        "and -1 could be confused with a real RT without documentation."
    ),
    options=(
        Option(
            label_pl="NaN",
            label_en="NaN",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Pusty string",
            label_en="Empty string",
            is_correct=False,
            consequence_easy_pl=(
                "Pusty string — Pandas czyta go jako tekst, nie liczbę."
            ),
            consequence_easy_en=(
                "Empty string — Pandas reads it as text, not a number."
            ),
        ),
        Option(
            label_pl="NULL",
            label_en="NULL",
            is_correct=False,
            consequence_easy_pl=(
                "NULL nie jest rozpoznawany przez wszystkie biblioteki Pythona."
            ),
            consequence_easy_en=("NULL: not recognised by all Python libraries."),
        ),
        Option(
            label_pl="-1",
            label_en="-1",
            is_correct=False,
            consequence_easy_pl=(
                "Wartość -1 nieodróżnialna od prawdziwego RT bez dokumentacji."
            ),
            consequence_easy_en=(
                "-1: indistinguishable from real RT without documentation."
            ),
        ),
    ),
)

scenario1 = Scenario(
    id=1,
    title_pl="Eks. 1: Laboratorium RT",
    title_en="Exp 1: RT Lab",
    intro_pl=(
        "Prowadzisz prosty eksperyment behawioralny mierzacy czasy reakcji. "
        "Masz 30 uczestników, około 200 prób każdy. "
        "Podejmij decyzje dotyczące zapisu i przechowywania danych."
    ),
    intro_en=(
        "You are running a simple behavioural experiment measuring reaction times. "
        "You have 30 participants, about 200 trials each. "
        "Make decisions about how to record and store the data."
    ),
    decisions=(
        _s1_d1,
        _s1_d2,
        _s1_d3,
        _s1_d4,
        _s1_d5,
        _s1_d6,
    ),
)


# ---------------------------------------------------------------------------
# Scenario 2 — EEG + Video (multimodal experiment, 7 decisions)
# ---------------------------------------------------------------------------

_s2_d1 = Decision(
    title_pl="Format danych behawioralnych",
    title_en="Behavioural data format",
    context_pl=(
        "Twój eksperyment łączą EEG z jednoczesnym nagraniem wideo i danymi behawioralnymi. "
        "Dane behawioralne to kilkaset wierszy z czasami reakcji i odpowiedziami. "
        "Wybierz format zapisu dla tej warstwy danych."
    ),
    context_en=(
        "Your experiment combines EEG with simultaneous video and behavioural data. "
        "Behavioural data is a few hundred rows of reaction times and responses. "
        "Choose the storage format for this data layer."
    ),
    hint_medium_pl=("Dane behawioralne to zwykła tabela — wybierz najprostszy format."),
    hint_medium_en=("Behavioural data is a simple table — choose the simplest format."),
    report_pl=(
        "Dla kilkuset wierszy CSV jest optymalny: lekki, czytelny i łatwy do analizy. "
        "Bardziej złożone formaty są tu przesadą."
    ),
    report_en=(
        "For a few hundred rows CSV is optimal: lightweight, readable, and easy to analyse. "
        "More complex formats are overkill here."
    ),
    options=(
        Option(
            label_pl="CSV",
            label_en="CSV",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="JSON",
            label_en="JSON",
            is_correct=False,
            consequence_easy_pl=("JSON to zbędna złożoność dla kilkuset wierszy RT."),
            consequence_easy_en=(
                "JSON: unnecessary complexity for a few hundred RT rows."
            ),
        ),
        Option(
            label_pl="HDF5",
            label_en="HDF5",
            is_correct=False,
            consequence_easy_pl=("HDF5 to przerost formy dla danych behawioralnych."),
            consequence_easy_en=("HDF5: overkill for behavioural data."),
        ),
        Option(
            label_pl="EDF/BDF",
            label_en="EDF/BDF",
            is_correct=False,
            consequence_easy_pl=("EDF służy do sygnału EEG, nie do danych RT."),
            consequence_easy_en=("EDF is for EEG signals, not RT data."),
        ),
    ),
)

_s2_d2 = Decision(
    title_pl="Format sygnału EEG",
    title_en="EEG signal format",
    context_pl=(
        "Rejestrujesz sygnał EEG z 64 elektrod z częstotliwością 1000 Hz przez godzine. "
        "Dane będziesz analizować w MNE-Python. "
        "Wybierz format przechowywania surowego sygnału."
    ),
    context_en=(
        "You record EEG from 64 electrodes at 1000 Hz for one hour. "
        "You will analyse the data in MNE-Python. "
        "Choose the storage format for the raw signal."
    ),
    hint_medium_pl=(
        "Oszacuj rozmiar danych i sprawdź, który format oferuje kompresję."
    ),
    hint_medium_en=(
        "Estimate the data size and check which format offers compression."
    ),
    report_pl=(
        "HDF5 kompresuje dane i umożliwia szybki dostęp do fragmentów sygnału. "
        "MNE-Python czyta i zapisuje HDF5. "
        "CSV zajmie około 10 GB bez kompresji, co sprawia, że parsowanie trwa godzinami."
    ),
    report_en=(
        "HDF5 compresses data and allows fast random access to signal segments. "
        "MNE-Python reads and writes HDF5. "
        "CSV would take around 10 GB uncompressed, making parsing take hours."
    ),
    options=(
        Option(
            label_pl="HDF5",
            label_en="HDF5",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="CSV",
            label_en="CSV",
            is_correct=False,
            consequence_easy_pl=(
                "Około 10 GB nieskompresowanego tekstu — parsowanie trwa godzinami."
            ),
            consequence_easy_en=(
                "Around 10 GB of uncompressed text — parsing takes hours."
            ),
        ),
        Option(
            label_pl="JSON",
            label_en="JSON",
            is_correct=False,
            consequence_easy_pl=(
                "JSON jest jeszcze większy niż CSV dla danych szeregowych."
            ),
            consequence_easy_en=("JSON: even larger than CSV for time-series data."),
        ),
        Option(
            label_pl="EDF/BDF",
            label_en="EDF/BDF",
            is_correct=False,
            consequence_easy_pl=(
                "EDF to standard kliniczny, ale słabe wsparcie MNE dla dużych plików."
            ),
            consequence_easy_en=(
                "EDF/BDF: clinical standard, but poor MNE-Python support for large files."
            ),
        ),
    ),
)

_s2_d3 = Decision(
    title_pl="Synchronizacja TTL",
    title_en="TTL synchronisation",
    context_pl=(
        "Twój eksperyment uruchamia bodzce w oprogramowaniu behawioralnym "
        "i jednoczesnie rejestruje EEG. "
        "Musisz zdecydować, czy używać sygnałów TTL do synchronizacji między systemami."
    ),
    context_en=(
        "Your experiment triggers stimuli in behavioural software "
        "while simultaneously recording EEG. "
        "You must decide whether to use TTL signals to synchronise the two systems."
    ),
    hint_medium_pl=(
        "Zastanów się, co się stanie z analizą ERP jeżeli zegary dwóch systemów nie są zsynchronizowane."
    ),
    hint_medium_en=(
        "Think about what happens to ERP analysis if two system clocks are not synchronised."
    ),
    report_pl=(
        "Bez sygnału TTL dryfowanie zegarów niszczy wyrównanie ERP. "
        "Dwa komputery mogą różnić się o kilka do kilkudziesięciu ms w ciągu godziny."
    ),
    report_en=(
        "Without TTL, clock drift destroys ERP alignment — data will be useless. "
        "Two computers can diverge by tens of milliseconds over an hour."
    ),
    options=(
        Option(
            label_pl="Tak",
            label_en="Yes",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Nie",
            label_en="No",
            is_correct=False,
            consequence_easy_pl=(
                "Dryfowanie zegarów niszczy wyrównanie ERP — dane będą bezużyteczne."
            ),
            consequence_easy_en=(
                "Clock drift destroys ERP alignment — data will be useless."
            ),
        ),
    ),
)

_s2_d4 = Decision(
    title_pl="Częstotliwość próbkowania EEG",
    title_en="EEG sampling rate",
    context_pl=(
        "Interesują cię komponenty ERP: P100, N200 i P300. "
        "Musisz wybrać częstotliwość próbkowania EEG. "
        "Wyższa częstotliwość daje lepszą rozdzielczość, ale też większe pliki."
    ),
    context_en=(
        "You are interested in ERP components: P100, N200 and P300. "
        "You must choose the EEG sampling rate. "
        "Higher rates give better resolution but also larger files."
    ),
    hint_medium_pl=(
        "Przypomnij sobie twierdzenie Nyquista: częstotliwość próbkowania musi być "
        "co najmniej dwa razy większa od najszybszego składnika, który chcesz uchwycić."
    ),
    hint_medium_en=(
        "Recall the Nyquist theorem: sampling rate must be at least twice "
        "the highest frequency component you want to capture."
    ),
    report_pl=(
        "1000 Hz to standard dla ERP — wystarczy do rozróżnienia P100 od N200 "
        "i nie generuje niepotrzebnie dużych plików. "
        "128 Hz jest zbyt małe dla szybkich komponentów."
    ),
    report_en=(
        "1000 Hz is the ERP standard — sufficient to distinguish P100 from N200 "
        "and does not generate unnecessarily large files. "
        "128 Hz is insufficient for fast components."
    ),
    options=(
        Option(
            label_pl="128 Hz",
            label_en="128 Hz",
            is_correct=False,
            consequence_easy_pl=(
                "128 Hz jest niedostateczne do rozróżnienia P100 od N200."
            ),
            consequence_easy_en=("128 Hz: insufficient to distinguish P100 from N200."),
        ),
        Option(
            label_pl="256 Hz",
            label_en="256 Hz",
            is_correct=False,
            consequence_easy_pl=(
                "256 Hz to ryzyko aliasingu dla szybkich komponentów."
            ),
            consequence_easy_en=(
                "256 Hz: borderline — aliasing risk for fast components."
            ),
        ),
        Option(
            label_pl="1000 Hz",
            label_en="1000 Hz",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="2000 Hz",
            label_en="2000 Hz",
            is_correct=False,
            consequence_easy_pl=("2000 Hz podwaja rozmiar danych bez żadnej korzyści."),
            consequence_easy_en=(
                "2000 Hz: unnecessary resolution, doubles data size without benefit."
            ),
        ),
    ),
)

_s2_d5 = Decision(
    title_pl="Przechowywanie wideo",
    title_en="Video storage",
    context_pl=(
        "Nagranie wideo twarzy uczestnika trwa 60 minut per sesja. "
        "Masz 30 uczestników. "
        "Musisz zdecydować, co przechowywać z nagrania wideo."
    ),
    context_en=(
        "Video of the participant's face lasts 60 minutes per session. "
        "You have 30 participants. "
        "You must decide what to store from the video recording."
    ),
    hint_medium_pl=(
        "Oszacuj łącznie, ile miejsca zajmie pełne wideo dla wszystkich uczestników."
    ),
    hint_medium_en=(
        "Estimate the total storage needed for full video across all participants."
    ),
    report_pl=(
        "Klatki kluczowe lub tylko metadane (czas mrugniecia, keypoint twarzy) "
        "redukuja rozmiar z ~50 GB do kilku MB per uczestnika. "
        "Pełne wideo MP4 to problem przestrzenny bez wyraźnej korzyści naukowej."
    ),
    report_en=(
        "Keyframes or metadata only (blink timestamps, face keypoints) "
        "reduce size from ~50 GB to a few MB per participant. "
        "Full MP4 video is a storage problem without clear scientific benefit."
    ),
    options=(
        Option(
            label_pl="Klatki kluczowe",
            label_en="Keyframes",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Tylko metadane",
            label_en="Metadata only",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Pełne wideo (MP4)",
            label_en="Full video (MP4)",
            is_correct=False,
            consequence_easy_pl=(
                "Około 50 GB na sesję — problem z przestrzenią przy 30 uczestnikach."
            ),
            consequence_easy_en=(
                "Around 50 GB per session — storage problem with 30 participants."
            ),
        ),
    ),
)

_s2_d6 = Decision(
    title_pl="Markery zdarzeń",
    title_en="Event markers",
    context_pl=(
        "Bodzce sa wyzwalane synchronicznie w oprogramowaniu behawioralnym i EEG. "
        "Markery zdarzeń można zapisać w osobnym pliku CSV, osadzic w sygnale EEG "
        "lub w obu miejscach jednoczesnie. "
        "Wybierz strategię zapisu markerów."
    ),
    context_en=(
        "Stimuli are triggered synchronously in behavioural software and EEG. "
        "Event markers can be stored in a separate CSV file, embedded in the EEG signal, "
        "or in both places simultaneously. "
        "Choose the marker storage strategy."
    ),
    hint_medium_pl=(
        "Zastanów się nad nadmiarowością: co się stanie, jeśli jeden ze zbiorów danych zostanie uszkodzony?"
    ),
    hint_medium_en=(
        "Think about redundancy: what happens if one of the data sources is corrupted?"
    ),
    report_pl=(
        "Zapis w obu miejscach zapewnia nadmiarowość. "
        "Jeśli jeden plik zostanie uszkodzony lub zaginiony, można odtworzyć markery z drugiego źródła."
    ),
    report_en=(
        "Storing in both places provides redundancy. "
        "If one file is corrupted or lost, markers can be recovered from the other source."
    ),
    options=(
        Option(
            label_pl="Oba",
            label_en="Both",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Osobny CSV",
            label_en="Separate CSV",
            is_correct=False,
            consequence_easy_pl=(
                "Jeden plik — jeśli uszkodzony, tracisz wszystkie markery."
            ),
            consequence_easy_en=("Single file — if corrupted, you lose all markers."),
        ),
        Option(
            label_pl="Osadzone w EEG",
            label_en="Embedded in EEG",
            is_correct=False,
            consequence_easy_pl=("Jeden rekord — ryzyko utraty przy błędzie formatu."),
            consequence_easy_en=("Single record — risk of loss on format error."),
        ),
        Option(
            label_pl="Żadne",
            label_en="None",
            is_correct=False,
            consequence_easy_pl=(
                "Bez markerów niemożliwe wyrównanie EEG z bodźcami po fakcie."
            ),
            consequence_easy_en=(
                "Without markers it's impossible to align EEG with stimuli after the fact."
            ),
        ),
    ),
)

_s2_d7 = Decision(
    title_pl="Organizacja plików",
    title_en="File organisation",
    context_pl=(
        "Masz 30 uczestników, każdy z plikiem EEG, CSV behawioralnym i metadanymi. "
        "To łącznie około 100 plików. "
        "Wybierz schemat organizacji katalogów."
    ),
    context_en=(
        "You have 30 participants, each with an EEG file, behavioural CSV and metadata. "
        "That's around 100 files in total. "
        "Choose a directory organisation scheme."
    ),
    hint_medium_pl=(
        "Pomyśl o tym, jak znaleźć wszystkie pliki konkretnego uczestnika za 2 lata."
    ),
    hint_medium_en=(
        "Think about how to find all files for a specific participant two years from now."
    ),
    report_pl=(
        "Katalogi per uczestnik lub standard BIDS (Brain Imaging Data Structure) "
        "ułatwiają nawigację i są zrozumiałe dla innych badaczy. "
        "Wszystko w jednym folderze prowadzi do chaosu już przy kilkudziesięciu plikach."
    ),
    report_en=(
        "Per-participant directories or BIDS (Brain Imaging Data Structure) "
        "make navigation easy and are understandable by other researchers. "
        "All files in one directory leads to chaos beyond a few dozen files."
    ),
    options=(
        Option(
            label_pl="Katalogi per uczestnik",
            label_en="Per-participant dirs",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="BIDS",
            label_en="BIDS",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Wszystko w jednym katalogu",
            label_en="All in one directory",
            is_correct=False,
            consequence_easy_pl=("3000 plików w jednym folderze -> chaos."),
            consequence_easy_en=("3000 files in one folder -> chaos."),
        ),
    ),
)

scenario2 = Scenario(
    id=2,
    title_pl="Eks. 2: EEG + Wideo",
    title_en="Exp 2: EEG + Video",
    intro_pl=(
        "Projektujesz multimodalny eksperyment łączący EEG z nagraniem wideo twarzy "
        "i danymi behawioralnymi. "
        "Podejmij decyzje dotyczące formatów, synchronizacji i przechowywania danych."
    ),
    intro_en=(
        "You are designing a multimodal experiment combining EEG with face video "
        "and behavioural data. "
        "Make decisions about formats, synchronisation, and data storage."
    ),
    decisions=(
        _s2_d1,
        _s2_d2,
        _s2_d3,
        _s2_d4,
        _s2_d5,
        _s2_d6,
        _s2_d7,
    ),
)


# ---------------------------------------------------------------------------
# Scenario 3 — Multi-site Clinical Study (6 decisions)
# ---------------------------------------------------------------------------

_s3_d1 = Decision(
    title_pl="Format wymiany EEG",
    title_en="EEG exchange format",
    context_pl=(
        "Prowadzisz wieloośrodkowe badanie kliniczne EEG w 5 szpitalach. "
        "Każdy ośrodek używa innego oprogramowania do akwizycji. "
        "Musisz wybrać wspólny format wymiany plików EEG."
    ),
    context_en=(
        "You run a multi-site clinical EEG study at 5 hospitals. "
        "Each site uses different acquisition software. "
        "You must choose a common exchange format for EEG files."
    ),
    hint_medium_pl=(
        "Sprawdź, który format EEG jest standardem w oprogramowaniu klinicznym na całym świecie."
    ),
    hint_medium_en=(
        "Check which EEG format is the standard in clinical software worldwide."
    ),
    report_pl=(
        "EDF/BDF to międzynarodowy standard kliniczny wspierany przez wszystkie systemy EEG. "
        "Zawiera metadane kliniczne i jest czytelny przez każde oprogramowanie do analizy EEG."
    ),
    report_en=(
        "EDF/BDF is the international clinical standard supported by all EEG systems. "
        "It includes clinical metadata and is readable by every EEG analysis package."
    ),
    options=(
        Option(
            label_pl="EDF/BDF",
            label_en="EDF/BDF",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="CSV",
            label_en="CSV",
            is_correct=False,
            consequence_easy_pl=(
                "CSV traci metadane kliniczne i rozdzielczość czasowa."
            ),
            consequence_easy_en=("CSV: loses clinical metadata and time resolution."),
        ),
        Option(
            label_pl="HDF5",
            label_en="HDF5",
            is_correct=False,
            consequence_easy_pl=(
                "HDF5 nie jest obsługiwany przez kliniczne oprogramowanie EEG."
            ),
            consequence_easy_en=("HDF5: not supported by clinical EEG software."),
        ),
        Option(
            label_pl="JSON",
            label_en="JSON",
            is_correct=False,
            consequence_easy_pl=("JSON nie nadaje sie do sygnału EEG."),
            consequence_easy_en=("JSON: not suitable for EEG signals."),
        ),
    ),
)

_s3_d2 = Decision(
    title_pl="Standaryzacja struktury",
    title_en="Structure standardisation",
    context_pl=(
        "Każdy szpital prowadzi własną dokumentację w innych formatach i z innymi nazwami kolumn. "
        "Przed meta-analizą musisz zdecydować, jak ujednolicić strukturę danych między ośrodkami."
    ),
    context_en=(
        "Each hospital maintains its own documentation in different formats "
        "and with different column names. "
        "Before meta-analysis you must decide how to standardise data structure across sites."
    ),
    hint_medium_pl=(
        "Poszukaj standardu specyficznego dla neuronauki, który definiuje nazwy plików i strukturę folderów."
    ),
    hint_medium_en=(
        "Look for a neuroscience-specific standard that defines file names and folder structure."
    ),
    report_pl=(
        "BIDS (Brain Imaging Data Structure) to otwarty standard zaprojektowany "
        "specjalnie dla danych neuronaukowych. "
        "Każdy badacz na świecie rozumie strukturę BIDS bez dokumentacji."
    ),
    report_en=(
        "BIDS (Brain Imaging Data Structure) is an open standard designed "
        "specifically for neuroscience data. "
        "Every researcher worldwide understands BIDS structure without documentation."
    ),
    options=(
        Option(
            label_pl="BIDS",
            label_en="BIDS",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Brak standaryzacji",
            label_en="None",
            is_correct=False,
            consequence_easy_pl=(
                "Każdy szpital ma inne nazwy kolumn -> niemożliwa meta-analiza."
            ),
            consequence_easy_en=(
                "Each hospital has its own column names -> impossible meta-analysis."
            ),
        ),
        Option(
            label_pl="Własna konwencja",
            label_en="Own convention",
            is_correct=False,
            consequence_easy_pl=("Własna konwencja: inni naukowcy jej nie znają."),
            consequence_easy_en=("Own convention: other scientists won't know it."),
        ),
    ),
)

_s3_d3 = Decision(
    title_pl="Nazewnictwo plików",
    title_en="File naming",
    context_pl=(
        "Masz 5 ośrodków, każdy zbiera dane od 50 pacjentów przez 2 lata. "
        "Pliki EEG będą transferowane między ośrodkami i archiwizowane. "
        "Wybierz schemat nazewnictwa plików."
    ),
    context_en=(
        "You have 5 sites, each collecting data from 50 patients over 2 years. "
        "EEG files will be transferred between sites and archived. "
        "Choose the file naming scheme."
    ),
    hint_medium_pl=(
        "Dobra nazwa pliku powinna być jednoznaczna między ośrodkami i czytelna po 5 latach."
    ),
    hint_medium_en=(
        "A good file name should be unique across sites and readable after 5 years."
    ),
    report_pl=(
        "Standard BIDS definiuje nazwy w postaci sub-001_task-rest_eeg.edf. "
        "Ten schemat jest jednoznaczny, sortowalny i zrozumialy dla wszystkich użytkowników BIDS."
    ),
    report_en=(
        "BIDS defines names in the form sub-001_task-rest_eeg.edf. "
        "This scheme is unique, sortable, and understandable to all BIDS users."
    ),
    options=(
        Option(
            label_pl="BIDS (sub-001_task-rest_eeg.edf)",
            label_en="BIDS (sub-001_task-rest_eeg.edf)",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="patient_001.edf",
            label_en="patient_001.edf",
            is_correct=False,
            consequence_easy_pl=("Kolizje między ośrodkami i nieczytelne po 5 latach."),
            consequence_easy_en=(
                "Collides between sites and unreadable after 5 years."
            ),
        ),
        Option(
            label_pl="{ośrodek}_{sub}_{data}.edf",
            label_en="{site}_{sub}_{date}.edf",
            is_correct=False,
            consequence_easy_pl=("Własna konwencja — inne ośrodki będą miały inne."),
            consequence_easy_en=(
                "Own convention — other sites will have different ones."
            ),
        ),
    ),
)

_s3_d4 = Decision(
    title_pl="Metadane uczestnika",
    title_en="Participant metadata",
    context_pl=(
        "Zbierasz dane od pacjentów klinicznych: płeć, wiek, diagnozę, leki. "
        "Musisz zdecydować, jakie metadane łączyć z danymi EEG "
        "i jak je przechowywać."
    ),
    context_en=(
        "You collect data from clinical patients: sex, age, diagnosis, medication. "
        "You must decide which metadata to link with EEG data "
        "and how to store it."
    ),
    hint_medium_pl=(
        "Pomyśl o RODO: jakie dane mogą być przechowywane razem z sygnałami EEG?"
    ),
    hint_medium_en=(
        "Think about GDPR: which data can be stored together with EEG signals?"
    ),
    report_pl=(
        "Sidecar JSON z ID + wiek + płeć jest zgodny z BIDS i RODO. "
        "Pełna dokumentacja kliniczna w pliku EEG naruszałaby RODO — "
        "dane wrażliwe muszą być oddzielone od danych badawczych."
    ),
    report_en=(
        "JSON sidecar with ID + age + gender is BIDS-compliant and GDPR-safe. "
        "Full clinical record in the EDF file would violate GDPR — "
        "sensitive data must be separated from research data."
    ),
    options=(
        Option(
            label_pl="ID + wiek + płeć w JSON sidecar",
            label_en="ID + age + gender in JSON sidecar",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Tylko ID",
            label_en="ID only",
            is_correct=False,
            consequence_easy_pl=(
                "Brak metadanych demograficznych — niemożliwa analiza wg wieku/płci."
            ),
            consequence_easy_en=(
                "No demographic metadata — impossible age/gender analysis."
            ),
        ),
        Option(
            label_pl="Pełna dokumentacja kliniczna w EDF",
            label_en="Full clinical record in EDF",
            is_correct=False,
            consequence_easy_pl=("Naruszenie RODO — dane wrażliwe w pliku danych."),
            consequence_easy_en=("GDPR violation — sensitive data in data file."),
        ),
    ),
)

_s3_d5 = Decision(
    title_pl="Format raportu klinicznego",
    title_en="Clinical report format",
    context_pl=(
        "Każdy ośrodek generuje raporty kliniczne po badaniu EEG. "
        "Raporty będą później agregowane i automatycznie przetwarzane "
        "w ramach meta-analizy wieloośrodkowej."
    ),
    context_en=(
        "Each site generates clinical reports after EEG examination. "
        "Reports will later be aggregated and automatically processed "
        "in a multi-site meta-analysis."
    ),
    hint_medium_pl=("Zastanów sie, który format łatwo parsuje skrypt Pythona bez NLP."),
    hint_medium_en=(
        "Think about which format a Python script can parse easily without NLP."
    ),
    report_pl=(
        "Ustrukturyzowany JSON lub HL7 FHIR umożliwiają automatyczne przetwarzanie. "
        "Tekst w Wordzie lub PDF wymaga drogiego NLP lub ręcznego parsowania."
    ),
    report_en=(
        "Structured JSON or HL7 FHIR enable automated processing. "
        "Word free text or PDF require expensive NLP or manual parsing."
    ),
    options=(
        Option(
            label_pl="Ustrukturyzowany JSON",
            label_en="Structured JSON",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="HL7 FHIR",
            label_en="HL7 FHIR",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Wolny tekst Word",
            label_en="Free text Word",
            is_correct=False,
            consequence_easy_pl=(
                "Niemożliwe automatyczne przetwarzanie bez drogiego NLP."
            ),
            consequence_easy_en=(
                "Impossible automated processing without expensive NLP."
            ),
        ),
        Option(
            label_pl="PDF",
            label_en="PDF",
            is_correct=False,
            consequence_easy_pl=("PDF jest trudny do automatycznego parsowania."),
            consequence_easy_en=("PDF: hard to parse automatically."),
        ),
    ),
)

_s3_d6 = Decision(
    title_pl="Wersjonowanie danych",
    title_en="Data versioning",
    context_pl=(
        "W trakcie badania pojdą poprawki: zmiana protokołu, korekty anotacji, "
        "aktualizacja oprogramowania do akwizycji. "
        "Musisz zdecydować, jak śledzić wersje plików danych."
    ),
    context_en=(
        "During the study there will be corrections: protocol changes, annotation fixes, "
        "acquisition software updates. "
        "You must decide how to track versions of data files."
    ),
    hint_medium_pl=(
        "Pomyśl, jak zachować historię zmian bez nadpisywania oryginalnych plików."
    ),
    hint_medium_en=(
        "Think about how to keep a history of changes without overwriting original files."
    ),
    report_pl=(
        "Nowe wersje z sufiksem (_v2, _v3) zachowują wszystkie wersje i są zrozumiałe "
        "nawet dla użytkowników bez wiedzy o gicie. "
        "Nadpisywanie niszczy historię i uniemożliwia reprodukcję wyników."
    ),
    report_en=(
        "New versions with suffix (_v2, _v3) preserve all versions and are understandable "
        "even for users without git knowledge. "
        "Overwriting destroys history and makes results irreproducible."
    ),
    options=(
        Option(
            label_pl="Nowe wersje z sufiksem (_v2)",
            label_en="New versions with suffix (_v2)",
            is_correct=True,
            consequence_easy_pl="",
            consequence_easy_en="",
        ),
        Option(
            label_pl="Brak wersjonowania",
            label_en="None",
            is_correct=False,
            consequence_easy_pl=(
                "Nie wiadomo co się zmieniło i kiedy -> niereprodukowalne."
            ),
            consequence_easy_en=("Unknown what changed and when -> irreproducible."),
        ),
        Option(
            label_pl="Nadpisz plik",
            label_en="Overwrite file",
            is_correct=False,
            consequence_easy_pl=("Utrata historii — nie można cofnac błędów."),
            consequence_easy_en=("History loss — can't undo errors."),
        ),
        Option(
            label_pl="Git LFS",
            label_en="Git LFS",
            is_correct=False,
            consequence_easy_pl=(
                "Git LFS wymaga wiedzy o gicie — nieodpowiednie dla klinicystów."
            ),
            consequence_easy_en=(
                "Git LFS: requires git knowledge — not appropriate for clinicians."
            ),
        ),
    ),
)

scenario3 = Scenario(
    id=3,
    title_pl="Eks. 3: Wieloośrodkowe Badanie Kliniczne",
    title_en="Exp 3: Multi-site Clinical Study",
    intro_pl=(
        "Koordynujesz wieloośrodkowe badanie kliniczne EEG w 5 szpitalach w Europie. "
        "Dane będą zbierane przez 2 lata i poddane meta-analizie. "
        "Podejmij kluczowe decyzje dotyczące standardów i zarządzania danymi."
    ),
    intro_en=(
        "You coordinate a multi-site clinical EEG study at 5 hospitals across Europe. "
        "Data will be collected over 2 years and subjected to meta-analysis. "
        "Make key decisions about standards and data management."
    ),
    decisions=(
        _s3_d1,
        _s3_d2,
        _s3_d3,
        _s3_d4,
        _s3_d5,
        _s3_d6,
    ),
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

SCENARIOS: tuple[Scenario, ...] = (scenario1, scenario2, scenario3)
