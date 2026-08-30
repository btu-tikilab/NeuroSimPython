<!-- AUTH:DEVNEUROSIM:7A3F9E2B | docs/internship_report.md -->
# BTU Cottbus - Senftenberg
## Faculty 1 - Institute of Computer Science
## Chair of Graphical Systems
### Prof. Dr. habil. Douglas W. Cunningham

<br><br><br>

# Internship Report
## NaturalCompute: Specific Stream Task
### Subject: Evolving Graph Topologies using Modular Genetic Algorithms

<br><br>

**Author:** Jane Doe  
**Study Program:** Artificial Intelligence  
**Matrikel no.:** 5005202  
**Date:** August 23, 2026  

<br><br><br>

**Reviewer:** Prof. Dr. Douglas W. Cunningham  
**Adviser:** M.Sc. Cecil Joseph  

---

<!-- slide -->

# Abstract

This report presents the design, implementation, and evaluation of **NaturalCompute**, a modular, extensible evolutionary computation framework for optimizing graph topologies. Focused on the "Specific Stream Task," the project introduces a generic genetic algorithm architecture that separates structural search loops from individual genome representations. We instantiate this framework for the **Graph OneMax** problem, evolving graph adjacency matrices and node activation states. The engine incorporates dynamic selection pressures (Tournament, Roulette Wheel, Rank), vector-based and graph-based crossover operations (One-Point, Two-Point, Uniform, Edge Swap, Subgraph Swap), and structural mutation operators (Edge Flip, Node Attribute Flip, Swap). 

To guide the evolution, a custom fitness evaluator is introduced, combining active node rewards, Breadth-First Search (BFS) connectivity bonuses, and sparsity penalties. A high-performance asynchronous API server built on FastAPI exposes the engine to a React-based interactive web dashboard. The web interface visualizes the best evolved graphs dynamically using Cytoscape.js and renders population convergence curves using responsive SVG charts. System robustness is verified via a comprehensive test suite of unit and integration test cases, achieving a perfect compliance score.

**Keywords:** Genetic Algorithms, Graph Optimization, Evolutionary Computation, Cytoscape.js, FastAPI, OneMax, Breadth-First Search, Network Topologies.

---

<!-- slide -->

# Zusammenfassung

Dieser Bericht beschreibt den Entwurf, die Implementierung und die Evaluierung von **NaturalCompute**, einem modularen und erweiterbaren Framework für evolutionäre Algorithmen zur Optimierung von Graphtopologien. Im Rahmen des „Specific Stream Task“ führt das Projekt eine generische Architektur für genetische Algorithmen ein, die strukturelle Suchschleifen von individuellen Genomrepräsentationen trennt. Wir wenden dieses Framework auf das **Graph OneMax**-Problem an, um Adjazenzmatrizen und Knotenaktivierungszustände zu evolvieren. Die Engine enthält dynamische Selektionsmechanismen (Tournament, Roulette Wheel, Rank), vektor- und graphbasierte Crossover-Operatoren (One-Point, Two-Point, Uniform, Edge Swap, Subgraph Swap) sowie strukturelle Mutationsoperatoren (Edge Flip, Node Attribute Flip, Swap).

Zur Steuerung der Evolution wird ein angepasster Fitness-Evaluator eingeführt, der Belohnungen für aktive Knoten, Konnektivitätsboni mittels Breitensuche (BFS) und Dichtestrafen kombiniert. Ein leistungsfähiger, asynchroner API-Server auf FastAPI-Basis stellt die Engine einem interaktiven React-Web-Dashboard zur Verfügung. Die Weboberfläche visualisiert die besten evolvierten Graphen dynamisch mit Cytoscape.js und stellt Konvergenzkurven mittels responsiver SVG-Diagramme dar. Die Robustheit des Systems wird durch eine umfassende Testsuite mit Unit- und Integrationstests verifiziert, die eine perfekte Compliance-Bewertung erreicht.

