# Teoria — Brakujące wartości i wartości odstające

## 1. Dlaczego brakujące dane to nie drobna niedogodność

Każdy empiryczny zbiór danych zawiera luki. Uczestnik nie zdąży odpowiedzieć przed upływem limitu czasu; czujnik przez trzy sekundy traci sygnał; pytanie w kwestionariuszu pozostaje puste. Pokusa jest prosta: usunąć te wiersze i kontynuować. Jednak brakujące dane nie są przypadkowym szumem — niosą informację o procesie, który je wytworzył. To wzorzec braków, a nie tylko ich liczba, decyduje o tym, jak poważne szkody wyrządzają wnioskom statystycznym.

Donald Rubin (1976) sformalizował to spostrzeżenie, wprowadzając taksonomię trzech mechanizmów generowania braków, która pozostaje standardowym odniesieniem dla ilościowych badaczy we wszystkich naukach empirycznych.

## 2. Taksonomia Rubina: MCAR, MAR, MNAR

### 2.1 Brakujące całkowicie losowo (MCAR)

Wartość jest **MCAR**, gdy prawdopodobieństwo jej braku nie zależy od żadnej zmiennej w zbiorze danych — obserwowanej ani nieobserwowanej. Formalnie, jeśli *R* jest binarnym wskaźnikiem braków, a *Y* to pełna macierz danych:

> P(R | Y) = P(R)

W praktyce MCAR oznacza, że brakujące wiersze są prostą losową próbką wszystkich wierszy. Jeśli to założenie jest spełnione, usuwanie wierszy (listwise deletion) daje nieobciążone estymatory. Jedynym kosztem jest zmniejszona moc statystyczna.

**Przykład:** Pożar laboratorium niszczy losowo wybrany 10 % arkuszy odpowiedzi. Szkoda jest czysto fizyczna i niezwiązana z zachowaniem uczestnika. To MCAR.

**Jak testować MCAR:** Test MCAR Little'a (1988) porównuje obserwowane średnie zmiennych w różnych wzorcach braków za pomocą statystyki chi-kwadrat. Nieistotny wynik jest spójny z MCAR (ale go nie dowodzi).

### 2.2 Brakujące losowo (MAR)

Wartość jest **MAR**, gdy prawdopodobieństwo jej braku zależy od *obserwowanych* zmiennych, ale nie od samej brakującej wartości. Formalnie:

> P(R | Y) = P(R | Y_obs)

Nazwa jest myląca: dane nie są losowe w potocznym sensie. Termin oznacza, że brak jest wyjaśnialny po uwzględnieniu tego, co widzimy.

**Przykład:** Starsi uczestnicy częściej pomijają ostatnią stronę kwestionariusza (prawdopodobnie z powodu zmęczenia). Wiek jest obserwowany. Jeśli kontrolujemy wiek, pozostałe braki są niezwiązane z odpowiedziami na pytania. To MAR.

W warunkach MAR usuwanie wierszy jest obciążone, ale estymacja metodą największej wiarygodności i wielokrotna imputacja — obie korzystające ze struktury obserwowanych danych — dają trafne wnioski (Schafer i Graham, 2002).

### 2.3 Brakujące nielosowo (MNAR)

Wartość jest **MNAR**, gdy prawdopodobieństwo jej braku zależy od *samej brakującej wartości*, nawet po uwzględnieniu wszystkich obserwowanych zmiennych. Formalnie:

> P(R | Y) ≠ P(R | Y_obs)

To najniebezpieczniejszy mechanizm, bo nie istnieje czysto statystyczne lekarstwo. Obciążenie można zmniejszyć jedynie przez jawne modelowanie procesu generowania braków lub zebranie dodatkowych danych.

**Przykład:** Pacjent rezygnuje z udziału w próbie klinicznej, bo jego objawy się nasiliły — właśnie ten wynik, który był mierzony, powoduje rezygnację. To MNAR.

### 2.4 Tabela podsumowująca

| Mechanizm | Od czego zależy brak | Usuwanie wierszy | Imputacja |
|---|---|---|---|
| MCAR | Od niczego | Nieobciążone (tylko utrata mocy) | Dopuszczalna |
| MAR | Od obserwowanych zmiennych | Obciążone | Trafna |
| MNAR | Od brakującej wartości | Obciążone | Obciążona |

