"""Lesson 11 - Visual Search (Visual Search Lab)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Przeszukiwanie wzrokowe to zdolność do znajdowania celu wśród dystraktorów. Na co dzień robi sie to setki razy - szukanie klucza na zawalonym biurku, twarzy znajomego w tłumie, ikony w aplikacji. Czas reakcji mówi, jak system wzrokowy przetwarza scenę.",
            "Przeszukiwanie cechowe (Feature Search) - jeśli cel różni sie od dystraktorów jedną wyrazistą cechą (kolor, kształt, orientacja), 'wyskakuje' z tła niezależnie od liczby elementów. Czas reakcji jest stały - nie rośnie ze wzrostem liczby dystraktorów. To tzw. efekt pop-out.",
            "Przeszukiwanie złożone (Conjunction Search) - gdy cel dzieli cechy z dystraktorami (np. czerwony X wśród czerwonych O i niebieskich X), mózg musi sprawdzać każdy element po kolei. Czas reakcji rośnie liniowo z liczbą elementów na ekranie - to skanowanie szeregowe.",
            "Efekt set-size - nachylenie prostej RT vs. liczba elementów jest kluczową miarą. W przeszukiwaniu cechowym nachylenie wynosi ok. 0 ms/element. W złożonym typowo 20-50 ms/element (cel obecny) i 40-80 ms/element (cel nieobecny - trzeba sprawdzić wszystkie). Stosunek nieobecny/obecny bliski 2:1 sugeruje skanowanie szeregowe z samokończeniem.",
            "Teoria Integracji Cech (Treisman, 1980) - proste cechy (kolor, orientacja, jasność) są rejestrowane równolegle przez wyspecjalizowane mapy cech. Dopiero ich połączenie w jeden obiekt wymaga skupienia uwagi. Anne Treisman otrzymała w 2011 roku Medal Narodowy Nauki USA za tę teorię i późniejsze badania nad uwagą.",
            "Badania bezpieczeństwa lotnisk (Parasuraman, 1998) wykazały, że po 30 minutach skanowania bagażu na monitorze RTG skuteczność wykrywania broni spada o ok. 30%, a wskaźnik fałszywych alarmów rośnie. Wiedza o przeszukiwaniu wzrokowym ma bezpośrednie zastosowanie praktyczne.",
        ],
        "notes": [
            "Pop-out nie zawsze jest absolutny - niektóre kombinacje cech dają nachylenia pośrednie (5-10 ms/element). Np. szukanie litery Q wśród O jest łatwe, ale nie tak błyskawiczne jak szukanie czerwonego kółka wśród niebieskich. Granica między 'cechowym' a 'złożonym' jest płynna.",
            "Asymetria poszukiwania - znalezienie prostej linii wśród skrzyżowanych jest łatwiejsze niż znalezienie skrzyżowanej wśród prostych. Cechy 'niezwykłe' wyróżniają sie mocniej niż 'zwykłe'. To asymetria wykrywania cech.",
            "Radiolodzy, piloci i kontrolerzy ruchu lotniczego pracują w warunkach przeszukiwania złożonego przez wiele godzin. Zmęczenie uwagi w tych zawodach ma bezpośrednie konsekwencje bezpieczeństwa - stąd obowiązkowe przerwy i limity czasu pracy.",
        ],
        "tasks": [
            "Porównaj wyniki: o ile ms dłużej trwało przeszukiwanie złożone niż cechowe? Sprawdź też dokładność - czy w jednym warunku pojawia sie więcej błędów?",
            "Oblicz nachylenie set-size: podziel różnicę RT (trudny minus łatwy poziom trudności) przez różnicę liczby elementów (24 minus 8 = 16). Ile ms kosztuje każdy dodatkowy element w warunku złożonym?",
            "Jak tryb bodźców (Litery vs Kształty) wpłynął na wyniki? Czy jedno przeszukiwanie było łatwiejsze? Jakie cechy wyróżniają X spośród O, a jakie odróżniają pomarańczowe kółko od niebieskiego?",
        ],
    },
    "en": {
        "theory": [
            "Visual search is the ability to find a target among distractors. It is performed hundreds of times a day - looking for keys on a cluttered desk, a friend's face in a crowd, an icon in an app. Reaction time reveals how the visual system processes the scene.",
            "Feature Search - if the target differs from distractors by a single salient feature (colour, shape, orientation), it 'pops out' from the background regardless of how many distractors are present. Reaction time is flat - it does not increase with set size. This is the pop-out effect.",
            "Conjunction Search - when the target shares features with distractors (e.g. a red X among red Os and blue Xs), the brain must check each element in turn. Reaction time grows linearly with the number of items on screen - this is serial scanning.",
            "The set-size effect - the slope of the RT x set-size function is the key measure. In feature search the slope is approximately 0 ms/item. In conjunction search it is typically 20-50 ms/item (target present) and 40-80 ms/item (target absent - every item must be checked). An absent/present ratio close to 2:1 suggests self-terminating serial search.",
            "Feature Integration Theory (Treisman, 1980) - simple features (colour, orientation, luminance) are registered in parallel by specialised feature maps. Binding them into a single object requires focused attention. Anne Treisman received the US National Medal of Science in 2011 for this theory and subsequent work on attention.",
            "Airport security research (Parasuraman, 1998) showed that after 30 minutes of scanning baggage on an X-ray monitor, weapon detection performance drops by approximately 30% and the false alarm rate rises. Knowledge of visual search has direct practical applications.",
        ],
        "notes": [
            "Pop-out is not always absolute - some feature combinations yield intermediate slopes (5-10 ms/item). For example, searching for Q among Os is easy, but not as instantaneous as finding a red circle among blue ones. The boundary between 'feature' and 'conjunction' search is gradual.",
            "Search asymmetry - finding a line with a gap among intact lines is easier than the reverse. 'Unusual' features stand out more than 'ordinary' ones. This is feature detection asymmetry.",
            "Radiologists, pilots, and air traffic controllers work under conjunction search conditions for many hours. Attentional fatigue in these professions has direct safety consequences - hence mandatory breaks and working-hour limits.",
        ],
        "tasks": [
            "Compare the results: by how many ms was conjunction search slower than feature search? Also check accuracy - are there more errors in one condition?",
            "Calculate the set-size slope: divide the RT difference (hard minus easy difficulty) by the difference in set sizes (24 minus 8 = 16). How many ms does each extra item cost in the conjunction condition?",
            "How did stimulus mode (Letters vs Shapes) affect the results? Was one search easier? What features distinguish X from O, and what distinguishes an orange circle from a blue one?",
        ],
    },
}
