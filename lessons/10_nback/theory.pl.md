# Teoria — Pamięć robocza i paradygmat n-back

## 1. Kontekst historyczny

Pojęcie systemu pamięci krótkotrwałej o ograniczonej pojemności, który aktywnie utrzymuje i manipuluje informacjami, zajmuje centralne miejsce w psychologii poznawczej od czasów Williama Jamesa, który w 1890 roku rozróżnił pamięć pierwotną i wtórną. Formalne zadanie n-back zostało wprowadzone przez **Wayne'a Kirchnera** (1958) w badaniu obciążenia pamięci krótkotrwałej kontrolerów ruchu lotniczego. Kluczowym odkryciem Kirchnera było to, że przez zmianę n — liczby kroków wstecz do porównania — może systematycznie zmieniać obciążenie pamięci bez zmiany samych bodźców.

Paradygmat przez kilka dekad pozostawał ciekawostką laboratoryjną, aż do pojawienia się neuroobrazowania w latach 90., które uczyniło go koniem roboczym neuronauki poznawczej. Jego zaleta dla badaczy fMRI jest parametryczne manipulowanie obciążeniem pamięci roboczej: n=0 (dopasowanie do stałego celu), n=1, n=2 i n=3 powodują przewidywalnie gradientowy wzrost aktywacji grzbietowo-bocznej kory przedczołowej (dlPFC). Zadanie n-back jest obecnie jednym z najczęściej cytowanych paradygmatów eksperymentalnych w neuronauce poznawczej.

Do świadomości publicznej zadanie wróciło za sprawą artykułu opublikowanego w 2008 roku w *PNAS* przez **Susanne Jaeggi** i współpracowników, którzy twierdzili, że około 4 tygodnie codziennego treningu dual n-back poprawia inteligencję płynną — twierdzenie, które wywołało jedną z najbardziej aktywnych debat w badaniach treningu poznawczego przez następną dekadę.

## 2. Model pamięci roboczej Baddeleya

Pamięć robocza (WM) to system poznawczy odpowiedzialny za aktywne utrzymywanie i manipulowanie ograniczoną ilością informacji przez krótkie okresy czasu w służbie bieżących zadań. Różni się od pamięci krótkotrwałej tym, że nie jest biernym magazynem, lecz aktywnym obszarem roboczym.

Najbardziej wpływowym opisem jest **wieloskładnikowy model Baddeleya** (Baddeley i Hitch, 1974; zrewidowany w Baddeley, 2000):

| Składnik | Funkcja | Pojemność | Rola w n-back |
|---|---|---|---|
| Pętla fonologiczna | Przechowuje i powtarza informacje werbalne/akustyczne | ~2 s mowy | Śledzenie liter w dual n-back |
| Szkicownik wzrokowo-przestrzenny | Przechowuje i manipuluje informacjami wzrokowymi i przestrzennymi | ~3–4 obiekty | Śledzenie pozycji w n-back |
| Centralny wykonawca | Kontrola uwagi; koordynacja systemów podrzędnych; aktualizacja i hamowanie zawartości WM | Ograniczona | Główne miejsce obciążenia n-back |
| Bufor epizodyczny | Integruje informacje z systemów podrzędnych i pamięci długookresowej w spójne epizody | ~4 chunki | Wiązanie kontekstu sekwencji |

**Pętla fonologiczna** ma dwa podskładniki: magazyn fonologiczny (bierny ślad akustyczny zanikający w ~2 sekundy) i artykulacyjny proces powtarzania (mowa wewnętrzna odświeżająca ślad). Słowa fonetycznie podobne (bat, mat, hat) trudniej zapamiętać niż rznobrzmiące — **efekt podobieństwa fonologicznego** — ponieważ podobne ślady kolidują w magazynie.

**Centralny wykonawca** jest najważniejszym składnikiem dla wyników n-back. Wykonuje trzy kluczowe operacje: *aktualizowanie* (zastępowanie starych treści WM nowymi informacjami), *hamowanie* (tłumienie nieistotnych lub zdezaktualizowanych informacji) i *przełączanie* (zmiana uwagi między zbiorami zadań). Wszystkie trzy są silnie obciążone przez n-back.

## 3. Paradygmat n-back: mechanika

W standardowym zadaniu n-back:

1. Sekwencja bodźców jest prezentowana jeden po drugim.
2. Na każdym kroku uczestnik decyduje: **czy ten bodziec odpowiada temu sprzed n kroków?**
3. Jeśli tak — odpowiada (naciska klawisz). Jeśli nie — powstrzymuje się.

