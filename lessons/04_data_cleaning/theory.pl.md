# Teoria — Czyszczenie danych

## 1. Dlaczego dane nigdy nie są czyste

Surowe dane najlepiej rozumieć jako **hipotezę** o tym, co wydarzyło się podczas eksperymentu. Są produktem sprzętu o skończonej precyzji, oprogramowania z opóźnieniami harmonogramowania, uczestników, którzy mrugają, drapią się po nosie i od czasu do czasu naciskają zły klawisz, oraz eksperymentatorów, którzy — mimo najlepszych intencji — czasem błędnie rejestrują warunek lub zostawiają uruchomione nagranie podczas przerwy.

Wyczyszczone dane to Twoje **najlepsze przybliżenie** tego, co rzeczywiście się wydarzyło, skonstruowane przez zastosowanie jawnych, wstępnie określonych kryteriów w celu usunięcia lub oznaczenia obserwacji, które są nieprawdopodobne, niemożliwe lub nieinformacyjne. Kluczowe słowo to *jawne*: każda decyzja dotycząca czyszczenia musi być udokumentowana, ponieważ decyzje o czyszczeniu są decyzjami analitycznymi, a decyzje analityczne wpływają na wyniki.

Relacja między surowymi a wyczyszczonymi danymi nie jest relacją odkrywania — jak gdyby „prawdziwy" zbiór danych był ukryty w surowym pliku, czekając na wydobycie. To relacja modelowania: różne wybory dotyczące czyszczenia produkują różne zbiory danych, a tym samym różne wyniki. Dlatego wstępne określenie kryteriów czyszczenia przed zapoznaniem się z danymi jest istotnym elementem rygorystycznej nauki.

## 2. Kategorie brudnych danych

### Zduplikowane wiersze

Awaria sprzętu w trakcie sesji i ponowne uruchomienie nagrywania przez eksperymentatora może powodować zduplikowane wiersze — ten sam `trial_id` pojawiający się dwukrotnie. Duplikaty zawyżają pozorną wielkość próby i zniekształcają szacunki rozkładów RT (ponieważ zduplikowane wolne próby podwajają swój udział w obliczeniu średniej). Wykrywanie: grupuj po `trial_id` i zliczaj; każda liczność > 1 wskazuje na duplikat.

### Wartości niemożliwe

Wartości naruszające ograniczenia fizyczne lub logiczne: ujemny RT (`response_time_ms = -400`), znacznik czasu odpowiedzi przed bodźcem (`response_time_ms = 0`) lub klawisz odpowiedzi, który nie należy do zestawu prawidłowych klawiszy odpowiedzi dla danego paradygmatu. Typowo odzwierciedlają błędy oprogramowania, uszkodzenie danych lub błędne wyrównanie kolumn podczas eksportu pliku.

### Wartości poza zakresem

Wartości, które są technicznie możliwe, ale nieprawdopodobne w kontekście eksperymentalnym: RT wynoszący 50 000 ms (50 sekund) w zadaniu z oknem odpowiedzi 2 000 ms, lub RT wynoszący 15 ms w zadaniu, gdzie bodziec musi zostać rozpoznany przed jakąkolwiek odpowiedzią. Nie są to błędy w ścisłym sensie — reprezentują rzeczywiste zdarzenia — ale nie są informacyjne dla badanego procesu poznawczego.

### Błędy kodowania

Znaki lub ciągi znaków, które nie powinny pojawiać się w danej kolumnie: klawisz odpowiedzi zarejestrowany jako `"\\n"` (znak nowej linii przypadkowo zarejestrowany), etykieta warunku z końcową spacją (`"go "` zamiast `"go"`), lub znak zastępczy Unicode tam, gdzie powinien być znak litery. Błędy kodowania są szczególnie powszechne przy łączeniu danych z różnych systemów operacyjnych lub różnych języków programowania.

### Brakujące wpisy

