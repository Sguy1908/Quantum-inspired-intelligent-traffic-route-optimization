#!/usr/bin/env python3
"""
Run Optimization Algorithm Benchmarks & Matplotlib Visualizations

Usage:
    python -m backend.benchmarks.run_benchmarks
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

try:
    from backend.benchmarks.benchmark_runner import BenchmarkRunner
    from backend.benchmarks.visualization import (
        plot_convergence,
        plot_metrics_comparison,
        plot_route_map_comparison,
        plot_traffic_impact,
    )
except ImportError:
    from benchmarks.benchmark_runner import BenchmarkRunner
    from benchmarks.visualization import (
        plot_convergence,
        plot_metrics_comparison,
        plot_route_map_comparison,
        plot_traffic_impact,
    )


def print_markdown_summary(results: dict):
    """Print formatted markdown comparison table."""
    print("\n" + "=" * 80)
    print("                      ALGORITHM BENCHMARK RESULTS SUMMARY                      ")
    print("=" * 80)
    print(f"| {'Algorithm':<22} | {'Fitness (Mean ± Std)':<22} | {'Min Fitness':<12} | {'Distance (km)':<14} | {'Runtime (s)':<12} |")
    print("|" + "-" * 24 + "|" + "-" * 24 + "|" + "-" * 14 + "|" + "-" * 16 + "|" + "-" * 14 + "|")

    for algo_name, stats in results.items():
        fit_str = f"{stats.fitness_mean:.2f} ± {stats.fitness_std:.2f}"
        min_fit = f"{stats.fitness_min:.2f}"
        dist_str = f"{stats.distance_mean:.2f}"
        rt_str = f"{stats.runtime_mean:.3f}"
        print(f"| {algo_name:<22} | {fit_str:<22} | {min_fit:<12} | {dist_str:<14} | {rt_str:<12} |")

    print("=" * 80 + "\n")


def main():
    plots_dir = Path(__file__).resolve().parent / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    print("Initializing benchmark suite (20 nodes, 10 customers, 3 vehicles)...")
    runner = BenchmarkRunner(
        num_nodes=20,
        num_customers=10,
        num_vehicles=3,
        vehicle_capacity=80.0,
        instance_seed=42,
    )

    print("\n--- Step 1: Running Statistical Benchmarks (5 trials per algorithm, 200 iterations each) ---")
    results = runner.run_benchmark(
        algorithms=["qpso", "pso", "ga", "random_search"],
        num_trials=5,
        max_iterations=200,
        num_particles=50,
        start_seed=100,
    )

    print_markdown_summary(results)

    # Export json results
    json_path = plots_dir / "benchmark_results.json"
    runner.export_results_json(results, json_path)
    print(f"Exported JSON benchmark statistics to: {json_path}")

    print("\n--- Step 2: Generating Matplotlib Visualizations ---")
    plot_convergence(results, output_dir=plots_dir, filename="convergence_comparison.png")
    plot_metrics_comparison(results, output_dir=plots_dir, filename="metrics_comparison.png")
    plot_route_map_comparison(runner.graph, runner.vrp, results, output_dir=plots_dir, filename="route_visualizations.png")

    print("\n--- Step 3: Running Dynamic Traffic Impact Experiment ---")
    dynamic_results = runner.run_dynamic_traffic_benchmark(
        congested_edge=(0, 1),
        congestion_factor=2.5,
        max_iterations=200,
        num_particles=50,
        seed=42,
    )
    plot_traffic_impact(dynamic_results, output_dir=plots_dir, filename="traffic_dynamic_comparison.png")

    import shutil
    artifact_dir = Path("/home/sguy/.gemini/antigravity/brain/0060a94c-9a43-405a-9b8b-70e9e35f8863")
    if artifact_dir.exists():
        for p in plots_dir.glob("*.png"):
            shutil.copy(p, artifact_dir / p.name)

    print("\n✓ All benchmark tasks and matplotlib visualizations completed successfully!")
    print(f"Generated plots saved in: {plots_dir}")


if __name__ == "__main__":
    main()
