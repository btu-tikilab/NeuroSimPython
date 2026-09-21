# NeuroSim.Engine/tests/bitga/operators/test_selection.py
import random

import pytest

from bitga.operators.selection import TournamentSelection


class TestTournamentSelectionInit:
    def test_valid_tournament_size(self):
        sel = TournamentSelection(tournament_size=3)
        assert sel.tournament_size == 3

    def test_default_tournament_size(self):
        sel = TournamentSelection()
        assert sel.tournament_size == 3

    @pytest.mark.parametrize("bad_size", [0, 1, -1])
    def test_tournament_size_below_2_raises(self, bad_size):
        with pytest.raises(ValueError, match="must be >= 2"):
            TournamentSelection(tournament_size=bad_size)


class TestSelect:
    def test_returns_requested_number_of_parents(self, rng):
        sel = TournamentSelection(tournament_size=2)
        population = [[0], [1], [0], [1]]
        fitness_values = [1.0, 2.0, 3.0, 4.0]
        parents = sel.select(population, fitness_values, num_parents=10, rng=rng)
        assert len(parents) == 10

    def test_mismatched_population_and_fitness_lengths_raises(self, rng):
        sel = TournamentSelection(tournament_size=2)
        with pytest.raises(ValueError, match="!="):
            sel.select([[0], [1]], [1.0, 2.0, 3.0], num_parents=2, rng=rng)

    def test_tournament_size_larger_than_population_raises(self, rng):
        sel = TournamentSelection(tournament_size=5)
        with pytest.raises(ValueError, match="population size"):
            sel.select([[0], [1]], [1.0, 2.0], num_parents=2, rng=rng)

    @pytest.mark.parametrize("bad_num_parents", [0, -1, -5])
    def test_non_positive_num_parents_raises(self, rng, bad_num_parents):
        sel = TournamentSelection(tournament_size=2)
        with pytest.raises(ValueError, match="num_parents must be positive"):
            sel.select([[0], [1]], [1.0, 2.0], num_parents=bad_num_parents, rng=rng)

    def test_dominant_individual_wins_most_tournaments(self):
        sel = TournamentSelection(tournament_size=4)
        population = [[0], [1], [2], [3]]
        fitness_values = [1.0, 1.0, 1.0, 100.0]
        parents = sel.select(population, fitness_values, num_parents=1000, rng=random.Random(1))
        win_rate = sum(1 for p in parents if p == [3]) / len(parents)
        assert win_rate > 0.6

    def test_selected_individuals_come_from_population(self, rng):
        sel = TournamentSelection(tournament_size=3)
        population = [[0], [1], [2], [3], [4]]
        fitness_values = [5.0, 1.0, 3.0, 2.0, 4.0]
        parents = sel.select(population, fitness_values, num_parents=20, rng=rng)
        for p in parents:
            assert p in population

    def test_reproducible_with_same_seed(self):
        """Ported from the legacy test_operators.py: same seed produces
        an identical parent list."""
        sel = TournamentSelection(tournament_size=3)
        population = [[1, 0, 1, 0], [0, 1, 1, 0], [1, 1, 0, 0]]
        fitness_values = [2, 1, 3]

        parents1 = sel.select(population, fitness_values, num_parents=20, rng=random.Random(42))
        parents2 = sel.select(population, fitness_values, num_parents=20, rng=random.Random(42))

        assert parents1 == parents2