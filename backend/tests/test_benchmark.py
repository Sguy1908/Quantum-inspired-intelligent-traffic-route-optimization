"""
Unit tests for the benchmarking suite and matplotlib visualization modules.

Usage:
    pytest backend/tests/test_benchmark.py
"""

import os
import sys
from pathlib import Path
import pytest

# Ensure parent directory is in sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.benchmarks.benchmark_runner import BenchmarkRunner
from backend.benchmarks.visualization import (
    plot_convergence,
    plot_metrics_comparison,
    plot_route_map_comparison,
    plot_traffic_impact,
)
from backend.optimizer.random_search import RandomSearchOptimizer


def test_random_search_optimizer():
    """Verify RandomSearchOptimizer initializes and runs correctly."""
    runner = BenchmarkRunner(num_nodes=10, num_customers=5, seed=42)
    opt = RandomSearchOptimizer(runner.vrp, num_samples_per_iter=10, seed=42)
    res = opt.optimize(max_iterations=10)

    assert res.best_fitness > 0
    assert len(res.best_routes) > 0
    assert len(res.convergence_history) == 11  # 0 to 10 inclusive


def test_benchmark_runner_and_visualizations(tmp_path):
    """Integration test verifying full benchmark execution and plot generation."""
    runner = BenchmarkRunner(num_nodes=10, num_customers=5, seed=42)

    # 1. Run quick benchmark (2 trials, 10 iterations)
    results = runner.run_benchmark(
        algorithms=["qpso", "pso", "ga", "random_search"],
        num_trials=2,
        max_iterations=10,
        num_particles=10,
        start_seed=100,
    )

    assert len(results) == 4
    for name, stats in results.items():
        assert stats.fitness_mean > 0
        assert len(stats.convergence_histories) == 2
        assert len(stats.convergence_histories[0]) == 11

    # 2. Test json export
    json_file = tmp_path / "test_results.json"
    runner.export_results_json(results, json_file)
    assert json_file.exists()

    # 3. Test plot generation
    plot_convergence(results, output_dir=tmp_path, filename="conv.png")
    assert (tmp_path / "conv.png").exists()

    plot_metrics_comparison(results, output_dir=tmp_path, filename="metrics.png")
    assert (tmp_path / "metrics.png").exists()

    plot_route_map_comparison(runner.graph, runner.vrp, results, output_dir=tmp_path, filename="routes.png")
    assert (tmp_path / "routes.png").exists()

    # 4. Test dynamic traffic benchmark & plot
    dynamic_results = runner.run_dynamic_traffic_benchmark(
        congested_edge=(0, 1),
        congestion_factor=2.0,
        max_iterations=10,
        num_particles=10,
        seed=42,
    )
    plot_traffic_impact(dynamic_results, output_dir=tmp_path, filename="traffic.png")
    assert (tmp_path / "traffic.png").exists()

    # Copy to brain artifact directory
    import shutil
    brain_dir = Path("/home/sguy/.gemini/antigravity/brain/0060a94c-9a43-405a-9b8b-70e9e35f8863")
    bench_plots = root_dir / "backend" / "benchmarks" / "plots"
    if brain_dir.exists() and bench_plots.exists():
        for p in bench_plots.glob("*.png"):
            shutil.copy(p, brain_dir / p.name)


def test_pso_vs_qpso_experiment_modules():
    """Verify backend.benchmarks.run_pso_vs_qpso_experiment imports and exposes key functions."""
    from backend.benchmarks import run_pso_vs_qpso_experiment
    assert hasattr(run_pso_vs_qpso_experiment, "run_experiments")
    assert hasattr(run_pso_vs_qpso_experiment, "generate_all_plots")
