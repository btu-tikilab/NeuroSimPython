# NeuroSim.Engine/tests/bitga/test_build_engine.py
import pytest

from bitga import build_engine
from bitga.engine import BitGAEngine
from bitga.operators.crossover import UniformCrossover, SinglePointCrossover, TwoPointCrossover
from bitga.operators.mutation import BitFlipMutation, SwapMutation, InversionMutation
from neurosim_problems import OneMaxProblem


class TestBuildEngineValidation:
    def test_missing_bitstring_length_raises(self, onemax_small):
        with pytest.raises(ValueError, match="bitstring_length"):
            build_engine(onemax_small, {})

    def test_unknown_crossover_type_raises(self, onemax_small):
        with pytest.raises(ValueError, match="Unknown crossover_type"):
            build_engine(onemax_small, {"bitstring_length": 10, "crossover_type": "Nonexistent"})

    def test_unknown_mutation_type_raises(self, onemax_small):
        with pytest.raises(ValueError, match="Unknown mutation_type"):
            build_engine(onemax_small, {"bitstring_length": 10, "mutation_type": "Nonexistent"})

    def test_negative_elitism_raises(self, onemax_small):
        with pytest.raises(ValueError, match="elitism must be >= 0"):
            build_engine(onemax_small, {"bitstring_length": 10, "elitism": -1})

    @pytest.mark.parametrize("bad_elitism", [20, 25])
    def test_elitism_not_below_population_size_raises(self, onemax_small, bad_elitism):
        """elitism must leave room for at least one offspring, so it has to
        be strictly less than population_size."""
        with pytest.raises(ValueError, match="must be < population_size"):
            build_engine(onemax_small, {
                "bitstring_length": 10,
                "population_size": 20,
                "elitism": bad_elitism,
            })


class TestBuildEngineDefaults:
    def test_returns_a_bitga_engine(self, onemax_small):
        engine = build_engine(onemax_small, {"bitstring_length": 10})
        assert isinstance(engine, BitGAEngine)

    def test_default_crossover_is_uniform(self, onemax_small):
        engine = build_engine(onemax_small, {"bitstring_length": 10})
        assert isinstance(engine.crossover, UniformCrossover)

    def test_default_mutation_is_bit_flip(self, onemax_small):
        engine = build_engine(onemax_small, {"bitstring_length": 10})
        assert isinstance(engine.mutation, BitFlipMutation)

    def test_config_values_passed_through(self, onemax_small):
        engine = build_engine(onemax_small, {
            "bitstring_length": 12,
            "population_size": 33,
            "generations": 77,
            "tournament_size": 5,
            "seed": 99,
            "elitism": 4,
        })
        assert engine.population_size == 33
        assert engine.max_generations == 77
        assert engine.selection.tournament_size == 5
        assert engine.elitism == 4

    def test_default_elitism_is_zero(self, onemax_small):
        engine = build_engine(onemax_small, {"bitstring_length": 10})
        assert engine.elitism == 0


class TestBuildEngineCrossoverTypes:
    @pytest.mark.parametrize("crossover_type,expected_cls", [
        ("Uniform", UniformCrossover),
        ("Single Point", SinglePointCrossover),
        ("Two Point", TwoPointCrossover),
    ])
    def test_each_crossover_type_builds_correct_class(self, onemax_small, crossover_type, expected_cls):
        engine = build_engine(onemax_small, {"bitstring_length": 10, "crossover_type": crossover_type})
        assert isinstance(engine.crossover, expected_cls)


class TestBuildEngineMutationTypes:
    @pytest.mark.parametrize("mutation_type,expected_cls", [
        ("Bit Flip", BitFlipMutation),
        ("Swap", SwapMutation),
        ("Inversion", InversionMutation),
    ])
    def test_each_mutation_type_builds_correct_class(self, onemax_small, mutation_type, expected_cls):
        engine = build_engine(onemax_small, {"bitstring_length": 10, "mutation_type": mutation_type})
        assert isinstance(engine.mutation, expected_cls)


class TestBuildEngineEndToEnd:
    @pytest.mark.parametrize("crossover_type", ["Uniform", "Single Point", "Two Point"])
    @pytest.mark.parametrize("mutation_type", ["Bit Flip", "Swap", "Inversion"])
    def test_every_combination_runs_successfully(self, crossover_type, mutation_type):
        """All 9 crossover x mutation combinations should build and run
        without error -- this is the same matrix verified manually
        during development, now captured as a permanent regression test."""
        problem = OneMaxProblem(length=12)
        engine = build_engine(problem, {
            "bitstring_length": 12,
            "population_size": 16,
            "generations": 8,
            "seed": 7,
            "crossover_type": crossover_type,
            "mutation_type": mutation_type,
            "mutation_rate": 0.1,
        })
        best = engine.run()
        assert len(best) == 12
        assert problem.fitness(best) >= 0