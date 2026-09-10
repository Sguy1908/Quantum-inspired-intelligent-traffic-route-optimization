"""Regression coverage for the interactive API orchestration layer."""
from __future__ import annotations

import pytest

from backend.api.routes import compare_algorithms, run_simulation
from backend.api.schemas import ComparisonRequest, SimulationRequest, SimulationResponse
from backend.graph.dynamic_traffic import DynamicTrafficModel
from backend.scenarios.generator import build_scenario


def _request(algorithm="QPSO", traffic_mode="dynamic"):
    return SimulationRequest(algorithm=algorithm, traffic_mode=traffic_mode, nodes=20,
                             customers=6, vehicles=3, seed=12345, population=8,
                             max_iterations=8, max_evaluations=40)


def test_same_seed_builds_the_same_graph_and_traffic_but_different_seed_changes_it():
    first = build_scenario(seed=21, nodes=20, customers=6, vehicles=3, traffic_mode="dynamic")
    same = build_scenario(seed=21, nodes=20, customers=6, vehicles=3, traffic_mode="dynamic")
    changed = build_scenario(seed=22, nodes=20, customers=6, vehicles=3, traffic_mode="dynamic")
    assert sorted(first.simulator.graph.graph.edges(data=True)) == sorted(same.simulator.graph.graph.edges(data=True))
    assert first.simulator.traffic.metadata() == same.simulator.traffic.metadata()
    assert first.simulator.graph.get_node_positions() != changed.simulator.graph.get_node_positions()


def test_dynamic_traffic_changes_over_time_and_static_traffic_does_not():
    dynamic = build_scenario(seed=7, nodes=20, customers=6, vehicles=3, traffic_mode="dynamic")
    static = build_scenario(seed=7, nodes=20, customers=6, vehicles=3, traffic_mode="static")
    edge = next(iter(dynamic.simulator.graph.graph.edges()))
    model = dynamic.simulator.traffic
    assert isinstance(model, DynamicTrafficModel)
    assert model.congestion(*edge, 0.0) != model.congestion(*edge, model.period / 4.0)
    assert static.simulator.traffic.congestion(*edge, 0.0) == static.simulator.traffic.congestion(*edge, 1000.0)


@pytest.mark.parametrize("traffic_mode", ["static", "dynamic"])
@pytest.mark.parametrize("algorithm", ["qpso", "pso", "ga", "alns", "random"])
def test_every_optimizer_receives_the_selected_traffic_model(algorithm, traffic_mode):
    scenario = build_scenario(seed=31, nodes=20, customers=6, vehicles=3, traffic_mode=traffic_mode)
    optimizer = scenario.simulator._create_optimizer(algorithm, num_particles=8, seed=31)
    assert optimizer.evaluator.traffic is scenario.simulator.traffic
    result = optimizer.optimize(max_iterations=4, max_evaluations=20)
    assert result.objective_evaluations == 20
    assert result.best_routes


@pytest.mark.parametrize("traffic_mode", ["static", "dynamic"])
@pytest.mark.parametrize("algorithm", ["QPSO", "PSO", "GA", "ALNS", "Random Search"])
def test_run_endpoint_returns_schema_valid_route_metrics_and_trace(algorithm, traffic_mode):
    payload = run_simulation(_request(algorithm, traffic_mode))
    response = SimulationResponse.model_validate(payload)
    assert response.algorithm["name"] == algorithm
    assert response.scenario["seed"] == 12345
    assert response.routes and response.expanded_routes
    assert response.metrics["distance_km"] > 0
    assert response.traffic["timeline"]
    assert response.metrics["nodes_visited"] == len(set(node for route in response.routes for node in route if node != response.scenario["depot"]))


def test_compare_endpoint_runs_every_algorithm_on_one_scenario():
    request = ComparisonRequest(**_request().model_dump())
    payload = compare_algorithms(request)
    assert payload["scenario"]["seed"] == request.seed
    assert {item["name"] for item in payload["results"]} == {"QPSO", "PSO", "GA", "ALNS", "Random Search"}
    assert all(item["objective_evaluations"] == request.max_evaluations for item in payload["results"])
