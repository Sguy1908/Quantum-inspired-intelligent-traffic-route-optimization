import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.benchmarks.benchmark_runner import BenchmarkConfig, BenchmarkRunner
from backend.benchmarks.visualization import plot_research_results


def test_paired_benchmark_persists_reproducible_raw_runs(tmp_path):
    config = BenchmarkConfig(network_sizes=[20], instances_per_size=1, optimizer_seeds=[7],
                             qpso_particles=8, max_iterations=20, max_evaluations=60,
                             output_dir=str(tmp_path))
    records = BenchmarkRunner(config).run()
    assert len(records) == 4
    assert {(r["algorithm"], r["traffic_mode"]) for r in records} == {
        ("qpso", "static"), ("alns", "static"), ("qpso", "dynamic"), ("alns", "dynamic")}
    assert {r["instance_seed"] for r in records} == {records[0]["instance_seed"]}
    assert all(r["objective_evaluations"] <= 60 and r["convergence"] for r in records)
    assert (tmp_path / "instances" / "n20_instance0.json").exists()
    assert (tmp_path / "raw_results.csv").exists()
    plot_research_results(tmp_path)
    assert (tmp_path / "plots" / "convergence.png").exists()
