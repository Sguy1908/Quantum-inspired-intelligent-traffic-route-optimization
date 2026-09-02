"""
Benchmark Runner

Executes multi-trial benchmark experiments comparing QPSO, PSO, GA, and Random Search
under controlled, identical conditions (same graphs, VRP instances, population size, iteration count).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Any

import numpy as np

import os
import sys

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.simulator.engine import build_sample_graph, build_sample_vrp, Simulator
from backend.optimizer.base import OptimizationResult
# except ImportError:
#     from simulator.engine import build_sample_graph, build_sample_vrp, Simulator
#     from optimizer.base import OptimizationResult


@dataclass
class AlgorithmStats:
    """Summary statistics for an algorithm across multiple runs."""
    algorithm_name: str
    num_trials: int
    fitness_mean: float
    fitness_std: float
    fitness_min: float
    fitness_max: float
    distance_mean: float
    travel_time_mean: float
    runtime_mean: float
    convergence_histories: List[List[float]]
    raw_fitness_scores: List[float]
    raw_runtimes: List[float]
    raw_distances: List[float]
    raw_travel_times: List[float]
    best_overall_routes: List[List[int]] = field(default_factory=list)


class BenchmarkRunner:
    """Orchestrates comparative statistical benchmarking of VRP optimizers."""

    def __init__(
        self,
        num_nodes: int = 20,
        num_customers: int = 10,
        num_vehicles: int = 3,
        vehicle_capacity: float = 80.0,
        instance_seed: int = 42,
    ):
        self.num_nodes = num_nodes
        self.num_customers = num_customers
        self.num_vehicles = num_vehicles
        self.vehicle_capacity = vehicle_capacity
        self.instance_seed = instance_seed

        # Build consistent problem environment
        self.graph = build_sample_graph(num_nodes=num_nodes, seed=instance_seed)
        self.vrp = build_sample_vrp(
            self.graph,
            num_customers=num_customers,
            num_vehicles=num_vehicles,
            vehicle_capacity=vehicle_capacity,
            seed=instance_seed,
        )

    def run_benchmark(
        self,
        algorithms: List[str] = None,
        num_trials: int = 10,
        max_iterations: int = 200,
        num_particles: int = 50,
        start_seed: int = 100,
    ) -> Dict[str, AlgorithmStats]:
        """Run statistical comparison across multiple random seeds.

        Parameters
        ----------
        algorithms : List[str]
            List of algorithm identifiers (e.g. ['qpso', 'pso', 'ga', 'random_search']).
        num_trials : int
            Number of independent runs per algorithm with different seeds.
        max_iterations : int
            Iteration count per run.
        num_particles : int
            Population/Swarm size.
        start_seed : int
            Base random seed incremented for each trial.

        Returns
        -------
        Dict[str, AlgorithmStats]
            Mapping from algorithm name to aggregated trial statistics.
        """
        if algorithms is None:
            algorithms = ["qpso", "pso", "ga", "random_search"]

        results: Dict[str, AlgorithmStats] = {}

        for algo in algorithms:
            conv_histories: List[List[float]] = []
            fitnesses: List[float] = []
            runtimes: List[float] = []
            distances: List[float] = []
            travel_times: List[float] = []

            best_fitness_overall = float("inf")
            best_routes_overall: List[List[int]] = []
            algo_display_name = ""

            for trial in range(num_trials):
                seed = start_seed + trial
                sim = Simulator(self.graph, self.vrp, seed=seed)
                sim.set_traffic("normal")

                res: OptimizationResult = sim.run_optimizer(
                    algorithm=algo,
                    max_iterations=max_iterations,
                    num_particles=num_particles,
                    seed=seed,
                )

                if trial == 0:
                    # Capture proper display name from optimizer instance
                    algo_display_name = res.metrics.get("algo_name", algo.upper())

                conv_histories.append(res.convergence_history)
                fitnesses.append(res.best_fitness)
                runtimes.append(res.runtime_seconds)
                distances.append(res.metrics["total_distance"])
                travel_times.append(res.metrics["total_travel_time"])

                if res.best_fitness < best_fitness_overall:
                    best_fitness_overall = res.best_fitness
                    best_routes_overall = res.best_routes

            # Fallback name if missing
            if not algo_display_name or algo_display_name == algo.upper():
                name_map = {
                    "qpso": "QPSOOptimizer",
                    "pso": "PSOOptimizer",
                    "ga": "GAOptimizer",
                    "random_search": "RandomSearchOptimizer",
                }
                algo_display_name = name_map.get(algo, algo)

            results[algo_display_name] = AlgorithmStats(
                algorithm_name=algo_display_name,
                num_trials=num_trials,
                fitness_mean=float(np.mean(fitnesses)),
                fitness_std=float(np.std(fitnesses)),
                fitness_min=float(np.min(fitnesses)),
                fitness_max=float(np.max(fitnesses)),
                distance_mean=float(np.mean(distances)),
                travel_time_mean=float(np.mean(travel_times)),
                runtime_mean=float(np.mean(runtimes)),
                convergence_histories=conv_histories,
                raw_fitness_scores=fitnesses,
                raw_runtimes=runtimes,
                raw_distances=distances,
                raw_travel_times=travel_times,
                best_overall_routes=best_routes_overall,
            )

        return results

    def run_dynamic_traffic_benchmark(
        self,
        congested_edge: tuple[int, int] = (0, 1),
        congestion_factor: float = 2.5,
        max_iterations: int = 200,
        num_particles: int = 50,
        seed: int = 42,
    ) -> Dict[str, Dict[str, OptimizationResult]]:
        """Compare algorithms before vs after a dynamic traffic congestion spike.

        Returns
        -------
        Dict[str, Dict[str, OptimizationResult]]
            Mapping algorithm -> {'normal': OptimizationResult, 'congested': OptimizationResult}
        """
        algorithms = ["qpso", "pso", "ga", "random_search"]
        out = {}

        # 1. Run under normal traffic
        sim_normal = Simulator(self.graph, self.vrp, seed=seed)
        sim_normal.set_traffic("normal")

        # 2. Run under congested traffic
        sim_congested = Simulator(self.graph, self.vrp, seed=seed)
        sim_congested.set_traffic("normal")
        sim_congested.congest_edge(congested_edge[0], congested_edge[1], congestion=congestion_factor)

        for algo in algorithms:
            res_norm = sim_normal.run_optimizer(algo, max_iterations=max_iterations, num_particles=num_particles, seed=seed)
            res_cong = sim_congested.run_optimizer(algo, max_iterations=max_iterations, num_particles=num_particles, seed=seed)
            out[res_norm.metrics.get("algo_name", algo.upper())] = {
                "normal": res_norm,
                "congested": res_cong,
            }

        return out

    def export_results_json(self, results: Dict[str, AlgorithmStats], filepath: str | Path):
        """Save benchmark statistics to a JSON file."""
        data = {}
        for name, stats in results.items():
            d = asdict(stats)
            data[name] = d

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
