"""
PSO vs QPSO Benchmark Experiment
=================================
Runs comparative experiments across problem sizes, saves JSON results,
and generates publication-quality matplotlib visualisations — all output
goes to  backend/benchmarks/plots/.
"""

import sys
import os
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

# ---------------------------------------------------------------------------
# Project path setup
# ---------------------------------------------------------------------------
root_dir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.simulator.engine import build_sample_graph, build_sample_vrp, Simulator
from backend.optimizer.pso import PSOOptimizer
from backend.optimizer.qpso import QPSOOptimizer

# ---------------------------------------------------------------------------
# Output directory — single canonical location
# ---------------------------------------------------------------------------
PLOTS_DIR = Path(__file__).resolve().parent / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Aesthetic constants
# ---------------------------------------------------------------------------
matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    "axes.edgecolor": "#CCCCCC",
    "axes.linewidth": 0.8,
    "grid.color": "#EAEAEA",
    "grid.linestyle": "--",
    "grid.alpha": 0.7,
    "figure.facecolor": "#FAFAFA",
    "axes.facecolor": "#FAFAFA",
})

PSO_COLOR = "#2980b9"
QPSO_COLOR = "#e74c3c"
PSO_LIGHT = "#a9cce3"
QPSO_LIGHT = "#f5b7b1"
ACCENT = "#27ae60"

# ═══════════════════════════════════════════════════════════════════════════
# 1.  EXPERIMENT RUNNER
# ═══════════════════════════════════════════════════════════════════════════

