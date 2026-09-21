# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/operators/mutation.py
"""
Mutation Operators
Introduce random variations to maintain population diversity
"""

from typing import List, Optional


def _validate_individual(individual):
    """Shared input validation used by every mutation operator below."""

    if not isinstance(individual, (list, tuple)):
        raise ValueError("Individual must be list or tuple")

    if len(individual) == 0:
        raise ValueError("Individual cannot be empty")


class BitFlipMutation:
    """Bit-flip mutation - each bit independently flips with probability p."""

    def __init__(self, mutation_rate: Optional[float] = None, length: Optional[int] = None):
        """
        Initialize bit-flip mutation.
        """
        if mutation_rate is not None:
            if not 0 <= mutation_rate <= 1:
                raise ValueError(
                    f"mutation_rate must be 0-1, got {mutation_rate}"
                )
            self.mutation_rate = mutation_rate

        elif length is not None:
            if length <= 0:
                raise ValueError("length must be positive")
            self.mutation_rate = 1.0 / length

        else:
            raise ValueError("Provide either mutation_rate or length")

    def mutate(self, individual: List[int], rng) -> List[int]:
        """
        Flip each bit independently with probability mutation_rate.
        """

        _validate_individual(individual)

        mutated = []

        for bit in individual:
            if rng.random() < self.mutation_rate:
                mutated.append(1 - bit)
            else:
                mutated.append(bit)

        return mutated


class SwapMutation:
    """Swap mutation - picks two random positions and swaps their bits."""

    def __init__(self, mutation_probability: float = 0.1):
        """
        Initialize swap mutation.
        """
        if not 0 <= mutation_probability <= 1:
            raise ValueError(
                f"mutation_probability must be 0-1, got {mutation_probability}"
            )
        self.mutation_probability = mutation_probability

    def mutate(self, individual: List[int], rng) -> List[int]:
        """
        Swap two random bit positions.
        """
        _validate_individual(individual)

        mutated = list(individual)

        if len(mutated) < 2:
            return mutated

        if rng.random() < self.mutation_probability:
            i, j = rng.sample(range(len(mutated)), 2)
            mutated[i], mutated[j] = mutated[j], mutated[i]

        return mutated


class InversionMutation:
    """Inversion mutation - reverses a random contiguous segment."""

    def __init__(self, mutation_probability: float = 0.1):
        """
        Initialize inversion mutation.
        """
        if not 0 <= mutation_probability <= 1:
            raise ValueError(
                f"mutation_probability must be 0-1, got {mutation_probability}"
            )
        self.mutation_probability = mutation_probability

    def mutate(self, individual: List[int], rng) -> List[int]:
        """
        Reverse a random contiguous segment of the genome.
        """
        _validate_individual(individual)

        mutated = list(individual)

        if len(mutated) < 2:
            return mutated

        if rng.random() < self.mutation_probability:
            i, j = sorted(rng.sample(range(len(mutated)), 2))
            mutated[i:j + 1] = reversed(mutated[i:j + 1])

        return mutated