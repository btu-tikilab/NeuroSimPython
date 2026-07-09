# NeuroSim/Engine/bitga/engine.py
"""
Main BitGA Engine
Orchestrates the genetic algorithm loop
"""

import random
import time
from typing import List
from dataclasses import dataclass

from .operators import (
    BitStringEncoding,
    TournamentSelection,
    UniformCrossover,
    BitFlipMutation
)

@dataclass
class GenerationStats:
    """Statistics for a single generation."""
    generation: int
    best_fitness: float
    avg_fitness: float
    worst_fitness: float
    best_genome: List[int]

@dataclass
class RunResult:
    """Final result of a GA run."""
    run_id: str
    best_fitness: float
    best_solution: List[int]
    generations_to_convergence: int
    total_generations: int
    convergence_history: List[GenerationStats]
    execution_time_seconds: float

class BitGAEngine:
    """Genetic Algorithm Engine for bitstring problems."""
    
    def __init__(self, problem, seed: int = 42):
        """
        Initialize GA engine.
        
        Args:
            problem: Problem instance (OneMaxProblem, KnapsackProblem, etc.)
            seed: Random seed for reproducibility
        """
        self.problem = problem
        self.seed = seed
        random.seed(seed)
    
    def run(self,
            population_size: int = 100,
            generations: int = 100,
            bitstring_length: int = 20,
            tournament_size: int = 3,
            mutation_rate: float = None,
            crossover_rate: float = 0.8,
            run_id: str = "run_001") -> RunResult:
        """
        Execute the genetic algorithm.
        
        Main algorithm loop:
        1. Initialize random population
        2. Loop for each generation:
           a. Evaluate fitness of all individuals
           b. Select best individuals
           c. Apply crossover to create offspring
           d. Apply mutation to offspring
           e. Replace population with offspring
        3. Return best solution found
        
        Args:
            population_size: Number of individuals per generation
            generations: Number of generations to run
            bitstring_length: Length of each bitstring
            tournament_size: Tournament selection size
            mutation_rate: Probability of flipping each bit
                          If None, use 1/bitstring_length
            crossover_rate: Probability of applying crossover
            run_id: Unique identifier for this run
            
        Returns:
            RunResult: Complete results with convergence history
        """
        
        start_time = time.time()
        
        # Initialize operators
        encoding = BitStringEncoding(bitstring_length)
        selection = TournamentSelection(tournament_size)
        crossover = UniformCrossover(crossover_rate)
        mutation = BitFlipMutation(
            mutation_rate or (1.0 / bitstring_length)
        )
        
        # Initialize population with random bitstrings
        population = [
            encoding.generate_random(random)
            for _ in range(population_size)
        ]
        
        # Track best solution across all generations
        best_fitness_ever = -float('inf')
        best_solution_ever = None
        generations_to_convergence = 0
        convergence_history = []
        
        # ==================== MAIN GA LOOP ====================
        for gen in range(generations):
            
            # STEP 1: EVALUATE
            # Calculate fitness for all individuals
            fitness_values = [
                self.problem.fitness(ind)
                for ind in population
            ]
            
            # STEP 2: RECORD STATISTICS
            best_idx = fitness_values.index(max(fitness_values))
            best_gen_fitness = fitness_values[best_idx]
            avg_gen_fitness = sum(fitness_values) / len(fitness_values)
            worst_gen_fitness = min(fitness_values)
            
            # Track if this is new best
            if best_gen_fitness > best_fitness_ever:
                best_fitness_ever = best_gen_fitness
                best_solution_ever = population[best_idx].copy()
                generations_to_convergence = gen
            
            # Record generation history
            convergence_history.append(GenerationStats(
                generation=gen,
                best_fitness=best_gen_fitness,
                avg_fitness=avg_gen_fitness,
                worst_fitness=worst_gen_fitness,
                best_genome=population[best_idx].copy()
            ))
            
            # STEP 3: SELECT
            # Choose individuals for reproduction
            parents = selection.select(
                population,
                fitness_values,
                population_size,
                random
            )
            
            # STEP 4: BREED (CROSSOVER)
            # Create offspring by combining parents
            offspring = []
            for i in range(0, len(parents), 2):
                if i + 1 < len(parents):
                    # Crossover with probability crossover_rate
                    if random.random() < crossover_rate:
                        child1, child2 = crossover.crossover(
                            parents[i],
                            parents[i + 1],
                            random
                        )
                        offspring.extend([child1, child2])
                    else:
                        # No crossover, copy parents
                        offspring.extend([parents[i], parents[i + 1]])
                else:
                    # Odd number of parents
                    offspring.append(parents[i])
            
            # STEP 5: MUTATE
            # Apply mutation to offspring
            offspring = [
                mutation.mutate(ind, random)
                for ind in offspring
            ]
            
            # STEP 6: REPLACE
            # Replace old population with new offspring
            population = offspring[:population_size]
        
        # ==================== END OF LOOP ====================
        
        execution_time = time.time() - start_time
        
        # Return complete results
        return RunResult(
            run_id=run_id,
            best_fitness=best_fitness_ever,
            best_solution=best_solution_ever,
            generations_to_convergence=generations_to_convergence,
            total_generations=generations,
            convergence_history=convergence_history,
            execution_time_seconds=execution_time
        )