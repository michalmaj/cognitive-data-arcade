# Teoria — Efekt Flankera

## 1. Kontekst historyczny

W 1974 roku Barbara A. Eriksen i Charles W. Eriksen opublikowali artykuł "Effects of noise letters upon the identification of a target letter in a nonsearch task" w *Perception & Psychophysics*. Ich oryginalny eksperyment używał liter, nie strzałek. Uczestnicy musieli identyfikować centralną literę docelową (np. H lub S), ignorując otaczające litery zgodne z wymaganą odpowiedzią (np. HHHHH), niezgodne (np. SSHSS) lub neutralne. Flankers niezawodnie zakłócały dobór odpowiedzi, nawet gdy uczestnicy wiedzieli, że są one nieistotne.

Paradygmat został zaprojektowany w celu odpowiedzi na konkretne pytanie teoretyczne: czy selektywna uwaga działa na poziomie pojedynczych bodźców, czy na poziomie regionów przestrzennych? Gdyby uwaga była doskonale selektywna na poziomie bodźców, flankers nie powodowałyby interferencji. Odkrycie, że powodują — demonstrując, że uwaga „rozlewa się" na przestrzennie sąsiadujące bodźce — stało się kamieniem węgielnym współczesnych badań nad uwagą.

Wersja ze strzałkami stosowana w skomputeryzowanych zadaniach (w tym Flanker Arena) została wprowadzona ze względów praktycznych: strzałki mają jednoznaczne mapowanie odpowiedzi (lewo lub prawo) bez konieczności uczenia się par litera–odpowiedź, co czyni zadanie dostępnym dla szerszych grup, w tym dzieci i grup klinicznych.

## 2. Struktura zadania

Próba w zadaniu flankera składa się ze strzałki centralnej otoczonej dwoma bodźcami po każdej stronie. Standardem są trzy warunki:

| Warunek | Bodziec | Typowy RT (młodzi dorośli) | Opis |
|---|---|---|---|
| Kongruentny (zgodny) | -> -> -> -> -> | ~420 ms | Flankers wskazują w tym samym kierunku co cel |
| Neutralny | -- -> -- | ~450 ms | Flankers nie niosą informacji kierunkowej |
| Inkongruentny (niezgodny) | <- <- -> <- <- | ~470–500 ms | Flankers wskazują w przeciwnym kierunku do celu |

Zwróć uwagę, że bezwzględne wartości RT dla zadania flankera są niższe niż dla zadania Stroopa. Wynika to z faktu, że naciśnięcie strzałki jest prostszą czynnością motoryczną niż ustne nazywanie koloru, a zadanie flankera umożliwia ogólnie szybsze odpowiedzi. Kluczową miarą jest różnica, nie wartości bezwzględne.

## 3. Efekt zgodności flankera

Podstawową miarą interferencji flankera jest:

```
Efekt zgodności flankera = RT(niezgodny) - RT(zgodny)
```

U zdrowych młodych dorosłych efekt ten wynosi typowo **20–80 ms**. Zwróć uwagę, że jest to istotnie mniej niż typowy efekt interferencji Stroopa (100–300 ms), co odzwierciedla fakt, że automatyczność czytania jest silniejsza niż przestrzenne torowanie odpowiedzi przez sąsiadujące strzałki.

Warunek neutralny pozwala wyodrębnić składowe analogiczne do projektu Stroopa:

```
Interferencja = RT(niezgodny) - RT(neutralny)
Facylitacja   = RT(neutralny) - RT(zgodny)
```

W zadaniu flankera facylitacja jest na ogół mniejsza w stosunku do interferencji niż w zadaniu Stroopa.

## 4. Dlaczego pojawia się interferencja flankera: model reflektora

Eriksen i St. James (1986) zaproponowali **model reflektora uwagi**: wizualna uwaga ma ograniczone pole skupienia, które można rozszerzać lub zawężać, ale nie można go skupić idealnie na jednym punkcie. Gdy pojawia się wyświetlenie, uwaga jest kierowana ku centrum, gdzie jest cel. Jednak reflektor nie jest idealnym okręgiem — ma miękkie krawędzie rozciągające się na otaczający obszar, gdzie znajdują się flankers.

Ponieważ flankers leżą w szerszym przestrzennym polu uwagi, są częściowo przetwarzane. Informacja kierunkowa w niezgodnym flankerze (np. strzałki skierowane w lewo) aktywuje rywalizującą odpowiedź (lewa ręka), tworząc konflikt odpowiedzi. Zanim można wybrać poprawną odpowiedź (prawa ręka), konflikt musi zostać wykryty i rozwiązany — co zajmuje czas, powodując wzrost RT.

Model stawia testowalną prognozę: wraz ze wzrostem odległości między celem a flankers efekt interferencji powinien maleć — ponieważ bardziej odległe flankers leżą dalej poza krawędzią reflektora uwagi. Ta prognoza była wielokrotnie potwierdzana (Eriksen & Eriksen, 1974; Eriksen & St. James, 1986).

