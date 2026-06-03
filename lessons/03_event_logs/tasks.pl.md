# Zadania — Logi zdarzeń i formaty danych

Wykonaj poniższe kroki podczas lekcji. Zapisuj obserwacje w notatniku lub dokumencie współdzielonym zgodnie z instrukcją prowadzącego.

## Krok 1: Wygeneruj plik sesji

Uruchom aplikację i zagraj w dowolną grę czasu reakcji (np. Lekcja 02 — Laboratorium czasu reakcji) przez co najmniej 20 prób. Gra automatycznie zapisuje plik CSV do `data/generated/`. Potwierdź istnienie pliku, sprawdzając ten katalog w menedżerze plików lub terminalu.

## Krok 2: Otwórz plik CSV

Otwórz plik CSV w aplikacji arkuszowej (Excel, LibreOffice Calc lub Google Sheets) lub w edytorze tekstu (Notepad, TextEdit, VS Code).

Najpierw obejrzyj surowy plik w edytorze tekstu. Zauważ, że pierwszy wiersz to **nagłówek** (nazwy kolumn), a każdy kolejny wiersz to jedna próba.

## Krok 3: Zidentyfikuj każdą kolumnę

Dla każdej z ośmiu standardowych kolumn wymienionych poniżej napisz jedno zdanie w notatniku opisujące, co zawiera i po co jest:

| Kolumna | Opis |
|---|---|
| `participant_id` | |
| `session_id` | |
| `trial_id` | |
| `condition` | |
| `stimulus_onset_ms` | |
| `response_time_ms` | |
| `response_key` | |
| `correct` | |

## Krok 4: Zlokalizuj czas reakcji

Która kolumna zawiera czas reakcji w milisekundach? Wpisz jej nazwę i zanotuj wartość minimalną i maksymalną zaobserwowaną we wszystkich wierszach.

- Minimalne RT: _______ ms
- Maksymalne RT: _______ ms

## Krok 5: Zweryfikuj tożsamość uczestnika

Sprawdź, czy `participant_id` jest identyczne w każdym wierszu pliku. Jeśli znajdziesz wiersz z inną wartością, zanotuj go.

Następnie oblicz liczbę unikalnych wartości w `session_id`. Dla pojedynczej sesji powinna wynosić 1. Jeśli zagrałeś dwie oddzielne sesje przed otwarciem pliku, może wynosić 2.

## Krok 6: Arytmetyka na znacznikach czasu

Przyjrzyj się kolumnie `stimulus_onset_ms`. Odejmij wartość z wiersza 1 od wartości z wiersza 2. To jest **interwał między próbami** (ITI) dla pierwszych dwóch prób.

- ITI między próbą 1 a próbą 2: _______ ms

Odejmij pierwszy `stimulus_onset_ms` od ostatniego. To przybliżony czas trwania sesji w milisekundach. Przelicz go na sekundy.

- Przybliżony czas trwania sesji: _______ sekund

## Pytania dyskusyjne

Omów poniższe pytania w grupie lub dostarcz pisemne odpowiedzi zgodnie z instrukcją:

1. **Dlaczego plik CSV nie zawiera wieku ani płci uczestnika?** Gdzie powinny być przechowywane te informacje i jak byłyby połączone z tym plikiem?
2. **Gdyby ten eksperyment był prowadzony jednocześnie z EEG**, której kolumny użyłbyś do wyrównania logu behawioralnego z zapisem EEG? Jakich dodatkowych danych potrzebowałbyś z systemu EEG?
3. **Wyobraź sobie, że dwa laboratoria prowadzą ten sam eksperyment i przechowują wyniki w plikach CSV z różnymi nazwami kolumn.** Jakie praktyczne problemy pojawią się, gdy trzeci badacz będzie chciał połączyć oba zbiory danych? Jak BIDS rozwiązuje ten problem?
