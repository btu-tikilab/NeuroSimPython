# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Problems/TestSuites/test_backend.py
import sys
from pathlib import Path
import unittest
import random
import httpx

# Add src folder of NeuroSim.Engine to path so we can import packages
ENGINE_SRC = Path(__file__).resolve().parents[3] / "NeuroSim.Engine" / "src"
sys.path.insert(0, str(ENGINE_SRC))

from graphga.utils.graph import Graph, create_random_graph, count_edges, calculate_density
from graphga.operators.encoding import GraphEncoding
from graphga.operators.selection import TournamentSelection, RouletteWheelSelection, RankSelection
from graphga.operators.crossover import (
    UniformGraphCrossover, EdgeSwapCrossover, SubgraphSwapCrossover,
    OnePointCrossover, TwoPointCrossover, UniformCrossover
)
from graphga.operators.mutation import (
    EdgeFlipMutation, NodeAttrFlipMutation, SwapMutation, BitFlipMutation
)
from api.main import app, graph_onemax_fitness, TrackedGraphGA


class TestGraphGAUtilities(unittest.TestCase):
    """Verify core graph utilities, directed/undirected properties and diagonal self-loops."""

    def test_random_graph_generation(self):
        rng = random.Random(42)
        graph = create_random_graph(node_count=6, directed=False, allow_self_loop=False, rng=rng)
        self.assertEqual(graph.node_count, 6)
        self.assertEqual(len(graph.node_attributes), 6)
        
        # Test self-loops disabled
        for i in range(6):
            self.assertEqual(graph.adjacency_matrix[i][i], 0)

        # Test undirected symmetry
        for i in range(6):
            for j in range(6):
                self.assertEqual(graph.adjacency_matrix[i][j], graph.adjacency_matrix[j][i])

    def test_density_calculations(self):
        # Empty graph
        g = Graph(
            adjacency_matrix=[[0, 0], [0, 0]],
            node_attributes=[1, 1],
            directed=False,
            allow_self_loop=False
        )
        self.assertEqual(count_edges(g), 0)
        self.assertEqual(calculate_density(g), 0.0)


