"""Figures for pillar B3 (resampling). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

SUB = "B3"
C = color(SUB)  # pillar-B accent


def bootstrap() -> None:
    """The bootstrap approximates a statistic's sampling distribution by resampling
    the data with replacement. Histogram of 5000 bootstrap medians + the 95%
    percentile CI. Lesson: n=60 from Exp(scale=2), rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, B = 60, 5000
    data = rng.exponential(scale=2.0, size=n)
    theta_hat = np.median(data)
    boot = np.array([np.median(rng.choice(data, n, replace=True)) for _ in range(B)])
    lo, hi = np.percentile(boot, [2.5, 97.5])

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.hist(boot, bins=50, density=True, color=C, alpha=0.75)
    ax.axvline(theta_hat, color=ACCENT, lw=2.2, label=f"sample median = {theta_hat:.2f}")
    ax.axvline(lo, color=HOT, ls="--", lw=1.6, label="95% percentile CI")
    ax.axvline(hi, color=HOT, ls="--", lw=1.6)
    ax.axvline(2 * np.log(2), color=FG_MUTE, ls=":", lw=1.4, label="true median = 1.39")
    ax.set_title("Bootstrap distribution of the median")
    ax.set_xlabel("median of a resample")
    ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "bootstrap")


def cross_validation() -> None:
    """Cross-validation estimates out-of-sample error: training error falls with
    model complexity, but the CV error is U-shaped and picks the sweet spot.
    Polynomial fits to a noisy sine, 5-fold CV, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 80
    x = np.sort(rng.uniform(0, 1, n))
    y = np.sin(2 * np.pi * x) + 0.3 * rng.normal(size=n)
    degrees = list(range(0, 12))
    folds = np.array_split(rng.permutation(n), 5)

    tr_err, cv_err = [], []
    for d in degrees:
        tr, cv = [], []
        for f in folds:
            mask = np.ones(n, bool); mask[f] = False
            coef = np.polyfit(x[mask], y[mask], d)
            tr.append(np.mean((np.polyval(coef, x[mask]) - y[mask]) ** 2))
            cv.append(np.mean((np.polyval(coef, x[f]) - y[f]) ** 2))
        tr_err.append(np.mean(tr)); cv_err.append(np.mean(cv))
    best = degrees[int(np.argmin(cv_err))]

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(degrees, tr_err, "-o", color=FG_MUTE, ms=4, label="training error")
    ax.plot(degrees, cv_err, "-o", color=C, ms=4, lw=2.2, label="5-fold CV error")
    ax.axvline(best, color=HOT, ls=":", lw=1.4, label=f"CV-optimal degree = {best}")
    ax.set_yscale("log")
    ax.set_title("Cross-validation picks model complexity")
    ax.set_xlabel("polynomial degree")
    ax.set_ylabel("mean squared error")
    ax.legend(loc="upper center", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "cross-validation")


def main() -> None:
    apply_style()
    bootstrap()
    cross_validation()


if __name__ == "__main__":
    main()
