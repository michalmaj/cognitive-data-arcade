# Game Quality Audit — v0.6.0

_Generated: 2026-06-23. Legend: ✅ OK · ⚠️ partial/unclear · ❌ missing._

---

## Summary

_To be filled after all sections are complete._

| Wymiar | ✅ | ⚠️ | ❌ |
|---|---|---|---|
| Instrukcje | — | — | — |
| Opis lekcji | — | — | — |
| SessionResult | — | — | — |
| Teoria | — | — | — |
| Feedback w trakcie | — | — | — |

---

## Module 1 — Dane i Podstawy

### L01 — Big Data Map
**Typ:** lab | **Moduł:** Dane i Podstawy

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | Wired via `make_how_to_play`; `info.py` zwraca 3 `description_lines` w PL i EN |
| Opis lekcji | ✅ | desc_pl 120 zn., desc_en 130 zn. |
| SessionResult | ❌ | Brak end-state — `_done` wyzwala się przy nawigacji do lekcji, nie po zakończeniu eksploracji; brak score/summary |
| Teoria | ✅ | lesson_01.py: 3 sekcje (`theory` 8 pozycji, `notes` 4, `tasks` 3), treść niepusta |
| Feedback w trakcie | ⚠️ | Klik węzła gra `navigate` SFX i podświetla połączone węzły, ale brak informacji correct/incorrect — to eksplorator, nie quiz |

**Action items:**
- [ ] Dodać podsumowanie sesji (ile węzłów odwiedzono, czas eksploracji, liczba otwartych lekcji)
- [ ] Rozważyć lekki feedback wizualny przy wejściu do lekcji (np. węzeł oznaczony jako "odwiedzony")

### L02 — Reaction Time Lab
**Typ:** arcade | **Moduł:** Dane i Podstawy

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | Wired via `make_how_to_play`; `info.py` zwraca 3 `description_lines` w PL i EN |
| Opis lekcji | ✅ | desc_pl 131 zn., desc_en 136 zn. |
| SessionResult | ✅ | `_build_next_scene()` tworzy `SessionResult` i przekazuje do `SessionSummaryScene` z AP, RT min/avg/max i badge evaluation |
| Teoria | ✅ | lesson_02.py: 3 sekcje (`theory` 8 pozycji, `notes` 4, `tasks` 3), treść niepusta |
| Feedback w trakcie | ✅ | `_Phase.FEEDBACK`: RT w ms w kolorze pomarańczowym (poprawna) lub tekst "too slow" w czerwonym; early press wyświetla ostrzeżenie w czerwonym w czasie rzeczywistym |

**Action items:** brak

### L03 — Event Log Detective
**Typ:** puzzle | **Moduł:** Dane i Podstawy

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `info.py` istnieje z 4 `description_lines` PL i EN; `HowToPlayScene` uruchamiana przez `_launch()` w `EventLogLevelScene` (nie via `game_launcher` bezpośrednio) |
| Opis lekcji | ✅ | desc_pl 117 zn., desc_en 129 zn. |
| SessionResult | ⚠️ | Ekran REPORT pokazuje `correct/total/pts` jako tekst, ale nie używa `SessionResult` ani `SessionSummaryScene`; wychodzi przez `_go_level_scene()` z powrotem do level-select — brak AP, brak badge evaluation |
| Teoria | ✅ | lesson_03.py: 3 sekcje (`theory` 9 pozycji, `notes` 4, `tasks` 3), treść niepusta |
| Feedback w trakcie | ✅ | Per-decyzja: popup ma zieloną/pomarańczową ramkę i kolorowy tytuł (`_GREEN` = poprawne, `_ACCENT` = błędne) natychmiast po wyborze opcji |

