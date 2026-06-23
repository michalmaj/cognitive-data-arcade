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
**Typ:** arcade | **Moduł:** Machine Learning

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ⚠️ | `_make_feature_hunter()` w menu.py zwraca `PausableGame` bez `make_how_to_play` — HowToPlay dostępny tylko przez pause menu; `info.py` ma 3 `description_lines` PL i EN; brak dedykowanego ekranu intro |
| Opis lekcji | ✅ | desc_pl 125 zn., desc_en 137 zn. |
| SessionResult | ❌ | `PhaseCScene` wyświetla wewnętrzne "Wyniki sesji" i przyciski "Zagraj ponownie" → `PhaseAScene`; `game.py` `next_scene()` zwraca `None` na końcu; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene` |
| Teoria | ✅ | lesson_17.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | Stan "revealed" w `PhaseBScene._draw_reveal_overlays()`: zielona/czerwona ramka + "OK"/"X" + delta accuracy (pp) per karta natychmiast po kliknięciu "Zatwierdź"; `_draw_reveal_summary()`: wynik rundy w kolorze zielonym/pomarańczowym/czerwonym |

**Action items:**
- [ ] Dodać `make_how_to_play` przed `PausableGame` w `_make_feature_hunter()` (menu.py) lub dodać `PhaseIntroScene` z instrukcjami analogicznie do L18/L19/L20
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` w `PhaseCScene` po wyświetleniu wyników sesji; zapisać `session_score` jako AP przez `ProfileManager`

### L18 — Classifier Battle
**Typ:** lab | **Moduł:** Machine Learning

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `ClassifierBattleScene` startuje od `PhaseIntroScene` z 6 liniami instrukcji PL; `info.py` ma 3 `description_lines` PL i EN dostępne przez pause menu |
| Opis lekcji | ✅ | desc_pl 130 zn., desc_en 108 zn. |
| SessionResult | ❌ | `PhaseSessionResultScene` wyświetla wyniki i przycisk "Zagraj ponownie" → `PhaseIntroScene`; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene`; `game.py` `next_scene()` zwraca `None` |
| Teoria | ✅ | lesson_18.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ⚠️ | `PhaseRoundResultScene` pokazuje słupki dokładności (Ty vs KNN/liniowy/drzewo) po każdej rundzie; brak per-kroku live feedback podczas rysowania granicy — gra opiera się na decyzji graficznej, nie per-decyzja |

**Action items:**
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` w `PhaseSessionResultScene._advance()` po ukończeniu 5 rund; zapisać `session_score` jako AP przez `ProfileManager`

### L19 — Overfitting Monster
**Typ:** lab | **Moduł:** Machine Learning

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `OverfittingMonsterScene` startuje od `PhaseIntroScene` z 8 liniami instrukcji PL; `info.py` ma 3 `description_lines` PL i EN dostępne przez pause menu |
| Opis lekcji | ✅ | desc_pl 114 zn., desc_en 119 zn. |
| SessionResult | ❌ | `PhaseSessionResultScene` wyświetla wykres + tabelę + "Zagraj ponownie" → `PhaseIntroScene`; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene`; `game.py` `next_scene()` zwraca `None` |
| Teoria | ✅ | lesson_19.py: 3 sekcje (`theory` 6 pozycji, `notes` 3, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ⚠️ | `PhaseRoundResultScene` pokazuje train/test accuracy, gap w pp i gwiazdki ASCII (xxx/xx./x..) per runda; brak live per-suwak feedback poprawny/błędny — wynik widoczny dopiero po zatwierdzeniu rundy |

**Action items:**
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` w `PhaseSessionResultScene._advance()` po ukończeniu 5 rund; zapisać `session_score` jako AP przez `ProfileManager`

