"""
Standard Particle Swarm Optimization (PSO) — Baseline

Classical velocity-based PSO for VRP using the same random-key encoding
as QPSO, enabling fair head-to-head comparison.
"""

from __future__ import annotations

import time
import os
import sys

import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from backend.optimizer.base import BaseOptimizer, OptimizationResult
    from backend.optimizer.vrp_instance import VRPInstance
    from backend.optimizer.encoding import decode_random_keys
    from backend.optimizer.objective import evaluate_solution
except ImportError:
    from optimizer.base import BaseOptimizer, OptimizationResult
    from optimizer.vrp_instance import VRPInstance
    from optimizer.encoding import decode_random_keys
    from optimizer.objective import evaluate_solution


class PSOOptimizer(BaseOptimizer):
    """Standard PSO baseline for the VRP."""

    def __init__(
        self,
        instance: VRPInstance,
        num_particles: int = 50,
        w: float = 0.7,
        c1: float = 1.5,
        c2: float = 1.5,
        seed: int = 42,
    ):
        """
        Parameters
        ----------
        w : float   — inertia weight
        c1 : float  — cognitive acceleration coefficient
        c2 : float  — social acceleration coefficient
        """
        super().__init__(instance, seed)
        self.num_particles = num_particles
        self.w = w
        self.c1 = c1
        self.c2 = c2

    def optimize(
        self,
        max_iterations: int = 200,
        time_step: int = 0,
    ) -> OptimizationResult:
        t_start = time.perf_counter()
        dim = self.instance.num_customers
        M = self.num_particles

        # Initialise
        positions = self.rng.random((M, dim))
        velocities = self.rng.uniform(-0.1, 0.1, (M, dim))
        pbest_positions = positions.copy()
        pbest_fitness = np.full(M, np.inf)
        gbest_position = np.zeros(dim)
        gbest_fitness = np.inf
        convergence: list[float] = []

        # Initial evaluation
        for i in range(M):
            routes = decode_random_keys(positions[i], self.instance, time_step)
            result = evaluate_solution(routes, self.instance, time_step)
            fitness = result["fitness"]
            pbest_fitness[i] = fitness
            if fitness < gbest_fitness:
                gbest_fitness = fitness
                gbest_position = positions[i].copy()
        convergence.append(float(gbest_fitness))

        # Main loop
        for iteration in range(1, max_iterations + 1):
            for i in range(M):
                r1 = self.rng.random(dim)
                r2 = self.rng.random(dim)

                velocities[i] = (
                    self.w * velocities[i]
                    + self.c1 * r1 * (pbest_positions[i] - positions[i])
                    + self.c2 * r2 * (gbest_position - positions[i])
                )
                positions[i] = np.clip(positions[i] + velocities[i], 0.0, 1.0)

                routes = decode_random_keys(
                    positions[i], self.instance, time_step
                )
                result = evaluate_solution(routes, self.instance, time_step)
                fitness = result["fitness"]

                if fitness < pbest_fitness[i]:
                    pbest_fitness[i] = fitness
                    pbest_positions[i] = positions[i].copy()
                if fitness < gbest_fitness:
                    gbest_fitness = fitness
                    gbest_position = positions[i].copy()

            convergence.append(float(gbest_fitness))

        best_routes = decode_random_keys(
            gbest_position, self.instance, time_step
        )
        best_metrics = evaluate_solution(best_routes, self.instance, time_step)
        elapsed = time.perf_counter() - t_start

        return OptimizationResult(
            best_routes=best_routes,
            best_fitness=gbest_fitness,
            metrics=best_metrics,
            convergence_history=convergence,
            runtime_seconds=elapsed,
        )
