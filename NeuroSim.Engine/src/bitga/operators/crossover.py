# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/operators/crossover.py
# NeuroSim/Engine/bitga/operators/crossover.py
"""
Crossover Operators
Combine genetic material from two parents to create offspring
"""

from typing import List, Tuple


def _validate_parents(parent1, parent2):
    """Shared input validation used by every crossover operator below."""

    if not isinstance(parent1, (list, tuple)):
        raise ValueError("parent1 must be list or tuple")

    if not isinstance(parent2, (list, tuple)):
        raise ValueError("parent2 must be list or tuple")

    if len(parent1) != len(parent2):
        raise ValueError(
            f"Parent lengths must match: {len(parent1)} vs {len(parent2)}"
        )


class UniformCrossover:
    """Uniform crossover - each bit independently from either parent."""

    def __init__(self, crossover_probability: float = 0.5):
        """
        Initialize uniform crossover.
        """
        if not 0 <= crossover_probability <= 1:
            raise ValueError(
                f"crossover_probability must be 0-1, got {crossover_probability}"
            )

        self.crossover_probability = crossover_probability

    def crossover(self,
                  parent1: List[int],
                  parent2: List[int],
                  rng) -> Tuple[List[int], List[int]]:
        """
        Create two offspring by mixing bits from both parents.
        """

        _validate_parents(parent1, parent2)

        offspring1 = []
        offspring2 = []

        for i in range(len(parent1)):
            if rng.random() < self.crossover_probability:
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
            else:
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])

        return offspring1, offspring2


class SinglePointCrossover:
    """Single-point crossover - one cut point splits the genome."""

    def crossover(self,
                  parent1: List[int],
                  parent2: List[int],
                  rng) -> Tuple[List[int], List[int]]:
        """
        Swap everything after one random cut point.
        """

        _validate_parents(parent1, parent2)

        if len(parent1) < 2:
            raise ValueError("Genome length must be >= 2 for a cut point")

        cut = rng.randint(1, len(parent1) - 1)

        offspring1 = list(parent1[:cut]) + list(parent2[cut:])
        offspring2 = list(parent2[:cut]) + list(parent1[cut:])

        return offspring1, offspring2


class TwoPointCrossover:
    """Two-point crossover - the segment between two cuts swaps."""

    def crossover(self,
                  parent1: List[int],
                  parent2: List[int],
                  rng) -> Tuple[List[int], List[int]]:
        """
        Swap the segment between two random cut points.
        """

        _validate_parents(parent1, parent2)

        if len(parent1) < 3:
            raise ValueError("Genome length must be >= 3 for two cut points")

        point_a = rng.randint(1, len(parent1) - 2)
        point_b = rng.randint(point_a + 1, len(parent1) - 1)

        offspring1 = (
            list(parent1[:point_a])
            + list(parent2[point_a:point_b])
            + list(parent1[point_b:])
        )
        offspring2 = (
            list(parent2[:point_a])
            + list(parent1[point_a:point_b])
            + list(parent2[point_b:])
        )

        return offspring1, offspring2