Trzy jednoczesne operacje poznawcze wymagane przy każdej próbie:

- **Identyfikacja** bieżącego bodźca (przetwarzanie percepcyjne)
- **Porównanie** z pozycją przechowywaną w pamięci na pozycji n
- **Aktualizacja** bufora pamięci: usuń bodziec z pozycji n+1 kroków temu, przesuń wszystkie pozostałe elementy o jedną pozycję wstecz, dodaj nowy bodziec na pozycję 1

Operacja aktualizacji jest wąskim gardłem. Przy n=1 utrzymujesz jeden element i ciągle aktualizujesz — łatwe dla większości dorosłych. Przy n=2 utrzymujesz dwuelementowy bufor i aktualizujesz po każdym bodźcu — umiarkowanie wymagające. Przy n=3 bufor przechowuje trzy elementy i operacja aktualizacji musi przebiegać bez gubienia porządku — bardzo wymagające dla większości dorosłych.

**Dlaczego trudność rośnie nieliniowo:** każdy przyrost n dodaje jeden element więcej do bufora *i* jedną operację aktualizacji na każdym kroku. Obciążenie kombinatoryczne rośnie szybko. Ponadto dłuższe bufory zwiększają interferencję proaktywną — elementy z wcześniejszych prób kolidują z odtworzeniem elementu sprzed n kroków.

## 4. Typowe wskaźniki wyników

| Poziom n | Typowa trafność (zdrowi dorośli) | Typowe d' |
|---|---|---|
| 0-Back (dopasowanie do celu) | >95% | >3,0 |
| 1-Back | 85–95% | 2,0–3,0 |
| 2-Back | 70–85% | 1,5–2,5 |
| 3-Back | 50–70% | 0,8–1,5 |
| 4-Back | 40–55% | 0,3–0,8 |

Trafność poniżej 55% przy n=3 sugeruje wyniki bliskie szansy losowej i może wskazywać, że bieżąca pojemność WM uczestnika nie obsługuje tego poziomu. Trafność powyżej 90% przy n=2 jest sygnałem, że system adaptacyjny powinien zwiększyć n.

Standardowy adaptacyjny n-back stosowany w badaniach (w tym ta aplikacja) celuje w **~75% trafności**. Gdy trafność rośnie powyżej ~85%, n jest zwiększane. Gdy spada poniżej ~65%, n jest zmniejszane. Utrzymuje to uczestnika w strefie produktywnej trudności.

## 5. Dual n-back

Zadanie **dual n-back** jednocześnie prezentuje dwa niezależne strumienie bodźców — typowo pozycję przestrzenną na siatce i słuchową literę — i wymaga śledzenia obu jednocześnie. Uczestnik musi udzielać odrębnych odpowiedzi dla każdego strumienia (dopasowanie pozycji i dopasowanie litery).

Dual n-back podwaja obciążenie poznawcze, angażując jednocześnie szkicownik wzrokowo-przestrzenny i pętlę fonologiczną, oprócz nakładów centralnego wykonawcy związanych z zarządzaniem dwoma niezależnymi buforami. Badania sugerują, że obciążenie dual n-back nie sumuje się po prostu — dwa strumienie interferują w centralnym wykonawcy, co sprawia, że dual n-back jest nieproporcjonalnie trudniejszy niż pojedynczy n-back na tym samym poziomie.

## 6. Kontrowersje wokół treningu

### Jaeggi i in. (2008)

Jaeggi i współpracownicy opublikowali w *PNAS* badanie twierdzące, że około 4 tygodnie codziennego treningu dual n-back (około 30 minut dziennie) powoduje wzrost **inteligencji płynnej** (Gf), mierzonej Matrycami Ravena — testem rozwiązywania nowych problemów, uznawanym ogólnie za trudno podatny na trening. Co kluczowe, wzrosty miały charakter zależny od dawki: im więcej sesji, tym większa poprawa Gf. Interpretowano to jako dowód *transferu odległego* — trening jednego zadania poprawia jakościowo odmienną zdolność.

Twierdzenie przyciągnęło ogromną uwagę, ponieważ inteligencja płynna była przez długi czas uważana za stabilną w trakcie dorosłości i odporną na interwencje środowiskowe.

### Replikacje i wyniki metaanaliz

W dekadzie po Jaeggi i in. przeprowadzono dziesiątki prób replikacji. Wyniki były różne i sporne:

