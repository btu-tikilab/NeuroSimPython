# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/neurosim_engine/__init__.py
"""
NeuroSim.Engine (python) package root.

Core: `BaseAlgorithm`, `BitstringGA` (generic bit GA).
Samples under `NeuroSimPython/samples/poc/` import from here via `sys.path`.
"""

from neurosim_engine.binary_ga import BitIndividual, BitstringGA
from neurosim_engine.core.base_algorithm import BaseAlgorithm

__all__ = ["BaseAlgorithm", "BitIndividual", "BitstringGA"]

