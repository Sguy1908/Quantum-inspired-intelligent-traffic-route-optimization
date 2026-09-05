"""Paired, reproducible experiment execution shared by all entry points."""
from __future__ import annotations

import csv
import json
import os
import platform
import secrets
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from backend.graph.dynamic_traffic import DynamicTrafficModel, StaticTrafficModel
from backend.optimizer.alns import ALNSOptimizer
from backend.optimizer.ga import GAOptimizer
from backend.optimizer.objective import ObjectiveConfig, ObjectiveEvaluator
from backend.optimizer.pso import PSOOptimizer
from backend.optimizer.qpso import QPSOOptimizer
from backend.optimizer.random_search import RandomSearchOptimizer
from backend.simulator.engine import build_sample_graph, build_sample_vrp

ALGORITHMS = ("alns", "ga", "pso", "qpso", "random")
TRAFFIC_MODES = ("dynamic", "static")


@dataclass
class BenchmarkConfig:
    network_sizes: list[int] = field(default_factory=lambda: [20, 50, 100, 200, 300, 400, 500])
    instances_per_size: int = 1
    runs_per_instance: int = 5
    seed_mode: str = "fixed"  # fixed | random
    base_seed: int = 10_000
    max_evaluations: int = 5_000
    max_iterations: int = 1_000
    qpso_particles: int = 50
    pso_particles: int = 50
    ga_population: int = 50
    random_samples: int = 50
    traffic_period: float = 240.0
    traffic_c_max: float = 1.5
    output_dir: str = "backend/results/research"
    experiment_id: str = "research"
    objective: dict[str, float] = field(default_factory=dict)
    algorithm_parameters: dict[str, dict[str, Any]] = field(default_factory=dict)

    def validate(self) -> None:
        if self.seed_mode not in {"fixed", "random"}: raise ValueError("seed_mode must be 'fixed' or 'random'")
        if not self.network_sizes or any(n < 3 for n in self.network_sizes): raise ValueError("network_sizes must contain node counts >= 3")
        if self.instances_per_size < 1 or self.runs_per_instance < 1 or self.max_evaluations < 1: raise ValueError("instances, runs, and evaluations must be positive")


