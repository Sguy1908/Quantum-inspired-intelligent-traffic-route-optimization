"""
Traffic Route Optimization Simulator

Orchestrates the full pipeline:
    1. Build or load a transportation graph.
    2. Apply traffic conditions.
    3. Define a VRP instance.
    4. Run one or more optimizers.
    5. Collect results & convergence data.
    6. Support dynamic re-optimization after traffic changes.
"""

from __future__ import annotations

import os
import sys
import numpy as np
from typing import Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.graph.graph import TransportationGraph
from backend.graph.dynamic_traffic import DynamicTrafficModel, StaticTrafficModel, static_traffic_from_graph
from backend.optimizer.objective import ObjectiveEvaluator
from backend.optimizer.alns import ALNSOptimizer
from backend.optimizer.vrp_instance import VRPInstance, Customer
from backend.optimizer.base import BaseOptimizer, OptimizationResult
from backend.optimizer.qpso import QPSOOptimizer
from backend.optimizer.pso import PSOOptimizer
from backend.optimizer.ga import GAOptimizer
from backend.optimizer.random_search import RandomSearchOptimizer


def build_sample_graph(num_nodes: int = 20,
                       seed: int = 42) -> TransportationGraph:
    """Generate a random synthetic transportation graph.

    Creates *num_nodes* nodes placed randomly in a 100×100 km grid,
    then connects each node to its ~3–5 nearest neighbours with
    distance-derived travel times.

    Parameters
    ----------
    num_nodes : int
        Number of nodes (intersections / locations).
    seed : int
        Random seed.

    Returns
    -------
    TransportationGraph
    """
    rng = np.random.default_rng(seed)
    tg = TransportationGraph()

    # Place nodes on a 2-D grid
    xs = rng.uniform(0, 100, num_nodes)
    ys = rng.uniform(0, 100, num_nodes)
    for i in range(num_nodes):
        node_type = "depot" if i == 0 else "customer"
        tg.add_node(i, x=float(xs[i]), y=float(ys[i]), node_type=node_type)

    # Connect each node to its k-nearest neighbours
    k = min(5, num_nodes - 1)
    for i in range(num_nodes):
        dists = np.sqrt((xs - xs[i]) ** 2 + (ys - ys[i]) ** 2)
        neighbours = np.argsort(dists)[1: k + 1]
        for j in neighbours:
            dist = float(dists[j])
            # Approximate free-flow travel time: ~60 km/h
            base_tt = dist / 60.0 * 60.0  # minutes
            tg.add_edge(i, int(j), distance=dist,
                        base_travel_time=base_tt, bidirectional=True)

    return tg


def build_sample_vrp(
    graph: TransportationGraph,
    num_customers: int = 10,
    num_vehicles: int = 3,
    vehicle_capacity: float = 100.0,
    seed: int = 42,
) -> VRPInstance:
    """Create a sample VRP instance from an existing graph.

    Picks *num_customers* random non-depot nodes, assigns random demands
    and loose time windows.

    Parameters
    ----------
    graph : TransportationGraph
    num_customers : int
    num_vehicles : int
    vehicle_capacity : float
    seed : int

    Returns
    -------
    VRPInstance
    """
    rng = np.random.default_rng(seed)
    all_nodes = sorted(graph.graph.nodes())
    depot = all_nodes[0]

    # Pick customer nodes (exclude depot)
    candidate_nodes = [n for n in all_nodes if n != depot]
    chosen = rng.choice(
        candidate_nodes,
        size=min(num_customers, len(candidate_nodes)),
        replace=False,
    )

    customers = []
    for nid in chosen:
        demand = float(rng.uniform(5, 30))
        tw_start = float(rng.uniform(0, 30))
        tw_end = tw_start + float(rng.uniform(60, 180))
        customers.append(
            Customer(
                node_id=int(nid),
                demand=demand,
                time_window=(tw_start, tw_end),
                service_time=float(rng.uniform(5, 15)),
            )
        )

    return VRPInstance(
        graph=graph,
        depot=depot,
        customers=customers,
        num_vehicles=num_vehicles,
        vehicle_capacity=vehicle_capacity,
    )


