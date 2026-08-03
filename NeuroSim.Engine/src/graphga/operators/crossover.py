"""
Graph Crossover Operators

Combine two parent graphs to create offspring.
Mirrors bitga/operators/crossover.py while operating on Graph genomes.
"""

from typing import Tuple

from graphga.utils.graph import Graph


class UniformGraphCrossover:
    """Uniform crossover for Graph genomes."""

    def __init__(self, crossover_probability: float = 0.5):
        """
        Initialize graph crossover.

        Args:
            crossover_probability:
                Probability that an edge is inherited
                from parent1.
        """
        if not 0 <= crossover_probability <= 1:
            raise ValueError(
                f"crossover_probability must be between 0 and 1, got {crossover_probability}"
            )

        self.crossover_probability = crossover_probability

    def crossover(
        self,
        parent1: Graph,
        parent2: Graph,
        rng,
    ) -> Tuple[Graph, Graph]:
        """
        Create two offspring using uniform crossover.

        Args:
            parent1: First parent graph.
            parent2: Second parent graph.
            rng: Seeded random number generator.

        Returns:
            Two offspring graphs.
        """

        if parent1.node_count != parent2.node_count:
            raise ValueError(
                "Parent graphs must have the same number of nodes."
            )

        size = parent1.node_count

        child1 = parent1.copy()
        child2 = parent2.copy()

        for i in range(size):
            for j in range(size):

                # Skip illegal self-loops
                if (
                    i == j
                    and not parent1.allow_self_loop
                ):
                    continue

                if rng.random() < self.crossover_probability:

                    child1.adjacency_matrix[i][j] = (
                        parent1.adjacency_matrix[i][j]
                    )

                    child2.adjacency_matrix[i][j] = (
                        parent2.adjacency_matrix[i][j]
                    )

                else:

                    child1.adjacency_matrix[i][j] = (
                        parent2.adjacency_matrix[i][j]
                    )

                    child2.adjacency_matrix[i][j] = (
                        parent1.adjacency_matrix[i][j]
                    )
                # Uniform crossover for node attributes
        for i in range(size):

            if rng.random() < self.crossover_probability:

                child1.node_attributes[i] = (
                    parent1.node_attributes[i]
                )

                child2.node_attributes[i] = (
                    parent2.node_attributes[i]
                )

            else:

                child1.node_attributes[i] = (
                    parent2.node_attributes[i]
                )

                child2.node_attributes[i] = (
                    parent1.node_attributes[i]
                )

        # Preserve symmetry for undirected graphs
        if not parent1.directed:
            for i in range(size):
                for j in range(i + 1, size):
                    child1.adjacency_matrix[j][i] = child1.adjacency_matrix[i][j]
                    child2.adjacency_matrix[j][i] = child2.adjacency_matrix[i][j]

        return child1, child2