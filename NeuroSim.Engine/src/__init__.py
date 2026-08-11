"""
NeuroSim Engine Package
Provides the existing generic BitstringGA implementation
and the newer modular BitGA implementation.
"""

__version__ = "1.0.0"

from .binary_ga import BitIndividual, BitstringGA
from .core.base_algorithm import BaseAlgorithm

from .bitga.engine import BitGAEngine
from .bitga.operators import (
    BitStringEncoding,
    TournamentSelection,
    UniformCrossover,
    BitFlipMutation,
)

from neurosim_problems import (
    OneMaxProblem,
    KnapsackProblem,
)

__all__ = [
    "BaseAlgorithm",
    "BitIndividual",
    "BitstringGA",
    "BitGAEngine",
    "BitStringEncoding",
    "TournamentSelection",
    "UniformCrossover",
    "BitFlipMutation",
    "OneMaxProblem",
    "KnapsackProblem",
]

