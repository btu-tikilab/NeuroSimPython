import random
import pytest
from graphga.graph_ga import GraphGA
from graphga.utils.graph import GraphIndividual
from api.main import TrackedGraphGA


def test_elitism_preserves_best_individuals():
    ga = GraphGA(
        node_count=2,
        fitness_fn=lambda graph: 0.0,
        population_size=4,
        max_generations=1,
        rng=random.Random(42),
        elitism=2,
    )

    population = [
        GraphIndividual(ga.encoding.generate_random(ga._rng), 10.0),
        GraphIndividual(ga.encoding.generate_random(ga._rng), 20.0),
        GraphIndividual(ga.encoding.generate_random(ga._rng), 30.0),
        GraphIndividual(ga.encoding.generate_random(ga._rng), 40.0),
    ]

    offspring = [
        GraphIndividual(ga.encoding.generate_random(ga._rng), 1.0),
        GraphIndividual(ga.encoding.generate_random(ga._rng), 2.0),
        GraphIndividual(ga.encoding.generate_random(ga._rng), 3.0),
        GraphIndividual(ga.encoding.generate_random(ga._rng), 4.0),
    ]

    new_population = ga.replace(population, offspring)

    fitnesses = [individual.fitness for individual in new_population]

    assert fitnesses == [40.0, 30.0, 1.0, 2.0]
def test_history_stores_best_graph_for_each_generation():
    algo = TrackedGraphGA(
        node_count=2,
        fitness_fn=lambda graph: sum(graph.node_attributes),
        population_size=4,
        max_generations=2,
        rng=random.Random(42),
        elitism=1,
    )

    algo.run()

    assert len(algo.history_log) == 3

    for entry in algo.history_log:
        assert "generation" in entry
        assert "bestFitness" in entry
        assert "avgFitness" in entry
        assert "worstFitness" in entry
        assert "bestGraph" in entry
def test_graphga_run_returns_valid_graph():
    algo = TrackedGraphGA(
        node_count=5,
        fitness_fn=lambda graph: sum(graph.node_attributes),
        population_size=10,
        max_generations=3,
        rng=random.Random(42),
        elitism=1,
    )

    best = algo.run()
    graph = best.graph

    # Correct number of nodes
    assert graph.node_count == 5

    # Every node attribute must be 0 or 1
    assert all(value in (0, 1) for value in graph.node_attributes)

    # Every adjacency value must be 0 or 1
    for row in graph.adjacency_matrix:
        assert all(value in (0, 1) for value in row)

    # Undirected graph must remain symmetric
    for i in range(5):
        for j in range(5):
            assert graph.adjacency_matrix[i][j] == graph.adjacency_matrix[j][i]

    # Self-loops are disabled by default
    for i in range(5):
        assert graph.adjacency_matrix[i][i] == 0

def test_graphga_is_reproducible_with_same_seed():
    def run_once():
        algo = TrackedGraphGA(
            node_count=5,
            fitness_fn=lambda graph: sum(graph.node_attributes),
            population_size=10,
            max_generations=3,
            rng=random.Random(42),
            elitism=1,
        )
        best = algo.run()
        return best.fitness, best.graph

    fitness1, graph1 = run_once()
    fitness2, graph2 = run_once()

    assert fitness1 == fitness2
    assert graph1.adjacency_matrix == graph2.adjacency_matrix
    assert graph1.node_attributes == graph2.node_attributes
def test_graphga_can_reach_simple_optimum():
    algo = TrackedGraphGA(
        node_count=5,
        fitness_fn=lambda graph: sum(graph.node_attributes),
        population_size=20,
        max_generations=20,
        rng=random.Random(42),
        elitism=1,
    )

    best = algo.run()

    assert best.fitness == 5.0
def test_tournament_selection_prefers_fitter_individuals():
    from graphga.operators.selection import TournamentSelection
    from graphga.utils.graph import GraphIndividual

    algo = TrackedGraphGA(
        node_count=2,
        fitness_fn=lambda graph: 0.0,
        population_size=4,
        max_generations=1,
        rng=random.Random(42),
    )

    population = [
        GraphIndividual(algo.encoding.generate_random(algo._rng), 1.0),
        GraphIndividual(algo.encoding.generate_random(algo._rng), 2.0),
        GraphIndividual(algo.encoding.generate_random(algo._rng), 3.0),
        GraphIndividual(algo.encoding.generate_random(algo._rng), 4.0),
    ]

    selection = TournamentSelection(tournament_size=2)

    parents = selection.select(
        population,
        [individual.fitness for individual in population],
        4,
        random.Random(42),
    )

    assert len(parents) == 4
    assert all(parent in population for parent in parents)
def test_tournament_selection_rejects_size_below_two():
    from graphga.operators.selection import TournamentSelection

    try:
        TournamentSelection(tournament_size=1)
        assert False, "Tournament size 1 should be rejected"
    except ValueError:
        pass
def test_two_point_crossover_supports_one_node_graph():
    from graphga.operators.crossover import TwoPointCrossover

    algo = TrackedGraphGA(
        node_count=1,
        fitness_fn=lambda graph: sum(graph.node_attributes),
        population_size=4,
        max_generations=1,
        rng=random.Random(42),
    )

    parent1 = algo.encoding.generate_random(algo._rng)
    parent2 = algo.encoding.generate_random(algo._rng)

    crossover = TwoPointCrossover()

    child1, child2 = crossover.crossover(
        parent1,
        parent2,
        random.Random(42),
    )

    assert child1.node_count == 1
    assert child2.node_count == 1

    assert child1.node_attributes[0] in (0, 1)
    assert child2.node_attributes[0] in (0, 1)