## 3. MCAR jest rzadkie w kognitywistyce

Założenie MCAR rzadko jest spełnione w badaniach behawioralnych i kognitywnych. Rozważmy najpowszechniejszą formę brakujących danych w paradygmatach czasu reakcji (RT): **próbę z przekroczonym limitem czasu**.

Gdy uczestnik nie odpowie w oknie odpowiedzi (zazwyczaj 2 000–3 000 ms), próba jest rejestrowana jako timeout. Czy ten brakujący RT nie zależy od niczego? Nie. Timeout pojawia się przede wszystkim w **trudnych** próbach — niezgodnych elementach Stroopa, zadaniach z dużym obciążeniem pamięci roboczej, niejednoznacznych bodźcach. Brakujący RT jest skorelowany z ukrytą trudnością próby, która jest nieobserwowana, ale realna. To klasyczny przykład **MNAR**.

Konsekwencja jest poważna: jeśli po prostu usuniesz próby z timeoutem i uśrednisz pozostałe RT, Twój estymator średniego RT w trudnym warunku jest obciążony *w dół* — usunąłeś dokładnie najwolniejsze odpowiedzi. Mierzony efekt Stroopa kurczy się sztucznie.

Podobna logika dotyczy:
- **Odrzucania artefaktów EEG:** Zaszumione epoki są częstsze podczas mrugnięć i ruchów, które współwystępują z określonymi stanami poznawczymi.
- **Rezygnacji w badaniach podłużnych:** Uczestnicy opuszczający kilkutygodniowe badanie to często ci z najgorszymi wynikami.
- **Kwestionariuszy samoopisu:** Pytania o wrażliwe tematy (zażywanie narkotyków, nasilenie depresji) są częściej pomijane przez osoby najbardziej dotknięte problemem.

## 4. Postępowanie z brakującymi danymi

### 4.1 Usuwanie wierszy (analiza kompletnych przypadków)

Usuwa wszystkie obserwacje z jakimkolwiek brakiem. Proste i przejrzyste. Trafne tylko przy MCAR. W warunkach MAR lub MNAR wprowadza obciążenie proporcjonalne do wskaźnika braków i siły korelacji między brakiem a wynikiem.

**Kiedy dopuszczalne:** Wskaźnik braków jest niski (< 5 %), mechanizm jest wiarygodnie MCAR, a w sekcji metod zamieszczono stosowną uwagę.

### 4.2 Imputacja średnią i medianą

Zastąp każdą brakującą wartość średnią (lub medianą) kolumny. Zachowuje wielkość próby, ale sztucznie zmniejsza zmienność — imputowany rozkład ma pik w miejscu średniej, co ściska odchylenia standardowe i korelacje. Daje to zbyt pewne (zbyt wąskie) przedziały ufności.

**Werdykt:** Odradzana w analizie wnioskowej. Dopuszczalna wyłącznie w tabelach eksploracyjnych, gdzie kształt rozkładu nie jest przedmiotem wnioskowania.

### 4.3 Wielokrotna imputacja (MI)

Wielokrotna imputacja (Rubin, 1987; van Buuren, 2018) generuje *m* kompletnych zbiorów danych, losując wiarygodne wartości z rozkładu a posteriori brakujących danych przy danych obserwowanych. Każdy zbiór jest analizowany oddzielnie, a wyniki są łączone za pomocą reguł Rubina. Metoda propaguje niepewność co do brakujących wartości do końcowego estymatora.

**Kroki:**
1. Utwórz *m* imputowanych zbiorów danych (zazwyczaj *m* = 20–100 przy dużym wskaźniku braków).
2. Dopasuj model do każdego zbioru.
3. Połącz estymatory parametrów: estymator punktowy to średnia *m* estymatorów; błąd standardowy uwzględnia zarówno wariancję wewnątrz-, jak i między-imputacyjną.

**Trafna przy:** MAR (i przy analizie wrażliwości — MNAR).