def run_experiments(
    sizes: list[int] | None = None,
    seeds: list[int] | None = None,
    max_iterations: int = 200,
    num_particles: int = 50,
) -> tuple[dict, dict]:
    """Run PSO vs QPSO across *sizes* × *seeds* grid and return (raw, summary)."""
    if sizes is None:
        sizes = [10, 20, 50, 100, 200]
    if seeds is None:
        seeds = [42, 101, 202, 303, 404]

    results: dict = {}

    for N in sizes:
        print(f"================ Running N = {N} ================")
        results[N] = {
            "pso": {"fitness": [], "runtime": [], "convergence": []},
            "qpso": {"fitness": [], "runtime": [], "convergence": []},
            "delta_F": [],
        }

        num_vehicles = max(3, N // 5)
        vehicle_capacity = 100.0 + N * 0.5

        for seed in seeds:
            graph = build_sample_graph(num_nodes=N + 1, seed=seed)
            vrp = build_sample_vrp(
                graph,
                num_customers=N,
                num_vehicles=num_vehicles,
                vehicle_capacity=vehicle_capacity,
                seed=seed,
            )

            # PSO
            pso_opt = PSOOptimizer(vrp, num_particles=num_particles, seed=seed)
            pso_res = pso_opt.optimize(max_iterations=max_iterations)

            # QPSO
            qpso_opt = QPSOOptimizer(vrp, num_particles=num_particles, seed=seed)
            qpso_res = qpso_opt.optimize(max_iterations=max_iterations)

            f_pso = pso_res.best_fitness
            f_qpso = qpso_res.best_fitness

            # Delta_F = ((F_PSO - F_QPSO) / F_PSO) * 100
            delta_f = ((f_pso - f_qpso) / f_pso) * 100.0

            results[N]["pso"]["fitness"].append(f_pso)
            results[N]["pso"]["runtime"].append(pso_res.runtime_seconds)
            results[N]["pso"]["convergence"].append(pso_res.convergence_history)

            results[N]["qpso"]["fitness"].append(f_qpso)
            results[N]["qpso"]["runtime"].append(qpso_res.runtime_seconds)
            results[N]["qpso"]["convergence"].append(qpso_res.convergence_history)

            results[N]["delta_F"].append(delta_f)

            print(
                f"Seed {seed:3d} | N={N:3d} | "
                f"F_PSO: {f_pso:10.2f} | F_QPSO: {f_qpso:10.2f} | "
                f"ΔF: {delta_f:+6.2f}% | "
                f"R_PSO: {pso_res.runtime_seconds:5.3f}s | "
                f"R_QPSO: {qpso_res.runtime_seconds:5.3f}s"
            )

    # ---- Aggregate summary ----
    summary: dict = {}
    for N in sizes:
        pso_fit = np.array(results[N]["pso"]["fitness"])
        qpso_fit = np.array(results[N]["qpso"]["fitness"])
        pso_rt = np.array(results[N]["pso"]["runtime"])
        qpso_rt = np.array(results[N]["qpso"]["runtime"])
        delta_f_arr = np.array(results[N]["delta_F"])

        summary[N] = {
            "pso_fitness_mean": float(np.mean(pso_fit)),
            "pso_fitness_std": float(np.std(pso_fit)),
            "qpso_fitness_mean": float(np.mean(qpso_fit)),
            "qpso_fitness_std": float(np.std(qpso_fit)),
            "pso_runtime_mean": float(np.mean(pso_rt)),
            "qpso_runtime_mean": float(np.mean(qpso_rt)),
            "delta_F_mean": float(np.mean(delta_f_arr)),
            "delta_F_std": float(np.std(delta_f_arr)),
            "pso_conv_mean": np.mean(
                results[N]["pso"]["convergence"], axis=0
            ).tolist(),
            "qpso_conv_mean": np.mean(
                results[N]["qpso"]["convergence"], axis=0
            ).tolist(),
        }

    # ---- Save JSON ----
    json_path = PLOTS_DIR / "experiment_results.json"
    with open(json_path, "w") as f:
        json.dump({"raw": results, "summary": summary}, f, indent=2)
    print(f"\nExperiment results saved to {json_path}")

    # ---- Console summary ----
    print("\n================ SUMMARY TABLE ================")
    print(
        f"{'N':<5} | {'F_PSO (Mean)':<14} | {'F_QPSO (Mean)':<14} | "
        f"{'ΔF Mean (%)':<18} | {'R_PSO (s)':<10} | {'R_QPSO (s)':<10}"
    )
    print("-" * 85)
    for N in sizes:
        s = summary[N]
        print(
            f"{N:<5} | {s['pso_fitness_mean']:<14.2f} | "
            f"{s['qpso_fitness_mean']:<14.2f} | "
            f"{s['delta_F_mean']:<18.2f} | "
            f"{s['pso_runtime_mean']:<10.3f} | "
            f"{s['qpso_runtime_mean']:<10.3f}"
        )

    return results, summary


# ═══════════════════════════════════════════════════════════════════════════
# 2.  VISUALISATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def _resolve_summary(summary: dict) -> dict:
    """Ensure keys are ints regardless of whether loaded from JSON (str keys)."""
    return {int(k): v for k, v in summary.items()}


def plot_delta_f(summary: dict, sizes: list[int]) -> Path:
    """Plot ΔF (%) vs problem size with error bars."""
    summary = _resolve_summary(summary)
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)

    delta_means = [summary[N]["delta_F_mean"] for N in sizes]
    delta_stds = [summary[N]["delta_F_std"] for N in sizes]

    ax.axhline(0, color="#95a5a6", linestyle="--", linewidth=1.5, label="Parity (0 %)")

    ax.errorbar(
        sizes, delta_means,
        yerr=delta_stds,
        fmt="-o",
        color=QPSO_COLOR,
        ecolor=QPSO_LIGHT,
        elinewidth=2,
        capsize=6,
        linewidth=2.5,
        markersize=8,
        markeredgecolor="white",
        markeredgewidth=1.2,
        label=r"$\Delta F = \frac{F_{\mathrm{PSO}} - F_{\mathrm{QPSO}}}{F_{\mathrm{PSO}}} \times 100\%$",
    )

    # Shade regions
    ax.axhspan(0, max(max(delta_means) + 5, 5), color=ACCENT, alpha=0.06)
    ax.axhspan(min(min(delta_means) - 5, -5), 0, color=QPSO_COLOR, alpha=0.06)

    ax.set_title(
        r"QPSO Performance Gain / Loss ($\Delta F$) vs Problem Size $N$",
        fontsize=13, fontweight="bold", pad=10,
    )
    ax.set_xlabel("Problem Size N (Number of Customers)", fontsize=11)
    ax.set_ylabel(
        r"$\Delta F$ (%)  [+ve = QPSO better, –ve = PSO better]", fontsize=10
    )
    ax.set_xticks(sizes)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10, loc="best")

    plt.tight_layout()
    out = PLOTS_DIR / "delta_F_scaling.png"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f"  ✓ Saved {out.name}")
    return out


