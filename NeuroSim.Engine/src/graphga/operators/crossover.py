# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/graphga/operators/crossover.py
"""
Graph Crossover Operators

Combine two parent graphs to create offspring.
"""

from typing import Tuple, List
from core.base_crossover import BaseCrossover
from graphga.utils.graph import Graph


# ── Helpers for Flattening/Unflattening Graphs ────────────────────────────────

def _flatten_graph(graph: Graph) -> List[int]:
    """Flatten adjacency matrix and node attributes into a single 1D list."""
    flat = []
    n = graph.node_count
    for i in range(n):
        for j in range(n):
            flat.append(graph.adjacency_matrix[i][j])
    for val in graph.node_attributes:
        flat.append(val)
    return flat


def _unflatten_graph(flat: List[int], template: Graph) -> Graph:
    """Reconstruct a Graph instance from a 1D list, enforcing constraints."""
    n = template.node_count
    child = template.copy()
    idx = 0
    for i in range(n):
        for j in range(n):
            child.adjacency_matrix[i][j] = flat[idx]
            idx += 1
    for i in range(n):
        child.node_attributes[i] = flat[idx]
        idx += 1

    # Enforce self-loop constraints
    for i in range(n):
        if not template.allow_self_loop:
            child.adjacency_matrix[i][i] = 0

    # Enforce undirected symmetry
    if not template.directed:
        for i in range(n):
            for j in range(i + 1, n):
                child.adjacency_matrix[j][i] = child.adjacency_matrix[i][j]

    return child


# ── Crossover Operators ───────────────────────────────────────────────────────

class UniformGraphCrossover(BaseCrossover):
    """Uniform crossover directly on graph matrices and attributes."""

    def __init__(self, crossover_probability: float = 0.5):
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
        if parent1.node_count != parent2.node_count:
            raise ValueError("Parent graphs must have the same number of nodes.")

        size = parent1.node_count
        child1 = parent1.copy()
        child2 = parent2.copy()

        for i in range(size):
            for j in range(size):
                if i == j and not parent1.allow_self_loop:
                    continue

                if rng.random() < self.crossover_probability:
                    child1.adjacency_matrix[i][j] = parent1.adjacency_matrix[i][j]
                    child2.adjacency_matrix[i][j] = parent2.adjacency_matrix[i][j]
                else:
                    child1.adjacency_matrix[i][j] = parent2.adjacency_matrix[i][j]
                    child2.adjacency_matrix[i][j] = parent1.adjacency_matrix[i][j]

        for i in range(size):
            if rng.random() < self.crossover_probability:
                child1.node_attributes[i] = parent1.node_attributes[i]
                child2.node_attributes[i] = parent2.node_attributes[i]
            else:
                child1.node_attributes[i] = parent2.node_attributes[i]
                child2.node_attributes[i] = parent1.node_attributes[i]

        # Preserve symmetry for undirected graphs
        if not parent1.directed:
            for i in range(size):
                for j in range(i + 1, size):
                    child1.adjacency_matrix[j][i] = child1.adjacency_matrix[i][j]
                    child2.adjacency_matrix[j][i] = child2.adjacency_matrix[i][j]

        return child1, child2


class EdgeSwapCrossover(BaseCrossover):
    """Randomly swaps connections (edges) and attributes between parents."""

    def crossover(
        self,
        parent1: Graph,
        parent2: Graph,
        rng,
    ) -> Tuple[Graph, Graph]:
        if parent1.node_count != parent2.node_count:
            raise ValueError("Parent graphs must have the same number of nodes.")

        size = parent1.node_count
        child1 = parent1.copy()
        child2 = parent2.copy()

        for i in range(size):
            for j in range(size):
                if i == j and not parent1.allow_self_loop:
                    continue

                if rng.random() < 0.5:
                    child1.adjacency_matrix[i][j] = parent1.adjacency_matrix[i][j]
                    child2.adjacency_matrix[i][j] = parent2.adjacency_matrix[i][j]
                else:
                    child1.adjacency_matrix[i][j] = parent2.adjacency_matrix[i][j]
                    child2.adjacency_matrix[i][j] = parent1.adjacency_matrix[i][j]

        for i in range(size):
            if rng.random() < 0.5:
                child1.node_attributes[i] = parent1.node_attributes[i]
                child2.node_attributes[i] = parent2.node_attributes[i]
            else:
                child1.node_attributes[i] = parent2.node_attributes[i]
                child2.node_attributes[i] = parent1.node_attributes[i]

        # Preserve symmetry for undirected graphs
        if not parent1.directed:
            for i in range(size):
                for j in range(i + 1, size):
                    child1.adjacency_matrix[j][i] = child1.adjacency_matrix[i][j]
                    child2.adjacency_matrix[j][i] = child2.adjacency_matrix[i][j]

        return child1, child2


