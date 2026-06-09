"""Figures for pillar C7 (model ensembling). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, apply_style, color, save

SUB = "C7"
C = color(SUB)  # pillar-C accent


def ensemble_theory() -> None:
    """Averaging decorrelated models cuts variance roughly like 1/B without adding
    bias — the whole point of bagging. Measured prediction variance of a bagged
    degree-10 fit vs ensemble size, against the 1/B reference. rng(0)."""
    import matplotlib.pyplot as plt

    def f(x):
        return np.sin(2 * np.pi * x)

    xt = np.linspace(0, 1, 120)
    Bs = [1, 2, 5, 10, 20, 50, 100]
    trials = 60
    var = []
    for B in Bs:
        preds = np.zeros((trials, xt.size))
        for t in range(trials):
            r = np.random.default_rng(1000 + t + B * 7919)
            x = r.uniform(0, 1, 30)
            y = f(x) + 0.3 * r.normal(size=30)
            acc = np.zeros(xt.size)
            for _ in range(B):
                bi = r.integers(0, 30, 30)            # bootstrap resample
                acc += np.polyval(np.polyfit(x[bi], y[bi], 10), xt)
            preds[t] = acc / B
        var.append(preds.var(axis=0).mean())

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(Bs, var, "-o", color=C, ms=5, label="bagged ensemble")
    ax.loglog(Bs, [var[0] / B for B in Bs], color=FG_MUTE, ls="--",
              label="$\\propto 1/B$ reference")
    ax.set_title("Bagging reduces variance like 1/B")
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
