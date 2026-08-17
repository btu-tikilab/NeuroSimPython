from abc import ABC, abstractmethod
from typing import List


class BaseEncoding(ABC):
    """Abstract interface for encoding and decoding solutions."""

    @abstractmethod
    def encode(self, solution) -> List[int]:
        """Convert a problem solution to its encoded representation."""
        pass

    @abstractmethod
    def decode(self, encoded_solution: List[int]):
        """Convert an encoded representation back to a problem solution."""
        pass

    @abstractmethod
    def generate_random(self, rng) -> List[int]:
        """Generate a random encoded representation."""
        pass