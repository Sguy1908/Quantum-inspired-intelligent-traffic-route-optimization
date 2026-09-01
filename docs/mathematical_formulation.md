# Mathematical Formulation of the Dynamic VRP for SIH 2026

## 1. Transportation Graph Model

The road network is modeled as a weighted directed graph $G = (V, E)$, where:
- $V = \{0, 1, \dots, N\}$: Set of nodes (Node $0$ is the central depot, nodes $1 \dots N$ are customers/delivery points).
- $E = \{(i, j) \mid i, j \in V, i \neq j\}$: Set of directed road links connecting nodes.

### Dynamic Edge Weight Function
For edge $(i, j)$ at time $t$, the generalized travel cost $w_{ij}(t)$ is given by:

$$w_{ij}(t) = \alpha \cdot T_{ij}(t) + \beta \cdot D_{ij} + \gamma \cdot C_{ij}(t)$$

Where:
- $D_{ij}$: Physical distance between node $i$ and $j$.
- $T_{ij}(t)$: Dynamic travel time on link $(i, j)$ at time $t$.
- $C_{ij}(t)$: Real-time traffic congestion penalty factor on link $(i, j)$.
- $\alpha, \beta, \gamma$: Weighting coefficients balancing travel time, distance, and congestion penalty.

---

## 2. Vehicle Routing Problem (VRP) Formulation

Let $K = \{1, 2, \dots, K_{max}\}$ be the set of available vehicles, each with maximum payload capacity $Q_k = Q$.

### Decision Variables
- $x_{ijk} \in \{0, 1\}$: Equals $1$ if vehicle $k$ travels directly from node $i$ to node $j$, and $0$ otherwise.
- $t_{ik} \ge 0$: Arrival time of vehicle $k$ at node $i$.

### Objective Function
Minimize total travel cost, including time, distance, dynamic congestion, and constraint violation penalties:

$$\min Z = \sum_{k \in K} \sum_{i \in V} \sum_{j \in V} w_{ij}(t_{ik}) \cdot x_{ijk} + P_{\text{capacity}} + P_{\text{time\_window}} + P_{\text{flow}}$$

---

## 3. Constraints

### A. Capacity Constraints
$$\sum_{i \in V \setminus \{0\}} d_i \sum_{j \in V} x_{ijk} \le Q \quad \forall k \in K$$
where $d_i$ is the demand of customer $i$.

### B. Flow Constraints (Routing Integrity)
$$\sum_{k \in K} \sum_{j \in V, j \neq i} x_{ijk} = 1 \quad \forall i \in V \setminus \{0\}$$
$$\sum_{j \in V \setminus \{0\}} x_{0jk} \le 1 \quad \forall k \in K$$
$$\sum_{i \in V} x_{ijk} - \sum_{i \in V} x_{jik} = 0 \quad \forall j \in V, \forall k \in K$$

### C. Time Window Constraints
$$a_i \le t_{ik} \le b_i \quad \forall i \in V, \forall k \in K$$
where $[a_i, b_i]$ defines the allowed arrival time window for node $i$.

---

## 4. Quantum-Inspired Particle Swarm Optimization (QPSO)

QPSO represents particles in a continuous state space $\mathbf{x}_i \in \mathbb{R}^D$.

### Mean Best Position ($m_{best}$)
$$m_{best}(t) = \frac{1}{M} \sum_{i=1}^M \mathbf{p}_i(t)$$
where $\mathbf{p}_i(t)$ is the personal best position of particle $i$.

### Stochastic Update Rule
$$\mathbf{p}_{i, d}^{\text{local}} = \phi \cdot \mathbf{p}_{i, d} + (1 - \phi) \cdot \mathbf{g}_d \quad \phi \sim U(0, 1)$$
$$\mathbf{x}_{i, d}(t+1) = \mathbf{p}_{i, d}^{\text{local}} \pm \beta \cdot |m_{best, d} - \mathbf{x}_{i, d}(t)| \cdot \ln(1/u) \quad u \sim U(0, 1)$$
where $\beta$ is the contraction-expansion coefficient controlling exploration/exploitation.

---

## 5. Random-Key Encoding / Decoding

- Continuous particle dimension $D = N$ (number of customers).
- Each continuous component $x_{i, d} \in [0, 1]$ represents a priority key.
- Sorting particle components produces a customer permutation.
- The decoder splits the permutation into feasible vehicle tours based on capacity $Q$ and route cost.
