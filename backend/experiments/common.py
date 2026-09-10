from __future__ import annotations
import argparse
import os
import sys
from dataclasses import fields
from pathlib import Path
import yaml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from backend.benchmarks.benchmark_runner import ALGORITHMS, BenchmarkConfig, BenchmarkRunner
from backend.benchmarks.visualization import generate_experiment_plots


def parser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("--config", default="backend/configs/sanity_benchmark.yaml")
    p.add_argument("--traffic", choices=("static", "dynamic", "both"), default="both")
    p.add_argument("--algorithms", nargs="+", choices=(*ALGORITHMS, "all"), default=["all"])
    p.add_argument("--network-sizes", nargs="+", type=int)
    p.add_argument("--instances", type=int)
    p.add_argument("--runs", type=int)
    p.add_argument("--seed-mode", choices=("fixed", "random"))
    p.add_argument("--base-seed", type=int)
    p.add_argument("--max-evaluations", type=int)
    p.add_argument("--max-iterations", type=int)
    p.add_argument("--population", type=int, help="Population/sample size for the selected random-key algorithm(s)")
    p.add_argument("--output-dir")
    p.add_argument("--experiment-id")
    p.add_argument("--traffic-period", type=float)
    p.add_argument("--traffic-c-max", type=float)
    p.add_argument("--plot", action="store_true")
    return p


def config_from_args(args) -> BenchmarkConfig:
    raw = yaml.safe_load(Path(args.config).read_text()) if args.config else {}
    valid = {f.name for f in fields(BenchmarkConfig)}
    unknown = set(raw or {}) - valid
    if unknown: raise ValueError(f"Unknown config keys: {sorted(unknown)}")
    cfg = BenchmarkConfig(**(raw or {}))
    mapping = {"network_sizes": args.network_sizes, "instances_per_size": args.instances, "runs_per_instance": args.runs,
               "seed_mode": args.seed_mode, "base_seed": args.base_seed, "max_evaluations": args.max_evaluations,
               "max_iterations": args.max_iterations, "output_dir": args.output_dir, "experiment_id": args.experiment_id,
               "traffic_period": args.traffic_period, "traffic_c_max": args.traffic_c_max}
    for name, value in mapping.items():
        if value is not None: setattr(cfg, name, value)
    if args.population is not None:
        cfg.qpso_particles = cfg.pso_particles = cfg.ga_population = cfg.random_samples = args.population
    return cfg


def execute(args, forced_algorithm: str | None = None) -> list[dict]:
    cfg = config_from_args(args)
    algorithms = [forced_algorithm] if forced_algorithm else (list(ALGORITHMS) if "all" in args.algorithms else args.algorithms)
    modes = ["static", "dynamic"] if args.traffic == "both" else [args.traffic]
    # A distinct default prevents a static/dynamic or individual/comparison run
    # from silently replacing earlier raw research data.
    if args.experiment_id is None:
        cfg.experiment_id = f"{cfg.experiment_id}_{'-'.join(sorted(algorithms))}_{args.traffic}"
    records = BenchmarkRunner(cfg).run(algorithms=algorithms, traffic_modes=modes)
    if args.plot: generate_experiment_plots(Path(cfg.output_dir) / cfg.experiment_id)
    return records
