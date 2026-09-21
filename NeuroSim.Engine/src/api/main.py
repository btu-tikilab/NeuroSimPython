# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/api/main.py
import time
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
import random

from graphga.graph_ga import GraphGA
from graphga.utils.graph import Graph, GraphIndividual

from bitga.engine import BitGAEngine
from bitga import build_engine
from neurosim_problems import OneMaxProblem, KnapsackProblem

app = FastAPI(
    title="NeuroSim Engine API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== GENERIC PLAYGROUND MODELS ====================
# bitga

class BitGARunRequest(BaseModel):
    problem: str
    bitstringLength: int
    populationSize: int = 100
    generations: int = 100
    mutationRate: Optional[float] = None
    tournamentSize: int = 3
    seed: Optional[int] = 42
    crossoverType: str = "Uniform"
    crossoverProbability: float = 0.5
    mutationType: str = "Bit Flip"
    values: Optional[List[float]] = None
    weights: Optional[List[float]] = None
    capacity: Optional[float] = None


class GenerationInHistory(BaseModel):
    generation: int
    bestFitness: float
    avgFitness: float
    worstFitness: float
    bestGenome: List[int]


class BitGARunResponse(BaseModel):
    runId: str
    bestFitness: float
    isOptimal: bool
    bestSolution: List[int]
    generationsToConvergence: int
    totalGenerations: int
    convergenceHistory: List[GenerationInHistory]
    executionTimeSeconds: float


# ==================== GRAPH GA MODELS & SCHEMAS ====================

class RunConfig(BaseModel):
    problem: str = "graph_onemax"
    populationSize: int = 50
    generations: int = 100
    mutationRate: float = 0.05
    crossoverRate: float = 0.8
    seed: int = 42
    nodeCount: int = 8
    graphMode: str = "Directed"
    allowSelfLoop: bool = False
    parentSelection: str = "Tournament"
    tournamentSize: int = 3
    crossoverType: str = "One Point"
    mutationType: str = "Bit Flip"
    eliteCount: int = 2
    targetFitness: float = 100.0
    connectivityBonus: float = 0.0
    sparsityPenalty: float = 0.0


# Global storage for last GraphGA result
_last_graph_result: Optional[Graph] = None
_last_graph_history: List[dict] = []
_last_graph_config: Optional[RunConfig] = None


# ==================== GRAPH GA FITNESS & SUBCLASS ====================

def graph_onemax_fitness(graph: Graph, conn_bonus: float = 10.0, spars_penalty: float = 2.0) -> float:
    # 1. Base score: active node attributes
    active_nodes = sum(graph.node_attributes)

    # 2. Connectivity bonus (BFS from node 0)
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

    connectivity_bonus = conn_bonus if is_connected else 0.0

    # 3. Sparsity penalty
    edges = 0
    for i in range(node_count):
        for j in range(node_count):
            if graph.adjacency_matrix[i][j] == 1:
                edges += 1

    if graph.directed:
        max_edges = node_count * node_count if graph.allow_self_loop else node_count * (node_count - 1)
    else:
        max_edges = node_count * (node_count - 1) // 2
        if graph.allow_self_loop:
            max_edges += node_count
        edges = 0
        for i in range(node_count):
            for j in range(i, node_count):
                if graph.adjacency_matrix[i][j] == 1:
                    edges += 1

    density = edges / max_edges if max_edges > 0 else 0.0
    sparsity_penalty = spars_penalty * density

    return active_nodes + connectivity_bonus - sparsity_penalty


def graph_pathfinding_fitness(graph: Graph, spars_penalty: float = 5.0) -> float:
    node_count = graph.node_count
    if node_count <= 1:
        return 0.0

    # BFS from node 0 to find shortest path to node N-1
    visited = [False] * node_count
    dist = [-1] * node_count
    queue = [0]
    visited[0] = True
    dist[0] = 0
    head = 0

    while head < len(queue):
        curr = queue[head]
        head += 1
        for neighbor in range(node_count):
            if graph.adjacency_matrix[curr][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True
                dist[neighbor] = dist[curr] + 1
                queue.append(neighbor)

    shortest_path_len = dist[node_count - 1]

    # Path reward logic (shorter path = higher bonus)
    if shortest_path_len != -1:
        path_bonus = 20.0 + (node_count - shortest_path_len) * 5.0
    else:
        path_bonus = 0.0

    # Sparsity penalty
    edges = 0
    for i in range(node_count):
        for j in range(node_count):
            if graph.adjacency_matrix[i][j] == 1:
                edges += 1

    if graph.directed:
        max_edges = node_count * node_count if graph.allow_self_loop else node_count * (node_count - 1)
    else:
        max_edges = node_count * (node_count - 1) // 2
        if graph.allow_self_loop:
            max_edges += node_count
        edges = 0
        for i in range(node_count):
            for j in range(i, node_count):
                if graph.adjacency_matrix[i][j] == 1:
                    edges += 1

    density = edges / max_edges if max_edges > 0 else 0.0
    sparsity_penalty = spars_penalty * density

    active_nodes = sum(graph.node_attributes)

    return active_nodes + path_bonus - sparsity_penalty


class TrackedGraphGA(GraphGA):
    def __init__(self, *args, **kwargs):
        parent_selection = kwargs.pop("parent_selection", "Tournament")
        crossover_type = kwargs.pop("crossover_type", "One Point")
        mutation_type = kwargs.pop("mutation_type", "Bit Flip")
        crossover_rate = kwargs.get("crossover_rate", 0.8)
        self.target_fitness = kwargs.pop("target_fitness", None)

        super().__init__(*args, **kwargs)
        self.crossover_rate = crossover_rate

        # 1. Selection Operator Mapping
        from graphga.operators.selection import TournamentSelection, RouletteWheelSelection, RankSelection
        if parent_selection == "Tournament":
            self.selection = TournamentSelection(tournament_size=kwargs.get("tournament_size", 3))
        elif parent_selection == "Roulette Wheel":
            self.selection = RouletteWheelSelection()
        elif parent_selection == "Rank":
            self.selection = RankSelection()

        # 2. Crossover Operator Mapping
        from graphga.operators.crossover import (
            OnePointCrossover, TwoPointCrossover, UniformCrossover,
            EdgeSwapCrossover, SubgraphSwapCrossover
        )
        if crossover_type == "One Point":
            self.crossover = OnePointCrossover()
        elif crossover_type == "Two Point":
            self.crossover = TwoPointCrossover()
        elif crossover_type == "Uniform":
            self.crossover = UniformCrossover()
        elif crossover_type == "Edge Swap":
            self.crossover = EdgeSwapCrossover()
        elif crossover_type == "Subgraph Swap":
            self.crossover = SubgraphSwapCrossover()

        # 3. Mutation Operator Mapping
        from graphga.operators.mutation import (
            EdgeFlipMutation, NodeAttrFlipMutation, SwapMutation, BitFlipMutation
        )
        m_rate = kwargs.get("mutation_rate")
        if m_rate is None:
            m_rate = 1.0 / kwargs.get("node_count", 8)

        if mutation_type == "Edge Flip":
            self.mutation = EdgeFlipMutation(mutation_rate=m_rate)
        elif mutation_type == "Node Attr Flip":
            self.mutation = NodeAttrFlipMutation(mutation_rate=m_rate)
        elif mutation_type == "Swap":
            self.mutation = SwapMutation(mutation_rate=m_rate)
        elif mutation_type == "Bit Flip":
            self.mutation = BitFlipMutation(mutation_rate=m_rate)

        self.history_log = []

    def _should_stop(self) -> bool:
        if self.target_fitness is not None and self.history_log:
            best_so_far = self.history_log[-1]["bestFitness"]
            if best_so_far >= self.target_fitness:
                return True
        return False

    def breed(self, parents: List[GraphIndividual]) -> List[GraphIndividual]:
        offspring = []
        while len(offspring) < self.population_size:
            p1 = parents[self._rng.randrange(len(parents))]
            p2 = parents[self._rng.randrange(len(parents))]

            # Apply crossover based on crossover_rate
            if self._rng.random() < self.crossover_rate:
                child1, child2 = self.crossover.crossover(p1.graph, p2.graph, self._rng)
            else:
                child1, child2 = p1.graph.copy(), p2.graph.copy()

            child1 = self.mutation.mutate(child1, self._rng)
            child2 = self.mutation.mutate(child2, self._rng)

            offspring.append(GraphIndividual(graph=child1, fitness=0.0))
            if len(offspring) < self.population_size:
                offspring.append(GraphIndividual(graph=child2, fitness=0.0))
        return offspring

    def run(self) -> Any:
        pop = self.initialize()
        pop = self.evaluate(pop)

        best_ind = self.best_solution(pop)
        self.history_log.append({
            "generation": 0,
            "bestFitness": best_ind.fitness,
            "avgFitness": sum(ind.fitness for ind in pop) / len(pop),
            "worstFitness": min(ind.fitness for ind in pop),
            "bestGraph": best_ind.graph.copy()
        })

        gen = 0
        while gen < self.max_generations and not self._should_stop():
            parents = self.select(pop)
            offspring = self.breed(parents)
            offspring = self.evaluate(offspring)
            pop = self.replace(pop, offspring)
            gen += 1

            best_ind = self.best_solution(pop)
            self.history_log.append({
                "generation": gen,
                "bestFitness": best_ind.fitness,
                "avgFitness": sum(ind.fitness for ind in pop) / len(pop),
                "worstFitness": min(ind.fitness for ind in pop),
                "bestGraph": best_ind.graph.copy()
            })

        return self.best_solution(pop)


def serialize_graph_to_cytoscape(graph: Graph) -> dict:
    nodes = []
    n = graph.node_count
    for i in range(n):
        node_type = "input" if i == 0 else "output" if i == n - 1 else "hidden"
        nodes.append({
            "id": f"n{i}",
            "type": node_type,
            "value": int(graph.node_attributes[i])
        })

    edges = []
    for i in range(n):
        for j in range(n):
            if graph.adjacency_matrix[i][j] == 1:
                if not graph.directed and j < i:
                    continue
                edges.append({
                    "source": f"n{i}",
                    "target": f"n{j}",
                    "weight": 1.0
                })
    return {"nodes": nodes, "edges": edges}


# ==================== BIT GA HELPERS ====================

MAX_KNAPSACK_ITEMS = 200
MAX_KNAPSACK_CAPACITY = 100_000


def _build_bitga_problem(request: BitGARunRequest):
    if request.problem == "knapsack":
        if not request.values or not request.weights or request.capacity is None:
            raise HTTPException(
                status_code=400,
                detail="knapsack requires 'values', 'weights', and 'capacity'",
            )
        if len(request.values) != request.bitstringLength:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"len(values)={len(request.values)} must equal "
                    f"bitstringLength={request.bitstringLength}"
                ),
            )
        if len(request.values) > MAX_KNAPSACK_ITEMS:
            raise HTTPException(
                status_code=400,
                detail=f"too many items: {len(request.values)} > {MAX_KNAPSACK_ITEMS}",
            )
        if request.capacity > MAX_KNAPSACK_CAPACITY:
            raise HTTPException(
                status_code=400,
                detail=f"capacity too large: {request.capacity} > {MAX_KNAPSACK_CAPACITY}",
            )
        try:
            return KnapsackProblem(
                values=request.values,
                weights=request.weights,
                capacity=request.capacity,
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    if request.problem == "onemax":
        try:
            return OneMaxProblem(length=request.bitstringLength)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    raise HTTPException(
        status_code=400,
        detail=f"Unknown problem: {request.problem!r} (expected 'onemax' or 'knapsack')",
    )


def _run_bitga_with_history(engine: BitGAEngine):
    start_time = time.time()

    history: List[GenerationInHistory] = []
    best_fitness_ever = float("-inf")
    generations_to_convergence = 0

    def record(population, generation):
        nonlocal best_fitness_ever, generations_to_convergence

        best_idx = engine.fitness_values.index(max(engine.fitness_values))
        best = engine.fitness_values[best_idx]
        avg = sum(engine.fitness_values) / len(engine.fitness_values)
        worst = min(engine.fitness_values)

        if best > best_fitness_ever:
            best_fitness_ever = best
            generations_to_convergence = generation

        history.append(
            GenerationInHistory(
                generation=generation,
                bestFitness=best,
                avgFitness=avg,
                worstFitness=worst,
                bestGenome=list(population[best_idx]),
            )
        )

    pop = engine.initialize()
    pop = engine.evaluate(pop)
    record(pop, 0)

    gen = 0
    while gen < engine.max_generations and not engine._should_stop():
        parents = engine.select(pop)
        offspring = engine.breed(parents)
        offspring = engine.evaluate(offspring)
        pop = engine.replace(pop, offspring)
        gen += 1
        record(pop, gen)

    best_genome = engine.best_solution(pop)
    execution_time = time.time() - start_time

    return best_genome, history, generations_to_convergence, execution_time


# ==================== ENDPOINTS ====================

@app.get("/app-info")
@app.get("/api/info")
def get_app_info():
    return {
        "appName": "NeuroSim",
        "version": "1.0.0"
    }


@app.get("/playgrounds")
@app.get("/api/playgrounds")
def get_playgrounds():
    return {
        "playgrounds": [
            {
                "id": "bitga",
                "name": "BitGA",
                "description": "Binary Genetic Algorithm Playground"
            },
            {
                "id": "graphga",
                "name": "GraphGA",
                "description": "Graph Based Genetic Algorithm Playground"
            }
        ]
    }


@app.post("/api/graphga/run")
def run_graphga(config: RunConfig):
    global _last_graph_result, _last_graph_history, _last_graph_config

    _last_graph_config = config
    rng = random.Random(config.seed)

    if config.problem == "graph_pathfinding":
        fit_fn = lambda g: graph_pathfinding_fitness(g, spars_penalty=config.sparsityPenalty)
    else:
        fit_fn = lambda g: graph_onemax_fitness(g, conn_bonus=config.connectivityBonus,
                                                spars_penalty=config.sparsityPenalty)

    algo = TrackedGraphGA(
        node_count=config.nodeCount,
        fitness_fn=fit_fn,
        population_size=config.populationSize,
        max_generations=config.generations,
        rng=rng,
        directed=(config.graphMode == "Directed"),
        allow_self_loop=config.allowSelfLoop,
        tournament_size=config.tournamentSize,
        crossover_rate=config.crossoverRate,
        mutation_rate=config.mutationRate,
        elitism=config.eliteCount,
        parent_selection=config.parentSelection,
        crossover_type=config.crossoverType,
        mutation_type=config.mutationType,
        target_fitness=config.targetFitness
    )

    best_individual = algo.run()
    _last_graph_result = best_individual.graph
    _last_graph_history = algo.history_log

    return {
        "generation": len(_last_graph_history) - 1,
        "bestFitness": best_individual.fitness,
        "avgFitness": _last_graph_history[-1]["avgFitness"],
        "worstFitness": _last_graph_history[-1]["worstFitness"],
    }


@app.get("/api/graphga/best")
def get_graphga_best():
    if _last_graph_result is None:
        return {"nodes": [], "edges": [], "fitness": 0.0, "generation": 0}
    return serialize_graph_to_cytoscape(_last_graph_result)


@app.get("/api/graphga/history")
def get_graphga_history():
    return _last_graph_history


@app.get("/api/graphga/snapshot/{generation}")
def get_graphga_snapshot(generation: int):
    if not _last_graph_history:
        return {
            "generation": generation,
            "bestFitness": 0.0,
            "avgFitness": 0.0,
            "worstFitness": 0.0,
            "bestGenome": {},
        }

    entry = next(
        (e for e in _last_graph_history if e["generation"] == generation),
        None,
    )
    if entry is None:
        entry = _last_graph_history[-1]

    # Return serialized snapshot
    snap_genome = serialize_graph_to_cytoscape(entry["bestGraph"]) if entry.get("bestGraph") else {}
    if snap_genome:
        snap_genome["generation"] = entry["generation"]

    return {
        "generation": generation,
        "bestFitness": entry["bestFitness"],
        "avgFitness": entry["avgFitness"],
        "worstFitness": entry["worstFitness"],
        "bestGenome": snap_genome,
    }


# ==================== BIT GA ENDPOINTS ====================

@app.get("/bitga/problems")
def get_bitga_problems():
    return {
        "problems": [
            {
                "id": "onemax",
                "name": "OneMax",
                "description": "Maximize number of 1s in bitstring"
            },
            {
                "id": "knapsack",
                "name": "0/1 Knapsack",
                "description": "Maximize value while respecting weight"
            }
        ]
    }


@app.post("/bitga/run")
def run_bitga(request: BitGARunRequest) -> BitGARunResponse:
    problem = _build_bitga_problem(request)

    config = {
        "bitstring_length": request.bitstringLength,
        "population_size": request.populationSize,
        "generations": request.generations,
        "seed": request.seed if request.seed is not None else 42,
        "tournament_size": request.tournamentSize,
        "crossover_type": request.crossoverType,
        "crossover_probability": request.crossoverProbability,
        "mutation_type": request.mutationType,
        "mutation_rate": request.mutationRate,
    }

    try:
        engine = build_engine(problem, config)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    best_genome, history, generations_to_convergence, execution_time = (
        _run_bitga_with_history(engine)
    )

    best_fitness = problem.fitness(best_genome)
    is_optimal = problem.is_optimal(best_genome)
    run_id = f"run_{uuid.uuid4().hex[:12]}"

    return BitGARunResponse(
        runId=run_id,
        bestFitness=best_fitness,
        isOptimal=is_optimal,
        bestSolution=best_genome,
        generationsToConvergence=generations_to_convergence,
        totalGenerations=len(history) - 1,
        convergenceHistory=history,
        executionTimeSeconds=execution_time,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)