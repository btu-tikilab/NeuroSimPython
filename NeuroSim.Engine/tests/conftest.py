# NeuroSim.Engine/tests/conftest.py
"""
Shared pytest configuration for NeuroSim.Engine's test suite.

Puts this repo's src/ AND NeuroSim.Problems' src/ on sys.path once,
here, so individual test files don't each need their own path hacks
(the original test_engine.py did this per-file; centralizing it here
means every test file just does `from bitga.engine import ...` etc.
directly).
"""

import sys
from pathlib import Path

_ENGINE_SRC = Path(__file__).parent.parent / "src"
_PROBLEMS_SRC = Path(__file__).parent.parent.parent / "NeuroSim.Problems" / "src"

for _path in (_ENGINE_SRC, _PROBLEMS_SRC):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import random
import pytest

from neurosim_problems import OneMaxProblem, KnapsackProblem


@pytest.fixture
def rng():
    """A fresh seeded RNG for tests that need deterministic randomness."""
    return random.Random(42)


@pytest.fixture
def onemax_small():
    """A small OneMax instance, cheap enough for fast unit tests."""
    return OneMaxProblem(length=10)


@pytest.fixture
def knapsack_small():
    """
    A small Knapsack instance with a known, hand-verifiable optimum:
    items (value, weight) = (10,5), (20,10), (30,15), capacity=20.
    True optimum is items 0+2 (value 40, weight 20) -- verified against
    brute force during development.
    """
    return KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)