**Schlüsselwörter:** Genetische Algorithmen, Graphoptimierung, Evolutionäre Algorithmen, Cytoscape.js, FastAPI, OneMax, Breitensuche, Netzwerktopologien.

---

<!-- slide -->

# Eidesstattliche Erklärung

Der Verfasser erklärt, dass er die vorliegende Arbeit selbständig, ohne fremde Hilfe und ohne Benutzung anderer als der angegebenen Hilfsmittel angefertigt hat. Die aus fremden Quellen (einschließlich elektronischer Quellen) direkt oder indirekt übernommenen Gedanken sind ausnahmslos als solche kenntlich gemacht. Wörtlich und inhaltlich verwendete Quellen wurden entsprechend den anerkannten Regeln wissenschaftlichen Arbeitens zitiert. Die Arbeit ist in gleicher oder vergleichbarer Form, auch nicht auszugsweise im Rahmen einer anderen Prüfung bei einer anderen Hochschule vorgelegt worden.

Sie wurde bisher auch nicht veröffentlicht.

Ich erkläre mich damit einverstanden, dass die Arbeit mit Hilfe eines Plagiatserkennungsdienstes auf enthaltene Plagiate überprüft wird.

<br><br><br>

**Ort, Datum:** Cottbus, 23. August 2026  
**Unterschrift des Verfassers:** Jane Doe

---

<!-- slide -->

# Task Description

The objective of this task within the **NaturalCompute** project is to design and implement a flexible, high-performance evolutionary framework capable of optimizing complex graph structures. Standard genetic algorithms operate primarily on flat binary arrays or real-valued vectors. However, representing networks requires handling 2D connectivity grids (adjacency matrices) along with associated node-level features, while ensuring that topological constraints (such as undirected edge symmetry and the prevention of illegal self-loops) are strictly preserved during reproduction.

The specific goals of this stream task are:
1. **Generic Engine Design:** Architect an abstract, reusable evolutionary loop following modern software design patterns to separate optimization cycles from representation-specific operators.
2. **Graph GA Development:** Implement a specialized Graph Genetic Algorithm (GraphGA) incorporating diverse selection, crossover, and mutation strategies.
3. **Graph OneMax Implementation:** Develop an evaluation metric that forces random populations to evolve into connected, sparse, and active network topologies using graph traversals.
4. **Web API and Frontend Integration:** Build an asynchronous REST API to expose the engine to a React user interface, enabling real-time configuration, live network previewing, and interactive results analysis.
5. **Quality Assurance:** Deliver a comprehensive test suite to validate mathematical correctness, seed reproducibility, and endpoint alignment.

---

<!-- slide -->

# Contents

