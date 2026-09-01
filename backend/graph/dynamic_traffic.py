"""
Dynamic Traffic Model

Manages time-varying congestion on the transportation graph.
Supports three traffic profiles (normal, moderate, heavy) and
allows per-edge congestion updates to trigger route re-optimization.
"""

import numpy as np
from typing import Optional

from backend.graph.graph import TransportationGraph


# Pre-defined congestion profiles
TRAFFIC_PROFILES = {
    "normal": (0.0, 0.1),       # congestion drawn from U(0, 0.1)
    "moderate": (0.3, 0.6),     # congestion drawn from U(0.3, 0.6)
    "heavy": (0.8, 1.5),        # congestion drawn from U(0.8, 1.5)
}


class DynamicTrafficModel:
    """Applies and evolves dynamic congestion on a TransportationGraph."""

    def __init__(self, transport_graph: TransportationGraph,
                 rng: Optional[np.random.Generator] = None):
        """
        Parameters
        ----------
        transport_graph : TransportationGraph
            The graph whose edge congestion values will be mutated.
        rng : numpy random Generator, optional
            For reproducibility.
        """
        self.tg = transport_graph
        self.rng = rng or np.random.default_rng()
        self.time_step = 0
        self.history: list[dict] = []  # records of past congestion snapshots

    # ------------------------------------------------------------------
    # Bulk congestion updates
    # ------------------------------------------------------------------

    def apply_profile(self, profile: str = "normal"):
        """Set congestion on every edge according to a named traffic profile.

        Parameters
        ----------
        profile : str
            One of 'normal', 'moderate', 'heavy'.
        """
        lo, hi = TRAFFIC_PROFILES[profile]
        snapshot = {}
        for u, v in self.tg.graph.edges():
            c = float(self.rng.uniform(lo, hi))
            self.tg.graph.edges[u, v]["congestion"] = c
            snapshot[(u, v)] = c
        self.history.append({"time_step": self.time_step, "profile": profile,
                             "snapshot": snapshot})

    def apply_random_congestion(self, lo: float = 0.0, hi: float = 1.0):
        """Assign uniform random congestion in [lo, hi] to every edge."""
        for u, v in self.tg.graph.edges():
            self.tg.graph.edges[u, v]["congestion"] = float(
                self.rng.uniform(lo, hi)
            )

    # ------------------------------------------------------------------
    # Targeted congestion changes (for demonstrating re-optimization)
    # ------------------------------------------------------------------

    def set_edge_congestion(self, u: int, v: int, congestion: float,
                            bidirectional: bool = True):
        """Manually set congestion on a specific edge.

        Useful for simulating an incident or road closure.
        """
        if self.tg.graph.has_edge(u, v):
            self.tg.graph.edges[u, v]["congestion"] = congestion
        if bidirectional and self.tg.graph.has_edge(v, u):
            self.tg.graph.edges[v, u]["congestion"] = congestion

    # ------------------------------------------------------------------
    # Time-step evolution
    # ------------------------------------------------------------------

    def step(self, drift: float = 0.05):
        """Advance one time step with small random congestion drift.

        Each edge's congestion is perturbed by a small Gaussian noise,
        clamped to [0, 2].

        Parameters
        ----------
        drift : float
            Standard deviation of the Gaussian noise added each step.
        """
        self.time_step += 1
        for u, v in self.tg.graph.edges():
            old = self.tg.graph.edges[u, v].get("congestion", 0.0)
            new = old + float(self.rng.normal(0, drift))
            self.tg.graph.edges[u, v]["congestion"] = float(
                np.clip(new, 0.0, 2.0)
            )

    def __repr__(self) -> str:
        return (
            f"DynamicTrafficModel(time_step={self.time_step}, "
            f"edges={self.tg.num_edges})"
        )
