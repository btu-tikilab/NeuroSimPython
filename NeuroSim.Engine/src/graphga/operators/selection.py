"""
Selection Operators

Choose individuals for reproduction based on fitness.
Mirrors bitga/operators/selection.py.
"""

from typing import List

from core.base_selection import BaseSelection
from graphga.utils.graph import GraphIndividual

class TournamentSelection(BaseSelection):
    """Select individuals via tournament."""

    def __init__(self, tournament_size: int = 3):
        """
        Initialize tournament selection.

        Args:
            tournament_size: Number of individuals per tournament (k).
                             Larger k = higher selection pressure.
            tournament_size default taken as 3 because it balances selection pressure and diversity.
        """
        if tournament_size < 2:
            raise ValueError("tournament_size must be >= 2")

        self.tournament_size = tournament_size

    def select(
        self,
        population: List,
        fitness_values: List[float],
        num_parents: int,
        rng,
    ) -> List[GraphIndividual]:
        """
        Select parents using tournament selection.

        Algorithm:
        1. For each parent needed:
        2. Randomly pick k individuals.
        3. Return the one with highest fitness.
        4. Repeat num_parents times.

        Args:
            population: List of Graph individuals.
            fitness_values: Fitness values corresponding to the population.
            num_parents: Number of parents to select.
            rng: Seeded random number generator.

        Returns:
            List of selected parents.
        """
        # length should be equal , for every individual have exactly one fitness value
        if len(population) != len(fitness_values):
            raise ValueError(
                f"Population size {len(population)} != "
                f"fitness_values size {len(fitness_values)}"
            )
        # it should not be greater than population size, otherwise we will get index out of range error
        if self.tournament_size > len(population):
            raise ValueError(
                f"tournament_size {self.tournament_size} > "
                f"population size {len(population)}"
            )

        parents = []
        population_size = len(population)

        for _ in range(num_parents):

            tournament_indices = [
                rng.randint(0, population_size - 1)
                for _ in range(self.tournament_size)
            ]

            winner_idx = tournament_indices[0]
            winner_fitness = fitness_values[winner_idx]

            for idx in tournament_indices[1:]:
                if fitness_values[idx] > winner_fitness:
                    winner_idx = idx
                    winner_fitness = fitness_values[idx]

            parents.append(population[winner_idx])

        return parents