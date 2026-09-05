"""The single shared VRP objective evaluator used by every optimiser."""
from __future__ import annotations

from dataclasses import dataclass
import os
import sys
import networkx as nx

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.graph.dynamic_traffic import TrafficModel, static_traffic_from_graph
from backend.optimizer.vrp_instance import VRPInstance


@dataclass(frozen=True)
class ObjectiveConfig:
    distance_weight: float = 0.0
    travel_time_weight: float = 1.0
    congestion_weight: float = 0.0  # disabled: time already contains congestion
    capacity_penalty: float = 10_000.0
    time_window_penalty: float = 10_000.0
    route_penalty: float = 100_000.0


class ObjectiveEvaluator:
    """Evaluates routes with sequential, traffic-dependent time propagation."""
    def __init__(self, instance: VRPInstance, traffic: TrafficModel | None = None,
                 config: ObjectiveConfig | None = None, start_time: float = 0.0):
        self.instance = instance
        self.traffic = traffic or static_traffic_from_graph(instance.graph)
        self.config = config or ObjectiveConfig()
        self.start_time = start_time

    def _path(self, u: int, v: int) -> list[int] | None:
        graph = self.instance.graph.graph
        if graph.has_edge(u, v):
            return [u, v]
        try:
            return nx.shortest_path(graph, u, v, weight="distance")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def evaluate(self, routes: list[list[int]]) -> dict:
        cfg, graph, depot = self.config, self.instance.graph.graph, self.instance.depot
        distance = travel_time = congestion_exposure = 0.0
        capacity_violation = time_violation = route_violation = 0.0
        served: list[int] = []
        route_arrivals: list[list[float]] = []

        for route in routes:
            if len(route) < 3 or route[0] != depot or route[-1] != depot:
                route_violation += 1.0
                continue
            current_time, load, arrivals = self.start_time, 0.0, []
            for u, v in zip(route, route[1:]):
                path = self._path(u, v)
                if path is None:
                    route_violation += 1.0
                    continue
                for a, b in zip(path, path[1:]):
                    edge = graph.edges[a, b]
                    c = self.traffic.congestion(a, b, current_time)
                    tt = self.traffic.travel_time(edge["base_travel_time"], a, b, current_time)
                    distance += edge["distance"]
                    travel_time += tt
                    congestion_exposure += c
                    current_time += tt
                customer = self.instance.customer_by_node(v)
                if customer is not None:
                    served.append(v)
                    load += customer.demand
                    lo, hi = customer.time_window
                    if current_time < lo:
                        current_time = lo
                    elif current_time > hi:
                        time_violation += current_time - hi
                    arrivals.append(current_time)
                    current_time += customer.service_time
            capacity_violation += max(0.0, load - self.instance.vehicle_capacity)
            route_arrivals.append(arrivals)

        expected = set(self.instance.customer_ids)
        counts = {node: served.count(node) for node in expected}
        route_violation += sum(1 for node in expected if counts[node] == 0)
        route_violation += sum(max(0, count - 1) for count in counts.values())
        route_violation += max(0, len(routes) - self.instance.num_vehicles)
        violation = capacity_violation + time_violation + route_violation
        routing_cost = cfg.distance_weight * distance + cfg.travel_time_weight * travel_time
        congestion_cost = cfg.congestion_weight * congestion_exposure
        fitness = (routing_cost + congestion_cost + cfg.capacity_penalty * capacity_violation
                   + cfg.time_window_penalty * time_violation + cfg.route_penalty * route_violation)
        return {"fitness": float(fitness), "routing_cost": float(routing_cost),
                "total_distance": float(distance), "total_travel_time": float(travel_time),
                "congestion_cost": float(congestion_cost), "congestion_exposure": float(congestion_exposure),
                "capacity_penalty": float(capacity_violation), "time_penalty": float(time_violation),
                "flow_penalty": float(route_violation), "constraint_violation": float(violation),
                "feasible": violation == 0.0, "num_vehicles_used": len(routes),
                "route_arrival_times": route_arrivals}


def evaluate_solution(routes: list[list[int]], instance: VRPInstance, time_step: int = 0,
                      evaluator: ObjectiveEvaluator | None = None, **legacy_penalties) -> dict:
    """Compatibility wrapper; new code should share an ``ObjectiveEvaluator``."""
    return (evaluator or ObjectiveEvaluator(instance, start_time=float(time_step))).evaluate(routes)
