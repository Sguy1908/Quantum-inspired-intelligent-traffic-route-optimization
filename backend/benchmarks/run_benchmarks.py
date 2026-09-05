"""Run the paired static/dynamic QPSO--ALNS research benchmark."""
from __future__ import annotations
import argparse
import os
import sys
from dataclasses import fields
from pathlib import Path
import yaml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.benchmarks.benchmark_runner import BenchmarkConfig, BenchmarkRunner
from backend.benchmarks.visualization import plot_research_results


def load_config(path: str | None) -> BenchmarkConfig:
    if path is None: return BenchmarkConfig()
    raw = yaml.safe_load(Path(path).read_text()) or {}
    valid = {f.name for f in fields(BenchmarkConfig)}
    unknown = set(raw) - valid
    if unknown: raise ValueError(f"Unknown benchmark configuration keys: {sorted(unknown)}")
    return BenchmarkConfig(**raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="YAML benchmark configuration")
    parser.add_argument("--plot", action="store_true", help="Generate plots after benchmark")
    args = parser.parse_args()
    config = load_config(args.config)
    records = BenchmarkRunner(config).run()
    if args.plot: plot_research_results(config.output_dir)
    print(f"Wrote {len(records)} raw runs to {config.output_dir}")

if __name__ == "__main__": main()