Oprogramowanie: `mice` (R), `IterativeImputer` (scikit-learn), Amelia II (R), fancyimpute (Python).

### 4.4 Podejścia modelowe

Pełna informacja przez maksymalizację wiarygodności (FIML) i modele bayesowskie używają wszystkich dostępnych danych, maksymalizując wiarygodność na obserwowanym wzorcu danych, marginalizując po brakujących wartościach. Są teoretycznie równoważne wielokrotnej imputacji w warunkach MAR i są domyślne w wielu pakietach do modelowania równań strukturalnych.

## 5. Wartości odstające: dwie definicje w konflikcie

**Wartość odstająca** to obserwacja skrajna względem reszty danych. Ale „skrajna" może oznaczać dwie różne rzeczy:

- **Statystyczna wartość odstająca:** Obserwacja leżąca daleko od masy rozkładu, zazwyczaj definiowana jako wynik z |z| > 3 lub wartość poza Q1 − 1,5·IQR lub Q3 + 1,5·IQR (kryterium Tukeya).
- **Teoretyczna wartość odstająca:** Obserwacja niemożliwa do uzasadnienia na podstawie wiedzy dziedzinowej, niezależnie od jej odległości statystycznej od średniej próby.

Te dwie definicje mogą być sprzeczne. Czas reakcji 850 ms może być całkowicie normalny dla zadania Stroopa (nie jest statystyczną wartością odstającą), ale być najszybszą odpowiedzią danego uczestnika, co sugeruje reakcję antycypacyjną. I odwrotnie — odpowiedź 2 800 ms może nie przekraczać progu wynikającego z z-score u powolnego uczestnika, a mimo to reprezentować lukę uwagową.

**Wiedza dziedzinowa musi mieć pierwszeństwo.** Statystyki mogą wskazywać kandydatów; tylko ekspertyza może podjąć decyzję.

## 6. Wartości odstające w danych czasu reakcji

Rozkłady RT mają dobrze ustalone ograniczenia fizjologiczne, które definiują twarde granice:

### 6.1 Dolna granica: odpowiedzi antycypacyjne

Minimalny czas potrzebny do wykrycia bodźca wzrokowego, przetworzenia go i zainicjowania odpowiedzi ruchowej wynosi około **100 ms**. Odzwierciedla to:
- ~40–60 ms na transdukcję siatkówkową i wczesne przetwarzanie w korze wzrokowej
- ~20–40 ms na transmisję polecenia ruchowego i aktywację mięśni

Każda odpowiedź szybsza niż 100 ms została wyprodukowana *zanim* bodziec mógł być w pełni przetworzony. To **odpowiedzi antycypacyjne** — uczestnik nacisnął klawisz w oczekiwaniu, a nie w reakcji. Należy je wykluczyć niezależnie od warunku.

### 6.2 Górna granica: luki uwagowe

Nie istnieje stała górna granica, ale odpowiedzi wolniejsze niż **3 000 ms** (a w szybkich zadaniach — 2 000 ms) zazwyczaj odzwierciedlają chwile, gdy uwaga uczestnika była gdzie indziej — kichnięcie, powiadomienie telefonu, chwila rozbłąkanych myśli. Te skrajne wartości lepiej modelować jako składnik mieszaniny (proces lapsów) niż jako prawdziwą wydajność wykonania zadania.

Ratcliff (1993) przeanalizował kilka strategii przycinania i stwierdził, że usunięcie odpowiedzi poniżej 200 ms i powyżej 3 000 ms, połączone z 2,5 % przycinaniem z każdego ogona pozostałego rozkładu, zapewnia równowagę między obciążeniem a efektywnością dla większości paradygmatów RT.

### 6.3 Wpływ wartości odstających na średnią

Rozkłady RT są **prawostronnie skośne**: istnieje twarda dolna granica, ale rozległy prawy ogon. W prawostronnie skośnym rozkładzie średnia przekracza medianę, a jedna skrajna wartość może istotnie przesunąć średnią.

**Przykład obliczeń:**

| Próba | RT (ms) |
|---|---|
| 1 | 450 |
| 2 | 510 |
| 3 | 490 |
| 4 | 530 |
| 5 | 5 200 |