## 5. Korelaty nerwowe: ACC i składowa N2

**Przednia kora zakrętu obręczy (ACC):** ACC odgrywa centralną rolę w monitorowaniu konfliktu. Gdy niezgodne flankers aktywują rywalizującą odpowiedź, ACC wykrywa konflikt i sygnalizuje korze przedczołowej konieczność zwiększenia kontroli poznawczej. Aktywacja ACC rośnie proporcjonalnie do stopnia konfliktu odpowiedzi.

**Składowa N2 w ERP:** W elektroencefalografii (EEG) N2 to ujemna składowa potencjałów wywołanych osiągająca szczyt około 200–350 ms po pojawieniu się bodźca, maksymalna w okolicach czołowo-centralnych skalpu. Niezgodne flankers wytwarzają większe amplitudy N2 niż zgodne. N2 jest powszechnie interpretowana jako nerwowy marker wykrywania konfliktu — jej latencja informuje, kiedy konflikt jest rejestrowany, a amplituda odzwierciedla natężenie konfliktu.

**Składowa P3:** Po N2 następuje P3 (szczyt ~300–600 ms), która odzwierciedla dobór odpowiedzi i aktualizację decyzji. Warunki niezgodne dają opóźnione szczyty P3, zgodnie z dodatkowym czasem potrzebnym do rozwiązania konfliktu flankera przed dokonaniem odpowiedzi.

## 6. Efekt Grattona: sekwencyjna adaptacja kontroli poznawczej

Jednym z najważniejszych odkryć dokonanych za pomocą zadania flankera jest **efekt Grattona** (Gratton, Coles & Donchin, 1992), zwany też sekwencyjnym efektem zgodności. Odkrycie: wielkość efektu zgodności flankera zależy od tego, co wydarzyło się w poprzedniej próbie.

Konkretnie:
- Po próbie kongruentnej (CC) efekt zgodności w następnej próbie jest **większy**.
- Po próbie inkongruentnej (CI) efekt zgodności w następnej próbie jest **mniejszy**.

Wynika to z faktu, że doświadczenie konfliktu w próbie niezgodnej podnosi poziom kontroli poznawczej — reflektor uwagi jest zawężany, przetwarzanie flankers jest tłumione, a kolejna próba wykazuje w efekcie mniejszą interferencję. Po próbie kongruentnej potrzeba utrzymania wysokiej kontroli jest mniejsza, więc reflektor znów się rozszerza.

Efekt Grattona demonstruje, że kontrola poznawcza nie jest stałym ustawieniem — jest dynamicznie dostosowywana próba po próbie w odpowiedzi na historię niedawnych konfliktów. Ma to implikacje dla rozumienia, jak mózg uczy się zarządzać konkurującymi informacjami w czasie rzeczywistym.

## 7. Test Sieci Uwagi (ANT)

Fan, McCandliss, Sommer, Raz i Posner (2002, *Journal of Cognitive Neuroscience*) rozszerzyli paradygmat flankera w **Test Sieci Uwagi (ANT)**, który mierzy trzy funkcjonalnie odrębne sieci uwagi:

| Sieć | Funkcja | Mierzona przez |
|---|---|---|
| Alertowanie | Osiąganie i utrzymywanie stanu wysokiej czujności | Różnica RT między próbami ostrzeżonymi i nieostrzeżonymi |
| Orientowanie | Selekcja informacji z wejścia sensorycznego | Różnica RT między poprawnymi i niepoprawnymi wskazówkami przestrzennymi |
| Kontrola wykonawcza | Rozwiązywanie konfliktu | Różnica RT między flankers niezgodnymi i zgodnymi |

ANT dostarcza trzech odrębnych wyników z jednego 20-minutowego zadania. Był stosowany w setkach badań nad rozwojem (dzieci wykazują większe wyniki kontroli wykonawczej), starzeniem (starsi dorośli wykazują wyższe koszty kontroli wykonawczej), medytacją (meditujący wykazują mniejsze koszty kontroli wykonawczej) i populacjami klinicznymi (ADHD wiąże się z dużymi wynikami kontroli wykonawczej).

Wynik kontroli wykonawczej w ANT jest bezpośrednio analogiczny do efektu zgodności flankera mierzonego w Flanker Arena.

## 8. Różnice indywidualne

**Wiek:** Dzieci poniżej 10 lat wykazują istotnie większe efekty flankera niż dorośli, co odzwierciedla długotrwały rozwój kontroli hamowania i uwagi wykonawczej (Rueda i in., 2004). Efekt zgodności maleje w ciągu dzieciństwa i adolescencji, stabilizując się we wczesnej dorosłości. U starszych dorosłych efekt znów rośnie wraz z pogarszaniem się kontroli hamowania.

**ADHD:** Osoby z ADHD wykazują większe efekty flankera niż dopasowane grupy kontrolne (Mullane i in., 2009, *Journal of Attention Disorders*), zgodnie z udokumentowanymi deficytami uwagi wykonawczej i tłumienia dystraktorów.

