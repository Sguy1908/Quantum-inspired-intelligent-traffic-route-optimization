"""
Genetic Algorithm (GA) — Baseline

Permutation-based GA for VRP using the same random-key encoding
as QPSO/PSO for fair comparison.
"""

from __future__ import annotations

import time

import numpy as np

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


class GAOptimizer(BaseOptimizer):
    """Genetic Algorithm baseline for the VRP."""

    def __init__(
        self,
        instance: VRPInstance,
        pop_size: int = 50,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.1,
        tournament_size: int = 3,
        seed: int = 42,
    ):
        super().__init__(instance, seed)
        self.pop_size = pop_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size

    def _evaluate(self, individual: np.ndarray,
                  time_step: int) -> float:
        routes = decode_random_keys(individual, self.instance, time_step)
        result = evaluate_solution(routes, self.instance, time_step)
        return result["fitness"]

    def _tournament_select(self, population: np.ndarray,
                           fitness_vals: np.ndarray) -> np.ndarray:
        """Tournament selection."""
        candidates = self.rng.choice(
            len(population), size=self.tournament_size, replace=False
        )
        best = candidates[np.argmin(fitness_vals[candidates])]
        return population[best].copy()

    def _blend_crossover(self, p1: np.ndarray,
                         p2: np.ndarray) -> np.ndarray:
        """BLX-α crossover on random keys."""
        alpha = 0.5
        child = np.empty_like(p1)
        for d in range(len(p1)):
            lo = min(p1[d], p2[d])
            hi = max(p1[d], p2[d])
            span = hi - lo
            child[d] = self.rng.uniform(lo - alpha * span,
                                        hi + alpha * span)
        return np.clip(child, 0.0, 1.0)

    def _mutate(self, individual: np.ndarray) -> np.ndarray:
        """Gaussian mutation on random keys."""
        mask = self.rng.random(len(individual)) < self.mutation_rate
        individual[mask] += self.rng.normal(0, 0.1, mask.sum())
        return np.clip(individual, 0.0, 1.0)

    def optimize(
        self,
        max_iterations: int = 200,
        time_step: int = 0,
    ) -> OptimizationResult:
        t_start = time.perf_counter()
        dim = self.instance.num_customers
        pop_size = self.pop_size

        # Initialise population
        population = self.rng.random((pop_size, dim))
        fitness_vals = np.array([
            self._evaluate(population[i], time_step)
            for i in range(pop_size)
        ])

        best_idx = np.argmin(fitness_vals)
        gbest_fitness = fitness_vals[best_idx]
        gbest_individual = population[best_idx].copy()
        convergence = [float(gbest_fitness)]

        for generation in range(1, max_iterations + 1):
            new_pop = []
            for _ in range(pop_size):
                p1 = self._tournament_select(population, fitness_vals)
                p2 = self._tournament_select(population, fitness_vals)
                if self.rng.random() < self.crossover_rate:
                    child = self._blend_crossover(p1, p2)
                else:
                    child = p1.copy()
                child = self._mutate(child)
                new_pop.append(child)

            population = np.array(new_pop)
            fitness_vals = np.array([
                self._evaluate(population[i], time_step)
                for i in range(pop_size)
            ])

            gen_best_idx = np.argmin(fitness_vals)
            if fitness_vals[gen_best_idx] < gbest_fitness:
                gbest_fitness = fitness_vals[gen_best_idx]
                gbest_individual = population[gen_best_idx].copy()

            convergence.append(float(gbest_fitness))

        best_routes = decode_random_keys(
            gbest_individual, self.instance, time_step
        )
        best_metrics = evaluate_solution(
            best_routes, self.instance, time_step
        )
        elapsed = time.perf_counter() - t_start

        return OptimizationResult(
            best_routes=best_routes,
            best_fitness=gbest_fitness,
            metrics=best_metrics,
            convergence_history=convergence,
            runtime_seconds=elapsed,
        )
