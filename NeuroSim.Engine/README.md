<!-- AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/README.md -->
# NeuroSim.Engine

Generic evolutionary engine supporting multiple genome paradigms and pluggable operators.

Currently shipped:
- `BaseAlgorithm`: Stable-Baselines–style hook for evolution cycles.

See `../samples/poc/` for concrete, pure-Python toy implementations.

## BaseAlgorithm
BaseAlgorithm path: src/core/base_algorithm.py

BaseAlgorithm is an abstract class that defines the common lifecycle of a Genetic Algorithm.

It provides the generic evolution loop:

Initialize → Evaluate → Select → Breed → Replace → Repeat

Different Genetic Algorithms (such as BitGA and GraphGA) inherit from BaseAlgorithm and implement the problem-specific methods.

### Implemented by subclasses

- initialize()
- evaluate()
- select()
- breed()
- replace()
- best_solution()

The run() method is shared by all algorithms and executes the complete evolution process.

