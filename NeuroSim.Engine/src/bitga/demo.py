"""
Demo for BitGA Engine

Runs:
1. OneMax Problem
2. Knapsack Problem
"""

from bitga.engine import BitGAEngine
from neurosim_problems.onemax import OneMaxProblem
from neurosim_problems.knapsack import KnapsackProblem


def print_result(result):
    """Print RunResult in a readable format."""

    print("=" * 70)
    print(f"Problem              : {result.problem_name}")
    print(f"Run ID               : {result.run_id}")
    print(f"Best Fitness         : {result.best_fitness}")
    print(f"Best Solution        : {result.best_solution}")
    print(f"Best Generation      : {result.generations_to_convergence}")
    print(f"Total Generations    : {result.total_generations}")
    print(f"Execution Time       : {result.execution_time_seconds:.6f} seconds")

    print("\nGeneration Statistics")
    print("-" * 70)
    print(f"{'Gen':<8}{'Best':<10}{'Average':<12}{'Worst':<10}")

    for stat in result.convergence_history:
        print(
            f"{stat.generation:<8}"
            f"{stat.best_fitness:<10}"
            f"{stat.avg_fitness:<12.2f}"
            f"{stat.worst_fitness:<10}"
        )

    print("=" * 70)
    print()


def run_onemax():
    """Run OneMax example."""

    problem = OneMaxProblem(length=10)

    engine = BitGAEngine(
        problem=problem,
        population_size=20,
        generations=10,
        bitstring_length=10,
        run_id="onemax_demo",
    )

    return engine.run()


def run_knapsack():
    """Run Knapsack example."""

    values = [20, 30, 35, 12, 3, 40]
    weights = [2, 5, 7, 3, 1, 9]
    capacity = 10

    problem = KnapsackProblem(
        values=values,
        weights=weights,
        capacity=capacity,
    )

    engine = BitGAEngine(
        problem=problem,
        population_size=20,
        generations=10,
        bitstring_length=len(values),
        run_id="knapsack_demo",
    )

    return engine.run()


def main():

    print("\nRunning OneMax...\n")
    one_max_result = run_onemax()
    print_result(one_max_result)

    print("\nRunning Knapsack...\n")
    knapsack_result = run_knapsack()
    print_result(knapsack_result)


if __name__ == "__main__":
    main()