"""deploy.py - Deployable relay node stub.

RESEARCH USE ONLY. Provides a lightweight stub that represents a
deployable consent relay node in testbed experiments. No actual
network traffic is generated or forwarded.
"""

from __future__ import annotations

import dataclasses
import logging
import threading
from typing import Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# Type alias for a relay handler function.
RelayHandler = Callable[[str, str, str], Optional[List[str]]]


# ---------------------------------------------------------------------------
# Node configuration
# ---------------------------------------------------------------------------


@dataclasses.dataclass
class NodeConfig:
    """Runtime configuration for a deployable relay node."""

    node_id: str
    consents: List[str] = dataclasses.field(default_factory=list)
    max_hops: int = 10
    """Maximum number of relay hops before a route is rejected."""
    metadata: Dict[str, str] = dataclasses.field(default_factory=dict)


# ---------------------------------------------------------------------------
# Relay node stub
# ---------------------------------------------------------------------------


class RelayNode:
    """Stub implementation of a deployable consent relay node.

    In a real deployment this class would manage a network socket and
    forward traffic to peer nodes. In the testbed it simply records
    relay requests and invokes an in-process handler for routing.

    All relay operations are simulated in-memory. No real network I/O
    is performed.
    """

    def __init__(self, config: NodeConfig, handler: Optional[RelayHandler] = None) -> None:
        self._config = config
        self._handler = handler
        self._lock = threading.Lock()
        self._relay_log: List[Dict] = []
        self._running = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Mark the node as running."""
        with self._lock:
            if self._running:
                logger.warning("Node %s is already running.", self._config.node_id)
                return
            self._running = True
        logger.info("Relay node %s started (RESEARCH STUB).", self._config.node_id)

    def stop(self) -> None:
        """Mark the node as stopped."""
        with self._lock:
            self._running = False
        logger.info("Relay node %s stopped.", self._config.node_id)

    @property
    def is_running(self) -> bool:
        """Return True if the node is in the running state."""
        with self._lock:
            return self._running

    # ------------------------------------------------------------------
    # Relay logic
    # ------------------------------------------------------------------

    def relay(
        self,
        source: str,
        target: str,
        purpose: str,
    ) -> Optional[List[str]]:
        """Attempt to relay a request from *source* to *target* for *purpose*.

        Returns the resolved path (list of node IDs) on success, or
        ``None`` if the relay cannot be completed.

        This method is thread-safe.
        """
        if not self.is_running:
            logger.error(
                "Relay request rejected — node %s is not running.",
                self._config.node_id,
            )
            return None

        if purpose not in self._config.consents:
            logger.warning(
                "Node %s has not consented to purpose '%s'; relay denied.",
                self._config.node_id,
                purpose,
            )
            path = None
        elif self._handler is not None:
            path = self._handler(source, target, purpose)
        else:
            # No external handler — trivially return a direct path.
            path = [source, self._config.node_id, target]

        with self._lock:
            self._relay_log.append(
                {
                    "source": source,
                    "target": target,
                    "purpose": purpose,
                    "path": path,
                    "success": path is not None,
                }
            )

        return path

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def relay_log(self) -> List[Dict]:
        """Return a copy of the relay audit log."""
        with self._lock:
            return list(self._relay_log)

    def summary(self) -> Dict:
        """Return a concise summary of this node's relay activity."""
        log = self.relay_log()
        successful = sum(1 for e in log if e["success"])
        return {
            "node_id": self._config.node_id,
            "running": self.is_running,
            "total_relays": len(log),
            "successful_relays": successful,
            "failed_relays": len(log) - successful,
        }


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------


def create_node(
    node_id: str,
    consents: Optional[List[str]] = None,
    handler: Optional[RelayHandler] = None,
    **kwargs,
) -> RelayNode:
    """Convenience factory for creating and starting a :class:`RelayNode`."""
    config = NodeConfig(
        node_id=node_id,
        consents=consents or [],
        **kwargs,
    )
    node = RelayNode(config=config, handler=handler)
    node.start()
    return node
