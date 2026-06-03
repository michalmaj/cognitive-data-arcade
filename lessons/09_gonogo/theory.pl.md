# Teoria — Hamowanie odpowiedzi i paradygmat Go/No-Go

## 1. Kontekst historyczny

Naukowy pomiar hamowania odpowiedzi ma korzenie w jednym z najstarszych eksperymentow w psychologii poznawczej. **Franciscus Donders** (1868) opisal swoja "reakcje C" — warunek, w ktorym uczestnik musial odpowiadac na jeden z dwoch bodzcow i powstrzymywac odpowiedz na drugi. Donders zauwazyl, ze ta selektywna reakcja zajmuje wiecej czasu niz prosta reakcja i przypisal roznice czasowi wymaganemu do rozroznienia bodzcow i wyboru odpowiedzi. Byl to konceptualny przodek wspolczesnego zadania Go/No-Go.

Paradygmat Go/No-Go zostal sformalizowany jako laboratoryjny pomiar **hamowania odpowiedzi** w latach 70. XX wieku i upowszechnil sie w neuropsychologii w latach 80. i 90. Nalezy dzis do najczesciej stosowanych zadan w neuronauce poznawczej, klinicznej neuropsychologii i badaniach rozwojowych. Jego atrakcyjnosc tkwi w prostocie: jeden przycisk, dwa typy bodzcow, jednoznaczny wskaznik nieudanego hamowania — blad komisji.

## 2. Struktura zadania

W kazdej probie zadania Go/No-Go na ekranie pojawia sie jeden bodziec. Uczestnik musi:

- Nacisnac klawisz **jak najszybciej**, gdy pojawi sie bodziec Go (np. zielone kolo, litera X, strzalka w gore).
- **Powstrzymac** nacisnięcie, gdy pojawi sie bodziec No-Go (np. czerwone kolo, litera K, strzalka w dol).

Wyzwanie poznawcze wynika z asymetrii miedzy probami Go i No-Go. Poniewaz proby Go stanowia wiekszosc (zazwyczaj 70–80% wszystkich prob), uczestnicy wyksztalcaja **prepotentna odpowiedz** — silna, nawykowa tendencje do naciskania klawisza za kazdym razem, gdy pojawia sie jakikolwiek bodziec. Bodziec No-Go musi przerywac te automatyczna tendencje w momencie, gdy jest ona najsilniejsza.

Dlatego prawidlowe zahamowanie w probach No-Go nie jest po prostu brakiem ruchu. Jest to aktywne stlumienie odpowiedzi motorycznej, ktora zostala juz czesciowo przygotowana. Neuronalne i obliczeniowe zasoby wymagane do tego tlumienia sa przedmiotem dekad badan.

## 3. Proporcja Go i prepotencja

**Proporcja Go** to udzial prob Go wzgledem wszystkich prob. Jest glownym wyznacznikiem trudnosci zadania:

| Proporcja Go | Proporcja No-Go | Prepotencja | Typowy wskaznik bledow komisji |
|---|---|---|---|
| 50% | 50% | Niska | ~5% |
| 70% | 30% | Umiarkowana | ~8–12% |
| 75% | 25% | Wysoka | ~10–15% |
| 80% | 20% | Bardzo wysoka | ~15–20% |
| 90% | 10% | Ekstremalna | ~25–35% |

W tej aplikacji:
- **Latwy:** 80% Go (1,2 s okno odpowiedzi)
- **Sredni:** 75% Go (standard, 1,0 s okno odpowiedzi)
- **Trudny:** 60% Go (mniejsza prepotencja, ale krotsze okno 0,7 s — presja czasowa rekompensuje)

Wyzsza proporcja Go zwieksza prepotencje, a tym samym bledy komisji. To operacyjna definicja obciazenia hamowania: im wieksza automatycznosc odpowiedzi Go, tym wiecej zasobow poznawczych potrzeba do jej zatrzymania.

## 4. Dwa rodzaje bledow

Zadanie Go/No-Go generuje dwa odrębne rodzaje bledow, z ktorych kazdy mierzy inny proces poznawczy:

**Bledy komisji (falszywe alarmy):** Uczestnik naciska klawisz w probie No-Go. Jest to niepowodzenie kontroli hamowania. Wskazuje, ze prepotentna odpowiedz Go zostala zainicjowana, ale nie zostala stlumiona na czas. Bledy komisji sa glownym wynikiem zadania — indeksuja zdolnosc do **hamowania odpowiedzi**.

**Bledy pominiecia (chybienia):** Uczestnik nie naciska klawisza w probie Go. Nie jest to brak hamowania, lecz zazwyczaj niepowodzenie **uwagi podtrzymanej** — uczestnik nie byl wystarczajaco czujny, by wykryc bodziec Go w oknie odpowiedzi, lub reaguowal zbyt wolno. Wysokie wskazniki chybien zwykle wskazuja na zmeczenie, nieuwage lub skrajnie konserwatywna strategie odpowiadania.