- **Transfer bliski** (poprawa w innych zadaniach WM) był konsekwentnie obserwowany. Trening WM niezawodnie poprawia wyniki w zadaniach o podobnej strukturze do trenowanego.
- **Transfer odległy** (poprawa inteligencji płynnej) okazał się nieuchwytny. Kilka dobrze zasilonych badań (np. Redick i in., 2013; Shipstead i in., 2012) nie wykazało wzrostów Gf przy niemal identycznych protokołach treningowych.
- **Melby-Lervåg i Hulme (2013)** przeprowadzili metaanalizę 23 badań treningu WM. Wniosek: efekty bliskiego transferu są solidne i trwałe; efekty odległego transferu są nierzetelne i prawdopodobnie zerowe lub zaniedbywalnie małe.

Obecny konsensus naukowy, odzwierciedlony w oświadczeniu konsensusowym z 2018 roku podpisanym przez ponad 70 naukowców poznawczych, stanowi, że:

1. Trening WM niezawodnie poprawia wyniki w trenowanych zadaniach i blisko związanych zadaniach.
2. Trening WM nie poprawia niezawodnie inteligencji płynnej ani innych szerokich zdolności poznawczych.
3. Wcześniej zgłoszone efekty odległego transferu były prawdopodobnie spowodowane artefaktami metodologicznymi (aktywne vs. pasywne grupy kontrolne, efekty oczekiwań, stronniczość publikacji).

Komercyjny program treningowy Cogmed i podobne produkty były szeroko reklamowane na podstawie wczesnych pozytywnych wyników. Ich skuteczność kliniczna dla ADHD i innych populacji pozostaje przedmiotem aktywnej debaty.

## 7. Dlaczego pojemność WM ma znaczenie

Mimo kontrowersji treningowych, indywidualne różnice w pojemności WM są solidnie związane z ważnymi wynikami:

- **Rozumienie czytanego tekstu:** Osoby z wysoką WM utrzymują więcej informacji podczas przetwarzania zdania, redukując błędy ścieżki ogrodowej i umożliwiając generowanie wniosków (Kane i Engle, 2002).
- **Rozumowanie matematyczne:** Rozwiązywanie zadań arytmetycznych i algebraicznych silnie opiera się na WM do utrzymywania wyników pośrednich.
- **Inteligencja płynna:** Pojemność WM jest jednym z najsilniejszych poznawczych predyktorów wyników w zadaniach nowego rozumowania.
- **Błądzenie myśli:** Osoby z niską WM wykazują więcej błądzenia myśli podczas zadań podtrzymanych, co jest wykrywalne jako gorsze wyniki specyficznie w pozycjach następujących po okresach błądzenia myśli (Smallwood i in., 2004).

Te korelacje nie implikują, że WM *powoduje* inteligencję — związek jest dwukierunkowy i mediowany przez czynniki neuronalne i genetyczne. Jednak pojemność WM dostarcza użytecznego okna na architekturę poznawczą leżącą u podstaw myślenia wyższego rzędu.

## 8. Neuronalne podstawy wyników n-back

Badania fMRI z paradygmatem n-back konsekwentnie wskazały rdzeń sieci obszarów mózgu:

**Obustronna grzbietowo-boczna kora przedczołowa (dlPFC):** Najrzetelniej aktywowany obszar. Aktywność wzrasta monotonicznie z n. Uważa się, że dlPFC utrzymuje i manipuluje informacjami istotnymi dla celu pomimo dekoncentracji. Pacjenci z uszkodzeniami dlPFC wykazują specyficzne upośledzenia w zadaniach n-back względem dopasowanych kontroli.

**Przedni zakręt obręczy (ACC):** Aktywny podczas warunków n-back wysokiego obciążenia. ACC monitoruje konflikty między konkurencyjnymi tendencjami odpowiedzi — istotne w n-back, gdy bieżący element jest podobny, ale nie identyczny z elementem sprzed n kroków (próby pozorów).

**Tylna kora ciemieniowa:** Lewa ciemieniowa dla obciążenia werbalnego (pętla fonologiczna), prawa ciemieniowa dla obciążenia wzrokowo-przestrzennego. Uważa się, że kora ciemieniowa dostarcza przestrzeni roboczej, w której reprezentacje WM są utrzymywane aktywne.

**Wkłady móżdżku:** Móżdżek przyczynia się do sekwencjonowania czasowego, kluczowego dla utrzymania porządku ordynalnego elementów w buforze n-back.

