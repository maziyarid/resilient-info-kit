"""Unit tests for resilient_info_kit.deploy module."""

import pytest
from resilient_info_kit.deploy import (
    RelayNodeConfig,
    RelayNodeStub,
    DeploymentManager,
    NodeStatus,
)


@pytest.fixture
def node_config() -> RelayNodeConfig:
    return RelayNodeConfig(
        node_id="relay-001",
        host="127.0.0.1",
        port=9000,
        consented_purposes={"analytics", "research"},
        max_hops=5,
    )


@pytest.fixture
def relay_stub(node_config: RelayNodeConfig) -> RelayNodeStub:
    return RelayNodeStub(config=node_config)


class TestRelayNodeConfig:
    def test_config_fields(self, node_config: RelayNodeConfig) -> None:
        assert node_config.node_id == "relay-001"
        assert node_config.host == "127.0.0.1"
        assert node_config.port == 9000
        assert "analytics" in node_config.consented_purposes
        assert node_config.max_hops == 5

    def test_config_to_dict(self, node_config: RelayNodeConfig) -> None:
        data = node_config.to_dict()
        assert data["node_id"] == "relay-001"
        assert data["host"] == "127.0.0.1"
        assert data["port"] == 9000
        assert "analytics" in data["consented_purposes"]

    def test_config_from_dict_round_trip(self, node_config: RelayNodeConfig) -> None:
        data = node_config.to_dict()
        rebuilt = RelayNodeConfig.from_dict(data)
        assert rebuilt.node_id == node_config.node_id
        assert rebuilt.port == node_config.port
        assert rebuilt.consented_purposes == node_config.consented_purposes


class TestRelayNodeStub:
    def test_initial_status(self, relay_stub: RelayNodeStub) -> None:
        assert relay_stub.status == NodeStatus.STOPPED

    def test_start(self, relay_stub: RelayNodeStub) -> None:
        relay_stub.start()
        assert relay_stub.status == NodeStatus.RUNNING

    def test_stop(self, relay_stub: RelayNodeStub) -> None:
        relay_stub.start()
        relay_stub.stop()
        assert relay_stub.status == NodeStatus.STOPPED

    def test_double_start(self, relay_stub: RelayNodeStub) -> None:
        relay_stub.start()
        relay_stub.start()  # idempotent
        assert relay_stub.status == NodeStatus.RUNNING

    def test_relay_message_running(self, relay_stub: RelayNodeStub) -> None:
        relay_stub.start()
        result = relay_stub.relay(payload={"data": "test"}, purpose="analytics")
        assert result["accepted"] is True
        assert result["node_id"] == "relay-001"

    def test_relay_message_no_consent(self, relay_stub: RelayNodeStub) -> None:
        relay_stub.start()
        result = relay_stub.relay(payload={"data": "ads"}, purpose="advertising")
        assert result["accepted"] is False

    def test_relay_message_stopped(self, relay_stub: RelayNodeStub) -> None:
        result = relay_stub.relay(payload={"data": "test"}, purpose="analytics")
        assert result["accepted"] is False

    def test_get_info(self, relay_stub: RelayNodeStub) -> None:
        info = relay_stub.get_info()
        assert info["node_id"] == "relay-001"
        assert "status" in info
        assert "consented_purposes" in info


class TestDeploymentManager:
    def test_register_node(self, node_config: RelayNodeConfig) -> None:
        manager = DeploymentManager()
        manager.register(node_config)
        assert "relay-001" in manager.list_nodes()

    def test_start_node(self, node_config: RelayNodeConfig) -> None:
        manager = DeploymentManager()
        manager.register(node_config)
        manager.start_node("relay-001")
        assert manager.get_status("relay-001") == NodeStatus.RUNNING

    def test_stop_node(self, node_config: RelayNodeConfig) -> None:
        manager = DeploymentManager()
        manager.register(node_config)
        manager.start_node("relay-001")
        manager.stop_node("relay-001")
        assert manager.get_status("relay-001") == NodeStatus.STOPPED

    def test_start_all(self, node_config: RelayNodeConfig) -> None:
        manager = DeploymentManager()
        config2 = RelayNodeConfig(
            node_id="relay-002",
            host="127.0.0.1",
            port=9001,
            consented_purposes={"research"},
            max_hops=3,
        )
        manager.register(node_config)
        manager.register(config2)
        manager.start_all()
        assert manager.get_status("relay-001") == NodeStatus.RUNNING
        assert manager.get_status("relay-002") == NodeStatus.RUNNING

    def test_stop_all(self, node_config: RelayNodeConfig) -> None:
        manager = DeploymentManager()
        manager.register(node_config)
        manager.start_all()
        manager.stop_all()
        assert manager.get_status("relay-001") == NodeStatus.STOPPED

    def test_unknown_node_raises(self) -> None:
        manager = DeploymentManager()
        with pytest.raises(KeyError):
            manager.start_node("nonexistent")

    def test_summary(self, node_config: RelayNodeConfig) -> None:
        manager = DeploymentManager()
        manager.register(node_config)
        manager.start_all()
        summary = manager.summary()
        assert summary["total"] == 1
        assert summary["running"] == 1
        assert summary["stopped"] == 0
