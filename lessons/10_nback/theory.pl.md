# Teoria — Pamiec robocza i paradygmat n-back

## 1. Kontekst historyczny

Pojecie systemu pamieci krotkotrwalej o ograniczonej pojemnosci, ktory aktywnie utrzymuje i manipuluje informacjami, zajmuje centralne miejsce w psychologii poznawczej od czasow Williama Jamesa, ktory w 1890 roku rozroznil pamiec pierwotna i wtorna. Formalne zadanie n-back zostalo wprowadzone przez **Wayne'a Kirchnera** (1958) w badaniu obciazenia pamieci krotkotrwalej kontrolerow ruchu lotniczego. Kluczowym odkryciem Kirchnera bylo to, ze przez zmiane n — liczby krokow wstecz do porownania — moze systematycznie zmieniac obciazenie pamieci bez zmiany samych bodzcow.

Paradygmat przez kilka dekad pozostawal ciekawostka laboratoryjna, az do pojawienia sie neuroobrazowania w latach 90., ktore uczynilo go konikiem roboczym neuronauki poznawczej. Jego zaleta dla badaczy fMRI jest parametryczne manipulowanie obciazeniem pamieci roboczej: n=0 (dopasowanie do stalego celu), n=1, n=2 i n=3 powoduja przewidywalnie gradientowy wzrost aktywacji grzbietowo-bocznej kory przedczolowej (dlPFC). Zadanie n-back jest obecnie jednym z najczesciej cytowanych paradygmatow eksperymentalnych w neuronauce poznawczej.

Do swiadomosci publicznej zadanie wrocilo za sprawa artykulu opublikowanego w 2008 roku w *PNAS* przez **Susanne Jaeggi** i wspolpracownikow, ktorzy twierdzili, ze trening na dual n-back poprawia inteligencje plynna — twierdzenie, ktore wywolalo jedna z najbardziej aktywnych debat w badaniach treningu poznawczego przez nastepna dekade.

## 2. Model pamieci roboczej Baddeleya

Pamiec robocza (WM) to system poznawczy odpowiedzialny za aktywne utrzymywanie i manipulowanie ograniczona iloscia informacji przez krotkie okresy czasu w sluzbie biezacych zadan. Rozni sie od pamieci krotkotrwalej tym, ze nie jest biernym magazynem, lecz aktywnym obszarem roboczym.

Najbardziej wplywowym opisem jest **wieloskladnikowy model Baddeleya** (Baddeley i Hitch, 1974; zrewidowany w Baddeley, 2000):

| Skladnik | Funkcja | Pojemnosc | Rola w n-back |
|---|---|---|---|
| Petla fonologiczna | Przechowuje i powazuje informacje werbalne/akustyczne | ~2 s mowy | Sledzenie liter w dual n-back |
| Szkicownik wzrokowo-przestrzenny | Przechowuje i manipuluje informacjami wzrokowymi i przestrzennymi | ~3–4 obiekty | Sledzenie pozycji w n-back |
| Centralny wykonawca | Kontrola uwagi; koordynacja systemow podrządnych; aktualizacja i hamowanie zawartosci WM | Ograniczona | Glowne miejsce obciazenia n-back |
| Bufor epizodyczny | Integruje informacje z systemow podrządnych i pamieci dlugookresowej w spojne epizody | ~4 chunki | Wiazanie kontekstu sekwencji |

**Petla fonologiczna** ma dwa podsklaadniki: magazyn fonologiczny (bierna slad akustyczny zanikajacy w ~2 sekundy) i artykularyjny proces powarzania (mowa wewnetrzna odswiezajaca slad). Slowa fonetycznie podobne (bat, mat, hat) trudniej zapamietac niz roznobrzmiace — **efekt podobienstwa fonologicznego** — poniewaz podobne slady koliduja w magazynie.

**Centralny wykonawca** jest najwazniejszym skladnikiem dla wynikow n-back. Wykonuje trzy kluczowe operacje: *aktualizowanie* (zastepowanie starych tresci WM nowymi informacjami), *hamowanie* (tlumienie nieistotnych lub zdezaktualizowanych informacji) i *przełaczanie* (zmiana uwagi miedzy zbiorami zadan). Wszystkie trzy sa silnie obciazone przez n-back.

## 3. Paradygmat n-back: mechanika

W standardowym zadaniu n-back:

1. Sekwencja bodzcow jest prezentowana jeden po drugim.
2. Na kazdym kroku uczestnik decyduje: **czy ten bodziec odpowiada temu sprzed n krokow?**
3. Jesli tak — odpowiada (naciska klawisz). Jesli nie — powstrzymuje sie.

