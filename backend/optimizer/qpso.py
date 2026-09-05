"""
Quantum-Inspired Particle Swarm Optimization (QPSO)

Implements QPSO for the Vehicle Routing Problem using random-key encoding.

Key equations (Sun et al., 2004):
    mbest(t)  = (1/M) * Σ pbest_i(t)
    p_local   = φ * pbest_i + (1 - φ) * gbest,    φ ~ U(0,1)
    x_i(t+1)  = p_local ± β * |mbest - x_i(t)| * ln(1/u),   u ~ U(0,1)

The contraction-expansion coefficient β controls exploration vs exploitation
and is linearly decreased from β_max to β_min over the run.
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
    from backend.optimizer.objective import ObjectiveEvaluator
except ImportError:
    from optimizer.base import BaseOptimizer, OptimizationResult
    from optimizer.vrp_instance import VRPInstance
    from optimizer.encoding import decode_random_keys
    from optimizer.objective import ObjectiveEvaluator


class QPSOOptimizer(BaseOptimizer):
    """QPSO optimizer for the Capacitated VRP with Time Windows."""

    def __init__(
        self,
        instance: VRPInstance,
        num_particles: int = 50,
        beta_max: float = 1.0,
        beta_min: float = 0.5,
        seed: int = 42,
        evaluator: ObjectiveEvaluator | None = None,
    ):
        """
        Parameters
        ----------
        instance : VRPInstance
            The VRP problem to solve.
        num_particles : int
            Swarm size M.
        beta_max : float
            Initial contraction-expansion coefficient (exploration).
        beta_min : float
            Final contraction-expansion coefficient (exploitation).
        seed : int
            Random seed for reproducibility.
        """
        super().__init__(instance, seed, evaluator)
        self.num_particles = num_particles
        self.beta_max = beta_max
        self.beta_min = beta_min

    def optimize(
        self,
        max_iterations: int = 200,
        time_step: int = 0,
        max_evaluations: int | None = None,
    ) -> OptimizationResult:
        """Run the QPSO optimization loop.

        Parameters
        ----------
        max_iterations : int
            Number of QPSO iterations.
        time_step : int
            Current discrete time step for dynamic edge costs.

        Returns
        -------
        OptimizationResult
        """
        t_start = time.perf_counter()
        dim = self.instance.num_customers
        M = self.num_particles

        # ------------------------------------------------------------------
        # Initialise swarm: random keys in [0, 1]
        # ------------------------------------------------------------------
        positions = self.rng.random((M, dim))
        pbest_positions = positions.copy()
        pbest_fitness = np.full(M, np.inf)
        gbest_position = np.zeros(dim)
        gbest_fitness = np.inf

        convergence: list[float] = []

        # Evaluate initial population
        for i in range(M):
            routes = decode_random_keys(positions[i], self.instance, time_step)
            result = self.evaluate_routes(routes)
            fitness = result["fitness"]
            pbest_fitness[i] = fitness
            if fitness < gbest_fitness:
                gbest_fitness = fitness
                gbest_position = positions[i].copy()

        convergence.append({"evaluations": self.objective_evaluations, "best_fitness": float(gbest_fitness)})

        # ------------------------------------------------------------------
        # Main QPSO loop
        # ------------------------------------------------------------------
        for iteration in range(1, max_iterations + 1):
            if max_evaluations is not None and self.objective_evaluations >= max_evaluations:
                break
            # Linearly decrease β from β_max → β_min
            beta = (
                self.beta_max
                - (self.beta_max - self.beta_min) * iteration / max_iterations
            )

            # Mean best position (mbest)
            mbest = pbest_positions.mean(axis=0)

            for i in range(M):
                if max_evaluations is not None and self.objective_evaluations >= max_evaluations:
                    break
                # Stochastic local attractor
                phi = self.rng.random(dim)
                p_local = phi * pbest_positions[i] + (1.0 - phi) * gbest_position

                # QPSO position update
                u = self.rng.random(dim)
                # Avoid log(0)
                u = np.clip(u, 1e-10, 1.0)

                delta = beta * np.abs(mbest - positions[i]) * np.log(1.0 / u)

                # ± with equal probability
                direction = self.rng.choice([-1.0, 1.0], size=dim)
                new_pos = p_local + direction * delta

                # Clamp to [0, 1] (valid random-key range)
                new_pos = np.clip(new_pos, 0.0, 1.0)
                positions[i] = new_pos

                # Evaluate new position
                routes = decode_random_keys(
                    positions[i], self.instance, time_step
                )
                result = self.evaluate_routes(routes)
                fitness = result["fitness"]

                # Update personal best
                if fitness < pbest_fitness[i]:
                    pbest_fitness[i] = fitness
                    pbest_positions[i] = positions[i].copy()

                # Update global best
                if fitness < gbest_fitness:
                    gbest_fitness = fitness
                    gbest_position = positions[i].copy()

            convergence.append({"evaluations": self.objective_evaluations, "best_fitness": float(gbest_fitness)})

        # ------------------------------------------------------------------
        # Build final result
        # ------------------------------------------------------------------
        best_routes = decode_random_keys(
            gbest_position, self.instance, time_step
        )
        best_metrics = self.evaluator.evaluate(best_routes)
        elapsed = time.perf_counter() - t_start

        return OptimizationResult(
            best_routes=best_routes,
            best_fitness=gbest_fitness,
            metrics=best_metrics,
            convergence_history=convergence,
            runtime_seconds=elapsed,
            objective_evaluations=self.objective_evaluations,
        )