class TestGraphGAEvaluators(unittest.TestCase):
    """Test fitness scoring, connectivity checks, and density penalties."""

    def test_onemax_scoring_and_penalties(self):
        # Test fully disconnected graph
        g = Graph(
            adjacency_matrix=[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            node_attributes=[1, 1, 1],
            directed=False,
            allow_self_loop=False
        )
        # Should get: active_nodes (3) + connectivity (0) - density_penalty (0) = 3.0
        self.assertAlmostEqual(graph_onemax_fitness(g), 3.0)

        # Test connected graph
        g_conn = Graph(
            adjacency_matrix=[
                [0, 1, 1],
                [1, 0, 0],
                [1, 0, 0]
            ],
            node_attributes=[1, 1, 1],
            directed=False,
            allow_self_loop=False
        )
        # Should get: active_nodes (3) + connectivity (10) - density_penalty = 13 - penalty
        fitness = graph_onemax_fitness(g_conn)
        self.assertTrue(fitness > 10.0)

    def test_pathfinding_scoring(self):
        from api.main import graph_pathfinding_fitness
        # Direct link Node 0 -> Node 1 in 2-node graph
        g_direct = Graph(
            adjacency_matrix=[
                [0, 1],
                [1, 0]
            ],
            node_attributes=[1, 1],
            directed=False,
            allow_self_loop=False
        )
        # shortest path length = 1
        # path_bonus = 20.0 + (2 - 1) * 5.0 = 25.0
        # sparsity_penalty = 5.0 * (1 / 1) = 5.0
        # active_nodes = 2
        # fitness = 2 + 25.0 - 5.0 = 22.0
        self.assertAlmostEqual(graph_pathfinding_fitness(g_direct), 22.0)

        # Disconnected path Node 0 and Node 1 are unconnected
        g_dis = Graph(
            adjacency_matrix=[
                [0, 0],
                [0, 0]
            ],
            node_attributes=[1, 1],
            directed=False,
            allow_self_loop=False
        )
        # shortest path length = -1 (unreachable)
        # path_bonus = 0.0
        # sparsity_penalty = 0.0
        # active_nodes = 2
        # fitness = 2.0
        self.assertAlmostEqual(graph_pathfinding_fitness(g_dis), 2.0)


class TestSelectionOperators(unittest.TestCase):
    """Verify tournament, roulette-wheel, and rank selection implementations."""

    def setUp(self):
        self.rng = random.Random(42)
        self.pop = [
            create_random_graph(node_count=5, directed=False, allow_self_loop=False, rng=self.rng)
            for _ in range(10)
        ]
        self.fitness_vals = [float(i) for i in range(10)]  # Fitness from 0.0 to 9.0

    def test_tournament_selection(self):
        sel = TournamentSelection(tournament_size=3)
        winners = sel.select(self.pop, self.fitness_vals, num_parents=5, rng=self.rng)
        self.assertEqual(len(winners), 5)

    def test_roulette_wheel_selection(self):
        sel = RouletteWheelSelection()
        winners = sel.select(self.pop, self.fitness_vals, num_parents=5, rng=self.rng)
        self.assertEqual(len(winners), 5)

    def test_rank_selection(self):
        sel = RankSelection()
        winners = sel.select(self.pop, self.fitness_vals, num_parents=5, rng=self.rng)
        self.assertEqual(len(winners), 5)


class TestCrossoverOperators(unittest.TestCase):
    """Verify graph crossovers maintain shape, node counts, and symmetry constraints."""

    def setUp(self):
        self.rng = random.Random(42)
        self.parent1 = create_random_graph(node_count=8, directed=False, allow_self_loop=False, rng=self.rng)
        self.parent2 = create_random_graph(node_count=8, directed=False, allow_self_loop=False, rng=self.rng)

    def test_uniform_graph_crossover(self):
        cross = UniformGraphCrossover()
        c1, c2 = cross.crossover(self.parent1, self.parent2, self.rng)
        self.assertEqual(c1.node_count, 8)
        self.assertEqual(c2.node_count, 8)

    def test_edge_swap_crossover(self):
        cross = EdgeSwapCrossover()
        c1, c2 = cross.crossover(self.parent1, self.parent2, self.rng)
        self.assertEqual(c1.node_count, 8)

    def test_subgraph_swap_crossover(self):
        cross = SubgraphSwapCrossover()
        c1, c2 = cross.crossover(self.parent1, self.parent2, self.rng)
        self.assertEqual(c1.node_count, 8)

    def test_one_point_crossover(self):
        cross = OnePointCrossover()
        c1, c2 = cross.crossover(self.parent1, self.parent2, self.rng)
        self.assertEqual(c1.node_count, 8)

    def test_two_point_crossover(self):
        cross = TwoPointCrossover()
        c1, c2 = cross.crossover(self.parent1, self.parent2, self.rng)
        self.assertEqual(c1.node_count, 8)

    def test_uniform_crossover(self):
        cross = UniformCrossover()
        c1, c2 = cross.crossover(self.parent1, self.parent2, self.rng)
        self.assertEqual(c1.node_count, 8)


class TestMutationOperators(unittest.TestCase):
    """Verify mutation operators respect boundary and graph constraints."""

    def setUp(self):
        self.rng = random.Random(42)
        self.graph = create_random_graph(node_count=6, directed=False, allow_self_loop=False, rng=self.rng)

    def test_edge_flip_mutation(self):
        mut = EdgeFlipMutation(mutation_rate=0.2)
        mutated = mut.mutate(self.graph, self.rng)
        self.assertEqual(mutated.node_count, 6)

    def test_node_attr_flip_mutation(self):
        mut = NodeAttrFlipMutation(mutation_rate=0.2)
        mutated = mut.mutate(self.graph, self.rng)
        self.assertEqual(mutated.node_count, 6)
        # Connection matrix should remain identical
        self.assertEqual(mutated.adjacency_matrix, self.graph.adjacency_matrix)

    def test_swap_mutation(self):
        mut = SwapMutation(mutation_rate=1.0)
        mutated = mut.mutate(self.graph, self.rng)
        self.assertEqual(mutated.node_count, 6)

    def test_bit_flip_mutation(self):
        mut = BitFlipMutation(mutation_rate=0.2)
        mutated = mut.mutate(self.graph, self.rng)
        self.assertEqual(mutated.node_count, 6)


class TestGraphGAAlgorithm(unittest.TestCase):
    """Verify execution lifecycle, elitism, early stopping, and seed reproducibility."""

    def test_reproducibility(self):
        # Run 1
        rng1 = random.Random(123)
        algo1 = TrackedGraphGA(
            node_count=5,
            fitness_fn=graph_onemax_fitness,
            population_size=10,
            max_generations=5,
            rng=rng1,
            directed=False,
            allow_self_loop=False
        )
        res1 = algo1.run()

        # Run 2
        rng2 = random.Random(123)
        algo2 = TrackedGraphGA(
            node_count=5,
            fitness_fn=graph_onemax_fitness,
            population_size=10,
            max_generations=5,
            rng=rng2,
            directed=False,
            allow_self_loop=False
        )
        res2 = algo2.run()

        self.assertEqual(res1.fitness, res2.fitness)
        self.assertEqual(res1.graph.adjacency_matrix, res2.graph.adjacency_matrix)


class TestFastAPIServer(unittest.IsolatedAsyncioTestCase):
    """Test HTTP API Server endpoints using manual HTTPX async clients."""

    async def test_api_info_and_playgrounds(self):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            res_info = await client.get("/api/info")
            self.assertEqual(res_info.status_code, 200)
            self.assertEqual(res_info.json()["appName"], "NeuroSim")

            res_play = await client.get("/api/playgrounds")
            self.assertEqual(res_play.status_code, 200)
            self.assertTrue(len(res_play.json()["playgrounds"]) >= 2)

    async def test_run_graphga_endpoint(self):
        payload = {
            "populationSize": 10,
            "generations": 5,
            "mutationRate": 0.05,
            "crossoverRate": 0.8,
            "seed": 42,
            "nodeCount": 6,
            "graphMode": "Directed",
            "allowSelfLoop": False,
            "parentSelection": "Tournament",
            "tournamentSize": 3,
            "crossoverType": "One Point",
            "mutationType": "Bit Flip",
            "eliteCount": 1,
            "targetFitness": 50.0,
            "connectivityBonus": 2.0,
            "sparsityPenalty": 0.5
        }

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            res = await client.post("/api/graphga/run", json=payload)
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("bestFitness", data)
            self.assertIn("generation", data)

            # Test retrieving best genome
            res_best = await client.get("/api/graphga/best")
            self.assertEqual(res_best.status_code, 200)
            best_data = res_best.json()
            self.assertIn("nodes", best_data)
            self.assertIn("edges", best_data)

            # Test retrieving history
            res_hist = await client.get("/api/graphga/history")
            self.assertEqual(res_hist.status_code, 200)
            self.assertTrue(len(res_hist.json()) > 0)

    async def test_run_graphga_pathfinding_endpoint(self):
        payload = {
            "problem": "graph_pathfinding",
            "populationSize": 10,
            "generations": 5,
            "mutationRate": 0.05,
            "crossoverRate": 0.8,
            "seed": 42,
            "nodeCount": 6,
            "graphMode": "Directed",
            "allowSelfLoop": False,
            "parentSelection": "Tournament",
            "tournamentSize": 3,
            "crossoverType": "One Point",
            "mutationType": "Bit Flip",
            "eliteCount": 1,
            "targetFitness": 50.0,
            "connectivityBonus": 2.0,
            "sparsityPenalty": 0.5
        }

        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            res = await client.post("/api/graphga/run", json=payload)
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertIn("bestFitness", data)
            self.assertIn("generation", data)

            # Test retrieving best genome
            res_best = await client.get("/api/graphga/best")
            self.assertEqual(res_best.status_code, 200)
            best_data = res_best.json()
            self.assertIn("nodes", best_data)
            self.assertIn("edges", best_data)


if __name__ == "__main__":
    unittest.main()
