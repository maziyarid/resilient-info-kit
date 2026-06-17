"""
resilient_info_kit — Consent Relay Testbed Research Prototype.

RESEARCH USE ONLY. This package provides:
- A graph-theoretic model for consent-based relay routing (model.py)
- Scenario I/O and simulation orchestration (simulate.py)
- A deployable Docker testbed for empirical collateral damage measurement (testbed/)
- A CLI entry point (cli.py)

All testbed operations must be run in isolated Docker/VM environments only.
No real-world traffic is proxied. See MANIFEST.md for ethical boundaries.
"""

__version__ = "0.2.0"
__all__ = ["model", "simulate", "cli", "testbed"]
