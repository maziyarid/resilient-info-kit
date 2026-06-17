# MANIFEST — Consent Relay Testbed Research Prototype

**Project:** Resilient Info Kit — Consent Relay Testbed
**Version:** 0.2.0
**Classification:** Research Prototype — Controlled Testbed Only
**License:** MIT

---

## Purpose

This repository contains the **Consent Relay Testbed**: a deployable research prototype for studying the interdependence of infrastructure nodes in a shared-access relay mesh, and for quantitatively measuring the collateral damage to co-located legitimate services when hypothetical communication restrictions are applied.

The project is designed for use by:
- Academic researchers in network resilience, internet governance, and infrastructure interdependence.
- Policy researchers and civil-society technologists studying the societal costs of large-scale communication restrictions.
- Engineers building reproducible testbeds for empirical measurement of connectivity disruption effects.

---

## What This Project Is

1. **A deployable, containerized relay mesh testbed** using Docker Compose, with each node representing an institutional participant (university, clinic, library, hosting provider, etc.).
2. **A graph-theoretic model** for analyzing consent-based routing, node/link failure propagation, and collateral reachability loss.
3. **An orchestration and measurement framework** for running controlled "shutdown" experiments: applying hypothetical blocks to relay nodes and measuring how many co-located legitimate services lose reachability as a consequence.
4. **A CLI and Python API** for scripting repeatable experiments and exporting structured results (JSON/CSV) for research analysis.

---

## What This Project Is NOT

- **Not a circumvention tool.** No component implements stealth, obfuscation, domain fronting, anti-detection, or any technique designed to evade real-world censors.
- **Not a general-purpose proxy.** All proxying is strictly allowlisted to pre-defined test endpoints within the isolated testbed network. No arbitrary external traffic is proxied.
- **Not a VPN or anonymity network.** The system does not provide anonymity, encryption for concealment, or any privacy-enhancing transport.
- **Not intended for deployment outside controlled environments.** The testbed must only be run inside Docker networks, local virtual machines, or isolated VPS clusters with no exposure to real-world internet traffic.

---

## Core Concepts

### Consent Relay Mesh
A set of institutional nodes that have explicitly opted in to relay traffic within the testbed. Each node's consent flag is a first-class attribute in the data model. Non-consenting nodes are never used as intermediate hops, ensuring the model reflects real-world voluntary participation.

### Hypothetical Shutdown Scenarios
A "shutdown" is a modeled action in which one or more relay nodes or links are marked as blocked. This represents a hypothetical administrative or technical disconnection event. The testbed applies this block by stopping Docker containers or manipulating Docker networks, and then measures reachability.

### Collateral Damage Measurement
The primary research metric is **collateral damage**: the fraction of co-located legitimate services (e.g., a clinic's patient portal hosted on the same server as a relay node) that lose reachability when the relay is blocked. This is measured concretely, by running synthetic HTTP probes from client containers to service containers before and after each shutdown event.

---

## Ethical Boundaries and Deployment Requirements

- **Isolated environments only.** The testbed MUST be run exclusively in Docker Compose networks, local VMs, or isolated VPS clusters with no bridging to the public internet.
- **No real-world traffic.** Test endpoints are synthetic services running inside the testbed. No real user traffic is ever proxied.
- **Explicit consent modeling.** Every relay node requires an explicit `consent: true` flag. This is enforced in code; non-consenting nodes cannot relay.
- **Research and education use only.** This project is intended for empirical research, academic publication, and policy education. Deployment in production environments or for operational circumvention is explicitly prohibited.

---

## Repository Structure

```
resilient-info-kit/
├── MANIFEST.md                    # This file
├── README.md                      # Project overview and quickstart
├── pyproject.toml                 # Python package configuration
├── docker/
│   ├── compose.testbed.yml        # Multi-container testbed topology
│   └── relay/
│       ├── Dockerfile             # Relay node container image
│       └── caddy/
│           └── Caddyfile          # Caddy forward proxy configuration
├── src/
│   └── resilient_info_kit/
│       ├── __init__.py
│       ├── model.py               # Graph model: Network, Node, Edge
│       ├── simulate.py            # Scenario I/O and simulation orchestration
│       ├── testbed/
│       │   ├── __init__.py
│       │   ├── orchestrator.py    # Docker testbed lifecycle management
│       │   ├── metrics.py         # Reachability probing and collateral measurement
│       │   └── shutdown.py        # Block application: container stop / network cut
│       └── cli.py                 # CLI entry point (rik)
├── examples/
│   └── testbed_scenario.json      # Example 8-node testbed scenario
├── tests/
│   └── test_model.py              # Unit tests for graph model
└── .github/
    └── workflows/
        └── ci.yml                 # GitHub Actions CI
```

---

## Novelty

This project is novel in combining:
1. **Real deployable relay nodes** (Docker containers running Caddy) rather than pure simulation.
2. **Explicit consent modeling** at the infrastructure level, enforced in both the graph model and the container configuration.
3. **Automated, quantitative collateral damage measurement** using live HTTP probes against synthetic co-located services.

This enables researchers to run repeatable, empirically grounded experiments on the question: *what is the measurable cost, in terms of legitimate service reachability, of blocking relay nodes that also host critical institutional services?*

---

*This research prototype was developed for empirical study of infrastructure interdependence and the collateral costs of communication restrictions. All experiments must be conducted in isolated, controlled environments. No real-world traffic is involved.*
