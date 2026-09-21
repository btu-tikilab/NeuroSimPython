# AUTH:DEVNEUROSIM:7A3F9E2B | NeuroSim.Engine/src/bitga/config.py
"""
BitGA Engine Builder
Translates a config dict into a fully configured BitGAEngine.
"""

from typing import Any, Dict

from .engine import BitGAEngine
from .operators.crossover import (
    UniformCrossover,
    SinglePointCrossover,
    TwoPointCrossover,
)
from .operators.mutation import (
    BitFlipMutation,
    SwapMutation,
    InversionMutation,
)


def _build_crossover(crossover_type: str, config: Dict[str, Any]):
    """
    Build a crossover operator from its type name.
    """

    if crossover_type == "Uniform":
        return UniformCrossover(
            crossover_probability=config.get("crossover_probability", 0.5)
        )

    if crossover_type == "Single Point":
        return SinglePointCrossover()

    if crossover_type == "Two Point":
        return TwoPointCrossover()

    raise ValueError(f"Unknown crossover_type: {crossover_type!r}")


def _build_mutation(mutation_type: str, config: Dict[str, Any]):
    """
    Build a mutation operator from its type name.
    """

    mutation_rate = config.get("mutation_rate")
    bitstring_length = config["bitstring_length"]

    if mutation_type == "Bit Flip":
        return BitFlipMutation(mutation_rate=mutation_rate, length=bitstring_length)

    if mutation_type == "Swap":
        return SwapMutation(
            mutation_probability=mutation_rate if mutation_rate is not None else 0.1
        )

    if mutation_type == "Inversion":
        return InversionMutation(
            mutation_probability=mutation_rate if mutation_rate is not None else 0.1
        )

    raise ValueError(f"Unknown mutation_type: {mutation_type!r}")


def build_engine(problem, config: Dict[str, Any]) -> BitGAEngine:
    """
    Build a fully configured BitGAEngine from a config dict.
    """

    if "bitstring_length" not in config:
        raise ValueError("config must include 'bitstring_length'")

    crossover = _build_crossover(
        config.get("crossover_type", "Uniform"), config
    )
    mutation = _build_mutation(
        config.get("mutation_type", "Bit Flip"), config
    )

    return BitGAEngine(
        problem=problem,
        population_size=config.get("population_size", 100),
        generations=config.get("generations", 100),
        bitstring_length=config["bitstring_length"],
        tournament_size=config.get("tournament_size", 3),
        seed=config.get("seed", 42),
        crossover=crossover,
        mutation=mutation,
    )