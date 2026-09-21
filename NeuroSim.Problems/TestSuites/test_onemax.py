# NeuroSim.Problems/tests/test_onemax.py
import pytest

from neurosim_problems import OneMaxProblem


class TestOneMaxInit:
    def test_valid_length(self):
        p = OneMaxProblem(length=10)
        assert p.length == 10
        assert p.optimal_fitness == 10

    @pytest.mark.parametrize("bad_length", [0, -1, -50])
    def test_non_positive_length_raises(self, bad_length):
        with pytest.raises(ValueError, match="positive"):
            OneMaxProblem(length=bad_length)


class TestOneMaxFitness:
    def test_counts_ones(self):
        p = OneMaxProblem(length=5)
        assert p.fitness([1, 1, 1, 1, 1]) == 5
        assert p.fitness([0, 0, 0, 0, 0]) == 0
        assert p.fitness([1, 0, 1, 0, 1]) == 3

    def test_wrong_length_raises(self):
        p = OneMaxProblem(length=5)
        with pytest.raises(ValueError, match="!="):
            p.fitness([1, 1, 1])


class TestOneMaxIsOptimal:
    def test_all_ones_is_optimal(self):
        p = OneMaxProblem(length=6)
        assert p.is_optimal([1, 1, 1, 1, 1, 1]) is True

    def test_not_all_ones_is_not_optimal(self):
        p = OneMaxProblem(length=6)
        assert p.is_optimal([1, 1, 1, 1, 1, 0]) is False

    def test_tolerance_allows_near_optimal(self):
        p = OneMaxProblem(length=10)
        # 8 ones, 2 zeros -- within tolerance=2 of the optimum (10)
        assert p.is_optimal([1] * 8 + [0] * 2, tolerance=2) is True
        assert p.is_optimal([1] * 8 + [0] * 2, tolerance=1) is False