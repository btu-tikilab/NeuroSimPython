# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/graphga/operators/selection.py
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


class RouletteWheelSelection:
    """Select individuals via roulette wheel selection."""

    def select(
        self,
        population: List,
        fitness_values: List[float],
        num_parents: int,
        rng,
    ) -> List[GraphIndividual]:
        """
        Select parents using roulette wheel selection.
        Handles negative or zero fitness values via shifting.
        """
        if len(population) != len(fitness_values):
            raise ValueError(
                f"Population size {len(population)} != "
                f"fitness_values size {len(fitness_values)}"
            )

        min_fit = min(fitness_values)
        if min_fit < 0:
            weights = [f - min_fit + 1e-6 for f in fitness_values]
        else:
            weights = [f + 1e-6 for f in fitness_values]

        return rng.choices(population, weights=weights, k=num_parents)


class RankSelection:
    """Select individuals via rank selection."""

    def select(
        self,
        population: List,
        fitness_values: List[float],
        num_parents: int,
        rng,
    ) -> List[GraphIndividual]:
        """
        Select parents using rank selection.
        Avoids scaling/negative issues by using ranks.
        """
        if len(population) != len(fitness_values):
            raise ValueError(
                f"Population size {len(population)} != "
                f"fitness_values size {len(fitness_values)}"
            )

        n = len(population)
        indexed_pop = list(enumerate(fitness_values))
        sorted_pop = sorted(indexed_pop, key=lambda x: x[1])

        rank_weights = [0] * n
        for rank, (original_idx, _) in enumerate(sorted_pop, 1):
            rank_weights[original_idx] = rank

        return rng.choices(population, weights=rank_weights, k=num_parents)