### L20 — Anomaly Alert
**Typ:** lab | **Moduł:** Machine Learning

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `AnomalyAlertScene` startuje od `PhaseIntroScene` z 9 liniami instrukcji PL (scoring, PPM hint, limity czasowe); `info.py` ma 3 `description_lines` PL i EN przez pause menu |
| Opis lekcji | ✅ | desc_pl 130 zn., desc_en 120 zn. |
| SessionResult | ❌ | `PhaseSessionResultScene` wyświetla wykres słupkowy + tabelę + rangę (Zloto/Srebro/Braz) + "Zagraj ponownie"; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene`; `game.py` `next_scene()` zwraca `None` |
| Teoria | ✅ | lesson_20.py: 3 sekcje (`theory` 6 pozycji, `notes` 2, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | Live panel w `PhaseRoundScene` aktualizuje `+{found_preview * 20} pkt (trafione)` w `_GREEN` i `-{fp_preview * 5} pkt (alarmy)` w `_RED` przy każdym kliknięciu LPM; zaznaczony punkt dostaje pomarańczowy pierścień natychmiast |

**Action items:**
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` w `PhaseSessionResultScene._replay()` po zakończeniu 6 rund; zapisać `_total` jako AP przez `ProfileManager`

---

## Module 5 — NLP

### L21 — Text Tokenizer Lab
**Typ:** lab | **Moduł:** NLP

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ⚠️ | `_make_text_tokenizer()` zwraca `PausableGame` bez `make_how_to_play` — HowToPlay dostępny tylko przez pause menu; `info.py` ma 3 `description_lines` PL i EN |
| Opis lekcji | ✅ | desc_pl 104 zn., desc_en 111 zn. |
| SessionResult | ❌ | `TextTokenizerLabScene._done` zawsze `False`, `next_scene()` zwraca `None`; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene` — otwarta piaskownica bez end-state |
| Teoria | ✅ | lesson_21.py: 3 sekcje (`theory` 7 pozycji, `notes` 2, `tasks` 4), treść niepusta w PL i EN |
| Feedback w trakcie | ⚠️ | Open-ended sandbox bez decyzji do oceniania — zmiany parametrów aktualizują tabelę tokenów i wykres częstości natychmiast (implicitny feedback), ale brak wskaźnika correct/incorrect |

**Action items:**
- [ ] Dodać `make_how_to_play` przed `PausableGame` w `_make_text_tokenizer()` (menu.py) z wykorzystaniem istniejącego `info.py`
- [ ] Dodać opcjonalne podsumowanie sesji (liczba tokenów, rozmiar słownika po preprocessing, top n-gram) z `SessionResult` i `SessionSummaryScene`

### L22 — Word Weight Factory
**Typ:** lab | **Moduł:** NLP

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ⚠️ | `_make_word_weight_factory()` zwraca `PausableGame` bez `make_how_to_play` — HowToPlay dostępny tylko przez pause menu; `info.py` ma 3 `description_lines` PL i EN |
| Opis lekcji | ✅ | desc_pl 117 zn., desc_en 114 zn. |
| SessionResult | ❌ | `WordWeightFactoryScene._done` zawsze `False`, `next_scene()` zwraca `None`; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene` — otwarta piaskownica bez end-state |
| Teoria | ✅ | lesson_22.py: 3 sekcje (`theory` 5 pozycji, `notes` 2, `tasks` 4), treść niepusta w PL i EN |
| Feedback w trakcie | ⚠️ | Open-ended sandbox bez decyzji do oceniania — zmiana korpusu i preprocessing aktualizuje macierz BoW/TF-IDF natychmiast (implicitny feedback), ale brak wskaźnika correct/incorrect |

**Action items:**
- [ ] Dodać `make_how_to_play` przed `PausableGame` w `_make_word_weight_factory()` (menu.py) z wykorzystaniem istniejącego `info.py`
- [ ] Dodać opcjonalne podsumowanie sesji (top-5 tokenów TF-IDF, rozmiar słownika) z `SessionResult` i `SessionSummaryScene`

### L23 — Emotion Classifier
**Typ:** lab | **Moduł:** NLP

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `EmotionClassifierScene` startuje od `PhaseIntroScene` z 10 liniami instrukcji PL (LPM/PPM, panel leksykonu, wskazówka PPM, liczba rund) |
| Opis lekcji | ✅ | desc_pl 108 zn., desc_en 121 zn. |
| SessionResult | ❌ | `PhaseSessionResultScene._advance()` → `PhaseIntroScene()`; `game.py` `next_scene()` zwraca zawsze `None`; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene` |
| Teoria | ✅ | lesson_23.py: 3 sekcje (`theory` 6 pozycji, `notes` 2, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | `PhaseRoundResultScene` wyświetla 3 pola werdyktu (Leksykon / Prawdziwy / Ty) w `_GREEN`/`_RED`/`_PURPLE` + punkty (correct_pts, wrong_pts, beat_bonus, speed_bonus) natychmiast po kliknięciu ZATWIERDŹ |

**Action items:**
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` w `PhaseSessionResultScene._advance()` po ukończeniu 8 rund; zapisać `session_score` jako AP przez `ProfileManager`

