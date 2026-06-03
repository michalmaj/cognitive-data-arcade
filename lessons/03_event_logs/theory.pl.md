# Teoria — Logi zdarzeń i formaty danych

## 1. Czym jest log zdarzeń?

Każdy eksperyment behawioralny generuje **log zdarzeń**: opatrzony znacznikiem czasu rejestr dyskretnych, dających się datować zdarzeń, które wystąpiły w trakcie sesji. Log zdarzeń odpowiada na pytanie: *co się stało i dokładnie kiedy?* Typowe zdarzenia to: pojawienie się bodźca na ekranie, odpowiedź uczestnika (naciśnięcie klawisza lub przycisku), dostarczenie informacji zwrotnej oraz adnotacje eksperymentatora.

Badanie czasu reakcji Franciscusa Dondersa z 1868 roku jest najwcześniejszym sformalizowanym przykładem rozumowania w kategoriach logów zdarzeń. Jego tabela danych zapisywała dla każdej próby typ bodźca i czas, który upłynął do odpowiedzi — dokładnie te same dwie kolumny, które pojawiają się w każdym nowoczesnym logu RT. Struktura konceptualna nie zmieniła się przez 150 lat; wzrosły jedynie precyzja i objętość danych.

Nowoczesne eksperymenty mogą rejestrować tysiące zdarzeń na sekundę. Zapis EEG przy częstotliwości 1 000 Hz generuje 1 000 próbek z znacznikami czasu na sekundę na elektrodę; czepek z 64 kanałami daje 64 000 wartości opatrzonych znacznikiem czasu na sekundę. Paradygmaty behawioralne działające w PsychoPy lub E-Prime emitują zdarzenia na poziomie prób, ale leżąca u ich podstaw infrastruktura czasowa może rozwiązywać interwały poniżej milisekundy przy odpowiedniej konfiguracji sprzętu.

## 2. Popularne formaty danych

### CSV i TSV

**Wartości oddzielone przecinkami (CSV)** i **wartości oddzielane tabulatorem (TSV)** są uniwersalnymi formatami przechowywania danych w naukach behawioralnych. Każdy wiersz to jedna obserwacja; każda kolumna — jedna zmienna; wartości są oddzielone przecinkiem lub znakiem tabulatora.

Zalety: czytelne dla człowieka, edytowalne w dowolnej aplikacji arkuszowej, parsowalne przez każde oprogramowanie statystyczne (R, Python, SPSS, MATLAB). Nie wymagają żadnych specjalnych bibliotek.

Wady: tylko struktura płaska — zagnieżdżone lub hierarchiczne metadane (np. współrzędne elektrod, nazwy kanałów, adnotacje na poziomie sesji) nie mogą być elegancko reprezentowane bez dodatkowych plików pomocniczych. Duże pliki (powyżej 10 milionów wierszy) zaczynają obciążać pamięć.

### JSON

**JavaScript Object Notation (JSON)** to format tekstowy obsługujący zagnieżdżone struktury klucz-wartość, tablice i mieszane typy danych w jednym dokumencie.

Zalety: hierarchiczny — pojedynczy dokument JSON może zawierać dane demograficzne uczestnika, parametry sesji i wszystkie zdarzenia na poziomie prób w naturalnie zagnieżdżonej strukturze. Parsowany przez każdy nowoczesny język programowania.

Wady: rozwlekły (klucze są powtarzane przy każdym rekordzie na płaskiej liście), wolniejszy w parsowaniu niż formaty binarne dla dużych plików, nie importowany bezpośrednio do tradycyjnego oprogramowania statystycznego bez wstępnego przetwarzania.

### HDF5

**Hierarchical Data Format version 5 (HDF5)** to format binarny przeznaczony do dużych zbiorów danych numerycznych. Organizuje dane w hierarchię grup i zbiorów danych podobną do systemu plików, obsługuje kompresję i umożliwia częściowy odczyt (wczytanie fragmentu dużej tablicy bez ładowania całego pliku).

