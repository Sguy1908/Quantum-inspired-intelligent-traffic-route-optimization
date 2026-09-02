"""Benchmarks sub-package — BenchmarkRunner and Matplotlib visualization tools."""

try:
    from backend.benchmarks.benchmark_runner import BenchmarkRunner, AlgorithmStats
    from backend.benchmarks.visualization import (
        plot_convergence,
        plot_metrics_comparison,
        plot_route_map_comparison,
        plot_traffic_impact,
    )
except ImportError:
    from benchmarks.benchmark_runner import BenchmarkRunner, AlgorithmStats
    from benchmarks.visualization import (
        plot_convergence,
        plot_metrics_comparison,
        plot_route_map_comparison,
        plot_traffic_impact,
    )

__all__ = [
    "BenchmarkRunner",
    "AlgorithmStats",
    "plot_convergence",
    "plot_metrics_comparison",
    "plot_route_map_comparison",
    "plot_traffic_impact",
]