class Simulator:
    """High-level simulator orchestrating graph, traffic, and optimizers."""

    def __init__(
        self,
        graph: TransportationGraph,
        vrp_instance: VRPInstance,
        seed: int = 42,
    ):
        self.graph = graph
        self.vrp = vrp_instance
        self.traffic = static_traffic_from_graph(graph)
        self.seed = seed
        self.results: dict[str, OptimizationResult] = {}

    # ------------------------------------------------------------------
    # Traffic controls
    # ------------------------------------------------------------------

    def set_traffic(self, profile: str = "normal"):
        """Apply a named traffic profile to the entire network."""
        ranges = {"normal": (0.0, .1), "moderate": (.3, .6), "heavy": (.8, 1.5)}
        lo, hi = ranges[profile]; rng = np.random.default_rng(self.seed)
        self.traffic = StaticTrafficModel({(u, v): float(rng.uniform(lo, hi)) for u, v in self.graph.graph.edges()})

    def congest_edge(self, u: int, v: int, congestion: float = 1.5):
        """Manually spike congestion on a specific road segment."""
        values = dict(self.traffic.congestion_by_edge)
        values[(u, v)] = values[(v, u)] = congestion
        self.traffic = StaticTrafficModel(values)

    def step_traffic(self, drift: float = 0.05):
        """Advance traffic by one time step with random drift."""
        # Legacy interactive control: install a reproducible dynamic environment.
        self.traffic = DynamicTrafficModel.from_graph(self.graph, seed=self.seed, amplitude_range=(drift, drift), base_range=(0.0, .3))

    # ------------------------------------------------------------------
    # Optimization
    # ------------------------------------------------------------------

    def run_optimizer(
        self,
        algorithm: str = "qpso",
        max_iterations: int = 200,
        num_particles: int = 50,
        seed: Optional[int] = None,
    ) -> OptimizationResult:
        """Run a named optimizer on the current VRP instance.

        Parameters
        ----------
        algorithm : str
            One of 'qpso', 'pso', 'ga'.
        max_iterations : int
            Maximum iterations for the metaheuristic.
        num_particles : int
            Swarm / population size.
        seed : int, optional
            Random seed override.

        Returns
        -------
        OptimizationResult
        """
        s = seed if seed is not None else self.seed
        algo = algorithm.lower()

        if algo == "qpso":
            opt = QPSOOptimizer(self.vrp, num_particles=num_particles, seed=s, evaluator=ObjectiveEvaluator(self.vrp, self.traffic))
        elif algo == "alns":
            opt = ALNSOptimizer(self.vrp, seed=s, evaluator=ObjectiveEvaluator(self.vrp, self.traffic))
        elif algo == "pso":
            opt = PSOOptimizer(self.vrp, num_particles=num_particles, seed=s)
        elif algo == "ga":
            opt = GAOptimizer(self.vrp, pop_size=num_particles, seed=s)
        elif algo in ("random_search", "random"):
            opt = RandomSearchOptimizer(self.vrp, num_samples_per_iter=num_particles, seed=s)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        result = opt.optimize(
            max_iterations=max_iterations,
            time_step=0,
        )
        self.results[opt.name] = result
        return result

    def run_all(
        self,
        max_iterations: int = 200,
        num_particles: int = 50,
        seed: Optional[int] = None,
        algorithms: tuple[str, ...] = ("qpso", "pso", "ga", "random_search"),
    ) -> dict[str, OptimizationResult]:
        """Run QPSO, PSO, GA, and Random Search and return comparative results."""
        out: dict[str, OptimizationResult] = {}
        for algo in algorithms:
            res = self.run_optimizer(
                algo, max_iterations, num_particles, seed
            )
            out[algo] = res
        return out

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """Return a human-readable summary of the last optimization runs."""
        lines = ["=" * 60, "  SIMULATION RESULTS", "=" * 60]
        for name, res in self.results.items():
            m = res.metrics
            lines.append(f"\n--- {name} ---")
            lines.append(f"  Best Fitness     : {res.best_fitness:.4f}")
            lines.append(f"  Routing Cost     : {m['routing_cost']:.4f}")
            lines.append(f"  Total Distance   : {m['total_distance']:.2f} km")
            lines.append(f"  Total Travel Time: {m['total_travel_time']:.2f} min")
            lines.append(f"  Congestion Cost  : {m['congestion_cost']:.4f}")
            lines.append(f"  Vehicles Used    : {m['num_vehicles_used']}")
            lines.append(f"  Runtime          : {res.runtime_seconds:.3f} s")
            lines.append(f"  Routes:")
            for i, route in enumerate(res.best_routes):
                lines.append(f"    Vehicle {i+1}: {' → '.join(map(str, route))}")
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
