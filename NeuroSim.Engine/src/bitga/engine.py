# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/engine.py
"""
Main BitGA Engine
Implements the BaseAlgorithm lifecycle
"""

import random
import time
from dataclasses import dataclass
from typing import List

from core.base_algorithm import BaseAlgorithm

from .operators import (
    BitStringEncoding,
    TournamentSelection,
    UniformCrossover,
    BitFlipMutation,
)


@dataclass
class GenerationStats:
    generation: int
    best_fitness: float
    avg_fitness: float
    worst_fitness: float
    best_genome: List[int]


@dataclass
class RunResult:
    problem_name: str
    run_id: str
    best_fitness: float
    best_solution: List[int]
    generations_to_convergence: int
    total_generations: int
    convergence_history: List[GenerationStats]
    execution_time_seconds: float


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
        crossover_rate=0.8,
        seed=42,
        run_id="run_001",
    ):

        self.problem = problem
        self.run_id = run_id

        self.bitstring_length = bitstring_length

        self._rng = random.Random(seed)

        super().__init__(
            population_size=population_size,
            max_generations=generations,
            rng=self._rng,
        )

        # Operators
        self.encoding = BitStringEncoding(bitstring_length)
        self.selection = TournamentSelection(tournament_size)
        self.crossover = UniformCrossover(crossover_rate)
        self.mutation = BitFlipMutation(mutation_rate=mutation_rate, length=bitstring_length,
        )

        # Runtime state
        self.population = None
        self.fitness_values = None

        self.best_solution_ever = None
        self.best_fitness_ever = float("-inf")
        self.generations_to_convergence = 0
        self.convergence_history = []

        self.current_generation = 0
        self.start_time = None

    # -----------------------------------------------------
    # BaseAlgorithm Hooks
    # -----------------------------------------------------

    def initialize(self):

        self.start_time = time.time()

        population = [
            self.encoding.generate_random(self._rng)
            for _ in range(self.population_size)
        ]

        return population

    def evaluate(self, population):

        self.fitness_values = [
            self.problem.fitness(ind)
            for ind in population
        ]

        best_idx = self.fitness_values.index(max(self.fitness_values))

        best = self.fitness_values[best_idx]
        avg = sum(self.fitness_values) / len(self.fitness_values)
        worst = min(self.fitness_values)

        if best > self.best_fitness_ever:
            self.best_fitness_ever = best
            self.best_solution_ever = population[best_idx].copy()
            self.generations_to_convergence = len(self.convergence_history)

        self.convergence_history.append(
            GenerationStats(
                generation=len(self.convergence_history),
                best_fitness=best,
                avg_fitness=avg,
                worst_fitness=worst,
                best_genome=population[best_idx].copy(),
            )
        )

        return population

    def select(self, population):

        return self.selection.select(
            population,
            self.fitness_values,
            self.population_size,
            self._rng,
        )

    def breed(self, parents):

        offspring = []

        for i in range(0, len(parents), 2):

            if i + 1 < len(parents):

                child1, child2 = self.crossover.crossover(
                    parents[i],
                    parents[i + 1],
                    self._rng,
                )

                offspring.append(
                    self.mutation.mutate(child1, self._rng)
                )

                offspring.append(
                    self.mutation.mutate(child2, self._rng)
                )

            else:

                offspring.append(
                    self.mutation.mutate(
                        parents[i],
                        self._rng,
                    )
                )

        return offspring

    def replace(self, population, offspring):

        self.current_generation += 1

        return offspring[: self.population_size]

    def best_solution(self, population):

        execution_time = time.time() - self.start_time

        return RunResult(
            problem_name=type(self.problem).__name__,
            run_id=self.run_id,
            best_fitness=self.best_fitness_ever,
            best_solution=self.best_solution_ever,
            generations_to_convergence=self.generations_to_convergence,
            total_generations=self.max_generations,
            convergence_history=self.convergence_history,
            execution_time_seconds=execution_time,
        )