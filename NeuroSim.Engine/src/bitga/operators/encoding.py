# NeuroSim/Engine/bitga/operators/encoding.py
"""
Bitstring Encoding/Decoding
Converts between problem representations and bitstrings
"""

from typing import List

from core.base_encoding import BaseEncoding


class BitStringEncoding(BaseEncoding):
    """Convert between problem data and bitstrings."""
    
    def __init__(self, length: int):
        """
        Initialize bitstring encoding.
        
        Args:
            length: Number of bits in the bitstring
        """
        if length <= 0:
            raise ValueError("Length must be positive")
        
        self.length = length
    
    def encode(self, solution) -> List[int]:
        """
        Convert problem solution to bitstring.
        
        For simple problems like OneMax, this is identity function.
        For complex problems, would implement custom logic.
        
        Args:
            solution: Problem-specific solution (list or tuple)
            
        Returns:
            bitstring: List of 0s and 1s
        """
        if not isinstance(solution, (list, tuple)):
            raise ValueError("Solution must be list or tuple")
        
        if len(solution) != self.length:
            raise ValueError(
                f"Solution length {len(solution)} != expected {self.length}"
            )
        
        # Validate all are bits
        for bit in solution:
            if bit not in [0, 1]:
                raise ValueError(f"Invalid bit value: {bit} (must be 0 or 1)")
        
        return list(solution)
    
    def decode(self, bitstring: List[int]):
        """
        Convert bitstring to problem solution.
        
        Args:
            bitstring: List of 0s and 1s
            
        Returns:
            solution: Problem-specific solution
        """
        return self.encode(bitstring)  # For simple problems, same as encode
    
    def generate_random(self, rng) -> List[int]:
        """
        Generate random bitstring using seeded RNG.
        
        Args:
            rng: Seeded random number generator
            
        Returns:
            bitstring: Random list of 0s and 1s
        """
        return [rng.randint(0, 1) for _ in range(self.length)]