def plot_runtime(summary: dict, sizes: list[int]) -> Path:
    """Plot runtime scaling R(N) for PSO vs QPSO."""
    summary = _resolve_summary(summary)
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)

    r_pso = [summary[N]["pso_runtime_mean"] for N in sizes]
    r_qpso = [summary[N]["qpso_runtime_mean"] for N in sizes]

    ax.fill_between(sizes, r_pso, alpha=0.12, color=PSO_COLOR)
    ax.fill_between(sizes, r_qpso, alpha=0.12, color=QPSO_COLOR)
    ax.plot(sizes, r_pso, "-o", color=PSO_COLOR, linewidth=2.5, markersize=8,
            markeredgecolor="white", markeredgewidth=1.2, label="PSO Runtime R(N)")
    ax.plot(sizes, r_qpso, "-s", color=QPSO_COLOR, linewidth=2.5, markersize=8,
            markeredgecolor="white", markeredgewidth=1.2, label="QPSO Runtime R(N)")

    ax.set_title("Execution Runtime R(N) vs Problem Size N",
                 fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Problem Size N (Number of Customers)", fontsize=11)
    ax.set_ylabel("Mean Runtime R(N) [Seconds]", fontsize=11)
    ax.set_xticks(sizes)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10, loc="upper left")

    plt.tight_layout()
    out = PLOTS_DIR / "runtime_scaling.png"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f"  ✓ Saved {out.name}")
    return out


def plot_convergence(summary: dict, sizes: list[int]) -> Path:
    """Plot mean convergence profiles F(t) for each N in a 2×3 subplot grid."""
    summary = _resolve_summary(summary)
    fig, axes = plt.subplots(2, 3, figsize=(16, 9.5), dpi=300)
    axes = axes.flatten()

    for idx, N in enumerate(sizes):
        ax = axes[idx]
        pso_c = summary[N]["pso_conv_mean"]
        qpso_c = summary[N]["qpso_conv_mean"]
        iters = range(len(pso_c))

        ax.plot(iters, pso_c, color=PSO_COLOR, linewidth=2, label="PSO", alpha=0.9)
        ax.plot(iters, qpso_c, color=QPSO_COLOR, linewidth=2, label="QPSO", alpha=0.9)
        ax.fill_between(iters, pso_c, alpha=0.08, color=PSO_COLOR)
        ax.fill_between(iters, qpso_c, alpha=0.08, color=QPSO_COLOR)

        ax.set_title(f"Convergence F(t) — N = {N}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Iteration t", fontsize=9)
        ax.set_ylabel("Mean Fitness F(t)", fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9, loc="upper right")
        ax.set_yscale("log")

    # Hide 6th empty subplot
    axes[5].axis("off")

    fig.suptitle(
        "Mean Convergence Profiles F(t) Across Problem Sizes",
        fontsize=14, fontweight="bold",
    )
    plt.tight_layout()
    out = PLOTS_DIR / "convergence_profiles.png"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f"  ✓ Saved {out.name}")
    return out


