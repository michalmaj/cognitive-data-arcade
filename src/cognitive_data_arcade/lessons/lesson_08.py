"""Lesson 08 - Flanker Effect (Flanker Arena)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Zadanie Eriksena Flankera (1974) - środkowa strzałka to cel, otaczające ją strzałki to flankers. Kongruentny (>>>): szybki. Inkongruentny (<><): wolniejszy. Zadanie: ignoruj flankers, odpowiedz na cel.",
            "Artykuł opublikowali razem Barbara i Charles Eriksen - małżeństwo pracujące w University of Illinois. Barbara Eriksen (z domu Hamm) była współautorką oryginalnej pracy z 1974 roku, choć w cytowaniach często pojawia sie samo nazwisko Charles'a.",
            "Flanker effect - RT(inkongruentny) - RT(kongruentny). Mierzy zdolność do selektywnej uwagi i hamowania dystraktorów. Typowe wartości: 20-80 ms. Duży efekt = trudność z ignorowaniem bodźców otoczenia.",
            "Skąd nazwa 'flanker' - flanker to żołnierz osłaniający skrzydła formacji. W zadaniu flankers 'otaczają' cel tak jak żołnierze flankujący chronią centrum szyku bojowego.",
            "Uwaga selektywna - zdolność do skupienia sie na istotnym bodźcu przy ignorowaniu nieistotnych. Flanker task mierzy tę zdolność w warunkach konfliktu przestrzennego.",
            "Model uwagi Posnera - uwaga może być ukierunkowana jak reflektor. Gdy cel i dystraktory są blisko siebie, reflektor 'rozlewa sie' na sąsiednie bodźce. Efekt maleje, gdy flankers są dalej od celu.",
            "ANT (Attention Network Test) - Fan i in. (2002) połączyli zadanie flankera z paradygmatem wskazówek Posnera. Test mierzy trzy sieci uwagi niezależnie: alerting (czujność), orienting (ukierunkowanie), executive control (kontrola wykonawcza). Jeden test dostarcza trzech niezależnych miar funkcji uwagi.",
        ],
        "notes": [
            "Efekt flankera = RT(inkongruentny) - RT(kongruentny). Warto sprawdzić też dokładność w obu warunkach. Uczestnik szybki z niską dokładnością może stosować strategię 'szybko bez refleksji'.",
            "Typowe wartości - efekt flankera 20-50 ms to norma dla młodych dorosłych. Powyżej 80 ms sugeruje trudności z kontrolą hamowania. Poniżej 10 ms może oznaczać strategię 'wolno i dokładnie'.",
            "Efekt ćwiczenia a flanker effect - wraz z ćwiczeniem ogólny RT spada, ale flanker effect może pozostać podobny. Można nauczyć sie reagować szybciej, ale konflikt dystraktorów nie znika automatycznie.",
        ],
        "tasks": [
            "Jaki jest medianowy efekt flankera? Porównaj go z typowym zakresem 20-80 ms. Czy wynik wskazuje na trudności z ignorowaniem strzałek otaczających cel?",
            "Porównaj dokładność dla warunków kongruentnego i inkongruentnego. Czy w warunku inkongruentnym pojawia sie więcej błędów?",
            "Czy efekt flankera zmienia sie między pierwszym a ostatnim blokiem? Czy widoczna jest adaptacja uwagi w trakcie sesji?",
        ],
    },
    "en": {
        "theory": [
            "Eriksen's Flanker task (1974) - the centre arrow is the target, surrounding arrows are flankers. Congruent (>>>): fast. Incongruent (<><): slower. Task: ignore the flankers, respond to the target.",
            "The paper was published jointly by Barbara and Charles Eriksen - a married couple working at the University of Illinois. Barbara Eriksen (nee Hamm) was co-author of the original 1974 paper, although citations often list only Charles Eriksen.",
            "Flanker effect - RT(incongruent) - RT(congruent). Measures selective attention and distractor suppression. Typical values: 20-80 ms. A large effect means difficulty ignoring surrounding stimuli.",
            "Why 'flanker' - a flanker is a soldier covering the wings of a formation. In the task, flankers 'surround' the target just as flanking soldiers protect the centre of a battle line.",
            "Selective attention - the ability to focus on a relevant stimulus while ignoring irrelevant ones. The Flanker task measures this ability under conditions of spatial conflict.",
            "Posner's spotlight model - attention can be directed like a spotlight. When the target and distractors are close together, the spotlight 'spills over' onto neighbouring stimuli. The effect diminishes when flankers are farther from the target.",
            "ANT (Attention Network Test) - Fan et al. (2002) combined the flanker task with Posner's cuing paradigm. The test measures three attention networks independently: alerting, orienting, and executive control. A single test yields three independent measures of attentional function.",
        ],
        "notes": [
            "Flanker effect = RT(incongruent) - RT(congruent). Accuracy in both conditions is also worth checking. A participant who is fast with low accuracy may be using a 'respond without thinking' strategy.",
            "Typical values - flanker effect of 20-50 ms is normal for young adults. Above 80 ms suggests difficulty with inhibitory control. Below 10 ms may indicate a 'slow but accurate' strategy.",
            "Practice and the flanker effect - overall RT decreases with practice, but the flanker effect may stay similar. It is possible to learn to respond faster without the distractor conflict disappearing.",
        ],
        "tasks": [
            "What is the median flanker effect? Compare it to the typical range of 20-80 ms. Does the result suggest difficulty ignoring the arrows surrounding the target?",
            "Compare accuracy in the congruent and incongruent conditions. Are there more errors in the incongruent condition?",
            "Does the flanker effect change between the first and last block? Is there visible attentional adaptation across the session?",
        ],
    },
}
