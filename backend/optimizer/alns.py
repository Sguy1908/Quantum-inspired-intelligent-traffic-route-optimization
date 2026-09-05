"""Adaptive Large Neighbourhood Search baseline for the shared VRP model."""
from __future__ import annotations

import os
import sys
import time
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.optimizer.base import BaseOptimizer, OptimizationResult
from backend.optimizer.encoding import decode_random_keys
from backend.optimizer.objective import ObjectiveEvaluator
from backend.optimizer.vrp_instance import VRPInstance


class ALNSOptimizer(BaseOptimizer):
    """ALNS with adaptive random/worst removal and greedy/regret insertion.

    It uses route solutions directly, but every candidate is assessed by the
    exact same ``ObjectiveEvaluator`` used by QPSO.
    """
    def __init__(self, instance: VRPInstance, seed: int = 42,
                 evaluator: ObjectiveEvaluator | None = None,
                 destroy_fraction: tuple[float, float] = (0.10, 0.30),
                 reaction_factor: float = 0.2, initial_temperature: float = 0.05):
        super().__init__(instance, seed, evaluator)
        self.destroy_fraction = destroy_fraction
        self.reaction_factor = reaction_factor
        self.initial_temperature = initial_temperature

    def _evaluate(self, routes):
        return self.evaluate_routes(routes)

    def _initial_routes(self):
        return decode_random_keys(self.rng.random(self.instance.num_customers), self.instance)

    @staticmethod
    def _customers(routes):
        return [n for r in routes for n in r[1:-1]]

    def _destroy(self, routes, kind: int, count: int):
        customers = self._customers(routes)
        if kind == 0:
            removed = set(self.rng.choice(customers, min(count, len(customers)), replace=False).tolist())
        else:  # route removal: perturb the largest routes without hidden evaluations
            ordered = [node for route in sorted(routes, key=lambda r: len(r), reverse=True) for node in route[1:-1]]
            removed = set(ordered[:count])
        partial = []
        for route in routes:
            retained = [n for n in route[1:-1] if n not in removed]
            if retained:
                partial.append([self.instance.depot, *retained, self.instance.depot])
        return partial, list(removed)

    def _repair(self, routes, removed, kind: int, max_evaluations: int | None):
        pending = list(removed)
        while pending and (max_evaluations is None or self.objective_evaluations < max_evaluations):
            # Regret-2 selects the customer whose second-best insertion is costly.
            choices = []
            for customer in pending:
                insertions = []
                candidates = list(range(len(routes))) + ([len(routes)] if len(routes) < self.instance.num_vehicles else [])
                for ri in candidates:
                    route = routes[ri] if ri < len(routes) else [self.instance.depot, self.instance.depot]
                    for pos in range(1, len(route)):
                        candidate = [r[:] for r in routes]
                        if ri == len(candidate): candidate.append(route[:])
                        candidate[ri].insert(pos, customer)
                        metric = self._evaluate(candidate)
                        insertions.append((metric["fitness"], candidate))
                        if max_evaluations is not None and self.objective_evaluations >= max_evaluations: break
                    if max_evaluations is not None and self.objective_evaluations >= max_evaluations: break
                if insertions:
                    insertions.sort(key=lambda x: x[0])
                    regret = (insertions[min(1, len(insertions)-1)][0] - insertions[0][0]) if kind else 0.0
                    choices.append((regret, customer, insertions[0][1], insertions[0][0]))
                if max_evaluations is not None and self.objective_evaluations >= max_evaluations: break
            if not choices: break
            _, customer, routes, _ = max(choices, key=lambda x: x[0]) if kind else min(choices, key=lambda x: x[3])
            pending.remove(customer)
        # If budget ended, retain explicit violation rather than silently dropping customers.
        if pending:
            routes = [r[:] for r in routes] + [[self.instance.depot, *pending, self.instance.depot]]
        return routes

    def optimize(self, max_iterations: int = 200, time_step: int = 0,
                 max_evaluations: int | None = None) -> OptimizationResult:
        start = time.perf_counter()
        current = self._initial_routes()
        current_metrics = self._evaluate(current)
        best, best_metrics = [r[:] for r in current], current_metrics
        weights = np.ones((2, 2))  # destroy × repair
        convergence = [{"evaluations": self.objective_evaluations, "best_fitness": best_metrics["fitness"]}]
        temperature = max(1e-9, self.initial_temperature * max(1.0, best_metrics["fitness"]))
        for _ in range(max_iterations):
            if max_evaluations is not None and self.objective_evaluations >= max_evaluations: break
            flat = weights.ravel() / weights.sum()
            operator = int(self.rng.choice(4, p=flat)); destroy_kind, repair_kind = divmod(operator, 2)
            n_remove = int(self.rng.integers(max(1, round(self.destroy_fraction[0] * self.instance.num_customers)),
                                              max(2, round(self.destroy_fraction[1] * self.instance.num_customers)) + 1))
            partial, removed = self._destroy(current, destroy_kind, n_remove)
            candidate = self._repair(partial, removed, repair_kind, max_evaluations)
            if max_evaluations is not None and self.objective_evaluations >= max_evaluations: break
            candidate_metrics = self._evaluate(candidate)
            delta = candidate_metrics["fitness"] - current_metrics["fitness"]
            accepted = delta <= 0 or self.rng.random() < np.exp(-delta / temperature)
            score = 0.0
            if accepted:
                current, current_metrics, score = candidate, candidate_metrics, 1.0
            if candidate_metrics["fitness"] < best_metrics["fitness"]:
                best, best_metrics, score = [r[:] for r in candidate], candidate_metrics, 5.0
            weights[destroy_kind, repair_kind] = ((1 - self.reaction_factor) * weights[destroy_kind, repair_kind]
                                                  + self.reaction_factor * max(0.1, score))
            temperature *= 0.995
            convergence.append({"evaluations": self.objective_evaluations, "best_fitness": best_metrics["fitness"]})
        return OptimizationResult(best, best_metrics["fitness"], best_metrics, convergence,
                                  time.perf_counter() - start, self.objective_evaluations)
