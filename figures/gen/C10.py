"""Figures for pillar C10 (model evaluation). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GRID, HOT, apply_style, color, save

SUB = "C10"
C = color(SUB)  # pillar-C accent


def learning_curves() -> None:
    """Two diagnostic curves. Left: train/validation error vs training-set size —
    the gap closes as data grows. Right: train/validation error vs model
    complexity — the U-shape of the validation curve picks the sweet spot."""
    import matplotlib.pyplot as plt

    def f(x):
        return np.sin(2 * np.pi * x)

    sigma = 0.3
    # Held-out NOISY test set, so validation error has the same σ² floor as
    # training — both curves converge to σ², the canonical learning-curve story.
    rng_test = np.random.default_rng(999)
    xt = np.linspace(0, 1, 400)
    yt = f(xt) + sigma * rng_test.normal(size=xt.size)

    def fit_eval(degree, n, trials=12):
        tr, va = [], []
        for t in range(trials):
            rng = np.random.default_rng(t)
            x = rng.uniform(0, 1, n)
            y = f(x) + sigma * rng.normal(size=n)
            coef = np.polyfit(x, y, degree)
            tr.append(np.mean((np.polyval(coef, x) - y) ** 2))
            va.append(np.mean((np.polyval(coef, xt) - yt) ** 2))
        return np.mean(tr), np.mean(va)

    # Left: learning curve (vs n) at fixed high complexity
    ns = [15, 25, 40, 60, 100, 200, 400]
    lc = np.array([fit_eval(9, n) for n in ns])
    # Right: validation curve (vs degree) at fixed n
    degs = [0, 1, 2, 3, 5, 7, 9, 12, 15]
    vc = np.array([fit_eval(d, 30) for d in degs])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax1.plot(ns, lc[:, 0], "-o", color=FG_MUTE, ms=4, label="training")
    ax1.plot(ns, lc[:, 1], "-o", color=C, ms=4, label="validation")
    ax1.axhline(sigma**2, color=ACCENT, ls=":", lw=1.2, label="noise floor $\\sigma^2$")
    ax1.set_yscale("log")
    ax1.set_title("Learning curve (degree 9)")
    ax1.set_xlabel("training-set size $n$")
    ax1.set_ylabel("mean squared error")
    ax1.legend(loc="upper right", fontsize=9)

    ax2.plot(degs, vc[:, 0], "-o", color=FG_MUTE, ms=4, label="training")
    ax2.plot(degs, vc[:, 1], "-o", color=C, ms=4, label="validation")
    best = degs[int(np.argmin(vc[:, 1]))]
    ax2.axvline(best, color=HOT, ls=":", lw=1.4, label=f"best degree = {best}")
    ax2.set_yscale("log")
    ax2.set_title("Validation curve (n = 30)")
    ax2.set_xlabel("polynomial degree")
    ax2.legend(loc="upper center", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "learning-curves")


def classification_metrics() -> None:
    """On an imbalanced problem (5% positive) the ROC curve looks strong, but the
    precision-recall curve is more honest about how hard the positives are to
    rank — its baseline is the positive rate, not 0.5. rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.metrics import (auc, precision_recall_curve, roc_curve)

    rng = np.random.default_rng(0)
    n = 5000
    y = (rng.random(n) < 0.05).astype(int)
    scores = y + 0.9 * rng.normal(size=n)

    fpr, tpr, _ = roc_curve(y, scores)
    roc_auc = auc(fpr, tpr)
    prec, rec, _ = precision_recall_curve(y, scores)
    pr_auc = auc(rec, prec)
    base = y.mean()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 4.0))
    ax1.plot(fpr, tpr, color=C, lw=2.4, label=f"ROC (AUC = {roc_auc:.2f})")
    ax1.plot([0, 1], [0, 1], color=FG_MUTE, ls="--", lw=1.2, label="random")
    ax1.set_title("ROC curve")
    ax1.set_xlabel("false positive rate")
    ax1.set_ylabel("true positive rate")
    ax1.legend(loc="lower right", fontsize=9)

    ax2.plot(rec, prec, color=HOT, lw=2.4, label=f"PR (AUC = {pr_auc:.2f})")
    ax2.axhline(base, color=FG_MUTE, ls="--", lw=1.2,
                label=f"baseline = {base:.2f}")
    ax2.set_title("Precision-recall curve")
    ax2.set_xlabel("recall")
    ax2.set_ylabel("precision")
    ax2.set_ylim(0, 1.02)
    ax2.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "classification-metrics")


def main() -> None:
    apply_style()
    learning_curves()
    classification_metrics()


if __name__ == "__main__":
    main()
