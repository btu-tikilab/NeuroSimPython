# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Problems/TestSuites/test_problems.py
# NeuroSim.Engine/tests/test_problems.py
"""
Unit tests for problems
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from neurosim_problems import OneMaxProblem, KnapsackProblem

class TestOneMax:
    """Test OneMax problem."""
    
    def test_onemax_fitness_all_zeros(self):
        problem = OneMaxProblem(length=10)
        
        fitness = problem.fitness([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        
        assert fitness == 0
    
    def test_onemax_fitness_all_ones(self):
        problem = OneMaxProblem(length=10)
        
        fitness = problem.fitness([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        
        assert fitness == 10
    
    def test_onemax_fitness_mixed(self):
        problem = OneMaxProblem(length=10)
        
        fitness = problem.fitness([1, 0, 1, 0, 1, 0, 0, 0, 0, 0])
        
        assert fitness == 3
    
    def test_onemax_optimal(self):
        problem = OneMaxProblem(length=10)
        
        assert problem.is_optimal([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        assert not problem.is_optimal([1, 0, 1, 0, 1, 0, 0, 0, 0, 0])
    
    def test_onemax_optimal_with_tolerance(self):
        problem = OneMaxProblem(length=10)
        
        assert problem.is_optimal([1, 1, 1, 1, 1, 1, 1, 1, 1, 0], tolerance=1)

class TestKnapsack:
    """Test Knapsack problem."""
    
    def test_knapsack_fitness_empty(self):
        values = [10, 20, 30]
        weights = [5, 10, 15]
        capacity = 30
        problem = KnapsackProblem(values, weights, capacity)
        
        fitness = problem.fitness([0, 0, 0])
        
        assert fitness == 0
    
    def test_knapsack_fitness_single_item(self):
        values = [10, 20, 30]
        weights = [5, 10, 15]
        capacity = 30
        problem = KnapsackProblem(values, weights, capacity)
        
        fitness = problem.fitness([1, 0, 0])
        
        assert fitness == 10
    
    def test_knapsack_fitness_all_items(self):
        values = [10, 20, 30]
        weights = [5, 10, 15]
        capacity = 50
        problem = KnapsackProblem(values, weights, capacity)
        
        fitness = problem.fitness([1, 1, 1])
        
        assert fitness == 60
    
    def test_knapsack_fitness_overage_penalty(self):
        values = [10, 20, 30]
        weights = [5, 10, 15]
        capacity = 20
        problem = KnapsackProblem(values, weights, capacity)
        
        fitness = problem.fitness([1, 1, 1], penalty=100)
        
        assert fitness == 0
    
    def test_knapsack_feasible(self):
        values = [10, 20, 30]
        weights = [5, 10, 15]
        capacity = 30
        problem = KnapsackProblem(values, weights, capacity)
        
        assert problem.is_optimal([1, 1, 1])