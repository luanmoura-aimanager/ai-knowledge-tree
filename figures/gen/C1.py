"""Figures for pillar C1 (linear models). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import GOOD, HOT, apply_style, color, save

SUB = "C1"
C = color(SUB)  # pillar-C accent


def bias_variance() -> None:
    """The canonical bias-variance U-curve.

    Reproduces the lesson's experiment exactly: truth f(x) = sin(2πx), n = 30
    points with σ = 0.3 noise, polynomial fits across degrees, bias²/variance/
    total estimated over many random datasets.
    """
    import matplotlib.pyplot as plt

    def f(x):
        return np.sin(2 * np.pi * x)

    sigma = 0.3
    x_test = np.linspace(0, 1, 200)
    f_test = f(x_test)
    degrees = list(range(1, 16))
    trials = 200

    bias2, variance, total = [], [], []
    for d in degrees:
        preds = np.zeros((trials, len(x_test)))
        for t in range(trials):
            rng = np.random.default_rng(1000 + t)
            x_tr = rng.uniform(0, 1, 30)
            y_tr = f(x_tr) + sigma * rng.normal(size=30)
            coefs = np.polyfit(x_tr, y_tr, d)
            preds[t] = np.polyval(coefs, x_test)
        mean_pred = preds.mean(axis=0)
        b2 = np.mean((mean_pred - f_test) ** 2)
        var = np.mean(preds.var(axis=0))
        bias2.append(b2)
        variance.append(var)
        total.append(b2 + var + sigma**2)

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(degrees, bias2, "-o", color=GOOD, ms=4, label="bias$^2$")
    ax.plot(degrees, variance, "-o", color=HOT, ms=4, label="variance")
    ax.plot(degrees, total, "-o", color=C, ms=4, lw=2.4, label="total error")
    ax.axhline(sigma**2, color="#6c7596", ls="--", lw=1.2, label=f"noise floor $\\sigma^2$={sigma**2:.2f}")

    best = degrees[int(np.argmin(total))]
    ax.axvline(best, color=C, ls=":", lw=1.2, alpha=0.7)
    ax.annotate(
        f"sweet spot\n(degree {best})",
        xy=(best, min(total)),
        xytext=(best + 1.5, min(total) + 0.25),
        color=C,
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color=C, lw=1.2),
    )

    ax.set_yscale("log")
    ax.set_title("Bias-variance tradeoff vs model complexity")
    ax.set_xlabel("polynomial degree (complexity)")
    ax.set_ylabel("error (log scale)")
    ax.set_xticks(degrees)
    ax.legend(loc="upper center", ncol=2)

    fig.tight_layout()
    save(fig, SUB, "bias-variance")


def main() -> None:
    apply_style()
    bias_variance()


if __name__ == "__main__":
    main()