Wiersze, w których jedna lub więcej komórek jest pustych lub zawiera wartość zastępczą (np. `NA`, `NaN`, `-1`). Brakujące klucze odpowiedzi w próbach, gdzie odpowiedź była oczekiwana, wskazują, że uczestnik nie odpowiedział — ale czy to przekroczenie limitu czasu (okno odpowiedzi wygasło) czy utrata danych, musi być określone na podstawie kontekstu.

### Niejednoznaczność strefy czasowej

Znaczniki czasu na poziomie sesji, które nie uwzględniają strefy czasowej, mogą stać się niejednoznaczne przy łączeniu danych z wielu ośrodków lub gdy sesja obejmuje zmianę czasu letniego. Rzadko jest to istotne dla kolumn RT wewnątrz prób (które są względne, nie bezwzględne), ale może zniekształcać kolejność sesji przy sortowaniu według czasu rozpoczęcia sesji.

## 3. Specyficzne kryteria wykluczenia RT

Rozkłady czasu reakcji są prawostronnie skośne i ograniczone od dołu przez nieodzowny minimalny czas na przetwarzanie sensoryczne i wykonanie ruchu. Standardowe kryteria wykluczenia odzwierciedlają te biologiczne ograniczenia:

### Antycypacje (RT < 100 ms)

Odpowiedź występująca mniej niż 100 ms po pojawieniu się bodźca nie mogła zostać wyprodukowana przez przetwarzanie tego bodźca. W 100 ms światło od bodźca ledwo zakończyło drogę przez układ wzrokowy do pierwotnej kory wzrokowej (V1), nie wspominając o przetworzeniu przez podrzędne mechanizmy decyzyjne. Odpowiedzi tak szybkie są **antycypacyjne**: uczestnik odpowiedział przed zakończeniem przetwarzania, albo zgadując czas odpowiedzi, albo reagując na niezamierzoną wskazówkę.

Włączenie odpowiedzi antycypacyjnych do średnich RT sztucznie obniżałoby średnie i zawyżało pozorną szybkość. Powinny być wykluczone i liczone osobno (jako miara przestrzegania zadania i strategii).

### Przerwy uwagi (RT > 2000–3000 ms)

Bardzo wolne odpowiedzi — typowo powyżej 2 000 lub 3 000 ms, w zależności od paradygmatu — odzwierciedlają przerwy uwagi: uczestnik był chwilowo niezaangażowany w zadanie. Odpowiedzi te są rzeczywiste, ale nie są informacyjne dla badanego procesu poznawczego (mechanizm zainteresowania działa w skali setek milisekund, nie sekund). Ich włączenie zawyża średnie RT i wariancję.

Dokładny górny punkt odcięcia różni się w zależności od paradygmatu i konwencji badacza. Ratcliff (1993) przejrzał wiele strategii przycinania; Ulrich i Miller (1994) pokazali, że różne metody przycinania produkują systematycznie różne szacunki średnich RT, czyniąc wybór punktu odcięcia decyzją metodologiczną, którą należy zgłosić.

### Próby z przekroczeniem limitu czasu

Próby, w których nie zarejestrowano odpowiedzi w oknie odpowiedzi (np. `response_time_ms` jest brakujące lub oznaczone jako timeout), to odrębna kategoria. Nie są to wolne odpowiedzi — to nieobecne odpowiedzi, które niosą inne informacje:

- Wysoki wskaźnik przekroczeń limitu czasu może wskazywać na trudność zadania, dezorientację uczestnika lub źle skalibrowane okno odpowiedzi.
- Przekroczenia limitu czasu muszą być raportowane osobno od rozkładu RT.
- W analizach dokładności przekroczenia limitu czasu są typowo kodowane jako błędne, ale powinny być odróżniane od błędów komisji (nieprawidłowych odpowiedzi, które zostały udzielone).

### Zasada trzech kategorii

Każda próba należy do dokładnie jednej z trzech kategorii: (1) prawidłowa odpowiedź — włączona do analizy RT; (2) wykluczona odpowiedź — odpowiedź została udzielona, ale wykluczona na podstawie wstępnie określonych kryteriów; (3) nieobecna odpowiedź — nie udzielono odpowiedzi (timeout). Mieszanie tych kategorii produkuje nieinterpretowalny wyniki.

