# Teoria — Hamowanie odpowiedzi i paradygmat Go/No-Go

## 1. Kontekst historyczny

Naukowy pomiar hamowania odpowiedzi ma korzenie w jednym z najstarszych eksperymentów w psychologii poznawczej. **Franciscus Donders** (1868) opisał swoją "reakcję C" — warunek, w którym uczestnik musiał odpowiadać na jeden z dwóch bodźców i powstrzymywać odpowiedź na drugi. Donders zauważył, że ta selektywna reakcja zajmuje więcej czasu niż prosta reakcja i przypisał różnicę czasowi wymaganemu do rozróżnienia bodźców i wyboru odpowiedzi. Był to konceptualny przodek współczesnego zadania Go/No-Go.

Paradygmat Go/No-Go został sformalizowany jako laboratoryjny pomiar **hamowania odpowiedzi** w latach 70. XX wieku i upowszechnił się w neuropsychologii w latach 80. i 90. Należy dziś do najczęściej stosowanych zadań w neuronauce poznawczej, klinicznej neuropsychologii i badaniach rozwojowych. Jego atrakcyjność tkwi w prostocie: jeden przycisk, dwa typy bodźców, jednoznaczny wskaźnik nieudanego hamowania — błąd komisji.

## 2. Struktura zadania

W każdej próbie zadania Go/No-Go na ekranie pojawia się jeden bodziec. Uczestnik musi:

- Nacisnąć klawisz **jak najszybciej**, gdy pojawi się bodziec Go (np. zielone koło, litera X, strzałka w górę).
- **Powstrzymać** naciśnięcie, gdy pojawi się bodziec No-Go (np. czerwone koło, litera K, strzałka w dół).

Wyzwanie poznawcze wynika z asymetrii między próbami Go i No-Go. Ponieważ próby Go stanowią większość (zazwyczaj 70–80% wszystkich prób), uczestnicy wykształcają **prepotentną odpowiedź** — silną, nawykową tendencję do naciskania klawisza za każdym razem, gdy pojawia się jakikolwiek bodziec. Bodziec No-Go musi przerywać tę automatyczną tendencję w momencie, gdy jest ona najsilniejsza.

Dlatego prawidłowe zahamowanie w próbach No-Go nie jest po prostu brakiem ruchu. Jest to aktywne stłumienie odpowiedzi motorycznej, która została już częściowo przygotowana. Neuronalne i obliczeniowe zasoby wymagane do tego tłumienia są przedmiotem dekad badań.

## 3. Proporcja Go i prepotencja

**Proporcja Go** to udział prób Go względem wszystkich prób. Jest głównym wyznacznikiem trudności zadania:

| Proporcja Go | Proporcja No-Go | Prepotencja | Typowy wskaźnik błędów komisji |
|---|---|---|---|
| 50% | 50% | Niska | ~5% |
| 70% | 30% | Umiarkowana | ~8–12% |
| 75% | 25% | Wysoka | ~10–15% |
| 80% | 20% | Bardzo wysoka | ~15–20% |
| 90% | 10% | Ekstremalna | ~25–35% |

W tej aplikacji:
- **Łatwy:** 80% Go (1,2 s okno odpowiedzi)
- **Średni:** 75% Go (standard, 1,0 s okno odpowiedzi)
- **Trudny:** 60% Go (mniejsza prepotencja, ale krótsze okno 0,7 s — presja czasowa rekompensuje)

Wyższa proporcja Go zwiększa prepotencję, a tym samym błędy komisji. To operacyjna definicja obciążenia hamowania: im większa automatyczność odpowiedzi Go, tym więcej zasobów poznawczych potrzeba do jej zatrzymania.

## 4. Dwa rodzaje błędów

Zadanie Go/No-Go generuje dwa odrębne rodzaje błędów, z których każdy mierzy inny proces poznawczy:

**Błędy komisji (fałszywe alarmy):** Uczestnik naciska klawisz w próbie No-Go. Jest to niepowodzenie kontroli hamowania. Wskazuje, że prepotentna odpowiedź Go została zainicjowana, ale nie została stłumiona na czas. Błędy komisji są głównym wynikiem zadania — indeksują zdolność do **hamowania odpowiedzi**.

**Błędy pominięcia (chybienia):** Uczestnik nie naciska klawisza w próbie Go. Nie jest to brak hamowania, lecz zazwyczaj niepowodzenie **uwagi podtrzymanej** — uczestnik nie był wystarczająco czujny, by wykryć bodziec Go w oknie odpowiedzi, lub reagował zbyt wolno. Wysokie wskaźniki chybień zwykle wskazują na zmęczenie, nieuwagę lub skrajnie konserwatywną strategię odpowiadania.

Rozróżnienie ma znaczenie kliniczne. Uczestnik z wieloma błędami komisji, ale nielicznymi chybieniami jest impulsywny. Uczestnik z nielicznymi błędami komisji, ale wieloma chybieniami może być nadmiernie zachowawczy lub nieuważny.