Zalety: wyjątkowo wydajny dla dużych sygnałów ciągłych (EEG, szeregi czasowe BOLD fMRI, strumienie akcelerometru). MNE-Python, dominująca biblioteka do analizy EEG/MEG, używa HDF5 wewnętrznie. Pliki mogą osiągać rozmiary terabajtów bez utraty wydajności.

Wady: nieczytelny dla człowieka; wymaga dedykowanych bibliotek (h5py w Pythonie, rhdf5 w R); istnieją problemy ze zgodnością między wersjami biblioteki HDF5.

### EDF i BDF

**European Data Format (EDF)** i jego 24-bitowe rozszerzenie **BDF** to standardowe formaty wymiany danych EEG w badaniach klinicznych i naukowych. EDF został zaprojektowany w 1992 roku przez Kempa i in. w celu przesyłania danych polisomnograficznych między systemami szpitalnymi. BDF rozszerza EDF do 24-bitowych próbek, zapewniając wystarczający zakres dynamiczny dla wysokogęstościowych wzmacniaczy EEG.

Zalety: powszechnie obsługiwane przez oprogramowanie do analizy EEG (EEGLAB, MNE-Python, BrainVision Analyzer, MATLAB). Stosowane w klinicznym EEG na całym świecie, co sprawia, że pliki EDF są natychmiast interpretowalne przez każdego neurologa ze standardowym sprzętem.

Wady: stała struktura nagłówka utrudnia osadzanie złożonych metadanych eksperymentalnych. Nieodpowiednie dla danych innych niż EEG.

### Zestawienie kompromisów formatów

| Format | Czytelny dla człowieka | Hierarchiczny | Duże dane | Standard w dziedzinie |
|---|---|---|---|---|
| CSV/TSV | Tak | Nie | Słaby | Nauki behawioralne |
| JSON | Tak | Tak | Słaby | Interfejsy API, pliki pomocnicze z metadanymi |
| HDF5 | Nie | Tak | Doskonały | Neuroobrazowanie, EEG |
| EDF/BDF | Nie | Nie | Dobry | Kliniczne EEG |

## 3. Anatomia behawioralnego logu zdarzeń

Dobrze ustrukturyzowany log behawioralny zawiera kolumny, które razem jednoznacznie identyfikują każdą obserwację i rejestrują wszystko, co jest potrzebne do analizy. Poniższa tabela opisuje standardowe kolumny w plikach generowanych przez tę aplikację:

| Kolumna | Typ | Cel |
|---|---|---|
| `participant_id` | ciąg znaków | Jednoznacznie identyfikuje uczestnika we wszystkich sesjach i badaniach |
| `session_id` | ciąg/liczba całkowita | Identyfikuje pojedynczą ciągłą sesję nagrania |
| `trial_id` | liczba całkowita | Kolejny numer próby w sesji; umożliwia analizę efektów kolejności |
| `condition` | ciąg znaków | Etykieta warunku eksperymentalnego (np. `congruent`, `incongruent`, `go`, `nogo`) |
| `stimulus_onset_ms` | liczba całkowita | Milisekundy od początku sesji do pojawienia się bodźca |
| `response_time_ms` | liczba całkowita | Milisekundy od początku bodźca do odpowiedzi uczestnika (RT) |
| `response_key` | ciąg znaków | Klawisz lub przycisk naciśnięty przez uczestnika |
| `correct` | wartość logiczna | Czy odpowiedź była zgodna z oczekiwaną odpowiedzią dla danej próby |

Każda kolumna służy celowi analitycznemu. `participant_id` i `session_id` umożliwiają modelowanie wielopoziomowe. `trial_id` umożliwia analizy sekwencyjne i efektów ćwiczenia. `condition` to zmienna niezależna. `stimulus_onset_ms` umożliwia wyrównanie czasowe z sygnałami fizjologicznymi. `response_time_ms` to pierwszorzędna zmienna zależna. `response_key` umożliwia analizę błędów. `correct` jest wymagane do kryteriów wykluczenia opartych na dokładności.

