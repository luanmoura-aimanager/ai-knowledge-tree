"""Figures for pillar M6 (robustness, sensitivity & assumptions).

See figures/gen/_style.py. Deterministic (rng(0)); run via `npm run figures`.
Numpy-only (no sklearn/scipy), matching the lessons' runnable code.
"""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, GOOD, HOT, apply_style, color, save

SUB = "M6"
C = color(SUB)  # pillar-M accent
FG_LINE = FG_DIM  # neutral line color for reference lines / annotations


def confounding_bias() -> None:
    """An omitted binary confounder U injects a bias delta = (mean shift in U
    across treatment groups) * (effect of U on Y). As the confounder grows more
    imbalanced across treatment, the adjusted estimate drifts away from the true
    ATE = 0. Lesson unconfoundedness-failure.mdx: true ATE = 0, rng(0)."""
    import matplotlib.pyplot as plt

    true_ate = 0.0
    gammas = np.linspace(0.0, 0.45, 40)   # P(U=1|W=1) - P(U=1|W=0) imbalance
    beta_vals = [0.5, 1.0, 2.0]           # effect of U on the outcome
    cols = [ACCENT, C, HOT]

    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    for beta, col in zip(beta_vals, cols):
        bias = beta * gammas            # delta = beta_U * imbalance
        ax.plot(gammas, true_ate + bias, color=col, lw=2.2,
                label=fr"$\beta_U = {beta}$")
    ax.axhline(true_ate, color=GOOD, lw=2.0, ls="--", label="true ATE = 0")
    ax.set_title("Bias from an omitted confounder")
    ax.set_xlabel(r"confounder imbalance $\delta = P(U{=}1\mid W{=}1)-P(U{=}1\mid W{=}0)$")
    ax.set_ylabel(r"adjusted estimate $\hat\tau$")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "confounding-bias")


def evalue_curve() -> None:
    """The E-value RR + sqrt(RR*(RR-1)) is the minimum confounder-association
    strength (on the risk-ratio scale) needed to explain away an observed risk
    ratio RR. Larger observed effects demand stronger confounding to overturn.
    Lesson sensitivity-rosenbaum-evalue.mdx."""
    import matplotlib.pyplot as plt

    rr = np.linspace(1.0, 4.0, 300)
    evalue = rr + np.sqrt(rr * (rr - 1.0))

    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    ax.plot(rr, evalue, color=C, lw=2.4, label=r"E-value $= RR + \sqrt{RR(RR-1)}$")
    ax.plot(rr, rr, color=FG_LINE, lw=1.4, ls=":", label="$y = RR$ (reference)")
    for r0 in [1.5, 2.0, 3.0]:
        e0 = r0 + np.sqrt(r0 * (r0 - 1.0))
        ax.scatter([r0], [e0], color=HOT, zorder=5, s=36)
        ax.annotate(f"RR={r0}\nE={e0:.2f}", (r0, e0),
                    textcoords="offset points", xytext=(8, -2), fontsize=8.5,
                    color=ACCENT)
    ax.set_title("E-value grows with the observed effect")
    ax.set_xlabel("observed risk ratio $RR$")
    ax.set_ylabel("E-value")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "evalue-curve")


def manski_bounds() -> None:
    """The no-assumption (worst-case) bounds on the ATE have width 1 (for a
    binary outcome); layering monotone treatment response, then monotone
    treatment selection, shrinks the identified interval. Lesson
    partial-identification-bounds.mdx: stylized binary-outcome numbers."""
    import matplotlib.pyplot as plt

    # Stylized identified intervals for the ATE on a binary outcome.
    # [lower, upper] under successively stronger assumptions.
    rows = [
        ("point id.\n(ignorability)", 0.20, 0.20),
        ("MTS + MTR", 0.00, 0.34),
        ("monotone response\n(MTR)", -0.18, 0.34),
        ("no assumptions\n(Manski)", -0.45, 0.55),
    ]
    cols = [GOOD, ACCENT, C, HOT]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for i, ((label, lo, hi), col) in enumerate(zip(rows, cols)):
        ax.plot([lo, hi], [i, i], color=col, lw=8, solid_capstyle="round",
                alpha=0.85)
        ax.scatter([lo, hi], [i, i], color=col, s=22, zorder=5)
        ax.text(hi + 0.02, i, f"[{lo:.2f}, {hi:.2f}]", va="center",
                fontsize=8.5, color=FG_LINE)
    ax.axvline(0.20, color=GOOD, lw=1.4, ls="--", alpha=0.7,
               label="true ATE = 0.20")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=9)
    ax.set_xlabel("identified interval for the ATE")
    ax.set_title("Assumptions shrink the Manski bounds")
    ax.set_xlim(-0.6, 0.85)
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "manski-bounds")


def refutation_histogram() -> None:
    """A placebo (random common cause / placebo treatment) refuter re-estimates
    the effect under a null perturbation many times; a robust estimate yields a
    placebo distribution centered at zero, far from the real estimate. A failing
    estimate sits inside the placebo cloud. Lesson refutation-tests.mdx: rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 1500
    reps = 600
    true_effect = 1.0

    # Real (robust) estimate from a simple confounded-but-adjusted design.
    X = rng.normal(0, 1, n)
    W = (rng.uniform(size=n) < 1 / (1 + np.exp(-0.7 * X))).astype(float)
    Y = true_effect * W + 0.5 * X + rng.normal(0, 0.5, n)
    # adjusted difference in means via residual-on-residual (FWL with [1, X]).
    B = np.column_stack([np.ones(n), X])

    def resid(v):
        coef = np.linalg.lstsq(B, v, rcond=None)[0]
        return v - B @ coef

    Wt, Yt = resid(W), resid(Y)
    real_est = (Wt * Yt).mean() / (Wt ** 2).mean()

    # Placebo: permute the treatment label, breaking any W->Y link; re-estimate.
    placebo = np.empty(reps)
    for r in range(reps):
        Wp = rng.permutation(W)
        Wpt = resid(Wp)
        placebo[r] = (Wpt * Yt).mean() / (Wpt ** 2).mean()

    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    ax.hist(placebo, bins=40, density=True, color=ACCENT, alpha=0.6,
            label="placebo (permuted W)")
    ax.axvline(0.0, color=FG_LINE, lw=1.2, ls=":", label="zero (expected null)")
    ax.axvline(real_est, color=HOT, lw=2.4,
               label=f"real estimate = {real_est:.2f}")
    ax.set_title("Placebo refuter: real effect vs. null cloud")
    ax.set_xlabel(r"estimated effect $\hat\tau$")
    ax.set_ylabel("density")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "refutation-histogram")


def main() -> None:
    apply_style()
    confounding_bias()
    evalue_curve()
    manski_bounds()
    refutation_histogram()


if __name__ == "__main__":
    main()
