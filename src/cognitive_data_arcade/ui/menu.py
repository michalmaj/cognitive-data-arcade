from __future__ import annotations

from pathlib import Path

import pygame
from cognitive_data_arcade.engine.fonts import get_font, get_font_medium

from cognitive_data_arcade.engine import audio
from cognitive_data_arcade.engine.badges import (
    _MODULE_BADGES,
    load_badge_icon,
    module_complete,
)
from cognitive_data_arcade.engine.i18n import Strings, get_strings
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.engine.scrollbar import ScrollBar
from cognitive_data_arcade.profile.manager import ProfileManager

# ── Layout ──────────────────────────────────────────────────────────────────
_W, _H = 1024, 640
_TOPBAR_H = 56
_HINTBAR_H = 28
_SIDEBAR_W = 340
_SIDEBAR_H = _H - _TOPBAR_H - _HINTBAR_H  # 556
_PANEL_X = _SIDEBAR_W + 1  # 341
_PANEL_W = _W - _PANEL_X  # 683
_SB_TRACK_W = 4
_SB_X = _SIDEBAR_W - _SB_TRACK_W - 2  # 334

# ── Palette ─────────────────────────────────────────────────────────────────
_C_BG = (13, 15, 26)
_C_SURFACE = (22, 24, 40)
_C_SURFACE2 = (30, 32, 56)
_C_ACCENT = (99, 102, 241)
_C_ACCENT_LIGHT = (129, 140, 248)
_C_ACCENT_BG = (20, 22, 52)
_C_HOVER_BG = (19, 21, 34)
_C_TEXT = (240, 241, 255)
_C_TEXT_DIM = (90, 96, 144)
_C_TEXT_DARK = (61, 64, 96)
_C_TEXT_XDARK = (45, 48, 82)

_TYPE_COLORS: dict[str, tuple[int, int, int]] = {
    "arcade": _C_ACCENT,
    "lab": (34, 211, 238),
    "puzzle": (251, 191, 36),
}
_C_DONE = (74, 222, 128)

