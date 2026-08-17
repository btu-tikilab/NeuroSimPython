# NeuroSim/Engine/bitga/operators/mutation.py
"""
Mutation Operators
Introduce random variations to maintain population diversity
"""

from typing import List

from core.base_mutation import BaseMutation


class BitFlipMutation(BaseMutation):
    """Bit-flip mutation - randomly flip bits."""
    
    def __init__(self, mutation_rate: float = None, length: int = None):
        """
        Initialize bit-flip mutation.
        
        Args:
            mutation_rate: Probability of flipping each bit (0-1)
                          If None, calculated as 1/length
            length: Length of bitstring (needed if mutation_rate=None)
        """
        
        if mutation_rate is not None:
            # Use provided rate
            if not 0 <= mutation_rate <= 1:
                raise ValueError(
                    f"mutation_rate must be 0-1, got {mutation_rate}"
                )
            self.mutation_rate = mutation_rate
        
        elif length is not None:
            # Calculate default: 1/L
            if length <= 0:
                raise ValueError("length must be positive")
            self.mutation_rate = 1.0 / length
        
        else:
            raise ValueError("Provide either mutation_rate or length")
    
    def mutate(self, individual: List[int], rng) -> List[int]:
        """
        Apply bit-flip mutation to individual.
        
        Algorithm:
        For each bit:
        1. With probability p_m, flip the bit
        2. Otherwise, keep it unchanged
        
        Args:
            individual: Bitstring to mutate
            rng: Seeded random number generator
            
        Returns:
            mutated: Mutated bitstring
        """
        
        if not isinstance(individual, (list, tuple)):
            raise ValueError("Individual must be list or tuple")
        
        if len(individual) == 0:
            raise ValueError("Individual cannot be empty")
        
        mutated = []
        
        # For each bit
        for bit in individual:
            # Check if this bit should be flipped
            if rng.random() < self.mutation_rate:
                # Flip bit: 0→1 or 1→0
                mutated.append(1 - bit)
            else:
                # Keep bit unchanged
                mutated.append(bit)
        
        return mutated