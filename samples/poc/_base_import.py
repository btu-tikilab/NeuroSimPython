# AUTH:DEVNEUROSIM:7A3F9E2B | samples/poc/_base_import.py
"""
Import helper for `BaseAlgorithm`.

The repo doesn't ship a Python package installer for `NeuroSim.Engine`, so the sample
scripts add `NeuroSim.Engine/src` to `sys.path`.

Sample Use Only Need Reimplementation with BaseAlgorithm Clearly Explored
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


def _engine_src() -> Path:
    poc_dir = Path(__file__).resolve().parent
    neuro_sim_root = poc_dir.parents[1]  # .../NeuroSimPython
    return neuro_sim_root / "NeuroSim.Engine" / "src"


def ensure_engine_src_on_path() -> Path:
    """Insert `NeuroSim.Engine/src` on `sys.path` if missing (for POC imports)."""
    engine_src = _engine_src()
    if not (engine_src / "neurosim_engine").exists():
        raise RuntimeError(f"NeuroSim.Engine python package not found at: {engine_src}")
    s = str(engine_src)
    if s not in sys.path:
        sys.path.insert(0, s)
    return engine_src


def import_base_algorithm() -> Any:
    ensure_engine_src_on_path()
    from neurosim_engine.core.base_algorithm import BaseAlgorithm  # type: ignore

    return BaseAlgorithm

