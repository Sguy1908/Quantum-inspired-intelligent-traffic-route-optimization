#!/usr/bin/env python3
"""
Unit tests for VRP encoding, objective function evaluation, and optimizers (QPSO, PSO, GA).
"""

import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.graph.graph import TransportationGraph
from backend.optimizer.vrp_instance import VRPInstance, Customer
from backend.optimizer.encoding import decode_random_keys
from backend.optimizer.objective import evaluate_solution
from backend.optimizer.qpso import QPSOOptimizer
from backend.optimizer.pso import PSOOptimizer
from backend.optimizer.ga import GAOptimizer


@pytest.fixture
def sample_vrp():
    tg = TransportationGraph(alpha=1.0, beta=0.5, gamma=0.1)
    for i in range(4):
        tg.add_node(i, x=float(i), y=0.0)

    # Fully connect all nodes
    for i in range(4):
        for j in range(4):
            if i != j:
                tg.add_edge(i, j, distance=10.0, base_travel_time=10.0, bidirectional=False)

    customers = [
        Customer(node_id=1, demand=10.0, time_window=(0.0, 100.0), service_time=5.0),
        Customer(node_id=2, demand=15.0, time_window=(0.0, 100.0), service_time=5.0),
        Customer(node_id=3, demand=20.0, time_window=(0.0, 100.0), service_time=5.0),
    ]

    return VRPInstance(
        graph=tg,
        depot=0,
        customers=customers,
        num_vehicles=2,
        vehicle_capacity=30.0,
    )


def test_random_key_decoding(sample_vrp):
    # Customer order based on keys: [0.1, 0.9, 0.4] -> customer 1, customer 3, customer 2
    keys = np.array([0.1, 0.9, 0.4])
    routes = decode_random_keys(keys, sample_vrp)

    # Vehicle capacity is 30.
    # Cust 1 (demand 10) + Cust 3 (demand 20) = 30 -> Route 1: [0, 1, 3, 0]
    # Cust 2 (demand 15) -> Route 2: [0, 2, 0]
    assert len(routes) == 2
    assert routes[0] == [0, 1, 3, 0]
    assert routes[1] == [0, 2, 0]


def test_evaluate_solution(sample_vrp):
    routes = [[0, 1, 3, 0], [0, 2, 0]]
    result = evaluate_solution(routes, sample_vrp)

    assert result["fitness"] > 0
    assert result["capacity_penalty"] == 0.0
    assert result["flow_penalty"] == 0.0
    assert result["num_vehicles_used"] == 2


def test_qpso_optimizer(sample_vrp):
    opt = QPSOOptimizer(sample_vrp, num_particles=10, seed=42)
    res = opt.optimize(max_iterations=10)

    assert res.best_fitness > 0
    assert len(res.best_routes) > 0
    assert len(res.convergence_history) == 11


def test_pso_optimizer(sample_vrp):
    opt = PSOOptimizer(sample_vrp, num_particles=10, seed=42)
    res = opt.optimize(max_iterations=10)

    assert res.best_fitness > 0
    assert len(res.best_routes) > 0


def test_ga_optimizer(sample_vrp):
    opt = GAOptimizer(sample_vrp, pop_size=10, seed=42)
    res = opt.optimize(max_iterations=10)

    assert res.best_fitness > 0
    assert len(res.best_routes) > 0
