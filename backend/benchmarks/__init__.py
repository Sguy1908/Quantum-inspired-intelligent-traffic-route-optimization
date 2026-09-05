"""Benchmarks sub-package — BenchmarkRunner and Matplotlib visualization tools."""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from backend.benchmarks.benchmark_runner import BenchmarkRunner, BenchmarkConfig
    from backend.benchmarks.visualization import (
        plot_convergence,
        plot_metrics_comparison,
        plot_route_map_comparison,
        plot_traffic_impact,
    )
except ImportError:
    from benchmarks.benchmark_runner import BenchmarkRunner, BenchmarkConfig
    from benchmarks.visualization import (
        plot_convergence,
        plot_metrics_comparison,
        plot_route_map_comparison,
        plot_traffic_impact,
    )

__all__ = [
    "BenchmarkRunner",
    "BenchmarkConfig",
    "plot_convergence",
    "plot_metrics_comparison",
    "plot_route_map_comparison",
    "plot_traffic_impact",
]