### L24 — Semantic Space Explorer
**Typ:** lab | **Moduł:** NLP

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `SemanticSpaceScene` startuje od `PhaseIntroScene` z 3 slajdami (co to embedding, klastry, zadania) w PL |
| Opis lekcji | ✅ | desc_pl 105 zn., desc_en 106 zn. |
| SessionResult | ❌ | `PhaseResultScene._advance()` → `PhaseIntroScene()`; `game.py` `next_scene()` zwraca zawsze `None`; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene` |
| Teoria | ✅ | lesson_24.py: 3 sekcje (`theory` 6 pozycji, `notes` 2, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ⚠️ | `PhaseMissionScene._submit()` przechodzi natychmiast do następnej misji bez fazy feedback — brak wizualnego reveal correct/incorrect; wybrany węzeł zielenieje podczas wyboru, ale nie ma podsumowania tury (wynik +N pkt) przed przejściem do kolejnej misji |

**Action items:**
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` w `PhaseResultScene._advance()` po ukończeniu 8 misji; zapisać `session_score` jako AP przez `ProfileManager`
- [ ] Dodać krótką fazę `PhaseMissionResultScene` (np. 1 s) po `_submit()` pokazującą "Poprawnie! +N pkt" / "Blad! 0 pkt" w GREEN/RED przed przejściem do kolejnej misji

### L25 — Topic Detective
**Typ:** lab | **Moduł:** NLP

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `TopicDetectiveScene` startuje od `PhaseIntroScene` z 3 slajdami (LDA, odcisk palca, mieszanina) w PL |
| Opis lekcji | ✅ | desc_pl 113 zn., desc_en 102 zn. |
| SessionResult | ❌ | `PhaseResultScene._advance()` → `PhaseIntroScene()`; `game.py` `next_scene()` zwraca zawsze `None`; brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene` |
| Teoria | ✅ | lesson_25.py: 3 sekcje (`theory` 6 pozycji, `notes` 2, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | `PhaseMissionScene._draw_left_assign_doc()` wyświetla "Poprawnie!" w `_GREEN` lub "Blad -- dominuje: X" w `_RED` natychmiast po wyborze; misje intruder i name_topic kończą się natychmiast z wynikiem |

**Action items:**
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` w `PhaseResultScene._advance()` po ukończeniu 8 misji; zapisać `session_score` jako AP przez `ProfileManager`

### L26 — Human vs Model Challenge
**Typ:** arcade | **Moduł:** NLP

| Wymiar | Status | Uwagi |
|---|---|---|
| Instrukcje (HowToPlay) | ✅ | `HumanVsModelScene` startuje od `PhaseIntroScene` z 3 slajdami (co robi model, kiedy AI zawodzi, misja) w PL |
| Opis lekcji | ✅ | desc_pl 122 zn., desc_en 123 zn. |
| SessionResult | ❌ | `PhaseResultScene` ("Menu" klawisz) ustawia `_next = None` i `_done = True` — gra kończy sie czysto, ale brak `SessionResult`, `complete_lesson` ani `SessionSummaryScene`; `game.py` `next_scene()` zwraca zawsze `None` |
| Teoria | ✅ | lesson_26.py: 3 sekcje (`theory` 6 pozycji, `notes` 2, `tasks` 3), treść niepusta w PL i EN |
| Feedback w trakcie | ✅ | Wszystkie 3 fazy (classify, detect, complete) mają stan `"reveal"` po wyborze: wybrany przycisk zielony (`_GREEN`) gdy poprawny lub czerwony (`_RED`) gdy błędny + `+N pkt` w zielonym natychmiast po odpowiedzi |

**Action items:**
- [ ] Podpiąć `SessionResult` + `SessionSummaryScene` w `PhaseResultScene` po kliknięciu "Menu"; zapisać `session_score` jako AP przez `ProfileManager` (już jest zliczane: `session_score` i `beat_ai_count`)

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