Log pozbawiony którejkolwiek z tych kolumn zmusza analityka do przyjęcia założeń — niewidocznych i niemożliwych do weryfikacji przez kogokolwiek czytającego opublikowany artykuł.

## 4. Problem wyrównania czasowego

Synchronizacja znaczników czasu między urządzeniami to jedno z najbardziej wymagających technicznie zagadnień w kognitywnych naukach o mózgu. Rozważmy typowy eksperyment EEG:

1. **Komputer bodźców** uruchamia PsychoPy i rejestruje czas pojawienia się każdego bodźca przy użyciu zegara systemu operacyjnego.
2. **Wzmacniacz EEG** rejestruje ciągłą aktywność mózgu, opatrując ją znacznikami czasu ze swojego własnego oscylatora kwarcowego.
3. **Pudełko odpowiedzi** może korzystać z trzeciego zegara.

Jeśli te trzy zegary nie są zsynchronizowane, eksperymentator nie może dopasować sygnału mózgowego do bodźca. Niezesynchronizowany dryf 20 ms między komputerem bodźców a wzmacniaczem EEG zakłóciłby wszystkie uśrednienia potencjałów wywołanych (ERP), ponieważ komponent „N200" wyśrodkowany w 200 ms po bodźcu byłby w rzeczywistości rozmytą średnią sygnałów występujących między 180 a 220 ms.

### Wyzwalacze TTL

Standardowym rozwiązaniem są **wyzwalacze TTL (Transistor-Transistor Logic)**: komputer bodźców wysyła krótki impuls elektryczny przez port równoległy lub kabel wyzwalacza jednocześnie z każdym pojawieniem się bodźca. Wzmacniacz EEG rejestruje ten impuls jako specjalny kanał obok danych mózgowych, opatrzony znacznikiem czasu własnego zegara wzmacniacza. Ponieważ wyzwalacz dociera do strumienia danych EEG dokładnie w tym samym momencie co bodziec, czasy początku prób można precyzyjnie zrekonstruować w bazie czasowej wzmacniacza — niezależnie od różnicy między zegarami.

### Opóźnienie tylko programowe

Eksperymenty prowadzone bez wyzwalaczy sprzętowych (np. badania online w jsPsych lub zadania tylko behawioralne bez rejestracji fizjologicznej) napotykają niepewność czasową na poziomie oprogramowania. Standardowe odpytywanie klawiatury przez system operacyjny odbywa się w odstępach 8–15 ms na większości konsumenckiego sprzętu, co oznacza, że zarejestrowany znacznik czasu naciśnięcia klawisza może opóźniać się względem rzeczywistego naciśnięcia o maksymalnie 15 ms. Tę granicę precyzji należy uwzględniać przy interpretacji małych różnic RT: efekt o wartości 10 ms mieści się w granicach błędu pomiarowego na konsumenckim sprzęcie.

Precyzyjny pomiar czasu behawioralnego wymaga albo dedykowanych sprzętowych pudełek odpowiedzi (dokładnych do 1 ms lub lepiej), albo platform programowych zsynchronizowanych z odświeżaniem ekranu.

## 5. Częstotliwości próbkowania i rozdzielczość czasowa

**Częstotliwość próbkowania** systemu nagrywania określa najdrobniejszą różnicę czasową, jaką może rozwiązać. Twierdzenie Nyquista stwierdza, że system próbkujący z częstotliwością *f* może wiernie reprezentować sygnały do *f/2*. Dla danych na poziomie zdarzeń wynika z tego:

- **EEG przy 1 000 Hz**: jedna próbka co 1 ms. Rozdzielczość czasowa wystarczająca do odróżnienia komponentu P100 (100 ms) od N200 (200 ms) wizualnych ERP.
- **Odpytywanie klawiatury przy 125 Hz** (standardowy USB HID): jedna próbka co 8 ms. Rozdzielczość wystarczająca dla typowych porównań RT (wielkości efektów powyżej 50 ms), ale nie dla efektów poniżej 10 ms.
- **Śledzenie wzroku przy 250–1 000 Hz**: jedna próbka co 1–4 ms. Wystarczająca do wykrywania początku sakady, które wymaga precyzji ~1 ms.

