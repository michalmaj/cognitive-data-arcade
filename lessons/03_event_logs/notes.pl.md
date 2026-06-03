# Notatki dla prowadzącego — Logi zdarzeń i formaty danych

## Przewodnik czasowy

| Aktywność | Czas | Uwagi |
|---|---|---|
| Czytanie teorii (własnym tempem) | 25–30 min | Zadać przed zajęciami; studenci nieznający CSV powinni poświęcić więcej czasu na sekcję 3 |
| Zadania — inspekcja CSV | 15–20 min | Studenci otwierają rzeczywiste pliki wyjściowe gry; zob. Zadania po instrukcję krok po kroku |
| Zapisywanie obserwacji | 5 min | |
| Dyskusja | 20–25 min | Zob. wskazówki do pytań poniżej |
| **Razem** | **~65–80 min** | Brak gry w tej lekcji; dostosuj tempo odpowiednio |

## Oczekiwane obserwacje podczas zadań

Studenci otworzą plik CSV z `data/generated/`. Plik powinien mieć osiem standardowych kolumn. Większość studentów od razu rozpozna `response_time_ms` jako RT, ale niektórzy pomylą ją z `stimulus_onset_ms`. Skorzystaj z tego zamieszania konstruktywnie: zapytaj, co oznacza różnica między tymi dwiema kolumnami w sensie konceptualnym.

Studenci wykonujący zadanie arytmetyczne na znacznikach czasu (Krok 5 w Zadaniach) powinni stwierdzić, że kolejne wartości `stimulus_onset_ms` różnią się o długość przerwy między próbami. Na przestrzeni całej sesji mogą obliczyć przybliżony czas trwania sesji. Ukonkretnia to abstrakcyjny pomysł „rejestrowania z precyzją milisekundową".

## Wskazówki do pytań dyskusyjnych

**Pytanie 1 — Dlaczego CSV nie przechowuje wieku uczestnika?**
Oczekiwane odpowiedzi: wiek to metadane na poziomie sesji, a nie dane na poziomie prób. Należy je przechowywać w osobnym pliku uczestników i łączyć przez `participant_id`. Kluczowa koncepcja: jednostka analizy wyznacza jednostkę przechowywania. To łagodne wprowadzenie do struktury danych relacyjnych bez używania tego terminu.

**Pytanie 2 — Co się dzieje z pomiarem RT, jeśli dwa komputery mają nieznacznie różne zegary?**
Oczekiwane odpowiedzi: sama kolumna RT nie jest dotknięta problemem, jeśli RT jest obliczany na jednym komputerze (jako czas upływający od pojawienia się bodźca do odpowiedzi na tej samej maszynie). Problem pojawia się jedynie przy wyrównywaniu danych z dwóch różnych systemów nagrywania (np. log behawioralny i EEG). Wyróżnij różnicę między RT wewnątrz urządzenia (wewnętrznie spójnym) a wyrównaniem między urządzeniami (wymagającym synchronizacji).

**Pytanie 3 — Dlaczego BIDS ma znaczenie, jeśli nigdy nie udostępniasz swoich danych?**
Odpowiedzi wahają się od „nie ma" do „zmusza cię do dokumentowania danych w sposób, który przyszłe ja zrozumie". Nakieruj studentów na drugą odpowiedź. Najsilniejszy argument: standaryzacja przynosi korzyść samemu badaczowi — zbiór danych, który nie może być ponownie analizowany po dwóch latach, ma ograniczoną wartość.

## Częste błędy i nieporozumienia

- **„CSV to najlepszy format, bo otwiera się w Excelu."** Prawda, że czytelność jest cenna. Ale pytaj: co się dzieje z 5 GB CSV w Excelu? A z zagnieżdżonymi danymi (metadane uczestnika + dane prób)? Czytelność jest jednym wymiarem jakości formatu, nie jedynym.
- **„Czas reakcji jest już w CSV, więc precyzja czasowa nie ma znaczenia."** RT w CSV to różnica obliczona przez oprogramowanie między dwoma znacznikami czasu na tej samej maszynie. Problem polega na tym, że sam znacznik czasu może być opóźniony przez harmonogramowanie systemu operacyjnego. Interwał odpytywania 10 ms oznacza, że zarejestrowany RT może być o maksymalnie 10 ms wyższy niż prawdziwy RT.
- **„EDF to stary format i pewnie przestarzały."** EDF pochodzi z 1992 roku i nadal jest dominującym formatem wymiany EEG w placówkach klinicznych na całym świecie. Wiek nie oznacza przestarzałości w formatach danych; adopcja i ekosystem mają większe znaczenie niż nowość.
- **„Otwarte dane oznaczają, że każdy może ich używać do czegokolwiek."** Zbiory danych z OpenNeuro można swobodnie pobierać, ale są objęte licencjami. Co ważniejsze, reidentyfikacja uczestników na podstawie danych neuroobrazowania jest realnym ryzykiem; otwarte udostępnianie wiąże się z odpowiedzialnością etyczną.

## Połączenie z następnymi lekcjami

Lekcja 04 (Czyszczenie danych) następuje bezpośrednio po tej. Pliki CSV, które studenci przeglądają w zadaniach tej lekcji, to te same pliki, które będą czyścić w Lekcji 04. Zachęć studentów do zachowania notatek z zadania inspekcji CSV — przydadzą się przy obliczaniu wskaźników wykluczenia.

Kolumna `stimulus_onset_ms`, która często wprawia studentów w zakłopotanie podczas tej lekcji, staje się kluczowym kontekstem do dyskusji w Lekcji 04 o tym, dlaczego próby przekraczające limit czasu (brak odpowiedzi w oknie czasowym) są fundamentalnie różne od wolnych odpowiedzi.
