"""Regression coverage for sparse ALNS histories and size-specific plots."""
import json

import numpy as np
import pytest

from backend.benchmarks.visualization import _convergence_grid, generate_experiment_plots


def _run(history, budget=5000):
    return {"objective_evaluations": budget, "convergence": [
        {"evaluations": e, "best_fitness": f} for e, f in history
    ]}


def test_sparse_history_carries_forward_to_completed_budget():
    grid, values = _convergence_grid([
        _run([(1, 100), (1402, 80)]),
        _run([(50, 110), (100, 90), (5000, 70)]),
        _run([(1, 120)]),
    ])
    np.testing.assert_array_equal(grid, [50, 100, 1402, 5000])
    np.testing.assert_array_equal(values, [
        [100, 100, 80, 80], [110, 90, 90, 70], [120, 120, 120, 120]
    ])


def test_different_completed_budgets_use_shared_range():
    grid, values = _convergence_grid([
        _run([(1, 100)], budget=2000),
        _run([(50, 110), (3000, 80)]),
    ])
    np.testing.assert_array_equal(grid, [50, 2000])
    np.testing.assert_array_equal(values, [[100, 100], [110, 110]])


def test_missing_history_is_reported():
    with pytest.raises(ValueError, match="nonempty history"):
        _convergence_grid([_run([])])


def test_plots_are_separate_for_each_size_and_traffic_mode(tmp_path):
    records = []
    for mode in ("static", "dynamic"):
        for size in (20, 50):
            for algorithm in ("alns", "pso"):
                record = _run([(1, 100)] if algorithm == "alns" else [(50, 110), (5000, 90)])
                record.update(algorithm=algorithm, traffic_mode=mode, network_size=size,
                              instance_id=0, random_seed=1, objective=record["convergence"][-1]["best_fitness"],
                              runtime_seconds=1., constraint_violation=0., total_distance=100.,
                              total_travel_time=100., feasible=True)
                records.append(record)
    (tmp_path / "raw_results.json").write_text(json.dumps(records))
    paths = generate_experiment_plots(tmp_path)
    assert len(paths) == 15
    assert all(p.is_file() and p.stat().st_size for p in paths)
    assert {p.name for p in paths if "convergence" in p.name} == {
        f"{mode}_N{size:03d}_convergence.png"
        for mode in ("static", "dynamic") for size in (20, 50)
    }
