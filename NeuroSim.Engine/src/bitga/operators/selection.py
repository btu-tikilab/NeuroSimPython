# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/operators/selection.py
# NeuroSim/Engine/bitga/operators/selection.py
"""
Selection Operators
Choose individuals for reproduction based on fitness
"""

from typing import List

from core.base_selection import BaseSelection


class TournamentSelection(BaseSelection):
    """Select individuals via tournament."""

    def __init__(self, tournament_size: int = 3):
        """
        Initialize tournament selection.

        Args:
            tournament_size: Number of individuals per tournament (k)
                            Larger k = higher selection pressure
        """
        if tournament_size < 2:
            raise ValueError("tournament_size must be >= 2")

        self.tournament_size = tournament_size

    def select(self,
               population: List,
               fitness_values: List[float],
               num_parents: int,
               rng) -> List:
        """
        Select parents using tournament selection.

        Algorithm:
        1. For each parent needed:
        2.   Randomly pick k individuals
        3.   Return the one with highest fitness
        4. Repeat num_parents times

        Args:
            population: List of individuals (bitstrings)
            fitness_values: List of fitness values (same order as population)
            num_parents: How many parents to select
            rng: Seeded random number generator

        Returns:
            parents: List of selected individuals
        """

        # Validate inputs
        if len(population) != len(fitness_values):
            raise ValueError(
                f"Population size {len(population)} != "
                f"fitness_values size {len(fitness_values)}"
            )

        if self.tournament_size > len(population):
            raise ValueError(
                f"tournament_size {self.tournament_size} > "
                f"population size {len(population)}"
            )

        parents = []
        population_size = len(population)

        # Select num_parents individuals
        for _ in range(num_parents):
            # Step 1: Random tournament
            tournament_indices = [
                rng.randint(0, population_size - 1)
                for _ in range(self.tournament_size)
            ]

            # Step 2: Find winner (highest fitness)
            winner_idx = tournament_indices[0]
            winner_fitness = fitness_values[winner_idx]

            for idx in tournament_indices[1:]:
                if fitness_values[idx] > winner_fitness:
                    winner_idx = idx
                    winner_fitness = fitness_values[idx]

            # Step 3: Add winner to parents
            parents.append(population[winner_idx])

        return parents