# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/tests/test_operators.py
# NeuroSim.Engine/tests/test_operators.py
"""
Unit tests for operators
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import random
import pytest

from src import (
    BitStringEncoding,
    TournamentSelection,
    UniformCrossover,
    BitFlipMutation
)

class TestEncoding:
    """Test BitStringEncoding."""
    
    def test_encode_simple(self):
        encoding = BitStringEncoding(length=5)
        solution = [1, 0, 1, 0, 1]
        result = encoding.encode(solution)
        assert result == [1, 0, 1, 0, 1]
    
    def test_decode_simple(self):
        encoding = BitStringEncoding(length=5)
        bitstring = [1, 0, 1, 0, 1]
        result = encoding.decode(bitstring)
        assert result == [1, 0, 1, 0, 1]
    
    def test_encode_wrong_length(self):
        encoding = BitStringEncoding(length=5)
        with pytest.raises(ValueError):
            encoding.encode([1, 0, 1])
    
    def test_encode_invalid_bit(self):
        encoding = BitStringEncoding(length=5)
        with pytest.raises(ValueError):
            encoding.encode([1, 0, 2, 0, 1])
    
    def test_generate_random(self):
        encoding = BitStringEncoding(length=20)
        random.seed(42)
        bitstring = encoding.generate_random(random)
        
        assert len(bitstring) == 20
        assert all(b in [0, 1] for b in bitstring)
    
    def test_reproducibility(self):
        encoding = BitStringEncoding(length=30)
        
        random.seed(42)
        bits1 = encoding.generate_random(random)
        
        random.seed(42)
        bits2 = encoding.generate_random(random)
        
        assert bits1 == bits2

class TestSelection:
    """Test TournamentSelection."""
    
    def test_select_basic(self):
        selection = TournamentSelection(tournament_size=3)
        
        population = [[1,0,1,0], [0,1,1,0], [1,1,0,0], [1,1,1,0]]
        fitness = [2, 1, 1, 3]
        
        random.seed(42)
        parents = selection.select(population, fitness, 10, random)
        
        assert len(parents) == 10
        assert all(p in population for p in parents)
    
    def test_selection_reproducibility(self):
        selection = TournamentSelection(tournament_size=3)
        
        population = [[1,0,1,0], [0,1,1,0], [1,1,0,0]]
        fitness = [2, 1, 3]
        
        random.seed(42)
        parents1 = selection.select(population, fitness, 20, random)
        
        random.seed(42)
        parents2 = selection.select(population, fitness, 20, random)
        
        assert parents1 == parents2
    
    def test_selection_pressure(self):
        """Best individual should be selected more often."""
        selection = TournamentSelection(tournament_size=3)
        
        population = [[1,0,1,0], [0,0,0,0], [1,1,1,1]]
        fitness = [2, 0, 4]
        
        random.seed(42)
        parents = selection.select(population, fitness, 100, random)
        
        best = population[2]
        count = sum(1 for p in parents if p == best)
        
        assert count > 30

class TestCrossover:
    """Test UniformCrossover."""
    
    def test_crossover_basic(self):
        crossover = UniformCrossover(crossover_probability=0.5)
        
        parent1 = [1, 0, 1, 0, 1]
        parent2 = [0, 1, 0, 1, 0]
        
        random.seed(42)
        off1, off2 = crossover.crossover(parent1, parent2, random)
        
        assert len(off1) == 5
        assert len(off2) == 5
        assert all(b in [0, 1] for b in off1)
        assert all(b in [0, 1] for b in off2)
    
    def test_crossover_reproducibility(self):
        crossover = UniformCrossover(crossover_probability=0.5)
        
        parent1 = [1, 0, 1, 0, 1, 0, 1, 0]
        parent2 = [0, 1, 0, 1, 0, 1, 0, 1]
        
        random.seed(42)
        off1_a, off2_a = crossover.crossover(parent1, parent2, random)
        
        random.seed(42)
        off1_b, off2_b = crossover.crossover(parent1, parent2, random)
        
        assert off1_a == off1_b
        assert off2_a == off2_b
    
    def test_crossover_extreme_prob_1(self):
        crossover = UniformCrossover(crossover_probability=1.0)
        
        parent1 = [1, 1, 1, 1, 1]
        parent2 = [0, 0, 0, 0, 0]
        
        random.seed(42)
        off1, off2 = crossover.crossover(parent1, parent2, random)
        
        assert off1 == parent1
        assert off2 == parent2
    
    def test_crossover_mismatched_length(self):
        crossover = UniformCrossover(crossover_probability=0.5)
        
        parent1 = [1, 0, 1]
        parent2 = [0, 1]
        
        with pytest.raises(ValueError):
            crossover.crossover(parent1, parent2, random)

class TestMutation:
    """Test BitFlipMutation."""
    
    def test_mutation_all_flip(self):
        mutation = BitFlipMutation(mutation_rate=1.0)
        
        individual = [1, 0, 1, 0, 1]
        random.seed(42)
        mutated = mutation.mutate(individual, random)
        
        assert mutated == [0, 1, 0, 1, 0]
    
    def test_mutation_no_flip(self):
        mutation = BitFlipMutation(mutation_rate=0.0)
        
        individual = [1, 0, 1, 0, 1]
        random.seed(42)
        mutated = mutation.mutate(individual, random)
        
        assert mutated == individual
    
    def test_mutation_default_rate(self):
        length = 20
        mutation = BitFlipMutation(length=length)
        
        assert mutation.mutation_rate == 1.0 / length
    
    def test_mutation_reproducibility(self):
        mutation = BitFlipMutation(mutation_rate=0.1)
        
        individual = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        
        random.seed(42)
        mutated1 = mutation.mutate(individual, random)
        
        random.seed(42)
        mutated2 = mutation.mutate(individual, random)
        
        assert mutated1 == mutated2
    
    def test_mutation_expected_flips(self):
        """Expected flips should be L * p_m"""
        length = 100
        mutation_rate = 0.1
        mutation = BitFlipMutation(mutation_rate=mutation_rate)
        
        individual = [0] * length
        
        random.seed(42)
        mutated = mutation.mutate(individual, random)
        
        num_flips = sum(mutated)
        
        assert 7 <= num_flips <= 13