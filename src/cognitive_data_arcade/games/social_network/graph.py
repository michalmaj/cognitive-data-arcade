from __future__ import annotations

import copy
import math
import random
from dataclasses import dataclass, field

_TOP_H = 50
_NET_H = 520  # matches game layout: 720 - 50(top) - 150(bottom)


@dataclass
class Node:
    x: float
    y: float
    state: str = "S"  # "S" | "I" | "R"
    degree: int = 0


@dataclass
class Graph:
    nodes: list[Node] = field(default_factory=list)
    edges: list[tuple[int, int]] = field(default_factory=list)


def _circular_layout(n: int, panel_x: int, panel_w: int) -> list[Node]:
    if n == 0:
        return []
    cx = panel_x + panel_w // 2
    cy = _TOP_H + _NET_H // 2
    radius = min(panel_w, _NET_H) * 0.38
    nodes: list[Node] = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        nodes.append(Node(x=x, y=y))
    return nodes


def generate_random(n: int, p: float, panel_x: int, panel_w: int) -> Graph:
    """Erdos-Renyi G(n,p): each pair connected independently with probability p."""
    nodes = _circular_layout(n, panel_x, panel_w)
    edges: list[tuple[int, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                edges.append((i, j))
                nodes[i].degree += 1
                nodes[j].degree += 1
    return Graph(nodes=nodes, edges=edges)


def generate_scale_free(n: int, m: int, panel_x: int, panel_w: int) -> Graph:
    """Barabasi-Albert preferential attachment: each new node connects to m existing nodes."""
    nodes = _circular_layout(n, panel_x, panel_w)
    edges: list[tuple[int, int]] = []
    if n <= 1:
        return Graph(nodes=nodes, edges=edges)

    init = min(m + 1, n)
    for i in range(init):
        for j in range(i + 1, init):
            edges.append((i, j))
            nodes[i].degree += 1
            nodes[j].degree += 1

    for new_idx in range(init, n):
        degrees = [max(nodes[i].degree, 1) for i in range(new_idx)]
        total = sum(degrees)
        targets: set[int] = set()
        retries = 0
        while len(targets) < min(m, new_idx) and retries < 500:
            r = random.random() * total
            cumsum = 0.0
            for idx, d in enumerate(degrees):
                cumsum += d
                if r <= cumsum:
                    targets.add(idx)
                    break
            retries += 1
        for t in targets:
            edges.append((t, new_idx))
            nodes[t].degree += 1
            nodes[new_idx].degree += 1

    return Graph(nodes=nodes, edges=edges)


def sir_step(graph: Graph, p_infect: float, p_recover: float) -> Graph:
    """Returns a new Graph with updated node states. Original is unchanged."""
    new_graph = copy.deepcopy(graph)
    adj: list[list[int]] = [[] for _ in graph.nodes]
    for a, b in graph.edges:
        adj[a].append(b)
        adj[b].append(a)
    for i, node in enumerate(graph.nodes):
        if node.state == "I":
            for nb in adj[i]:
                if new_graph.nodes[nb].state == "S" and random.random() < p_infect:
                    new_graph.nodes[nb].state = "I"
            if random.random() < p_recover:
                new_graph.nodes[i].state = "R"
    return new_graph


def hub_node_index(graph: Graph) -> int:
    """Returns index of node with highest degree. Ties broken by first occurrence."""
    return max(range(len(graph.nodes)), key=lambda i: graph.nodes[i].degree)


def periphery_node_index(graph: Graph) -> int:
    """Returns index of node with lowest degree > 0. Falls back to 0 if all isolated."""
    connected = [i for i, nd in enumerate(graph.nodes) if nd.degree > 0]
    if not connected:
        return 0
    return min(connected, key=lambda i: graph.nodes[i].degree)
