"""
VRP Instance Definition

Encapsulates a Capacitated Vehicle Routing Problem with Time Windows (CVRPTW):
    - depot node
    - customer nodes with demands and time windows
    - vehicle fleet with uniform capacity
    - reference to the underlying transportation graph
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Optional

from backend.graph.graph import TransportationGraph


@dataclass
class Customer:
    """A delivery / pickup customer."""
    node_id: int
    demand: float
    time_window: tuple[float, float] = (0.0, float("inf"))
    # service_time: time spent at the customer location
    service_time: float = 0.0


@dataclass
class VRPInstance:
    """Complete description of a Capacitated VRP with Time Windows.

    Attributes
    ----------
    graph : TransportationGraph
        The underlying road network.
    depot : int
        Node ID of the central depot (vehicles start and return here).
    customers : list[Customer]
        List of customers to be served.
    num_vehicles : int
        Number of available vehicles.
    vehicle_capacity : float
        Uniform payload capacity Q for every vehicle.
    """
    graph: TransportationGraph
    depot: int
    customers: list[Customer]
    num_vehicles: int
    vehicle_capacity: float

    @property
    def num_customers(self) -> int:
        return len(self.customers)

    @property
    def customer_ids(self) -> list[int]:
        """Node IDs of all customers (excludes depot)."""
        return [c.node_id for c in self.customers]

    @property
    def demands(self) -> np.ndarray:
        """Array of customer demands, indexed by position in self.customers."""
        return np.array([c.demand for c in self.customers])

    def customer_by_node(self, node_id: int) -> Optional[Customer]:
        """Look up a Customer by its node ID."""
        for c in self.customers:
            if c.node_id == node_id:
                return c
        return None

    def __repr__(self) -> str:
        return (
            f"VRPInstance(depot={self.depot}, "
            f"customers={self.num_customers}, "
            f"vehicles={self.num_vehicles}, "
            f"capacity={self.vehicle_capacity})"
        )
