"""
Random-Key Encoding & Route Decoder

Bridges the continuous QPSO search space and the discrete VRP domain.

Encoding:
    A particle is a vector x ∈ R^N  (N = number of customers).
    Each component x_d ∈ [0, 1] is a *priority key*.

Decoding:
    1. Sort keys to obtain a customer permutation.
    2. Greedily split the permutation into vehicle tours
       that respect vehicle capacity Q.
    3. Each tour starts and ends at the depot.
"""

from __future__ import annotations

import numpy as np

try:
    from backend.optimizer.vrp_instance import VRPInstance
except ImportError:
    from optimizer.vrp_instance import VRPInstance


def decode_random_keys(
    keys: np.ndarray,
    instance: VRPInstance,
    time_step: int = 0,
) -> list[list[int]]:
    """Convert a continuous random-key vector into a set of vehicle routes.

    Parameters
    ----------
    keys : np.ndarray, shape (N,)
        Continuous priority keys, one per customer.
    instance : VRPInstance
        The VRP problem definition.
    time_step : int
        Current time step (for dynamic edge costs).

    Returns
    -------
    list[list[int]]
        List of routes. Each route is a list of node IDs
        starting and ending at the depot.
        Example: [[0, 3, 7, 0], [0, 1, 5, 0]]
    """
    n_customers = instance.num_customers
    assert len(keys) == n_customers, (
        f"Key vector length {len(keys)} != num_customers {n_customers}"
    )

    # Step 1: produce customer visit order by sorting keys
    sorted_indices = np.argsort(keys)
    customer_order = [instance.customers[i].node_id for i in sorted_indices]
    demand_order = [instance.customers[i].demand for i in sorted_indices]

    # Step 2: greedy split into capacity-feasible routes
    depot = instance.depot
    capacity = instance.vehicle_capacity
    routes: list[list[int]] = []
    current_route: list[int] = [depot]
    current_load = 0.0

    for cust_node, demand in zip(customer_order, demand_order):
        if current_load + demand > capacity and len(current_route) > 1:
            # Close the current route and start a new one
            current_route.append(depot)
            routes.append(current_route)
            current_route = [depot]
            current_load = 0.0

        current_route.append(cust_node)
        current_load += demand

    # Close the last route
    if len(current_route) > 1:
        current_route.append(depot)
        routes.append(current_route)

    return routes
