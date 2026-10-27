# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/graphga/engine.py
"""
Graph Genetic Algorithm Engine.

Runs GraphGA for the Graph OneMax problem.
"""

from __future__ import annotations

import random

from graphga.graph_ga import GraphGA
from graph_onemax import GraphOneMaxProblem


class GraphGAEngine:
    """
    Engine for running the Graph Genetic Algorithm.
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = random.Random(seed)
        self.problem = GraphOneMaxProblem()

    def run(
        self,
        node_count: int = 20,
        population_size: int = 100,
        generations: int = 100,
        directed: bool = False,
        allow_self_loop: bool = False,
    ):
        """
        Execute GraphGA and return the best individual.
        """

        ga = GraphGA(
            node_count=node_count,
            fitness_fn=self.problem.fitness,
            population_size=population_size,
            max_generations=generations,
            rng=self.rng,
            directed=directed,
            allow_self_loop=allow_self_loop,
        )

        return ga.run()