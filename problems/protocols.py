# AUTH:DEVNEUROSIM:7A3F9E2B | problems/protocols.py
"""Typing protocols for bit-based NAS / toy problems."""

from __future__ import annotations

from typing import Callable, Protocol, Tuple

Genome = Tuple[int, ...]


class FitnessEvaluator(Protocol):
    """Maps a binary genome to a scalar fitness (maximize)."""

    def __call__(self, genome: Genome) -> float: ...
