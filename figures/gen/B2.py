"""Figures for pillar B2 (Bayesian inference). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, CYCLE, FG_MUTE, GRID, HOT, apply_style, color, save

SUB = "B2"
C = color(SUB)  # pillar-B accent


def prior_likelihood_posterior() -> None:
    """Bayesian updating: a Beta(2,2) prior combined with Binomial data gives a
    Beta posterior that concentrates on the truth (θ=0.3) as n grows. Lesson's
    setup, rng(0)."""
    import matplotlib.pyplot as plt
    from scipy.stats import beta

    rng = np.random.default_rng(0)
    theta_true = 0.3
    a0, b0 = 2.0, 2.0
    g = np.linspace(0, 1, 500)
    data = rng.binomial(1, theta_true, 500)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(g, beta.pdf(g, a0, b0), color=FG_MUTE, lw=2.0, ls="--", label="prior Beta(2,2)")
    for n, col in zip([5, 20, 100, 500], CYCLE):
        k = data[:n].sum()
        ax.plot(g, beta.pdf(g, a0 + k, b0 + n - k), color=col, lw=2.0, label=f"posterior, n={n}")
    ax.axvline(theta_true, color=HOT, ls=":", lw=1.4, label="θ = 0.3")
    ax.set_title("Posterior concentrates as data accrues")
    ax.set_xlabel("θ")
    ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "prior-likelihood-posterior")


def conjugate_priors() -> None:
    """Conjugacy: a Beta prior stays Beta after Bernoulli data — each batch's
    posterior becomes the next batch's prior. Coin with θ=0.6, rng(0)."""
    import matplotlib.pyplot as plt
    from scipy.stats import beta

    rng = np.random.default_rng(0)
    theta = 0.6
    g = np.linspace(0, 1, 500)
    data = rng.binomial(1, theta, 200)
    a, b = 1.0, 1.0  # uniform prior

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(g, beta.pdf(g, a, b), color=FG_MUTE, lw=1.8, ls="--", label="prior Beta(1,1)")
    seen = 0
    for batch, col in zip([10, 30, 60, 100], CYCLE):
        chunk = data[seen:batch]
        a += chunk.sum()
        b += len(chunk) - chunk.sum()
        seen = batch
        ax.plot(g, beta.pdf(g, a, b), color=col, lw=2.0, label=f"after {batch} flips")
    ax.axvline(theta, color=HOT, ls=":", lw=1.4, label="θ = 0.6")
    ax.set_title("Sequential Beta updates stay Beta")
    ax.set_xlabel("θ")
    ax.set_ylabel("density")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "conjugate-priors")


def hierarchical_models() -> None:
    """Partial pooling shrinks each group's estimate toward the global mean by an
    amount set by its sample size — small groups borrow more strength. J=8 groups,
    μ=50, τ=10, σ=15, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    J, mu, tau, sigma = 8, 50.0, 10.0, 15.0
    ns = np.sort(rng.integers(5, 40, J))
    theta = rng.normal(mu, tau, J)
    ybar = np.array([rng.normal(t, sigma / np.sqrt(n)) for t, n in zip(theta, ns)])
    grand = ybar.mean()
    lam = tau**2 / (tau**2 + sigma**2 / ns)          # shrinkage weight
    partial = lam * ybar + (1 - lam) * grand

    x = np.arange(J)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.scatter(x, ybar, s=55, color=C, label="no pooling (group mean)", zorder=3)
    ax.scatter(x, partial, s=55, marker="D", color=ACCENT, label="partial pooling", zorder=3)
    for i in range(J):
        ax.plot([i, i], [ybar[i], partial[i]], color=FG_MUTE, lw=1.0, alpha=0.7)
    ax.axhline(grand, color=HOT, ls="--", lw=1.6, label="complete pooling (grand mean)")
    ax.set_title("Shrinkage: partial pooling pulls toward the mean")
    ax.set_xlabel("group (sorted by sample size →)")
    ax.set_ylabel("estimated mean")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "hierarchical-models")


def main() -> None:
    apply_style()
    prior_likelihood_posterior()
    conjugate_priors()
    hierarchical_models()


if __name__ == "__main__":
    main()