def sort_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Canonical numeric ordering; never rely on directory/dict order."""
    return sorted(records, key=lambda r: (r["algorithm"], r["traffic_mode"], int(r["network_size"]),
                                          int(r["instance_id"]), int(r["random_seed"])))


class BenchmarkRunner:
    def __init__(self, config: BenchmarkConfig):
        config.validate(); self.config = config

    def _seed_plan(self) -> dict[str, Any]:
        count = len(self.config.network_sizes) * self.config.instances_per_size
        if self.config.seed_mode == "fixed":
            rng = np.random.default_rng(self.config.base_seed)
            draw = lambda n: rng.integers(1, 2**31 - 1, size=n).astype(int).tolist()
        else:
            source = secrets.SystemRandom()
            draw = lambda n: [source.randrange(1, 2**31 - 1) for _ in range(n)]
        return {"mode": self.config.seed_mode, "base_seed": self.config.base_seed,
                "instance_seeds": draw(count), "optimizer_seeds": draw(self.config.runs_per_instance)}

    def _build_instance(self, size: int, seed: int):
        graph = build_sample_graph(num_nodes=size, seed=seed)
        vehicles = max(3, int(np.ceil((size - 1) / 10)))
        instance = build_sample_vrp(graph, num_customers=size - 1, num_vehicles=vehicles,
                                    vehicle_capacity=200.0, seed=seed + 1)
        for customer in instance.customers: customer.time_window = (0.0, 10_000.0)
        dynamic = DynamicTrafficModel.from_graph(graph, seed=seed + 2, period=self.config.traffic_period,
                                                  c_max=self.config.traffic_c_max)
        static = StaticTrafficModel({edge: dynamic.congestion(*edge, 0.0) for edge in sorted(dynamic.base_by_edge)}, dynamic.alpha)
        return graph, instance, static, dynamic

    @staticmethod
    def _instance_record(seed, graph, instance, static, dynamic) -> dict:
        return {"seed": seed, "depot": instance.depot, "num_vehicles": instance.num_vehicles,
                "vehicle_capacity": instance.vehicle_capacity,
                "nodes": [{"id": n, **d} for n, d in sorted(graph.graph.nodes(data=True))],
                "edges": [{"u": u, "v": v, **d} for u, v, d in sorted(graph.graph.edges(data=True))],
                "customers": [{"node_id": c.node_id, "demand": c.demand, "time_window": c.time_window,
                               "service_time": c.service_time} for c in sorted(instance.customers, key=lambda c: c.node_id)],
                "static_traffic": static.metadata(), "dynamic_traffic": dynamic.metadata()}

    def _optimizer(self, algorithm: str, instance, evaluator, seed: int):
        params = self.config.algorithm_parameters.get(algorithm, {})
        if algorithm == "qpso": return QPSOOptimizer(instance, self.config.qpso_particles, seed=seed, evaluator=evaluator, **params)
        if algorithm == "pso": return PSOOptimizer(instance, self.config.pso_particles, seed=seed, evaluator=evaluator, **params)
        if algorithm == "ga": return GAOptimizer(instance, self.config.ga_population, seed=seed, evaluator=evaluator, **params)
        if algorithm == "random": return RandomSearchOptimizer(instance, self.config.random_samples, seed=seed, evaluator=evaluator, **params)
        if algorithm == "alns": return ALNSOptimizer(instance, seed=seed, evaluator=evaluator, **params)
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    def _algorithm_parameters(self, algorithm: str) -> dict[str, Any]:
        sizes = {"qpso": {"num_particles": self.config.qpso_particles}, "pso": {"num_particles": self.config.pso_particles},
                 "ga": {"pop_size": self.config.ga_population}, "random": {"num_samples_per_iter": self.config.random_samples}, "alns": {}}
        return {**sizes[algorithm], **self.config.algorithm_parameters.get(algorithm, {})}

    def _run_one(self, algorithm, instance, traffic, seed):
        evaluator = ObjectiveEvaluator(instance, traffic, ObjectiveConfig(**self.config.objective))
        result = self._optimizer(algorithm, instance, evaluator, seed).optimize(
            max_iterations=self.config.max_iterations, max_evaluations=self.config.max_evaluations)
        return result, evaluator

    def run(self, algorithms: list[str] | tuple[str, ...] = ALGORITHMS,
            traffic_modes: list[str] | tuple[str, ...] = TRAFFIC_MODES) -> list[dict[str, Any]]:
        algorithms = tuple(sorted(set(algorithms)))
        traffic_modes = tuple(sorted(set(traffic_modes)))
        if set(algorithms) - set(ALGORITHMS) or set(traffic_modes) - set(TRAFFIC_MODES): raise ValueError("Unknown algorithm or traffic mode")
        root = Path(self.config.output_dir) / self.config.experiment_id
        if root.exists() and any(root.iterdir()):
            raise FileExistsError(f"Experiment directory already exists: {root}. Choose a new experiment_id; results are never overwritten.")
        instances_dir = root / "instances"; instances_dir.mkdir(parents=True, exist_ok=True)
        plan = self._seed_plan()
        (root / "experiment_metadata.json").write_text(json.dumps({"config": asdict(self.config), "seed_plan": plan,
            "python": sys.version, "platform": platform.platform()}, indent=2))
        records: list[dict[str, Any]] = []; seed_index = 0
        for size in sorted(self.config.network_sizes):
            for instance_id in range(self.config.instances_per_size):
                instance_seed = plan["instance_seeds"][seed_index]; seed_index += 1
                graph, instance, static, dynamic = self._build_instance(size, instance_seed)
                instance_file = instances_dir / f"N{size:03d}_instance{instance_id:03d}.json"
                instance_file.write_text(json.dumps(self._instance_record(instance_seed, graph, instance, static, dynamic), indent=2))
                environments = {"static": static, "dynamic": dynamic}
                for run_seed in sorted(plan["optimizer_seeds"]):
                    for traffic_mode in traffic_modes:
                        for algorithm in algorithms:
                            result, evaluator = self._run_one(algorithm, instance, environments[traffic_mode], run_seed)
                            m = result.metrics
                            record = {"experiment_id": self.config.experiment_id, "algorithm": algorithm,
                                "traffic_mode": traffic_mode, "network_size": size, "instance_id": instance_id,
                                "instance_seed": instance_seed, "random_seed": run_seed, "objective": result.best_fitness,
                                "routing_cost": m["routing_cost"], "total_distance": m["total_distance"],
                                "total_travel_time": m["total_travel_time"], "congestion_exposure": m["congestion_exposure"],
                                "constraint_violation": m["constraint_violation"], "feasible": m["feasible"],
                                "num_routes": m["num_vehicles_used"], "runtime_seconds": result.runtime_seconds,
                                "objective_evaluations": result.objective_evaluations, "iterations": len(result.convergence_history) - 1,
                                "parameters": {"budget": {"max_evaluations": self.config.max_evaluations, "max_iterations": self.config.max_iterations},
                                    "algorithm": self._algorithm_parameters(algorithm),
                                    "objective": asdict(evaluator.config), "traffic": environments[traffic_mode].metadata()},
                                "convergence": result.convergence_history}
                            records.append(record)
                            out = root / "raw" / algorithm / traffic_mode / f"N{size:03d}"
                            out.mkdir(parents=True, exist_ok=True)
                            (out / f"instance{instance_id:03d}_seed{run_seed:010d}.json").write_text(json.dumps(record, indent=2))
        records = sort_records(records); self.write(records, root)
        return records

    def write(self, records: list[dict[str, Any]], root: Path) -> None:
        root.mkdir(parents=True, exist_ok=True)
        (root / "raw_results.json").write_text(json.dumps(records, indent=2))
        fields = [k for k in records[0] if k not in {"parameters", "convergence"}] if records else []
        with (root / "raw_results.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
            writer.writerows([{k: r[k] for k in fields} for r in records])