Rozroznienie ma znaczenie kliniczne. Uczestnik z wieloma bledami komisji, ale nielicznymi chybieniami jest impulsywny. Uczestnik z nielicznymi bledami komisji, ale wieloma chybieniami moze byc nadmiernie zachowawczy lub nieuważny.

## 5. Teoria detekcji sygnalu i d'

Surowe wyniki trafnosci i liczby bledow zalezy od **strategii odpowiadania** — ogolnej tendencji uczestnika do naciskania lub nienaciskania klawisza, niezaleznie od bodzcow. Uczestnik, ktory nigdy nie naciska klawisza, bedzie mial zero bledow komisji, ale rowniez wiele chybien. Uczestnik, ktory zawsze naciska, bedzie mial zero chybien, ale wiele bledow komisji. Zadne z tych ekstremalnych zachowan nie jest dobrym wynikiem — oba swiadcza o niepowodzeniu rozroznienia Go od No-Go.

**Teoria detekcji sygnalu (SDT)** dostarcza miary dyskryminacyjnosci niezaleznej od strategii: **d' (d-prim)**.

Wzor:

```
d' = Z(wskaznik trafien) - Z(wskaznik falszywych alarmow)
```

Gdzie:
- **Wskaznik trafien** = (liczba prob Go z odpowiedzia) / (calkowita liczba prob Go)
- **Wskaznik FA** = (liczba prob No-Go z odpowiedzia) / (calkowita liczba prob No-Go)
- **Z(p)** to odwrotnosc normalnej dystrybuanty — wynik z odpowiadajacy prawdopodobienstwu p

### Interpretacja d'

| Wartosc d' | Interpretacja |
|---|---|
| 0,0 | Brak dyskryminacji — wynik przypadkowy |
| 1,0 | Slaba dyskryminacja |
| 2,0 | Dobra dyskryminacja (typowy zdrowy dorosly) |
| 2,5–3,5 | Silna dyskryminacja |
| > 4,0 | Niemal doskonala dyskryminacja |

Przyklad obliczenia: uczestnik odpowiada w 92% prob Go (trafien = 0,92) i w 8% prob No-Go (FA = 0,08). Z tabeli: Z(0,92) ≈ 1,41; Z(0,08) ≈ −1,41. Zatem d' = 1,41 − (−1,41) = 2,82 — silna dyskryminacja.

Uproszczona tabela wynikow z dla czestych wartosci:

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

**Uwaga:** Jesli wskaznik trafien = 1,00 lub wskaznik FA = 0,00, wynik z jest nieokreslony. W praktyce stosuje sie korekcje: 0 zastepuje sie wartoscia 0,5/n, a 1 zastepuje sie (n − 0,5)/n, gdzie n jest liczba prob danego typu (Macmillan i Creelman, 2005).

## 6. Neuronalne podstawy kontroli hamowania

Hamowanie odpowiedzi nie jest jednolitym procesem zlokalizowanym w jednym obszarze mozgu. W jego realizacje zaangazowanych jest wiele obwodow przedczolowych i podkorowych:

**Prawy zakret czolowy dolny (rIFG):** Uwazany za glowny "hamulec" odpowiedzi motorycznych. Uszkodzenia rIFG u ludzi (np. po udarze) powoduja wzrost bledow komisji w zadaniach Go/No-Go i Stop-Signal. Przezczaszkowa stymulacja magnetyczna (TMS) rIFG rowniez uposleda wyniki hamowania u zdrowych uczestnikow (Aron i Poldrack, 2006).

**Prawy obszar przedczolowy (rPFC) szerzej:** Badania fMRI konsekwentnie wykazuja prawostronna aktywacje przedczolowa w udanych probach No-Go w porownaniu z probami Go.

**Jadro niskowzgorzowe (STN):** Gleboka struktura w jadrach podstawy. Uważa sie, ze "nadprosty szlak" z rIFG do STN posredniczy w szybkim, globalnym zatrzymaniu programow motorycznych — rodzaj hamulca awaryjnego.

**Komponenty ERP:** Komponent N2 (ujemne odchylenie ~200–300 ms po bodzcach No-Go) jest wiekszy w probach No-Go niz Go i odzwierciedla proces hamowania. Komponent P3 (~300–500 ms) w probach No-Go odzwierciedla wynik przetwarzania hamujacego.

## 7. Zmiany rozwojowe w kontroli hamowania

Hamowanie odpowiedzi wykazuje dluga krzywą rozwojowa. Dzieci w wieku 6–8 lat maja wskazniki bledow komisji na poziomie 30–40%, nawet przy standardowej proporcji Go. Wyniki poprawiaja sie znacznie miedzy 8. a 12. rokiem zycia i nadal — choć wolniej — przez adolescencje az do wczesnej doroslosci.

