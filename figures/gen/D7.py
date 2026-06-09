"""Figures for pillar D7 (training systems). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "D7"
C = color(SUB)  # pillar-D accent (blue)


def flash_attention() -> None:
    """Standard attention materializes the full n×n score matrix, so its memory
    grows quadratically with sequence length; FlashAttention streams the computation
    in tiles, keeping memory linear — the difference between gigabytes and megabytes
    at long context."""
    import matplotlib.pyplot as plt

    n = np.logspace(2, 5.3, 100)
    bytes_per = 2                       # fp16
    standard = n**2 * bytes_per / 1e9   # GB for the n x n scores
    flash = n * 128 * bytes_per / 1e9   # GB, O(n) working set

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(n, standard, color=HOT, lw=2.4, label="standard attention  $O(n^2)$")
    ax.loglog(n, flash, color=C, lw=2.4, label="FlashAttention  $O(n)$")
    ax.set_title("Attention memory vs sequence length")
    ax.set_xlabel("sequence length $n$")
    ax.set_ylabel("score memory (GB)")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "flash-attention")


def gradient_checkpointing() -> None:
    """Gradient checkpointing trades memory for compute: storing K evenly spaced
    checkpoints across L layers needs about K + L/K layers of activations, minimized
    at K ≈ √L — turning O(L) activation memory into O(√L) for one extra forward
    pass."""
    import matplotlib.pyplot as plt

    L = 48
    K = np.arange(1, L + 1)
    mem = K + L / K
    kbest = int(round(np.sqrt(L)))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(K, mem, "-o", color=C, ms=3.5, label="stored activations  $K + L/K$")
    ax.axhline(L, color=FG_MUTE, ls="--", lw=1.4, label=f"no checkpointing  (L = {L})")
    ax.axvline(kbest, color=HOT, ls=":", lw=1.4, label=f"optimum K ≈ √L = {kbest}")
    ax.set_title("Gradient checkpointing: memory vs checkpoints")
    ax.set_xlabel("number of checkpoints $K$")
    ax.set_ylabel("activation memory (layer-units)")
    ax.legend(loc="upper center", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "gradient-checkpointing")


def main() -> None:
    apply_style()
    flash_attention()
    gradient_checkpointing()


if __name__ == "__main__":
    main()
