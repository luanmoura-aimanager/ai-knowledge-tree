"""Figures for pillar M2 (heterogeneous treatment effects). See figures/gen/_style.py.

One function per figure, deterministic (np.random.default_rng(0)), written with
save(fig, SUB, name). Embedded in the M2 lessons via
![caption](/figures/M2/<name>.svg). sklearn is permitted here but numpy is
preferred; these stay numpy-only to mirror the runnable lesson blocks.
"""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, GOOD, HOT, apply_style, color, save

SUB = "M2"
C = color(SUB)  # pillar-M accent (#ee7de0)


def _lin_fit(xx, yy):
    A = np.column_stack([np.ones_like(xx), xx])
    return np.linalg.lstsq(A, yy, rcond=None)[0]


def meta_learners_imbalance() -> None:
    """Under 10% treatment, the S-learner (shrunk interaction) flattens toward
    the mean, the T-learner is noisy from its tiny treated sample, and the
    X-learner tracks the true CATE tau(x) = 1 + x. Mirrors meta-learners.mdx."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 6000
    x = rng.normal(0, 1, n)
    W = (rng.random(n) < 0.10).astype(float)  # heavy imbalance
    tau = 1.0 + x
    Y0 = 0.5 * x + rng.normal(0, 1, n)
    Y1 = Y0 + tau
    Y = W * Y1 + (1 - W) * Y0

    def pred(coef, xx):
        return coef[0] + coef[1] * xx

    c1, c0 = _lin_fit(x[W == 1], Y[W == 1]), _lin_fit(x[W == 0], Y[W == 0])
    tau_T = pred(c1, x) - pred(c0, x)

    # X-learner
    imp_t = Y[W == 1] - pred(c0, x[W == 1])
    imp_c = pred(c1, x[W == 0]) - Y[W == 0]
    d1, d0 = _lin_fit(x[W == 1], imp_t), _lin_fit(x[W == 0], imp_c)
    ex = W.mean()
    tau_X = ex * pred(d0, x) + (1 - ex) * pred(d1, x)

    # S-learner with heavily shrunk interaction (collapses toward a flat effect).
    Phi = np.column_stack([np.ones(n), x, W, x * W])
    R = 4000.0 * np.eye(4)
    R[0, 0] = R[1, 1] = 0.0  # penalize only treatment-related coefs
    beta = np.linalg.solve(Phi.T @ Phi + R, Phi.T @ Y)
    tau_S = beta[2] + beta[3] * x

    grid = np.linspace(-2.5, 2.5, 200)
    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    ax.plot(grid, 1.0 + grid, color=GOOD, lw=2.4, label="true $\\tau(x)=1+x$")
    ax.plot(grid, _eval_line(x, tau_S, grid), color=HOT, lw=2.0,
            label="S-learner (flattened)")
    ax.plot(grid, _eval_line(x, tau_T, grid), color=ACCENT, lw=2.0,
            label="T-learner (noisy)")
    ax.plot(grid, _eval_line(x, tau_X, grid), color=C, lw=2.2,
            label="X-learner (tracks)")
    ax.set_title("Meta-learners under 10% treatment")
    ax.set_xlabel("covariate $x$")
    ax.set_ylabel("estimated CATE $\\hat\\tau(x)$")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "meta-learners-imbalance")


def _eval_line(x, tau_vals, grid):
    """Fit a line to (x, tau_vals) and evaluate on grid, for a clean curve."""
    coef = _lin_fit(x, tau_vals)
    return coef[0] + coef[1] * grid


def r_learner_fit() -> None:
    """R-learner CATE estimate vs truth, with point sizes encoding the squared
    treatment-residual weights (W - e(x))^2: predictable-treatment units shrink.
    Mirrors r-learner.mdx."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 2500
    x = rng.normal(0, 1, n)
    e_true = 1 / (1 + np.exp(-0.8 * x))
    W = (rng.random(n) < e_true).astype(float)
    tau = 1.0 + x
    Y = tau * W + np.sin(x) + rng.normal(0, 0.5, n)

    B = np.column_stack([np.ones(n), x, x**2, x**3])
    m_hat = B @ np.linalg.lstsq(B, Y, rcond=None)[0]
    e_hat = B @ np.linalg.lstsq(B, W, rcond=None)[0]
    Yt, Wt = Y - m_hat, W - e_hat

    F = np.column_stack([Wt, x * Wt])
    a, b = np.linalg.lstsq(F, Yt, rcond=None)[0]

    weights = Wt**2
    sizes = 4 + 90 * (weights / weights.max())

    grid = np.linspace(-2.5, 2.5, 200)
    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    ax.scatter(x, np.where(np.abs(Wt) > 1e-6, Yt / Wt, np.nan),
               s=sizes, color=C, alpha=0.18, edgecolor="none",
               label="units (size $\\propto (W-e)^2$)")
    ax.plot(grid, 1.0 + grid, color=GOOD, lw=2.4, label="true $\\tau(x)=1+x$")
    ax.plot(grid, a + b * grid, color=HOT, lw=2.2, ls="--",
            label="R-learner fit")
    ax.set_ylim(-4, 6)
    ax.set_title("R-learner: weighted residual-on-residual fit")
    ax.set_xlabel("covariate $x$")
    ax.set_ylabel("CATE / pseudo-target")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "r-learner-fit")