**Action items:**
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` do ekranu raportu (AP, badge evaluation)
- [ ] Zarejestrować wynik w `ProfileManager` (obecnie wynik jest tylko wyświetlany, nie zapisywany)

### L04 — Data Quality Lab
**Typ:** lab | **Moduł:** Dane i Podstawy

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ⚠️ | Wired z `get_game_info` (3 `description_lines` PL i EN), ale `game_launcher` nie używa `make_how_to_play` — ekran HowToPlay dostępny tylko przez pause menu, nie przy starcie gry |
| Opis lekcji | ✅ | desc_pl 118 zn., desc_en 123 zn. |
| SessionResult | ❌ | Faza REPORT wyświetla raport, ale `_done` **nigdy** nie jest ustawiany na `True`; `_handle_report` to `pass` — gra utknęła na ekranie raportu bez możliwości wyjścia; brak `SessionResult` / `SessionSummaryScene` |
| Teoria | ✅ | lesson_04.py: 3 sekcje (`theory` 14 pozycji, `notes` 6, `tasks` 6), treść niepusta |
| Feedback w trakcie | ✅ | Identyfikacja: kolorowy tekst wskazówki (zielony=poprawna flaga, czerwony=fałszywa flaga) z timerem; naprawa: zielony/pomarańczowy/czerwony tekst z czasowym wyświetlaniem po każdej decyzji |

**Action items:**
- [ ] Naprawić krytyczny bug: `_handle_report` jest `pass` i `_done` nigdy nie = True — gra utknięta na REPORT; dodać obsługę klawisza (ENTER/ESC) i ustawić `self._done = True`
- [ ] Dodać `SessionResult` + `SessionSummaryScene` po fazie REPORT
- [ ] Dodać `make_how_to_play` przy starcie gry w `game_launcher.py` (L04)

### L06 — EDA Sandbox
**Typ:** lab | **Moduł:** Dane i Podstawy

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | Wired via `make_how_to_play`; `info.py` zwraca 3 `description_lines` w PL i EN |
| Opis lekcji | ✅ | desc_pl 115 zn., desc_en 126 zn. |
| SessionResult | ❌ | `is_done()` zwraca zawsze `False` — brak end-state, brak score, brak `SessionResult`; otwarta piaskownica bez zakończenia sesji |
| Teoria | ✅ | lesson_06.py: 3 sekcje (`theory` 8 pozycji, `notes` 3, `tasks` 3), treść niepusta |
| Feedback w trakcie | ⚠️ | Po GENERATE: wykresy i statystyki aktualizują się natychmiast (implicitny feedback), ale brak wyraźnego per-akcji wskaźnika correct/incorrect ani SFX — open-ended lab bez oceniania |

**Action items:**
- [ ] Dodać opcjonalne podsumowanie sesji (liczba generacji, najniższe p-value, hipoteza vs wynik)
- [ ] Rozważyć feedback dźwiękowy przy GENERATE (krótki klik/SFX dla potwierdzenia akcji)

---

## Module 2 — Kognitywistyka

### L07 — Stroop Challenge
_TODO_

### L08 — Flanker Task
_TODO_

### L09 — Go/No-Go
_TODO_

### L10 — N-Back
_TODO_

### L11 — Visual Search Lab
_TODO_

### L12 — Cognitive Dashboard
_TODO_

---

## Module 3 — Statystyka

### L13 — Distribution Playground
_TODO_

### L14 — Correlation Trap
_TODO_

### L15 — Hypothesis Arena
_TODO_

### L16 — Prediction Slider
_TODO_

---

## Module 4 — Machine Learning

### L17 — Feature Hunter
_TODO_

### L18 — Classifier Battle
_TODO_

### L19 — Overfitting Monster
_TODO_

### L20 — Anomaly Alert
_TODO_

---

## Module 5 — NLP

### L21 — Text Tokenizer Lab
_TODO_

### L22 — Word Weight Factory
_TODO_

### L23 — Emotion Classifier
_TODO_

### L24 — Semantic Space Explorer
_TODO_

### L25 — Topic Detective
_TODO_

### L26 — Human vs Model
_TODO_

---

## Module 6 — Sieci i Etyka

### L27 — Social Network Simulator
_TODO_

### L28 — Misinformation Spread
_TODO_

### L29 — Recommendation Bubble
_TODO_

### L30 — Bias Blind Spot
_TODO_

### L31 — You Were the Dataset
_TODO_

### L32 — The Architect's Trial
_TODO_
