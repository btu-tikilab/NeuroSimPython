# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Problems/src/neurosim_problems/base.py
# NeuroSim/Engine/bitga/problems/base.py
"""
Base Problem Class
Abstract base for all optimization problems
"""

from abc import ABC, abstractmethod
from typing import List

class BaseProblem(ABC):
    """Abstract base class for all problems."""
    
    @abstractmethod
    def fitness(self, bitstring: List[int]) -> float:
        """
        Evaluate fitness of a solution.
        
        Args:
            bitstring: Candidate solution
            
        Returns:
            fitness: Fitness value (higher is better)
        """
        pass
    
    @abstractmethod
    def is_optimal(self, bitstring: List[int], tolerance: float = 0) -> bool:
        """
        Check if solution is optimal.
        
        Args:
            bitstring: Candidate solution
            tolerance: How close to optimal is acceptable
            
        Returns:
            is_optimal: True if solution is optimal
        """
        pass