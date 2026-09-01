"""
Transportation Network Graph Model

Represents the road network as a weighted graph G = (V, E) using NetworkX.
Each edge carries distance, base travel time, and a dynamic congestion multiplier.
The composite edge cost is:

    w_ij(t) = alpha * T_ij(t) + beta * D_ij + gamma * C_ij(t)
"""

import networkx as nx
import numpy as np
from typing import Optional


class TransportationGraph:
    """Weighted directed graph modelling a transportation network."""

    def __init__(
        self,
        alpha: float = 1.0,
        beta: float = 0.5,
        gamma: float = 0.3,
    ):
        """
        Parameters
        ----------
        alpha : float
            Weight for travel-time component.
        beta : float
            Weight for distance component.
        gamma : float
            Weight for congestion-penalty component.
        """
        self.graph = nx.DiGraph()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    # ------------------------------------------------------------------
    # Graph construction helpers
    # ------------------------------------------------------------------

    def add_node(self, node_id: int, x: float = 0.0, y: float = 0.0,
                 node_type: str = "intersection", **kwargs):
        """Add a node with spatial coordinates and optional metadata.

        Parameters
        ----------
        node_id : int
            Unique integer identifier for the node.
        x, y : float
            Spatial coordinates (for visualization / distance calculations).
        node_type : str
            One of 'depot', 'customer', 'intersection'.
        """
        self.graph.add_node(
            node_id, x=x, y=y, node_type=node_type, **kwargs
        )

    def add_edge(self, u: int, v: int, distance: float,
                 base_travel_time: float,
                 congestion: float = 0.0,
                 bidirectional: bool = True):
        """Add a road link between two nodes.

        Parameters
        ----------
        u, v : int
            Source and destination node IDs.
        distance : float
            Physical distance of the road segment (km).
        base_travel_time : float
            Travel time under free-flow conditions (minutes).
        congestion : float
            Current congestion penalty factor (0 = free-flow).
        bidirectional : bool
            If True, also adds the reverse edge with identical attributes.
        """
        attrs = dict(
            distance=distance,
            base_travel_time=base_travel_time,
            congestion=congestion,
        )
        self.graph.add_edge(u, v, **attrs)
        if bidirectional:
            self.graph.add_edge(v, u, **attrs)

    # ------------------------------------------------------------------
    # Cost computation
    # ------------------------------------------------------------------

    def edge_cost(self, u: int, v: int, time_step: int = 0) -> float:
        """Compute the composite cost w_ij(t) for a single edge.

        Parameters
        ----------
        u, v : int
            Edge endpoints.
        time_step : int
            Current discrete time step (used by dynamic traffic model).

        Returns
        -------
        float
            Composite edge cost.
        """
        data = self.graph.edges[u, v]
        distance = data["distance"]
        base_tt = data["base_travel_time"]
        congestion = data.get("congestion", 0.0)

        # Dynamic travel time = base time scaled by congestion
        travel_time = base_tt * (1.0 + congestion)

        cost = (
            self.alpha * travel_time
            + self.beta * distance
            + self.gamma * congestion
        )
        return cost

    def route_cost(self, route: list[int], time_step: int = 0) -> float:
        """Compute total cost for an ordered sequence of nodes.

        Parameters
        ----------
        route : list[int]
            Ordered node IDs forming a path (e.g. [0, 3, 7, 1, 0]).
        time_step : int
            Discrete time step for dynamic weight lookup.

        Returns
        -------
        float
            Cumulative route cost. Returns ``inf`` if any edge is missing.
        """
        total = 0.0
        for i in range(len(route) - 1):
            u, v = route[i], route[i + 1]
            if not self.graph.has_edge(u, v):
                return float("inf")
            total += self.edge_cost(u, v, time_step)
        return total

    # ------------------------------------------------------------------
    # Shortest path baseline (Dijkstra)
    # ------------------------------------------------------------------

    def dijkstra(self, source: int, target: int,
                 time_step: int = 0) -> tuple[list[int], float]:
        """Classical Dijkstra shortest path using composite edge costs.

        Returns
        -------
        tuple[list[int], float]
            (path, cost). path is [] and cost is inf if no path exists.
        """
        # Build a temporary weight attribute
        for u, v in self.graph.edges():
            self.graph.edges[u, v]["_cost"] = self.edge_cost(u, v, time_step)

        try:
            path = nx.dijkstra_path(self.graph, source, target, weight="_cost")
            cost = nx.dijkstra_path_length(self.graph, source, target,
                                           weight="_cost")
            return path, cost
        except nx.NetworkXNoPath:
            return [], float("inf")

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------

    @property
    def num_nodes(self) -> int:
        return self.graph.number_of_nodes()

    @property
    def num_edges(self) -> int:
        return self.graph.number_of_edges()

    def get_node_positions(self) -> dict[int, tuple[float, float]]:
        """Return {node_id: (x, y)} for all nodes."""
        return {
            n: (d["x"], d["y"])
            for n, d in self.graph.nodes(data=True)
        }

    def get_distance_matrix(self, time_step: int = 0) -> np.ndarray:
        """Build a full cost matrix using composite edge costs and shortest paths.

        Diagonal entries are 0.0, direct edges use edge_cost, and non-adjacent pairs
        use shortest path cost (or ``inf`` if unreachable).
        """
        for u, v in self.graph.edges():
            self.graph.edges[u, v]["_cost"] = self.edge_cost(u, v, time_step)

        nodes = sorted(self.graph.nodes())
        idx = {n: i for i, n in enumerate(nodes)}
        size = len(nodes)
        mat = np.full((size, size), np.inf)
        np.fill_diagonal(mat, 0.0)

        length_dict = dict(nx.all_pairs_dijkstra_path_length(self.graph, weight="_cost"))
        for source, targets in length_dict.items():
            if source in idx:
                s_i = idx[source]
                for target, length in targets.items():
                    if target in idx:
                        mat[s_i, idx[target]] = length

        return mat

    def __repr__(self) -> str:
        return (
            f"TransportationGraph(nodes={self.num_nodes}, "
            f"edges={self.num_edges}, "
            f"α={self.alpha}, β={self.beta}, γ={self.gamma})"
        )
