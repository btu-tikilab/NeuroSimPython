# NeuroSim.Engine/tests/bitga/operators/test_mutation.py
import random

import pytest

from bitga.operators.mutation import BitFlipMutation, SwapMutation, InversionMutation


class TestBitFlipMutationInit:
    def test_valid_mutation_rate(self):
        m = BitFlipMutation(mutation_rate=0.1)
        assert m.mutation_rate == 0.1

    def test_derives_rate_from_length(self):
        m = BitFlipMutation(length=20)
        assert m.mutation_rate == pytest.approx(1.0 / 20)

    @pytest.mark.parametrize("bad_rate", [-0.1, 1.1])
    def test_out_of_range_rate_raises(self, bad_rate):
        with pytest.raises(ValueError, match="0-1"):
            BitFlipMutation(mutation_rate=bad_rate)

    def test_non_positive_length_raises(self):
        with pytest.raises(ValueError, match="positive"):
            BitFlipMutation(length=0)

    def test_neither_rate_nor_length_raises(self):
        with pytest.raises(ValueError, match="Provide either"):
            BitFlipMutation()


class TestBitFlipMutationBehavior:
    def test_output_length_matches_input(self, rng):
        m = BitFlipMutation(mutation_rate=0.1)
        result = m.mutate([0, 1, 0, 1, 0], rng)
        assert len(result) == 5

    def test_rate_zero_never_mutates(self, rng):
        m = BitFlipMutation(mutation_rate=0.0)
        original = [0, 1, 1, 0, 1, 0, 0, 1]
        result = m.mutate(original, rng)
        assert result == original

    def test_rate_one_always_flips_every_bit(self, rng):
        m = BitFlipMutation(mutation_rate=1.0)
        original = [0, 1, 1, 0, 1]
        result = m.mutate(original, rng)
        assert result == [1, 0, 0, 1, 0]

    def test_non_list_individual_raises(self, rng):
        m = BitFlipMutation(mutation_rate=0.1)
        with pytest.raises(ValueError, match="list or tuple"):
            m.mutate(None, rng)

    def test_empty_individual_raises(self, rng):
        m = BitFlipMutation(mutation_rate=0.1)
        with pytest.raises(ValueError, match="cannot be empty"):
            m.mutate([], rng)

    def test_output_only_contains_0_and_1(self, rng):
        m = BitFlipMutation(mutation_rate=0.5)
        result = m.mutate([0, 1, 0, 1, 0, 1, 0, 1], rng)
        assert all(bit in (0, 1) for bit in result)

    def test_reproducible_with_same_seed(self):
        """Ported from the legacy test_operators.py: same seed produces
        an identical mutation result at a realistic (non-extreme) rate."""
        m = BitFlipMutation(mutation_rate=0.1)
        individual = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        result1 = m.mutate(individual, random.Random(42))
        result2 = m.mutate(individual, random.Random(42))

        assert result1 == result2

    def test_expected_number_of_flips_matches_rate(self):
        """Ported from the legacy test_operators.py: with mutation_rate=0.1
        on 100 bits, the expected number of flips is ~10 -- checks the
        operator isn't systematically over- or under-flipping."""
        m = BitFlipMutation(mutation_rate=0.1)
        individual = [0] * 100

        result = m.mutate(individual, random.Random(42))
        num_flips = sum(result)

        assert 7 <= num_flips <= 13


class TestSwapMutation:
    def test_init_out_of_range_raises(self):
        with pytest.raises(ValueError, match="0-1"):
            SwapMutation(mutation_probability=1.5)

    def test_preserves_multiset_of_bits(self, rng):
        m = SwapMutation(mutation_probability=1.0)
        original = [0, 0, 0, 1, 1]
        result = m.mutate(original, random.Random(3))
        assert sorted(result) == sorted(original)

    def test_probability_zero_never_mutates(self, rng):
        m = SwapMutation(mutation_probability=0.0)
        original = [0, 1, 0, 1, 1]
        result = m.mutate(original, rng)
        assert result == original

    def test_single_element_returns_unchanged(self, rng):
        m = SwapMutation(mutation_probability=1.0)
        result = m.mutate([1], rng)
        assert result == [1]

    def test_empty_individual_raises(self, rng):
        m = SwapMutation()
        with pytest.raises(ValueError, match="cannot be empty"):
            m.mutate([], rng)


class TestInversionMutation:
    def test_init_out_of_range_raises(self):
        with pytest.raises(ValueError, match="0-1"):
            InversionMutation(mutation_probability=-0.5)

    def test_preserves_multiset_of_bits(self, rng):
        m = InversionMutation(mutation_probability=1.0)
        original = [0, 0, 1, 1, 0, 1]
        result = m.mutate(original, random.Random(5))
        assert sorted(result) == sorted(original)

    def test_probability_zero_never_mutates(self, rng):
        m = InversionMutation(mutation_probability=0.0)
        original = [0, 1, 0, 1, 1]
        result = m.mutate(original, rng)
        assert result == original

    def test_single_element_returns_unchanged(self, rng):
        m = InversionMutation(mutation_probability=1.0)
        result = m.mutate([1], rng)
        assert result == [1]

    def test_empty_individual_raises(self, rng):
        m = InversionMutation()
        with pytest.raises(ValueError, match="cannot be empty"):
            m.mutate([], rng)