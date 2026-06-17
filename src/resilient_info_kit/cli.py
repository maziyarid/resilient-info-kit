"""cli.py - Command-line entry point for resilient_info_kit.

RESEARCH USE ONLY. Provides a CLI interface for running consent relay
simulations and inspecting scenario results.

Usage examples::

    resilient-info-kit run scenario.json
    resilient-info-kit run scenario.json --output report.json
    resilient-info-kit inspect scenario.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from . import __version__
from .simulate import load_scenario, run_simulation, save_report

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        format="%(levelname)s %(name)s: %(message)s",
        level=level,
    )


# ---------------------------------------------------------------------------
# Sub-commands
# ---------------------------------------------------------------------------


def cmd_run(args: argparse.Namespace) -> int:
    """Execute a simulation scenario and optionally save a report."""
    scenario_path = Path(args.scenario)
    if not scenario_path.exists():
        print(f"Error: scenario file not found: {scenario_path}", file=sys.stderr)
        return 1

    config = load_scenario(scenario_path)
    report = run_simulation(config)

    summary = {
        "scenario": report.scenario_name,
        "total_routes": report.total_routes,
        "successful_routes": report.successful_routes,
        "failed_routes": report.failed_routes,
        "success_rate_pct": round(report.success_rate * 100, 2),
    }
    print(json.dumps(summary, indent=2))

    if args.output:
        output_path = Path(args.output)
        save_report(report, output_path)
        print(f"Full report written to: {output_path}")

    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    """Pretty-print the graph structure of a scenario file."""
    scenario_path = Path(args.scenario)
    if not scenario_path.exists():
        print(f"Error: scenario file not found: {scenario_path}", file=sys.stderr)
        return 1

    config = load_scenario(scenario_path)
    graph_dict = config.graph.to_dict()

    print(f"Scenario : {config.name}")
    print(f"Nodes    : {len(graph_dict['nodes'])}")
    print(f"Edges    : {len(graph_dict['edges'])}")
    print(f"Routes   : {len(config.routes)}")
    print()
    print("-- Graph (JSON) --")
    print(json.dumps(graph_dict, indent=2))
    return 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="resilient-info-kit",
        description="Consent Relay Testbed Research Prototype (RESEARCH USE ONLY).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug-level logging.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # run
    run_p = sub.add_parser("run", help="Run a simulation scenario.")
    run_p.add_argument("scenario", help="Path to scenario JSON file.")
    run_p.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write full JSON report to FILE.",
    )
    run_p.set_defaults(func=cmd_run)

    # inspect
    inspect_p = sub.add_parser("inspect", help="Inspect a scenario graph.")
    inspect_p.add_argument("scenario", help="Path to scenario JSON file.")
    inspect_p.set_defaults(func=cmd_inspect)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """CLI entry point; returns an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    _configure_logging(args.verbose)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
