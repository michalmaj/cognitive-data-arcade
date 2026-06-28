"""Lesson 27 - Social Network Simulator (graphs and social networks)."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Graf to zbiór węzłów (nodes) połączonych krawędziami (edges). W sieci społecznej węzły to ludzie, krawędzie to znajomości. Stopień węzła (degree) to liczba jego krawędzi - im wyższy stopień, tym ważniejszy węzeł.",
            "Eksperyment małego świata (Milgram, 1967) - Milgram poprosił losowych uczestników w Nebrasce, by wysłali list do nieznanej im osoby w Bostonie, przekazując go tylko przez bezpośrednich znajomych. Mediana liczby pośredników wynosiła 6 - stąd wyrażenie '6 stopni separacji'. Watts i Strogatz (1998) sformalizowali tę własność matematycznie.",
            "Hub to węzeł o bardzo wysokim stopniu. W sieci społecznej to influencer, w sieci komputerowej to serwer centralny. Usunięcie huba może rozpaść sieć na wiele odłączonych składowych.",
            "Sieć losowa (Erdos-Renyi) łączy każdą parę węzłów z tym samym prawdopodobieństwem p. Sieć bezskalowa (Barabasi i Albert, 1999) łączy nowe węzły preferencyjnie z tymi, które już mają dużo połączeń - 'bogaty staje się bogatszy'. Artykuł Barabasiego z 1999 r. w Science wykazał, że internet, WWW i sieci białkowe mają rozkład potęgowy stopni.",
            "Model SIR dzieli populację na S (podatny), I (zarażony), R (odporny). Co krok: każdy I zaraża sąsiadów S z prawdopodobieństwem p_infect, sam wraca do R z prawdopodobieństwem p_recover. Epidemia gaśnie gdy nie ma już węzłów I.",
        ],
        "notes": [
            "Sieci bezskalowe są odporne na losowe awarie (mało hubów, dużo peryferyjnych węzłów), ale wrażliwe na celowe ataki na huby. Internet, sieci społecznościowe i sieci cytatów wykazują rozkład potęgowy - to efekt preferential attachment w czasie wzrostu sieci.",
            "Model SIR zakłada jednorodne mieszanie - każdy zarażony kontaktuje się z każdym sąsiadem z tym samym prawdopodobieństwem. Realne epidemie zależą od struktury sieci kontaktów, asymetrii, super-spreaderów i interwencji (np. szczepień targetowanych na huby).",
        ],
        "tasks": [
            "Zbuduj sieć z jednym centralnym hubem (gwiazda) i uruchom spread od huba. Potem zbuduj łańcuch i uruchom od peryferium. Porównaj szybkość rozprzestrzeniania - co decyduje o różnicy?",
            "Wygeneruj sieć Random i Scale-free dla tej samej liczby węzłów. Uruchom spread od huba na obu jednocześnie. Która epidemia osiąga szczyt szybciej? Dlaczego?",
            "Pomyśl o realnym scenariuszu gdzie usunięcie hubów spowalnia spread (np. szczepienia influencerów, zamknięcie węzłów kolejowych). Co stałoby się po usunięciu huba ze sieci przed uruchomieniem epidemii?",
        ],
    },
    "en": {
        "theory": [
            "A graph is a set of nodes connected by edges. In a social network nodes are people, edges are friendships. Node degree is its number of edges - higher degree means a more influential node.",
            "The small world experiment (Milgram, 1967) - Milgram asked random participants in Nebraska to send a letter to an unknown person in Boston, passing it only through direct acquaintances. The median number of intermediaries was 6 - hence the expression '6 degrees of separation'. Watts and Strogatz (1998) formalised this property mathematically.",
            "A hub is a node with very high degree. In social networks it is an influencer, in computer networks a central server. Removing a hub can split the network into many disconnected components.",
            "A random network (Erdos-Renyi) connects each pair of nodes with the same probability p. A scale-free network (Barabasi and Albert, 1999) connects new nodes preferentially to those already well-connected - the rich get richer. Barabasi's 1999 paper in Science demonstrated that the internet, the WWW, and protein networks all follow a power-law degree distribution.",
            "The SIR model divides a population into S (susceptible), I (infected), R (recovered). Each step: every I node infects S neighbours with probability p_infect, and recovers to R with probability p_recover. The epidemic ends when no I nodes remain.",
        ],
        "notes": [
            "Scale-free networks are robust to random failures (few hubs, many peripheral nodes) but vulnerable to targeted hub attacks. The internet, social networks, and citation networks all show power-law degree distributions - a result of preferential attachment during growth.",
            "The SIR model assumes homogeneous mixing - each infected node contacts each neighbour with the same probability. Real epidemics depend on contact network structure, asymmetries, super-spreaders, and interventions (e.g., targeted vaccination of hubs).",
        ],
        "tasks": [
            "Build a star network (one central hub) and start spread from the hub. Then build a chain and start from the periphery. Compare spread speeds - what determines the difference?",
            "Generate a Random and Scale-free network with the same number of nodes. Start spread from the hub on both simultaneously. Which epidemic peaks faster? Why?",
            "Think of a real scenario where removing hubs slows spread (e.g., vaccinating influencers, closing railway hubs). What would happen after removing the hub from the network before starting the epidemic?",
        ],
    },
}

REFLECTION = {
    "pl": {
        "title": "Social Network Simulator — Refleksja",
        "cards": [
            {
                "label": "Sieć bezskalowa",
                "color": "indigo",
                "text": "Barabasi-Albert (1999): nowe węzły łączą się preferencyjnie z hubami — 'bogaty staje się bogatszy'. Rozkład potęgowy stopni: kilka hubów z tysiącami połączeń, większość węzłów z kilkoma.",
            },
            {
                "label": "Mały świat",
                "color": "orange",
                "text": "Milgram (1967): mediana 6 pośredników między losowymi ludźmi w USA. Watts i Strogatz (1998): wysoka lokalność + krótkie ścieżki globalne = sieć małego świata. Dotyczy internetu, WWW i sieci białkowych.",
            },
            {
                "label": "SIR i epidemie",
                "color": "green",
                "text": "R0 = p_infect / p_recover. R0 > 1: epidemia rośnie. Sieci bezskalowe są odporne na losowe awarie węzłów, ale dramatycznie wrażliwe na celowe ataki na huby.",
            },
        ],
        "question": "Hub z 500 połączeniami jest 'patient zero'. Dlaczego szczepienie hubów jest wielokrotnie skuteczniejsze niż szczepienie losowych węzłów? Jak to wynika ze struktury sieci bezskalowej?",
    },
    "en": {
        "title": "Social Network Simulator — Reflection",
        "cards": [
            {
                "label": "Scale-free network",
                "color": "indigo",
                "text": "Barabasi-Albert (1999): new nodes attach preferentially to hubs — 'the rich get richer'. Power-law degree distribution: a few hubs with thousands of connections, most nodes with just a few.",
            },
            {
                "label": "Small world",
                "color": "orange",
                "text": "Milgram (1967): median of 6 intermediaries between random people in the USA. Watts and Strogatz (1998): high local clustering + short global paths = small-world network. Applies to the internet, WWW, and protein networks.",
            },
            {
                "label": "SIR and epidemics",
                "color": "green",
                "text": "R0 = p_infect / p_recover. R0 > 1: epidemic grows. Scale-free networks are robust to random node failures but dramatically vulnerable to targeted attacks on hubs.",
            },
        ],
        "question": "A hub with 500 connections is 'patient zero'. Why is vaccinating hubs many times more effective than vaccinating random nodes? How does this follow from the structure of a scale-free network?",
    },
}
