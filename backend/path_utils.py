"""Central project-path bootstrap for executable experiment entry points."""
from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
BACKEND_DIR = PROJECT_ROOT / "backend"
CONFIGS_DIR = BACKEND_DIR / "configs"
RESULTS_DIR = BACKEND_DIR / "results"


def ensure_project_root() -> Path:
    """Make absolute ``backend.*`` imports work regardless of cwd."""
    root = str(PROJECT_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    return PROJECT_ROOT


def project_path(path: str | Path) -> Path:
    """Resolve relative project paths against the repository, never ``cwd``."""
    candidate = Path(path)
    return candidate if candidate.is_absolute() else PROJECT_ROOT / candidate
