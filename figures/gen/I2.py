"""Figures for pillar I2 (training infra & HPO). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GRID, HOT, apply_style, color, save

SUB = "I2"
C = color(SUB)  # pillar-I accent (green)


def hyperparameter_search() -> None:
    """Random search beats grid search when only a few hyperparameters matter: a grid
    wastes trials on a coarse lattice, while random sampling tries a distinct value of
    the important parameter on every trial — covering it far more densely for the same
    budget. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 4.2))
    g = np.linspace(0.08, 0.92, 5)
    gx, gy = np.meshgrid(g, g)
    ax1.scatter(gx.ravel(), gy.ravel(), s=40, color=C)
    ax1.set_title("grid search (25 trials)")
    rx, ry = rng.random(25), rng.random(25)
    ax2.scatter(rx, ry, s=40, color=HOT)
    ax2.set_title("random search (25 trials)")
    for ax, xs in [(ax1, g), (ax2, rx)]:
        ax.set_xlabel("important parameter"); ax.set_ylabel("unimportant parameter")
        # marginal coverage ticks on top
        for v in xs:
            ax.plot([v, v], [1.02, 1.06], color=ACCENT, lw=1.4, clip_on=False)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    fig.suptitle("Random search covers the important axis more densely", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "hyperparameter-search")


def multi_fidelity_hpo() -> None:
    """Multi-fidelity HPO (successive halving / Hyperband) starts many configurations
    on a small budget, then repeatedly keeps only the top half and gives them more —
    so compute concentrates on the promising configs instead of training every one to
    completion. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n0 = 16
    budgets = [1, 2, 4, 8]
    quality = rng.uniform(0.3, 0.95, n0)        # latent asymptotic quality
    alive = list(range(n0))

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for k, b in enumerate(budgets):
        for i in alive:
            perf = quality[i] * (1 - np.exp(-b / 3)) + 0.02 * rng.normal()
            nb = budgets[k + 1] if k + 1 < len(budgets) else b * 2
            perf2 = quality[i] * (1 - np.exp(-nb / 3))
            ax.plot([b, nb], [perf, perf2], color=C, alpha=0.5, lw=1.2)
        # keep top half
        alive = sorted(alive, key=lambda i: -quality[i])[:max(1, len(alive) // 2)]
    best = max(range(n0), key=lambda i: quality[i])
    bb = quality[best] * (1 - np.exp(-np.array([1, 2, 4, 8, 16]) / 3))
    ax.plot([1, 2, 4, 8, 16], bb, "-o", color=HOT, lw=2.2, ms=4, label="survivor")
    ax.set_xscale("log", base=2)
    ax.set_title("Successive halving concentrates compute")
    ax.set_xlabel("budget per config (epochs)"); ax.set_ylabel("validation score")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "multi-fidelity-hpo")


def main() -> None:
    apply_style()
    hyperparameter_search()
    multi_fidelity_hpo()


if __name__ == "__main__":
    main()
