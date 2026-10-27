import re

filepath = "/Users/samruddhipowar5gmail.com/Desktop/Neuro/NeuroSim.Engine/src/api/main.py"
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add target_fitness and _should_stop to TrackedGraphGA
init_pattern = r'class TrackedGraphGA\(GraphGA\):\n    def __init__\(self, \*args, \*\*kwargs\):\n        parent_selection = kwargs\.pop\("parent_selection", "Tournament"\)\n        crossover_type = kwargs\.pop\("crossover_type", "One Point"\)\n        mutation_type = kwargs\.pop\("mutation_type", "Bit Flip"\)\n        crossover_rate = kwargs\.get\("crossover_rate", 0\.8\)'
init_repl = r'class TrackedGraphGA(GraphGA):\n    def __init__(self, *args, **kwargs):\n        parent_selection = kwargs.pop("parent_selection", "Tournament")\n        crossover_type = kwargs.pop("crossover_type", "One Point")\n        mutation_type = kwargs.pop("mutation_type", "Bit Flip")\n        crossover_rate = kwargs.get("crossover_rate", 0.8)\n        self.target_fitness = kwargs.pop("target_fitness", None)'

content = re.sub(init_pattern, init_repl, content)

should_stop_code = """
    def _should_stop(self) -> bool:
        if self.target_fitness is not None and self.history_log:
            best_so_far = self.history_log[-1]["bestFitness"]
            if best_so_far >= self.target_fitness:
                return True
        return False
"""
content = content.replace('self.history_log = []', 'self.history_log = []\n' + should_stop_code)

# 2. Add target_fitness argument to TrackedGraphGA instantiation
algo_pattern = r'crossover_type=config\.crossoverType,\n        mutation_type=config\.mutationType\n    \)'
algo_repl = r'crossover_type=config.crossoverType,\n        mutation_type=config.mutationType,\n        target_fitness=config.targetFitness\n    )'
content = re.sub(algo_pattern, algo_repl, content)


# 3. Modify global fitness functions to accept config dynamically
# First, remove the global graph_onemax_fitness and graph_pathfinding_fitness
fit_pattern = r'def graph_onemax_fitness\(graph: Graph\) -> float:.*?def run_graphga\(config: RunConfig\):'
fit_repl = r'def run_graphga(config: RunConfig):'
content = re.sub(fit_pattern, fit_repl, content, flags=re.DOTALL)


run_setup_pattern = r'def run_graphga\(config: RunConfig\):\n    global _last_graph_result, _last_graph_history, _last_graph_config\n\n    _last_graph_config = config\n    rng = random\.Random\(config\.seed\)\n\n    if config\.problem == "graph_pathfinding":\n        fit_fn = graph_pathfinding_fitness\n    else:\n        fit_fn = graph_onemax_fitness'

new_run_setup = """def run_graphga(config: RunConfig):
    global _last_graph_result, _last_graph_history, _last_graph_config

    _last_graph_config = config
    rng = random.Random(config.seed)

    if config.problem == "graph_pathfinding":
        def fit_fn(graph: Graph) -> float:
            node_count = graph.node_count
            if node_count <= 1: return 0.0
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
            if shortest_path_len != -1:
                path_bonus = 20.0 + (node_count - shortest_path_len) * 5.0
            else:
                path_bonus = 0.0
            edges = 0
            for i in range(node_count):
                for j in range(node_count):
                    if graph.adjacency_matrix[i][j] == 1:
                        edges += 1
            max_edges = node_count * node_count if graph.allow_self_loop else node_count * (node_count - 1)
            if not graph.directed:
                edges = edges // 2
                max_edges = max_edges // 2
            density = edges / max_edges if max_edges > 0 else 0.0
            sparsity_penalty = config.sparsityPenalty * density
            active_nodes = sum(graph.node_attributes)
            return active_nodes + path_bonus - sparsity_penalty
    else:
        def fit_fn(graph: Graph) -> float:
            active_nodes = sum(graph.node_attributes)
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
            connectivity_bonus = config.connectivityBonus if is_connected else 0.0
            edges = 0
            for i in range(node_count):
                for j in range(node_count):
                    if graph.adjacency_matrix[i][j] == 1:
                        edges += 1
            max_edges = node_count * node_count if graph.allow_self_loop else node_count * (node_count - 1)
            if not graph.directed:
                edges = edges // 2
                max_edges = max_edges // 2
            density = edges / max_edges if max_edges > 0 else 0.0
            sparsity_penalty = config.sparsityPenalty * density
            return active_nodes + connectivity_bonus - sparsity_penalty"""

content = re.sub(run_setup_pattern, new_run_setup, content)

with open(filepath, 'w') as f:
    f.write(content)

print("Modified main.py")
