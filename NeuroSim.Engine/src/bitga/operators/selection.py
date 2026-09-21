# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/operators/selection.py
# NeuroSim/Engine/bitga/operators/selection.py
"""
Selection Operators
Choose individuals for reproduction based on fitness
"""

from typing import List


class TournamentSelection:
    """Select individuals via tournament."""

    def __init__(self, tournament_size: int = 3):
        """
        Initialize tournament selection.
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
        """

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

        if num_parents <= 0:
            raise ValueError(
                f"num_parents must be positive, got {num_parents}"
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