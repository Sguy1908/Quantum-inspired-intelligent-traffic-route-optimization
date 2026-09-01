"""
Objective Function & Constraint Penalties

Evaluates a decoded VRP solution and returns a scalar fitness value:

    F(R) = routing_cost + λ1 * P_capacity + λ2 * P_time_window + λ3 * P_flow

Lower fitness is better.
"""

from __future__ import annotations

import numpy as np

try:
    from backend.optimizer.vrp_instance import VRPInstance
except ImportError:
    from optimizer.vrp_instance import VRPInstance


def evaluate_solution(
    routes: list[list[int]],
    instance: VRPInstance,
    time_step: int = 0,
    lambda_capacity: float = 1000.0,
    lambda_time: float = 500.0,
    lambda_flow: float = 1000.0,
) -> dict:
    """Compute the full objective value for a set of vehicle routes.

    Parameters
    ----------
    routes : list[list[int]]
        Decoded routes, each starting and ending at the depot.
    instance : VRPInstance
        The VRP problem definition.
    time_step : int
        Current time step for dynamic edge costs.
    lambda_capacity : float
        Penalty coefficient for capacity violations.
    lambda_time : float
        Penalty coefficient for time-window violations.
    lambda_flow : float
        Penalty coefficient for invalid/missing edges (flow violations).

    Returns
    -------
    dict
        Keys: 'fitness', 'routing_cost', 'total_distance',
              'total_travel_time', 'congestion_cost',
              'capacity_penalty', 'time_penalty', 'flow_penalty',
              'num_vehicles_used'.
    """
    graph = instance.graph
    depot = instance.depot

    total_distance = 0.0
    total_travel_time = 0.0
    total_congestion = 0.0
    routing_cost = 0.0
    capacity_penalty = 0.0
    time_penalty = 0.0
    flow_penalty = 0.0
    served_customers: set[int] = set()

    for route in routes:
        route_load = 0.0
        arrival_time = 0.0

        for i in range(len(route) - 1):
            u, v = route[i], route[i + 1]

            if graph.graph.has_edge(u, v):
                edge = graph.graph.edges[u, v]
                dist = edge["distance"]
                base_tt = edge["base_travel_time"]
                cong = edge.get("congestion", 0.0)
                travel_time = base_tt * (1.0 + cong)

                total_distance += dist
                total_travel_time += travel_time
                total_congestion += cong
                routing_cost += graph.edge_cost(u, v, time_step)
                arrival_time += travel_time
            else:
                path, cost = graph.dijkstra(u, v, time_step)
                if path and cost < float("inf"):
                    for j in range(len(path) - 1):
                        pu, pv = path[j], path[j + 1]
                        edge = graph.graph.edges[pu, pv]
                        dist = edge["distance"]
                        base_tt = edge["base_travel_time"]
                        cong = edge.get("congestion", 0.0)
                        travel_time = base_tt * (1.0 + cong)

                        total_distance += dist
                        total_travel_time += travel_time
                        total_congestion += cong
                        routing_cost += graph.edge_cost(pu, pv, time_step)
                        arrival_time += travel_time
                else:
                    flow_penalty += 1.0

            # Time-window penalty and customer load accumulation for node v
            customer = instance.customer_by_node(v)
            if customer is not None and v != depot:
                served_customers.add(v)
                route_load += customer.demand
                tw_lo, tw_hi = customer.time_window
                if arrival_time < tw_lo:
                    # Early arrival — wait until window opens
                    arrival_time = tw_lo
                elif arrival_time > tw_hi:
                    # Late arrival — penalise delay
                    time_penalty += (arrival_time - tw_hi)
                arrival_time += customer.service_time

        # Capacity penalty for this route
        if route_load > instance.vehicle_capacity:
            capacity_penalty += (route_load - instance.vehicle_capacity)

    # Penalty for unserved customers
    all_customer_nodes = set(instance.customer_ids)
    unserved = all_customer_nodes - served_customers
    flow_penalty += len(unserved)

    # Penalty if we used more vehicles than available
    if len(routes) > instance.num_vehicles:
        flow_penalty += (len(routes) - instance.num_vehicles)

    fitness = (
        routing_cost
        + lambda_capacity * capacity_penalty
        + lambda_time * time_penalty
        + lambda_flow * flow_penalty
    )

    return {
        "fitness": fitness,
        "routing_cost": routing_cost,
        "total_distance": total_distance,
        "total_travel_time": total_travel_time,
        "congestion_cost": total_congestion,
        "capacity_penalty": capacity_penalty,
        "time_penalty": time_penalty,
        "flow_penalty": flow_penalty,
        "num_vehicles_used": len(routes),
    }
