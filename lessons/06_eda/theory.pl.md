# Teoria — Eksploracyjna analiza danych

## 1. Czym jest EDA i skąd się wzięła?

**Eksploracyjna analiza danych (EDA)** to praktyka podsumowywania i wizualizowania zbioru danych w celu zrozumienia jego struktury *przed* określeniem i przetestowaniem formalnego modelu statystycznego. Termin wprowadził amerykański matematyk i statystyk **John Tukey** w swojej książce z 1977 roku pod tym samym tytułem, która pozostaje jednym z najbardziej wpływowych tekstów metodologicznych w nauce ilościowej.

Centralna teza Tukeya była taka, że analiza statystyczna zazwyczaj zaczyna się od złego końca. Badacze zbierają dane, natychmiast obliczają statystykę testową i raportują p-wartość — nigdy nie zaglądając do surowych liczb. Ten sposób pracy ułatwia przeoczenie anomalii, błędną interpretację wzorców i wyciąganie wniosków z artefaktów zamiast z sygnału.

EDA odwraca kolejność: najpierw patrz, potem modeluj. Cele są następujące:

1. **Wykrywanie anomalii** — wartości odstające, niemożliwe wartości, efekty podłogowe i sufitowe, które sygnalizują problemy z jakością danych.
2. **Zrozumienie rozkładu** — czy jest symetryczny? Skośny? Dwumodalny? Kształt rozkładu decyduje o tym, które testy wnioskowe są odpowiednie.
3. **Identyfikacja związków** — czy dwie zmienne są skorelowane? Czy związek jest liniowy czy krzywoliniowy? Czy istnieją podgrupy zachowujące się inaczej?
4. **Generowanie hipotez** — EDA generuje kandydujące hipotezy do analizy konfirmacyjnej. Ich nie testuje.

Ostatni punkt jest krytyczny. Hipotezy sugerowane przez dane nie mogą być właściwie testowane na tych samych danych. EDA jest z założenia generatorem hipotez, nie ich weryfikatorem. Etap konfirmacyjny wymaga albo osobnego zbioru danych, albo — idealnie — pre-rejestracji hipotez przed zbieraniem danych (Simmons i in., 2011).

## 2. Statystyki opisowe dla danych RT

Pierwszym ilościowym krokiem w każdej EDA jest obliczenie **statystyk opisowych**: liczb podsumowujących kształt, położenie i rozrzut rozkładu.

### 2.1 Tendencja centralna

- **Średnia (średnia arytmetyczna):** Wrażliwa na wartości skrajne. Odpowiednia dla rozkładów symetrycznych. Dla prawostronnie skośnych danych RT średnia przewyższa medianę i przeszacowuje, gdzie leży większość odpowiedzi.
- **Mediana (50. percentyl):** Wartość dzieląca rozkład na połowę. Odporna na wartości odstające. Zalecana jako podstawowe podsumowanie danych RT.
- **Moda:** Najczęstsza wartość. Rzadko raportowana dla danych ciągłych, ale koncepcja odpowiada wierzchołkowi estymatora gęstości jądra.

### 2.2 Rozrzut

- **Odchylenie standardowe (SD):** Średnia odległość obserwacji od średniej. Wrażliwe na wartości odstające (ponieważ używa średniej). Dla danych RT SD wynosi zazwyczaj 100–250 ms w obrębie jednego warunku.
- **Rozstęp kwartylowy (IQR = Q3 − Q1):** Zakres zawierający środkowe 50 % obserwacji. Odporny na wartości odstające. Mniej wrażliwy na ciężki ogon charakteryzujący rozkłady RT.
- **Rozstęp (max − min):** Maksymalna wrażliwość na wartości skrajne. Użyteczny tylko do flagowania niemożliwych granic.

### 2.3 Kształt