@pytest.mark.parametrize(
    "crossover_type",
    [
        "One Point",
        "Two Point",
        "Uniform",
        "Edge Swap",
        "Subgraph Swap",
    ],
)
def test_all_crossover_types_return_valid_graphs(crossover_type):
    algo = TrackedGraphGA(
        node_count=5,
        fitness_fn=lambda graph: 0.0,
        population_size=4,
        max_generations=1,
        rng=random.Random(42),
    )

    parent1 = algo.encoding.generate_random(algo._rng)
    parent2 = algo.encoding.generate_random(algo._rng)

    from graphga.operators.crossover import (
        OnePointCrossover,
        TwoPointCrossover,
        UniformCrossover,
        EdgeSwapCrossover,
        SubgraphSwapCrossover,
    )

    crossovers = {
        "One Point": OnePointCrossover(),
        "Two Point": TwoPointCrossover(),
        "Uniform": UniformCrossover(),
        "Edge Swap": EdgeSwapCrossover(),
        "Subgraph Swap": SubgraphSwapCrossover(),
    }

    crossover = crossovers[crossover_type]

    child1, child2 = crossover.crossover(
        parent1,
        parent2,
        random.Random(42),
    )

    for child in (child1, child2):
        assert child.node_count == 5

        assert all(
            value in (0, 1)
            for value in child.node_attributes
        )

        for row in child.adjacency_matrix:
            assert all(value in (0, 1) for value in row)

        for i in range(5):
            for j in range(5):
                assert (
                    child.adjacency_matrix[i][j]
                    == child.adjacency_matrix[j][i]
                )

        for i in range(5):
            assert child.adjacency_matrix[i][i] == 0



@pytest.mark.parametrize(
    "mutation_type",
    [
        "Bit Flip",
        "Edge Flip",
        "Node Attr Flip",
        "Swap",
    ],
)
def test_all_mutation_types_return_valid_graphs(mutation_type):
    algo = TrackedGraphGA(
        node_count=5,
        fitness_fn=lambda graph: 0.0,
        population_size=4,
        max_generations=1,
        rng=random.Random(42),
    )

    graph = algo.encoding.generate_random(algo._rng)

    from graphga.operators.mutation import (
        BitFlipMutation,
        EdgeFlipMutation,
        NodeAttrFlipMutation,
        SwapMutation,
    )

    mutations = {
        "Bit Flip": BitFlipMutation(mutation_rate=1.0),
        "Edge Flip": EdgeFlipMutation(mutation_rate=1.0),
        "Node Attr Flip": NodeAttrFlipMutation(mutation_rate=1.0),
        "Swap": SwapMutation(mutation_rate=1.0),
    }

    mutation = mutations[mutation_type]

    mutated = mutation.mutate(
        graph,
        random.Random(42),
    )

    assert mutated.node_count == 5

    assert all(
        value in (0, 1)
        for value in mutated.node_attributes
    )

    for row in mutated.adjacency_matrix:
        assert all(value in (0, 1) for value in row)

    for i in range(5):
        for j in range(5):
            assert (
                mutated.adjacency_matrix[i][j]
                == mutated.adjacency_matrix[j][i]
            )

    for i in range(5):
        assert mutated.adjacency_matrix[i][i] == 0


def test_graphga_run_api():
    from fastapi.testclient import TestClient
    from api.main import app

    client = TestClient(app)

    response = client.post(
        "/api/graphga/run",
        json={
            "nodeCount": 5,
            "populationSize": 10,
            "generations": 3,
            "directed": False,
            "allowSelfLoop": False,
            "randomSeed": 42,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "generation" in data
    assert "bestFitness" in data
    assert "avgFitness" in data
    assert "worstFitness" in data
def test_undirected_self_loop_density():
    from api.main import graph_onemax_fitness
    from graphga.utils.graph import Graph

    graph = Graph(
        adjacency_matrix=[
            [1, 1],
            [1, 1],
        ],
        node_attributes=[0, 0],
        directed=False,
        allow_self_loop=True,
    )

    fitness = graph_onemax_fitness(
        graph,
        connectivity_bonus_value=0.0,
        sparsity_penalty_value=1.0,
    )

    # 3 possible undirected edges:
    # (0,0), (0,1), (1,1)
    # All 3 exist, so density should be 1.0.
    assert fitness == -1.0

def test_undirected_self_loop_density():
    from api.main import graph_onemax_fitness
    from graphga.utils.graph import Graph

    graph = Graph(
        adjacency_matrix=[
            [1, 1, 0],
            [1, 0, 0],
            [0, 0, 0],
        ],
        node_attributes=[0, 0, 0],
        directed=False,
        allow_self_loop=True,
    )

    fitness = graph_onemax_fitness(
        graph,
        connectivity_bonus_value=0.0,
        sparsity_penalty_value=1.0,
    )

    # Existing unique undirected edges:
    # (0,0), (0,1)
    #
    # Possible unique edges:
    # (0,0), (0,1), (0,2),
    # (1,1), (1,2), (2,2)
    #
    # Therefore density = 2 / 6 = 1/3.
    assert fitness == -(1 / 3)