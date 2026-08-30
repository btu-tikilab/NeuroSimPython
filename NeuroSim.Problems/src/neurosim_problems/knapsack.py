# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Problems/src/neurosim_problems/knapsack.py
# NeuroSim/Engine/bitga/problems/knapsack.py
"""
0/1 Knapsack Problem
Maximize value while respecting weight constraint
"""

from typing import List
from .base import BaseProblem

class KnapsackProblem(BaseProblem):
    """
    0/1 Knapsack: Select items to maximize value within weight limit.
    
    Each bit represents: 1=include item, 0=exclude item
    """
    
    def __init__(self, values: List[float], weights: List[float], capacity: float):
        """
        Initialize knapsack problem.
        
        Args:
            values: Value of each item
            weights: Weight of each item
            capacity: Weight capacity of knapsack
        """
        if len(values) != len(weights):
            raise ValueError("values and weights must have same length")
        
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        
        self.values = values
        self.weights = weights
        self.capacity = capacity
        self.num_items = len(values)
    
    def fitness(self, bitstring: List[int], penalty: float = 1000) -> float:
        """
        Evaluate fitness: value maximization with weight penalty.
        
        Algorithm:
        1. Calculate total value of selected items
        2. Calculate total weight of selected items
        3. If weight > capacity, penalize heavily
        
        Args:
            bitstring: Which items to include
            penalty: Penalty for violating weight constraint
            
        Returns:
            fitness: Total value (penalized if infeasible)
        """
        
        if len(bitstring) != self.num_items:
            raise ValueError(
                f"Bitstring length {len(bitstring)} != "
                f"num_items {self.num_items}"
            )
        
        # Calculate total value and weight
        total_value = 0
        total_weight = 0
        
        for i in range(self.num_items):
            if bitstring[i] == 1:  # Item included
                total_value += self.values[i]
                total_weight += self.weights[i]
        
        # Penalize if over capacity
        if total_weight > self.capacity:
            # Large penalty to make infeasible solutions worse
            penalty_amount = penalty * (total_weight - self.capacity)
            return max(0, total_value - penalty_amount)
        
        # Feasible: return value
        return total_value
    
    def is_optimal(self, bitstring: List[int], tolerance: float = 0) -> bool:
        """
        Check if solution is feasible (within weight constraint).
        
        Args:
            bitstring: Candidate solution
            tolerance: Allowed weight overage
            
        Returns:
            is_optimal: True if feasible
        """
        total_weight = sum(
            self.weights[i] * bitstring[i] 
            for i in range(self.num_items)
        )
        return total_weight <= (self.capacity + tolerance)