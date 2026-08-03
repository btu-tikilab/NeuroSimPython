"""
Graph Encoding/Decoding

Converts between problem representations and Graph genomes.
Mirrors bitga/operators/encoding.py.
"""

from graphga.utils.graph import Graph, create_random_graph


class GraphEncoding:
    """Convert between problem data and Graph genomes."""

    def __init__(
        self,
        node_count: int,
        directed: bool = False,
        allow_self_loop: bool = False,
    ):
        """
        Initialize graph encoding.

        Args:
            node_count: Number of nodes in the graph.
            directed: Whether graph is directed.
            allow_self_loop: Whether self-loops are allowed.
        """
        if node_count <= 0:
            raise ValueError("node_count must be positive")

        self.node_count = node_count
        self.directed = directed
        self.allow_self_loop = allow_self_loop

    def encode(self, solution: Graph) -> Graph:
        """
        Convert a problem solution to a Graph genome.

        For simple graph problems, this mainly validates the graph and
        returns a defensive copy.

        Args:
            solution: Graph instance.

        Returns:
            Graph genome.
        """
        if not isinstance(solution, Graph):
            raise ValueError("Solution must be a Graph")

        if solution.node_count != self.node_count:
            raise ValueError(
                f"Graph has {solution.node_count} nodes, "
                f"expected {self.node_count}"
            )

        if len(solution.node_attributes) != self.node_count:
            raise ValueError(
                f"Expected {self.node_count} node attributes, "
                f"got {len(solution.node_attributes)}"
        )

        for value in solution.node_attributes:
            if value not in (0, 1):
                raise ValueError("Node attributes must be 0 or 1")

        return solution.copy()

    def decode(self, graph: Graph) -> Graph:
        """
        Convert Graph genome back to problem representation.

        For simple problems this is identical to encode().
        """
        return self.encode(graph)

    def generate_random(self, rng) -> Graph:
        """
        Generate a random Graph genome.

        Args:
            rng: Seeded random number generator.

        Returns:
            Random Graph.
        """
        return create_random_graph(
            node_count=self.node_count,
            directed=self.directed,
            allow_self_loop=self.allow_self_loop,
            rng=rng,
        )