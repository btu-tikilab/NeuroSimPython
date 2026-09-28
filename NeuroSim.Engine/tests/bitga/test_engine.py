# NeuroSim.Engine/tests/bitga/test_engine.py
import pytest

from bitga.engine import BitGAEngine
from bitga.operators.crossover import SinglePointCrossover
from bitga.operators.mutation import SwapMutation
from neurosim_problems import OneMaxProblem, KnapsackProblem


class TestInitialize:
    def test_creates_correct_population_size(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=25, bitstring_length=10, seed=1)
        population = engine.initialize()
        assert len(population) == 25

    def test_each_genome_has_correct_length(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=10, bitstring_length=10, seed=1)
        population = engine.initialize()
        assert all(len(genome) == 10 for genome in population)

    def test_genomes_are_binary(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=10, bitstring_length=10, seed=1)
        population = engine.initialize()
        assert all(bit in (0, 1) for genome in population for bit in genome)


class TestEvaluate:
    def test_sets_fitness_values(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=5, bitstring_length=10, seed=1)
        population = [[1] * 10, [0] * 10, [1, 0] * 5, [0, 1] * 5, [1] * 5 + [0] * 5]
        engine.evaluate(population)
        assert engine.fitness_values == [10, 0, 5, 5, 5]

    def test_returns_population_unchanged(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=2, bitstring_length=10, seed=1)
        population = [[1] * 10, [0] * 10]
        result = engine.evaluate(population)
        assert result == population
        assert result is population  # same object, not a copy


class TestSelect:
    def test_returns_population_size_parents(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=8, bitstring_length=10, tournament_size=2, seed=1)
        population = engine.initialize()
        engine.evaluate(population)
        parents = engine.select(population)
        assert len(parents) == 8


class TestBreed:
    def test_produces_population_size_offspring_when_even(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=10, bitstring_length=10, seed=1)
        parents = [[i % 2] * 10 for i in range(10)]
        offspring = engine.breed(parents)
        assert len(offspring) == 10

    def test_handles_odd_parent_count(self, onemax_small):
        """An odd-length parent list should clone+mutate the leftover
        parent rather than crash or drop it."""
        engine = BitGAEngine(problem=onemax_small, population_size=5, bitstring_length=10, seed=1)
        parents = [[0] * 10] * 5
        offspring = engine.breed(parents)
        assert len(offspring) == 5

    def test_offspring_genomes_correct_length(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=6, bitstring_length=15, seed=1)
        parents = [[1] * 15] * 6
        offspring = engine.breed(parents)
        assert all(len(g) == 15 for g in offspring)

    def test_uses_injected_crossover_and_mutation(self, onemax_small):
        """Confirms crossover=/mutation= injection actually gets used,
        not just accepted and ignored."""
        engine = BitGAEngine(
            problem=onemax_small,
            population_size=4,
            bitstring_length=10,
            seed=1,
            crossover=SinglePointCrossover(),
            mutation=SwapMutation(mutation_probability=1.0),
        )
        assert isinstance(engine.crossover, SinglePointCrossover)
        assert isinstance(engine.mutation, SwapMutation)
        # SwapMutation preserves the bit multiset -- verify that held true
        # through a real breed() call, confirming the injected operator ran.
        parents = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0]] * 4
        offspring = engine.breed(parents)
        for child in offspring:
            assert sorted(child) == [0] * 7 + [1] * 3


class TestReplace:
    def test_truncates_offspring_to_population_size(self, onemax_small):
        """With elitism=0 (the default) the previous population is discarded
        entirely and only offspring survive."""
        engine = BitGAEngine(problem=onemax_small, population_size=5, bitstring_length=10, seed=1)
        offspring = [[i] for i in range(10)]
        next_gen = engine.replace([], offspring)
        assert len(next_gen) == 5
        assert next_gen == offspring[:5]


