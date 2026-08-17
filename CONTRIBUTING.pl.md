# Wkład w projekt Cognitive Data Arcade

## Cele wersji beta

Bieżącym celem stabilizacji jest wydanie wersji beta nadającej się do użytku na zajęciach **10 października 2026 r.**

Celem nie jest maksymalizacja liczby zmienionych linii kodu. Celem jest uczynienie projektu:

- **stabilnym** — bez crashów P0, blokad nawigacji ani utraty danych,
- **odpowiedzialnym naukowo** — bez niepopartych norm, bez języka diagnostycznego dla krótkich zadań behawioralnych,
- **użytecznym dydaktycznie** — pojęcia wyjaśnione klarownie i z odpowiednią niepewnością,
- **przejrzystym w kwestii lokalnych danych** — studenci wiedzą, co jest przechowywane i jak to usunąć,
- **łatwiejszym w utrzymaniu** — ścieżki uruchamiania, ścieżki danych i metadane lekcji są skonsolidowane,
- **przewidywalnym do testowania i pakowania** — CI działa niezawodnie; spakowana aplikacja uruchamia się z czystego katalogu.

### Jawnie przesunięte poza beta

To są poprawne ulepszenia, które nie będą blokować wydania beta:

- pełna migracja treści lekcji do Markdown lub YAML,
- typowanie całej warstwy UI Pygame,
- eliminacja wszystkich testów dotykających prywatnych składowych,
- nowe gry lub moduły,
- refaktory kosmetyczne i przeprojektowania wizualne,
- ogólne abstrakcje storage bez konkretnej korzyści dla beta.

W razie presji harmonogramu: najpierw odcinamy te elementy — nigdy poprawności naukowej ani przejrzystości prywatności.
