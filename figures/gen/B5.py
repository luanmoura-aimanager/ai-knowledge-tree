"""Figures for pillar B5 (causal inference). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, GOOD, HOT, apply_style, color, save

SUB = "B5"
C = color(SUB)  # pillar-B accent


def potential_outcomes() -> None:
    """Each unit has two potential outcomes Y(0), Y(1); we see only one. Here the
    effect is a constant +1 (points sit on Y(1)=Y(0)+1), but treated units (which
    have higher X) cluster at higher outcomes — the source of selection bias.
    Lesson: n=1000, ATE=1, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 1000
    X = rng.normal(0, 1, n)
    W = (X + rng.normal(0, 1, n) > 0).astype(int)
    Y0 = 0.5 * X + rng.normal(0, 1, n)
    Y1 = Y0 + 1.0

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.scatter(Y0[W == 0], Y1[W == 0], s=12, color=ACCENT, alpha=0.5, edgecolor="none",
               label="control (W=0)")
    ax.scatter(Y0[W == 1], Y1[W == 1], s=12, color=HOT, alpha=0.5, edgecolor="none",
               label="treated (W=1)")
    lo, hi = Y0.min(), Y0.max()
    ax.plot([lo, hi], [lo + 1, hi + 1], color=GOOD, lw=2.2, label="Y(1) = Y(0) + 1")
    ax.set_title("Potential outcomes (constant effect, but selection in X)")
    ax.set_xlabel("$Y(0)$")
    ax.set_ylabel("$Y(1)$")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "potential-outcomes")


def propensity_scores() -> None:
    """The propensity score e(x)=P(W=1|x) summarizes confounders into one number;
    causal claims need overlap — both groups present across the score range.
    Lesson: n=2000, logistic assignment in X1,X2, rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LogisticRegression

    rng = np.random.default_rng(0)
    n = 2000
    X1, X2 = rng.normal(0, 1, n), rng.normal(0, 1, n)
    W = (0.5 * X1 + 0.3 * X2 + rng.normal(0, 1, n) > 0).astype(int)
    X = np.column_stack([X1, X2])
    e = LogisticRegression().fit(X, W).predict_proba(X)[:, 1]

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.hist(e[W == 1], bins=30, density=True, color=HOT, alpha=0.55, label="treated")
    ax.hist(e[W == 0], bins=30, density=True, color=ACCENT, alpha=0.55, label="control")
    ax.set_title("Propensity-score overlap")
    ax.set_xlabel("estimated propensity $\\hat e(x)$")
    ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "propensity-scores")


def iv_estimation() -> None:
    """An instrument Z shifts treatment W but affects the outcome Y only through W,
    so the IV (Wald) estimate — reduced-form effect ÷ first-stage effect —
    recovers the true effect (2.0) where naive OLS is confounded. Lesson: n=5000,
    rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 8000
    Z = rng.binomial(1, 0.5, n).astype(float)
    U = rng.normal(0, 1, n)
    W = (2.0 * Z + 0.4 * U + rng.normal(0, 1, n) > 0).astype(float)  # strong instrument
    Y0 = 1.0 * U + rng.normal(0, 0.5, n)
    Y = W * (Y0 + 2.0) + (1 - W) * Y0

    w0, w1 = W[Z == 0].mean(), W[Z == 1].mean()
    y0, y1 = Y[Z == 0].mean(), Y[Z == 1].mean()
    wald = (y1 - y0) / (w1 - w0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.9))
    ax1.bar([0, 1], [w0, w1], color=ACCENT, width=0.5)
    ax1.set_title(f"First stage: P(W=1 | Z)\nΔ = {w1 - w0:.2f}")
    ax1.set_xticks([0, 1]); ax1.set_xlabel("instrument $Z$"); ax1.set_ylabel("mean treatment $W$")

    ax2.bar([0, 1], [y0, y1], color=C, width=0.5)
    ax2.set_title(f"Reduced form: E[Y | Z]\nΔ = {y1 - y0:.2f}")
    ax2.set_xticks([0, 1]); ax2.set_xlabel("instrument $Z$"); ax2.set_ylabel("mean outcome $Y$")
    fig.suptitle(f"IV (Wald) estimate = {y1 - y0:.2f} / {w1 - w0:.2f} = {wald:.2f}   (true effect 2.0)", y=1.02)
    fig.tight_layout()
    save(fig, SUB, "iv-estimation")


def main() -> None:
    apply_style()
    potential_outcomes()
    propensity_scores()
    iv_estimation()


if __name__ == "__main__":
    main()
