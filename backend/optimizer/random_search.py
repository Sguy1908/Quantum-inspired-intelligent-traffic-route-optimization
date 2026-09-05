"""
Random Search — Baseline

Pure uniform random search baseline for VRP using random-key encoding.
Evaluates the same number of candidates per iteration as swarm/evolutionary methods.
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


class RandomSearchOptimizer(BaseOptimizer):
    """Uniform Random Search baseline for VRP."""

    def __init__(
        self,
        instance: VRPInstance,
        num_samples_per_iter: int = 50,
        seed: int = 42,
        evaluator: ObjectiveEvaluator | None = None,
    ):
        """
        Parameters
        ----------
        instance : VRPInstance
            The VRP problem instance.
        num_samples_per_iter : int
            Number of random keys sampled per iteration (matches swarm size).
        seed : int
            Random seed.
        """
        super().__init__(instance, seed, evaluator)
        self.num_samples_per_iter = num_samples_per_iter

    def optimize(
        self,
        max_iterations: int = 200,
        time_step: int = 0,
        max_evaluations: int | None = None,
    ) -> OptimizationResult:
        t_start = time.perf_counter()
        dim = self.instance.num_customers
        M = self.num_samples_per_iter

        gbest_position = np.zeros(dim)
        gbest_fitness = np.inf
        convergence: list[dict] = []

        # Iteration 0
        samples = self.rng.random((M, dim))
        for i in range(M):
            if max_evaluations is not None and self.objective_evaluations >= max_evaluations: break
            routes = decode_random_keys(samples[i], self.instance, time_step)
            result = self.evaluate_routes(routes)
            fitness = result["fitness"]
            if fitness < gbest_fitness:
                gbest_fitness = fitness
                gbest_position = samples[i].copy()

        convergence.append({"evaluations": self.objective_evaluations, "best_fitness": float(gbest_fitness)})

        # Iterations 1 to max_iterations
        for iteration in range(1, max_iterations + 1):
            if max_evaluations is not None and self.objective_evaluations >= max_evaluations: break
            samples = self.rng.random((M, dim))
            for i in range(M):
                if max_evaluations is not None and self.objective_evaluations >= max_evaluations: break
                routes = decode_random_keys(samples[i], self.instance, time_step)
                result = self.evaluate_routes(routes)
                fitness = result["fitness"]
                if fitness < gbest_fitness:
                    gbest_fitness = fitness
                    gbest_position = samples[i].copy()

            convergence.append({"evaluations": self.objective_evaluations, "best_fitness": float(gbest_fitness)})

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