Średnia bez próby 5: 495 ms. Średnia z próbą 5: 1 236 ms. Mediana z próbą 5: 510 ms.

Jeden 5 200 ms lapsus zawyża średnią o 741 ms — więcej niż jakikolwiek prawdziwy efekt Stroopa. Mediana pozostaje niezmieniona.

| Statystyka | Odporna na wartości odstające? |
|---|---|
| Średnia | Nie |
| Mediana | Tak |
| Ucięta średnia (2,5 %) | Częściowo |
| Odchylenie standardowe | Nie |
| IQR | Tak |

### 6.4 Ucięta średnia

**Ucięta średnia** odrzuca stały odsetek obserwacji z każdego ogona przed uśrednieniem pozostałych. 10 % ucięta średnia usuwa najniższy 10 % i najwyższy 10 % wartości. Jest bardziej odporna na wartości odstające niż pełna średnia i bardziej efektywna (używa więcej danych) niż mediana.

Wilcox (2005) zaleca 20 % uciętą średnią dla danych RT jako odporny estymator, który zachowuje wrażliwość na prawdziwe efekty eksperymentalne, jednocześnie tłumiąc zanieczyszczenie lapsami.

## 7. Standardy raportowania

**Podręcznik publikacji APA** (7. wyd.) i **CONSORT** (dla badań klinicznych) wymagają jawnego raportowania wykluczeń danych. Kluczowe elementy to:

1. **N wykluczonych według kryterium** — ile obserwacji usunięto na każdym kroku.
2. **Powód wykluczenia** — zastosowane kryterium (np. RT < 100 ms, dokładność < 50 %).
3. **Podział według warunków** — czy wykluczenia były równomiernie rozłożone między warunkami? Nierównomierne wskaźniki wykluczeń mogą wprowadzać obciążenie.
4. **Mechanizm braków** — jakie założono mechanizm (MCAR, MAR) i dlaczego.
5. **Zastosowana metoda** — usuwanie wierszy, metoda imputacji, pakiet oprogramowania.

Przejrzyste sprawozdanie może brzmieć: *„Próby z RT < 100 ms (N = 12, 0,4 % łącznie) i RT > 3 000 ms (N = 8, 0,3 %) wykluczono przed analizą. Dodatkowo wykluczono trzech uczestników (N = 186 prób, 6,2 %) z ogólną dokładnością poniżej 60 %. Brakujące dane nie były imputowane; zastosowano analizę kompletnych przypadków, która jest trafna przy założeniu, że wykluczenia były MCAR względem warunku."*

## 8. Lista kontrolna

Przed złożeniem jakiejkolwiek analizy obejmującej brakujące dane lub usuwanie wartości odstających:

- [ ] Podaj łączną liczbę brakujących/wykluczonych obserwacji i odsetek całości.
- [ ] Uzasadnij kryteria wykluczeń (podaj odniesienie lub uzasadnienie fizjologiczne).
- [ ] Sprawdź, czy wskaźniki wykluczeń różnią się między warunkami eksperymentalnymi.
- [ ] Podaj zakładany mechanizm braków i uzasadnij go lub podaj odniesienie.
- [ ] Przedstaw wyniki zarówno z wyłączeniem, jak i bez wyłączenia wartości odstających jako analizę wrażliwości.

## Piśmiennictwo

- Rubin, D. B. (1976). Inference and missing data. *Biometrika, 63*(3), 581–592.
- Schafer, J. L. i Graham, J. W. (2002). Missing data: Our view of the state of the art. *Psychological Methods, 7*(2), 147–177.
- Ratcliff, R. (1993). Methods for dealing with reaction time outliers. *Psychological Bulletin, 114*(3), 510–532.
- van Buuren, S. (2018). *Flexible Imputation of Missing Data* (wyd. 2). CRC Press. [Otwarty dostęp: https://stefvanbuuren.name/fimd/]
- Little, R. J. A. (1988). A test of missing completely at random for multivariate data with missing values. *Journal of the American Statistical Association, 83*(404), 1198–1202.
- Wilcox, R. R. (2005). *Introduction to Robust Estimation and Hypothesis Testing* (wyd. 2). Academic Press.
