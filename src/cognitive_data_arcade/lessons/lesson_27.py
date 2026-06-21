"""Lesson 27 - Social Network Simulator (graphs and social networks)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Graf to zbiór węzłów (nodes) połączonych krawędziami (edges). "
            "W sieci społecznej węzły to ludzie, krawędzie to znajomości. "
            "Stopień węzła (degree) to liczba jego krawędzi - im wyższy stopień, tym ważniejszy węzeł.",
            "Hub to węzeł o bardzo wysokim stopniu. W sieci społecznej to influencer, "
            "w sieci komputerowej to serwer centralny. "
            "Usunięcie huba może rozpaść sieć na wiele odłączonych składowych.",
            "Sieć losowa (Erdos-Renyi) łączy każdą parę węzłów z tym samym prawdopodobieństwem p. "
            "Sieć bezskalowa (Barabasi-Albert) łączy nowe węzły preferencyjnie z tymi, "
            "które już mają dużo połączeń - 'bogaty staje się bogatszy'. "
            "Rozkład stopni sieci bezskalowej jest potęgowy: mało hubów, dużo peryferyjnych.",
            "Model SIR dzieli populację na S (podatny), I (zarażony), R (odporny). "
            "Co krok: każdy I zaraża sąsiadów S z prawdop. p_infect, sam wraca do R z prawdop. p_recover. "
            "Epidemia gaśnie gdy nie ma już węzłów I.",
        ],
        "notes": [
            "Sieci bezskalowe są odporne na losowe awarie (mało hubów, dużo peryferyjnych węzłów), "
            "ale wrażliwe na celowe ataki na huby. Internet, sieci społecznościowe i sieci cytatów "
            "wykazują rozkład potęgowy - to efekt preferential attachment w czasie wzrostu sieci.",
            "Model SIR zakłada jednorodne mieszanie - każdy zarażony kontaktuje się "
            "z każdym sąsiadem z tym samym prawdopodobieństwem. "
            "Realne epidemie zależą od struktury sieci kontaktów, asymetrii, "
            "super-spreaderów i interwencji (np. szczepień targetowanych na huby).",
        ],
        "tasks": [
            "Zbuduj sieć z jednym centralnym hubem (gwiazda) i uruchom spread od huba. "
            "Potem zbuduj łańcuch (każdy węzeł połączony tylko z następnym) i uruchom od peryferium. "
            "Porównaj szybkość rozprzestrzeniania - co decyduje o różnicy?",
            "Wygeneruj sieć Random i Scale-free dla tej samej liczby węzłów. "
            "Uruchom spread od huba na obu jednocześnie. "
            "Która epidemia osiąga szczyt szybciej? Dlaczego?",
            "Pomyśl o realnym scenariuszu gdzie usunięcie hubów spowalnia spread "
            "(np. szczepienia influencerów, zamknięcie węzłów kolejowych). "
            "Co stałoby się gdybyś usunął hub ze swojej sieci przed uruchomieniem epidemii?",
        ],
    },
    "en": {
        "theory": [
            "A graph is a set of nodes connected by edges. "
            "In a social network nodes are people, edges are friendships. "
            "Node degree is its number of edges - higher degree means more influential node.",
            "A hub is a node with very high degree. In social networks it is an influencer, "
            "in computer networks a central server. "
            "Removing a hub can split the network into many disconnected components.",
            "A random network (Erdos-Renyi) connects each pair of nodes with the same probability p. "
            "A scale-free network (Barabasi-Albert) connects new nodes preferentially to those "
            "already well-connected - the rich get richer. "
            "Degree distribution in scale-free networks is power-law: few hubs, many peripheral nodes.",
            "The SIR model divides a population into S (susceptible), I (infected), R (recovered). "
            "Each step: every I node infects S neighbors with probability p_infect, "
            "and recovers to R with probability p_recover. "
            "The epidemic ends when no I nodes remain.",
        ],
        "notes": [
            "Scale-free networks are robust to random failures (few hubs, many peripheral nodes) "
            "but vulnerable to targeted hub attacks. The internet, social networks, and citation networks "
            "all show power-law degree distributions - a result of preferential attachment during growth.",
            "The SIR model assumes homogeneous mixing - each infected node contacts each neighbor "
            "with the same probability. Real epidemics depend on contact network structure, "
            "asymmetries, super-spreaders, and interventions (e.g., targeted vaccination of hubs).",
        ],
        "tasks": [
            "Build a star network (one central hub) and start spread from the hub. "
            "Then build a chain (each node connected only to the next) and start from the periphery. "
            "Compare spread speeds - what determines the difference?",
            "Generate a Random and Scale-free network with the same number of nodes. "
            "Start spread from the hub on both simultaneously. "
            "Which epidemic peaks faster? Why?",
            "Think of a real scenario where removing hubs slows spread "
            "(e.g., vaccinating influencers, closing railway hubs). "
            "What would happen if you removed the hub from your network before starting the epidemic?",
        ],
    },
}
