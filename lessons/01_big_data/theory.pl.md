# Teoria — Big Data w Kognitywistyce

## 1. Czym jest Big Data?

Big Data to zbiory danych o tak dużej objętości i złożoności, że tradycyjne narzędzia do przetwarzania danych nie są w stanie ich obsłużyć. Trzy właściwości — często nazywane **trzema V** — definiują pojęcie Big Data:

- **Wolumen (Volume):** Ogromna ilość danych. Jedna sesja fMRI generuje kilka gigabajtów surowego sygnału; Human Connectome Project przechowuje dane ponad 1 200 uczestników, zajmując łącznie kilka terabajtów.
- **Prędkość (Velocity):** Szybkość powstawania danych. Urządzenia do śledzenia wzroku rejestrują pozycję spojrzenia z częstotliwością 250–1 000 próbek na sekundę. Wzmacniacze EEG strumieniują setki kanałów z prędkością nawet 10 000 Hz.
- **Różnorodność (Variety):** Zróżnicowanie typów danych. Kognitywistyka łączy obrazy mózgu, logi behawioralne, nagrania mowy, sygnały fizjologiczne i elektroniczne rekordy medyczne — często w ramach jednego badania.

## 2. Zarys historyczny

Pomiar procesów poznawczych za pomocą danych zapoczątkował **Franciscus Donders** w 1868 roku, odejmując czas prostej reakcji od czasu reakcji wyboru w celu oszacowania czasu trwania decyzji umysłowej — to pierwsze udokumentowane zastosowanie logiki odejmowania do danych behawioralnych.

Pod koniec XX wieku pojawiły się projekty wielkoskalowego neuroobrazowania. Inicjatywy takie jak **Human Connectome Project** (2010) i **OpenNeuro** (2017) po raz pierwszy udostępniły publicznie wielogigabajtowe zbiory danych mózgowych, umożliwiając badaczom na całym świecie zadawanie pytań, na które żadne pojedyncze laboratorium nie mogłoby samodzielnie odpowiedzieć.

Obecna dekada rozszerza gromadzenie danych poza laboratorium. **Cyfrowa fenotypizacja** — ciągły, pasywny pomiar zachowania za pomocą smartfonów — generuje strumienie współrzędnych GPS, odczytów akcelerometru i logów interakcji korelujących ze stanem zdrowia psychicznego w skali populacji.

## 3. Kluczowe otwarte zbiory danych w kognitywistyce

**Human Connectome Project (HCP)**
Dane strukturalnego i funkcjonalnego MRI od 1 200 zdrowych dorosłych, zebrane w wielu ośrodkach. Jeden z największych i starannie opracowanych zbiorów danych neuroobrazowania, stosowany do mapowania architektury sieci ludzkiego mózgu.

**OpenNeuro**
Publiczne repozytorium tysięcy zbiorów danych neuroobrazowania (fMRI, EEG, MEG), udostępnianych przez badaczy z całego świata. Dane są dostępne do pobrania na otwartych licencjach, umożliwiając analizę wtórną bez konieczności zbierania nowych danych.

**CHILDES Corpus**
Wielonarodowy zbiór transkrybowanych nagrań mowy dzieci obejmujący dziesiątki języków i etapów rozwojowych. Podstawowy zasób dla badań obliczeniowych i empirycznych nad przyswajaniem języka.

**UK Biobank**
Dane medyczne i genetyczne 500 000 dorosłych mieszkańców Wielkiej Brytanii, zbierane od 2006 roku. Obejmują neuroobrazowanie, oceny poznawcze, pomiary fizyczne i sekwencje genomowe — umożliwiając wielkoskalowe badania starzenia się mózgu i ryzyka psychiatrycznego.

## 4. Dlaczego skala ma znaczenie

Małe próby ograniczają pytania, jakie mogą zadawać badacze. Badanie z 30 uczestnikami pozwala wykryć jedynie duże efekty; subtelne zjawiska — takie jak zależność między jakością snu a konsolidacją pamięci — wymagają setek lub tysięcy obserwacji, by osiągnąć wiarygodność statystyczną.

Duże zbiory danych przesuwają granicę tego, co jest możliwe do odkrycia. Badanie ABCD (11 800 dzieci obserwowanych podłużnie) ujawniło trajektorie rozwojowe niewidoczne dla wcześniejszych, mniejszych kohort. Analizy UK Biobank zidentyfikowały warianty genetyczne związane ze zdolnościami poznawczymi, których żadne poprzednie badanie nie miało wystarczającej mocy, by wykryć.

Skala niesie też nowe obowiązki metodologiczne: przy wystarczającej liczbie danych pozorne korelacje stają się statystycznie istotne. Badacze pracujący z Big Data muszą stosować rygorystyczną korektę na wielokrotne porównania i prerejestracją, aby uniknąć fałszywych odkryć.