## 4. Dokumentowanie decyzji dotyczących czyszczenia

**Dziennik czyszczenia** rejestruje każdą decyzję podjętą podczas czyszczenia danych:

- Jakie kryterium zostało zastosowane
- Ile prób zostało wykluczonych przez to kryterium
- Jaki procent wszystkich prób to stanowi
- W jakich warunkach wystąpiły wykluczenia (aby wykryć problemy z jakością danych specyficzne dla warunków)

Dziennik czyszczenia jest tak samo ważny naukowo jak sam plik danych. Opublikowany wynik bez dziennika czyszczenia nie może być niezależnie zweryfikowany, ponieważ czytelnik nie może wiedzieć, czy zgłoszony efekt zależy od dokonanych wyborów dotyczących czyszczenia.

### Prerejestracja

**Prerejestracja** oznacza określenie kryteriów czyszczenia — i wszystkich innych decyzji analitycznych — przed zbieraniem lub analizowaniem danych, i złożenie tej specyfikacji w datowanym publicznym rejestrze (np. na Open Science Framework, osf.io). Oddziela to analizy konfirmacyjne (testowanie wstępnie określonych hipotez za pomocą wstępnie określonych metod) od analiz eksploracyjnych (próbowanie wielu podejść do czyszczenia i raportowanie tego, które daje najsilniejszy wynik).

To rozróżnienie ma znaczenie, ponieważ przy typowym zbiorze danych RT, zmienianie górnego progu RT między 1 500 ms a 3 000 ms może znacząco zmienić średnie warunków i istotność statystyczną porównań. Bez prerejestracji badacz mógłby — świadomie lub nie — wybrać próg, który daje pożądany wynik.

## 5. Reguła 5–10% jako punkt odniesienia

Jeśli więcej niż 5–10% prób w warunku jest wykluczonych, wynik tego warunku jest niepewny. Ta wytyczna nie pochodzi z formalnego twierdzenia, lecz ze skumulowanego doświadczenia empirycznego: przy wskaźnikach wykluczenia powyżej 10%, wykluczone próby prawdopodobnie nie są losową próbką wszystkich prób, co oznacza, że pozostałe włączone próby stanowią systematycznie obciążony podzbiór zamierzonego pomiaru.

Wskaźniki wykluczenia powinny być zawsze raportowane razem z głównymi wynikami, na warunek. Czysty zbiór danych z 2% wskaźnikiem wykluczenia wzbudza większe zaufanie niż identyczna średnia RT uzyskana ze zbioru danych z 15% wykluczeniem.

Jeśli wskaźniki wykluczenia różnią się istotnie między warunkami (np. 2% w warunku zgodnym vs. 12% w warunku niezgodnym), ta różnica sama w sobie jest odkryciem: warunek niezgodny wywołał jakościowo inne zaangażowanie behawioralne. Pominięcie tej informacji przez proste raportowanie wyczyszczonych średnich ukryłoby ważny wynik.

## 6. Odtwarzalne czyszczenie

Potok czyszczenia jest odtwarzalny wtedy i tylko wtedy, gdy można go **uruchomić ponownie z surowych danych** i zawsze produkuje ten sam wyczyszczony wynik. Wymaga to:

1. **Skryptu** (Python, R lub inny), który wczytuje surowy CSV, stosuje wszystkie kroki czyszczenia programowo i zapisuje wyczyszczony CSV.
2. **Braku ręcznej edycji** surowego CSV. Jakakolwiek ręczna zmiana (usunięcie wiersza w Excelu, ręczna korekta literówki) jest niewidoczna dla jakiegokolwiek systemu kontroli wersji i nie może być odtworzona przez innego badacza.
3. **Skryptów pod kontrolą wersji**. Skrypt czyszczenia powinien być zacommitowany do tego samego repozytorium co dane, tak aby każda zmiana logiki czyszczenia była śledzona z taką samą rygorytyką jak same dane.

