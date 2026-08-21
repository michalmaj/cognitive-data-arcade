# Przewodnik dla studentów — Cognitive Data Arcade

Ten przewodnik przeprowadza Cię przez pełny cykl nauki w projekcie:

**zagraj w grę → dane się pojawiają → przeanalizuj je → zinterpretuj wynik → zastanów się, co to oznacza**

Nie musisz znać Pythona przed startem. Musisz być ciekawy.

---

## Czym jest ten projekt?

Cognitive Data Arcade to zbiór interaktywnych eksperymentów zbudowanych w Pythonie. Każdy eksperyment prosi Cię o wykonanie jakiejś czynności — zareagowanie, podjęcie decyzji, klasyfikowanie, budowanie — i zapisuje to, co zrobiłeś. Następnie otwierasz te dane w Pythonie i analizujesz je tak, jak zrobiłby to badacz.

Celem nie jest granie w gry. Celem jest doświadczenie pełnego potoku data science na danych, które pochodzą od Ciebie.

---

## Instalacja

```bash
git clone https://github.com/michalmaj/cognitive-data-arcade.git
cd cognitive-data-arcade
uv sync
```

Uruchom arkadę:

```bash
uv run cognitive-data-arcade
```

Otworzy się okno z listą 31 gier. Nawiguj strzałkami. Naciśnij **Enter**, aby uruchomić.

---

## Pierwsze laboratorium: czas reakcji

Zacznij od **Reaction Time Lab** (lekcja 2 w menu). To najkrótsza ścieżka do pełnego cyklu.

### Co będziesz robić

Gra wyświetla okrąg na ekranie po losowym opóźnieniu. Naciśnij **Spację** tak szybko, jak możesz. Po 20 próbach sesja kończy się i pokazuje podsumowanie.

Uruchom ją co najmniej dwa razy — raz normalnie, raz celowo rozpraszając uwagę (odwróć wzrok, postukaj nogą, licz wstecz). Zobaczysz różnicę w danych.

### Gdzie są Twoje dane?

Po każdej sesji plik CSV pojawia się w folderze z danymi użytkownika:

- **Windows:** `C:\Users\<nazwa_użytkownika>\.cognitive_data_arcade\data\generated\reaction_time\`
- **macOS / Linux:** `~/.cognitive_data_arcade/data/generated/reaction_time/`

Nazwa pliku to znacznik czasu, np. `20260527_161352.csv`. Otwórz go w dowolnym edytorze tekstu, aby zobaczyć surowe wiersze.

Każdy wiersz to jedna próba:

```
participant_id, session_id, trial_id, task_name, condition,
stimulus, expected_response, actual_response, correct,
reaction_time_ms, timestamp, distractor_count
```

Kolumny, które mają największe znaczenie w pierwszej analizie: `correct`, `reaction_time_ms`, `condition`.

### Pierwsza analiza

Otwórz sesję Pythona (lub notatnik) w katalogu projektu:

```bash
uv run python
```

```python
import pandas as pd
from pathlib import Path

# Ścieżka do danych (taka sama na wszystkich platformach)
data_dir = Path.home() / ".cognitive_data_arcade" / "data" / "generated" / "reaction_time"

# Wczytaj najnowszą sesję
files = sorted(data_dir.glob("*.csv"))
df = pd.read_csv(files[-1])

# Ile prób?
print(len(df))

# Ile poprawnych?
print(df["correct"].value_counts())

# Średni czas reakcji w poprawnych próbach
correct = df[df["correct"]]
print(correct["reaction_time_ms"].describe().round(1))
```

### Na co zwrócić uwagę

Typowy wynik dla skupionego dorosłego: mediana **200–350 ms**, mała odchyłka standardowa.

Jeśli Twoja mediana przekracza 450 ms, coś Cię spowalniało — rozproszenie, niepewność lub zmęczenie.

Jeśli Twoje odchylenie standardowe jest bardzo wysokie (> 150 ms), Twoje odpowiedzi były niespójne — co samo w sobie jest odkryciem.

### Proste porównanie

Jeśli uruchamiałeś dwie sesje (skupiony vs. rozproszony):

```python
data_dir = Path.home() / ".cognitive_data_arcade" / "data" / "generated" / "reaction_time"
files = sorted(data_dir.glob("*.csv"))

session_a = pd.read_csv(files[-2])   # wcześniejsza sesja
session_b = pd.read_csv(files[-1])   # późniejsza sesja

