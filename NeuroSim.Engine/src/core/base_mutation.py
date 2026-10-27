# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/core/base_mutation.py
from abc import ABC, abstractmethod
from typing import List


class BaseMutation(ABC):
    """Abstract interface for mutation operators."""

    @abstractmethod
    def mutate(self, individual: List[int], rng) -> List[int]:
        pass