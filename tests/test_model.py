"""test_model.py - Unit tests for resilient_info_kit.model."""

from __future__ import annotations

import pytest

from resilient_info_kit.model import ConsentRelayGraph, Edge, Node


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def simple_graph() -> ConsentRelayGraph:
    """A minimal three-node graph: A -> B -> C.

    B has consented to 'analytics'; C has consented to 'analytics'.
    """
    graph = ConsentRelayGraph()
    graph.add_node(Node(node_id="A", label="Source", consents=frozenset()))
    graph.add_node(
        Node(node_id="B", label="Relay", consents=frozenset({"analytics"}))
    )
    graph.add_node(
        Node(node_id="C", label="Target", consents=frozenset({"analytics"}))
    )
    graph.add_edge(
        Edge(source="A", target="B", required_consents=frozenset({"analytics"}))
    )
    graph.add_edge(
        Edge(source="B", target="C", required_consents=frozenset({"analytics"}))
    )
    return graph


# ---------------------------------------------------------------------------
# Node tests
# ---------------------------------------------------------------------------


class TestNode:
    def test_has_consent_true(self) -> None:
        node = Node(node_id="X", consents=frozenset({"analytics"}))
        assert node.has_consent("analytics") is True

    def test_has_consent_false(self) -> None:
        node = Node(node_id="X", consents=frozenset({"analytics"}))
        assert node.has_consent("marketing") is False

    def test_node_is_hashable(self) -> None:
        node = Node(node_id="X")
        assert {node}  # can be added to a set


# ---------------------------------------------------------------------------
# Graph topology tests
# ---------------------------------------------------------------------------


class TestConsentRelayGraph:
    def test_add_and_neighbors(self, simple_graph: ConsentRelayGraph) -> None:
        assert "B" in simple_graph.neighbors("A")
        assert "C" in simple_graph.neighbors("B")
        assert simple_graph.neighbors("C") == []

    def test_consent_path_exists(self, simple_graph: ConsentRelayGraph) -> None:
        path = simple_graph.consent_path("A", "C", "analytics")
        assert path is not None
        assert path[0] == "A"
        assert path[-1] == "C"

    def test_consent_path_no_consent(self, simple_graph: ConsentRelayGraph) -> None:
        """No path for a purpose that B has not consented to."""
        path = simple_graph.consent_path("A", "C", "marketing")
        assert path is None

    def test_consent_path_unknown_node(self, simple_graph: ConsentRelayGraph) -> None:
        path = simple_graph.consent_path("A", "UNKNOWN", "analytics")
        assert path is None

    def test_to_dict_round_trip(self, simple_graph: ConsentRelayGraph) -> None:
        data = simple_graph.to_dict()
        rebuilt = ConsentRelayGraph.from_dict(data)
        assert len(rebuilt.to_dict()["nodes"]) == len(data["nodes"])
        assert len(rebuilt.to_dict()["edges"]) == len(data["edges"])

    def test_to_dict_structure(self, simple_graph: ConsentRelayGraph) -> None:
        data = simple_graph.to_dict()
        assert "nodes" in data
        assert "edges" in data
        node_ids = {n["node_id"] for n in data["nodes"]}
        assert node_ids == {"A", "B", "C"}

    def test_empty_graph_no_path(self) -> None:
        graph = ConsentRelayGraph()
        graph.add_node(Node(node_id="A"))
        graph.add_node(Node(node_id="B"))
        assert graph.consent_path("A", "B", "analytics") is None
