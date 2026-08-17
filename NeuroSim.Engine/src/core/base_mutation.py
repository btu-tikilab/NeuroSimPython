from abc import ABC, abstractmethod
from typing import List


class BaseMutation(ABC):
    """Abstract interface for mutation operators."""

    @abstractmethod
    def mutate(self, individual: List[int], rng) -> List[int]:
        pass