"""
Matplotlib Visualization Module for Algorithm Benchmark Comparison

Provides high-resolution, publication-ready figures comparing QPSO, PSO, GA, and Random Search:
    1. Convergence Curves (Fitness vs. Iteration with error bands).
    2. Performance Metrics Comparison (Fitness, Distance, Travel Time, Runtime).
    3. Spatial Route Maps (2D graph paths for each algorithm).
    4. Dynamic Traffic Impact (Pre- vs. Post-Congestion performance).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from backend.graph.graph import TransportationGraph
    from backend.optimizer.vrp_instance import VRPInstance
    from backend.optimizer.base import OptimizationResult
except ImportError:
    from graph.graph import TransportationGraph
    from optimizer.vrp_instance import VRPInstance
    from optimizer.base import OptimizationResult

# Modern aesthetic color palette
COLOR_MAP = {
    "QPSOOptimizer": "#6C5CE7",       # Vibrant Indigo / Purple
    "QPSO": "#6C5CE7",
    "PSOOptimizer": "#FF7675",        # Coral Red
    "PSO": "#FF7675",
    "GAOptimizer": "#00B894",         # Emerald Teal
    "GA": "#00B894",
    "RandomSearchOptimizer": "#636E72", # Slate Gray
    "RandomSearch": "#636E72",
}

STYLE_MAP = {
    "QPSOOptimizer": {"linestyle": "-", "marker": "o"},
    "PSOOptimizer": {"linestyle": "--", "marker": "s"},
    "GAOptimizer": {"linestyle": "-.", "marker": "^"},
    "RandomSearchOptimizer": {"linestyle": ":", "marker": "d"},
}


def setup_matplotlib_style():
    """Apply clean, modern matplotlib parameters."""
    plt.rcParams["font.sans-serif"] = "DejaVu Sans, Arial, Helvetica"
    plt.rcParams["axes.edgecolor"] = "#CCCCCC"
    plt.rcParams["axes.linewidth"] = 0.8
    plt.rcParams["grid.color"] = "#EAEAEA"
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["grid.alpha"] = 0.7


def plot_convergence(
    results: Dict[str, AlgorithmStats],
    output_dir: str | Path = "plots",
    filename: str = "convergence_comparison.png",
    show_std: bool = True,
):
    """Plot mean convergence curves with shaded ±1 std error bands.

    Parameters
    ----------
    results : Dict[str, AlgorithmStats]
        Benchmark results.
    output_dir : str | Path
        Directory to save plot.
    filename : str
        Output file name.
    show_std : bool
        Whether to draw standard deviation confidence bands.
    """
    setup_matplotlib_style()
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    for algo_name, stats in results.items():
        histories = np.array(stats.convergence_histories)  # shape: (trials, iterations+1)
        mean_hist = np.mean(histories, axis=0)
        std_hist = np.std(histories, axis=0)
        iterations = np.arange(len(mean_hist))

        color = COLOR_MAP.get(algo_name, "#2D3436")
        style = STYLE_MAP.get(algo_name, {"linestyle": "-", "marker": "o"})

        # Plot mean curve
        ax.plot(
            iterations,
            mean_hist,
            label=algo_name,
            color=color,
            linestyle=style["linestyle"],
            linewidth=2.2,
            markevery=max(1, len(iterations) // 10),
            markersize=6,
        )

        # Plot shaded std deviation band
        if show_std:
            ax.fill_between(
                iterations,
                np.maximum(0, mean_hist - std_hist),
                mean_hist + std_hist,
                color=color,
                alpha=0.15,
            )

    ax.set_title("Algorithm Convergence Comparison (Fitness vs Iteration)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Iteration / Generation", fontsize=11, fontweight="medium")
    ax.set_ylabel("Best Objective Value (Fitness)", fontsize=11, fontweight="medium")
    ax.grid(True)
    ax.legend(frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=10, loc="upper right")

    plt.tight_layout()

    out_path = Path(output_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved convergence plot: {out_path}")


def plot_metrics_comparison(
    results: Dict[str, AlgorithmStats],
    output_dir: str | Path = "plots",
    filename: str = "metrics_comparison.png",
):
    """Plot 2x2 panel comparing Fitness, Distance, Travel Time, and Runtime.

    Parameters
    ----------
    results : Dict[str, AlgorithmStats]
        Benchmark results.
    output_dir : str | Path
    filename : str
    """
    setup_matplotlib_style()
    fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=300)
    axes = axes.flatten()

    algos = list(results.keys())
    colors = [COLOR_MAP.get(name, "#2D3436") for name in algos]
    x_pos = np.arange(len(algos))

    # Metric 1: Mean Fitness (lower is better)
    fit_means = [results[a].fitness_mean for a in algos]
    fit_stds = [results[a].fitness_std for a in algos]
    bars1 = axes[0].bar(x_pos, fit_means, yerr=fit_stds, capsize=5, color=colors, alpha=0.85, edgecolor="#333333")
    axes[0].set_title("Mean Fitness (Lower is Better)", fontweight="bold", fontsize=12)
    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels(algos, rotation=15, ha="right", fontsize=9)
    axes[0].grid(axis="y")
    for bar in bars1:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + (0.02 * yval if yval > 0 else 0.5), f"{yval:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")

    # Metric 2: Total Distance (km)
    dist_means = [results[a].distance_mean for a in algos]
    dist_stds = [np.std(results[a].raw_distances) for a in algos]
    bars2 = axes[1].bar(x_pos, dist_means, yerr=dist_stds, capsize=5, color=colors, alpha=0.85, edgecolor="#333333")
    axes[1].set_title("Total Route Distance (km)", fontweight="bold", fontsize=12)
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(algos, rotation=15, ha="right", fontsize=9)
    axes[1].grid(axis="y")
    for bar in bars2:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2.0, yval + 1.0, f"{yval:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")

    # Metric 3: Total Travel Time (min)
    time_means = [results[a].travel_time_mean for a in algos]
    time_stds = [np.std(results[a].raw_travel_times) for a in algos]
    bars3 = axes[2].bar(x_pos, time_means, yerr=time_stds, capsize=5, color=colors, alpha=0.85, edgecolor="#333333")
    axes[2].set_title("Total Travel Time (minutes)", fontweight="bold", fontsize=12)
    axes[2].set_xticks(x_pos)
    axes[2].set_xticklabels(algos, rotation=15, ha="right", fontsize=9)
    axes[2].grid(axis="y")
    for bar in bars3:
        yval = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width()/2.0, yval + 1.0, f"{yval:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")

    # Metric 4: Runtime (seconds)
    runtime_means = [results[a].runtime_mean for a in algos]
    runtime_stds = [np.std(results[a].raw_runtimes) for a in algos]
    bars4 = axes[3].bar(x_pos, runtime_means, yerr=runtime_stds, capsize=5, color=colors, alpha=0.85, edgecolor="#333333")
    axes[3].set_title("Execution Runtime (seconds)", fontweight="bold", fontsize=12)
    axes[3].set_xticks(x_pos)
    axes[3].set_xticklabels(algos, rotation=15, ha="right", fontsize=9)
    axes[3].grid(axis="y")
    for bar in bars4:
        yval = bar.get_height()
        axes[3].text(bar.get_x() + bar.get_width()/2.0, yval + 0.01, f"{yval:.3f}s", ha="center", va="bottom", fontsize=8, fontweight="bold")

    fig.suptitle("Performance Comparison Across Benchmark Metrics", fontsize=15, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    out_path = Path(output_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved metrics comparison plot: {out_path}")


def plot_route_map_comparison(
    graph: TransportationGraph,
    vrp: VRPInstance,
    results: Dict[str, AlgorithmStats],
    output_dir: str | Path = "plots",
    filename: str = "route_visualizations.png",
):
    """Plot 2D spatial route maps side-by-side for each algorithm's best solution.

    Parameters
    ----------
    graph : TransportationGraph
    vrp : VRPInstance
    results : Dict[str, AlgorithmStats]
    output_dir : str | Path
    filename : str
    """
    setup_matplotlib_style()
    num_algos = len(results)
    cols = 2
    rows = (num_algos + 1) // 2
    fig, axes = plt.subplots(rows, cols, figsize=(13, 6 * rows), dpi=300)
    axes = axes.flatten()

    # Route line colors per vehicle
    vehicle_colors = ["#E74C3C", "#3498DB", "#2ECC71", "#9B59B6", "#F1C40F"]

    node_pos = {n: (graph.graph.nodes[n]["x"], graph.graph.nodes[n]["y"]) for n in graph.graph.nodes()}

    for idx, (algo_name, stats) in enumerate(results.items()):
        ax = axes[idx]
        routes = stats.best_overall_routes

        # 1. Draw underlying graph edges faintly
        for u, v in graph.graph.edges():
            x1, y1 = node_pos[u]
            x2, y2 = node_pos[v]
            ax.plot([x1, x2], [y1, y2], color="#E0E0E0", lw=1.0, zorder=1)

        # 2. Draw nodes
        for node, (x, y) in node_pos.items():
            if node == vrp.depot:
                ax.scatter(x, y, c="#F39C12", s=180, marker="*", edgecolor="black", zorder=4, label="Depot" if idx == 0 else "")
                ax.text(x + 1.2, y + 1.2, "Depot", fontsize=8, fontweight="bold", color="#B7950B")
            elif node in vrp.customer_ids:
                c_info = vrp.customer_by_node(node)
                demand = c_info.demand if c_info else 10
                ax.scatter(x, y, c="#34495E", s=50 + demand * 3, marker="o", edgecolor="white", zorder=3)
                ax.text(x + 1.0, y + 1.0, f"C{node}", fontsize=7, color="#2C3E50")
            else:
                ax.scatter(x, y, c="#BDC3C7", s=30, marker="o", zorder=2)

        # 3. Draw vehicle routes
        for v_idx, route in enumerate(routes):
            color = vehicle_colors[v_idx % len(vehicle_colors)]
            for i in range(len(route) - 1):
                u, v = route[i], route[i + 1]
                path, _ = graph.dijkstra(u, v)
                if not path:
                    path = [u, v]

                for p in range(len(path) - 1):
                    pu, pv = path[p], path[p + 1]
                    x1, y1 = node_pos[pu]
                    x2, y2 = node_pos[pv]
                    ax.annotate(
                        "",
                        xy=(x2, y2),
                        xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color=color, lw=2.0, shrinkA=5, shrinkB=5),
                        zorder=5,
                    )

        ax.set_title(f"{algo_name}\nBest Fitness: {stats.fitness_min:.2f} | Dist: {stats.raw_distances[0]:.1f}km", fontsize=11, fontweight="bold")
        ax.set_xlabel("X Coordinate (km)", fontsize=9)
        ax.set_ylabel("Y Coordinate (km)", fontsize=9)
        ax.grid(True)

    # Hide extra subplots if odd number of algos
    for extra in range(idx + 1, len(axes)):
        axes[extra].set_visible(False)

    fig.suptitle("Spatial Route Maps (Vehicle Paths on Transportation Graph)", fontsize=15, fontweight="bold", y=0.99)
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    out_path = Path(output_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved route visualization plot: {out_path}")


def plot_traffic_impact(
    dynamic_results: Dict[str, Dict[str, OptimizationResult]],
    output_dir: str | Path = "plots",
    filename: str = "traffic_dynamic_comparison.png",
):
    """Plot bar chart showing fitness response before vs after road congestion spike.

    Parameters
    ----------
    dynamic_results : Dict[str, Dict[str, OptimizationResult]]
    output_dir : str | Path
    filename : str
    """
    setup_matplotlib_style()
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    algos = list(dynamic_results.keys())
    x = np.arange(len(algos))
    width = 0.35

    normal_fits = [dynamic_results[a]["normal"].best_fitness for a in algos]
    congested_fits = [dynamic_results[a]["congested"].best_fitness for a in algos]

    rects1 = ax.bar(x - width/2, normal_fits, width, label="Normal Traffic", color="#2ECC71", alpha=0.85, edgecolor="#1B4D3E")
    rects2 = ax.bar(x + width/2, congested_fits, width, label="Heavy Congestion (Spike on Edge 0→1)", color="#E74C3C", alpha=0.85, edgecolor="#78281F")

    ax.set_title("Algorithm Performance Under Dynamic Traffic Congestion", fontsize=14, fontweight="bold", pad=12)
    ax.set_ylabel("Best Objective Value (Fitness)", fontsize=11, fontweight="medium")
    ax.set_xticks(x)
    ax.set_xticklabels(algos, fontsize=10, fontweight="bold")
    ax.legend(frameon=True, facecolor="white", edgecolor="#DDDDDD", fontsize=10)
    ax.grid(axis="y")

    # Add labels
    for rect in rects1:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.0, h + 1.0, f"{h:.1f}", ha="center", va="bottom", fontsize=8)

    for rect in rects2:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.0, h + 1.0, f"{h:.1f}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()

    out_path = Path(output_dir) / filename
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved traffic dynamic comparison plot: {out_path}")


def plot_research_results(results_dir: str | Path) -> None:
    """Plot all raw paired runs; uncertainty is never hidden behind one run."""
    import json
    results_dir = Path(results_dir)
    records = json.loads((results_dir / "raw_results.json").read_text())
    if not records:
        return
    plot_dir = results_dir / "plots"; plot_dir.mkdir(parents=True, exist_ok=True)
    from collections import defaultdict
    buckets = defaultdict(list)
    for record in records:
        buckets[(record["network_size"], record["algorithm"], record["traffic_mode"])].append(record)
    grouped = []
    for (size, algorithm, mode), runs in buckets.items():
        def mean(name): return float(np.mean([r[name] for r in runs]))
        def std(name): return float(np.std([r[name] for r in runs]))
        grouped.append({"network_size": size, "algorithm": algorithm, "traffic_mode": mode,
                        "objective_mean": mean("objective"), "objective_std": std("objective"),
                        "runtime_mean": mean("runtime_seconds"), "runtime_std": std("runtime_seconds"),
                        "evaluations_mean": mean("objective_evaluations"),
                        "feasibility_rate": mean("feasible"), "violation_mean": mean("constraint_violation")})
    import csv
    with (plot_dir / "aggregate_statistics.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=grouped[0].keys()); writer.writeheader(); writer.writerows(grouped)
    for metric, label in (("objective_mean", "Objective"), ("runtime_mean", "Runtime (s)"),
                          ("evaluations_mean", "Objective evaluations"), ("feasibility_rate", "Feasibility rate"),
                          ("violation_mean", "Mean constraint violation")):
        fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
        for algorithm, mode in sorted({(r["algorithm"], r["traffic_mode"]) for r in grouped}):
            part = sorted((r for r in grouped if r["algorithm"] == algorithm and r["traffic_mode"] == mode), key=lambda r: r["network_size"])
            xs, ys = [r["network_size"] for r in part], [r[metric] for r in part]
            ax.plot(xs, ys, marker="o", label=f"{algorithm.upper()} / {mode}")
            if metric in {"objective_mean", "runtime_mean"}:
                sd = [r[metric.replace("_mean", "_std")] for r in part]
                ax.fill_between(xs, np.array(ys) - np.array(sd), np.array(ys) + np.array(sd), alpha=.15)
        ax.set(xlabel="Network size (nodes, depot included)", ylabel=label, title=f"{label} by network size")
        ax.legend(); ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(plot_dir / f"{metric}.png"); plt.close(fig)
    # Evaluation-indexed convergence retains every run in raw JSON; plot means per paired group.
    fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
    for algorithm, mode in sorted({(r["algorithm"], r["traffic_mode"]) for r in records}):
        curves = [r["convergence"] for r in records if r["algorithm"] == algorithm and r["traffic_mode"] == mode and r["convergence"]]
        if not curves: continue
        grid = np.linspace(0, min(c[-1]["evaluations"] for c in curves), 100)
        values = [np.interp(grid, [p["evaluations"] for p in c], [p["best_fitness"] for p in c]) for c in curves]
        ax.plot(grid, np.mean(values, axis=0), label=f"{algorithm.upper()} / {mode}")
    ax.set(xlabel="Objective evaluations", ylabel="Best-so-far objective", title="Aggregate convergence (all sizes pooled)")
    ax.legend(); ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(plot_dir / "convergence.png"); plt.close(fig)


def generate_experiment_plots(experiment_dir: str | Path) -> list[Path]:
    """Generate aggregate all-algorithm plots from sorted raw records."""
    from backend.benchmarks.analysis import aggregate_experiment, load_raw_results
    experiment_dir = Path(experiment_dir)
    rows = aggregate_experiment(experiment_dir)
    raw = load_raw_results(experiment_dir)
    target = experiment_dir / "plots"; target.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    colors = {"qpso": "#6C5CE7", "pso": "#E17055", "ga": "#00B894", "random": "#636E72", "alns": "#0984E3"}
    for mode in ("static", "dynamic"):
        part = [r for r in rows if r["traffic_mode"] == mode]
        for metric, label in (("objective", "Objective"), ("runtime_seconds", "Runtime (s)"),
                              ("objective_evaluations", "Objective evaluations"), ("constraint_violation", "Constraint violation"),
                              ("feasibility_rate", "Feasibility rate")):
            fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
            for algorithm in sorted({r["algorithm"] for r in part}):
                series = sorted((r for r in part if r["algorithm"] == algorithm), key=lambda r: r["network_size"])
                x = [r["network_size"] for r in series]
                if metric == "feasibility_rate":
                    y, sd = [r[metric] for r in series], None
                else:
                    y, sd = [r[f"{metric}_mean"] for r in series], [r[f"{metric}_std"] for r in series]
                ax.errorbar(x, y, yerr=sd, marker="o", capsize=3, label=algorithm.upper(), color=colors.get(algorithm))
            ax.set(xlabel="Network size (nodes)", ylabel=label, title=f"{mode.title()} traffic: {label}")
            ax.grid(alpha=.3); ax.legend(); fig.tight_layout()
            path = target / f"{mode}_{metric}.png"; fig.savefig(path); plt.close(fig); saved.append(path)
    # Aggregate convergence is evaluated on a common evaluation grid for each condition.
    for mode in ("static", "dynamic"):
        fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
        for algorithm in sorted({r["algorithm"] for r in raw if r["traffic_mode"] == mode}):
            curves = [r["convergence"] for r in raw if r["algorithm"] == algorithm and r["traffic_mode"] == mode and r["convergence"]]
            grid = np.linspace(0, min(c[-1]["evaluations"] for c in curves), 100)
            values = [np.interp(grid, [p["evaluations"] for p in c], [p["best_fitness"] for p in c]) for c in curves]
            ax.plot(grid, np.mean(values, axis=0), label=algorithm.upper(), color=colors.get(algorithm))
        ax.set(xlabel="Objective evaluations", ylabel="Best-so-far objective", title=f"{mode.title()} traffic convergence (all raw runs)")
        ax.grid(alpha=.3); ax.legend(); fig.tight_layout(); path = target / f"{mode}_convergence.png"; fig.savefig(path); plt.close(fig); saved.append(path)
    # Direct static-to-dynamic degradation in mean final objective.
    fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
    for algorithm in sorted({r["algorithm"] for r in rows}):
        static = {r["network_size"]: r["objective_mean"] for r in rows if r["algorithm"] == algorithm and r["traffic_mode"] == "static"}
        dynamic = {r["network_size"]: r["objective_mean"] for r in rows if r["algorithm"] == algorithm and r["traffic_mode"] == "dynamic"}
        sizes = sorted(static.keys() & dynamic.keys())
        if sizes: ax.plot(sizes, [dynamic[n] - static[n] for n in sizes], marker="o", label=algorithm.upper(), color=colors.get(algorithm))
    ax.set(xlabel="Network size (nodes)", ylabel="Dynamic − static objective", title="Traffic-induced objective degradation")
    ax.grid(alpha=.3); ax.legend(); fig.tight_layout(); path = target / "dynamic_minus_static_objective.png"; fig.savefig(path); plt.close(fig); saved.append(path)
    if not all(path.exists() for path in saved): raise RuntimeError("Plot generation did not create every expected image")
    return saved