# ── Lesson catalogue ──────────────────────────────────────────────────────────
_LESSON_DATA: list[dict] = [
    # ── Module 1 ──
    {
        "num": 1,
        "name": "Big Data in Cognitive Science",
        "type": "lab",
        "desc_pl": (
            "Skąd pochodzi big data w nauce kognitywnej?\n"
            "Odkryj, jak dane z tysięcy uczestników\n"
            "rozkładają się i co nam o nich mówią."
        ),
        "desc_en": (
            "Where does cognitive big data come from?\n"
            "Explore how data from thousands of participants\n"
            "distributes and what patterns it reveals."
        ),
    },
    {
        "num": 2,
        "name": "Reaction Time Lab",
        "type": "arcade",
        "desc_pl": (
            "Jak szybko reagujesz na bodziec wizualny?\n"
            "Naciśnij SPACJĘ gdy zaświeci kółko - mierzysz\n"
            "czas reakcji, kluczową zmienną w badaniach."
        ),
        "desc_en": (
            "How fast do you react to a visual stimulus?\n"
            "Press SPACE when the circle lights up and measure\n"
            "reaction time, a key variable in research."
        ),
    },
    {
        "num": 3,
        "name": "Event Log Detective",
        "type": "puzzle",
        "desc_pl": (
            "Detektyw danych: zbadaj zdarzenia w logu\n"
            "eksperymentu i wykryj co poszło nie tak.\n"
            "Poznaj formaty danych w psychologii."
        ),
        "desc_en": (
            "Data detective: investigate events in an\n"
            "experiment log and find what went wrong.\n"
            "Learn data formats used in psychology research."
        ),
    },
    {
        "num": 4,
        "name": "Data Quality Lab",
        "type": "lab",
        "desc_pl": (
            "Czy Twoje dane są gotowe do analizy?\n"
            "Wykryj błędy, wartości odstające i braki\n"
            "w surowym zbiorze danych z eksperymentu."
        ),
        "desc_en": (
            "Are your data ready for analysis?\n"
            "Detect errors, outliers and missing values\n"
            "in a raw dataset from a psychology experiment."
        ),
    },
    {
        "num": 6,
        "name": "EDA Sandbox",
        "type": "lab",
        "desc_pl": (
            "Zanim uruchomisz model - poznaj swoje dane.\n"
            "Eksploruj rozkłady, korelacje i wzorce\n"
            "w interaktywnej piaskownicy EDA."
        ),
        "desc_en": (
            "Before running a model - understand your data.\n"
            "Explore distributions, correlations and patterns\n"
            "in an interactive EDA sandbox."
        ),
    },
    # ── Module 2 ──
    {
        "num": 7,
        "name": "Stroop Challenge",
        "type": "arcade",
        "desc_pl": (
            "Nazwij kolor tuszu - nie słowo!\n"
            "Efekt Stroopa mierzy konflikt poznawczy\n"
            "między automatycznym czytaniem a uwagą."
        ),
        "desc_en": (
            "Name the ink colour - not the word!\n"
            "The Stroop effect measures cognitive conflict\n"
            "between automatic reading and attention."
        ),
    },
    {
        "num": 8,
        "name": "Flanker Arena",
        "type": "arcade",
        "desc_pl": (
            "Ignoruj otaczające strzałki, reaguj na środek.\n"
            "Zadanie Eriksena testuje selektywną uwagę\n"
            "i zdolność do ignorowania dystraktorów."
        ),
        "desc_en": (
            "Ignore surrounding arrows, react to the centre.\n"
            "The Eriksen Flanker tests selective attention\n"
            "and the ability to suppress distractors."
        ),
    },
    {
        "num": 9,
        "name": "Go/No-Go Guard",
        "type": "arcade",
        "desc_pl": (
            "Reaguj na zielony sygnał, hamuj na czerwony.\n"
            "Mierz czas reakcji i kontrolę impulsów -\n"
            "kluczowe zmienne w badaniach nad uwagą."
        ),
        "desc_en": (
            "React to green signals, stop for red ones.\n"
            "Measure reaction time and impulse control -\n"
            "key variables in attention and inhibition research."
        ),
    },
    {
        "num": 10,
        "name": "N-Back Memory Grid",
        "type": "arcade",
        "desc_pl": (
            "Czy ta figura pojawiała się N kroków temu?\n"
            "N-Back obciąża pamięć roboczą i testuje\n"
            "jej pojemność w czasie rzeczywistym."
        ),
        "desc_en": (
            "Did that shape appear N steps ago?\n"
            "N-Back loads working memory and tests\n"
            "its capacity in real time."
        ),
    },
    {
        "num": 11,
        "name": "Visual Search Lab",
        "type": "arcade",
        "desc_pl": (
            "Znajdź cel ukryty wśród dystraktorów.\n"
            "Czas przeszukiwania ujawnia strategie uwagi\n"
            "i efektywność wzrokowego filtrowania."
        ),
        "desc_en": (
            "Find the target hidden among distractors.\n"
            "Search time reveals attentional strategies\n"
            "and the efficiency of visual filtering."
        ),
    },
    {
        "num": 12,
        "name": "Cognitive Dashboard",
        "type": "lab",
        "desc_pl": (
            "Zestawienie Twoich wyników z wszystkich\n"
            "gier kognitywnych. Porównaj swój profil\n"
            "poznawczy z danymi referencyjnymi."
        ),
        "desc_en": (
            "A summary of your results across all\n"
            "cognitive games. Compare your cognitive\n"
            "profile against reference data."
        ),
    },
    # ── Module 3 ──
    {
        "num": 13,
        "name": "Distribution Playground",
        "type": "lab",
        "desc_pl": (
            "Zmień parametry, obserwuj jak zmienia się rozkład.\n"
            "Normalne, Poissona, t-Studenta - intuicyjnie\n"
            "zrozum kształty danych w psychologii."
        ),
        "desc_en": (
            "Change parameters, watch the distribution shift.\n"
            "Normal, Poisson, t-Student - build intuition\n"
            "for data shapes in psychology research."
        ),
    },
    {
        "num": 14,
        "name": "Correlation Trap",
        "type": "lab",
        "desc_pl": (
            "Korelacja to nie przyczynowość! Odkryj\n"
            "fałszywe zależności w danych i naucz się\n"
            "odróżniać związek statystyczny od przyczynowego."
        ),
        "desc_en": (
            "Correlation is not causation! Discover\n"
            "spurious relationships in data and learn to\n"
            "distinguish statistical from causal links."
        ),
    },
    {
        "num": 15,
        "name": "Hypothesis Arena",
        "type": "lab",
        "desc_pl": (
            "Testuj hipotezy na symulowanych danych.\n"
            "Poznaj p-value, poziom istotności i moc testu -\n"
            "filary wnioskowania statystycznego."
        ),
        "desc_en": (
            "Test hypotheses on simulated data.\n"
            "Learn p-values, significance levels and power -\n"
            "the pillars of statistical inference."
        ),
    },
    {
        "num": 16,
        "name": "Prediction Slider",
        "type": "lab",
        "desc_pl": (
            "Przesuń suwakiem i przewiduj wyniki.\n"
            "Odkryj, jak model liniowy minimalizuje błąd\n"
            "i kiedy prognoza zawodzi."
        ),
        "desc_en": (
            "Drag the slider and make predictions.\n"
            "See how a linear model minimises error\n"
            "and when predictions break down."
        ),
    },
    # ── Module 4 ──
    {
        "num": 17,
        "name": "Feature Hunter",
        "type": "arcade",
        "desc_pl": (
            "Które cechy najbardziej wpływają na predykcję?\n"
            "Odkryj ważność zmiennych przez eliminację\n"
            "i zbuduj intuicję feature selection."
        ),
        "desc_en": (
            "Which features most influence the prediction?\n"
            "Discover variable importance through elimination\n"
            "and build intuition for feature selection."
        ),
    },
    {
        "num": 18,
        "name": "Classifier Battle",
        "type": "arcade",
        "desc_pl": (
            "Wybierz klasyfikator, dostosuj hiperparametry.\n"
            "Porównaj SVM, las losowy i sieć neuronową\n"
            "na rzeczywistych danych psychologicznych."
        ),
        "desc_en": (
            "Pick a classifier, tune hyperparameters.\n"
            "Compare SVM, random forest and neural nets\n"
            "on real psychology data."
        ),
    },
    {
        "num": 19,
        "name": "Overfitting Monster",
        "type": "arcade",
        "desc_pl": (
            "Czy Twój model zapamiętał dane treningowe?\n"
            "Odkryj overfitting przez krzywą uczenia\n"
            "i regularyzację jako lekarstwo."
        ),
        "desc_en": (
            "Did your model memorise the training data?\n"
            "Discover overfitting through learning curves\n"
            "and regularisation as the cure."
        ),
    },
    {
        "num": 20,
        "name": "Anomaly Alert",
        "type": "arcade",
        "desc_pl": (
            "Wykryj anomalie w strumieniu danych.\n"
            "Poznaj algorytmy detekcji wartości odstających\n"
            "i zastosowania w analizie danych kognitywnych."
        ),
        "desc_en": (
            "Detect anomalies in a data stream.\n"
            "Learn outlier detection algorithms and their\n"
            "applications in cognitive data analysis."
        ),
    },
    # ── Module 5 ──
    {
        "num": 21,
        "name": "Text Tokenizer Lab",
        "type": "lab",
        "desc_pl": (
            "Jak komputer widzi tekst? Tokenizuj zdania,\n"
            "usuń stop words, stwórz bag-of-words -\n"
            "pierwsze kroki w NLP."
        ),
        "desc_en": (
            "How does a computer see text? Tokenise sentences,\n"
            "remove stop words, build a bag-of-words -\n"
            "first steps in NLP."
        ),
    },
    {
        "num": 22,
        "name": "Word Weight Factory",
        "type": "lab",
        "desc_pl": (
            "TF-IDF waży słowa według ważności.\n"
            "Odkryj, które słowa najlepiej opisują dokument\n"
            "w zbiorze tekstów psychologicznych."
        ),
        "desc_en": (
            "TF-IDF weights words by importance.\n"
            "Discover which words best characterise a document\n"
            "in a psychology text corpus."
        ),
    },
    {
        "num": 23,
        "name": "Emotion Classifier",
        "type": "lab",
        "desc_pl": (
            "Czy komputer rozpozna emocje w tekście?\n"
            "Wytrenuj i oceń klasyfikator uczuć\n"
            "na danych z opisów eksperymentów."
        ),
        "desc_en": (
            "Can a computer recognise emotion in text?\n"
            "Train and evaluate a sentiment classifier\n"
            "on data from experiment descriptions."
        ),
    },
    {
        "num": 24,
        "name": "Semantic Space Explorer",
        "type": "lab",
        "desc_pl": (
            "Zbadaj przestrzeń semantyczną słów.\n"
            "Odkryj jak word embeddings reprezentują\n"
            "znaczenie i relacje językowe."
        ),
        "desc_en": (
            "Explore the semantic space of words.\n"
            "See how word embeddings represent\n"
            "meaning and language relationships."
        ),
    },
    {
        "num": 25,
        "name": "Topic Detective",
        "type": "puzzle",
        "desc_pl": (
            "Jakie tematy kryją się w korpusie tekstów?\n"
            "Użyj LDA do odkrycia ukrytych tematów\n"
            "i zidentyfikuj kto o czym pisał."
        ),
        "desc_en": (
            "What topics hide in a text corpus?\n"
            "Use LDA to uncover latent topics\n"
            "and identify who wrote about what."
        ),
    },
    {
        "num": 26,
        "name": "Human vs Model",
        "type": "arcade",
        "desc_pl": (
            "Czy model językowy przechytrzy Ciebie?\n"
            "Porównaj swoje klasyfikacje z modelem\n"
            "i odkryj gdzie AI wygrywa, a gdzie przegrywa."
        ),
        "desc_en": (
            "Can a language model outsmart you?\n"
            "Compare your classifications against a model's\n"
            "and see where AI wins and where it fails."
        ),
    },
    # ── Module 6 ──
    {
        "num": 27,
        "name": "Social Network Simulator",
        "type": "lab",
        "desc_pl": (
            "Jak informacja rozprzestrzenia się w sieci?\n"
            "Symuluj model SIR na grafie społecznym\n"
            "i obserwuj dynamikę szerzenia się treści."
        ),
        "desc_en": (
            "How does information spread in a network?\n"
            "Simulate an SIR model on a social graph\n"
            "and watch the dynamics of content spread."
        ),
    },
    {
        "num": 28,
        "name": "Misinformation Spread",
        "type": "arcade",
        "desc_pl": (
            "Powstrzymaj fake newsy zanim się rozejdą!\n"
            "Decyduj co moderować w sieci społecznej -\n"
            "uczysz się o wirusowości dezinformacji."
        ),
        "desc_en": (
            "Stop fake news before they spread!\n"
            "Decide what to moderate in a social network -\n"
            "learn about the virality of misinformation."
        ),
    },
    {
        "num": 29,
        "name": "Recommendation Bubble",
        "type": "lab",
        "desc_pl": (
            "Czy algorytmy rekomendacji tworzą bańkę filtrującą?\n"
            "Symuluj personalizację treści i zmierz\n"
            "jak komora pogłosowa informacyjna się nasila."
        ),
        "desc_en": (
            "Do recommendation algorithms create filter bubbles?\n"
            "Simulate content personalisation and measure\n"
            "how information echo chambers intensify."
        ),
    },
    {
        "num": 30,
        "name": "Bias Blind Spot",
        "type": "puzzle",
        "desc_pl": (
            "Czy rozpoznasz bias w projekcie badania?\n"
            "Zidentyfikuj ukryte założenia i błędy metodologiczne\n"
            "w opisach eksperymentów naukowych."
        ),
        "desc_en": (
            "Can you spot bias in a research design?\n"
            "Identify hidden assumptions and methodological flaws\n"
            "in scientific experiment descriptions."
        ),
    },
    {
        "num": 32,
        "name": "The Architect's Trial",
        "type": "arcade",
        "desc_pl": (
            "Finalne wyzwanie: zaprojektuj własne badanie.\n"
            "Połącz wiedzę ze wszystkich modułów\n"
            "i obróń swój projekt przed krytykami."
        ),
        "desc_en": (
            "The final challenge: design your own study.\n"
            "Combine knowledge from all modules\n"
            "and defend your research design."
        ),
    },
    {
        "num": 31,
        "name": "You Were the Dataset",
        "type": "lab",
        "desc_pl": (
            "Przez cały kurs byłeś częścią datasetu.\n"
            "Przeanalizuj swoje własne dane kognitywne\n"
            "i napisz raport z badań nad sobą."
        ),
        "desc_en": (
            "Throughout the course you were part of the dataset.\n"
            "Analyse your own cognitive data collected\n"
            "and write a report on your own research."
        ),
    },
]

