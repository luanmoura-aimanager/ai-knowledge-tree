"""Figures for pillar F8 (Bayesian deep learning & UQ). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import GOOD, HOT, apply_style, color, save

SUB = "F8"
C = color(SUB)  # pillar-F accent (cyan)


def _gp(xt, yt, xs, ell=1.0, sf=1.0, sn=0.05):
    k = lambda a, b: sf**2 * np.exp(-0.5 * (a[:, None] - b[None, :]) ** 2 / ell**2)
    K = k(xt, xt) + sn**2 * np.eye(len(xt))
    L = np.linalg.cholesky(K)
    alpha = np.linalg.solve(L.T, np.linalg.solve(L, yt))
    mu = k(xs, xt) @ alpha
    v = np.linalg.solve(L, k(xs, xt).T)
    var = np.clip(np.diag(k(xs, xs)) - np.sum(v**2, axis=0), 1e-9, None)
    return mu, np.sqrt(var), L, alpha, k


def bayesian_neural_networks() -> None:
    """A Bayesian neural network puts a distribution over weights, so its predictions
    come with uncertainty: the band is tight where data is dense and widens in the
    gaps and beyond the data — honest 'I don't know'. (Shown with a GP, the BNN's
    infinite-width limit.) rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    xt = np.concatenate([rng.uniform(-4, -1, 8), rng.uniform(1, 4, 8)])
    yt = np.sin(xt) + 0.1 * rng.normal(size=xt.size)
    xs = np.linspace(-6, 6, 300)
    mu, sd, *_ = _gp(xt, yt, xs, ell=1.0)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.fill_between(xs, mu - 2 * sd, mu + 2 * sd, color=C, alpha=0.2, label="±2σ predictive")
    ax.plot(xs, mu, color=C, lw=2.2, label="predictive mean")
    ax.scatter(xt, yt, s=24, color=HOT, zorder=5, label="training data")
    ax.set_title("BNN predictive uncertainty widens off-data")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.legend(loc="upper center", fontsize=8, ncol=3)
    fig.tight_layout()
    save(fig, SUB, "bayesian-neural-networks")


def conformal_prediction() -> None:
    """Conformal prediction wraps any model in a calibrated interval: pick the
    quantile of calibration residuals and the band ±q achieves the target coverage
    (here ~90%) with no distributional assumptions. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    f = lambda x: 1.5 * np.sin(x)
    xc = rng.uniform(-4, 4, 2000); yc = f(xc) + 0.5 * rng.normal(size=xc.size)
    resid = np.abs(yc - f(xc))
    q = np.quantile(resid, 0.90)
    xt = rng.uniform(-4, 4, 600); yt = f(xt) + 0.5 * rng.normal(size=xt.size)
    inside = np.abs(yt - f(xt)) <= q
    xs = np.linspace(-4, 4, 200)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.fill_between(xs, f(xs) - q, f(xs) + q, color=C, alpha=0.2,
                    label=f"90% conformal band (±{q:.2f})")
    ax.plot(xs, f(xs), color=C, lw=2.2, label="prediction")
    ax.scatter(xt[inside], yt[inside], s=10, color=GOOD, alpha=0.6, label="covered")
    ax.scatter(xt[~inside], yt[~inside], s=14, color=HOT, alpha=0.8, label="missed")
    ax.set_title(f"Conformal prediction (empirical coverage {inside.mean()*100:.0f}%)")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.legend(loc="upper center", fontsize=8, ncol=2)
    fig.tight_layout()
    save(fig, SUB, "conformal-prediction")


def mc_dropout_ensembles() -> None:
    """MC dropout (and deep ensembles) estimate uncertainty by sampling many
    predictors: each forward pass is a slightly different function, and their spread
    is the predictive uncertainty — narrow on data, fanning out where the model
    extrapolates. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    xt = np.linspace(-3, 3, 12)
    yt = np.sin(xt)
    xs = np.linspace(-6, 6, 300)
    mu, sd, L, alpha, k = _gp(xt, yt, xs, ell=1.1, sn=0.08)
    Ks = k(xs, xs) + 1e-6 * np.eye(len(xs))
    v = np.linalg.solve(L, k(xs, xt).T)
    cov = Ks - v.T @ v
    Lc = np.linalg.cholesky(cov + 1e-6 * np.eye(len(xs)))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for _ in range(20):
        samp = mu + Lc @ rng.normal(size=len(xs))
        ax.plot(xs, samp, color=C, lw=0.7, alpha=0.35)
    ax.plot(xs, mu, color=HOT, lw=2.4, label="mean prediction")
    ax.scatter(xt, yt, s=22, color=GOOD, zorder=5, label="training data")
    ax.plot([], [], color=C, lw=0.7, label="sampled predictors")
    ax.set_ylim(-3, 3)
    ax.set_title("MC dropout / ensembles: a spread of functions")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.legend(loc="upper center", fontsize=8, ncol=3)
    fig.tight_layout()
    save(fig, SUB, "mc-dropout-ensembles")


def main() -> None:
    apply_style()
    bayesian_neural_networks()
    conformal_prediction()
    mc_dropout_ensembles()


if __name__ == "__main__":
    main()