Trzy jednoczesne operacje poznawcze wymagane przy kazdej probie:

- **Identyfikacja** biezacego bodzcca (przetwarzanie percepcyjne)
- **Porownanie** z pozycja przechowywaną w pamieci na pozycji n
- **Aktualizacja** bufora pamieci: usun bodziec z pozycji n+1 krokow temu, przesuń wszystkie pozostale elementy o jedna pozycje wstecz, dodaj nowy bodziec na pozycje 1

Operacja aktualizacji jest waskim gardlem. Przy n=1 utrzymujesz jeden element i ciagle aktualizujesz — latwe dla wiekszosci doroslych. Przy n=2 utrzymujesz dwuelementowy bufor i aktualizujesz po kazdym bodzczu — umiarkowanie wymagajace. Przy n=3 bufor przechowuje trzy elementy i operacja aktualizacji musi przebiegac bez gubienia porzadku — bardzo wymagajace dla wiekszosci doroslych.

**Dlaczego trudnosc rosnie nieliniowo:** kazdy przyrost n dodaje jeden element wiecej do bufora *i* jedna operacje aktualizacji na kazdym kroku. Obciazenie kombinatoryczne rosnie szybko. Ponadto dluzsze bufory zwiekszaja interferencje proaktywna — elementy z wczesniejszych prob koliduja z odtworzeniem elementu sprzed n krokow.

## 4. Typowe wskazniki wynikow

| Poziom n | Typowa trafnosc (zdrowi dorosli) | Typowe d' |
|---|---|---|
| 0-Back (dopasowanie do celu) | >95% | >3,0 |
| 1-Back | 85–95% | 2,0–3,0 |
| 2-Back | 70–85% | 1,5–2,5 |
| 3-Back | 50–70% | 0,8–1,5 |
| 4-Back | 40–55% | 0,3–0,8 |

Trafnosc ponizej 55% przy n=3 sugeruje wyniki bliskie szansy losowej i moze wskazywac, ze biezaca pojemnosc WM uczestnika nie obsluguje tego poziomu. Trafnosc powyzej 90% przy n=2 jest sygnalem, ze system adaptacyjny powinien zwiekszyc n.

Standardowy adaptacyjny n-back stosowany w badaniach (w tym ta aplikacja) celuje w **~75% trafnosci**. Gdy trafnosc rosnie powyzej ~85%, n jest zwiekszane. Gdy spada ponizej ~65%, n jest zmniejszane. Utrzymuje to uczestnika w strefie produktywnej trudnosci.

## 5. Dual n-back

Zadanie **dual n-back** jednoczesnie prezentuje dwa niezalezne strumienie bodzcow — typowo pozycje przestrzenna na siatce i sluchowa litere — i wymaga sledzenia obu jednoczesnie. Uczestnik musi udzielac odrebnych odpowiedzi dla kazdego strumienia (dopasowanie pozycji i dopasowanie litery).

Dual n-back podwaja obciazenie poznawcze, angazujac jednoczesnie szkicownik wzrokowo-przestrzenny i petle fonologiczna, oprócz nakladow centralnego wykonawcy zwiazanych z zarzadzaniem dwoma niezaleznymi buforami. Badania sugeruja, ze obciazenie dual n-back nie sumuje sie po prostu — dwa strumienie interferuja w centralnym wykonawcy, co sprawia, ze dual n-back jest nieproporcjonalnie trudniejszy niz pojedynczy n-back na tym samym poziomie.

## 6. Kontrowersje wokol treningu

### Jaeggi i in. (2008)

Jaeggi i wspolpracownicy opublikowali w *PNAS* badanie twierdzace, ze okolo 4 tygodnie codziennego treningu dual n-back (okolo 30 minut dziennie) powoduje wzrost **inteligencji plynnej** (Gf), mierzonej Matrycami Ravena — testem rozwiazywania nowych problemow, uznawanym ogolnie za trudno podatny na trening. Co kluczowe, wzrosty mialy charakter zalezny od dawki: im wiecej sesji, tym wieksza poprawa Gf. Interpretowano to jako dowod *transferu odleglego* — trening jednego zadania poprawia jakosciowo odmienna zdolnosc.

Twierdzenie przyciagnelo ogromna uwage, poniewaz inteligencja plynna byla przez dlugi czas uwazana za stabilna w trakcie doroslosci i odporna na interwencje srodowiskowe.

### Replikacje i wyniki metaanaliz

W dekadzie po Jaeggi i in. przeprowadzono dziesiatki prob replikacji. Wyniki byly rozne i sporne:

- **Transfer bliski** (poprawa w innych zadaniach WM) byl konsekwentnie obserwowany. Trening WM niezawodnie poprawia wyniki w zadaniach o podobnej strukturze do trenowanego.
- **Transfer odlegly** (poprawa inteligencji plynnej) okazal sie nieuchwytny. Kilka dobrze zasilonych badan (np. Redick i in., 2013; Shipstead i in., 2012) nie wykazalo wzrostow Gf przy niemal identycznych protokolach treningowych.
- **Melby-Lervåg i Hulme (2013)** przeprowadzili metaanalize 23 badan treningu WM. Wniosek: efekty bliskiego transferu sa solidne i trwale; efekty odleglego transferu sa nierzetelne i prawdopodobnie zerowe lub zaniedbywalnie male.

Obecny konsensus naukowy, odzwierciedlony w oswiadczeniu konsensusowym z 2018 roku podpisanym przez ponad 70 naukocow poznawczych, stanowi, ze:

1. Trening WM niezawodnie poprawia wyniki w trenowanych zadaniach i blisko zwiazanych zadaniach.
2. Trening WM nie poprawia niezawodnie inteligencji plynnej ani innych szerokich zdolnosci poznawczych.
3. Wczesniej zgloszone efekty odleglego transferu byly prawdopodobnie spowodowane artefaktami metodologicznymi (aktywne vs. pasywne grupy kontrolne, efekty oczekiwan, stronniczosc publikacji).

Komercyjny program treningowy Cogmed i podobne produkty byly szeroko reklamowane na podstawie wczesnych pozytywnych wynikow. Ich skutecznosc kliniczna dla ADHD i innych populacji pozostaje przedmiotem aktywnej debaty.

## 7. Dlaczego pojemnosc WM ma znaczenie

Mimo kontrowersji treningowych, indywidualne roznice w pojemnosci WM sa solidnie zwiazane z wazanymi wynikami:

- **Rozumienie czytanego tekstu:** Osoby z wysoka WM utrzymuja wiecej informacji podczas przetwarzania zdania, redukujac bledy sciezki ogrodowej i umozliwiajac generowanie wnioskow (Kane i Engle, 2002).
- **Rozumowanie matematyczne:** Rozwiazywanie zadan arytmetycznych i algebraicznych silnie opiera sie na WM do utrzymywania wynikow posrednich.
- **Inteligencja plynna:** Pojemnosc WM jest jednym z najsilniejszych poznawczych predyktorow wynikow w zadaniach nowego rozumowania.
- **Bladzenie mysli:** Osoby z niska WM wykazuja wiecej bladzenia mysli podczas zadan podtrzymanych, co jest wykrywalne jako gorsze wyniki specyficznie w pozycjach nastepujacych po okresach bladzenia mysli (Smallwood i in., 2004).

Te korelacje nie implikuja, ze WM *powoduje* inteligencje — zwiazek jest dwukierunkowy i mediowany przez czynniki neuronalne i genetyczne. Jednak pojemnosc WM dostarcza uzytecznego okna na architekture poznawcza lezaca u podstaw myslenia wyzszego rzedu.

## 8. Neuronalne podstawy wynikow n-back

Badania fMRI z paradygmatem n-back konsekwentnie wskazaly rdzen sieci obszarow mozgu:

**Obustronna grzbietowo-boczna kora przedczolowa (dlPFC):** Najrzetelniej aktywowany obszar. Aktywnosc wzrasta monotonicznie z n. Uwaza sie, ze dlPFC utrzymuje i manipuluje informacjami istotnymi dla celu pomimo dekoncentracji. Pacjenci z uszkodzeniami dlPFC wykazuja specyficzne uposledzenia w zadaniach n-back wzgledem dopasowanych kontroli.

**Przedni zakret obrecz (ACC):** Aktywny podczas warunkow n-back wysokiego obciazenia. ACC monitoruje konflikty miedzy konkurencyjnymi tendencjami odpowiedzi — istotne w n-back, gdy biezacy element jest podobny, ale nie identyczny z elementem sprzed n krokow (proby pozorow).

**Tylna kora ciemieniowa:** Lewa ciemieniowa dla obciazenia werbalnego (petla fonologiczna), prawa ciemieniowa dla obciazenia wzrokowo-przestrzennego. Uwaza sie, ze kora ciemieniowa dostarcza przestrzeni roboczej, w ktorej reprezentacje WM sa utrzymywane aktywne.

**Wklady mozdzku:** Mozdzek przyczynia sie do sekwencjonowania czasowego, kluczowego dla utrzymania porzadku ordynalnego elementow w buforze n-back.