Zrozumienie granicy precyzji systemu nagrywania zapobiega nadinterpretacji małych różnic numerycznych. Jeśli dwa warunki różnią się średnim RT o 12 ms, ale urządzenie do odpowiedzi ma drgania czasowe wynoszące 15 ms, różnica jest nieinterpretowalną.

## 6. Otwarte standardy danych: BIDS

**Brain Imaging Data Structure (BIDS)** to standard społecznościowy organizowania i opisywania zbiorów danych neuroobrazowania i elektrofizjologii (Gorgolewski i in., 2016, *Scientific Data*). BIDS określa:

- Układ katalogów (np. `sub-01/ses-01/eeg/sub-01_ses-01_task-flanker_eeg.bdf`)
- Wymagane i opcjonalne pliki pomocnicze JSON opisujące parametry akwizycji
- Ustandaryzowany format pliku zdarzeń (TSV z kolumnami `onset`, `duration`, `trial_type`)
- Plik `dataset_description.json` na poziomie zbioru danych i `participants.tsv` na poziomie uczestnika

Główną motywacją dla BIDS jest **samoopis**: właściwie sformatowany zbiór danych BIDS zawiera wystarczającą ilość metadanych, aby każdy badacz — nawet nieznający oryginalnego eksperymentu — mógł zrozumieć, co zostało zarejestrowane, jak zebrano dane i co zawiera każdy plik, bez kontaktowania się z oryginalnymi autorami.

**OpenNeuro** (openneuro.org) przechowuje tysiące zbiorów danych w formacie BIDS dostarczonych przez grupy badawcze z całego świata. Wszystkie zbiory danych można swobodnie pobierać. Platforma uruchamia automatyczną walidację (BIDS Validator) w celu zapewnienia zgodności przed publicznym udostępnieniem.

Kryzys replikacji w psychologii i kognitywnych naukach o mózgu był częściowo spowodowany brakiem standardów formatu danych: różne laboratoria przechowywały ten sam typ danych w niekompatybilnych formatach z różnymi nazwami kolumn, jednostkami i konwencjami, co czyniło niezależną reanalyzę praktycznie niemożliwą. BIDS jest strukturalną odpowiedzią na ten problem.

## 7. Kontekst historyczny: od tabel do terabajtów

Dane Dondersa z 1868 roku mieściły się w ręcznie napisanej tabeli. Współczesne badanie EEG z 40 uczestnikami, 64 kanałami i próbkowaniem 1 000 Hz generuje około 9 GB surowych danych. Duże badanie neuroobrazowania (ABCD Study, n = 11 800) produkuje petabajty.

Ten wzrost objętości danych stworzył potrzebę ustandaryzowanych formatów: gdy dane są małe, idiosynkratyczne formaty przechowywania są jedynie niedogodne. Gdy dane są duże i współdzielone między instytucjami, brakująca nazwa kolumny lub niejednoznaczna konwencja jednostek może zmarnować tygodnie pracy analityka, a w najgorszym przypadku prowadzić do błędnych wniosków naukowych.

PhysioNet (physionet.org) przechowuje kliniczne zbiory danych fizjologicznych — EKG, EEG, oddech — w otwartych formatach z obszerną dokumentacją, umożliwiając badaczom na całym świecie opracowywanie i walidację algorytmów analitycznych na prawdziwych danych ludzkich bez prowadzenia nowych eksperymentów.

## Literatura

- Donders, F. C. (1868). On the speed of mental processes. *Acta Psychologica*, 30, 412–431.
- Gorgolewski, K. J. i in. (2016). The brain imaging data structure, a format for organizing and describing outputs of neuroimaging experiments. *Scientific Data*, 3, 160044.
- Kemp, B. i in. (1992). A simple format for exchange of digitized polygraphic recordings. *Electroencephalography and Clinical Neurophysiology*, 82(5), 391–393.
- OpenNeuro: openneuro.org
- PhysioNet: physionet.org
- Specyfikacja BIDS: bids-specification.readthedocs.io