- **Skośność:** Miara asymetrii. Dodatnia skośność oznacza prawy ogon (średnia > mediana). Rozkłady RT są niemal powszechnie **prawostronnie skośne** ze względu na twardą dolną granicę przy ~100 ms i otwarty prawy ogon.
  - Skośność ≈ 0: w przybliżeniu symetryczny
  - Skośność > 1: wyraźnie prawostronnie skośny (powszechne dla surowego RT)
  - Skośność < −1: wyraźnie lewostronnie skośny (rzadkie dla RT)
- **Kurtoza:** Miara ciężkości ogona względem rozkładu normalnego. Wysoka kurtoza (leptokurtyczny) oznacza ostrzejszy wierzchołek i cięższe ogony. Rozkłady RT często mają nadmierną kurtozę (kurtoza > 3 w konwencji Pearsona), co odzwierciedla skupienie większości odpowiedzi blisko mody i nietrywialny odsetek bardzo wolnych odpowiedzi.

Rozkład normalny ma skośność = 0 i kurtozę = 3 (nadmierna kurtoza = 0). Dane RT praktycznie nigdy nie spełniają tych kryteriów, co oznacza, że każdy test statystyczny zakładający normalność jest technicznie naruszony dla surowego RT. Transformacja logarytmiczna lub modelowanie ex-Gaussowskie to powszechne rozwiązania.

| Statystyka | Wrażliwa na wartości odstające? | Odpowiednia dla RT? |
|---|---|---|
| Średnia | Tak | Używaj razem z medianą |
| Mediana | Nie | Podstawowe podsumowanie |
| SD | Tak | Raportuj, ale interpretuj ostrożnie |
| IQR | Nie | Zalecane |
| Skośność | Tak | Zawsze raportuj dla RT |
| Kurtoza | Tak | Raportuj dla opisu kształtu |

## 3. Wizualizacje dla danych RT

Każda wizualizacja ujawnia inny aspekt danych. Żaden pojedynczy wykres nie jest wystarczający.

### 3.1 Histogram

Histogram grupuje obserwacje w przedziały i liczy, ile wpada do każdego. Pokazuje **pełny kształt** rozkładu: położenie, rozrzut, skośność, modalność (jeden lub dwa wierzchołki) oraz obecność wartości odstających w ogonach.

**Kiedy używać:** Jako pierwsza wizualizacja każdej nowej zmiennej. Zawsze rysuj histogram RT przed obliczeniem średniej.

**Ograniczenia:** Szerokość przedziałów ma ogromne znaczenie. Za szeroka: traci się szczegóły. Za wąska: dominuje szum próbkowania. Zasada kciuka: zacznij od reguły Sturgesa (k = 1 + log₂ n) i dostosuj wizualnie.

### 3.2 Wykres pudełkowy

Wykres pudełkowy (box-and-whisker plot) pokazuje:
- **Medianę** jako poziomą linię wewnątrz pudełka
- **IQR** jako wysokość pudełka (Q1 do Q3)
- **Wąsy** sięgające 1,5·IQR poza krawędzie pudełka
- **Punkty wartości odstających** poza wąsami

Wykresy pudełkowe są idealne do **porównywania rozkładów między warunkami** na tej samej osi. Jedno spojrzenie ujawnia różnice w medianie, rozrzucie i częstotliwości wartości odstających.

**Ograniczenia:** Wykresy pudełkowe ściskają wszystkie informacje o kształcie rozkładu do pięciu liczb. Dwa rozkłady mogą mieć identyczne wykresy pudełkowe, ale wyglądać zupełnie inaczej jako histogramy (np. bimodalny vs. jednostajny).

### 3.3 Wykres skrzypcowy

Wykres skrzypcowy (violin plot) łączy statystyki podsumowujące wykresu pudełkowego z **estymatorem gęstości jądra** (KDE) pełnego rozkładu, odbitym symetrycznie. Im szerszy skrzypce w danym punkcie, tym więcej obserwacji leży blisko tej wartości.

**Kiedy używać:** Gdy kształt rozkładu ma znaczenie — na przykład, aby wykryć, czy rozkład RT jest jednomodalny, czy istnieje drugi tryb przy wysokich RT (możliwie odzwierciedlający podrozkład lapsów). Wykresy skrzypcowe czynią efekt Stroopa widocznym nie tylko jako przesunięcie mediany, ale jako przesunięcie całego rozkładu.