def dr_learner_robustness() -> None:
    """DR-learner CATE vs truth under a deliberately wrong (flat) outcome model
    but a correct propensity: the doubly-robust correction recovers tau(x)=1+x.
    Mirrors dr-learner.mdx."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 40000
    x = rng.normal(0, 1, n)
    e_true = 1 / (1 + np.exp(-x))
    W = (rng.random(n) < e_true).astype(float)
    tau = 1.0 + x
    Y = 0.5 * x + tau * W + rng.normal(0, 0.5, n)

    # Wrong outcome models: global arm means. Correct propensity.
    mu0_hat = np.full(n, Y[W == 0].mean())
    mu1_hat = np.full(n, Y[W == 1].mean())
    B = np.column_stack([np.ones(n), x, x**2])
    e_hat = np.clip(B @ np.linalg.lstsq(B, W, rcond=None)[0], 0.02, 0.98)

    Gamma = (mu1_hat - mu0_hat) \
        + W * (Y - mu1_hat) / e_hat \
        - (1 - W) * (Y - mu0_hat) / (1 - e_hat)
    a, b = np.linalg.lstsq(np.column_stack([np.ones(n), x]), Gamma, rcond=None)[0]

    # Naive plug-in with the wrong outcome model (flat, badly biased).
    plug = mu1_hat - mu0_hat  # constant

    grid = np.linspace(-2.5, 2.5, 200)
    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    ax.plot(grid, 1.0 + grid, color=GOOD, lw=2.4, label="true $\\tau(x)=1+x$")
    ax.plot(grid, a + b * grid, color=C, lw=2.2, ls="--",
            label="DR-learner (recovers line)")
    ax.axhline(plug.mean(), color=HOT, lw=2.0, ls=":",
               label="plug-in, wrong outcome model")
    ax.set_title("DR-learner: doubly robust under wrong outcome model")
    ax.set_xlabel("covariate $x$")
    ax.set_ylabel("estimated CATE $\\hat\\tau(x)$")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "dr-learner-robustness")


def causal_forest_ci() -> None:
    """Honest causal-forest CATE with 95% bands across X0, against the true line
    tau(x) = 1 + x0. Mirrors generalized-random-forests.mdx (binned proxy CIs)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 6000
    X = rng.normal(0, 1, (n, 3))
    x0 = X[:, 0]
    e_true = 1 / (1 + np.exp(-0.6 * x0))
    W = (rng.random(n) < e_true).astype(float)
    tau = 1.0 + x0
    Y = 0.5 * x0 + tau * W + rng.normal(0, 0.5, n)

    # Residualize linearly in X.
    A = np.column_stack([np.ones(n), X])
    Yt = Y - A @ np.linalg.lstsq(A, Y, rcond=None)[0]
    Wt = W - A @ np.linalg.lstsq(A, W, rcond=None)[0]

    # Local moment solution in X0 bins (stand-in for the forest's local weights),
    # with a bootstrap-free CI from the per-bin slope's standard error.
    edges = np.linspace(-2.2, 2.2, 13)
    centers, est, se = [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (x0 >= lo) & (x0 < hi)
        if m.sum() < 30:
            continue
        wt, yt = Wt[m], Yt[m]
        denom = (wt**2).sum()
        t = (wt * yt).sum() / denom
        resid = yt - t * wt
        var = (wt**2 * resid**2).sum() / denom**2  # sandwich-style variance
        centers.append(0.5 * (lo + hi))
        est.append(t)
        se.append(np.sqrt(var))
    centers, est, se = map(np.array, (centers, est, se))

    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    grid = np.linspace(-2.2, 2.2, 200)
    ax.plot(grid, 1.0 + grid, color=GOOD, lw=2.4, label="true $\\tau(x)=1+x_0$")
    ax.fill_between(centers, est - 1.96 * se, est + 1.96 * se,
                    color=C, alpha=0.25, label="95% interval")
    ax.plot(centers, est, color=C, lw=2.2, marker="o", ms=4,
            label="causal forest $\\hat\\tau$")
    ax.set_title("Causal-forest CATE with honest confidence bands")
    ax.set_xlabel("covariate $x_0$")
    ax.set_ylabel("estimated CATE $\\hat\\tau(x_0)$")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "causal-forest-ci")


