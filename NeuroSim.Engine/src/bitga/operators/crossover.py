# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/operators/crossover.py
# NeuroSim/Engine/bitga/operators/crossover.py
"""
Crossover Operators
Combine genetic material from two parents to create offspring
"""

from typing import List, Tuple

from core.base_crossover import BaseCrossover


class UniformCrossover(BaseCrossover):
    """Uniform crossover - each bit from either parent."""
    
    def __init__(self, crossover_probability: float = 0.5):
        """
        Initialize uniform crossover.
        
        Args:
            crossover_probability: Probability that bit comes from parent1
                                  (1 - this = comes from parent2)
        """
        if not 0 <= crossover_probability <= 1:
            raise ValueError(
                f"crossover_probability must be 0-1, got {crossover_probability}"
            )
        
        self.crossover_probability = crossover_probability
    
    def crossover(self, 
                  parent1: List[int], 
                  parent2: List[int], 
                  rng) -> Tuple[List[int], List[int]]:
        """
        Create two offspring from two parents.
        
        Algorithm:
        For each bit position:
        1. With probability p_c, take from parent1
        2. Otherwise, take from parent2
        3. Do opposite for second offspring
        
        Args:
            parent1: First parent bitstring
            parent2: Second parent bitstring
            rng: Seeded random number generator
            
        Returns:
            (offspring1, offspring2): Two new bitstrings
        """
        
        # Validate inputs
        if len(parent1) != len(parent2):
            raise ValueError(
                f"Parent lengths must match: {len(parent1)} vs {len(parent2)}"
            )
        
        offspring1 = []
        offspring2 = []
        
        # For each bit position
        for i in range(len(parent1)):
            # Decide which parent to inherit from
            if rng.random() < self.crossover_probability:
                # Inherit from parent1
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
            else:
                # Inherit from parent2
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])
        
        return offspring1, offspring2