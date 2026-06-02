"""Lesson 08 — Flanker Effect (Flanker Arena)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Zadanie Eriksena Flankera (1974) — środkowa strzałka to cel, otaczające ją strzałki to flankers. Kongruentny (→→→): szybki. Inkongruentny (←→←): wolniejszy. Zadanie: ignoruj flankers, odpowiedz na cel.",
            "Flanker effect — RT(inkongruentny) − RT(kongruentny). Mierzy zdolność do selektywnej uwagi i hamowania dystraktorów. Typowe wartości: 20–80 ms. Duży efekt = trudność z ignorowaniem bodźców otoczenia.",
            "Skąd nazwa 'flanker' — flanker to żołnierz osłaniający skrzydła formacji. W zadaniu flankers 'otaczają' cel tak jak żołnierze flankujący chronią centrum szyku bojowego.",
            "Uwaga selektywna — zdolność do skupienia się na istotnym bodźcu przy ignorowaniu nieistotnych. Flanker task mierzy tę zdolność w warunkach konfliktu przestrzennego.",
            "Model uwagi Posnera — uwaga może być ukierunkowana jak reflektor. Gdy cel i dystraktory są blisko siebie, reflektor 'rozlewa się' na sąsiednie bodźce. Stąd efekt maleje gdy flankers są daleko od celu.",
        ],
        "notes": [
            "Mierz flanker effect = RT(inkongruentny) − RT(kongruentny). Sprawdź też dokładność w obu warunkach. Ktoś szybki z niską dokładnością może stosować strategię 'szybko i nie myślę'.",
            "Typowe wartości — flanker effect 20–50 ms to norma dla młodych dorosłych. Powyżej 80 ms sugeruje trudności z kontrolą hamowania. Poniżej 10 ms może oznaczać strategię 'wolno i dokładnie'.",
            "Efekt ćwiczenia a flanker effect — wraz z ćwiczeniem ogólny RT spada, ale flanker effect może pozostać podobny. Można nauczyć się reagować szybciej, ale konflikt dystraktorów nie znika automatycznie.",
        ],
        "tasks": [
            "Jaki jest Twój flanker effect? Porównaj go z typowym zakresem 20–80 ms. Czy masz trudności z ignorowaniem strzałek otaczających cel?",
            "Porównaj dokładność dla warunków kongruentnego i inkongruentnego. Czy popełniasz więcej błędów gdy flankers wskazują w przeciwnym kierunku?",
            "Czy Twój flanker effect zmienia się między pierwszym a ostatnim blokiem? Czy widzisz adaptację uwagi w ciągu sesji?",
        ],
    },
    "en": {
        "theory": [
            "Eriksen's Flanker task (1974) — the centre arrow is the target, surrounding arrows are flankers. Congruent (→→→): fast. Incongruent (←→←): slower. Task: ignore the flankers, respond to the target.",
            "Flanker effect — RT(incongruent) − RT(congruent). Measures selective attention and distractor suppression. Typical values: 20–80 ms. A large effect means difficulty ignoring surrounding stimuli.",
            "Why 'flanker' — a flanker is a soldier covering the wings of a formation. In the task, flankers 'surround' the target just as flanking soldiers protect the centre of a battle line.",
            "Selective attention — the ability to focus on a relevant stimulus while ignoring irrelevant ones. The Flanker task measures this ability under conditions of spatial conflict.",
            "Posner's spotlight model — attention can be directed like a spotlight. When the target and distractors are close together, the spotlight 'spills over' onto neighbouring stimuli. Hence the effect diminishes when flankers are far from the target.",
        ],
        "notes": [
            "Measure the flanker effect = RT(incongruent) − RT(congruent). Also check accuracy in both conditions. Someone fast with low accuracy may be using a 'respond without thinking' strategy.",
            "Typical values — flanker effect of 20–50 ms is normal for young adults. Above 80 ms suggests difficulty with inhibitory control. Below 10 ms may indicate a 'slow but accurate' strategy.",
            "Practice and the flanker effect — overall RT decreases with practice, but the flanker effect may stay similar. You can learn to respond faster, but the distractor conflict does not disappear automatically.",
        ],
        "tasks": [
            "What is your flanker effect? Compare it to the typical range of 20–80 ms. Do you have difficulty ignoring the arrows surrounding the target?",
            "Compare accuracy in the congruent and incongruent conditions. Do you make more errors when the flankers point in the opposite direction?",
            "Does your flanker effect change between the first and last block? Do you see attentional adaptation across the session?",
        ],
    },
}
