from __future__ import annotations

import networkx as nx


class NetworkPKI:
    """Edge A -> B means A issued a certificate for B."""

    def __init__(self, adjacency: dict[str, list[str]]) -> None:
        self.graph = nx.DiGraph(adjacency)
        self.graph.add_nodes_from(
            dst for dsts in adjacency.values() for dst in dsts
        )

    @property
    def adjacency(self) -> dict[str, list[str]]:
        return {node: list(self.graph.successors(node)) for node in self.nodes()}

    def nodes(self) -> list[str]:
        return sorted(self.graph.nodes())

    def adjacency_matrix(self) -> tuple[list[str], list[list[int]]]:
        nodes = self.nodes()
        matrix = [[int(self.graph.has_edge(u, v)) for v in nodes] for u in nodes]
        return nodes, matrix

    def trust_chain(self, trust_anchor: str, target: str) -> list[str] | None:
        if trust_anchor not in self.graph or target not in self.graph:
            raise KeyError("trust_anchor or target missing from graph")
        try:
            return nx.shortest_path(self.graph, trust_anchor, target)
        except nx.NetworkXNoPath:
            return None
