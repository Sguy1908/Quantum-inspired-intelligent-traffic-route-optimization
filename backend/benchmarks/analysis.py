"""Loading, canonical ordering, and raw-run aggregation for experiments."""
from __future__ import annotations
import csv
import json
from collections import defaultdict
from pathlib import Path
import numpy as np

from backend.benchmarks.benchmark_runner import sort_records


def load_raw_results(experiment_dir: str | Path) -> list[dict]:
    records = json.loads((Path(experiment_dir) / "raw_results.json").read_text())
    return sort_records(records)


def aggregate_records(records: list[dict]) -> list[dict]:
    buckets = defaultdict(list)
    for r in sort_records(records): buckets[(r["algorithm"], r["traffic_mode"], int(r["network_size"]))].append(r)
    output = []
    metrics = ("objective", "runtime_seconds", "objective_evaluations", "constraint_violation", "total_distance", "total_travel_time")
    for (algorithm, traffic_mode, network_size), runs in sorted(buckets.items()):
        row = {"algorithm": algorithm, "traffic_mode": traffic_mode, "network_size": network_size, "runs": len(runs),
               "feasibility_rate": float(np.mean([r["feasible"] for r in runs]))}
        for metric in metrics:
            values = np.array([r[metric] for r in runs], dtype=float)
            row.update({f"{metric}_mean": float(values.mean()), f"{metric}_median": float(np.median(values)),
                        f"{metric}_std": float(values.std()), f"{metric}_best": float(values.min()), f"{metric}_worst": float(values.max())})
        output.append(row)
    return output


def write_aggregate(experiment_dir: str | Path, rows: list[dict]) -> Path:
    target = Path(experiment_dir) / "aggregated"; target.mkdir(parents=True, exist_ok=True)
    (target / "summary.json").write_text(json.dumps(rows, indent=2))
    with (target / "summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else []); writer.writeheader()
        writer.writerows(rows)
    return target


def aggregate_experiment(experiment_dir: str | Path) -> list[dict]:
    rows = aggregate_records(load_raw_results(experiment_dir)); write_aggregate(experiment_dir, rows); return rows
