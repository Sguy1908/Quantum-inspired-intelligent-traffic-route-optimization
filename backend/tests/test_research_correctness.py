import numpy as np
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.graph.dynamic_traffic import DynamicTrafficModel, StaticTrafficModel
from backend.graph.graph import TransportationGraph
from backend.optimizer.objective import ObjectiveConfig, ObjectiveEvaluator
from backend.optimizer.qpso import QPSOOptimizer
from backend.optimizer.vrp_instance import Customer, VRPInstance


def _instance():
    g = TransportationGraph()
    for node in range(3): g.add_node(node)
    for u, v in ((0, 1), (1, 2), (2, 0), (1, 0), (2, 1), (0, 2)):
        g.add_edge(u, v, distance=10., base_travel_time=10., bidirectional=False)
    return VRPInstance(g, 0, [Customer(1, 1, (0, 14), 2), Customer(2, 1, (0, 100), 0)], 1, 10)


def test_evaluator_propagates_dynamic_time_and_does_not_double_count_congestion():
    instance = _instance()
    traffic = DynamicTrafficModel({(0, 1): .5, (1, 2): .5, (2, 0): .5},
                                  {(0, 1): .5, (1, 2): .5, (2, 0): .5},
                                  {(0, 1): 0., (1, 2): np.pi / 2, (2, 0): np.pi}, period=100)
    result = ObjectiveEvaluator(instance, traffic).evaluate([[0, 1, 2, 0]])
    # edge 1->2 is entered after the traffic-dependent first leg and must not
    # be evaluated at t=0; congestion is a metric, not an unadvertised cost.
    assert result["total_travel_time"] != 30.0
    assert result["routing_cost"] == result["total_travel_time"]
    assert result["congestion_cost"] == 0.0
    assert result["time_penalty"] > 0.0


def test_qpso_is_reproducible_and_evaluation_budgeted():
    instance = _instance(); traffic = StaticTrafficModel({})
    a = QPSOOptimizer(instance, num_particles=5, seed=9, evaluator=ObjectiveEvaluator(instance, traffic)).optimize(max_iterations=30, max_evaluations=20)
    b = QPSOOptimizer(instance, num_particles=5, seed=9, evaluator=ObjectiveEvaluator(instance, traffic)).optimize(max_iterations=30, max_evaluations=20)
    assert a.best_fitness == b.best_fitness
    assert a.best_routes == b.best_routes
    assert a.objective_evaluations == b.objective_evaluations == 20
    assert all("evaluations" in p and "best_fitness" in p for p in a.convergence_history)
