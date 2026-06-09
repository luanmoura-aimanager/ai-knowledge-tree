"""Figures for pillar C7 (model ensembling). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, apply_style, color, save

SUB = "C7"
C = color(SUB)  # pillar-C accent


def ensemble_theory() -> None:
    """Averaging B independent models cuts prediction variance exactly like 1/B
    without adding bias — the core reason ensembles reduce error. Measured variance
    of an averaged degree-3 fit vs ensemble size, tracking the 1/B reference."""
    import matplotlib.pyplot as plt

    def f(x):
        return np.sin(2 * np.pi * x)

    xt = np.linspace(0.1, 0.9, 40)        # interior points (avoid edge extrapolation)
    Bs = [1, 2, 4, 8, 16, 32, 64]
    trials = 400
    var = []
    for B in Bs:
        preds = np.zeros((trials, xt.size))
        for t in range(trials):
            r = np.random.default_rng(10_000 * B + t)
            acc = np.zeros(xt.size)
            for _ in range(B):                       # each model: own independent data
                x = r.uniform(0, 1, 20)
                y = f(x) + 0.3 * r.normal(size=20)
                acc += np.polyval(np.polyfit(x, y, 3), xt)
            preds[t] = acc / B
        var.append(preds.var(axis=0).mean())

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(Bs, var, "-o", color=C, ms=5, label="averaged ensemble")
    ax.loglog(Bs, [var[0] / B for B in Bs], color=FG_MUTE, ls="--",
              label="$1/B$ reference")
    ax.set_title("Averaging reduces variance like 1/B")
    ax.set_xlabel("ensemble size $B$")
    ax.set_ylabel("prediction variance")
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "ensemble-theory")


def main() -> None:
    apply_style()
    ensemble_theory()


if __name__ == "__main__":
    main()
