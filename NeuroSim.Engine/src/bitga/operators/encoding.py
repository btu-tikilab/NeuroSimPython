# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/operators/encoding.py
# NeuroSim/Engine/bitga/operators/encoding.py
"""
Bitstring Encoding
Generates random bitstring representations for the GA population.
"""

from typing import List


class BitStringEncoding:
    """Generate random bitstrings for the GA population."""

    def __init__(self, length: int):
        """
        Initialize bitstring encoding.
        """
        if length <= 0:
            raise ValueError("Length must be positive")

        self.length = length

    def generate_random(self, rng) -> List[int]:
        """
        Generate a random bitstring using a seeded RNG.
        """
        return [rng.randint(0, 1) for _ in range(self.length)]