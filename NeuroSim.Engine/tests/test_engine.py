# NeuroSim.Engine/tests/test_engine.py
"""
Integration tests for the GA engine
"""
import sys
from pathlib import Path

# Better approach - ensure package is installed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "NeuroSim.Engine" / "src"))

from neurosim_engine.bitga.engine import BitGAEngine
from neurosim_problems import OneMaxProblem, KnapsackProblem

class TestBitGAEngine:
    """Test BitGA Engine."""
    
    def test_engine_onemax_basic(self):
        """Test engine runs on OneMax."""
        problem = OneMaxProblem(length=20)
        engine = BitGAEngine(problem, seed=42)
        
        result = engine.run(
            population_size=50,
            generations=50,
            bitstring_length=20,
            tournament_size=3,
            run_id="test_001"
        )
        
        assert result.run_id == "test_001"
        assert result.best_fitness > 0
        assert len(result.best_solution) == 20
        assert result.total_generations == 50
        assert len(result.convergence_history) == 50
        assert result.execution_time_seconds > 0
    
    def test_engine_onemax_convergence(self):
        """Test that engine converges on OneMax."""
        problem = OneMaxProblem(length=20)
        engine = BitGAEngine(problem, seed=42)
        
        result = engine.run(
            population_size=100,
            generations=100,
            bitstring_length=20,
            tournament_size=3
        )
        
        assert result.best_fitness >= 15, \
            f"Fitness {result.best_fitness} too low"
    
    def test_engine_reproducibility(self):
        """Same seed → same results."""
        problem1 = OneMaxProblem(length=15)
        engine1 = BitGAEngine(problem1, seed=42)
        result1 = engine1.run(
            population_size=30,
            generations=20,
            bitstring_length=15
        )
        
        problem2 = OneMaxProblem(length=15)
        engine2 = BitGAEngine(problem2, seed=42)
        result2 = engine2.run(
            population_size=30,
            generations=20,
            bitstring_length=15
        )
        
        assert result1.best_fitness == result2.best_fitness
        assert result1.best_solution == result2.best_solution
    
    def test_engine_convergence_history(self):
        """Check convergence history is recorded correctly."""
        problem = OneMaxProblem(length=10)
        engine = BitGAEngine(problem, seed=42)
        
        result = engine.run(
            population_size=20,
            generations=10,
            bitstring_length=10
        )
        
        assert len(result.convergence_history) == 10
        
        for i, stat in enumerate(result.convergence_history):
            assert stat.generation == i
            assert stat.best_fitness >= stat.avg_fitness
            assert stat.avg_fitness >= stat.worst_fitness
            assert len(stat.best_genome) == 10
    
    def test_engine_knapsack(self):
        """Test engine on Knapsack problem."""
        values = [10, 20, 30, 40, 50]
        weights = [5, 10, 15, 20, 25]
        capacity = 50
        problem = KnapsackProblem(values, weights, capacity)
        
        engine = BitGAEngine(problem, seed=42)
        
        result = engine.run(
            population_size=50,
            generations=50,
            bitstring_length=5,
            tournament_size=3
        )
        
        assert result.best_fitness > 0
        assert problem.is_optimal(result.best_solution, tolerance=10)
    
    def test_engine_different_params(self):
        """Test with different parameters."""
        problem = OneMaxProblem(length=10)
        
        engine1 = BitGAEngine(problem, seed=42)
        result1 = engine1.run(
            population_size=10,
            generations=20,
            bitstring_length=10
        )
        
        engine2 = BitGAEngine(problem, seed=42)
        result2 = engine2.run(
            population_size=100,
            generations=20,
            bitstring_length=10
        )
        
        assert result1.best_fitness > 0
        assert result2.best_fitness > 0