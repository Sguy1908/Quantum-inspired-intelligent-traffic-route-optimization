import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from backend.simulator.engine import (
        Simulator,
        build_sample_graph,
        build_sample_vrp,
    )
except ImportError:
    from simulator.engine import (
        Simulator,
        build_sample_graph,
        build_sample_vrp,
    )

__all__ = ["Simulator", "build_sample_graph", "build_sample_vrp"]