### 3.4 Wykres Q-Q (kwantyl-kwantyl)

Wykres Q-Q porównuje kwantyle obserwowanego rozkładu z kwantylami rozkładu teoretycznego (zazwyczaj normalnego). Jeśli dane mają rozkład normalny, punkty leżą na prostej diagonalnej. Odchylenia od linii ujawniają:
- **Zakrzywiony w górę:** skośność prawa (typowa dla RT)
- **Zakrzywiony w dół:** skośność lewa
- **W kształcie litery S:** ciężkie ogony (nadmierna kurtoza)

**Dlaczego ma znaczenie dla RT:** Każdy test parametryczny zakładający normalność (np. sparowany t-test) jest technicznie nieważny dla surowych danych RT. Wykres Q-Q czyni to naruszenie widocznym. Badacze powinni albo zastosować transformację (log-RT), test nieparametryczny, lub model specyficzny dla rozkładu (ex-Gaussian).

### 3.5 Wykres rozrzutu

Wykres rozrzutu wyświetla dwie zmienne jako punkty w przestrzeni 2D, ujawniając związek między nimi. Przed obliczeniem jakiegokolwiek współczynnika korelacji **zawsze rysuj wykres rozrzutu** — to jest podstawowa lekcja Kwartetu Anscombe'a (patrz sekcja 4).

**Dla danych RT:** Wykresy rozrzutu służą do badania efektów ćwiczenia (RT a numer próby), zamienności szybkości i dokładności (RT a dokładność na blok) oraz różnic indywidualnych (średnie RT uczestnika a jakaś kowarjata).

## 4. Kwartet Anscombe'a: dlaczego wizualizacja nie jest opcjonalna

W 1973 roku statystyk Francis Anscombe opublikował artykuł demonstrujący cztery zbiory danych, które są statystycznie identyczne pod każdą standardową miarą podsumowującą, a jednak wyglądają zupełnie inaczej po narysowaniu:

| Zbiór | Średnia X | Średnia Y | SD X | SD Y | Pearson r |
|---|---|---|---|---|---|
| I | 9,00 | 7,50 | 3,32 | 2,03 | 0,816 |
| II | 9,00 | 7,50 | 3,32 | 2,03 | 0,816 |
| III | 9,00 | 7,50 | 3,32 | 2,03 | 0,816 |
| IV | 9,00 | 7,50 | 3,32 | 2,03 | 0,817 |

Zbiór I jest w przybliżeniu liniowy z łagodnym szumem. Zbiór II podąża za doskonałą krzywą — model liniowy jest błędny. Zbiór III to doskonała linia z jedną wartością odstającą zawyżającą korelację. Zbiór IV składa się z pionowego stosu identycznych wartości X i jednej skrajnej wartości odstającej, która napędza całą korelację.

**Lekcja jest jednoznaczna:** Współczynnik korelacji r = 0,82 nie mówi, czy związek jest liniowy, czy istnieją wartości odstające, ani czy model jest odpowiedni. Wykres rozrzutu mówi to wszystko w ciągu sekund. Raportowanie korelacji bez wykresu rozrzutu jest niekompletne i potencjalnie wprowadzające w błąd.

Ta zasada rozciąga się na każdą statystykę podsumowującą. Statystyki opisowe opisują tylko to, co mierzysz; ukrywają wszystko inne.

## 5. Przepływ pracy EDA dla danych z kognitywistyki

Poniższa sekwencja powinna być stosowana do każdego nowego zbioru danych przed wykonaniem testów wnioskowych:

1. **Wczytaj i sprawdź:** `df.shape`, `df.dtypes`, `df.head()`, `df.tail()`. Potwierdź, że liczba wierszy odpowiada oczekiwaniom, typy kolumn są poprawne, a w pierwszych/ostatnich wierszach nie pojawiają się nieoczekiwane wartości.