Szczegolnie waznym odkryciem jest **zalezna od obciazenia dezaktywacja** **sieci domyslnego trybu** (DMN) — zestawu obszarow obejmujacego przyrodkowa kore przedczolowa, tylny zakret obrecz i zakret katowy — ktore sa aktywne podczas odpoczynku i dezaktywowane podczas poznawczo wymagajacych zadan. Wysokie obciazenie n-back powoduje silna supresje DMN; niepowodzenie supresji DMN koreluje z gorszymi wynikami zadania i bladzeniem mysli.

## 9. Proby pozorne i interferencja proaktywna

Wazna cecha metodologiczna n-back wplywajaca na wyniki sa **proby pozorne** — proby, w ktorych bodziec pasuje do elementu sprzed n+1 lub n−1 krokow (ale nie n krokow temu). Proby pozorne sa szczegolnie podatne na bledy, poniewaz uczestnik musi odrozniac prawdziwe dopasowanie (n krokow temu) od fałszywego alarmu (n±1 krokow temu). Wymaga to precyzyjnego oznaczania czasowego reprezentacji WM.

Trudnosc prob pozornych ilustruje **interferencje proaktywna**: stare tresci WM (elementy z poprzednich pozycji) koliduja z odtworzeniem elementu docelowego na pozycji n. Interferencja proaktywna wzrasta z n, poniewaz w pamieci gromadzi sie wiecej nieistotnych elementow.

## 10. Pomiar wynikow n-back: teoria detekcji sygnalu

Wyniki n-back najlepiej charakteryzuje sie przy uzyciu teorii detekcji sygnalu (SDT) — tych samych ram, ktore wprowadzono w Lekcji 09 (Go/No-Go Guard). Proby dopasowania sa "sygnalem", a proby niedopasowania "szumem".

| Wynik SDT | Znaczenie w n-back |
|---|---|
| Trafienie | Odpowiedz "dopasowanie" w prawdziwej probie dopasowania |
| Chybienie | Brak odpowiedzi w probie dopasowania |
| Falszywy alarm | Odpowiedz "dopasowanie" w probie niedopasowania |
| Prawidlowe odrzucenie | Brak odpowiedzi w probie niedopasowania |

Wzor na d' (d-prim):

```
d' = Z(wskaznik trafien) - Z(wskaznik falszywych alarmow)
```

gdzie wskaznik trafien = trafienia / lacznie prob dopasowania, a wskaznik FA = falszywe alarmy / lacznie prob niedopasowania.

d' jest preferowana miara nad surowa trafnoscia, poniewaz jest niezalezne od strategii odpowiadania. Uczestnik odpowiadajacy "dopasowanie" na niemal kazdy bodziec bedzie miec wysoki wskaznik trafien, ale takze wysoki wskaznik FA — d' prawidlowo zidentyfikuje to jako slaba dyskryminacje. Uczestnik, ktory niemal nigdy nie odpowiada, bedzie miec niski wskaznik FA, ale takze niski wskaznik trafien — d' rowniez uchwytuje to jako slaba dyskryminacje.

**Czulosc na proby pozorne:** Niektorzy badacze obliczaja odrebne d' dla prob pozornych (bodzcow pasujacych do pozycji n±1 krokow temu). Mierzy to precyzje oznaczania czasowego — czy reprezentacje WM uczestnika zawieraja dokladne informacje o porzadku ordynalnym, czy tez jedynie "wydaje sie znajome" bez niezawodnego znacznika pozycji.

## 11. Literatura

- Baddeley, A. D. (2000). The episodic buffer: a new component of working memory? *Trends in Cognitive Sciences, 4*(11), 417–423.
- Baddeley, A. D., & Hitch, G. J. (1974). Working memory. W: G. H. Bower (red.), *The Psychology of Learning and Motivation* (Tom 8, s. 47–89). Academic Press.
- Jaeggi, S. M., Buschkuehl, M., Jonides, J., & Perrig, W. J. (2008). Improving fluid intelligence with training on working memory. *Proceedings of the National Academy of Sciences, 105*(19), 6829–6833.
- Kane, M. J., & Engle, R. W. (2002). The role of prefrontal cortex in working-memory capacity, executive attention, and general fluid intelligence. *Psychonomic Bulletin & Review, 9*(4), 637–671.
- Kirchner, W. K. (1958). Age differences in short-term retention of rapidly changing information. *Journal of Experimental Psychology, 55*(4), 352–358.
- Melby-Lervåg, M., & Hulme, C. (2013). Is working memory training effective? A meta-analytic review. *Developmental Psychology, 49*(2), 270–291.
- Smallwood, J., Fishman, D. J., & Schooler, J. W. (2007). Counting the cost of an absent mind: mind wandering as an underrecognized influence on educational performance. *Psychonomic Bulletin & Review, 14*(2), 230–236.