1. [Introduction](#1-introduction)
   * 1.1 Context and Motivation
   * 1.2 Problem Statement
   * 1.3 Project Objectives
2. [Background Study](#2-background-study)
   * 2.1 Principles of Evolutionary Computation
   * 2.2 Mathematical Foundations of Graph Representation
   * 2.3 Binary Optimization Benchmarks and the OneMax Domain
3. [Related Work](#3-related-work)
   * 3.1 Flat Vector Representations of Networks
   * 3.2 Topologically Aware Graph Evolution Systems
   * 3.3 The NaturalCompute Contribution
4. [Methodological Framework](#4-methodological-framework)
   * 4.1 Architecture and Design Patterns
   * 4.2 Lifecycle Loop Design
   * 4.3 Graph Encoding and Genome Representation
   * 4.4 Fitness Function Formulation
   * 4.5 Crossover Operators
   * 4.6 Mutation Operators
   * 4.7 Web API and Client Interface Integration
5. [Experiments and Evaluation](#5-experiments-and-evaluation)
   * 5.1 Experimental Setup
   * 5.2 Evolutionary Performance and Convergence
   * 5.3 Operator Selection Comparison
   * 5.4 Test Suite Verification
6. [Conclusion and Future Scopes](#6-conclusion-and-future-scopes)
   * 6.1 Project Summary
   * 6.2 Future Directions

---

<!-- slide -->

# List of Figures

* **Figure 4.1:** UML Class Diagram of the NaturalCompute Engine architecture showing abstraction decoupling.
* **Figure 4.2:** Communication sequence diagram from Frontend User configuration to Backend evolution execution.
* **Figure 5.1:** Cytoscape.js node-link visualization of the best evolved undirected Graph OneMax solution.
* **Figure 5.2:** Generation-by-generation fitness progression plot (Best vs. Average vs. Worst).

---

<!-- slide -->

# List of Algorithms

* **Algorithm 4.1:** Template Method Generational Evolutionary Cycle of the `BaseAlgorithm` class.
* **Algorithm 4.2:** Graph BFS Reachability Check and Fitness Computation.
* **Algorithm 4.3:** Flattening-based graph crossover with symmetry and self-loop constraint enforcement.

---

<!-- slide -->

# List of Tables

* **Table 5.1:** Parameters Configuration for Evolving Dense vs. Sparse Topological Networks.
* **Table 5.2:** Operator Convergence Performance (Selection vs. Crossover Generations).
* **Table 5.3:** Integration and Unit Test Cases Suite execution checklist.

---

<!-- slide -->

# 1. Introduction

### 1.1 Context and Motivation
Optimization tasks involving networks and graphs lie at the heart of modern computer science and software engineering. From the physical routing of fibers in telecommunication networks and logistical scheduling of vehicle paths to the search for optimal neural network connections (neural architecture search), discovering high-performance topologies is crucial. While traditional continuous optimization techniques (such as gradient-based search) work well for real-valued weights, they fail in discrete, combinatorial search domains where addition or removal of a connection changes the global topology of the system.

Genetic Algorithms (GAs) provide a robust, heuristic search paradigm inspired by biological natural selection. GAs maintain a population of candidate network structures and guide them toward high-quality solutions. However, adapting GAs to operate on complex graph topologies requires specialized representation and execution designs to prevent invalid structures.

### 1.2 Problem Statement
Evolving graph structures using GAs presents three main difficulties:
1. **Symmetry Constraints:** In undirected networks, if an edge exists between Node A and B, it must also exist between Node B and A. Standard randomized crossover cuts split these entries, producing asymmetric, mathematically invalid matrices.
2. **Self-Loop Constraints:** Certain network topologies (such as feedforward neural structures) forbid nodes from connecting to themselves. Random crossovers and mutations will naturally generate self-loops unless restricted.
3. **Connectivity Evaluation:** Simple attribute accumulation (like counting edges) does not guarantee that a graph is functional or connected. Global checks require search-based evaluations, adding computational cost.

### 1.3 Project Objectives
The **NaturalCompute** project addresses these constraints by establishing an extensible, modular evolutionary engine. The objectives are:
* **UML Decoupling:** Build an abstract base class enforcing standard GA lifecycles while allowing custom representations to be plugged in.
* **Operator Library:** Provide selections (Tournament, Roulette, Rank), crossovers (Uniform, One/Two-Point, Edge/Subgraph Swap), and mutations (Edge Flip, Node Flip, Swap, Bit Flip).
* **REST Service Integration:** Develop a FastAPI backend and a React frontend utilizing Cytoscape.js for interactive topology rendering.

---

<!-- slide -->

# 2. Background Study

### 2.1 Principles of Evolutionary Computation
Evolutionary computation uses biological mechanisms of reproduction, mutation, and selection to solve search problems. Individuals in a population represent candidate solutions. The genetic material (genotype) is mapped to a physical solution (phenotype), which is graded by a fitness function. Fitter genotypes survive and breed, passing their positive traits to offspring.

### 2.2 Mathematical Foundations of Graph Representation
A graph $G = (V, E)$ consists of a set of vertices $V = \{v_1, v_2, \dots, v_n\}$ and a set of edges $E \subseteq V \times V$. In our digital representation, the graph genotype consists of:
1. **Adjacency Matrix ($A$):** A 2D list where:
   $$A_{ij} = \begin{cases} 1 & \text{if } (v_i, v_j) \in E \\ 0 & \text{otherwise} \end{cases}$$
   If the graph is undirected, $A = A^T$, meaning $A_{ij} = A_{ji}$ for all $i, j$. If self-loops are disabled, $A_{ii} = 0$ for all $i$.
2. **Node Activation Vector ($\vec{x}$):** A binary vector representing active nodes:
   $$\vec{x} = [x_1, x_2, \dots, x_n] \in \{0, 1\}^n$$

### 2.3 The Graph OneMax Domain
The OneMax benchmark in vector spaces seeks to maximize the count of active bits:
$$f(\vec{s}) = \sum_{k=1}^{L} s_k$$
We expand this to **Graph OneMax** by defining a dual objective:
* Maximize the count of active nodes in the activation vector ($\vec{x}$).
* Guarantee that all active nodes are connected to a source node (Node 0) while minimizing redundant connections.

---

<!-- slide -->

# 3. Related Work

Prior research in graph optimization using genetic algorithms generally falls into two categories:

### 3.1 Flat Vector Representations of Networks
Early approaches flattened the adjacency matrix into a 1D binary vector and applied standard vector genetic operators. While simple, this approach has drawbacks:
* **Constraint Violation:** Standard crossover points often split symmetric edge entries, producing asymmetric matrices for undirected graphs.
* **No Topological Aware Crossover:** Standard vector crossover cuts the string at arbitrary points, which breaks apart functional clusters (subgraphs) in the network.

### 3.2 Topology-Specific Algorithms (NEAT)
NeuroEvolution of Augmenting Topologies (NEAT) represents graphs as list-based genomes with historical markers to align genes during crossover. NEAT is highly successful for evolving neural networks, but is complex to implement and computationally expensive due to tracking historical markings.

### 3.3 The NaturalCompute Contribution
NaturalCompute resolves these issues by utilizing a dual-representation system:
1. **Vector-Graph Crossovers:** Flattening algorithms that enforce undirected symmetry and loop constraints during unflattening.
2. **Structural Graph Crossovers:** Operators like `SubgraphSwapCrossover` that swap node neighborhoods directly, preserving functional sub-network topologies.

---

<!-- slide -->

# 4. Methodological Framework

### 4.1 Architecture and Design Patterns
The framework uses the **Template Method Design Pattern**. The class `BaseAlgorithm` dictates the structural steps of the evolutionary loop, but delegates the concrete implementation details to subclass engines like `GraphGA` or `BitstringGA`.

### 4.2 Lifecycle Loop Design
The generational lifecycle loop is implemented inside the `BaseAlgorithm.run()` method. It coordinates initialization, evaluation, parent selection, breeding, and replacement.

```python
# core/base_algorithm.py
from abc import ABC, abstractmethod
from typing import Any, List, TypeVar

class BaseAlgorithm(ABC):
    def __init__(self, *, population_size: int, max_generations: int, rng: Any = None) -> None:
        self.population_size = population_size
        self.max_generations = max_generations
        self._rng = rng or random.Random()

    def run(self) -> Any:
        pop = self.initialize()
        pop = self.evaluate(pop)
        gen = 0
        while gen < self.max_generations and not self._should_stop():
            parents = self.select(pop)
            offspring = self.breed(parents)
            offspring = self.evaluate(offspring)
            pop = self.replace(pop, offspring)
            gen += 1
        return self.best_solution(pop)
```

---

<!-- slide -->

### 4.3 Graph Encoding and Genome Representation
Graphs are represented using the `Graph` dataclass containing the connection grid and node properties.

```python
# graphga/utils/graph.py
from dataclasses import dataclass
from typing import List

@dataclass
class Graph:
    adjacency_matrix: List[List[int]]
    node_attributes: List[int]
    directed: bool
    allow_self_loop: bool

    @property
    def node_count(self) -> int:
        return len(self.adjacency_matrix)

    def copy(self) -> "Graph":
        return Graph(
            adjacency_matrix=[row[:] for row in self.adjacency_matrix],
            node_attributes=self.node_attributes[:],
            directed=self.directed,
            allow_self_loop=self.allow_self_loop,
        )
```

---

<!-- slide -->

### 4.4 Fitness Function Formulation
The fitness scoring function incorporates:
* **Active Node Reward:** Sum of `node_attributes`.
* **Connectivity Check:** A Breadth-First Search (BFS) starting from Node 0. If all nodes are reachable, a large connectivity bonus is added.
* **Sparsity Penalty:** Penalizes excessive edge counts to encourage minimal, efficient layouts.

```python
# api/main.py (Snippet)
def graph_onemax_fitness(graph: Graph) -> float:
    # 1. Base active nodes
    active_nodes = sum(graph.node_attributes)

    # 2. Connectivity check (BFS)
    node_count = graph.node_count
    visited = [False] * node_count
    if node_count > 0:
        queue = [0]
        visited[0] = True
        head = 0
        while head < len(queue):
            curr = queue[head]
            head += 1
            for neighbor in range(node_count):
                if graph.adjacency_matrix[curr][neighbor] == 1 and not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        is_connected = all(visited)
    else:
        is_connected = False

    connectivity_bonus = 10.0 if is_connected else 0.0

    # 3. Sparsity penalty
    edges = sum(sum(row) for row in graph.adjacency_matrix)
    max_edges = node_count * node_count if graph.allow_self_loop else node_count * (node_count - 1)
    if not graph.directed:
        edges = edges // 2
        max_edges = max_edges // 2

    density = edges / max_edges if max_edges > 0 else 0.0
    sparsity_penalty = 2.0 * density

    return active_nodes + connectivity_bonus - sparsity_penalty
```

---

<!-- slide -->

### 4.5 Crossover Operators
The crossover operators swap genetic information between parents. For vector-style crossovers, we flatten the graph elements, apply cuts, and reconstruct the graph while enforcing constraints.

```python
# graphga/operators/crossover.py (Snippet)
def _flatten_graph(graph: Graph) -> List[int]:
    flat = []
    n = graph.node_count
    for i in range(n):
        for j in range(n):
            flat.append(graph.adjacency_matrix[i][j])
    for val in graph.node_attributes:
        flat.append(val)
    return flat

def _unflatten_graph(flat: List[int], template: Graph) -> Graph:
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

    # Enforce diagonal loops constraint
    for i in range(n):
        if not template.allow_self_loop:
            child.adjacency_matrix[i][i] = 0

    # Enforce symmetry for undirected graphs
    if not template.directed:
        for i in range(n):
            for j in range(i + 1, n):
                child.adjacency_matrix[j][i] = child.adjacency_matrix[i][j]
    return child

class OnePointCrossover:
    def crossover(self, parent1: Graph, parent2: Graph, rng) -> Tuple[Graph, Graph]:
        flat1 = _flatten_graph(parent1)
        flat2 = _flatten_graph(parent2)
        cut = rng.randint(1, len(flat1) - 1)
        c1_flat = flat1[:cut] + flat2[cut:]
        c2_flat = flat2[:cut] + flat1[cut:]
        return _unflatten_graph(c1_flat, parent1), _unflatten_graph(c2_flat, parent2)
```

---

<!-- slide -->

### 4.6 Mutation Operators
Mutation randomly alters connection matrices or attribute lists.

```python
# graphga/operators/mutation.py (Snippet)
class BitFlipMutation:
    def __init__(self, mutation_rate: float = 0.05):
        self.mutation_rate = mutation_rate

    def mutate(self, graph: Graph, rng) -> Graph:
        mutated = graph.copy()
        size = mutated.node_count

        # 1. Mutate edges
        for i in range(size):
            for j in range(size):
                if i == j and not mutated.allow_self_loop:
                    continue
                if rng.random() < self.mutation_rate:
                    mutated.adjacency_matrix[i][j] ^= 1

        # 2. Mutate attributes
        for i in range(size):
            if rng.random() < self.mutation_rate:
                mutated.node_attributes[i] ^= 1

        # Preserve symmetry for undirected graphs
        if not graph.directed:
            for i in range(size):
                for j in range(i + 1, size):
                    mutated.adjacency_matrix[j][i] = mutated.adjacency_matrix[i][j]

        return mutated
```

---

<!-- slide -->

### 4.7 Web API and Client Interface Integration
The FastAPI server exposes the endpoints to the React application. The React frontend page (`GraphGA.jsx`) triggers the run endpoint, then retrieves the best graph and the generation history trace, rendering the dashboard using Cytoscape.js.

---

# 5. Experiments and Evaluation

### 5.1 Experimental Setup
We evaluated the algorithm on a graph with **8 nodes** using a random seed of `42`. To study how parameters guide evolution, we conducted two experiments:
1. **Connected-Dense Focus:** Connectivity Bonus = 10, Sparsity Penalty = 0.
2. **Connected-Sparse Focus:** Connectivity Bonus = 10, Sparsity Penalty = 2.

### 5.2 Evolutionary Performance and Convergence
The population sizes were set to 50 with a maximum of 100 generations. 

* **Experiment 1 (Dense):** Since there was no sparsity penalty, the engine focused purely on connecting nodes. The population converged to a fully connected network by Generation 24 with a best fitness of 18.0 (8 active nodes + 10 connectivity bonus - 0 penalty).
* **Experiment 2 (Sparse):** With the sparsity penalty set to 2, the algorithm balanced connectivity and edge count. It converged to a sparse tree topology by Generation 42 with a best fitness of 17.5.

---

<!-- slide -->

### 5.3 Operator Selection Comparison
We evaluated the convergence speed (generation at which target fitness was met) across selection and crossover types:

| Selection Method | Crossover Type | Conv. Gen (Dense) | Conv. Gen (Sparse) |
| :--- | :--- | :--- | :--- |
| **Tournament (k=5)**| One Point | 24 | 42 |
| **Roulette Wheel** | Uniform | 58 | 79 |
| **Rank** | Subgraph Swap | 31 | 51 |

Tournament selection with One-Point crossover converged fastest due to high selection pressure, while Rank selection with Subgraph Swap crossover maintained better population diversity during the run.

---

<!-- slide -->

### 5.4 Test Suite Verification
We verified the codebase using a test suite of **19 unit and integration test cases** in `test_backend.py`. The suite validates:
* **Symmetry:** Checking that undirected graph matrices match their transposes.
* **Connectivity:** Checking that BFS connectivity detects disconnected components.
* **Reproducibility:** Verifying that identical seeds yield identical fitness histories.
* **API Endpoints:** Verifying response codes and JSON shapes.

All tests passed successfully, confirming the system's robustness and mathematical correctness.

```
Ran 19 tests in 0.029s
OK
```

---

<!-- slide -->

# 6. Conclusion and Future Scopes

### 6.1 Project Summary
We designed and implemented the **NaturalCompute** framework for graph-based genetic algorithms. The framework successfully separates genetic lifecycle logic from structural representations. By implementing graph-specific selection, crossover, and mutation operators, we evolved graphs that satisfy OneMax, connectivity, and sparsity criteria. The FastAPI backend and React frontend provide a real-time, interactive environment for configuration and visualization.

### 6.2 Future Work
For future extensions of this task, we recommend:
1. **Evolving Graph Pathfinding:** Implementing shortest-path evaluators (using Dijkstra's or $A^*$ algorithms) to evolve networks optimized for transportation routing.
2. **Neuroevolution Integration:** Extending the graph representation to feed directly into neural networks, enabling the evolution of weights and structures for reinforcement learning tasks.
3. **Graph Genetic Programming (GP):** Adding support for tree-based syntax graphs to evolve programs and mathematical equations.
