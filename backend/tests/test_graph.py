#!/usr/bin/env python3
"""
Unit tests for TransportationGraph and DynamicTrafficModel.
"""

import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.graph.graph import TransportationGraph
from backend.graph.dynamic_traffic import DynamicTrafficModel, StaticTrafficModel


def test_transportation_graph_basic():
    tg = TransportationGraph(alpha=1.0, beta=0.5, gamma=0.2)
    tg.add_node(0, x=0.0, y=0.0, node_type="depot")
    tg.add_node(1, x=3.0, y=4.0, node_type="customer")
    tg.add_edge(0, 1, distance=5.0, base_travel_time=10.0, congestion=0.5, bidirectional=True)

    assert tg.num_nodes == 2
    assert tg.num_edges == 2  # bidirectional

    # cost = alpha * tt * (1+cong) + beta * dist + gamma * cong
    # = 1.0 * 10 * 1.5 + 0.5 * 5.0 + 0.2 * 0.5 = 15.0 + 2.5 + 0.1 = 17.6
    cost = tg.edge_cost(0, 1)
    assert abs(cost - 17.6) < 1e-5

    # Route cost
    assert abs(tg.route_cost([0, 1, 0]) - 35.2) < 1e-5
    assert tg.route_cost([0, 99]) == float("inf")


def test_dijkstra_and_distance_matrix():
    tg = TransportationGraph(alpha=1.0, beta=1.0, gamma=0.0)
    tg.add_node(0)
    tg.add_node(1)
    tg.add_node(2)

    # 0 -> 1 -> 2
    tg.add_edge(0, 1, distance=2.0, base_travel_time=5.0, bidirectional=False)
    tg.add_edge(1, 2, distance=3.0, base_travel_time=5.0, bidirectional=False)

    path, cost = tg.dijkstra(0, 2)
    assert path == [0, 1, 2]
    assert abs(cost - 15.0) < 1e-5  # (5+2) + (5+3) = 15

    # Distance matrix
    mat = tg.get_distance_matrix()
    assert mat.shape == (3, 3)
    assert mat[0, 0] == 0.0
    assert abs(mat[0, 2] - 15.0) < 1e-5
    assert mat[2, 0] == float("inf")  # no path from 2 to 0


def test_dynamic_traffic_model():
    tg = TransportationGraph()
    tg.add_node(0)
    tg.add_node(1)
    tg.add_edge(0, 1, distance=10.0, base_travel_time=10.0)

    model = DynamicTrafficModel.from_graph(tg, seed=42, period=100.0)
    assert model.congestion(0, 1, 0.0) == DynamicTrafficModel.from_graph(tg, seed=42, period=100.0).congestion(0, 1, 0.0)
    assert model.travel_time(10.0, 0, 1, 0.0) != model.travel_time(10.0, 0, 1, 25.0)
    static = StaticTrafficModel({(0, 1): .5, (1, 0): .5})
    assert static.travel_time(10.0, 0, 1, 0.0) == static.travel_time(10.0, 0, 1, 99.0)
