# Notatki dla prowadzącego — Brakujące wartości i wartości odstające

## Harmonogram zajęć

| Aktywność | Czas | Uwagi |
|---|---|---|
| Czytanie teorii (własnym tempem) | 30–35 min | Zalecane przed zajęciami |
| Ćwiczenia z zadaniami | 20–25 min | Dobrze sprawdzają się pary |
| Dyskusja | 20 min | Patrz wskazówki poniżej |
| **Łącznie** | **~70–80 min** | |

## Kluczowy koncept do wzmocnienia

Najważniejszą koncepcją tej lekcji jest to, że **brak danych jest sam w sobie daną**. Studenci wychowani na czystych arkuszach kalkulacyjnych często traktują komórki NaN jak przypadkowe pomyłki do usunięcia. Przykład MNAR — timeouty pojawiające się w trudnych próbach — powinien uczynić stawkę konkretną.

Zalecana sekwencja:

1. Zapytaj: „Jeśli student nie odpowiada na pytanie 7 na egzaminie, czy to coś mówi?"
2. Większość studentów odpowiada twierdząco: pytanie było pewnie trudne lub student skończył czas.
3. Zapytaj teraz: „Jeśli usuniesz to pytanie z analizy ocen, czy dokładnie przedstawiasz to, co się stało?"
4. To mapuje się bezpośrednio na próby z timeoutem w zadaniu Stroopa.

## Wskazówki do pytań dyskusyjnych

**Pytanie 1 — Czy próba z timeoutem w Stroopie jest MCAR, MAR czy MNAR?**
Oczekiwana odpowiedź: MNAR. Timeout pojawia się najczęściej w niezgodnych próbach, które z definicji są trudniejsze. Brakujący RT jest skorelowany z trudnością tej konkretnej próby — a trudność to nieobserwowana zmienna, na której nam zależy. Usuwanie wierszy zatem zaniża szacunek średniego RT w warunku niezgodnym, sztucznie zmniejszając efekt Stroopa.

**Pytanie 2 — Odpowiedź 85 ms: czy to wartość odstająca?**
To podchwytliwe pytanie z jednoznaczną odpowiedzią. 85 ms jest fizjologicznie niemożliwe jako prawdziwa reakcja na bodziec wzrokowy (minimalny czas przetwarzania wynosi ~100 ms). Prawidłowe postępowanie to wykluczenie niezależnie od z-score, niezależnie od średniej próby, niezależnie od tego, czy jest statystycznie wyjątkowe. To pokazuje, że wiedza dziedzinowa ma pierwszeństwo przed statystyką.

**Pytanie 3 — Czy zawsze należy wykluczać wartości odstające?**
Nie. Decyzja zależy od pytania badawczego. Jeśli badamy pełny rozkład odpowiedzi (w tym lapsy), wykluczenie wartości odstających usuwa właśnie badane zjawisko. Jeśli szacujemy modę rozkładu RT przy optymalnej uwadze, wykluczenie lapsów jest uzasadnione. Kluczowe jest podanie kryterium, uzasadnienie go i sprawdzenie, czy wskaźniki wykluczeń różnią się między warunkami.

## Typowe błędy rozumowania

- **„Więcej danych to zawsze lepiej, więc nigdy nic nie wykluczaj."** Kontr: uwzględnianie fizjologicznie niemożliwych wartości pogarsza estymator mierzonej wielkości. Decyzje o uwzględnieniu powinny być zasadne, a nie maksymalistyczne.
- **„Imputacja średnią jest bezpieczna, bo zachowuje średnią."** Kontr: zachowuje średnią grupową, ale systematycznie zaniża wariancję i kowariancję. W każdej analizie używającej błędów standardowych, przedziałów ufności lub korelacji imputacja średnią wprowadza systematyczne zniekształcenia.
- **„Jeśli p-wartość nie zmienia się bardzo, wartość odstająca nie była ważna."** Kontr: p-wartości zależą od wielkości próby. W dużych zbiorach danych wartość odstająca może nie przekroczyć progu istotności, ale istotnie zmienić szacunek wielkości efektu. Raportuj wielkości efektów, nie tylko p-wartości.

## Kluczowe liczby do zapamiętania

Podaj jako kartę referencyjną lub napisz na tablicy:

- RT < 100 ms → wyklucz (fizjologicznie niemożliwe)
- RT > 3 000 ms → zazwyczaj wyklucz (luka uwagowa)
- Wskaźnik braków > 10 % → wielokrotna imputacja lub metody modelowe; uzasadnij każde prostsze podejście
- Wskaźniki wykluczeń różniące się między warunkami o > 2–3 % → zbadaj przed kontynuowaniem

## Powiązanie z kolejnymi lekcjami

Lekcja 06 (EDA) opiera się bezpośrednio na oczyszczonym zbiorze danych. Prowadzący powinien zachęcić studentów do ukończenia kroków wykluczania/czyszczenia w Zadaniach Lekcji 05 *przed* sesją EDA, tak aby Lekcja 06 mogła zacząć się od danych gotowych do analizy. Kontrast między surowymi i oczyszczonymi histogramami to jedna z najbardziej wizualnie skutecznych demonstracji w kursie.
