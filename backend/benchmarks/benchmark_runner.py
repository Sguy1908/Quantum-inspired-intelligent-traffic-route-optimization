"""Reproducible, paired QPSO--ALNS benchmark runner."""
from __future__ import annotations

import csv, json, os, platform, sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.graph.dynamic_traffic import DynamicTrafficModel, StaticTrafficModel
from backend.optimizer.alns import ALNSOptimizer
from backend.optimizer.objective import ObjectiveConfig, ObjectiveEvaluator
from backend.optimizer.qpso import QPSOOptimizer
from backend.simulator.engine import build_sample_graph, build_sample_vrp


@dataclass
class BenchmarkConfig:
    network_sizes: list[int] = field(default_factory=lambda: [20, 50, 100, 200, 300, 400, 500])
    instances_per_size: int = 1
    optimizer_seeds: list[int] = field(default_factory=lambda: [101, 202, 303, 404, 505])
    base_instance_seed: int = 10_000
    max_evaluations: int = 5_000
    max_iterations: int = 1_000
    qpso_particles: int = 50
    traffic_period: float = 240.0
    traffic_c_max: float = 1.5
    output_dir: str = "results"
    objective: dict[str, float] = field(default_factory=dict)


class BenchmarkRunner:
    def __init__(self, config: BenchmarkConfig): self.config = config

    def _instance_seed(self, size: int, instance_id: int) -> int:
        return self.config.base_instance_seed + size * 1_000 + instance_id

    def _build_instance(self, size: int, instance_id: int):
        seed = self._instance_seed(size, instance_id)
        graph = build_sample_graph(num_nodes=size, seed=seed)
        # About ten customers/vehicle and capacity above mean total demand.
        vehicles = max(3, int(np.ceil((size - 1) / 10)))
        instance = build_sample_vrp(graph, num_customers=size - 1, num_vehicles=vehicles,
                                    vehicle_capacity=200.0, seed=seed + 1)
        # Generated windows must admit at least one feasible solution; tight-window
        # studies should be a separately recorded factor, not accidental infeasibility.
        for customer in instance.customers:
            customer.time_window = (0.0, 10_000.0)
        dynamic = DynamicTrafficModel.from_graph(graph, seed=seed + 2, period=self.config.traffic_period,
                                                  c_max=self.config.traffic_c_max)
        static = StaticTrafficModel({edge: dynamic.congestion(*edge, 0.0) for edge in dynamic.base_by_edge}, alpha=dynamic.alpha)
        return seed, graph, instance, static, dynamic

    @staticmethod
    def _instance_record(seed, graph, instance, static, dynamic) -> dict:
        return {"seed": seed, "depot": instance.depot, "num_vehicles": instance.num_vehicles,
                "vehicle_capacity": instance.vehicle_capacity,
                "nodes": [{"id": n, **d} for n, d in graph.graph.nodes(data=True)],
                "edges": [{"u": u, "v": v, **d} for u, v, d in graph.graph.edges(data=True)],
                "customers": [{"node_id": c.node_id, "demand": c.demand, "time_window": c.time_window,
                               "service_time": c.service_time} for c in instance.customers],
                "static_traffic": static.metadata(), "dynamic_traffic": dynamic.metadata()}

    def _run_one(self, algorithm, instance, traffic, seed):
        evaluator = ObjectiveEvaluator(instance, traffic, ObjectiveConfig(**self.config.objective))
        if algorithm == "qpso":
            optimizer = QPSOOptimizer(instance, num_particles=self.config.qpso_particles, seed=seed, evaluator=evaluator)
        elif algorithm == "alns":
            optimizer = ALNSOptimizer(instance, seed=seed, evaluator=evaluator)
        else: raise ValueError(f"Unsupported benchmark algorithm: {algorithm}")
        return optimizer.optimize(max_iterations=self.config.max_iterations, max_evaluations=self.config.max_evaluations)

    def run(self) -> list[dict[str, Any]]:
        out = Path(self.config.output_dir); (out / "instances").mkdir(parents=True, exist_ok=True)
        records = []
        for size in self.config.network_sizes:
            for iid in range(self.config.instances_per_size):
                instance_seed, graph, instance, static, dynamic = self._build_instance(size, iid)
                (out / "instances" / f"n{size}_instance{iid}.json").write_text(json.dumps(self._instance_record(instance_seed, graph, instance, static, dynamic), indent=2))
                for run_seed in self.config.optimizer_seeds:
                    for mode, traffic in (("static", static), ("dynamic", dynamic)):
                        for algorithm in ("qpso", "alns"):
                            result = self._run_one(algorithm, instance, traffic, run_seed)
                            metrics = result.metrics
                            records.append({"algorithm": algorithm, "traffic_mode": mode, "network_size": size,
                                            "instance_id": iid, "instance_seed": instance_seed, "random_seed": run_seed,
                                            "objective": result.best_fitness, "routing_cost": metrics["routing_cost"],
                                            "total_distance": metrics["total_distance"], "total_travel_time": metrics["total_travel_time"],
                                            "congestion_exposure": metrics["congestion_exposure"],
                                            "constraint_violation": metrics["constraint_violation"], "feasible": metrics["feasible"],
                                            "num_routes": metrics["num_vehicles_used"], "runtime_seconds": result.runtime_seconds,
                                            "objective_evaluations": result.objective_evaluations,
                                            "parameters": {"budget": {"max_evaluations": self.config.max_evaluations, "max_iterations": self.config.max_iterations},
                                                           "qpso_particles": self.config.qpso_particles, "objective": asdict(ObjectiveConfig(**self.config.objective)),
                                                           "traffic": traffic.metadata()}, "convergence": result.convergence_history})
        self.write(records)
        return records

    def write(self, records: list[dict[str, Any]]) -> None:
        out = Path(self.config.output_dir); out.mkdir(parents=True, exist_ok=True)
        (out / "raw_results.json").write_text(json.dumps(records, indent=2))
        fields = [k for k in records[0] if k not in {"parameters", "convergence"}] if records else []
        with (out / "raw_results.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
            writer.writerows([{k: r[k] for k in fields} for r in records])
        metadata = {"config": asdict(self.config), "python": sys.version, "platform": platform.platform()}
        (out / "experiment_metadata.json").write_text(json.dumps(metadata, indent=2))