| Grupa wiekowa | Typowy wskaznik bledow komisji (75% Go) |
|---|---|
| 6–8 lat | 30–40% |
| 9–11 lat | 20–28% |
| 12–14 lat | 12–18% |
| 15–17 lat | 8–12% |
| Mlodzi dorosli (18–25) | 5–12% |
| Starsi dorosli (60+) | 10–18% |

Pozne dojrzewanie kontroli hamowania jest rownolegle do dlugiego dojrzewania kory przedczolowej, ktora nie jest w pelni zmielinizowana az do okolo 25. roku zycia. Starsi dorosli wykazuja czesciowy powrot podwyzszonych bledow komisji, co jest zgodne z wiekowym spadkiem funkcji przedczolowych.

## 8. Zastosowania kliniczne

Zadanie Go/No-Go jest standardowym narzedziem w klinicznej neuropsychologii:

**ADHD:** Dzieci i dorosli z ADHD wykazuja znaczaco podwyzszone wskazniki bledow komisji i obnizony d', co odzwierciedla uposledzenie kontroli hamowania. Zadanie Go/No-Go jest zawarte w baterii CANTAB (Cambridge Neuropsychological Test Automated Battery) i podobnych skomputeryzowanych zestawach oceny. Bylo stosowane do monitorowania efektow leczenia — metylofenidat (Ritalin) niezawodnie zmniejsza bledy komisji w populacjach z ADHD (Heaton i in., 2004).

**Uszkodzenia platow czolowych:** Pacjenci z uszkodzeniami kory przedczolowej — spowodowanymi udarem, guzem lub urazowym uszkodzeniem mozgu — wykazuja podwyzszone bledy komisji nawet przy nienaruszonych ogolnych zdolnosciach intelektualnych i czasie reakcji. Zadanie Go/No-Go dostarcza zatem specyficznego pomiaru czolowych funkcji wykonawczych, wykraczajacego poza ogolna szybkosc przetwarzania.

**Uzywanie substancji i impulsywnosc:** Wyniki Go/No-Go koreluja z samooceną impulsywnosci oraz z zachowaniami ryzykownymi. Uczestnicy z wysokimi wynikami na skalach impulsywnosci cechowej (np. Skala Impulsywnosci Barratta) maja tendencje do wyaszych wskaznikow bledow komisji.

## 9. Zadanie Stop-Signal: pokrewny paradygmat

**Zadanie Stop-Signal (SST)** jest scisle zwiazane z zadaniem Go/No-Go, ale mierzy konceptualnie odrębny proces:

W SST kazda proba zaczyna sie jako proba Go — uczestnik przygotowuje i zaczyna wykonywac odpowiedz. W czesci prob pojawia sie **sygnal stopu** (dzwiek, blysk) krotko po sygnale Go. Uczestnik musi anulowac odpowiedz, ktora jest juz w toku. Opoznienie miedzy sygnalami Go i Stop jest zmieniane tak, aby zatrzymanie udawalo sie w okolo 50% przypadkow.

Na podstawie danych SST badacze szacuja **czas reakcji na sygnal stopu (SSRT)** — latencje ukrytego procesu zatrzymania. Ramy teoretyczne stanowi **model wyscigu koni** (Logan i Cowan, 1984): procesy Go i Stop scigaja sie ze soba; ten, ktory konczy sie pierwszy, wyznacza wynik.

| Cecha | Go/No-Go | Zadanie Stop-Signal |
|---|---|---|
| Przygotowanie odpowiedzi | Czesciowe | Pelne, juz zainicjowane |
| Czas sygnalu stopu | Rownolegle z bodźcem | Opozniony po sygnale Go |
| Glowna miara | Bledy komisji, d' | Czas reakcji na sygnal stopu (SSRT) |
| Rodzaj hamowania | Proaktywne (antycypacyjne) | Reaktywne (po inicjacji) |

Oba zadania angazuja rIFG, ale SST czysciej izoluje reaktywny proces zatrzymania (Verbruggen i Logan, 2008).

## 10. Literatura

- Aron, A. R., & Poldrack, R. A. (2006). Cortical and subcortical contributions to stop signal response inhibition: role of the subthalamic nucleus. *Journal of Neuroscience, 26*(9), 2424–2433.
- Donders, F. C. (1868/1969). On the speed of mental processes. *Acta Psychologica, 30*, 412–431. (Przetlumaczyl W. G. Koster)
- Heaton, S. C., Avila, M. T., Bailey, A. A., & Thaker, G. K. (2004). Specific working memory and executive function deficits in schizophrenia and related conditions. *Neuropsychology, 18*(4), 651–660.
- Logan, G. D., & Cowan, W. B. (1984). On the ability to inhibit thought and action: a theory of an act of control. *Psychological Review, 91*(3), 295–327.
- Macmillan, N. A., & Creelman, C. D. (2005). *Detection Theory: A User's Guide* (2. wyd.). Lawrence Erlbaum Associates.
- Verbruggen, F., & Logan, G. D. (2008). Response inhibition in the stop-signal paradigm. *Trends in Cognitive Sciences, 12*(11), 418–424.
