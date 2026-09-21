# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/engine.py
"""
Main BitGA Engine
Implements the BaseAlgorithm lifecycle
"""

import random

from core.base_algorithm import BaseAlgorithm

from .operators import (
    BitStringEncoding,
    TournamentSelection,
    UniformCrossover,
    BitFlipMutation,
)


class BitGAEngine(BaseAlgorithm):
    """Bitstring Genetic Algorithm."""

    def __init__(
        self,
        problem,
        population_size=100,
        generations=100,
        bitstring_length=20,
        tournament_size=3,
        mutation_rate=None,
        crossover_probability=0.8,
        seed=42,
        crossover=None,
        mutation=None,
    ):

        self.problem = problem
        self.bitstring_length = bitstring_length

        self._rng = random.Random(seed)

        super().__init__(
            population_size=population_size,
            max_generations=generations,
            rng=self._rng,
        )

        self.encoding = BitStringEncoding(bitstring_length)
        self.selection = TournamentSelection(tournament_size)

        self.crossover = (
            crossover if crossover is not None
            else UniformCrossover(crossover_probability)
        )

        self.mutation = (
            mutation if mutation is not None
            else BitFlipMutation(mutation_rate=mutation_rate, length=bitstring_length)
        )

        self.fitness_values = None

    def initialize(self):
        """
        Create the initial population of random bit individuals.
        """

        return [
            self.encoding.generate_random(self._rng)
            for _ in range(self.population_size)
        ]

    def evaluate(self, population):
        """
        Evaluate the fitness of every individual.
        """

        self.fitness_values = [
            self.problem.fitness(ind)
            for ind in population
        ]

        return population

    def select(self, population):
        """
        Select parents using Tournament Selection.
        """

        return self.selection.select(
            population,
            self.fitness_values,
            self.population_size,
            self._rng,
        )

    def breed(self, parents):
        """
        Generate offspring using crossover and mutation.
        """

        offspring = []

        for i in range(0, len(parents), 2):

            if i + 1 < len(parents):

                child1, child2 = self.crossover.crossover(
                    parents[i],
                    parents[i + 1],
                    self._rng,
                )

                offspring.append(self.mutation.mutate(child1, self._rng))
                offspring.append(self.mutation.mutate(child2, self._rng))

            else:

                offspring.append(
                    self.mutation.mutate(parents[i], self._rng)
                )

        return offspring

    def replace(self, population, offspring):
        """
        Replace the current population with the offspring.
        """

        return offspring[: self.population_size]

    def best_solution(self, population):
        """
        Return the individual with the highest fitness.
        """

        if self.fitness_values is None:
            raise RuntimeError(
                "best_solution() was called before any generation was "
                "evaluated. Call evaluate() (directly or via run()) at "
                "least once first."
            )

        best_idx = self.fitness_values.index(max(self.fitness_values))

        return population[best_idx]