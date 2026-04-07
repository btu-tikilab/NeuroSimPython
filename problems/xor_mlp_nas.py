# AUTH:DEVNEUROSIM:7A3F9E2B | problems/xor_mlp_nas.py
"""
XOR + numpy MLP: bits decode architecture; inner loop trains weights (SGD).

See `samples/poc/xor_mlp_nas.py` for a minimal runner using `BitstringGA`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, Tuple

import numpy as np

from problems.protocols import Genome

# XOR dataset (full batch)
_X_XOR = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]], dtype=np.float64)
_Y_XOR = np.array([[0.0], [1.0], [1.0], [0.0]], dtype=np.float64)

WIDTH_TABLE = (4, 8, 16, 24)

DEFAULT_GENOME_BITS = 8


@dataclass(frozen=True)
class ArchSpec:
    h1: int
    h2: int | None
    relu: bool

    @property
    def param_cap(self) -> int:
        return 2 * 24 + 24 + 24 * 24 + 24 + 24 * 1 + 1


@dataclass
class XorNasSession:
    """Updated by `make_xor_fitness_fn` (e.g. for early stopping on accuracy)."""

    best_acc: float = 0.0


def bits_to_int(bits: Sequence[int], start: int, length: int) -> int:
    v = 0
    for i in range(length):
        v = (v << 1) | int(bits[start + i])
    return v


def decode_arch(genome: Genome) -> ArchSpec:
    if len(genome) < 6:
        raise ValueError("genome too short for arch decode")
    h1 = WIDTH_TABLE[bits_to_int(genome, 0, 2) % len(WIDTH_TABLE)]
    two_hidden = genome[2] == 1
    h2_idx = bits_to_int(genome, 3, 2) % len(WIDTH_TABLE)
    h2 = WIDTH_TABLE[h2_idx] if two_hidden else None
    relu = genome[5] == 1
    return ArchSpec(h1=h1, h2=h2, relu=relu)


def genome_seed(genome: Genome) -> int:
    s = 0
    for b in genome:
        s = (s << 1) | int(b)
    return s & 0xFFFFFFFF


def param_count(arch: ArchSpec) -> int:
    n = 2 * arch.h1 + arch.h1
    if arch.h2 is None:
        n += arch.h1 * 1 + 1
    else:
        n += arch.h1 * arch.h2 + arch.h2
        n += arch.h2 * 1 + 1
    return n


def _activation(z: np.ndarray, relu: bool) -> np.ndarray:
    return np.maximum(z, 0.0) if relu else np.tanh(z)


def _activation_grad(g_a: np.ndarray, z: np.ndarray, relu: bool) -> np.ndarray:
    if relu:
        return g_a * (z > 0.0).astype(np.float64)
    t = np.tanh(z)
    return g_a * (1.0 - t * t)


def train_xor_mlp(
    arch: ArchSpec,
    genome: Genome,
    *,
    train_steps: int,
    lr: float,
) -> Tuple[float, float]:
    """Returns (mean_bce, accuracy) after training."""
    rng = np.random.default_rng(genome_seed(genome))

    if arch.h2 is None:
        w1 = rng.standard_normal((2, arch.h1)) * np.sqrt(2.0 / 2.0)
        b1 = np.zeros((1, arch.h1), dtype=np.float64)
        w2 = rng.standard_normal((arch.h1, 1)) * np.sqrt(2.0 / arch.h1)
        b2 = np.zeros((1, 1), dtype=np.float64)
    else:
        w1 = rng.standard_normal((2, arch.h1)) * np.sqrt(2.0 / 2.0)
        b1 = np.zeros((1, arch.h1), dtype=np.float64)
        w2 = rng.standard_normal((arch.h1, arch.h2)) * np.sqrt(2.0 / arch.h1)
        b2 = np.zeros((1, arch.h2), dtype=np.float64)
        w3 = rng.standard_normal((arch.h2, 1)) * np.sqrt(2.0 / arch.h2)
        b3 = np.zeros((1, 1), dtype=np.float64)

    x = _X_XOR
    y = _Y_XOR
    eps = 1e-7

    for _ in range(train_steps):
        if arch.h2 is None:
            z1 = x @ w1 + b1
            a1 = _activation(z1, arch.relu)
            z2 = a1 @ w2 + b2
            p = 1.0 / (1.0 + np.exp(-np.clip(z2, -60.0, 60.0)))
            loss_vec = -(y * np.log(p + eps) + (1.0 - y) * np.log(1.0 - p + eps))
            d_z2 = (p - y) / 4.0
            dw2 = a1.T @ d_z2
            db2 = np.sum(d_z2, axis=0, keepdims=True)
            da1 = d_z2 @ w2.T
            dz1 = _activation_grad(da1, z1, arch.relu)
            dw1 = x.T @ dz1
            db1 = np.sum(dz1, axis=0, keepdims=True)
            w2 -= lr * dw2
            b2 -= lr * db2
            w1 -= lr * dw1
            b1 -= lr * db1
        else:
            z1 = x @ w1 + b1
            a1 = _activation(z1, arch.relu)
            z2 = a1 @ w2 + b2
            a2 = _activation(z2, arch.relu)
            z3 = a2 @ w3 + b3
            p = 1.0 / (1.0 + np.exp(-np.clip(z3, -60.0, 60.0)))
            d_z3 = (p - y) / 4.0
            dw3 = a2.T @ d_z3
            db3 = np.sum(d_z3, axis=0, keepdims=True)
            da2 = d_z3 @ w3.T
            dz2 = _activation_grad(da2, z2, arch.relu)
            dw2 = a1.T @ dz2
            db2 = np.sum(dz2, axis=0, keepdims=True)
            da1 = dz2 @ w2.T
            dz1 = _activation_grad(da1, z1, arch.relu)
            dw1 = x.T @ dz1
            db1 = np.sum(dz1, axis=0, keepdims=True)
            w3 -= lr * dw3
            b3 -= lr * db3
            w2 -= lr * dw2
            b2 -= lr * db2
            w1 -= lr * dw1
            b1 -= lr * db1

    if arch.h2 is None:
        z1 = x @ w1 + b1
        a1 = _activation(z1, arch.relu)
        z2 = a1 @ w2 + b2
        p = 1.0 / (1.0 + np.exp(-np.clip(z2, -60.0, 60.0)))
    else:
        z1 = x @ w1 + b1
        a1 = _activation(z1, arch.relu)
        z2 = a1 @ w2 + b2
        a2 = _activation(z2, arch.relu)
        z3 = a2 @ w3 + b3
        p = 1.0 / (1.0 + np.exp(-np.clip(z3, -60.0, 60.0)))

    loss_vec = -(y * np.log(p + eps) + (1.0 - y) * np.log(1.0 - p + eps))
    mean_bce = float(np.mean(loss_vec))
    acc = float(np.mean(((p >= 0.5).astype(np.float64) == y).astype(np.float64)))
    return mean_bce, acc


def make_xor_fitness_fn(
    *,
    train_steps: int,
    lr: float,
    lambda_penalty: float,
    session: XorNasSession,
) -> Callable[[Genome], float]:
    """Fitness = 1/(1+mean_BCE) - λ * (params/param_cap); tracks `session.best_acc`."""

    def fitness_fn(genome: Genome) -> float:
        arch = decode_arch(genome)
        mean_bce, acc = train_xor_mlp(arch, genome, train_steps=train_steps, lr=lr)
        session.best_acc = max(session.best_acc, acc)
        n = param_count(arch)
        penalty = lambda_penalty * (n / max(1, arch.param_cap))
        return 1.0 / (1.0 + mean_bce) - penalty

    return fitness_fn