## 5. Teoria detekcji sygnału i d'

Surowe wyniki trafności i liczby błędów zależą od **strategii odpowiadania** — ogólnej tendencji uczestnika do naciskania lub nienaciskania klawisza, niezależnie od bodźców. Uczestnik, który nigdy nie naciska klawisza, będzie miał zero błędów komisji, ale również wiele chybień. Uczestnik, który zawsze naciska, będzie miał zero chybień, ale wiele błędów komisji. Żadne z tych ekstremalnych zachowań nie jest dobrym wynikiem — oba świadczą o niepowodzeniu rozróżnienia Go od No-Go.

**Teoria detekcji sygnału (SDT)** dostarcza miary dyskryminacyjności niezależnej od strategii: **d' (d-prim)**.

Wzór:

```
d' = Z(wskaźnik trafień) - Z(wskaźnik fałszywych alarmów)
```

Gdzie:
- **Wskaźnik trafień** = (liczba prób Go z odpowiedzią) / (całkowita liczba prób Go)
- **Wskaźnik FA** = (liczba prób No-Go z odpowiedzią) / (całkowita liczba prób No-Go)
- **Z(p)** to odwrotność normalnej dystrybuanty — wynik z odpowiadający prawdopodobieństwu p

### Interpretacja d'

| Wartość d' | Interpretacja |
|---|---|
| 0,0 | Brak dyskryminacji — wynik przypadkowy |
| 1,0 | Słaba dyskryminacja |
| 2,0 | Dobra dyskryminacja (typowy zdrowy dorosły) |
| 2,5–3,5 | Silna dyskryminacja |
| > 4,0 | Niemal doskonała dyskryminacja |

Przykład obliczenia: uczestnik odpowiada w 92% prób Go (trafień = 0,92) i w 8% prób No-Go (FA = 0,08). Z tabeli: Z(0,92) ≈ 1,41; Z(0,08) ≈ −1,41. Zatem d' = 1,41 − (−1,41) = 2,82 — silna dyskryminacja.

Uproszczona tabela wyników z dla częstych wartości:

| p | Z(p) |
|---|---|
| 0,01 | −2,33 |
| 0,05 | −1,64 |
| 0,10 | −1,28 |
| 0,20 | −0,84 |
| 0,30 | −0,52 |
| 0,40 | −0,25 |
| 0,50 | 0,00 |
| 0,60 | 0,25 |
| 0,70 | 0,52 |
| 0,80 | 0,84 |
| 0,90 | 1,28 |
| 0,95 | 1,64 |
| 0,99 | 2,33 |

**Uwaga:** Jeśli wskaźnik trafień = 1,00 lub wskaźnik FA = 0,00, wynik z jest nieokreślony. W praktyce stosuje się korektę: 0 zastępuje się wartością 0,5/n, a 1 zastępuje się (n − 0,5)/n, gdzie n jest liczbą prób danego typu (Macmillan i Creelman, 2005).

## 6. Neuronalne podstawy kontroli hamowania

Hamowanie odpowiedzi nie jest jednolitym procesem zlokalizowanym w jednym obszarze mózgu. W jego realizację zaangażowanych jest wiele obwodów przedczołowych i podkorowych:

**Prawy zakręt czołowy dolny (rIFG):** Uważany za główny "hamulec" odpowiedzi motorycznych. Uszkodzenia rIFG u ludzi (np. po udarze) powodują wzrost błędów komisji w zadaniach Go/No-Go i Stop-Signal. Przezczaszkowa stymulacja magnetyczna (TMS) rIFG również upośledza wyniki hamowania u zdrowych uczestników (Aron i Poldrack, 2006).

**Prawy obszar przedczołowy (rPFC) szerzej:** Badania fMRI konsekwentnie wykazują prawostronną aktywację przedczołową w udanych próbach No-Go w porównaniu z próbami Go.

**Jądro niskowzgórzowe (STN):** Głęboka struktura w jądrach podstawy. Uważa się, że "nadprosty szlak" z rIFG do STN pośredniczy w szybkim, globalnym zatrzymaniu programów motorycznych — rodzaj hamulca awaryjnego.

**Komponenty ERP:** Komponent N2 (ujemne odchylenie ~200–300 ms po bodźcach No-Go) jest większy w próbach No-Go niż Go i odzwierciedla proces hamowania. Komponent P3 (~300–500 ms) w próbach No-Go odzwierciedla wynik przetwarzania hamującego.

## 7. Zmiany rozwojowe w kontroli hamowania

Hamowanie odpowiedzi wykazuje długą krzywą rozwojową. Dzieci w wieku 6–8 lat mają wskaźniki błędów komisji na poziomie 30–40%, nawet przy standardowej proporcji Go. Wyniki poprawiają się znacznie między 8. a 12. rokiem życia i nadal — choć wolniej — przez adolescencję aż do wczesnej dorosłości.

