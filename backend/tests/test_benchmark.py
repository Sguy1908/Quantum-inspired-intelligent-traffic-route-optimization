import json
import os
import sys
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from backend.benchmarks.analysis import aggregate_records, load_raw_results
from backend.benchmarks.benchmark_runner import ALGORITHMS, BenchmarkConfig, BenchmarkRunner, sort_records
from backend.benchmarks.visualization import generate_experiment_plots


def _config(tmp_path, seed_mode="fixed"):
    return BenchmarkConfig(network_sizes=[20], instances_per_size=1, runs_per_instance=1, seed_mode=seed_mode,
        base_seed=19, max_evaluations=40, max_iterations=20, qpso_particles=8, pso_particles=8,
        ga_population=8, random_samples=8, output_dir=str(tmp_path), experiment_id="test")


def test_all_five_algorithms_are_paired_budgeted_and_plotted(tmp_path):
    records = BenchmarkRunner(_config(tmp_path)).run()
    assert len(records) == 10
    assert {(r["algorithm"], r["traffic_mode"]) for r in records} == {(a, t) for a in ALGORITHMS for t in ("static", "dynamic")}
    assert len({r["instance_seed"] for r in records}) == 1
    assert all(r["objective_evaluations"] == 40 and r["convergence"] for r in records)
    assert records == sort_records(records)
    root = tmp_path / "test"
    assert (root / "raw" / "qpso" / "dynamic" / "N020").exists()
    assert (root / "raw_results.csv").exists() and (root / "instances" / "N020_instance000.json").exists()
    images = generate_experiment_plots(root)
    assert len(images) == 13 and all(path.exists() for path in images)
    assert len(aggregate_records(load_raw_results(root))) == 10
    with pytest.raises(FileExistsError):
        BenchmarkRunner(_config(tmp_path)).run()


def test_seed_modes_and_numeric_ordering(tmp_path):
    fixed = BenchmarkRunner(_config(tmp_path / "one"))._seed_plan()
    assert fixed == BenchmarkRunner(_config(tmp_path / "two"))._seed_plan()
    random_plan = BenchmarkRunner(_config(tmp_path / "random", "random"))._seed_plan()
    assert random_plan["mode"] == "random" and len(random_plan["optimizer_seeds"]) == 1
    random_cfg = _config(tmp_path / "random-run", "random")
    random_records = BenchmarkRunner(random_cfg).run(algorithms=["random"], traffic_modes=["static"])
    saved_plan = json.loads((tmp_path / "random-run" / "test" / "experiment_metadata.json").read_text())["seed_plan"]
    assert random_records[0]["random_seed"] in saved_plan["optimizer_seeds"]
    assert random_records[0]["instance_seed"] in saved_plan["instance_seeds"]
    unordered = [{"algorithm": "qpso", "traffic_mode": "static", "network_size": n, "instance_id": 0, "random_seed": 1}
                 for n in [100, 20, 500, 50, 400, 200, 300]]
    assert [r["network_size"] for r in sort_records(unordered)] == [20, 50, 100, 200, 300, 400, 500]
