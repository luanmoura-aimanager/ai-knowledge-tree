"""Figures for pillar G5 (time-series causal inference). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "G5"
C = color(SUB)  # pillar-G accent (teal)


def causalimpact_bsts() -> None:
    """CausalImpact fits a model on the pre-intervention period, projects the
    counterfactual ('what would have happened'), and attributes the gap between the
    actual series and that projection to the intervention. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, t0 = 120, 80
    base = 10 + 0.04 * np.arange(n) + np.sin(np.arange(n) / 7)
    actual = base + rng.normal(0, 0.4, n)
    actual[t0:] += 3.0                              # intervention effect
    counterfactual = base
    band = 0.8

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 5.0), sharex=True)
    ax1.plot(actual, color=C, lw=1.6, label="actual")
    ax1.plot(counterfactual, color=HOT, ls="--", lw=1.8, label="counterfactual")
    ax1.fill_between(range(n), counterfactual - 2 * band, counterfactual + 2 * band,
                     color=HOT, alpha=0.12)
    ax1.axvline(t0, color=FG_MUTE, ls=":", lw=1.4, label="intervention")
    ax1.set_title("Actual vs predicted counterfactual"); ax1.legend(loc="upper left", fontsize=8)
    cum = np.cumsum(actual - counterfactual); cum[:t0] = 0
    ax2.plot(cum, color=GOOD, lw=2.0)
    ax2.axhline(0, color=FG_MUTE, lw=0.8); ax2.axvline(t0, color=FG_MUTE, ls=":", lw=1.4)
    ax2.set_title("cumulative causal effect"); ax2.set_xlabel("time")
    fig.tight_layout()
    save(fig, SUB, "causalimpact-bsts")


def granger_causality() -> None:
    """X Granger-causes Y if X's past helps predict Y beyond Y's own past. Here Y is
    a lagged, noisy copy of X, so X's moves systematically precede Y's — visible as Y
    tracking X shifted forward in time. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, lag = 120, 5
    x = np.cumsum(rng.normal(0, 1, n))
    y = np.zeros(n)
    for t in range(lag, n):
        y[t] = 0.8 * y[t - 1] + 0.6 * x[t - lag] + rng.normal(0, 0.3)

    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.plot(x, color=C, lw=1.6, label="X")
    ax.plot(y, color=HOT, lw=1.6, label=f"Y (driven by X lagged {lag})")
    ax.set_title("Granger causality: X's past predicts Y")
    ax.set_xlabel("time"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "granger-causality")


def synthetic_control() -> None:
    """Synthetic control builds a 'clone' of the treated unit as a weighted blend of
    untreated donor units that matches it before the intervention; the post-treatment
    gap between the real unit and its synthetic twin is the estimated effect. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, t0 = 60, 40
    common = 20 + 0.1 * np.arange(n) + np.sin(np.arange(n) / 5)
    treated = common + rng.normal(0, 0.3, n)
    treated[t0:] += 4.0
    synthetic = common + rng.normal(0, 0.25, n)     # matched blend of donors

    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.plot(treated, color=C, lw=2.0, label="treated unit")
    ax.plot(synthetic, color=HOT, ls="--", lw=2.0, label="synthetic control")
    ax.fill_between(range(t0, n), synthetic[t0:], treated[t0:], color=GOOD, alpha=0.25,
                    label="estimated effect")
    ax.axvline(t0, color=FG_MUTE, ls=":", lw=1.4, label="treatment")
    ax.set_title("Synthetic control")
    ax.set_xlabel("time"); ax.set_ylabel("outcome")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "synthetic-control")


def main() -> None:
    apply_style()
    causalimpact_bsts()
    granger_causality()
    synthetic_control()


if __name__ == "__main__":
    main()
