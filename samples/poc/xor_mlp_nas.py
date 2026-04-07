# AUTH:DEVNEUROSIM:7A3F9E2B | samples/poc/xor_mlp_nas.py
"""
POC runner: XOR + bit-encoded MLP NAS using `BitstringGA` + `problems.xor_mlp_nas`.

Problem logic lives in `problems/xor_mlp_nas.py`; generic GA in `neurosim_engine.binary_ga`.
"""

from __future__ import annotations

import random

if __package__ is None or __package__ == "":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from samples.poc._base_import import ensure_engine_src_on_path  # type: ignore
else:
    from ._base_import import ensure_engine_src_on_path

ensure_engine_src_on_path()

from neurosim_engine.binary_ga import BitstringGA  # type: ignore
from problems.xor_mlp_nas import (  # type: ignore
    DEFAULT_GENOME_BITS,
    XorNasSession,
    decode_arch,
    make_xor_fitness_fn,
    param_count,
    train_xor_mlp,
)


def main() -> None:
    rng = random.Random(0)
    session = XorNasSession()
    fitness_fn = make_xor_fitness_fn(
        train_steps=500,
        lr=0.45,
        lambda_penalty=0.12,
        session=session,
    )
    ga = BitstringGA(
        genome_bits=DEFAULT_GENOME_BITS,
        fitness_fn=fitness_fn,
        population_size=80,
        max_generations=100,
        rng=rng,
        elitism=2,
        should_stop=lambda: session.best_acc >= 0.999,
    )
    best = ga.run()
    arch = decode_arch(best.genome)
    mean_bce, acc = train_xor_mlp(arch, best.genome, train_steps=500, lr=0.45)
    genome_str = "".join(str(b) for b in best.genome)
    depth = 2 if arch.h2 is not None else 1
    act = "relu" if arch.relu else "tanh"
    print(
        f"xor_mlp_nas: acc={acc:.4f} mean_bce={mean_bce:.6f} "
        f"arch=({depth} hidden, h1={arch.h1}, h2={arch.h2}, {act}) "
        f"params={param_count(arch)} fitness={best.fitness:.6f} genome={genome_str}"
    )


if __name__ == "__main__":
    main()
