# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/graphga/graph_ga.py
"""
Graph Genetic Algorithm

Implements the Graph Genetic Algorithm using the BaseAlgorithm lifecycle.
"""

from __future__ import annotations

import random
from typing import Callable, List, Sequence

from core.base_algorithm import BaseAlgorithm

from graphga.utils.graph import Graph, GraphIndividual
from graphga.operators.encoding import GraphEncoding
from graphga.operators.selection import TournamentSelection
from graphga.operators.crossover import UniformGraphCrossover
from graphga.operators.mutation import EdgeFlipMutation


class GraphGA(BaseAlgorithm):
    """
    Graph-based Genetic Algorithm.

    Evolves graph genomes using:
    - Tournament Selection
    - Uniform Graph Crossover
    - Edge Flip Mutation
    """

    def __init__(
        self,
        *,
        node_count: int,
        fitness_fn: Callable[[Graph], float],
        population_size: int,
        max_generations: int,
        rng: random.Random,
        directed: bool = False,
        allow_self_loop: bool = False,
        tournament_size: int = 3,
        crossover_rate: float = 0.8,
        mutation_rate: float | None = None,
        elitism:int=2,
    ) -> None:

        super().__init__(
            population_size=population_size,
            max_generations=max_generations,
            rng=rng,
        )

        self.node_count = node_count
        self.fitness_fn = fitness_fn
        self.elitism = max(0, elitism)

        self.encoding = GraphEncoding(
            node_count=node_count,
            directed=directed,
            allow_self_loop=allow_self_loop,
        )

        self.selection = TournamentSelection(
            tournament_size=tournament_size
        )

        self.crossover = UniformGraphCrossover(
            crossover_rate
        )

        self.mutation = EdgeFlipMutation(
            mutation_rate, node_count
        )
    def initialize(self) -> List[GraphIndividual]:
        """
        Create the initial population of random graph individuals.
        """

        population = []

        for _ in range(self.population_size):

            graph = self.encoding.generate_random(self._rng)

            population.append(
                GraphIndividual(
                    graph=graph,
                    fitness=0.0,
                )
            )

        return population
    def evaluate(
        self,
        population: List[GraphIndividual],
    ) -> List[GraphIndividual]:
        """
        Evaluate the fitness of every individual.
        """

        evaluated_population = []

        for individual in population:

            fitness = float(
                self.fitness_fn(individual.graph)
            )

            evaluated_population.append(
                GraphIndividual(
                    graph=individual.graph,
                    fitness=fitness,
                )
        )

        return evaluated_population
    def select(
        self,
        population: List[GraphIndividual],
    ) -> List[GraphIndividual]:
        """
        Select parents using Tournament Selection.
        """

        fitness_values = [
            individual.fitness
            for individual in population
        ]

        return self.selection.select(
            population=population,
            fitness_values=fitness_values,
            num_parents=self.population_size,
            rng=self._rng,
        )
    def breed(
        self,
        parents: List[GraphIndividual],
    ) -> List[GraphIndividual]:
        """
        Generate offspring using crossover and mutation.
        """

        offspring = []

        while len(offspring) < self.population_size:

            parent1 = parents[
                self._rng.randrange(len(parents))
            ]

            parent2 = parents[
                self._rng.randrange(len(parents))
            ]

            child1, child2 = self.crossover.crossover(
                parent1.graph,
                parent2.graph,
                self._rng,
            )

            child1 = self.mutation.mutate(
                child1,
                self._rng,
            )

            child2 = self.mutation.mutate(
                child2,
                self._rng,
            )

            offspring.append(
                GraphIndividual(
                    graph=child1,
                    fitness=0.0,
                )
            )
            if len(offspring) < self.population_size:

                offspring.append(
                    GraphIndividual(
                        graph=child2,
                        fitness=0.0,
                    )
                )
            

        return offspring
    def replace(
        self,
        population: List[GraphIndividual],
        offspring: List[GraphIndividual],
        ) -> List[GraphIndividual]:
        """
        Replace the current population using elitism.

        The best `self.elitism` individuals from the current
        population are preserved directly. The remaining slots
        are filled with evaluated offspring.
        """

        population.sort(
            key=lambda individual: individual.fitness,
            reverse=True,
        )

        elite_count = min(
            self.elitism,
            self.population_size,
        )

        elites = population[:elite_count]

        remaining = self.population_size - elite_count

        return elites + offspring[:remaining]
    
    def best_solution(
        self,
        population: List[GraphIndividual],
    ) -> GraphIndividual:
        """
        Return the individual with the highest fitness.
        """

        return max(
            population,
            key=lambda individual: individual.fitness,
        )