# ── Module structure ──────────────────────────────────────────────────────────
# (header_pl, header_en, start_idx_in_LESSON_DATA, count)
_MODULES: list[tuple[str, str, int, int]] = [
    ("Modul 1 · Dane i Podstawy", "Module 1 · Data Basics", 0, 5),
    ("Modul 2 · Eksperymenty Kognitywne", "Module 2 · Cognitive Experiments", 5, 6),
    ("Modul 3 · Statystyka", "Module 3 · Statistics", 11, 4),
    ("Modul 4 · Machine Learning", "Module 4 · Machine Learning", 15, 4),
    ("Modul 5 · Jezyk i NLP", "Module 5 · Language & NLP", 19, 6),
    ("Modul 6 · Sieci Etyka i Final", "Module 6 · Networks, Ethics & Finale", 25, 6),
]

# ── Virtual sidebar row list ───────────────────────────────────────────────────
# Each entry: (kind, param, y_offset_px, height_px)
#   kind="header" → param = module index (0-5)
#   kind="item"   → param = _LESSON_DATA index (0-30)
_H_MODULE_ROW = 32
_H_ITEM_ROW = 36

_VIRTUAL_ROWS: list[tuple[str, int, int, int]] = []
_vy = 0
for _mi, (_mpl, _men, _mstart, _mcount) in enumerate(_MODULES):
    _VIRTUAL_ROWS.append(("header", _mi, _vy, _H_MODULE_ROW))
    _vy += _H_MODULE_ROW
    for _li in range(_mstart, _mstart + _mcount):
        _VIRTUAL_ROWS.append(("item", _li, _vy, _H_ITEM_ROW))
        _vy += _H_ITEM_ROW
_VIRTUAL_H = _vy  # 1308

# Lesson numbers follow the course README. Lesson 5 is absent because lessons 04 and 05
# (Data Cleaning + Missing Values) are merged into a single game (entry 4, "Data Quality Lab").
# Compatibility shim: keep _LESSONS for any remaining references
_LESSONS = [(d["num"], d["name"]) for d in _LESSON_DATA]


_ITEM_COLOR = (160, 160, 160)


