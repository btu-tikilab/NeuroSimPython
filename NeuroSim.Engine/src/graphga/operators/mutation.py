"""
Mutation Operators

Introduce random variations into graph genomes.
"""

from graphga.utils.graph import Graph


class EdgeMutation:
    """Randomly flip graph edges."""

    def __init__(
        self,
        mutation_rate: float = None,
        node_count: int = None,
    ):

        if mutation_rate is not None:
            #no negative mutation rate and not greater than 1
            if not 0 <= mutation_rate <= 1:
                raise ValueError(
                    f"mutation_rate must be between 0 and 1, got {mutation_rate}"
                )

            self.mutation_rate = mutation_rate

        elif node_count is not None:

            if node_count <= 0:
                raise ValueError("node_count must be positive")

            self.mutation_rate = 1.0 / node_count

        else:
            raise ValueError(
                "Provide either mutation_rate or node_count"
            )

    def mutate(
        self,
        graph: Graph,
        rng,
    ) -> Graph:

        mutated = graph.copy()

        size = mutated.node_count

        if mutated.directed:

            for i in range(size):
                for j in range(size):

                    if i == j and not mutated.allow_self_loop:
                        continue

                    if rng.random() < self.mutation_rate:
                        mutated.adjacency_matrix[i][j] ^= 1

        else:

            for i in range(size):
                for j in range(i + 1, size):

                    if rng.random() < self.mutation_rate:

                        value = mutated.adjacency_matrix[i][j] ^ 1

                        mutated.adjacency_matrix[i][j] = value
                        mutated.adjacency_matrix[j][i] = value

            if mutated.allow_self_loop:

                for i in range(size):
                    if rng.random() < self.mutation_rate:
                        mutated.adjacency_matrix[i][i] ^= 1
                # Mutate node attributes
        for i in range(size):

            if rng.random() < self.mutation_rate:
                mutated.node_attributes[i] ^= 1

        return mutated