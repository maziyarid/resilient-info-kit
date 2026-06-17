"""model.py - Graph-theoretic consent relay routing model.

RESEARCH USE ONLY. Implements a directed graph model for consent-based
information relay routing between nodes.
"""

from __future__ import annotations

import dataclasses
from typing import Dict, FrozenSet, List, Optional, Set, Tuple


@dataclasses.dataclass(frozen=True)
class Node:
    """A node in the consent relay graph."""

    node_id: str
    label: str = ""
    consents: FrozenSet[str] = dataclasses.field(default_factory=frozenset)

    def has_consent(self, purpose: str) -> bool:
        """Return True if this node has consented to *purpose*."""
        return purpose in self.consents


@dataclasses.dataclass
class Edge:
    """A directed edge representing a relay link between two nodes."""

    source: str
    target: str
    weight: float = 1.0
    required_consents: FrozenSet[str] = dataclasses.field(default_factory=frozenset)


class ConsentRelayGraph:
    """Directed graph model for consent-aware relay routing.

    All operations are performed in-memory and are suitable only for
    research simulation — no real data is transmitted.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}
        self._edges: List[Edge] = []

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def add_node(self, node: Node) -> None:
        """Register *node* in the graph (replaces existing entry)."""
        self._nodes[node.node_id] = node

    def add_edge(self, edge: Edge) -> None:
        """Add a directed *edge* to the graph."""
        self._edges.append(edge)

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def neighbors(self, node_id: str) -> List[str]:
        """Return IDs of nodes reachable from *node_id* in one hop."""
        return [e.target for e in self._edges if e.source == node_id]

    def consent_path(
        self,
        source: str,
        target: str,
        purpose: str,
    ) -> Optional[List[str]]:
        """BFS for a consent-valid path from *source* to *target*.

        A path is valid when every intermediate node has consented to
        *purpose* and every traversed edge permits *purpose*.

        Returns the path as a list of node IDs, or ``None`` if no
        valid path exists.
        """
        if source not in self._nodes or target not in self._nodes:
            return None

        queue: List[List[str]] = [[source]]
        visited: Set[str] = {source}

        while queue:
            path = queue.pop(0)
            current = path[-1]

            if current == target:
                return path

            for edge in self._edges:
                if edge.source != current:
                    continue
                if purpose in edge.required_consents:
                    node = self._nodes.get(edge.target)
                    if node is None or not node.has_consent(purpose):
                        continue
                if edge.target not in visited:
                    visited.add(edge.target)
                    queue.append(path + [edge.target])

        return None

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation of the graph."""
        return {
            "nodes": [
                {
                    "node_id": n.node_id,
                    "label": n.label,
                    "consents": sorted(n.consents),
                }
                for n in self._nodes.values()
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "weight": e.weight,
                    "required_consents": sorted(e.required_consents),
                }
                for e in self._edges
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConsentRelayGraph":
        """Reconstruct a graph from a dictionary produced by :meth:`to_dict`."""
        graph = cls()
        for n in data.get("nodes", []):
            graph.add_node(
                Node(
                    node_id=n["node_id"],
                    label=n.get("label", ""),
                    consents=frozenset(n.get("consents", [])),
                )
            )
        for e in data.get("edges", []):
            graph.add_edge(
                Edge(
                    source=e["source"],
                    target=e["target"],
                    weight=e.get("weight", 1.0),
                    required_consents=frozenset(e.get("required_consents", [])),
                )
            )
        return graph