class TestElitism:
    def test_default_is_zero(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=10, bitstring_length=10, seed=1)
        assert engine.elitism == 0

    def test_negative_elitism_raises(self, onemax_small):
        with pytest.raises(ValueError, match="elitism must be >= 0"):
            BitGAEngine(problem=onemax_small, population_size=10, bitstring_length=10, elitism=-1)

    @pytest.mark.parametrize("bad_elitism", [10, 15])
    def test_elitism_not_below_population_size_raises(self, onemax_small, bad_elitism):
        with pytest.raises(ValueError, match="must be < population_size"):
            BitGAEngine(problem=onemax_small, population_size=10, bitstring_length=10, elitism=bad_elitism)

    def test_best_parent_survives_into_next_generation(self):
        """The whole point of elitism: a strong parent must not be lost even
        when every offspring is worse."""
        problem = OneMaxProblem(length=6)
        engine = BitGAEngine(problem=problem, population_size=4, bitstring_length=6, seed=1, elitism=1)

        population = [[1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0]]
        offspring = [[0, 0, 0, 0, 0, 0]] * 4     # all strictly worse

        engine.evaluate(offspring)               # mirrors the real lifecycle order
        next_gen = engine.replace(population, offspring)

        assert [1, 1, 1, 1, 1, 1] in next_gen

    def test_population_size_is_preserved(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=10, bitstring_length=10, seed=1, elitism=3)
        population = engine.initialize()
        engine.evaluate(population)

        for _ in range(5):
            offspring = engine.breed(engine.select(population))
            engine.evaluate(offspring)
            population = engine.replace(population, offspring)
            assert len(population) == 10

    def test_fitness_values_stay_aligned_with_population(self, onemax_small):
        """replace() rebuilds fitness_values; if the two ever drift apart,
        best_solution() would index into the wrong individual."""
        engine = BitGAEngine(problem=onemax_small, population_size=10, bitstring_length=10, seed=1, elitism=2)
        population = engine.initialize()
        engine.evaluate(population)

        for _ in range(5):
            offspring = engine.breed(engine.select(population))
            engine.evaluate(offspring)
            population = engine.replace(population, offspring)

            assert len(engine.fitness_values) == len(population)
            for genome, score in zip(population, engine.fitness_values):
                assert onemax_small.fitness(genome) == score

    def test_best_fitness_never_decreases_across_generations(self):
        """Without elitism the best individual can be lost; with it, the best
        fitness in the population must be monotonically non-decreasing."""
        problem = OneMaxProblem(length=40)
        engine = BitGAEngine(
            problem=problem, population_size=20, generations=30,
            bitstring_length=40, seed=3, mutation_rate=0.05, elitism=2,
        )

        population = engine.evaluate(engine.initialize())
        best_so_far = max(engine.fitness_values)

        for _ in range(30):
            offspring = engine.breed(engine.select(population))
            engine.evaluate(offspring)
            population = engine.replace(population, offspring)

            current_best = max(engine.fitness_values)
            assert current_best >= best_so_far
            best_so_far = current_best


class TestBestSolution:
    def test_raises_before_any_evaluation(self, onemax_small):
        engine = BitGAEngine(problem=onemax_small, population_size=5, bitstring_length=10, seed=1)
        with pytest.raises(RuntimeError, match="before any generation"):
            engine.best_solution([[0] * 10])

    def test_returns_fittest_individual(self):
        problem = OneMaxProblem(length=5)
        engine = BitGAEngine(problem=problem, population_size=3, bitstring_length=5, seed=1)
        population = [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 0, 0, 0, 0]]
        engine.evaluate(population)
        best = engine.best_solution(population)
        assert best == [1, 1, 1, 1, 1]


class TestFullRun:
    def test_onemax_converges_reasonably(self):
        problem = OneMaxProblem(length=20)
        engine = BitGAEngine(problem=problem, population_size=50, generations=60, bitstring_length=20, seed=42)
        best = engine.run()
        assert problem.fitness(best) >= 15  # not a strict optimum requirement, just "clearly improved"

    def test_reproducibility_same_seed_same_result(self):
        p1 = OneMaxProblem(length=15)
        e1 = BitGAEngine(problem=p1, population_size=30, generations=20, bitstring_length=15, seed=42)
        r1 = e1.run()

        p2 = OneMaxProblem(length=15)
        e2 = BitGAEngine(problem=p2, population_size=30, generations=20, bitstring_length=15, seed=42)
        r2 = e2.run()

        assert r1 == r2

    def test_different_seeds_can_diverge(self):
        p1 = OneMaxProblem(length=15)
        e1 = BitGAEngine(problem=p1, population_size=10, generations=5, bitstring_length=15, seed=1)
        r1 = e1.run()

        p2 = OneMaxProblem(length=15)
        e2 = BitGAEngine(problem=p2, population_size=10, generations=5, bitstring_length=15, seed=2)
        r2 = e2.run()

        # Not asserting they MUST differ (could coincidentally match), just
        # that both runs complete and produce valid genomes independently.
        assert len(r1) == 15
        assert len(r2) == 15

    def test_knapsack_end_to_end(self, knapsack_small):
        engine = BitGAEngine(problem=knapsack_small, population_size=50, generations=50, bitstring_length=3, seed=42)
        best = engine.run()
        assert len(best) == 3
        assert knapsack_small.fitness(best) > 0

    def test_run_returns_bare_genome_not_wrapped(self):
        """best_solution() (and thus run()) returns the raw genome list,
        matching BaseAlgorithm's -> I contract, not a wrapper object."""
        problem = OneMaxProblem(length=8)
        engine = BitGAEngine(problem=problem, population_size=10, generations=5, bitstring_length=8, seed=1)
        result = engine.run()
        assert isinstance(result, list)
        assert all(bit in (0, 1) for bit in result)