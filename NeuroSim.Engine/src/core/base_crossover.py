from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseCrossover(ABC):
    """Abstract interface for crossover operators."""

    @abstractmethod
    def crossover(self, parent1: List[int], parent2: List[int], rng) -> Tuple[List[int], List[int]]:
        pass