class LessonMenuScene(Scene):
    def __init__(
        self, profile_manager: ProfileManager, strings: Strings, selected: int = 0
    ) -> None:
        self._pm = profile_manager
        self._strings = strings
        self._selected = selected
        self._hovered: int | None = None
        self._next: Scene | None = None
        self._done = False
        self._play_btn_rect: pygame.Rect | None = None
        self._teoria_btn_rect: pygame.Rect | None = None

        self._scrollbar = ScrollBar(
            total=_VIRTUAL_H,
            visible=_SIDEBAR_H,
            x=_SB_X,
            y=_TOPBAR_H,
            h=_SIDEBAR_H,
            width=_SB_TRACK_W,
        )
        # Scroll so that the initially selected item is vertically centred
        for kind, param, row_vy, _row_vh in _VIRTUAL_ROWS:
            if kind == "item" and param == selected:
                max_s = max(0, _VIRTUAL_H - _SIDEBAR_H)
                center = row_vy - (_SIDEBAR_H // 2)
                self._scrollbar.scroll_to(max(0, min(max_s, center)))
                break

        profile = self._pm.load()
        self._completed: set[int] = set(profile.completed_lessons)

        audio.play_music("menu")
        pygame.font.init()
        self._font_topbar_title = get_font_medium(28)
        self._font_topbar_sub = get_font(16)
        self._font_mod_header = get_font(13)
        self._font_item_num = get_font(14)
        self._font_item_name = get_font(18)
        self._font_panel_module = get_font(14)
        self._font_panel_badge = get_font(15)
        self._font_panel_title = get_font_medium(38)
        self._font_panel_desc = get_font(18)
        self._font_btn = get_font_medium(18)
        self._font_hintbar = get_font(14)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._handle_key(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
        elif event.type == pygame.MOUSEWHEEL:
            self._scrollbar.handle_wheel(-event.y * _H_ITEM_ROW)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_mouse_click(event)

    def _handle_key(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self._done = True
        elif event.key == pygame.K_UP:
            self._selected = max(0, self._selected - 1)
            self._ensure_visible()
            audio.play_sfx("navigate")
        elif event.key == pygame.K_DOWN:
            self._selected = min(len(_LESSON_DATA) - 1, self._selected + 1)
            self._ensure_visible()
            audio.play_sfx("navigate")
        elif event.key == pygame.K_RETURN:
            self._launch_selected_game()
        elif event.key == pygame.K_t:
            if self._teoria_available():
                lesson_num = _LESSON_DATA[self._selected]["num"]
                from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene

                back = LessonMenuScene(self._pm, self._strings, self._selected)
                self._next = LessonReaderScene(
                    lesson_num,
                    self._strings,
                    back,
                    play_factory=self._game_factory_for(lesson_num),
                )
                self._done = True
        elif event.key == pygame.K_p:
            from cognitive_data_arcade.ui.profile_screen import ProfileScene

            back = LessonMenuScene(self._pm, self._strings, self._selected)
            self._next = ProfileScene(self._pm, self._strings, back)
            self._done = True
        elif event.key == pygame.K_l:
            new_lang = "en" if self._strings.language == "pl" else "pl"
            self._pm.set_language(new_lang)
            self._strings = get_strings(new_lang)
        elif event.key == pygame.K_a:
            from cognitive_data_arcade.ui.session_picker import SessionPickerScene

            sessions_dir = Path("data") / "generated" / "reaction_time"
            self._next = SessionPickerScene(sessions_dir, self._strings, self._pm)
            self._done = True
        elif event.key == pygame.K_o:
            from cognitive_data_arcade.ui.options_scene import OptionsScene

            back = LessonMenuScene(self._pm, self._strings, self._selected)
            self._next = OptionsScene(self._pm, self._strings, back)
            self._done = True
        elif event.key == pygame.K_s:
            from cognitive_data_arcade.ui.syllabus_scene import SyllabusScene

            back = LessonMenuScene(self._pm, self._strings, self._selected)
            self._next = SyllabusScene(self._pm, self._strings, back)
            self._done = True
        elif event.key == pygame.K_d:
            self._next = self._make_daily_challenge()
            self._done = True
        elif event.key == pygame.K_z:
            self._launch_stroop_picker()

    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        self._scrollbar.handle_mousemotion(event.pos, event.buttons)
        x, y = event.pos
        if 0 <= x < _SIDEBAR_W and _TOPBAR_H <= y < _TOPBAR_H + _SIDEBAR_H:
            self._hovered = self._lesson_idx_at(y)
        else:
            self._hovered = None

    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        x, y = event.pos
        if 0 <= x < _SIDEBAR_W and _TOPBAR_H <= y < _TOPBAR_H + _SIDEBAR_H:
            if self._scrollbar.handle_mousedown(event.pos):
                return
            vy = y - _TOPBAR_H + self._scrollbar.scroll
            for kind, param, row_vy, row_vh in _VIRTUAL_ROWS:
                if kind == "header" and row_vy <= vy < row_vy + row_vh:
                    from cognitive_data_arcade.ui.module_runner_scene import ModuleRunnerScene
                    from cognitive_data_arcade.ui.act_intro_scene import make_act_intro

                    self._pm.set_current_module(param)
                    _runner = ModuleRunnerScene(param, self._pm, self._strings)
                    self._next = make_act_intro(self._pm, param, self._strings, back_scene=_runner)
                    self._done = True
                    return
            idx = self._lesson_idx_at(y)
            if idx is not None:
                self._selected = idx
            return
        if self._play_btn_rect and self._play_btn_rect.collidepoint(x, y):
            audio.play_sfx("select")
            self._launch_selected_game()
        elif (
            self._teoria_btn_rect
            and self._teoria_btn_rect.collidepoint(x, y)
            and self._teoria_available()
        ):
            lesson_num = _LESSON_DATA[self._selected]["num"]
            from cognitive_data_arcade.ui.lesson_reader import LessonReaderScene

            back = LessonMenuScene(self._pm, self._strings, self._selected)
            self._next = LessonReaderScene(
                lesson_num,
                self._strings,
                back,
                play_factory=self._game_factory_for(lesson_num),
            )
            self._done = True

    def _lesson_idx_at(self, screen_y: int) -> int | None:
        vy = screen_y - _TOPBAR_H + self._scrollbar.scroll
        for kind, param, row_vy, row_vh in _VIRTUAL_ROWS:
            if kind == "item" and row_vy <= vy < row_vy + row_vh:
                return param
        return None

    def _ensure_visible(self) -> None:
        for kind, param, row_vy, row_vh in _VIRTUAL_ROWS:
            if kind == "item" and param == self._selected:
                scroll = self._scrollbar.scroll
                if row_vy < scroll:
                    self._scrollbar.scroll_to(row_vy)
                elif row_vy + row_vh > scroll + _SIDEBAR_H:
                    self._scrollbar.scroll_to(row_vy + row_vh - _SIDEBAR_H)
                break

    def _launch_selected_game(self) -> None:
        audio.play_sfx("select")
        lesson_num = _LESSON_DATA[self._selected]["num"]
        self._pm.complete_lesson(lesson_num)
        if lesson_num == 1:
            self._launch_big_data_map()
        elif lesson_num == 2:
            self._launch_rt_lab()
        elif lesson_num == 3:
            self._launch_event_log_detective()
        elif lesson_num == 4:
            self._launch_data_cleaning()
        elif lesson_num == 8:
            self._launch_flanker()
        elif lesson_num == 9:
            self._launch_gono()
        elif lesson_num == 10:
            self._launch_nback()
        elif lesson_num == 11:
            self._launch_visual_search()
        elif lesson_num == 12:
            self._launch_cognitive_dashboard()
        elif lesson_num == 13:
            self._launch_distribution_playground()
        elif lesson_num == 14:
            self._launch_correlation_trap()
        elif lesson_num == 15:
            self._launch_hypothesis_arena()
        elif lesson_num == 16:
            self._launch_prediction_slider()
        elif lesson_num == 17:
            self._launch_feature_hunter()
        elif lesson_num == 18:
            self._launch_classifier_battle()
        elif lesson_num == 19:
            self._launch_overfitting_monster()
        elif lesson_num == 20:
            self._launch_anomaly_alert()
        elif lesson_num == 21:
            self._launch_text_tokenizer()
        elif lesson_num == 22:
            self._launch_word_weight_factory()
        elif lesson_num == 23:
            self._launch_emotion_classifier()
        elif lesson_num == 24:
            self._launch_semantic_space()
        elif lesson_num == 25:
            self._launch_topic_detective()
        elif lesson_num == 26:
            self._launch_human_vs_model()
        elif lesson_num == 27:
            self._launch_social_network()
        elif lesson_num == 28:
            self._launch_misinformation()
        elif lesson_num == 29:
            self._launch_recommendation_bubble()
        elif lesson_num == 30:
            self._launch_bias_blind_spot()
        elif lesson_num == 32:
            self._launch_architects_trial()
        elif lesson_num == 31:
            self._launch_you_were_the_dataset()
        elif lesson_num == 6:
            self._launch_eda()
        elif lesson_num == 7:
            self._launch_stroop()

    def _teoria_available(self) -> bool:
        from cognitive_data_arcade.engine.lesson_registry import lesson_available

        lesson_num = _LESSON_DATA[self._selected]["num"]
        return lesson_available(lesson_num)

    def _game_factory_for(self, lesson_num: int):
        from cognitive_data_arcade.ui.game_launcher import game_factory_for

        return game_factory_for(lesson_num, self._pm, self._strings)

    def _launch_big_data_map(self) -> None:
        self._next = self._make_big_data_map_game()
        self._done = True

    def _make_big_data_map_inner(self) -> Scene:
        """PausableGame(BigDataMapGame) without the HowToPlay screen.

        Used as back_scene from ConceptDetailScene so BACKSPACE returns
        directly to the network rather than replaying the how-to-play intro.
        """
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.big_data_map.game import BigDataMapGame
        from cognitive_data_arcade.games.big_data_map.info import get_game_info

        game_info = get_game_info(self._strings)

        def _detail_factory(lesson_num: int) -> Scene:
            from cognitive_data_arcade.games.big_data_map.detail import ConceptDetailScene

            back = self._make_big_data_map_inner()
            detail = ConceptDetailScene(lesson_num, self._strings, back_scene=back)
            return PausableGame(
                detail, game_info, lambda: _detail_factory(lesson_num), self._strings, self._pm
            )

        inner = BigDataMapGame(self._strings, self._pm, concept_detail_factory=_detail_factory)
        return PausableGame(
            inner, game_info, self._make_big_data_map_inner, self._strings, self._pm
        )

    def _make_big_data_map_game(self) -> Scene:
        from cognitive_data_arcade.games.big_data_map.info import get_game_info
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        game_info = get_game_info(self._strings)
        pausable = self._make_big_data_map_inner()
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_rt_lab(self) -> None:
        self._next = self._make_rt_lab_game()
        self._done = True

    def _launch_event_log_detective(self) -> None:
        from cognitive_data_arcade.ui.event_log_level_scene import EventLogLevelScene

        self._next = EventLogLevelScene(self._pm, self._strings)
        self._done = True

    def _make_rt_lab_game(self) -> Scene:
        import datetime

        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.reaction_time.config import DEFAULT_CONFIG
        from cognitive_data_arcade.games.reaction_time.game import ReactionTimeGame
        from cognitive_data_arcade.games.reaction_time.info import get_game_info
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        profile = self._pm.load()
        pid = profile.device_uuid
        sid = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = Path("data") / "generated" / "reaction_time" / f"{sid}.csv"
        inner = ReactionTimeGame(DEFAULT_CONFIG, self._pm, self._strings, pid, sid, csv_path)
        game_info = get_game_info(self._strings)
        pausable = PausableGame(inner, game_info, self._make_rt_lab_game, self._strings, self._pm)
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_data_cleaning(self) -> None:
        self._next = self._make_data_cleaning_game()
        self._done = True

    def _make_daily_challenge(self) -> Scene:
        from cognitive_data_arcade.engine.pause import GameInfo, PausableGame
        from cognitive_data_arcade.ui.daily_challenge_scene import DailyChallengeScene

        back = LessonMenuScene(self._pm, self._strings, self._selected)
        is_pl = self._strings.language == "pl"
        game_info = GameInfo(
            title=self._strings.daily_title,
            description_lines=[self._strings.daily_subtitle],
            key_bindings=[
                ("A/B/C/D", "wybierz odpowiedź" if is_pl else "select answer"),
                ("ENTER", "potwierdź" if is_pl else "confirm"),
                ("SPACJA", "dalej" if is_pl else "next"),
            ],
        )

        def _factory() -> Scene:
            return PausableGame(
                DailyChallengeScene(self._pm, self._strings, back),
                game_info,
                _factory,
                self._strings,
                self._pm,
            )

        return _factory()

    def _make_data_cleaning_game(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.data_cleaning.info import get_game_info
        from cognitive_data_arcade.games.data_cleaning.scene import DataCleaningScene

        inner = DataCleaningScene(self._strings, self._pm)
        game_info = get_game_info(self._strings)
        # DataCleaningScene has its own INTRO phase; HowToPlayScene is redundant
        return PausableGame(
            inner, game_info, self._make_data_cleaning_game, self._strings, self._pm
        )

    def _launch_eda(self) -> None:
        self._next = self._make_eda_game()
        self._done = True

    def _make_eda_game(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.eda.info import get_game_info
        from cognitive_data_arcade.games.eda.scene import EDAScene
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = EDAScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(inner, game_info, self._make_eda_game, self._strings, self._pm)
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_stroop(self) -> None:
        from cognitive_data_arcade.ui.stroop_level_scene import StroopLevelScene

        self._next = StroopLevelScene(self._pm, self._strings)
        self._done = True

    def _launch_stroop_picker(self) -> None:
        from cognitive_data_arcade.ui.stroop_session_picker import (
            StroopSessionPickerScene,
        )

        sessions_dir = Path("data") / "generated" / "stroop"
        self._next = StroopSessionPickerScene(sessions_dir, self._strings, self._pm)
        self._done = True

    def _launch_flanker(self) -> None:
        from cognitive_data_arcade.ui.flanker_level_scene import FlankerLevelScene

        self._next = FlankerLevelScene(self._pm, self._strings)
        self._done = True

    def _launch_gono(self) -> None:
        from cognitive_data_arcade.ui.gono_level_scene import GoNoGoLevelScene

        self._next = GoNoGoLevelScene(self._pm, self._strings)
        self._done = True

    def _launch_nback(self) -> None:
        from cognitive_data_arcade.ui.nback_level_scene import NBackLevelScene

        self._next = NBackLevelScene(self._pm, self._strings)
        self._done = True

    def _launch_visual_search(self) -> None:
        self._next = self._make_visual_search_game()
        self._done = True

    def _make_visual_search_game(self) -> Scene:
        from cognitive_data_arcade.ui.visual_search_level_scene import VisualSearchLevelScene

        return VisualSearchLevelScene(self._pm, self._strings)

    def _launch_cognitive_dashboard(self) -> None:
        self._next = self._make_cognitive_dashboard_scene()
        self._done = True

    def _make_cognitive_dashboard_scene(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.cognitive_dashboard.info import get_game_info
        from cognitive_data_arcade.games.cognitive_dashboard.mode_scene import (
            CognitiveDashboardModeScene,
        )
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = CognitiveDashboardModeScene(self._pm, self._strings)
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_cognitive_dashboard_scene, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_distribution_playground(self) -> None:
        self._next = self._make_distribution_playground()
        self._done = True

    def _make_distribution_playground(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.distribution_playground.info import get_game_info
        from cognitive_data_arcade.games.distribution_playground.scene import (
            DistributionPlaygroundScene,
        )
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = DistributionPlaygroundScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_distribution_playground, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_correlation_trap(self) -> None:
        self._next = self._make_correlation_trap()
        self._done = True

    def _make_correlation_trap(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.correlation_trap.info import get_game_info
        from cognitive_data_arcade.games.correlation_trap.scene import (
            CorrelationTrapScene,
        )
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = CorrelationTrapScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_correlation_trap, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_hypothesis_arena(self) -> None:
        self._next = self._make_hypothesis_arena()
        self._done = True

    def _make_hypothesis_arena(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.hypothesis_arena.info import get_game_info
        from cognitive_data_arcade.games.hypothesis_arena.scene import HypothesisArenaScene
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = HypothesisArenaScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_hypothesis_arena, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_prediction_slider(self) -> None:
        self._next = self._make_prediction_slider()
        self._done = True

    def _make_prediction_slider(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.prediction_slider.info import get_game_info
        from cognitive_data_arcade.games.prediction_slider.scene import PredictionSliderScene
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = PredictionSliderScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_prediction_slider, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_feature_hunter(self) -> None:
        self._next = self._make_feature_hunter()
        self._done = True

    def _make_feature_hunter(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.feature_hunter.game import FeatHunterScene
        from cognitive_data_arcade.games.feature_hunter.info import get_game_info
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = FeatHunterScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_feature_hunter, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_classifier_battle(self) -> None:
        self._next = self._make_classifier_battle()
        self._done = True

    def _make_classifier_battle(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.classifier_battle.game import ClassifierBattleScene
        from cognitive_data_arcade.games.classifier_battle.info import get_game_info

        inner = ClassifierBattleScene()
        game_info = get_game_info(self._strings)
        return PausableGame(inner, game_info, self._make_classifier_battle, self._strings, self._pm)

    def _launch_overfitting_monster(self) -> None:
        self._next = self._make_overfitting_monster()
        self._done = True

    def _make_overfitting_monster(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.overfitting_monster.game import OverfittingMonsterScene
        from cognitive_data_arcade.games.overfitting_monster.info import get_game_info

        inner = OverfittingMonsterScene()
        game_info = get_game_info(self._strings)
        return PausableGame(
            inner, game_info, self._make_overfitting_monster, self._strings, self._pm
        )

    def _launch_anomaly_alert(self) -> None:
        self._next = self._make_anomaly_alert()
        self._done = True

    def _make_anomaly_alert(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.anomaly_alert.game import AnomalyAlertScene
        from cognitive_data_arcade.games.anomaly_alert.info import get_game_info

        inner = AnomalyAlertScene()
        game_info = get_game_info(self._strings)
        return PausableGame(inner, game_info, self._make_anomaly_alert, self._strings, self._pm)

    def _launch_text_tokenizer(self) -> None:
        self._next = self._make_text_tokenizer()
        self._done = True

    def _make_text_tokenizer(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.text_tokenizer.info import get_game_info
        from cognitive_data_arcade.games.text_tokenizer.scene import TextTokenizerLabScene
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = TextTokenizerLabScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_text_tokenizer, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_word_weight_factory(self) -> None:
        self._next = self._make_word_weight_factory()
        self._done = True

    def _make_word_weight_factory(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.word_weight_factory.info import get_game_info
        from cognitive_data_arcade.games.word_weight_factory.scene import WordWeightFactoryScene
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = WordWeightFactoryScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_word_weight_factory, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_topic_detective(self) -> None:
        self._next = self._make_topic_detective()
        self._done = True

    def _make_topic_detective(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.topic_detective.game import TopicDetectiveScene
        from cognitive_data_arcade.games.topic_detective.info import get_game_info

        inner = TopicDetectiveScene()
        game_info = get_game_info(self._strings)
        return PausableGame(inner, game_info, self._make_topic_detective, self._strings, self._pm)

    def _launch_human_vs_model(self) -> None:
        self._next = self._make_human_vs_model()
        self._done = True

    def _make_human_vs_model(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.human_vs_model.game import HumanVsModelScene
        from cognitive_data_arcade.games.human_vs_model.info import get_game_info

        inner = HumanVsModelScene()
        game_info = get_game_info(self._strings)
        return PausableGame(inner, game_info, self._make_human_vs_model, self._strings, self._pm)

    def _launch_social_network(self) -> None:
        self._next = self._make_social_network()
        self._done = True

    def _make_social_network(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.social_network.game import SocialNetworkScene
        from cognitive_data_arcade.games.social_network.info import get_game_info
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = SocialNetworkScene()
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_social_network, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_misinformation(self) -> None:
        self._next = self._make_misinformation()
        self._done = True

    def _make_misinformation(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.misinformation.game import MisinformationScene
        from cognitive_data_arcade.games.misinformation.info import get_game_info

        inner = MisinformationScene()
        game_info = get_game_info(self._strings)
        return PausableGame(inner, game_info, self._make_misinformation, self._strings, self._pm)

    def _launch_recommendation_bubble(self) -> None:
        self._next = self._make_recommendation_bubble()
        self._done = True

    def _make_recommendation_bubble(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.recommendation_bubble.game import RecommendationBubbleScene
        from cognitive_data_arcade.games.recommendation_bubble.info import get_game_info

        inner = RecommendationBubbleScene()
        game_info = get_game_info(self._strings)
        return PausableGame(
            inner, game_info, self._make_recommendation_bubble, self._strings, self._pm
        )

    def _launch_bias_blind_spot(self) -> None:
        self._next = self._make_bias_blind_spot()
        self._done = True

    def _make_bias_blind_spot(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.bias_blind_spot.game import BiasBlindSpotScene
        from cognitive_data_arcade.games.bias_blind_spot.info import get_game_info

        inner = BiasBlindSpotScene()
        game_info = get_game_info(self._strings)
        return PausableGame(inner, game_info, self._make_bias_blind_spot, self._strings, self._pm)

    def _launch_architects_trial(self) -> None:
        self._next = self._make_architects_trial()
        self._done = True

    def _make_architects_trial(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.architects_trial.game import ArchitectsTrialScene
        from cognitive_data_arcade.games.architects_trial.info import get_game_info

        inner = ArchitectsTrialScene()
        game_info = get_game_info(self._strings)
        return PausableGame(inner, game_info, self._make_architects_trial, self._strings, self._pm)

    def _launch_you_were_the_dataset(self) -> None:
        self._next = self._make_you_were_the_dataset()
        self._done = True

    def _make_you_were_the_dataset(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.you_were_the_dataset.game import YouWereTheDatasetScene
        from cognitive_data_arcade.games.you_were_the_dataset.info import get_game_info
        from cognitive_data_arcade.ui.how_to_play_scene import make_how_to_play

        inner = YouWereTheDatasetScene(self._pm, self._strings)
        game_info = get_game_info(self._strings)
        pausable = PausableGame(
            inner, game_info, self._make_you_were_the_dataset, self._strings, self._pm
        )
        return make_how_to_play(
            self._pm,
            game_info,
            self._strings,
            back_scene=pausable,
            esc_scene=LessonMenuScene(self._pm, self._strings, self._selected),
        )

    def _launch_semantic_space(self) -> None:
        self._next = self._make_semantic_space()
        self._done = True

    def _make_semantic_space(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.semantic_space.game import SemanticSpaceScene
        from cognitive_data_arcade.games.semantic_space.info import get_game_info

        inner = SemanticSpaceScene()
        game_info = get_game_info(self._strings)
        return PausableGame(inner, game_info, self._make_semantic_space, self._strings, self._pm)

    def _launch_emotion_classifier(self) -> None:
        self._next = self._make_emotion_classifier()
        self._done = True

    def _make_emotion_classifier(self) -> Scene:
        from cognitive_data_arcade.engine.pause import PausableGame
        from cognitive_data_arcade.games.emotion_classifier.info import get_game_info
        from cognitive_data_arcade.games.emotion_classifier.game import EmotionClassifierScene

        inner = EmotionClassifierScene()
        game_info = get_game_info(self._strings)
        return PausableGame(
            inner, game_info, self._make_emotion_classifier, self._strings, self._pm
        )

    def update(self, dt_ms: float) -> None:
        pass

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_C_BG)
        self._draw_topbar(surface)
        self._draw_sidebar(surface)
        self._draw_panel(surface)
        self._draw_hintbar(surface)

    def _draw_topbar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _C_BG, (0, 0, _W, _TOPBAR_H))
        pygame.draw.line(surface, _C_SURFACE, (0, _TOPBAR_H - 1), (_W, _TOPBAR_H - 1))

        title = self._font_topbar_title.render("Cognitive Data Arcade", True, _C_TEXT)
        ty = (_TOPBAR_H - title.get_height()) // 2
        surface.blit(title, (28, ty))

        sub = self._font_topbar_sub.render(self._strings.menu_topbar_subtitle, True, _C_TEXT_DARK)
        surface.blit(sub, (28 + title.get_width() + 14, ty + 2))

        badge_txt = self._font_topbar_sub.render(self._strings.menu_lang_badge, True, _C_TEXT_DARK)
        bw = badge_txt.get_width() + 18
        bh = badge_txt.get_height() + 8
        bx = _W - bw - 20
        by = (_TOPBAR_H - bh) // 2
        pygame.draw.rect(surface, _C_SURFACE, (bx, by, bw, bh), border_radius=4)
        pygame.draw.rect(surface, _C_SURFACE2, (bx, by, bw, bh), 1, border_radius=4)
        surface.blit(badge_txt, (bx + 9, by + 4))

        done_count = len(self._completed)
        prog_txt = self._font_topbar_sub.render(
            f"{done_count} / {len(_LESSON_DATA)}", True, _C_DONE if done_count > 0 else _C_TEXT_DARK
        )
        px = bx - prog_txt.get_width() - 20
        py = (_TOPBAR_H - prog_txt.get_height()) // 2
        surface.blit(prog_txt, (px, py))

        profile = self._pm.load()
        if profile.current_module_idx is not None:
            midx = profile.current_module_idx
            lang = self._strings.language
            mname = _MODULES[midx][0] if lang == "pl" else _MODULES[midx][1]
            hint_txt = f"Kontynuuj: {mname}" if lang == "pl" else f"Continue: {mname}"
            hint_surf = self._font_topbar_sub.render(hint_txt, True, _C_ACCENT)
            surface.blit(hint_surf, (px - hint_surf.get_width() - 24, py))

        # Streak chip — left of lang badge area
        if profile.streak_days > 0:
            streak_surf = self._font_topbar_sub.render(f"* {profile.streak_days}d", True, _C_ACCENT)
            surface.blit(streak_surf, (_W - 200, (_TOPBAR_H - streak_surf.get_height()) // 2))

    def _draw_sidebar(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _C_BG, (0, _TOPBAR_H, _SIDEBAR_W, _SIDEBAR_H))
        pygame.draw.line(
            surface,
            _C_SURFACE,
            (_SIDEBAR_W, _TOPBAR_H),
            (_SIDEBAR_W, _TOPBAR_H + _SIDEBAR_H - 1),
        )

        scroll_px = self._scrollbar.scroll

        for kind, param, vy, vh in _VIRTUAL_ROWS:
            sy = _TOPBAR_H + vy - scroll_px
            if sy + vh <= _TOPBAR_H or sy >= _TOPBAR_H + _SIDEBAR_H:
                continue

            if kind == "header":
                label = self._strings.menu_modules[param]
                if param > 0 and sy > _TOPBAR_H:
                    pygame.draw.line(surface, _C_SURFACE, (0, sy), (_SIDEBAR_W, sy))
                # Subtle permanent background to distinguish header from lesson rows
                pygame.draw.rect(surface, _C_SURFACE2, (0, sy, _SIDEBAR_W, vh))
                mx, my = pygame.mouse.get_pos()
                mvy = my - _TOPBAR_H + scroll_px
                if vy <= mvy < vy + vh:
                    pygame.draw.rect(surface, _C_ACCENT_BG, (0, sy, _SIDEBAR_W, vh))
                txt = self._font_mod_header.render(label, True, _C_TEXT_DIM)
                mid_y_h = sy + (vh - txt.get_height()) // 2
                surface.blit(txt, (20, mid_y_h))
                if module_complete(param, self._completed):
                    icon = load_badge_icon(_MODULE_BADGES[param], size=20)
                    if icon:
                        ix = 20 + txt.get_width() + 6
                        surface.blit(icon, (ix, sy + (vh - 20) // 2))
                # Pill button signalling interactivity
                pill_lbl = "> Start" if self._strings.language == "pl" else "> Start"
                pill_surf = self._font_mod_header.render(pill_lbl, True, _C_TEXT)
                pill_px, pill_py = 10, 4
                pill_w = pill_surf.get_width() + pill_px * 2
                pill_h = pill_surf.get_height() + pill_py * 2
                pill_x = _SIDEBAR_W - pill_w - 12
                pill_y = sy + (vh - pill_h) // 2
                pygame.draw.rect(
                    surface, _C_ACCENT, (pill_x, pill_y, pill_w, pill_h), border_radius=4
                )
                surface.blit(pill_surf, (pill_x + pill_px, pill_y + pill_py))

            else:
                i = param
                d = _LESSON_DATA[i]
                is_active = i == self._selected
                is_hover = i == self._hovered

                if is_active:
                    pygame.draw.rect(surface, _C_ACCENT_BG, (0, sy, _SIDEBAR_W, vh))
                    pygame.draw.rect(surface, _C_ACCENT, (0, sy, 3, vh))
                elif is_hover:
                    pygame.draw.rect(surface, _C_HOVER_BG, (0, sy, _SIDEBAR_W, vh))

                num_color = _C_ACCENT if is_active else _C_TEXT_XDARK
                name_color = (
                    _C_TEXT if is_active else (_C_TEXT_DIM if not is_hover else (110, 120, 160))
                )

                num_surf = self._font_item_num.render(f"{i + 1:02d}", True, num_color)
                name_surf = self._font_item_name.render(d["name"], True, name_color)
                mid_y = sy + vh // 2

                surface.blit(num_surf, (20, mid_y - num_surf.get_height() // 2))
                surface.blit(name_surf, (48, mid_y - name_surf.get_height() // 2))

                lesson_num = d["num"]
                if lesson_num in self._completed:
                    pygame.draw.circle(surface, _C_DONE, (_SIDEBAR_W - 16, mid_y), 5)
                else:
                    dot_color = _TYPE_COLORS[d["type"]]
                    pygame.draw.circle(surface, dot_color, (_SIDEBAR_W - 16, mid_y), 4)

        self._scrollbar.draw(surface)

    def _draw_panel(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _C_BG, (_PANEL_X, _TOPBAR_H, _PANEL_W, _SIDEBAR_H))

        d = _LESSON_DATA[self._selected]
        lang = self._strings.language

        mod_label = ""
        for mi, (m_pl, m_en, start, count) in enumerate(_MODULES):
            if start <= self._selected < start + count:
                mod_label = self._strings.menu_modules[mi]
                break

        x0 = _PANEL_X + 36
        y = _TOPBAR_H + max(20, (_SIDEBAR_H - 200) // 2)

        mod_surf = self._font_panel_module.render(mod_label, True, _C_TEXT_DARK)
        surface.blit(mod_surf, (x0, y))
        y += mod_surf.get_height() + 10

        lesson_label = f"{self._strings.menu_lesson_prefix} {self._selected + 1}"
        bl_surf = self._font_panel_badge.render(lesson_label, True, _C_TEXT_DARK)
        bw = bl_surf.get_width() + 18
        bh = bl_surf.get_height() + 8
        pygame.draw.rect(surface, _C_SURFACE, (x0, y, bw, bh), border_radius=4)
        pygame.draw.rect(surface, _C_SURFACE2, (x0, y, bw, bh), 1, border_radius=4)
        surface.blit(bl_surf, (x0 + 9, y + 4))

        tx = x0 + bw + 8
        panel_dot_color = _C_DONE if d["num"] in self._completed else _TYPE_COLORS[d["type"]]
        pygame.draw.circle(surface, panel_dot_color, (tx + 5, y + bh // 2), 5)
        type_surf = self._font_panel_badge.render(d["type"], True, _C_ACCENT_LIGHT)
        surface.blit(type_surf, (tx + 14, y + 4))
        y += bh + 16

        title_surf = self._font_panel_title.render(d["name"], True, _C_TEXT)
        surface.blit(title_surf, (x0, y))
        y += title_surf.get_height() + 14

        desc = d["desc_pl"] if lang == "pl" else d["desc_en"]
        for line in desc.split("\n"):
            line_surf = self._font_panel_desc.render(line, True, _C_TEXT_DIM)
            surface.blit(line_surf, (x0, y))
            y += line_surf.get_height() + 3
        y += 14

        self._play_btn_rect = self._draw_panel_button(
            surface, x0, y, self._strings.label_play_game, primary=True
        )
        teoria_ok = self._teoria_available()
        self._teoria_btn_rect = self._draw_panel_button(
            surface,
            x0 + self._play_btn_rect.width + 10,
            y,
            self._strings.label_theory_lesson,
            primary=False,
            disabled=not teoria_ok,
        )

    def _draw_panel_button(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        label: str,
        primary: bool,
        disabled: bool = False,
    ) -> pygame.Rect:
        txt_color = (
            _C_TEXT
            if primary and not disabled
            else _C_ACCENT_LIGHT
            if not disabled
            else _C_TEXT_DARK
        )
        txt = self._font_btn.render(label, True, txt_color)
        w = txt.get_width() + 44
        h = 40
        rect = pygame.Rect(x, y, w, h)
        bg = _C_ACCENT if primary and not disabled else _C_SURFACE
        pygame.draw.rect(surface, bg, rect, border_radius=6)
        if not primary:
            pygame.draw.rect(surface, _C_SURFACE2, rect, 1, border_radius=6)
        surface.blit(txt, (x + 22, y + (h - txt.get_height()) // 2))
        return rect

    def _draw_hintbar(self, surface: pygame.Surface) -> None:
        by = _H - _HINTBAR_H
        pygame.draw.rect(surface, _C_BG, (0, by, _W, _HINTBAR_H))
        pygame.draw.line(surface, _C_SURFACE, (0, by), (_W, by))
        x = 20
        for item in self._strings.menu_hintbar_items:
            surf = self._font_hintbar.render(item, True, _C_TEXT_XDARK)
            surface.blit(surf, (x, by + (_HINTBAR_H - surf.get_height()) // 2))
            x += surf.get_width() + 20
