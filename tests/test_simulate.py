"""Unit tests for resilient_info_kit.simulate module."""

import pytest
from resilient_info_kit.model import ConsentRelayGraph, Node, Edge
from resilient_info_kit.simulate import (
    Scenario,
    SimulationResult,
    SimulationEngine,
)


@pytest.fixture
def simple_scenario() -> Scenario:
    """A minimal two-hop scenario fixture."""
    graph = ConsentRelayGraph()
    graph.add_node(Node(node_id="A", consented_purposes={"analytics"}))
    graph.add_node(Node(node_id="B", consented_purposes={"analytics"}))
    graph.add_node(Node(node_id="C", consented_purposes={"analytics"}))
    graph.add_edge(Edge(source="A", target="B", weight=1.0))
    graph.add_edge(Edge(source="B", target="C", weight=1.0))
    return Scenario(
        scenario_id="sc-001",
        description="Simple A->B->C relay",
        graph=graph,
        source="A",
        destination="C",
        purpose="analytics",
    )


class TestScenario:
    def test_scenario_fields(self, simple_scenario: Scenario) -> None:
        assert simple_scenario.scenario_id == "sc-001"
        assert simple_scenario.source == "A"
        assert simple_scenario.destination == "C"
        assert simple_scenario.purpose == "analytics"

    def test_scenario_to_dict(self, simple_scenario: Scenario) -> None:
        data = simple_scenario.to_dict()
        assert data["scenario_id"] == "sc-001"
        assert data["source"] == "A"
        assert data["destination"] == "C"
        assert data["purpose"] == "analytics"
        assert "graph" in data

    def test_scenario_from_dict_round_trip(self, simple_scenario: Scenario) -> None:
        data = simple_scenario.to_dict()
        rebuilt = Scenario.from_dict(data)
        assert rebuilt.scenario_id == simple_scenario.scenario_id
        assert rebuilt.source == simple_scenario.source
        assert rebuilt.destination == simple_scenario.destination
        assert rebuilt.purpose == simple_scenario.purpose


class TestSimulationResult:
    def test_result_success(self) -> None:
        result = SimulationResult(
            scenario_id="sc-001",
            success=True,
            path=["A", "B", "C"],
            hops=2,
            message="Path found.",
        )
        assert result.success is True
        assert result.hops == 2
        assert result.path == ["A", "B", "C"]

    def test_result_failure(self) -> None:
        result = SimulationResult(
            scenario_id="sc-002",
            success=False,
            path=None,
            hops=0,
            message="No consent path found.",
        )
        assert result.success is False
        assert result.path is None

    def test_result_to_dict(self) -> None:
        result = SimulationResult(
            scenario_id="sc-001",
            success=True,
            path=["A", "C"],
            hops=1,
            message="OK",
        )
        data = result.to_dict()
        assert data["success"] is True
        assert data["hops"] == 1
        assert data["scenario_id"] == "sc-001"


class TestSimulationEngine:
    def test_run_success(self, simple_scenario: Scenario) -> None:
        engine = SimulationEngine()
        result = engine.run(simple_scenario)
        assert result.success is True
        assert result.path is not None
        assert result.path[0] == "A"
        assert result.path[-1] == "C"

    def test_run_no_consent(self) -> None:
        graph = ConsentRelayGraph()
        graph.add_node(Node(node_id="A", consented_purposes={"analytics"}))
        graph.add_node(Node(node_id="B", consented_purposes=set()))  # no consent
        graph.add_edge(Edge(source="A", target="B", weight=1.0))
        scenario = Scenario(
            scenario_id="sc-003",
            description="B has no consent for marketing",
            graph=graph,
            source="A",
            destination="B",
            purpose="marketing",
        )
        engine = SimulationEngine()
        result = engine.run(scenario)
        assert result.success is False

    def test_run_unknown_destination(self, simple_scenario: Scenario) -> None:
        graph = ConsentRelayGraph()
        graph.add_node(Node(node_id="A", consented_purposes={"analytics"}))
        scenario = Scenario(
            scenario_id="sc-004",
            description="Destination does not exist",
            graph=graph,
            source="A",
            destination="Z",
            purpose="analytics",
        )
        engine = SimulationEngine()
        result = engine.run(scenario)
        assert result.success is False

    def test_run_batch(self, simple_scenario: Scenario) -> None:
        engine = SimulationEngine()
        results = engine.run_batch([simple_scenario, simple_scenario])
        assert len(results) == 2
        assert all(r.success for r in results)

    def test_summary_stats(self, simple_scenario: Scenario) -> None:
        engine = SimulationEngine()
        results = engine.run_batch([simple_scenario])
        stats = engine.summary_stats(results)
        assert stats["total"] == 1
        assert stats["successful"] == 1
        assert stats["failed"] == 0
        assert stats["success_rate"] == 1.0
