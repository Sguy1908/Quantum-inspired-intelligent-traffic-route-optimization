"""Reproducible, time-dependent traffic environments.

Traffic is deliberately read-only from an optimiser's perspective. A model
answers congestion/travel-time queries; it never changes a shared graph while
an experiment is running. This makes static and dynamic experiments differ
only in the environment seen by the common evaluator.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
import numpy as np


class TrafficModel(Protocol):
    def congestion(self, u: int, v: int, time: float) -> float: ...
    def travel_time(self, base_travel_time: float, u: int, v: int, time: float) -> float: ...
    def metadata(self) -> dict: ...


@dataclass(frozen=True)
class StaticTrafficModel:
    """Fixed per-edge congestion state, ``C_ij(t)=C_ij``."""
    congestion_by_edge: dict[tuple[int, int], float]
    alpha: float = 1.0

    def congestion(self, u: int, v: int, time: float = 0.0) -> float:
        return float(self.congestion_by_edge.get((u, v), 0.0))

    def travel_time(self, base_travel_time: float, u: int, v: int, time: float = 0.0) -> float:
        return base_travel_time * (1.0 + self.alpha * self.congestion(u, v, time))

    def metadata(self) -> dict:
        return {"mode": "static", "alpha": self.alpha,
                "congestion_by_edge": {f"{u},{v}": c for (u, v), c in self.congestion_by_edge.items()}}


@dataclass(frozen=True)
class DynamicTrafficModel:
    """Deterministic traffic: ``clip(base + amplitude*sin(2πt/T + phase))``."""
    base_by_edge: dict[tuple[int, int], float]
    amplitude_by_edge: dict[tuple[int, int], float]
    phase_by_edge: dict[tuple[int, int], float]
    period: float = 240.0
    c_max: float = 1.5
    alpha: float = 1.0

    @classmethod
    def from_graph(cls, transport_graph, seed: int = 42, base_range=(0.05, 0.25),
                   amplitude_range=(0.05, 0.25), period: float = 240.0,
                   c_max: float = 1.5, alpha: float = 1.0) -> "DynamicTrafficModel":
        rng = np.random.default_rng(seed)
        edges = sorted(transport_graph.graph.edges())
        return cls(
            {e: float(rng.uniform(*base_range)) for e in edges},
            {e: float(rng.uniform(*amplitude_range)) for e in edges},
            {e: float(rng.uniform(0.0, 2.0 * np.pi)) for e in edges},
            period, c_max, alpha,
        )

    def congestion(self, u: int, v: int, time: float = 0.0) -> float:
        base = self.base_by_edge.get((u, v), 0.0)
        amplitude = self.amplitude_by_edge.get((u, v), 0.0)
        phase = self.phase_by_edge.get((u, v), 0.0)
        return float(np.clip(base + amplitude * np.sin(2.0 * np.pi * time / self.period + phase), 0.0, self.c_max))

    def travel_time(self, base_travel_time: float, u: int, v: int, time: float = 0.0) -> float:
        return base_travel_time * (1.0 + self.alpha * self.congestion(u, v, time))

    def metadata(self) -> dict:
        return {"mode": "dynamic", "period": self.period, "c_max": self.c_max, "alpha": self.alpha,
                "base_by_edge": {f"{u},{v}": c for (u, v), c in self.base_by_edge.items()},
                "amplitude_by_edge": {f"{u},{v}": c for (u, v), c in self.amplitude_by_edge.items()},
                "phase_by_edge": {f"{u},{v}": c for (u, v), c in self.phase_by_edge.items()}}


def static_traffic_from_graph(transport_graph, alpha: float = 1.0) -> StaticTrafficModel:
    return StaticTrafficModel({(u, v): float(d.get("congestion", 0.0))
                               for u, v, d in transport_graph.graph.edges(data=True)}, alpha)
