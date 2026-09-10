"""Adapters between the optimisation core and the interactive API.

This module deliberately does not implement another solver.  It creates the
same synthetic graph/VRP structures used by the simulator and projects an
``OptimizationResult`` into data the web client can render.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.graph.dynamic_traffic import DynamicTrafficModel, StaticTrafficModel
from backend.optimizer.base import OptimizationResult
from backend.optimizer.objective import ObjectiveEvaluator
from backend.simulator.engine import Simulator, build_sample_graph, build_sample_vrp


@dataclass
class Scenario:
    simulator: Simulator
    traffic_mode: str
    seed: int


def build_scenario(
    *,
    seed: int,
    nodes: int,
    vehicles: int,
    traffic_mode: str,
    customers: int | None = None,
) -> Scenario:
    """Build one reproducible, connected scenario for one or many solvers."""
    if nodes < 3:
        raise ValueError("nodes must be at least 3")
    if vehicles < 1:
        raise ValueError("vehicles must be at least 1")
    if traffic_mode not in {"static", "dynamic"}:
        raise ValueError("traffic_mode must be 'static' or 'dynamic'")

    graph = build_sample_graph(num_nodes=nodes, seed=seed)
    # A live UI should remain responsive.  The graph may contain more nodes,
    # while a bounded subset are VRP customers unless the request specifies it.
    customer_count = customers if customers is not None else min(nodes - 1, 12)
    customer_count = min(max(1, customer_count), nodes - 1)
    instance = build_sample_vrp(
        graph,
        num_customers=customer_count,
        num_vehicles=vehicles,
        vehicle_capacity=100.0,
        seed=seed + 1,
    )
    # The interactive scenario is meant to demonstrate routing rather than
    # systematically create late deliveries from a random map scale.  Keep
    # time windows present in the instance but make them reachable; benchmark
    # configurations remain free to set stricter windows independently.
    for customer in instance.customers:
        customer.time_window = (0.0, 10_000.0)
    # The generated demands are deterministic.  Size capacity so every UI
    # fleet choice represents a potentially feasible routing problem.
    total_demand = sum(customer.demand for customer in instance.customers)
    instance.vehicle_capacity = max(100.0, max(customer.demand for customer in instance.customers), total_demand / vehicles * 1.10)

    simulator = Simulator(graph, instance, seed=seed)
    if traffic_mode == "static":
        # Static is derived from this exact graph and stays fixed for the run.
        simulator.set_traffic("moderate")
    else:
        simulator.traffic = DynamicTrafficModel.from_graph(graph, seed=seed + 2)
    return Scenario(simulator=simulator, traffic_mode=traffic_mode, seed=seed)


def _traffic_state(congestion: float) -> str:
    if congestion < 0.15:
        return "free_flow"
    if congestion < 0.50:
        return "moderate"
    return "congested"


def _coordinates(x: float, y: float) -> tuple[float, float]:
    """Place the synthetic coordinate plane consistently on the Leaflet map.

    These are visual coordinates only, not claims that the generated network
    follows real Jaipur roads.  Optimisation continues to use the original
    synthetic x/y metric coordinates.
    """
    return 26.55 + y / 100.0 * 0.42, 75.10 + x / 100.0 * 0.62


def _network_payload(scenario: Scenario) -> dict[str, list[dict[str, Any]]]:
    graph = scenario.simulator.graph.graph
    traffic = scenario.simulator.traffic
    nodes = []
    for node_id, data in sorted(graph.nodes(data=True)):
        lat, lng = _coordinates(float(data["x"]), float(data["y"]))
        nodes.append({"id": node_id, "x": data["x"], "y": data["y"], "lat": lat, "lng": lng,
                      "node_type": data.get("node_type", "intersection")})
    edges = []
    for u, v, data in sorted(graph.edges(data=True)):
        congestion = traffic.congestion(u, v, 0.0)
        travel_time = traffic.travel_time(data["base_travel_time"], u, v, 0.0)
        edges.append({"u": u, "v": v, "distance_km": data["distance"],
                      "base_time_min": data["base_travel_time"], "congestion": congestion,
                      "traffic_state": _traffic_state(congestion), "current_travel_time_min": travel_time,
                      "cost": travel_time})
    return {"nodes": nodes, "edges": edges}


def _route_timeline(scenario: Scenario, routes: list[list[int]]) -> tuple[list[dict[str, Any]], list[list[int]]]:
    """Replay returned routes with the selected traffic model edge by edge."""
    instance = scenario.simulator.vrp
    graph = scenario.simulator.graph.graph
    traffic = scenario.simulator.traffic
    evaluator = ObjectiveEvaluator(instance, traffic)
    timeline: list[dict[str, Any]] = []
    expanded_routes: list[list[int]] = []

    for vehicle_index, route in enumerate(routes):
        current_time = evaluator.start_time
        expanded = [route[0]] if route else []
        for u, v in zip(route, route[1:]):
            path = evaluator._path(u, v)
            if path is None:
                continue
            for a, b in zip(path, path[1:]):
                edge = graph.edges[a, b]
                congestion = float(traffic.congestion(a, b, current_time))
                travel_time = float(traffic.travel_time(edge["base_travel_time"], a, b, current_time))
                timeline.append({
                    "vehicle": vehicle_index + 1,
                    "u": a,
                    "v": b,
                    "distance_km": float(edge["distance"]),
                    "base_time_min": float(edge["base_travel_time"]),
                    "start_time_min": float(current_time),
                    "travel_time_min": travel_time,
                    "congestion": congestion,
                    "traffic_state": _traffic_state(congestion),
                    "cost": travel_time,
                })
                current_time += travel_time
                expanded.append(b)
            customer = instance.customer_by_node(v)
            if customer is not None:
                window_start, _ = customer.time_window
                current_time = max(current_time, window_start) + customer.service_time
        expanded_routes.append(expanded)
    return timeline, expanded_routes


def serialize_simulation(scenario: Scenario, algorithm_name: str, result: OptimizationResult) -> dict[str, Any]:
    """Turn one actual optimiser result into the public API response."""
    timeline, expanded_routes = _route_timeline(scenario, result.best_routes)
    metrics = result.metrics
    distance = float(metrics["total_distance"])
    travel_time = float(metrics["total_travel_time"])
    convergence = result.convergence_history
    first_fitness = convergence[0]["best_fitness"] if convergence else result.best_fitness
    convergence_percent = 0.0 if first_fitness <= 0 else max(0.0, (first_fitness - result.best_fitness) / first_fitness * 100.0)
    return {
        "scenario": {
            "seed": scenario.seed,
            "nodes": scenario.simulator.graph.num_nodes,
            "edges": scenario.simulator.graph.num_edges,
            "depot": scenario.simulator.vrp.depot,
            "origin": scenario.simulator.vrp.depot,
            "customers": scenario.simulator.vrp.customer_ids,
            "vehicles": scenario.simulator.vrp.num_vehicles,
            "vehicle_capacity": scenario.simulator.vrp.vehicle_capacity,
            "traffic_mode": scenario.traffic_mode,
        },
        "algorithm": {
            "name": algorithm_name,
            "iterations": max(0, len(convergence) - 1),
            "convergence_percent": float(convergence_percent),
            "runtime_ms": float(result.runtime_seconds * 1000.0),
            "objective_evaluations": result.objective_evaluations,
        },
        "traffic": {
            "mode": scenario.traffic_mode,
            "timeline": timeline,
            "metadata": scenario.simulator.traffic.metadata(),
        },
        "network": _network_payload(scenario),
        "routes": result.best_routes,
        "expanded_routes": expanded_routes,
        "metrics": {
            "distance_km": distance,
            "travel_time_min": travel_time,
            "average_speed_kmh": 0.0 if travel_time <= 0 else distance / travel_time * 60.0,
            "total_cost": float(metrics["routing_cost"] + metrics["congestion_cost"]),
            "nodes_visited": len(set(node for route in result.best_routes for node in route if node != scenario.simulator.vrp.depot)),
            "fitness": float(result.best_fitness),
            "feasible": bool(metrics["feasible"]),
            "constraint_violation": float(metrics["constraint_violation"]),
        },
        "convergence_history": convergence,
    }