def plot_fitness_comparison(summary: dict, sizes: list[int]) -> Path:
    """Grouped bar chart comparing mean fitness for PSO vs QPSO at each N."""
    summary = _resolve_summary(summary)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    x = np.arange(len(sizes))
    width = 0.35

    pso_means = [summary[N]["pso_fitness_mean"] for N in sizes]
    pso_stds = [summary[N]["pso_fitness_std"] for N in sizes]
    qpso_means = [summary[N]["qpso_fitness_mean"] for N in sizes]
    qpso_stds = [summary[N]["qpso_fitness_std"] for N in sizes]

    bars_pso = ax.bar(
        x - width / 2, pso_means, width,
        yerr=pso_stds, capsize=5,
        color=PSO_COLOR, alpha=0.85, edgecolor="#1a5276",
        label="PSO",
    )
    bars_qpso = ax.bar(
        x + width / 2, qpso_means, width,
        yerr=qpso_stds, capsize=5,
        color=QPSO_COLOR, alpha=0.85, edgecolor="#78281f",
        label="QPSO",
    )

    # Value labels
    for bar in bars_pso:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.02 * h,
                f"{h:.0f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    for bar in bars_qpso:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.02 * h,
                f"{h:.0f}", ha="center", va="bottom", fontsize=8, fontweight="bold")

    ax.set_title("Mean Best Fitness by Problem Size (Lower Is Better)",
                 fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Problem Size N", fontsize=11)
    ax.set_ylabel("Mean Best Fitness", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels([str(n) for n in sizes], fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=10)

    plt.tight_layout()
    out = PLOTS_DIR / "fitness_comparison.png"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f"  ✓ Saved {out.name}")
    return out


def plot_heatmap(summary: dict, sizes: list[int]) -> Path:
    """Heatmap of ΔF (%) across sizes for a quick visual summary."""
    summary = _resolve_summary(summary)
    fig, ax = plt.subplots(figsize=(8, 2.5), dpi=300)

    delta_means = np.array([[summary[N]["delta_F_mean"] for N in sizes]])

    cmap = plt.cm.RdYlGn  # Red = QPSO worse, Green = QPSO better
    im = ax.imshow(delta_means, cmap=cmap, aspect="auto", vmin=-15, vmax=15)

    ax.set_xticks(range(len(sizes)))
    ax.set_xticklabels([f"N={n}" for n in sizes], fontsize=10, fontweight="bold")
    ax.set_yticks([0])
    ax.set_yticklabels(["ΔF (%)"], fontsize=10)

    # Annotate cells
    for j, val in enumerate(delta_means[0]):
        color = "white" if abs(val) > 8 else "black"
        ax.text(j, 0, f"{val:+.1f}%", ha="center", va="center",
                fontsize=11, fontweight="bold", color=color)

    cbar = fig.colorbar(im, ax=ax, orientation="vertical", fraction=0.03, pad=0.04)
    cbar.set_label("ΔF (%)  [+ve = QPSO better]", fontsize=9)

    ax.set_title("ΔF Heatmap Across Problem Sizes", fontsize=12, fontweight="bold", pad=8)
    plt.tight_layout()
    out = PLOTS_DIR / "delta_F_heatmap.png"
    fig.savefig(out, dpi=300)
    plt.close(fig)
    print(f"  ✓ Saved {out.name}")
    return out


def generate_all_plots(summary: dict, sizes: list[int] | None = None) -> list[Path]:
    """Generate the full visualisation suite and return list of saved paths."""
    if sizes is None:
        sizes = [10, 20, 50, 100, 200]

    print("\n📊 Generating plots …")
    saved: list[Path] = []
    saved.append(plot_delta_f(summary, sizes))
    saved.append(plot_runtime(summary, sizes))
    saved.append(plot_convergence(summary, sizes))
    saved.append(plot_fitness_comparison(summary, sizes))
    saved.append(plot_heatmap(summary, sizes))
    print(f"\n✅ All {len(saved)} plots saved to {PLOTS_DIR}/")
    return saved


# ═══════════════════════════════════════════════════════════════════════════
# 3.  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Run experiments and immediately generate all plots."""
    _raw, summary = run_experiments()
    generate_all_plots(summary)


if __name__ == "__main__":
    main()