for label, s in [("Sesja A", session_a), ("Sesja B", session_b)]:
    correct = s[s["correct"]]
    print(f"{label}: mediana RT = {correct['reaction_time_ms'].median():.0f} ms, "
          f"trafność = {s['correct'].mean():.1%}")
```

### Zinterpretuj wynik

Nie podawaj tylko liczb. Zapytaj:

- Czy różnica między sesjami jest realna, czy mieści się w normalnej zmienności?
- Ile prób przeprowadziłeś? Czy 20 wystarczy, aby wyciągać wnioski?
- Co jeszcze oprócz rozproszenia mogło wyjaśnić tę różnicę?
- Jeśli teraz przeprowadziłbyś tę samą sesję, czy uzyskałbyś ten sam wynik?

Te pytania są esencją data science.

---

## Jakie dane generują gry?

Sześć gier zapisuje pliki CSV do `~/.cognitive_data_arcade/data/generated/` (Windows: `%USERPROFILE%\.cognitive_data_arcade\data\generated\`). Poniżej dokładne kolumny dla każdej z nich.

### Reaction Time Lab → `data/generated/reaction_time/`

| Kolumna | Typ | Opis |
|---------|-----|------|
| `participant_id` | string | UUID urządzenia — taki sam we wszystkich sesjach |
| `session_id` | string | Znacznik czasu, unikalny dla każdej sesji |
| `trial_id` | int | Numer próby w sesji (od 1) |
| `task_name` | string | Zawsze `reaction_time` |
| `condition` | string | `focused` lub `distracted` |
| `stimulus` | string | Pokazany kształt (`circle`) |
| `expected_response` | string | Klawisz, który powinien być naciśnięty |
| `actual_response` | string | Naciśnięty klawisz (pusty przy przekroczeniu czasu) |
| `correct` | bool | `True`, jeśli odpowiedź nastąpiła w czasie |
| `reaction_time_ms` | float | Czas od bodźca do naciśnięcia klawisza w ms |
| `timestamp` | string | Czas próby w formacie ISO 8601 |
| `distractor_count` | int | Liczba dystraktorów w trybie rozproszenia |

Kluczowe kolumny: `correct`, `reaction_time_ms`, `condition`.

---

### Stroop Challenge → `data/generated/stroop/`

| Kolumna | Typ | Opis |
|---------|-----|------|
| `participant_id` | string | UUID urządzenia |
| `session_id` | string | Znacznik czasu sesji |
| `trial_id` | int | Numer próby |
| `task_name` | string | Zawsze `stroop` |
| `condition` | string | `congruent` (kolor i słowo zgodne) lub `incongruent` (niezgodne) |
| `stimulus` | string | Pokazane słowo (np. `RED`) |
| `ink_color` | string | Rzeczywisty kolor atramentu (np. `blue`) |
| `word_color` | string | Kolor nazwany przez słowo |
| `expected_response` | string | Prawidłowa nazwa koloru atramentu |
| `actual_response` | string | Naciśnięty klawisz |
| `correct` | bool | Czy odpowiedź była prawidłowa |
| `reaction_time_ms` | float | Czas reakcji w ms |
| `timestamp` | string | Czas próby w formacie ISO 8601 |

Kluczowe pytanie: czy `reaction_time_ms` jest wyższy w warunkach `incongruent`? To właśnie jest efekt Stroopa.

---

### Flanker Arena → `data/generated/flanker/`

| Kolumna | Typ | Opis |
|---------|-----|------|
| `participant_id` | string | UUID urządzenia |
| `session_id` | string | Znacznik czasu sesji |
| `trial_id` | int | Numer próby |
| `task_name` | string | Zawsze `flanker` |
| `condition` | string | `congruent` lub `incongruent` |
| `target_direction` | string | `left` lub `right` — prawidłowa odpowiedź |
| `correct` | bool | Czy odpowiedź zgodna z kierunkiem celu |
| `reaction_time_ms` | float | Czas reakcji w ms |
| `timestamp` | string | Czas próby w formacie ISO 8601 |

Kluczowe pytanie: porównaj średni RT i trafność między warunkami `congruent` i `incongruent`.

---

### Go/No-Go Guard → `data/generated/gono/`

| Kolumna | Typ | Opis |
|---------|-----|------|
| `participant_id` | string | UUID urządzenia |
| `session_id` | string | Znacznik czasu sesji |
| `trial_id` | int | Numer próby |
| `task_name` | string | Zawsze `go_no_go` |
| `trial_type` | string | `go` (zareaguj) lub `nogo` (powstrzymaj się) |
| `response` | string | `hit`, `miss`, `false_alarm` lub `correct_rejection` |
| `correct` | bool | Czy odpowiedź była właściwa |
| `reaction_time_ms` | float | RT w ms; `0.0`, gdy nie udzielono odpowiedzi |
| `timestamp` | string | Czas próby w formacie ISO 8601 |

Kluczowe pytanie: jaki jest Twój wskaźnik fałszywych alarmów (naciśnięcie na próbach `nogo`)? To mierzy kontrolę impulsów.

---

### N-Back Memory Grid → `data/generated/nback/`

| Kolumna | Typ | Opis |
|---------|-----|------|
| `task_name` | string | Zawsze `n_back` |
| `participant_id` | string | UUID urządzenia |
| `session_id` | string | Znacznik czasu sesji |
| `trial_id` | int | Numer próby |
| `block_id` | int | Numer bloku |
| `n_level` | int | Grany poziom n-back (1, 2 lub 3) |
| `position` | int | Pokazana pozycja w siatce (0–8) |
| `letter` | string | Pokazana litera |
| `pos_match` | bool | Czy pozycja pasuje do N kroków wstecz |
| `let_match` | bool | Czy litera pasuje do N kroków wstecz |
| `key_a_pressed` | bool | Czy naciśnięto klawisz dopasowania pozycji |
| `key_l_pressed` | bool | Czy naciśnięto klawisz dopasowania litery |
| `pos_correct` | bool | Prawidłowa odpowiedź dla dopasowania pozycji |
| `let_correct` | bool | Prawidłowa odpowiedź dla dopasowania litery |
| `rt_a_ms` | float | Czas reakcji dla klawisza A (ms) |
| `rt_l_ms` | float | Czas reakcji dla klawisza L (ms) |

Kluczowe pytanie: jak zmienia się trafność (`pos_correct`, `let_correct`) wraz ze wzrostem `n_level`?

---

### Visual Search Lab → `data/generated/visual_search/`

| Kolumna | Typ | Opis |
|---------|-----|------|
| `participant_id` | string | UUID urządzenia |
| `session_id` | string | Znacznik czasu sesji |
| `trial_id` | int | Numer próby |
| `mode` | string | Typ wyszukiwania (`feature` lub `conjunction`) |
| `condition` | string | Warunek próby |
| `set_size` | int | Liczba elementów na ekranie |
| `target_present` | bool | Czy cel był obecny |
| `response` | string | `present`, `absent` lub `timeout` |
| `correct` | bool | Czy odpowiedź pasowała do obecności celu |
| `rt_ms` | float | Czas reakcji w ms (`NaN` przy przekroczeniu czasu) |
| `timestamp` | string | Czas próby w formacie ISO 8601 |

Kluczowe pytanie: czy `rt_ms` rośnie z `set_size` w wyszukiwaniu koniunkcji, ale nie w wyszukiwaniu cech? To jest nachylenie funkcji wyszukiwania.

---

## Przewodnik po modułach

Arkada jest zorganizowana w 6 modułów. Możesz grać w dowolnej kolejności, ale moduły nawiązują do siebie koncepcyjnie.

### Moduł 1 — Podstawy danych i kognitywistyki (lekcje 1–6)

**Cel:** Zrozum, jak wyglądają dane data science, zanim uruchomisz jakiekolwiek statystyki.

- **L01 Big Data Map** — przegląd tego, jak 31 lekcji łączy się ze sobą. Zacznij tutaj, jeśli chcesz zrozumieć szerszą perspektywę.
- **L02 Reaction Time Lab** — Twój pierwszy plik CSV. Patrz „Pierwsze laboratorium" powyżej.
- **L03 Event Log Detective** — zagadka: odczytaj i zinterpretuj pomieszany log eksperymentu. Brak CSV; cała analiza odbywa się w grze.
- **L04 Data Quality Lab** — wykrywaj brakujące wartości, wartości odstające, błędy kodowania w surowym zbiorze danych.
- **L06 EDA Sandbox** — zaprojektuj i przeprowadź mini-eksperyment; eksploruj dane na żywo przed modelowaniem.

**Po tym module:** Powinieneś umieć wczytać CSV z pandas, obliczać podstawowe statystyki i wyjaśniać, co oznacza każda kolumna.

---

### Moduł 2 — Kognitywistyka (lekcje 7–12)

**Cel:** Przeprowadź klasyczne eksperymenty psychologii poznawczej na sobie i odczytaj produkowane liczby.

- **L07 Stroop Challenge** — interferencja poznawcza; zapisuje CSV `stroop/`.
- **L08 Flanker Arena** — selektywna uwaga; zapisuje CSV `flanker/`.
- **L09 Go/No-Go Guard** — kontrola hamowania; zapisuje CSV `gono/`.
- **L10 N-Back Memory Grid** — obciążenie pamięci roboczej; zapisuje CSV `nback/`.
- **L11 Visual Search Lab** — wyszukiwanie cech vs. koniunkcji; zapisuje CSV `visual_search/`.
- **L12 Cognitive Dashboard** — odczytuje wszystkie pięć plików CSV powyżej i pokazuje Twój profil między zadaniami. **Najpierw zagraj w pięć gier, potem otwórz ten panel.** Jeśli otworzysz Dashboard przed zagraniem w jakąkolwiek grę, wyświetli przykładowe (syntetyczne) dane zamiast Twoich prawdziwych wyników.

**Po tym module:** Będziesz mieć pięć zbiorów CSV z własnych sesji poznawczych. Cognitive Dashboard odczytuje je automatycznie z `~/.cognitive_data_arcade/data/generated/`.

---

### Moduł 3 — Statystyki (lekcje 13–16)

**Cel:** Połącz rozkłady i liczby z modułów 1–2 z formalnymi narzędziami statystycznymi.

- **L13 Distribution Playground** — zmień parametry rozkładów Normalnego, Poissona i t; obserwuj zmianę kształtu.
- **L14 Correlation Trap** — Pearson r, błędy przyczynowości, kwartet Anscombe'a.
- **L15 Hypothesis Arena** — wartości p, rozmiar efektu, moc statystyczna — interaktywna gra zręcznościowa.
- **L16 Prediction Slider** — regresja liniowa; odległość Cooka; obserwuj, jak jedna wartość odstająca przesuwa linię.

**Po tym module:** Powinieneś umieć opisać rozkład, przeprowadzić korelację i interpretować wartość p bez traktowania jej jak werdyktu.

---

### Moduł 4 — Uczenie maszynowe (lekcje 17–20)

**Cel:** Zbuduj intuicję dotyczącą tego, co modele ML faktycznie robią, zanim napiszesz jakikolwiek kod `sklearn`.

- **L17 Feature Hunter** — przeciągaj cechy na model; obserwuj zmiany trafności.
- **L18 Classifier Battle** — perceptron, SVM, drzewo decyzyjne na tych samych danych; porównuj granice decyzji.
- **L19 Overfitting Monster** — piaskownica bilansu odchylenie-wariancja; obserwuj przeuczanie modelu w czasie rzeczywistym.
- **L20 Anomaly Alert** — Isolation Forest i odległość Mahalanobisa na danych syntetycznych.

**Po tym module:** Powinieneś umieć wyjaśnić przeuczanie, dlaczego wysoka trafność treningowa może być zła i czym jest granica decyzji.

---

### Moduł 5 — Przetwarzanie języka naturalnego (lekcje 21–26)

**Cel:** Zrozum, jak tekst staje się liczbami i co te liczby znaczą dla sensu.

- **L21 Text Tokenizer Lab** — prawo Zipfa, tokenizacja BPE, statystyki słownika.
- **L22 Word Weight Factory** — potok Bag-of-Words i TF-IDF, interaktywny.
- **L23 Emotion Classifier** — analiza sentymentu VADER; przetestuj ją na własnych zdaniach.
- **L24 Semantic Space Explorer** — embeddingi słów, podobieństwo kosinusowe, arytmetyka analogii.
- **L25 Topic Detective** — modelowanie tematyczne LDA; jakie tematy wyłaniają się z korpusu?
- **L26 Human vs. Model Challenge** — negacja, sarkazm, schematy Winograda: gdzie modele zawodzą.

**Po tym module:** Powinieneś umieć opisać założenie bag-of-words i wyjaśnić, dlaczego embeddingi słów to nie to samo co definicje słów.

---

### Moduł 6 — Sieci i etyka (lekcje 27–32)

**Cel:** Zrozum, jak struktura kształtuje zachowanie — i co się dzieje, gdy algorytmy podejmują istotne decyzje.

- **L27 Social Network Simulator** — model epidemiczny SIR na losowych vs. bezskalowych grafach.
- **L28 Misinformation Spread** — asymetria między rozsiewaczami a weryfikatorami faktów.
- **L29 Recommendation Bubble** — mechanika bańki filtrów; ocenianie różnorodności.
- **L30 Bias Blind Spot** — cechy zastępcze, twierdzenie o niemożliwości sprawiedliwości.
- **L31 You Were the Dataset** — dane behawioralne, efekt Hawthorne'a, RODO.
- **L32 The Architect's Trial** — gra decyzyjna o etyce AI; prawo Goodharta i unijne rozporządzenie o AI.

**Po tym module:** Powinieneś umieć wyjaśnić jeden konkretny sposób, w jaki algorytm może być sprawiedliwy według jednej metryki i niesprawiedliwy według innej — i dlaczego to nie jest błąd.

---

## Co oddać prowadzącemu

Każde laboratorium lub moduł ma określone efekty pracy. Oto, czego oczekuje prowadzący.

### Efekt pracy na sesję (za każdym razem, gdy grasz w grę)

Dla gier, które zapisują dane (L02, L07–L11):

1. **Plik CSV** — skopiuj go z `~/.cognitive_data_arcade/data/generated/<gra>/` i zachowaj. Nazwa pliku to znacznik czasu sesji.
2. **Krótka analiza** (5–10 linii Pythona) — minimum: wczytaj plik, oblicz średnią i medianę RT lub trafności na warunek, wydrukuj wynik.
3. **Jedno zdanie interpretacji** — co oznacza ta liczba? Czy jest zgodna z oczekiwaniami?

Nie musisz pisać raportu. Komórka notatnika z kodem i jedna komórka markdown z interpretacją wystarczą.

### Efekt pracy z modułu

Po ukończeniu wszystkich lekcji w module:

| Moduł | Co oddać |
|-------|----------|
| 1 — Podstawy danych | Wczytaj dowolny plik CSV. Opisz własnymi słowami, co oznacza każda kolumna. Wskaż jeden problem z jakością danych (nawet drobny). |
| 2 — Kognitywistyka | Połącz co najmniej dwa pliki CSV z zadań poznawczych. Porównaj swoje wyniki między zadaniami. Czy wyłania się jakiś wzorzec? |
| 3 — Statystyki | Weź dane RT z Modułu 2. Oblicz test t między warunkami congruent i incongruent. Podaj wartość p, rozmiar efektu i czy wynik jest interpretowalny przy danej wielkości próby. |
| 4 — Uczenie maszynowe | Użyj dowolnych danych CSV jako wejścia do klasyfikatora scikit-learn. Podaj trafność treningową vs. testową. Wyjaśnij jednym zdaniem, dlaczego się różnią. |
| 5 — NLP | Uruchom VADER na pięciu zdaniach, które sam napiszesz — dwa wyraźnie pozytywne, dwa wyraźnie negatywne, jedno niejednoznaczne. Podaj wynik compound i wyjaśnij, gdzie Cię zaskoczył. |
| 6 — Sieci i etyka | Wybierz jeden scenariusz z The Architect's Trial. Wyjaśnij trade-off, przed którym stanąłeś, co wybrałeś i co byś zmienił, gdybyś musiał podjąć tę samą decyzję w prawdziwym systemie. |

### Eksportuj swoje postępy

W dowolnym momencie naciśnij **X** na ekranie Profilu, aby wyeksportować podsumowanie JSON swoich postępów. Zawiera ukończone lekcje, punkty arkadowe, trafność w quizach i ukończenie per moduł. Możesz udostępnić ten plik prowadzącemu jako dowód ukończenia.

---

## Jak czytać teorię w grze

Każda gra ma ekran teorii. Naciśnij **T** w menu, aby otworzyć go przed grą. Wyjaśnia koncepcję poznawczą stojącą za zadaniem prostym językiem.

Czytaj przed grą, nie po. Teoria zmienia to, co zauważasz podczas gry.

---

## Uwaga o Twoich własnych danych

Dane, które generuje ten projekt, dotyczą Ciebie. Twoje czasy reakcji, trafność, decyzje. To sprawia, że analiza jest ciekawsza — i powód, by ostrożnie podchodzić do wyciąganych wniosków.

Jedna sesja z 20 próbami to nie jest badanie naukowe. To punkt startowy. Celem jest zrozumienie potoku, a nie diagnozowanie siebie.

Wszystkie dane pozostają na Twoim komputerze w `~/.cognitive_data_arcade/`. Aplikacja nigdy nie wysyła niczego przez sieć. Aby usunąć wszystkie nagrane dane, użyj opcji **Resetuj postępy** na ekranie Profilu lub ręcznie usuń folder `~/.cognitive_data_arcade/data/generated/`.
