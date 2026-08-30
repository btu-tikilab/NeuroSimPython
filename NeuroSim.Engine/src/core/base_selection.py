# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/core/base_selection.py
from abc import ABC, abstractmethod
from typing import List


class BaseSelection(ABC):
    """Abstract interface for selection operators."""

    @abstractmethod
    def select(self, population: List, fitness_values: List[float], num_parents: int, rng) -> List:
        pass
    