**Ćwiczenie:** Ogólny RT zmniejsza się z praktyką, ale efekt zgodności flankera jest bardziej odporny na redukcję niż globalna zmiana RT. Ta asymetria sugeruje, że tłumienie dystraktorów jest jakościowo różne od ogólnej szybkości odpowiedzi — można stać się szybszym bez koniecznie stawania się lepszym w ignorowaniu nieistotnych informacji.

**Presja czasowa:** Pod ścisłymi limitami czasowymi uczestnicy muszą decydować zanim proces rozwiązywania konfliktu dobiegnie końca. To powoduje więcej błędów w próbach niezgodnych i może faktycznie zmniejszyć różnicę RT między warunkami (przy jednoczesnym wzroście różnicy dokładności). Jest to kompromis szybkość–dokładność — fundamentalne ograniczenie wyników poznawczych.

## 9. Porównanie interferencji Stroopa i Flankera

Zarówno zadanie Stroopa, jak i zadanie Flankera mierzą konflikt odpowiedzi i kontrolę hamowania, ale różnią się w kilku ważnych aspektach:

| Cecha | Stroop | Flanker |
|---|---|---|
| Źródło konfliktu | Znaczenie słowa vs. kolor tuszu | Przestrzenny kierunek flankers vs. cel |
| Typowa wielkość efektu | 100–300 ms | 20–80 ms |
| Główna automatyczność | Czytanie (wysoce nadćwiczone) | Torowanie przestrzenne (częściowo automatyczne) |
| Czułość kliniczna | Płat czołowy, demencja | ADHD, rozwój u dzieci |
| Kluczowy pomiar | RT dla warunku | RT dla warunku + efekty sekwencyjne |

Obie zadania można dysocjować: niektórzy pacjenci wykazują zaburzenia wykonania w Stroopie przy stosunkowo nienaruszonym wykonaniu flankera i odwrotnie. Sugeruje to, że choć oba zadania angażują kontrolę hamowania, angażują częściowo nakładające się, ale odrębne mechanizmy nerwowe.

## 10. Analiza danych

### Zalecane kroki analizy

1. Wyklucz próby z RT < 150 ms (zbyt szybkie dla rzeczywistego przetwarzania bodźca) i RT > 1500 ms (prawdopodobnie brak uwagi ze względu na strukturę zadania).
2. Oblicz średni RT i dokładność dla każdego warunku dla każdego uczestnika.
3. Oblicz efekt zgodności flankera (RT niezgodny - RT zgodny).
4. Sprawdź kompromis szybkość–dokładność: jeśli uczestnik jest szybszy w próbach niezgodnych, ale mniej dokładny, może odpowiadać przed pełnym rozwiązaniem konfliktu (zgadywanie).
5. Dla efektów sekwencyjnych: zakoduj każdą próbę jako CC (poprzednia zgodna, bieżąca zgodna), CI, IC lub II i oblicz efekt zgodności oddzielnie dla każdego typu sekwencji.

### Typowe wartości z literatury

| Miara | Wartość | Źródło |
|---|---|---|
| RT zgodny | ~420 ms | Eriksen & Eriksen (1974); normy ANT |
| RT niezgodny | ~460–500 ms | Eriksen & Eriksen (1974); normy ANT |
| Efekt zgodności | 20–80 ms | Zakres populacyjny |
| Efekt po próbie kongruentnej | ~60–80 ms | Gratton i in. (1992) |
| Efekt po próbie inkongruentnej | ~10–30 ms | Gratton i in. (1992) |

## Kluczowe pozycje bibliograficzne

- Eriksen, B. A., & Eriksen, C. W. (1974). Effects of noise letters upon the identification of a target letter in a nonsearch task. *Perception & Psychophysics, 16*(1), 143–149.
- Eriksen, C. W., & St. James, J. D. (1986). Visual attention within and around the field of focal attention. *Perception & Psychophysics, 40*(4), 225–240.
- Gratton, G., Coles, M. G. H., & Donchin, E. (1992). Optimizing the use of information: Strategic control of activation of responses. *Journal of Experimental Psychology: General, 121*(4), 480–506.
- Fan, J., McCandliss, B. D., Sommer, T., Raz, A., & Posner, M. I. (2002). Testing the efficiency and independence of attentional networks. *Journal of Cognitive Neuroscience, 14*(3), 340–347.
- Rueda, M. R., Fan, J., McCandliss, B. D., Halparin, J. D., Gruber, D. B., Lercari, L. P., & Posner, M. I. (2004). Development of attentional networks in childhood. *Neuropsychologia, 42*(8), 1029–1040.
- Mullane, J. C., Corkum, P. V., Klein, R. M., & McLaughlin, E. (2009). Interference control in children with and without ADHD. *Journal of Attention Disorders, 13*(2), 191–200.
