"""Lesson 11 — Visual Search (Visual Search Lab)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Przeszukiwanie wzrokowe to zdolność do znajdowania celu wśród dystraktorów. Na co dzień robimy to setki razy — szukamy klucza na zawalonym biurku, twarzy znajomego w tłumie, ikony w aplikacji. Czas reakcji mówi nam, jak system wzrokowy przetwarza scenę.",
            "Przeszukiwanie cechowe (Feature Search) — jeśli cel różni się od dystraktorów jedną wyrazistą cechą (kolor, kształt, orientacja), 'wyskakuje' z tła niezależnie od liczby elementów. Czas reakcji jest stały — nie rośnie ze wzrostem liczby dystraktorów. To tzw. efekt pop-out.",
            "Przeszukiwanie złożone (Conjunction Search) — gdy cel dzieli cechy z dystraktorami (np. czerwony X wśród czerwonych O i niebieskich X), mózg musi sprawdzać każdy element po kolei. Czas reakcji rośnie liniowo z liczbą elementów na ekranie — to skanowanie szeregowe.",
            "Efekt set-size — nachylenie prostej RT vs. liczba elementów jest kluczową miarą. W przeszukiwaniu cechowym nachylenie ≈ 0 ms/element. W złożonym typowo 20–50 ms/element (gdy cel jest obecny) i 40–80 ms/element (gdy nieobecny — trzeba sprawdzić wszystkie). Stosunek nieobecny/obecny bliski 2:1 sugeruje skanowanie szeregowe z samokończeniem.",
            "Teoria Integracji Cech (Treisman, 1980) — proste cechy (kolor, orientacja, jasność) są rejestrowane równolegle przez wyspecjalizowane mapy cech. Dopiero ich połączenie w jeden obiekt wymaga skupienia uwagi. Przeszukiwanie złożone jest wolniejsze, bo uwaga musi 'sklejać' cechy obiekt po obiekcie.",
        ],
        "notes": [
            "Pop-out nie zawsze jest absolutny — niektóre kombinacje cech dają nachylenia pośrednie (5–10 ms/element). Np. szukanie litery Q wśród O jest łatwe, ale nie tak błyskawiczne jak szukanie czerwonego kółka wśród niebieskich. Granica między 'cechowym' a 'złożonym' jest płynna.",
            "Asymetria poszukiwania — znalezienie prostej linii wśród skrzyżowanych jest łatwiejsze niż znalezienie skrzyżowanej wśród prostych. Kierunek wyszukiwania ma znaczenie — cechy 'niezwykłe' wyróżniają się mocniej niż 'zwykłe'. To asymetria wykrywania cech.",
            "Praktyczne zastosowania — radiolodzy szukają guzków w RTG (przeszukiwanie złożone → zmęczenie uwagi), projektanci UI chcą, żeby kluczowe przyciski 'wyskakiwały' (efekt pop-out), kontrolerzy bagażu na lotniskach wykrywają broń wśród normalnych przedmiotów. Wiedza o przeszukiwaniu wzrokowym dosłownie ratuje życie.",
        ],
        "tasks": [
            "Porównaj swoje wyniki: o ile ms dłużej trwało przeszukiwanie złożone niż cechowe? Sprawdź też dokładność — czy w jednym warunku częściej się myliłeś? Jeśli tak, to dlaczego przeszukiwanie złożone jest bardziej podatne na błędy?",
            "Spróbuj obliczyć nachylenie set-size dla swojego wyniku: podziel różnicę RT (trudny minus łatwy poziom trudności) przez różnicę liczby elementów (24 minus 8 = 16). Ile ms kosztuje każdy dodatkowy element w warunku złożonym?",
            "Jak tryb bodźców (Litery vs Kształty) wpłynął na Twoje wyniki? Czy jedno przeszukiwanie było łatwiejsze? Zastanów się, dlaczego — jakie cechy wyróżniają X spośród O, a jakie odróżniają pomarańczowe kółko od niebieskiego?",
        ],
    },
    "en": {
        "theory": [
            "Visual search is the ability to find a target among distractors. We do it hundreds of times a day — looking for keys on a cluttered desk, a friend's face in a crowd, an icon in an app. Reaction time tells us how the visual system processes the scene.",
            "Feature Search — if the target differs from distractors by a single salient feature (colour, shape, orientation), it 'pops out' from the background regardless of how many distractors are present. Reaction time is flat — it does not increase with set size. This is the pop-out effect.",
            "Conjunction Search — when the target shares features with distractors (e.g. a red X among red Os and blue Xs), the brain must check each element in turn. Reaction time grows linearly with the number of items on screen — this is serial scanning.",
            "The set-size effect — the slope of the RT × set-size function is the key measure. In feature search the slope ≈ 0 ms/item. In conjunction search it is typically 20–50 ms/item (target present) and 40–80 ms/item (target absent — every item must be checked). An absent/present ratio close to 2:1 suggests self-terminating serial search.",
            "Feature Integration Theory (Treisman, 1980) — simple features (colour, orientation, luminance) are registered in parallel by specialised feature maps. Binding them into a single object requires focused attention. Conjunction search is slower because attention must 'glue' features object by object.",
        ],
        "notes": [
            "Pop-out is not always absolute — some feature combinations yield intermediate slopes (5–10 ms/item). For example, searching for Q among Os is easy, but not as instantaneous as finding a red circle among blue ones. The boundary between 'feature' and 'conjunction' search is gradual.",
            "Search asymmetry — finding a line with a gap among intact lines is easier than the reverse. The direction of search matters — 'unusual' features stand out more than 'ordinary' ones. This is feature detection asymmetry.",
            "Practical applications — radiologists search for tumours in X-rays (conjunction search → attentional fatigue), UI designers want key buttons to pop out, airport security officers detect weapons among normal objects. Knowledge of visual search literally saves lives.",
        ],
        "tasks": [
            "Compare your results: by how many ms was conjunction search slower than feature search? Also check accuracy — did you make more errors in one condition? If so, why is conjunction search more error-prone?",
            "Try calculating your set-size slope: divide the RT difference (hard minus easy difficulty) by the difference in set sizes (24 minus 8 = 16). How many ms does each extra item cost in the conjunction condition?",
            "How did stimulus mode (Letters vs Shapes) affect your results? Was one search easier? Think about why — what features distinguish X from O, and what distinguishes an orange circle from a blue one?",
        ],
    },
}