2. **Sprawdź brakujące wartości:** `df.isna().sum()`. Skonfrontuj z kryteriami z Lekcji 05 (RT < 100 ms, RT > 3 000 ms, próby z timeoutem).

3. **Oblicz `describe()`:** `df.describe()` zwraca liczbę, średnią, SD, min, Q1, medianę, Q3, max dla wszystkich kolumn numerycznych. Czytaj to uważnie: samo minimum i maksimum często ujawniają problemy z jakością danych.

4. **Narysuj rozkłady według warunku:** Narysuj histogram (lub wykres skrzypcowy) RT osobno dla każdego warunku eksperymentalnego (zgodny, neutralny, niezgodny dla Stroopa). Szukaj różnic w kształcie, a nie tylko w położeniu.

5. **Narysuj średnie według warunku ze słupkami błędu:** Oblicz średnie (lub medianę) RT na warunek z 95 % przedziałami ufności. To standardowy wykres wynikowy — ale powinien być *ostatnim* krokiem, po sprawdzeniu pełnego rozkładu.

6. **Narysuj RT względem kolejności prób:** Sprawdź efekty ćwiczenia (RT maleje w czasie) i efekty zmęczenia (RT rośnie pod koniec sesji). Prosty wykres rozrzutu RT a numer próby ujawnia te zjawiska.

7. **Sprawdź różnice indywidualne:** Jeśli zbiór danych zawiera wielu uczestników, sprawdź, czy wzorzec na poziomie grupy utrzymuje się w obrębie każdej osoby. Średnie grupowe mogą maskować heterogeniczność.

Dopiero po wykonaniu tych kroków powinieneś sformułować konkretną hipotezę do testowania konfirmacyjnego.

## 6. Porównania warunków i wielkość efektu

Ostatecznym celem EDA w paradygmacie Stroopa jest określenie, czy rozkłady RT w trzech warunkach różnią się znacząco.

### 6.1 Nakładające się rozkłady

Jeśli rozkłady RT w warunkach niezgodnym i zgodnym niemal całkowicie się nakładają, efekt Stroopa może być mały lub zmienność może być wysoka. Narysowanie obu rozkładów jako nakładających się histogramów lub wykresów skrzypcowych natychmiast to ujawnia. Jeśli rozkłady są dobrze rozdzielone, efekt jest duży i prawdopodobnie niezawodny.

### 6.2 d Cohena

Po EDA pierwszą liczbą do obliczenia nie jest p-wartość, ale **wielkość efektu**. d Cohena wyraża różnicę między dwiema średnimi w jednostkach połączonego odchylenia standardowego:

> d = (M₁ − M₂) / SD_połączone

Konwencjonalne punkty odniesienia (Cohen, 1988):

| d | Interpretacja |
|---|---|
| 0,2 | Mały |
| 0,5 | Średni |
| 0,8 | Duży |

W projektach wewnątrz-podmiotowych (jakimi zazwyczaj są paradygmaty Stroopa) odpowiednim wariantem jest Cohen's d_z — używający odchylenia standardowego *wyników różnicowych*.

Wielkość efektu jest krytyczna, ponieważ przy wystarczająco dużej próbie nawet trywialnie mała różnica (d = 0,05, odpowiadająca 3 ms przy wyjściowym RT 600 ms) będzie statystycznie istotna. Istotność statystyczna odpowiada na pytanie „czy efekt jest niezerowy?"; wielkość efektu odpowiada na pytanie „czy warto się nim przejmować?". EDA nie może odpowiedzieć na pierwsze pytanie, ale może definitywnie poinformować o drugim.

## Piśmiennictwo

- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- Anscombe, F. J. (1973). Graphs in statistical analysis. *The American Statistician, 27*(1), 17–21.
- Simmons, J. P., Nelson, L. D. i Simonsohn, U. (2011). False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant. *Psychological Science, 22*(11), 1359–1366.
- Wickham, H. (2016). *ggplot2: Elegant Graphics for Data Analysis* (wyd. 2). Springer.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (wyd. 2). Lawrence Erlbaum.
