"""Optimizer sub-package — QPSO engine, baselines, encoding, and objective."""

try:
    from backend.optimizer.vrp_instance import VRPInstance, Customer
    from backend.optimizer.encoding import decode_random_keys
    from backend.optimizer.objective import evaluate_solution
    from backend.optimizer.base import BaseOptimizer, OptimizationResult
    from backend.optimizer.qpso import QPSOOptimizer
    from backend.optimizer.pso import PSOOptimizer
    from backend.optimizer.ga import GAOptimizer
except ImportError:
    from optimizer.vrp_instance import VRPInstance, Customer
    from optimizer.encoding import decode_random_keys
    from optimizer.objective import evaluate_solution
    from optimizer.base import BaseOptimizer, OptimizationResult
    from optimizer.qpso import QPSOOptimizer
    from optimizer.pso import PSOOptimizer
    from optimizer.ga import GAOptimizer

__all__ = [
    "VRPInstance", "Customer",
    "decode_random_keys", "evaluate_solution",
    "BaseOptimizer", "OptimizationResult",
    "QPSOOptimizer", "PSOOptimizer", "GAOptimizer",
]