Biblioteka `pandas` w Pythonie zapewnia standardowy zestaw narzędzi do programowego czyszczenia danych RT. Minimalny potok czyszczenia może wyglądać następująco:

```python
import pandas as pd

raw = pd.read_csv("data/generated/session_001.csv")

# Wykluczenie 1: antycypacje
mask_anticipation = raw["response_time_ms"] < 100

# Wykluczenie 2: przerwy uwagi
mask_lapse = raw["response_time_ms"] > 2000

# Wykluczenie 3: timeout (brakujące RT)
mask_timeout = raw["response_time_ms"].isna()

excluded = raw[mask_anticipation | mask_lapse | mask_timeout].copy()
cleaned  = raw[~(mask_anticipation | mask_lapse | mask_timeout)].copy()

print(f"Łącznie prób: {len(raw)}")
print(f"Wykluczono: {len(excluded)} ({100*len(excluded)/len(raw):.1f}%)")
print(f"Włączono: {len(cleaned)}")

cleaned.to_csv("data/cleaned/session_001_clean.csv", index=False)
```

Ten skrypt jest dziennikiem czyszczenia: każde kryterium wykluczenia jest jawne, każda liczba jest odtwarzalna, a ponowne uruchomienie z tych samych surowych danych zawsze produkuje ten sam wyczyszczony wynik.

## 7. Kontekst historyczny: Konsekwencje niewyczyszczonych danych

### Ratcliff (1993)

Artykuł Rogera Ratcliffa z 1993 roku „Methods for dealing with reaction time outliers" jest podstawowym odniesieniem dla metodologii przycinania RT. Ratcliff pokazał, że różne strategie wykluczania wartości odstających produkują systematycznie różne szacunki podstawowej średniej RT, i że niektóre powszechne praktyki (np. usuwanie prób oddalonych o więcej niż dwa odchylenia standardowe od średniej, obliczone na pełnym rozkładzie) wprowadzają obciążenie, ponieważ sama średnia i SD są zniekształcone przez wartości odstające. Jego zalecenie: używać stałych bezwzględnych progów (np. dolna granica 100 ms, górna granica 3 000 ms), a nie progów względem rozkładu obliczonych na zainfekowanych rozkładach.

### Ulrich i Miller (1994)

Rolf Ulrich i Jeff Miller rozszerzyli analizę Ratcliffa, pokazując, że przycinanie wartości odstających wpływa nie tylko na średnie RT, ale także na pozorny rozmiar efektów eksperymentalnych. Efekt Stroopa mierzony na przyciętych danych (niezgodny minus zgodny) może być istotnie różny od efektu mierzonego na nieprzyciętych danych, nawet gdy obie analizy są wewnętrznie spójne. Potwierdza to, że wybór strategii przycinania jest zmienną metodologiczną, którą należy wstępnie określić i zgłosić.

### Kryzys replikacji

Znaczna część niepowodzeń replikacji udokumentowanych w projekcie Open Science Collaboration z 2015 roku (który nie był w stanie zreplikować 61% wyników z psychologii poznawczej i społecznej) dotyczyła elastycznej analizy danych — praktyki podejmowania decyzji analitycznych po zobaczeniu danych. Elastyczne kryteria czyszczenia to jedna forma elastycznej analizy. BIDS, prerejestracja na OSF i odtwarzalne skrypty czyszczenia są strukturalnymi odpowiedziami na ten problem, czyniąc „ogród rozwidlających się ścieżek" widocznym i audytowalnym.

## Literatura

- Ratcliff, R. (1993). Methods for dealing with reaction time outliers. *Psychological Bulletin*, 114(3), 510–532.
- Ulrich, R., & Miller, J. (1994). Effects of truncation on reaction time analysis. *Journal of Experimental Psychology: General*, 123(1), 34–80.
- Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.
- Open Science Framework: osf.io
- Gorgolewski, K. J. i in. (2016). The brain imaging data structure. *Scientific Data*, 3, 160044.
