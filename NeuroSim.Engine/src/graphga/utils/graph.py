from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List


@dataclass
class Graph:
    """
    Represents a graph using an adjacency matrix.
    Each node also has a binary activation attribute.
    """

    adjacency_matrix: List[List[int]]
    node_attributes: List[int]
    directed: bool
    allow_self_loop: bool

    @property
    def node_count(self) -> int:
        """
        Number of nodes in the graph.
        """
        return len(self.adjacency_matrix)

    def copy(self) -> "Graph":
        """
        Create a deep copy of the graph.
        """
        return Graph(
            adjacency_matrix=[row[:] for row in self.adjacency_matrix],
            node_attributes=self.node_attributes[:],
            directed=self.directed,
            allow_self_loop=self.allow_self_loop,
        )


@dataclass
class GraphIndividual:
    """
    Individual used by the Genetic Algorithm.
    """

    graph: Graph
    fitness: float = 0.0


def create_random_graph(
    node_count: int,
    directed: bool,
    allow_self_loop: bool,
    rng: random.Random,
) -> Graph:
    """
    Create a random graph using an adjacency matrix.
    """

    matrix: List[List[int]] = [
        [0 for _ in range(node_count)]
        for _ in range(node_count)
    ]

    for i in range(node_count):
        for j in range(node_count):

            # Skip diagonal if self loops are not allowed
            if i == j and not allow_self_loop:
                continue

            # Avoid duplicate edges for undirected graphs
            if not directed and j < i:
                continue

            edge = rng.randint(0, 1)

            matrix[i][j] = edge

            # Mirror edge for undirected graphs
            if not directed:
                matrix[j][i] = edge
    node_attributes = [
        rng.randint(0, 1)
        for _ in range(node_count)
    ]            
    return Graph(
        adjacency_matrix=matrix,
        node_attributes=node_attributes,
        directed=directed,
        allow_self_loop=allow_self_loop,
    )


def count_edges(graph: Graph) -> int:
    """
    Count the number of edges in the graph.
    """

    matrix = graph.adjacency_matrix
    node_count = graph.node_count

    edge_count = 0

    if graph.directed:

        for i in range(node_count):
            for j in range(node_count):
                if matrix[i][j] == 1:
                    edge_count += 1

    else:

        for i in range(node_count):
            for j in range(i, node_count):
                if matrix[i][j] == 1:
                    edge_count += 1

    return edge_count


def calculate_density(graph: Graph) -> float:
    """
    Calculate graph density.
    """

    node_count = graph.node_count

    if node_count <= 1:
        return 0.0

    edge_count = count_edges(graph)

    if graph.directed:

        max_edges = (
            node_count * node_count
            if graph.allow_self_loop
            else node_count * (node_count - 1)
        )

    else:

        max_edges = (
            node_count * (node_count + 1) / 2
            if graph.allow_self_loop
            else node_count * (node_count - 1) / 2
        )

    return edge_count / max_edges