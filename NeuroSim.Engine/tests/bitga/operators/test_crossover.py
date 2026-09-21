# NeuroSim.Engine/tests/bitga/operators/test_crossover.py
import random

import pytest

from bitga.operators.crossover import (
    UniformCrossover,
    SinglePointCrossover,
    TwoPointCrossover,
)


class TestUniformCrossoverInit:
    def test_valid_probability(self):
        cx = UniformCrossover(crossover_probability=0.5)
        assert cx.crossover_probability == 0.5

    @pytest.mark.parametrize("bad_p", [-0.1, 1.1, 2.0, -1.0])
    def test_out_of_range_probability_raises(self, bad_p):
        with pytest.raises(ValueError, match="0-1"):
            UniformCrossover(crossover_probability=bad_p)

    @pytest.mark.parametrize("edge_p", [0.0, 1.0])
    def test_boundary_probabilities_allowed(self, edge_p):
        UniformCrossover(crossover_probability=edge_p)


class TestUniformCrossoverBehavior:
    def test_offspring_length_matches_parents(self, rng):
        cx = UniformCrossover(0.5)
        c1, c2 = cx.crossover([0, 1, 0, 1], [1, 0, 1, 0], rng)
        assert len(c1) == 4
        assert len(c2) == 4

    def test_mismatched_parent_lengths_raises(self, rng):
        cx = UniformCrossover(0.5)
        with pytest.raises(ValueError, match="must match"):
            cx.crossover([0, 1, 0], [1, 0], rng)

    @pytest.mark.parametrize("bad_parent", [None, 123, "abc"])
    def test_non_list_parent1_raises(self, rng, bad_parent):
        cx = UniformCrossover(0.5)
        with pytest.raises(ValueError, match="parent1 must be list or tuple"):
            cx.crossover(bad_parent, [1, 0], rng)

    @pytest.mark.parametrize("bad_parent", [None, 123, "abc"])
    def test_non_list_parent2_raises(self, rng, bad_parent):
        cx = UniformCrossover(0.5)
        with pytest.raises(ValueError, match="parent2 must be list or tuple"):
            cx.crossover([1, 0], bad_parent, rng)

    def test_probability_1_clones_parent1_into_offspring1(self):
        cx = UniformCrossover(crossover_probability=1.0)
        p1, p2 = [1, 1, 1, 1], [0, 0, 0, 0]
        c1, c2 = cx.crossover(p1, p2, random.Random(1))
        assert c1 == p1
        assert c2 == p2

    def test_probability_0_swaps_parents_entirely(self):
        cx = UniformCrossover(crossover_probability=0.0)
        p1, p2 = [1, 1, 1, 1], [0, 0, 0, 0]
        c1, c2 = cx.crossover(p1, p2, random.Random(1))
        assert c1 == p2
        assert c2 == p1

    def test_every_offspring_bit_comes_from_one_of_the_two_parents(self, rng):
        cx = UniformCrossover(0.5)
        p1, p2 = [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]
        c1, c2 = cx.crossover(p1, p2, rng)
        for i in range(5):
            assert c1[i] in (p1[i], p2[i])
            assert c2[i] in (p1[i], p2[i])
            assert c1[i] != c2[i]

    def test_reproducible_with_same_seed(self):
        """Ported from the legacy test_operators.py: same seed produces
        identical offspring."""
        cx = UniformCrossover(crossover_probability=0.5)
        p1, p2 = [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1]

        c1a, c2a = cx.crossover(p1, p2, random.Random(42))
        c1b, c2b = cx.crossover(p1, p2, random.Random(42))

        assert c1a == c1b
        assert c2a == c2b


class TestSinglePointCrossover:
    def test_offspring_length_matches_parents(self, rng):
        cx = SinglePointCrossover()
        c1, c2 = cx.crossover([0, 1, 0, 1, 0], [1, 0, 1, 0, 1], rng)
        assert len(c1) == 5
        assert len(c2) == 5

    def test_genome_too_short_raises(self, rng):
        cx = SinglePointCrossover()
        with pytest.raises(ValueError, match=">= 2"):
            cx.crossover([1], [0], rng)

    def test_mismatched_lengths_raises(self, rng):
        cx = SinglePointCrossover()
        with pytest.raises(ValueError, match="must match"):
            cx.crossover([0, 1, 0], [1, 0], rng)

    def test_single_cut_produces_complementary_offspring(self, rng):
        cx = SinglePointCrossover()
        p1, p2 = [0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1]
        c1, c2 = cx.crossover(p1, p2, rng)
        for i in range(6):
            assert {c1[i], c2[i]} == {0, 1}
        switches = sum(1 for i in range(5) if c1[i] != c1[i + 1])
        assert switches <= 1


class TestTwoPointCrossover:
    def test_offspring_length_matches_parents(self, rng):
        cx = TwoPointCrossover()
        c1, c2 = cx.crossover([0, 1, 0, 1, 0], [1, 0, 1, 0, 1], rng)
        assert len(c1) == 5
        assert len(c2) == 5

    def test_genome_too_short_raises(self, rng):
        cx = TwoPointCrossover()
        with pytest.raises(ValueError, match=">= 3"):
            cx.crossover([1, 0], [0, 1], rng)

    def test_mismatched_lengths_raises(self, rng):
        cx = TwoPointCrossover()
        with pytest.raises(ValueError, match="must match"):
            cx.crossover([0, 1, 0], [1, 0], rng)

    def test_offspring_are_complementary(self, rng):
        cx = TwoPointCrossover()
        p1, p2 = [0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1]
        c1, c2 = cx.crossover(p1, p2, rng)
        for i in range(6):
            assert {c1[i], c2[i]} == {0, 1}