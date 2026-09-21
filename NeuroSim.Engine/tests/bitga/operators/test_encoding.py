# NeuroSim.Engine/tests/bitga/operators/test_encoding.py
import random

import pytest

from bitga.operators.encoding import BitStringEncoding


class TestBitStringEncodingInit:
    def test_valid_length(self):
        enc = BitStringEncoding(length=10)
        assert enc.length == 10

    @pytest.mark.parametrize("bad_length", [0, -1, -100])
    def test_non_positive_length_raises(self, bad_length):
        with pytest.raises(ValueError, match="positive"):
            BitStringEncoding(length=bad_length)


class TestGenerateRandom:
    def test_returns_correct_length(self, rng):
        enc = BitStringEncoding(length=15)
        genome = enc.generate_random(rng)
        assert len(genome) == 15

    def test_all_bits_are_0_or_1(self, rng):
        enc = BitStringEncoding(length=50)
        genome = enc.generate_random(rng)
        assert all(bit in (0, 1) for bit in genome)

    def test_reproducible_with_same_seed(self):
        enc = BitStringEncoding(length=20)
        genome1 = enc.generate_random(random.Random(7))
        genome2 = enc.generate_random(random.Random(7))
        assert genome1 == genome2

    def test_different_seeds_differ(self):
        enc = BitStringEncoding(length=50)
        genome1 = enc.generate_random(random.Random(1))
        genome2 = enc.generate_random(random.Random(2))
        # Astronomically unlikely to collide at length 50 with different seeds.
        assert genome1 != genome2

    def test_length_one(self, rng):
        enc = BitStringEncoding(length=1)
        genome = enc.generate_random(rng)
        assert len(genome) == 1
        assert genome[0] in (0, 1)