# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Problems/src/neurosim_problems/onemax.py
# NeuroSim/Engine/bitga/problems/onemax.py
"""
OneMax Problem
Maximize the number of 1s in a bitstring
"""

from typing import List
from .base import BaseProblem

class OneMaxProblem(BaseProblem):
    """
    OneMax Problem: Count the number of 1s.
    
    Simple baseline problem. Good for testing.
    Optimal solution: All 1s
    """
    
    def __init__(self, length: int):
        """
        Initialize OneMax problem.
        
        Args:
            length: Length of bitstring
        """
        if length <= 0:
            raise ValueError("Length must be positive")
        
        self.length = length
        self.optimal_fitness = length
    
    def fitness(self, bitstring: List[int]) -> float:
        """
        Evaluate fitness: count number of 1s.
        
        Args:
            bitstring: Candidate solution
            
        Returns:
            fitness: Number of 1s in the bitstring
        """
        if len(bitstring) != self.length:
            raise ValueError(
                f"Bitstring length {len(bitstring)} != expected {self.length}"
            )
        
        # Simple: count 1s
        return sum(bitstring)
    
    def is_optimal(self, bitstring: List[int], tolerance: float = 0) -> bool:
        """
        Check if solution is optimal (all or near-all 1s).
        
        Args:
            bitstring: Candidate solution
            tolerance: How many bits can be 0
            
        Returns:
            is_optimal: True if fitness >= (optimal - tolerance)
        """
        return self.fitness(bitstring) >= (self.optimal_fitness - tolerance)