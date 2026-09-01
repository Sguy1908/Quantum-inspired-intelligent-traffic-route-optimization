#!/usr/bin/env python3
"""
Quick Demo / Test — Run the full simulator pipeline.

Usage:
    python -m tests.test_demo
    pytest tests/test_demo.py
"""

import os
import sys

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from backend.simulator.engine import build_sample_graph, build_sample_vrp, Simulator
# except ImportError:
#     from simulator.engine import build_sample_graph, build_sample_vrp, Simulator


def test_simulator_demo():
    """Integration test verifying full simulator execution and optimizer runs."""
    # ── 1. Build a 20-node transportation graph ──
    graph = build_sample_graph(num_nodes=20, seed=42)
    assert graph.num_nodes == 20

    # ── 2. Generate a VRP instance ──
    vrp = build_sample_vrp(
        graph,
        num_customers=10,
        num_vehicles=3,
        vehicle_capacity=80.0,
        seed=42,
    )
    assert vrp.num_customers == 10

    # ── 3. Create the simulator ──
    sim = Simulator(graph, vrp, seed=42)

    # ── 4. Set traffic to "normal" ──
    sim.set_traffic("normal")

    # ── 5. Run QPSO ──
    qpso_res = sim.run_optimizer("qpso", max_iterations=50, num_particles=20, seed=42)
    assert qpso_res.best_fitness > 0
    assert len(qpso_res.best_routes) > 0

    # ── 6. Dynamic re-optimization test ──
    sim.congest_edge(0, 1, congestion=2.0)
    reopt_res = sim.run_optimizer("qpso", max_iterations=50, seed=42)
    assert reopt_res.best_fitness > 0


def main():
    print("Building 20-node transportation graph...")
    graph = build_sample_graph(num_nodes=20, seed=42)
    print(f"  {graph}")

    print("Generating VRP instance...")
    vrp = build_sample_vrp(
        graph,
        num_customers=10,
        num_vehicles=3,
        vehicle_capacity=80.0,
        seed=42,
    )
    print(f"  {vrp}")

    sim = Simulator(graph, vrp, seed=42)

    print("\nApplying NORMAL traffic profile...")
    sim.set_traffic("normal")

    print("Running QPSO, PSO, GA (200 iterations, 50 particles each)...\n")
    sim.run_all(max_iterations=200, num_particles=50, seed=42)
    print(sim.summary())

    print("\n★ Simulating heavy congestion on edge 0→1...")
    sim.congest_edge(0, 1, congestion=2.0)
    print("  Re-running QPSO under new traffic conditions...\n")
    result = sim.run_optimizer("qpso", max_iterations=200, seed=42)

    print("--- QPSO (after congestion spike) ---")
    print(f"  Best Fitness: {result.best_fitness:.4f}")
    for i, route in enumerate(result.best_routes):
        print(f"  Vehicle {i+1}: {' → '.join(map(str, route))}")


if __name__ == "__main__":
    main()