Szczególnie ważnym odkryciem jest **zależna od obciążenia dezaktywacja** **sieci domyślnego trybu** (DMN) — zestawu obszarów obejmującego przyśrodkową korę przedczołową, tylny zakręt obręczy i zakręt kątowy — które są aktywne podczas odpoczynku i dezaktywowane podczas poznawczo wymagających zadań. Wysokie obciążenie n-back powoduje silną supresję DMN; niepowodzenie supresji DMN koreluje z gorszymi wynikami zadania i błądzeniem myśli.

## 9. Próby pozorne i interferencja proaktywna

Ważną cechą metodologiczną n-back wpływającą na wyniki są **próby pozorne** — próby, w których bodziec pasuje do elementu sprzed n+1 lub n−1 kroków (ale nie n kroków temu). Próby pozorne są szczególnie podatne na błędy, ponieważ uczestnik musi odróżniać prawdziwe dopasowanie (n kroków temu) od fałszywego alarmu (n±1 kroków temu). Wymaga to precyzyjnego oznaczania czasowego reprezentacji WM.

Trudność prób pozornych ilustruje **interferencję proaktywną**: stare treści WM (elementy z poprzednich pozycji) kolidują z odtworzeniem elementu docelowego na pozycji n. Interferencja proaktywna wzrasta z n, ponieważ w pamięci gromadzi się więcej nieistotnych elementów.

## 10. Pomiar wyników n-back: teoria detekcji sygnału

Wyniki n-back najlepiej charakteryzuje się przy użyciu teorii detekcji sygnału (SDT) — tych samych ram, które wprowadzono w Lekcji 09 (Go/No-Go Guard). Próby dopasowania są "sygnałem", a próby niedopasowania "szumem".

| Wynik SDT | Znaczenie w n-back |
|---|---|
| Trafienie | Odpowiedź "dopasowanie" w prawdziwej próbie dopasowania |
| Chybienie | Brak odpowiedzi w próbie dopasowania |
| Fałszywy alarm | Odpowiedź "dopasowanie" w próbie niedopasowania |
| Prawidłowe odrzucenie | Brak odpowiedzi w próbie niedopasowania |

Wzór na d' (d-prim):

```
d' = Z(wskaźnik trafień) - Z(wskaźnik fałszywych alarmów)
```

gdzie wskaźnik trafień = trafienia / łącznie prób dopasowania, a wskaźnik FA = fałszywe alarmy / łącznie prób niedopasowania.

d' jest preferowaną miarą nad surową trafnością, ponieważ jest niezależne od strategii odpowiadania. Uczestnik odpowiadający "dopasowanie" na niemal każdy bodziec będzie mieć wysoki wskaźnik trafień, ale także wysoki wskaźnik FA — d' prawidłowo zidentyfikuje to jako słabą dyskryminację. Uczestnik, który niemal nigdy nie odpowiada, będzie mieć niski wskaźnik FA, ale także niski wskaźnik trafień — d' również uchwytuje to jako słabą dyskryminację.

**Czułość na próby pozorne:** Niektórzy badacze obliczają odrębne d' dla prób pozornych (bodźców pasujących do pozycji n±1 kroków temu). Mierzy to precyzję oznaczania czasowego — czy reprezentacje WM uczestnika zawierają dokładne informacje o porządku ordynalnym, czy też jedynie "wydaje się znajome" bez niezawodnego znacznika pozycji.

## 11. Literatura

- Baddeley, A. D. (2000). The episodic buffer: a new component of working memory? *Trends in Cognitive Sciences, 4*(11), 417–423.
- Baddeley, A. D., & Hitch, G. J. (1974). Working memory. W: G. H. Bower (red.), *The Psychology of Learning and Motivation* (Tom 8, s. 47–89). Academic Press.
- Jaeggi, S. M., Buschkuehl, M., Jonides, J., & Perrig, W. J. (2008). Improving fluid intelligence with training on working memory. *Proceedings of the National Academy of Sciences, 105*(19), 6829–6833.
- Kane, M. J., & Engle, R. W. (2002). The role of prefrontal cortex in working-memory capacity, executive attention, and general fluid intelligence. *Psychonomic Bulletin & Review, 9*(4), 637–671.
- Kirchner, W. K. (1958). Age differences in short-term retention of rapidly changing information. *Journal of Experimental Psychology, 55*(4), 352–358.
- Melby-Lervåg, M., & Hulme, C. (2013). Is working memory training effective? A meta-analytic review. *Developmental Psychology, 49*(2), 270–291.
- Smallwood, J., Fishman, D. J., & Schooler, J. W. (2007). Counting the cost of an absent mind: mind wandering as an underrecognized influence on educational performance. *Psychonomic Bulletin & Review, 14*(2), 230–236.
