from abc import ABC, abstractmethod
from typing import List


class BaseSelection(ABC):
    """Abstract interface for selection operators."""

    @abstractmethod
    def select(self, population: List, fitness_values: List[float], num_parents: int, rng) -> List:
        pass
    