def qini_curve() -> None:
    """Qini curve of an uplift model bowing above the random-targeting diagonal;
    the shaded area is the Qini coefficient. Mirrors uplift-modeling.mdx."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 20000
    x = rng.uniform(-1, 1, n)
    W = (rng.random(n) < 0.5).astype(float)
    p0 = 0.3 + 0.0 * x
    uplift = 0.4 * x
    p1 = np.clip(p0 + uplift, 0, 1)
    Y = np.where(W == 1, rng.random(n) < p1, rng.random(n) < p0).astype(float)

    bins = np.linspace(-1, 1, 21)
    b = np.clip(np.digitize(x, bins), 1, len(bins) - 1)
    score = np.zeros(n)
    for k in np.unique(b):
        m = b == k
        t, c = m & (W == 1), m & (W == 0)
        if t.sum() and c.sum():
            score[m] = Y[t].mean() - Y[c].mean()

    order = np.argsort(-score)
    Ws, Ys = W[order], Y[order]
    nt, nc = np.cumsum(Ws), np.cumsum(1 - Ws)
    yt, yc = np.cumsum(Ys * Ws), np.cumsum(Ys * (1 - Ws))
    with np.errstate(divide="ignore", invalid="ignore"):
        qini = yt - yc * np.where(nc > 0, nt / nc, 0.0)
    phi = np.arange(1, n + 1) / n
    diag = phi * qini[-1]

    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    ax.fill_between(phi, diag, qini, where=(qini >= diag), color=C, alpha=0.25,
                    label="Qini coefficient (area)")
    ax.plot(phi, qini, color=C, lw=2.4, label="uplift model")
    ax.plot(phi, diag, color=FG_DIM, lw=1.8, ls="--", label="random targeting")
    ax.set_title("Qini curve: uplift ranking vs random")
    ax.set_xlabel("fraction of population targeted $\\phi$")
    ax.set_ylabel("cumulative incremental conversions")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "qini-curve")


def main() -> None:
    meta_learners_imbalance()
    r_learner_fit()
    dr_learner_robustness()
    causal_forest_ci()
    qini_curve()


if __name__ == "__main__":
    apply_style()
    main()
