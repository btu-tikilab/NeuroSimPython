# NeuroSim.Problems/tests/test_knapsack.py
import itertools

import pytest

from neurosim_problems import KnapsackProblem


class TestKnapsackInit:
    def test_valid_construction(self):
        p = KnapsackProblem(values=[10, 20], weights=[5, 10], capacity=15)
        assert p.num_items == 2

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError, match="same length"):
            KnapsackProblem(values=[10, 20, 30], weights=[5, 10], capacity=15)

    @pytest.mark.parametrize("bad_capacity", [0, -1, -100])
    def test_non_positive_capacity_raises(self, bad_capacity):
        with pytest.raises(ValueError, match="positive"):
            KnapsackProblem(values=[10], weights=[5], capacity=bad_capacity)

    def test_negative_value_raises(self):
        with pytest.raises(ValueError, match="values must be non-negative"):
            KnapsackProblem(values=[10, -5], weights=[5, 5], capacity=10)

    def test_negative_weight_raises(self):
        with pytest.raises(ValueError, match="weights must be non-negative"):
            KnapsackProblem(values=[10, 5], weights=[5, -5], capacity=10)

    def test_zero_value_or_weight_allowed(self):
        # zero is non-negative, should not raise
        KnapsackProblem(values=[0, 10], weights=[0, 5], capacity=10)


class TestKnapsackFitness:
    def test_feasible_solution_returns_total_value(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        assert p.fitness([1, 0, 1]) == 40  # items 0+2: weight 20, value 40

    def test_infeasible_solution_is_penalized(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=10)
        # all items: weight 30 > capacity 10 -- should be penalized below the raw value
        fitness = p.fitness([1, 1, 1])
        assert fitness < 60  # raw sum would be 60
        assert fitness >= 0  # never goes negative (clamped by max(0, ...))

    def test_wrong_length_raises(self):
        p = KnapsackProblem(values=[10, 20], weights=[5, 10], capacity=15)
        with pytest.raises(ValueError, match="!="):
            p.fitness([1, 1, 1])

    def test_empty_selection_has_zero_value(self):
        p = KnapsackProblem(values=[10, 20], weights=[5, 10], capacity=15)
        assert p.fitness([0, 0]) == 0


class TestKnapsackIsOptimalLaziness:
    def test_optimal_value_not_computed_until_first_call(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        assert p._optimal_value_cache is None

    def test_cache_populated_after_is_optimal_call(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        p.is_optimal([1, 0, 0])
        assert p._optimal_value_cache is not None

    def test_cache_reused_on_subsequent_calls(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        p.is_optimal([1, 0, 0])
        first = p._optimal_value_cache
        p.is_optimal([0, 1, 0])
        assert p._optimal_value_cache == first


class TestKnapsackIsOptimalCorrectness:
    def test_true_optimum_reported_as_optimal(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        assert p.is_optimal([1, 0, 1]) is True  # value 40, the true optimum

    def test_infeasible_is_never_optimal(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        assert p.is_optimal([1, 1, 1]) is False  # weight 30 > capacity 20

    def test_feasible_but_suboptimal_is_not_optimal(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        assert p.is_optimal([1, 0, 0]) is False  # value 10, feasible but not the best

    def test_empty_selection_is_feasible_but_not_optimal(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        assert p.is_optimal([0, 0, 0]) is False  # this was the original bug we fixed

    def test_tolerance_allows_near_optimal(self):
        p = KnapsackProblem(values=[10, 20, 30], weights=[5, 10, 15], capacity=20)
        # value 30 (item 2 alone) is 10 below the true optimum of 40
        assert p.is_optimal([0, 0, 1], tolerance=10) is True
        assert p.is_optimal([0, 0, 1], tolerance=5) is False

    def test_dp_handles_zero_weight_items(self):
        """A zero-weight item is always worth including -- exercises the
        'weight <= 0' special case in the DP solver directly."""
        # item 0: free, worth 100; item 1: costs all the capacity, worth 5
        p = KnapsackProblem(values=[100, 5], weights=[0, 10], capacity=10)
        # true optimum: take both (free item + the only other item that fits)
        assert p._get_optimal_value() == 105

    @pytest.mark.parametrize("values,weights,capacity", [
        ([6, 10, 12], [1, 2, 3], 5),
        ([1, 4, 5, 7], [1, 3, 4, 5], 7),
        ([10, 20, 30, 40, 50], [5, 10, 15, 20, 25], 50),
        ([100, 5, 8], [0, 3, 4], 5),  # includes a free (zero-weight) item
    ])
    def test_dp_matches_brute_force(self, values, weights, capacity):
        """Cross-check the DP-based optimum against a brute-force search
        over every possible bitstring, for several small instances."""
        n = len(values)
        best_bf = 0
        for bits in itertools.product([0, 1], repeat=n):
            w = sum(b * wt for b, wt in zip(bits, weights))
            v = sum(b * val for b, val in zip(bits, values))
            if w <= capacity and v > best_bf:
                best_bf = v

        p = KnapsackProblem(values, weights, capacity)
        assert p._get_optimal_value() == best_bf