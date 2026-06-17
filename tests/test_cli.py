"""Unit tests for resilient_info_kit.cli module."""

import json
import pytest
from click.testing import CliRunner
from resilient_info_kit.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def scenario_file(tmp_path):
    """Write a minimal scenario JSON to a temp file."""
    scenario = {
        "scenario_id": "sc-cli-001",
        "description": "CLI test scenario",
        "source": "A",
        "destination": "C",
        "purpose": "analytics",
        "graph": {
            "nodes": [
                {"node_id": "A", "consented_purposes": ["analytics"]},
                {"node_id": "B", "consented_purposes": ["analytics"]},
                {"node_id": "C", "consented_purposes": ["analytics"]},
            ],
            "edges": [
                {"source": "A", "target": "B", "weight": 1.0},
                {"source": "B", "target": "C", "weight": 1.0},
            ],
        },
    }
    p = tmp_path / "scenario.json"
    p.write_text(json.dumps(scenario))
    return str(p)


class TestCliRun:
    def test_run_success(self, runner: CliRunner, scenario_file: str) -> None:
        result = runner.invoke(cli, ["run", scenario_file])
        assert result.exit_code == 0
        assert "success" in result.output.lower()

    def test_run_missing_file(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["run", "/nonexistent/path/scenario.json"])
        assert result.exit_code != 0

    def test_run_json_output(self, runner: CliRunner, scenario_file: str) -> None:
        result = runner.invoke(cli, ["run", "--output", "json", scenario_file])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "success" in data
        assert "scenario_id" in data

    def test_run_no_consent_path(self, runner: CliRunner, tmp_path) -> None:
        scenario = {
            "scenario_id": "sc-cli-002",
            "description": "No consent path",
            "source": "A",
            "destination": "B",
            "purpose": "marketing",
            "graph": {
                "nodes": [
                    {"node_id": "A", "consented_purposes": ["analytics"]},
                    {"node_id": "B", "consented_purposes": []},
                ],
                "edges": [
                    {"source": "A", "target": "B", "weight": 1.0},
                ],
            },
        }
        p = tmp_path / "no_consent.json"
        p.write_text(json.dumps(scenario))
        result = runner.invoke(cli, ["run", str(p)])
        assert result.exit_code == 0
        assert "fail" in result.output.lower() or "no" in result.output.lower()


class TestCliVersion:
    def test_version(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower() or "." in result.output


class TestCliHelp:
    def test_help(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "usage" in result.output.lower() or "commands" in result.output.lower()

    def test_run_help(self, runner: CliRunner) -> None:
        result = runner.invoke(cli, ["run", "--help"])
        assert result.exit_code == 0
