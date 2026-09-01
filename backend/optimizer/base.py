"""
Base Optimizer Interface

All optimizers (QPSO, PSO, GA, etc.) inherit from this abstract class
so the benchmarking runner can treat them uniformly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np

try:
    from backend.optimizer.vrp_instance import VRPInstance
except ImportError:
    from optimizer.vrp_instance import VRPInstance


@dataclass
class OptimizationResult:
    """Container for the output of an optimization run."""
    best_routes: list[list[int]]
    best_fitness: float
    metrics: dict
    convergence_history: list[float] = field(default_factory=list)
    runtime_seconds: float = 0.0


class BaseOptimizer(ABC):
    """Abstract base for all metaheuristic / exact optimizers."""

    def __init__(self, instance: VRPInstance, seed: int = 42):
        self.instance = instance
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    @abstractmethod
    def optimize(self, max_iterations: int = 200,
                 time_step: int = 0) -> OptimizationResult:
        """Run the optimizer and return the best solution found.

        Parameters
        ----------
        max_iterations : int
            Maximum number of iterations / generations.
        time_step : int
            Current time step for dynamic edge costs.

        Returns
        -------
        OptimizationResult
        """
        ...

    @property
    def name(self) -> str:
        return self.__class__.__name__