class SubgraphSwapCrossover(BaseCrossover):
    """Selects a random subset of nodes and swaps their complete subgraphs."""

    def crossover(
        self,
        parent1: Graph,
        parent2: Graph,
        rng,
    ) -> Tuple[Graph, Graph]:
        if parent1.node_count != parent2.node_count:
            raise ValueError("Parent graphs must have the same number of nodes.")

        size = parent1.node_count
        child1 = parent1.copy()
        child2 = parent2.copy()

        subset_size = max(1, size // 3)
        all_nodes = list(range(size))
        subset = rng.sample(all_nodes, subset_size)

        for node in subset:
            child1.node_attributes[node] = parent2.node_attributes[node]
            child2.node_attributes[node] = parent1.node_attributes[node]

            for neighbor in range(size):
                child1.adjacency_matrix[node][neighbor] = parent2.adjacency_matrix[node][neighbor]
                child2.adjacency_matrix[node][neighbor] = parent1.adjacency_matrix[node][neighbor]

                child1.adjacency_matrix[neighbor][node] = parent2.adjacency_matrix[neighbor][node]
                child2.adjacency_matrix[neighbor][node] = parent1.adjacency_matrix[neighbor][node]

        # Enforce self-loop constraints
        for i in range(size):
            if not parent1.allow_self_loop:
                child1.adjacency_matrix[i][i] = 0
                child2.adjacency_matrix[i][i] = 0

        # Preserve symmetry for undirected graphs
        if not parent1.directed:
            for i in range(size):
                for j in range(i + 1, size):
                    child1.adjacency_matrix[j][i] = child1.adjacency_matrix[i][j]
                    child2.adjacency_matrix[j][i] = child2.adjacency_matrix[i][j]

        return child1, child2


class OnePointCrossover(BaseCrossover):
    """Flattens the graph, performs standard 1-point cut crossover, and reconstructs."""

    def crossover(
        self,
        parent1: Graph,
        parent2: Graph,
        rng,
    ) -> Tuple[Graph, Graph]:
        flat1 = _flatten_graph(parent1)
        flat2 = _flatten_graph(parent2)

        cut = rng.randint(1, len(flat1) - 1)
        c1_flat = flat1[:cut] + flat2[cut:]
        c2_flat = flat2[:cut] + flat1[cut:]

        child1 = _unflatten_graph(c1_flat, parent1)
        child2 = _unflatten_graph(c2_flat, parent2)
        return child1, child2


class TwoPointCrossover(BaseCrossover):
    """Flattens the graph, performs standard 2-point cut crossover, and reconstructs."""

    def crossover(
        self,
        parent1: Graph,
        parent2: Graph,
        rng,
    ) -> Tuple[Graph, Graph]:
        flat1 = _flatten_graph(parent1)
        flat2 = _flatten_graph(parent2)

        length = len(flat1)
        if length < 3:
            return parent1.copy(),parent2.copy()
        p1 = rng.randint(1, length - 2)
        p2 = rng.randint(p1 + 1, length - 1)

        c1_flat = flat1[:p1] + flat2[p1:p2] + flat1[p2:]
        c2_flat = flat2[:p1] + flat1[p1:p2] + flat2[p2:]

        child1 = _unflatten_graph(c1_flat, parent1)
        child2 = _unflatten_graph(c2_flat, parent2)
        return child1, child2


class UniformCrossover(BaseCrossover):
    """Flattens the graph, performs standard uniform crossover, and reconstructs."""

    def crossover(
        self,
        parent1: Graph,
        parent2: Graph,
        rng,
    ) -> Tuple[Graph, Graph]:
        flat1 = _flatten_graph(parent1)
        flat2 = _flatten_graph(parent2)

        c1_flat = []
        c2_flat = []
        for i in range(len(flat1)):
            if rng.random() < 0.5:
                c1_flat.append(flat1[i])
                c2_flat.append(flat2[i])
            else:
                c1_flat.append(flat2[i])
                c2_flat.append(flat1[i])

        child1 = _unflatten_graph(c1_flat, parent1)
        child2 = _unflatten_graph(c2_flat, parent2)
        return child1, child2