| Grupa wiekowa | Typowy wskaźnik błędów komisji (75% Go) |
|---|---|
| 6–8 lat | 30–40% |
| 9–11 lat | 20–28% |
| 12–14 lat | 12–18% |
| 15–17 lat | 8–12% |
| Młodzi dorośli (18–25) | 5–12% |
| Starsi dorośli (60+) | 10–18% |

Późne dojrzewanie kontroli hamowania jest równoległe do długiego dojrzewania kory przedczołowej, która nie jest w pełni zmielinizowana aż do około 25. roku życia. Starsi dorośli wykazują częściowy powrót podwyższonych błędów komisji, co jest zgodne z wiekowym spadkiem funkcji przedczołowych.

## 8. Zastosowania kliniczne

Zadanie Go/No-Go jest standardowym narzędziem w klinicznej neuropsychologii:

**ADHD:** Dzieci i dorośli z ADHD wykazują znacząco podwyższone wskaźniki błędów komisji i obniżony d', co odzwierciedla upośledzenie kontroli hamowania. Zadanie Go/No-Go jest zawarte w baterii CANTAB (Cambridge Neuropsychological Test Automated Battery) i podobnych skomputeryzowanych zestawach oceny. Było stosowane do monitorowania efektów leczenia — metylofenidat (Ritalin) niezawodnie zmniejsza błędy komisji w populacjach z ADHD (Heaton i in., 2004).

**Uszkodzenia płatów czołowych:** Pacjenci z uszkodzeniami kory przedczołowej — spowodowanymi udarem, guzem lub urazowym uszkodzeniem mózgu — wykazują podwyższone błędy komisji nawet przy nienaruszonych ogólnych zdolnościach intelektualnych i czasie reakcji. Zadanie Go/No-Go dostarcza zatem specyficznego pomiaru czołowych funkcji wykonawczych, wykraczającego poza ogólną szybkość przetwarzania.

**Używanie substancji i impulsywność:** Wyniki Go/No-Go korelują z samooceną impulsywności oraz z zachowaniami ryzykownymi. Uczestnicy z wysokimi wynikami na skalach impulsywności cechowej (np. Skala Impulsywności Barratta) mają tendencję do wyższych wskaźników błędów komisji.

## 9. Zadanie Stop-Signal: pokrewny paradygmat

**Zadanie Stop-Signal (SST)** jest ściśle związane z zadaniem Go/No-Go, ale mierzy konceptualnie odrębny proces:

W SST każda próba zaczyna się jako próba Go — uczestnik przygotowuje i zaczyna wykonywać odpowiedź. W części prób pojawia się **sygnał stopu** (dźwięk, błysk) krótko po sygnale Go. Uczestnik musi anulować odpowiedź, która jest już w toku. Opóźnienie między sygnałami Go i Stop jest zmieniane tak, aby zatrzymanie udawało się w około 50% przypadków.

Na podstawie danych SST badacze szacują **czas reakcji na sygnał stopu (SSRT)** — latencję ukrytego procesu zatrzymania. Ramy teoretyczne stanowi **model wyścigu koni** (Logan i Cowan, 1984): procesy Go i Stop ścigają się ze sobą; ten, który kończy się pierwszy, wyznacza wynik.

| Cecha | Go/No-Go | Zadanie Stop-Signal |
|---|---|---|
| Przygotowanie odpowiedzi | Częściowe | Pełne, już zainicjowane |
| Czas sygnału stopu | Równolegle z bodźcem | Opóźniony po sygnale Go |
| Główna miara | Błędy komisji, d' | Czas reakcji na sygnał stopu (SSRT) |
| Rodzaj hamowania | Proaktywne (antycypacyjne) | Reaktywne (po inicjacji) |

Oba zadania angażują rIFG, ale SST czyściej izoluje reaktywny proces zatrzymania (Verbruggen i Logan, 2008).

## 10. Literatura

- Aron, A. R., & Poldrack, R. A. (2006). Cortical and subcortical contributions to stop signal response inhibition: role of the subthalamic nucleus. *Journal of Neuroscience, 26*(9), 2424–2433.
- Donders, F. C. (1868/1969). On the speed of mental processes. *Acta Psychologica, 30*, 412–431. (Przetłumaczył W. G. Koster)
- Heaton, S. C., Avila, M. T., Bailey, A. A., & Thaker, G. K. (2004). Specific working memory and executive function deficits in schizophrenia and related conditions. *Neuropsychology, 18*(4), 651–660.
- Logan, G. D., & Cowan, W. B. (1984). On the ability to inhibit thought and action: a theory of an act of control. *Psychological Review, 91*(3), 295–327.
- Macmillan, N. A., & Creelman, C. D. (2005). *Detection Theory: A User's Guide* (2. wyd.). Lawrence Erlbaum Associates.
- Verbruggen, F., & Logan, G. D. (2008). Response inhibition in the stop-signal paradigm. *Trends in Cognitive Sciences, 12*(11), 418–424.
