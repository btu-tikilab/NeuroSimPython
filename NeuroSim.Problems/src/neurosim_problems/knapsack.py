# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Problems/src/neurosim_problems/knapsack.py
# NeuroSim/Engine/bitga/problems/knapsack.py
"""
0/1 Knapsack Problem
Maximize value while respecting weight constraint
"""

from typing import List, Optional
from .base import BaseProblem

class KnapsackProblem(BaseProblem):
    """
    0/1 Knapsack: Select items to maximize value within weight limit.

    Each bit represents: 1=include item, 0=exclude item
    """

    def __init__(self, values: List[float], weights: List[float], capacity: float):
        """
        Initialize a Knapsack instance from items and a capacity.
        """
        if len(values) != len(weights):
            raise ValueError("values and weights must have same length")

        if capacity <= 0:
            raise ValueError("capacity must be positive")

        if any(v < 0 for v in values):
            raise ValueError("values must be non-negative")

        if any(w < 0 for w in weights):
            raise ValueError("weights must be non-negative")

        self.values = values
        self.weights = weights
        self.capacity = capacity
        self.num_items = len(values)

        # Computed lazily by _get_optimal_value() on first use, not here --
        # the DP solve costs O(num_items * capacity) and most callers
        # (the engine, the API) never call is_optimal() at all.
        self._optimal_value_cache: Optional[float] = None

    def fitness(self, bitstring: List[int], penalty: float = 1000) -> float:
        """
        Score a candidate: total value if feasible, penalized if over capacity.
        """
        if len(bitstring) != self.num_items:
            raise ValueError(
                f"Bitstring length {len(bitstring)} != "
                f"num_items {self.num_items}"
            )

        total_value = 0
        total_weight = 0

        for i in range(self.num_items):
            if bitstring[i] == 1:
                total_value += self.values[i]
                total_weight += self.weights[i]

        if total_weight > self.capacity:
            penalty_amount = penalty * (total_weight - self.capacity)
            return max(0, total_value - penalty_amount)

        return total_value

    def _get_optimal_value(self) -> float:
        """
        Return the true optimal value for this instance, computing and
        caching it via DP on first call. Subsequent calls are free.
        """
        if self._optimal_value_cache is None:
            self._optimal_value_cache = self._solve_optimal_value()
        return self._optimal_value_cache

    def _solve_optimal_value(self) -> float:
        """
        Exact 0/1 knapsack solve via dynamic programming.

        NOTE: the DP table is indexed by weight, which requires
        integer units. weights/capacity are rounded to the nearest
        integer for THIS computation only -- fitness() above still
        uses the exact float values.
        """
        capacity_units = int(round(self.capacity))
        weights_units = [int(round(w)) for w in self.weights]

        dp = [0.0] * (capacity_units + 1)

        for value, weight in zip(self.values, weights_units):
            if weight <= 0:
                dp = [d + value for d in dp]
                continue
            for w in range(capacity_units, weight - 1, -1):
                candidate = dp[w - weight] + value
                if candidate > dp[w]:
                    dp[w] = candidate

        return dp[capacity_units]

    def is_optimal(self, bitstring: List[int], tolerance: float = 0) -> bool:
        """
        Check if solution is feasible AND within `tolerance` of the
        true optimal value for this instance.
        """
        total_weight = sum(
            self.weights[i] * bitstring[i]
            for i in range(self.num_items)
        )
        if total_weight > self.capacity:
            return False

        total_value = sum(
            self.values[i] * bitstring[i]
            for i in range(self.num_items)
        )
        return total_value >= (self._get_optimal_value() - tolerance)