"""Lesson 27 -- Social Network Simulator (graphs and social networks)."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Graf to zbior wezlow (nodes) polaczonych krawedziami (edges). "
            "W sieci spolecznej wezly to ludzie, krawedzie to znajomosci. "
            "Stopien wezla (degree) to liczba jego krawedzi -- im wyzszy stopien, tym wazniejszy wezel.",
            "Hub to wezel o bardzo wysokim stopniu. W sieci spolecznej to influencer, "
            "w sieci komputerowej to serwer centralny. "
            "Usuniecie huba moze rozpasc siec na wiele odlaczonych skladowych.",
            "Siec losowa (Erdos-Renyi) laczy kazda pare wezlow z tym samym prawdopodobienstwem p. "
            "Siec bezskalowa (Barabasi-Albert) laczy nowe wezly preferencyjnie z tymi, "
            "ktore juz maja duzo polaczen -- 'bogaty staje sie bogatszy'. "
            "Rozklad stopni sieci bezskalowej jest potegowy: malo hubow, duzo peryferyjnych.",
            "Model SIR dzieli populacje na S (podatny), I (zarazony), R (odporny). "
            "Co krok: kazdy I zaraz sasiadow S z prawdop. p_infect, sam wraca do R z prawdop. p_recover. "
            "Epidemia gasnie gdy nie ma juz wezlow I.",
        ],
        "notes": [
            "Sieci bezskalowe sa odporne na losowe awarie (malo hubow, duzo peryferyjnych wezlow), "
            "ale wrazliwe na celowe ataki na huby. Internet, sieci spolecznosciowe i sieci cytatow "
            "wykazuja rozklad potegowy -- to efekt preferential attachment w czasie wzrostu sieci.",
            "Model SIR zaklada jednorodne mieszanie -- kazdy zarazony kontaktuje sie "
            "z kazdym sasiadem z tym samym prawdopodobienstwem. "
            "Realne epidemie zaleza od struktury sieci kontaktow, asymetrii, "
            "super-spreaderow i interwencji (np. szczepien targetowanych na huby).",
        ],
        "tasks": [
            "Zbuduj siec z jednym centralnym hubem (gwiazda) i uruchom spread od huba. "
            "Potem zbuduj lancuch (kazdy wezel polaczony tylko z nastepnym) i uruchom od peryferium. "
            "Porownaj szybkosc rozprzestrzeniania -- co decyduje o rozznicy?",
            "Wygeneruj siec Random i Scale-free dla tej samej liczby wezlow. "
            "Uruchom spread od huba na obu jednoczesnie. "
            "Ktora epidemia osiaga szczyt szybciej? Dlaczego?",
            "Pomysl o realnym scenariuszu gdzie usuniecie hubow spowalnia spread "
            "(np. szczepienia influencerow, zamkniecie wezlow kolejowych). "
            "Co staloby sie gdybys usunal hub ze swojej sieci przed uruchomieniem epidemii?",
        ],
    },
    "en": {
        "theory": [
            "A graph is a set of nodes connected by edges. "
            "In a social network nodes are people, edges are friendships. "
            "Node degree is its number of edges -- higher degree means more influential node.",
            "A hub is a node with very high degree. In social networks it is an influencer, "
            "in computer networks a central server. "
            "Removing a hub can split the network into many disconnected components.",
            "A random network (Erdos-Renyi) connects each pair of nodes with the same probability p. "
            "A scale-free network (Barabasi-Albert) connects new nodes preferentially to those "
            "already well-connected -- the rich get richer. "
            "Degree distribution in scale-free networks is power-law: few hubs, many peripheral nodes.",
            "The SIR model divides a population into S (susceptible), I (infected), R (recovered). "
            "Each step: every I node infects S neighbors with probability p_infect, "
            "and recovers to R with probability p_recover. "
            "The epidemic ends when no I nodes remain.",
        ],
        "notes": [
            "Scale-free networks are robust to random failures (few hubs, many peripheral nodes) "
            "but vulnerable to targeted hub attacks. The internet, social networks, and citation networks "
            "all show power-law degree distributions -- a result of preferential attachment during growth.",
            "The SIR model assumes homogeneous mixing -- each infected node contacts each neighbor "
            "with the same probability. Real epidemics depend on contact network structure, "
            "asymmetries, super-spreaders, and interventions (e.g., targeted vaccination of hubs).",
        ],
        "tasks": [
            "Build a star network (one central hub) and start spread from the hub. "
            "Then build a chain (each node connected only to the next) and start from the periphery. "
            "Compare spread speeds -- what determines the difference?",
            "Generate a Random and Scale-free network with the same number of nodes. "
            "Start spread from the hub on both simultaneously. "
            "Which epidemic peaks faster? Why?",
            "Think of a real scenario where removing hubs slows spread "
            "(e.g., vaccinating influencers, closing railway hubs). "
            "What would happen if you removed the hub from your network before starting the epidemic?",
        ],
    },
}
