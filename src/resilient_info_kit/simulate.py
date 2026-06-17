"""simulate.py - Scenario I/O and simulation orchestration.

RESEARCH USE ONLY. Provides utilities to load scenario definitions,
orchestrate relay simulations using the consent graph model, and
collect result statistics.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .model import ConsentRelayGraph, Edge, Node

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class ScenarioConfig:
    """Configuration for a single simulation scenario."""

    name: str
    graph: ConsentRelayGraph
    routes: List[Dict[str, str]] = field(default_factory=list)
    """Each route dict has keys ``source``, ``target``, and ``purpose``."""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RouteResult:
    """Result of a single route simulation attempt."""

    source: str
    target: str
    purpose: str
    path: Optional[List[str]]
    success: bool
    elapsed_ms: float


@dataclass
class SimulationReport:
    """Aggregated report for an entire scenario run."""

    scenario_name: str
    total_routes: int
    successful_routes: int
    failed_routes: int
    results: List[RouteResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Fraction of routes that succeeded (0.0 – 1.0)."""
        if self.total_routes == 0:
            return 0.0
        return self.successful_routes / self.total_routes

    def to_dict(self) -> dict:
        """Return a JSON-serialisable summary."""
        return {
            "scenario_name": self.scenario_name,
            "total_routes": self.total_routes,
            "successful_routes": self.successful_routes,
            "failed_routes": self.failed_routes,
            "success_rate": self.success_rate,
            "results": [
                {
                    "source": r.source,
                    "target": r.target,
                    "purpose": r.purpose,
                    "path": r.path,
                    "success": r.success,
                    "elapsed_ms": r.elapsed_ms,
                }
                for r in self.results
            ],
        }


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def load_scenario(path: Path) -> ScenarioConfig:
    """Load a :class:`ScenarioConfig` from a JSON file at *path*.

    Expected JSON structure::

        {
            "name": "example",
            "graph": { "nodes": [...], "edges": [...] },
            "routes": [
                {"source": "A", "target": "C", "purpose": "analytics"}
            ],
            "metadata": {}
        }
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    graph = ConsentRelayGraph.from_dict(raw.get("graph", {}))
    return ScenarioConfig(
        name=raw.get("name", path.stem),
        graph=graph,
        routes=raw.get("routes", []),
        metadata=raw.get("metadata", {}),
    )


def save_report(report: SimulationReport, path: Path) -> None:
    """Write *report* as JSON to *path*."""
    Path(path).write_text(
        json.dumps(report.to_dict(), indent=2),
        encoding="utf-8",
    )
    logger.info("Report written to %s", path)


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def run_simulation(config: ScenarioConfig) -> SimulationReport:
    """Execute all routes in *config* and return a :class:`SimulationReport`.

    This function is purely computational — no network I/O is performed.
    """
    logger.info(
        "Starting simulation '%s' with %d route(s).",
        config.name,
        len(config.routes),
    )

    results: List[RouteResult] = []

    for route in config.routes:
        source = route["source"]
        target = route["target"]
        purpose = route.get("purpose", "")

        t0 = time.perf_counter()
        path = config.graph.consent_path(source, target, purpose)
        elapsed_ms = (time.perf_counter() - t0) * 1_000

        result = RouteResult(
            source=source,
            target=target,
            purpose=purpose,
            path=path,
            success=path is not None,
            elapsed_ms=elapsed_ms,
        )
        results.append(result)
        logger.debug(
            "Route %s -> %s [%s]: %s",
            source,
            target,
            purpose,
            "OK" if result.success else "FAIL",
        )

    successful = sum(1 for r in results if r.success)
    report = SimulationReport(
        scenario_name=config.name,
        total_routes=len(results),
        successful_routes=successful,
        failed_routes=len(results) - successful,
        results=results,
    )
    logger.info(
        "Simulation complete. Success rate: %.1f%%",
        report.success_rate * 100,
    )
    return report
