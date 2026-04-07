# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/neurosim_engine/binary_ga.py
"""Generic bitstring GA on top of `BaseAlgorithm` (tournament, 1-point crossover, bit-flip)."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple

from neurosim_engine.core.base_algorithm import BaseAlgorithm

Genome = Tuple[int, ...]


@dataclass
class BitIndividual:
    genome: Genome
    fitness: float = 0.0


class BitstringGA(BaseAlgorithm):
    """
    Parameterized by `fitness_fn(genome) -> float` (higher is better).

    Optional `should_stop()` runs after each generation's evaluations (same timing as
    `BaseAlgorithm._should_stop`).
    """

    def __init__(
        self,
        *,
        genome_bits: int,
        fitness_fn: Callable[[Genome], float],
        population_size: int,
        max_generations: int,
        rng: random.Random,
        tournament_size: int = 3,
        mutation_prob: float | None = None,
        crossover_prob: float = 0.9,
        elitism: int = 2,
        after_evaluate: Callable[[List[BitIndividual]], None] | None = None,
        should_stop: Callable[[], bool] | None = None,
    ) -> None:
        super().__init__(population_size=population_size, max_generations=max_generations, rng=rng)
        if genome_bits < 1:
            raise ValueError("genome_bits must be >= 1")
        self.genome_bits = genome_bits
        self._fitness_fn = fitness_fn
        self.tournament_size = tournament_size
        self.mutation_prob = (
            mutation_prob if mutation_prob is not None else 1.0 / max(1, genome_bits)
        )
        self.crossover_prob = crossover_prob
        self.elitism = max(0, elitism)
        self._after_evaluate = after_evaluate
        self._should_stop_extra = should_stop

    def _new_random_genome(self) -> Genome:
        return tuple(1 if self._rng.random() < 0.5 else 0 for _ in range(self.genome_bits))

    def initialize(self) -> List[BitIndividual]:
        return [BitIndividual(genome=self._new_random_genome()) for _ in range(self.population_size)]

    def evaluate(self, population: List[BitIndividual]) -> List[BitIndividual]:
        out = [
            BitIndividual(genome=ind.genome, fitness=float(self._fitness_fn(ind.genome)))
            for ind in population
        ]
        if self._after_evaluate is not None:
            self._after_evaluate(out)
        return out

    def select(self, population: List[BitIndividual]) -> List[BitIndividual]:
        parents: List[BitIndividual] = []
        for _ in range(self.population_size):
            contenders = self._rng.sample(population, k=min(self.tournament_size, len(population)))
            parents.append(max(contenders, key=lambda x: x.fitness))
        return parents

    def breed(self, parents: Sequence[BitIndividual]) -> List[BitIndividual]:
        offspring: List[BitIndividual] = []
        while len(offspring) < self.population_size:
            p1 = parents[self._rng.randrange(len(parents))]
            p2 = parents[self._rng.randrange(len(parents))]
            if self._rng.random() < self.crossover_prob:
                c1, c2 = self._single_point_crossover(p1.genome, p2.genome)
            else:
                c1, c2 = p1.genome, p2.genome
            c1 = self._bit_flip_mutation(c1)
            c2 = self._bit_flip_mutation(c2)
            offspring.append(BitIndividual(genome=c1, fitness=0.0))
            if len(offspring) < self.population_size:
                offspring.append(BitIndividual(genome=c2, fitness=0.0))
        return offspring

    def _single_point_crossover(self, a: Genome, b: Genome) -> Tuple[Genome, Genome]:
        if self.genome_bits <= 1:
            return a, b
        cut = self._rng.randrange(1, self.genome_bits)
        return a[:cut] + b[cut:], b[:cut] + a[cut:]

    def _bit_flip_mutation(self, genome: Genome) -> Genome:
        g = list(genome)
        for i in range(len(g)):
            if self._rng.random() < self.mutation_prob:
                g[i] = 1 - g[i]
        return tuple(g)

    def replace(
        self, population: List[BitIndividual], offspring: List[BitIndividual]
    ) -> List[BitIndividual]:
        combined = population + offspring
        combined_sorted = sorted(combined, key=lambda x: x.fitness, reverse=True)
        return combined_sorted[: self.population_size]

    def best_solution(self, population: List[BitIndividual]) -> BitIndividual:
        return max(population, key=lambda x: x.fitness)

    def _should_stop(self) -> bool:
        if self._should_stop_extra is not None and self._should_stop_extra():
            return True
        return False
