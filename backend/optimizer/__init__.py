"""Optimizer sub-package — QPSO engine, baselines, encoding, and objective."""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from backend.optimizer.vrp_instance import VRPInstance, Customer
    from backend.optimizer.encoding import decode_random_keys
    from backend.optimizer.objective import evaluate_solution
    from backend.optimizer.base import BaseOptimizer, OptimizationResult
    from backend.optimizer.qpso import QPSOOptimizer
    from backend.optimizer.pso import PSOOptimizer
    from backend.optimizer.ga import GAOptimizer
    from backend.optimizer.random_search import RandomSearchOptimizer
    from backend.optimizer.alns import ALNSOptimizer
except ImportError:
    from optimizer.vrp_instance import VRPInstance, Customer
    from optimizer.encoding import decode_random_keys
    from optimizer.objective import evaluate_solution
    from optimizer.base import BaseOptimizer, OptimizationResult
    from optimizer.qpso import QPSOOptimizer
    from optimizer.pso import PSOOptimizer
    from optimizer.ga import GAOptimizer
    from optimizer.random_search import RandomSearchOptimizer
    from optimizer.alns import ALNSOptimizer

__all__ = [
    "VRPInstance", "Customer",
    "decode_random_keys", "evaluate_solution",
    "BaseOptimizer", "OptimizationResult",
    "QPSOOptimizer", "PSOOptimizer", "GAOptimizer", "RandomSearchOptimizer", "ALNSOptimizer",
]
