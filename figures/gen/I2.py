"""Figures for pillar I2 (training infra & HPO). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

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



def tpe() -> None:
    """One TPE step on the lesson's 1-D loss: 30 trials split at the best 20%, the
    Parzen densities l(x) and g(x), and the ratio whose argmax is the next trial.
    rng(0)."""
    import matplotlib.pyplot as plt

    def loss(x):
        return 0.05 * (x - 7.0) ** 2 + 0.3 * np.sin(3 * x) + 0.3

    def parzen(points, h, x):
        z = (x[:, None] - points[None, :]) / h
        return np.exp(-0.5 * z ** 2).mean(axis=1) / (h * np.sqrt(2 * np.pi))

    rng = np.random.default_rng(0)
    X = rng.uniform(0, 10, 30)
    Y = loss(X)
    order = np.argsort(Y)
    n_good = int(np.ceil(0.2 * len(X)))
    good, bad = X[order[:n_good]], X[order[n_good:]]
    h = 0.1 * 10 * len(X) ** (-0.2)
    grid = np.linspace(0, 10, 600)
    l, g = parzen(good, h, grid), parzen(bad, h, grid)
    ratio = l / (g + 1e-12)
    x_next = grid[np.argmax(ratio)]

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 5.6), sharex=True)
    a1.plot(grid, loss(grid), color=FG_MUTE, lw=1.4, label="validation loss")
    a1.plot(bad, loss(bad), "o", color=FG_MUTE, ms=5, label="bad trials")
    a1.plot(good, loss(good), "o", color=C, ms=7, label="good trials (best 20%)")
    a1.set_ylabel("loss")
    a1.set_title("TPE: model where good trials are, not the loss itself")
    a1.legend(loc="upper right", fontsize=8)
    a2.plot(grid, l, color=C, label="l(x): good-trial density")
    a2.plot(grid, g, color=FG_MUTE, label="g(x): bad-trial density")
    a2b = a2.twinx()
    a2b.plot(grid, ratio, color=HOT, lw=1.4, ls="--", label="l(x) / g(x)")
    a2b.set_ylabel("ratio", color=HOT)
    a2b.tick_params(axis="y", colors=HOT)
    a2b.grid(False)
    a2.axvline(x_next, color=HOT, lw=1.0, ls=":")
    a2.text(x_next - 0.15, a2.get_ylim()[1] * 0.92, "next trial", color=HOT, fontsize=9, va="top", ha="right")
    a2.set_xlabel("hyperparameter x")
    a2.set_ylabel("density")
    h1, l1 = a2.get_legend_handles_labels()
    h2, l2 = a2b.get_legend_handles_labels()
    a2.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "tpe")


def main() -> None:
    apply_style()
    tpe()
    hyperparameter_search()
    multi_fidelity_hpo()


if __name__ == "__main__":
    main()
