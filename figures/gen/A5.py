"""Figures for pillar A5 (algorithms & data structures). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, CYCLE, FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "A5"
C = color(SUB)  # pillar-A accent (gold)


def complexity_analysis() -> None:
    """The complexity classes separate sharply as input grows: constant and
    logarithmic stay flat, linear and n·log n grow gently, while quadratic and
    exponential explode — which is why asymptotics decide scalability."""
    import matplotlib.pyplot as plt

    n = np.arange(1, 41)
    curves = [
        ("O(1)", np.ones_like(n, dtype=float)),
        ("O(log n)", np.log2(n + 1)),
        ("O(n)", n.astype(float)),
        ("O(n log n)", n * np.log2(n + 1)),
        ("O(n²)", n.astype(float) ** 2),
        ("O(2ⁿ)", 2.0 ** n),
    ]
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    for (lab, y), col in zip(curves, CYCLE):
        ax.plot(n, y, color=col, lw=2.2, label=lab)
    ax.set_yscale("log")
    ax.set_ylim(0.5, 1e12)
    ax.set_title("Growth rates of common complexity classes")
    ax.set_xlabel("input size $n$")
    ax.set_ylabel("operations (log scale)")
    ax.legend(loc="upper left", fontsize=9, ncol=2)
    fig.tight_layout()
    save(fig, SUB, "complexity-analysis")


def sorting() -> None:
    """Comparison counts make the gap concrete: the O(n log n) sorts (merge, quick)
    scale gracefully, while insertion sort's O(n²) comparisons blow up — for n=2000
    that is a ~45× difference."""
    import matplotlib.pyplot as plt

    n = np.arange(10, 2001)
    merge = n * np.log2(n)
    quick = 1.39 * n * np.log2(n)
    insertion = n**2 / 4

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(n, insertion, color=HOT, lw=2.2, label="insertion sort  $O(n^2)$")
    ax.plot(n, quick, color=ACCENT, lw=2.2, label="quicksort  $\\sim n\\log n$")
    ax.plot(n, merge, color=C, lw=2.2, label="merge sort  $n\\log n$")
    ax.set_yscale("log")
    ax.set_title("Sorting: comparison counts vs n")
    ax.set_xlabel("array size $n$")
    ax.set_ylabel("comparisons (log scale)")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "sorting")


def main() -> None:
    apply_style()
    complexity_analysis()
    sorting()


if __name__ == "__main__":
    main()
