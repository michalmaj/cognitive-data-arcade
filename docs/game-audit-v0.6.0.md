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
**Typ:** arcade | **Moduł:** Kognitywistyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | Wired via `make_how_to_play` w `stroop_level_scene.py`; `info.py` zwraca 3 `description_lines` w PL i EN; dodatkowo `game.py` ma wbudowaną fazę `_Phase.INSTRUCTIONS` |
| Opis lekcji | ✅ | desc_pl 111 zn., desc_en 122 zn. |
| SessionResult | ✅ | `_build_next_scene()` tworzy `SessionResult` i przekazuje do `SessionSummaryScene` z AP (`ap_per_correct`), RT min/avg/max i badge evaluation |
| Teoria | ✅ | lesson_07.py: 3 sekcje (`theory` 7 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | `_Phase.FEEDBACK`: RT w ms w kolorze pomarańczowym (poprawna) lub czerwonym (błędna); timeout wyświetla `stroop_too_slow` w czerwonym; SFX `correct`/`wrong` po każdej decyzji |

**Action items:** brak

### L08 — Flanker Task
**Typ:** arcade | **Moduł:** Kognitywistyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | Wired via `make_how_to_play` w `flanker_level_scene.py`; `info.py` zwraca 3 `description_lines` w PL i EN |
| Opis lekcji | ✅ | desc_pl 128 zn., desc_en 134 zn. |
| SessionResult | ✅ | `_build_next_scene()` tworzy `SessionResult` → `SessionSummaryScene` z AP, SP (flanker effect bonus), RT i badge evaluation; w panelu analizy dostępny `FlankerAnalysisScene` |
| Teoria | ✅ | lesson_08.py: 3 sekcje (`theory` 7 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | `_Phase.FEEDBACK`: `"OK  {rt:.0f} ms"` w zielonym lub `"X  {rt:.0f} ms"` w czerwonym; SFX `correct`/`wrong` per decyzja |

**Action items:** brak

### L09 — Go/No-Go
**Typ:** arcade | **Moduł:** Kognitywistyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | Wired via `make_how_to_play` w `gono_level_scene.py`; `info.py` zwraca 4 `description_lines` w PL i EN |
| Opis lekcji | ✅ | desc_pl 125 zn., desc_en 138 zn. |
| SessionResult | ✅ | `_build_next_scene()` tworzy `SessionResult` → `SessionSummaryScene` z AP (`ap_per_hit`), SP (d-prime bonus), RT i badge evaluation; dostępny `GoNoGoAnalysisScene` |
| Teoria | ✅ | lesson_09.py: 3 sekcje (`theory` 7 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | `_Phase.FEEDBACK`: `"OK"` w zielonym lub `"X"` w czerwonym (`fb_color` = `(39, 174, 96)`/`(231, 76, 60)`) natychmiast po każdej odpowiedzi; SFX `correct`/`wrong` |

**Action items:** brak

### L10 — N-Back
**Typ:** arcade | **Moduł:** Kognitywistyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `HowToPlayScene` (bez `make_how_to_play`) w `nback_level_scene.py`; `info.py` zwraca 4 `description_lines` w PL i EN |
| Opis lekcji | ✅ | desc_pl 119 zn., desc_en 99 zn. |
| SessionResult | ✅ | `_build_next_scene()` tworzy `SessionResult` → `SessionSummaryScene` z AP, SP (d-prime bonus dla pozycji i litery), RT i badge evaluation; dostępny `NBackAnalysisScene` |
| Teoria | ✅ | lesson_10.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ⚠️ | `_commit_trial()` gra SFX `correct`/`wrong` per próbę, ale brak fazy `FEEDBACK` — brak wizualnego symbolu OK/X; gracz słyszy wynik, ale nie widzi go |

**Action items:**
- [ ] Dodać krótką fazę `FEEDBACK` (np. 300 ms) po `RESPONSE_WINDOW` wyświetlającą "OK" w zielonym / "X" w czerwonym, zanim siatka przejdzie do ITI

### L11 — Visual Search Lab
**Typ:** lab | **Moduł:** Kognitywistyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `HowToPlayScene` w `visual_search_level_scene.py`; `info.py` zwraca 4 `description_lines` w PL i EN |
| Opis lekcji | ✅ | desc_pl 119 zn., desc_en 124 zn. |
| SessionResult | ❌ | `_build_next_scene()` → `VisualSearchAnalysisScene` → `LessonMenuScene`; brak `SessionResult`, brak AP/SP, brak badge evaluation |
| Teoria | ✅ | lesson_11.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | `_Phase.FEEDBACK`: `"OK  {rt_text}"` w `_GREEN` lub `"X  {rt_text}"` w `_RED` + SFX `correct`/`wrong` po każdej decyzji |

**Action items:**
- [ ] Dodać `SessionResult` + badge evaluation w `_build_next_scene()` (przed przekazaniem do `VisualSearchAnalysisScene`); rozważyć AP za poprawne odpowiedzi

### L12 — Cognitive Dashboard
**Typ:** lab | **Moduł:** Kognitywistyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ❌ | `game_launcher.py` zwraca `CognitiveDashboardModeScene` bezpośrednio — brak wywołania `make_how_to_play`; `mode_scene.py` nie otwiera HowToPlay; `info.py` istnieje, ale nie jest używany przy starcie |
| Opis lekcji | ✅ | desc_pl 114 zn., desc_en 108 zn. |
| SessionResult | ❌ | Brak `SessionResult` w całym `cognitive_dashboard/`; minizadania zapisują wyniki do `DashboardSession`, ale nie do `ProfileManager` — brak AP, SP, badge evaluation |
| Teoria | ✅ | lesson_12.py: 3 sekcje (`theory` 7 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | Minizadania w `mini_tasks.py` mają fazę `_Phase.FEEDBACK`: kolorowy napis "OK"/"ZA WOLNO"/"BLAD" + kolor `_GREEN`/`_RED` per próbę; dashboard wyświetla kafelki z avg RT i trafnością po zakończeniu każdego zadania |

**Action items:**
- [ ] Dodać `make_how_to_play` przy starcie (`game_launcher.py` L12) z wykorzystaniem istniejącego `info.py`
- [ ] Dodać `SessionResult` i zapis AP/SP przez `ProfileManager` po ukończeniu wszystkich 4 zadań (gdy `session.is_complete()`)
- [ ] Powiązać badge evaluation z `BadgeEngine` (podobnie jak inne gry M2)

---

## Module 3 — Statystyka

### L13 — Distribution Playground
**Typ:** lab | **Moduł:** Statystyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ⚠️ | `_make_distribution_playground()` zwraca `PausableGame` bez `make_how_to_play` — HowToPlay dostępny tylko przez pause menu; `info.py` ma 4 `description_lines` PL i EN |
| Opis lekcji | ✅ | desc_pl 133 zn., desc_en 133 zn. |
| SessionResult | ❌ | `DistributionPlaygroundScene._done` zawsze `False`, `next_scene()` zwraca `None`; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene` |
| Teoria | ✅ | lesson_13.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ⚠️ | Faza A: brak per-akcji feedback (open-ended sandbox); Faza B: `match_score` wyświetla dopasowanie w % w kolorze zielonym/pomarańczowym przy każdej zmianie suwaka — implicite; Faza C: brak per-akcji informacji correct/incorrect |

**Action items:**
- [ ] Dodać `make_how_to_play` przed `PausableGame` w `_make_distribution_playground()` (menu.py)
- [ ] Dodać end-state (np. po ukończeniu Fazy B z wynikiem >= 85%) z `SessionResult` i `SessionSummaryScene`
- [ ] Dodać wyraźny komunikat sukcesu w Fazie B po osiągnięciu progu dopasowania (aktualnie tylko "Świetnie! Dalej >>") — brak SFX

### L14 — Correlation Trap
**Typ:** lab | **Moduł:** Statystyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ⚠️ | `_make_correlation_trap()` zwraca `PausableGame` bez `make_how_to_play` — HowToPlay dostępny tylko przez pause menu; `info.py` ma 4 `description_lines` PL i EN |
| Opis lekcji | ✅ | desc_pl 128 zn., desc_en 125 zn. |
| SessionResult | ❌ | `CorrelationTrapScene._done` zawsze `False`, `next_scene()` zwraca `None`; Faza B ma wewnętrzny licznik `_correct` i ekran "summary", ale wynik nie jest zapisywany do `ProfileManager` ani `SessionResult` |
| Teoria | ✅ | lesson_14.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | Faza B (`phase_b.py`): po każdym wyborze TAK/NIE ujawnia verdyktsPanel z `_GREEN`/`_RED` etykietą ("Tak! Przyczynowość" / "Pułapka!"), wyjaśnieniem i "+10 pkt" jeśli poprawnie; Faza A/C: open-ended sandbox bez oceniania |

**Action items:**
- [ ] Dodać `make_how_to_play` przed `PausableGame` w `_make_correlation_trap()` (menu.py)
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` gdy Faza B osiąga "summary" (po przejściu wszystkich 8 scenariuszy); zapisać wynik `_correct / total` jako AP przez `ProfileManager`

### L15 — Hypothesis Arena
**Typ:** lab | **Moduł:** Statystyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ⚠️ | `_make_hypothesis_arena()` zwraca `PausableGame` bez `make_how_to_play` — HowToPlay dostępny tylko przez pause menu; `info.py` ma 4 `description_lines` PL i EN |
| Opis lekcji | ✅ | desc_pl 123 zn., desc_en 120 zn. |
| SessionResult | ❌ | `HypothesisArenaScene._done` zawsze `False`, `next_scene()` zwraca `None`; Faza B (`phase_b.py`) ma `_score` i per-scenariuszowy feedback, ale wynik nie jest przekazywany do `ProfileManager` ani `SessionResult` |
| Teoria | ✅ | lesson_15.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | Faza B (`phase_b.py`): po kliknięciu "Uruchom eksperyment" ujawnia verdykt (`_GREEN`/`_ORANGE`/`_RED` ramka) z komunikatem moc/p-value; `_feedback()` zwraca specyficzną wiadomość per wynik scenariusza natychmiast po kliknięciu |

**Action items:**
- [ ] Dodać `make_how_to_play` przed `PausableGame` w `_make_hypothesis_arena()` (menu.py)
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` po ukończeniu wszystkich 6 scenariuszy Fazy B; zapisać `_score` jako AP przez `ProfileManager`

### L16 — Prediction Slider
**Typ:** lab | **Moduł:** Statystyka

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ⚠️ | `_make_prediction_slider()` zwraca `PausableGame` bez `make_how_to_play` — HowToPlay dostępny tylko przez pause menu; `info.py` ma 4 `description_lines` PL i EN |
| Opis lekcji | ✅ | desc_pl 106 zn., desc_en 109 zn. |
| SessionResult | ❌ | `PredictionSliderScene._done` zawsze `False`, `next_scene()` zwraca `None`; Faza B (`phase_b.py`) ma `_score` (suma per-runda), ale wynik nigdy nie jest zapisywany do `ProfileManager` ani `SessionResult` |
| Teoria | ✅ | lesson_16.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | Faza B (`phase_b.py`): po kliknięciu "Zatwierdź predykcję" `_draw_verdict()` wyświetla "Wynik rundy: N / 100" w `_GREEN`/`_ORANGE`/`_RED` natychmiast; linia błędu na wykresie (zielona <= 15% błąd, czerwona > 15%) per suwak |

**Action items:**
- [ ] Dodać `make_how_to_play` przed `PausableGame` w `_make_prediction_slider()` (menu.py)
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` po ukończeniu wszystkich 5 scenariuszy Fazy B; zapisać `_score` (maks. 500) jako AP przez `ProfileManager`

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
