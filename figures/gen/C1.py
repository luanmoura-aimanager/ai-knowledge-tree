"""Figures for pillar C1 (linear models). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import (ACCENT, CYCLE, FG_MUTE, GOOD, GRID, HOT, LEGEND_BG,
                    apply_style, color, save)

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
    ax.axhline(sigma**2, color=FG_MUTE, ls="--", lw=1.2, label=f"noise floor $\\sigma^2$={sigma**2:.2f}")

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


def ridge_regression() -> None:
    """Ridge coefficient paths: every coefficient shrinks smoothly toward 0 as λ
    grows. Lesson's setup: rng(0), n=30, d=12."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n, d = 30, 12
    X = rng.normal(size=(n, d))
    X[:, 0] = 1.0
    beta_true = rng.normal(size=d)
    y = X @ beta_true + 0.3 * rng.normal(size=n)

    lams = np.logspace(-2, 3, 80)
    XtX, Xty = X.T @ X, X.T @ y
    paths = np.array([np.linalg.solve(XtX + lam * np.eye(d), Xty) for lam in lams])

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for j in range(d):
        ax.plot(lams, paths[:, j], color=CYCLE[j % len(CYCLE)], lw=1.5, alpha=0.9)
    ax.axhline(0, color=FG_MUTE, lw=0.8)
    ax.set_xscale("log")
    ax.set_title("Ridge coefficient paths: smooth shrinkage")
    ax.set_xlabel("regularization $\\lambda$")
    ax.set_ylabel("coefficient value")
    fig.tight_layout()
    save(fig, SUB, "ridge-regression")


def lasso() -> None:
    """LASSO coefficient paths: as λ grows, coefficients hit exactly zero one by
    one (sparsity). The few true-nonzero coordinates survive longest. rng(0),
    n=150, d=200, k=8 true nonzeros."""
    import matplotlib.pyplot as plt
    from sklearn.linear_model import lasso_path

    rng = np.random.default_rng(0)
    n, d, k = 150, 200, 8
    A = rng.normal(size=(n, d)) / np.sqrt(n)
    beta_true = np.zeros(d)
    support = rng.choice(d, k, replace=False)
    beta_true[support] = rng.normal(size=k) * 3
    y = A @ beta_true + 0.01 * rng.normal(size=n)

    alphas, coefs, _ = lasso_path(A, y, n_alphas=120)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    true_set = set(support.tolist())
    for j in range(d):
        if j in true_set:
            ax.plot(alphas, coefs[j], color=C, lw=1.8, zorder=3)
        else:
            ax.plot(alphas, coefs[j], color=FG_MUTE, lw=0.6, alpha=0.5)
    ax.set_xscale("log")
    ax.invert_xaxis()  # strong→weak regularization left→right
    ax.axhline(0, color=FG_MUTE, lw=0.8)
    ax.plot([], [], color=C, lw=1.8, label=f"{k} true-nonzero coefs")
    ax.plot([], [], color=FG_MUTE, lw=1.0, label="192 true-zero coefs")
    ax.set_title("LASSO paths: coefficients hit exactly zero")
    ax.set_xlabel("regularization $\\lambda$  (strong → weak)")
    ax.set_ylabel("coefficient value")
    ax.legend(loc="upper left")
    fig.tight_layout()
    save(fig, SUB, "lasso")


def elastic_net() -> None:
    """The constraint-ball geometry behind the three penalties: the L1 diamond
    has corners (→ exact zeros / sparsity), the L2 circle is smooth (no corners),
    and elastic-net blends them — corners kept, edges rounded."""
    import matplotlib.pyplot as plt

    t = np.linspace(0, 2 * np.pi, 400)
    g = np.linspace(-1.3, 1.3, 400)
    gx, gy = np.meshgrid(g, g)

    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    # L2 ball: circle
    ax.plot(np.cos(t), np.sin(t), color=ACCENT, lw=2.0, label="L2 (ridge)")
    # L1 ball: diamond |x|+|y|=1
    ax.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], color=HOT, lw=2.0, label="L1 (lasso)")
    # Elastic net: alpha|.|1 + (1-alpha)|.|2^2 = 1, alpha=0.5
    a = 0.5
    enet = a * (np.abs(gx) + np.abs(gy)) + (1 - a) * (gx**2 + gy**2)
    ax.contour(gx, gy, enet, levels=[1.0], colors=[C], linewidths=2.4)
    ax.plot([], [], color=C, lw=2.4, label="elastic net (α=0.5)")

    ax.set_aspect("equal")
    ax.axhline(0, color=GRID, lw=0.8)
    ax.axvline(0, color=GRID, lw=0.8)
    ax.set_title("Penalty balls: corners make sparsity")
    ax.set_xlabel("$\\beta_1$")
    ax.set_ylabel("$\\beta_2$")
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "elastic-net")


def logistic_regression() -> None:
    """Left: the logistic sigmoid mapping a score to a probability. Right: the
    resulting linear decision boundary and probability contours on 2D data."""
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LogisticRegression

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.8))

    z = np.linspace(-6, 6, 300)
    ax1.plot(z, 1 / (1 + np.exp(-z)), color=C, lw=2.4)
    ax1.axhline(0.5, color=FG_MUTE, ls=":", lw=1.0)
    ax1.axvline(0, color=FG_MUTE, ls=":", lw=1.0)
    ax1.set_title("The logistic sigmoid")
    ax1.set_xlabel("score $z = x^\\top\\beta$")
    ax1.set_ylabel("$P(y=1)$")

    rng = np.random.default_rng(0)
    n = 200
    X = np.vstack([rng.normal([1.6, 0.6], 0.9, (n, 2)),
                   rng.normal([-1.2, -0.6], 0.9, (n, 2))])
    yb = np.array([1] * n + [0] * n)
    clf = LogisticRegression().fit(X, yb)
    gx, gy = np.meshgrid(np.linspace(-4, 4, 250), np.linspace(-4, 4, 250))
    P = clf.predict_proba(np.c_[gx.ravel(), gy.ravel()])[:, 1].reshape(gx.shape)
    cf = ax2.contourf(gx, gy, P, levels=12, cmap="RdBu_r", alpha=0.7, vmin=0, vmax=1)
    ax2.contour(gx, gy, P, levels=[0.5], colors=[FG_MUTE], linewidths=2.0)
    ax2.scatter(X[yb == 1, 0], X[yb == 1, 1], s=10, color=HOT, edgecolor="none")
    ax2.scatter(X[yb == 0, 0], X[yb == 0, 1], s=10, color=ACCENT, edgecolor="none")
    ax2.set_title("Decision boundary (P = 0.5)")
    ax2.set_xlabel("$x_1$")
    ax2.set_ylabel("$x_2$")
    cb = fig.colorbar(cf, ax=ax2, fraction=0.046, pad=0.04)
    cb.ax.tick_params(colors=FG_MUTE)
    cb.outline.set_edgecolor(GRID)
    fig.tight_layout()
    save(fig, SUB, "logistic-regression")


def softmax_regression() -> None:
    """Softmax (multinomial logistic) regression carves the plane into three
    decision regions with linear boundaries. Lesson's three blobs at [2,0],
    [-2,0], [0,2], rng(0)."""
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LogisticRegression

    rng = np.random.default_rng(0)
    npc = 200
    X = np.vstack([rng.normal([2, 0], 0.8, (npc, 2)),
                   rng.normal([-2, 0], 0.8, (npc, 2)),
                   rng.normal([0, 2], 0.8, (npc, 2))])
    y3 = np.array([0] * npc + [1] * npc + [2] * npc)
    clf = LogisticRegression().fit(X, y3)

    gx, gy = np.meshgrid(np.linspace(-5, 5, 300), np.linspace(-3, 5, 300))
    Z = clf.predict(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)

    from matplotlib.colors import ListedColormap
    cols = [ACCENT, HOT, GOOD]
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    ax.contourf(gx, gy, Z, levels=[-0.5, 0.5, 1.5, 2.5],
                colors=cols, alpha=0.25)
    for c in range(3):
        ax.scatter(X[y3 == c, 0], X[y3 == c, 1], s=12, color=cols[c], edgecolor="none")
    ax.set_title("Softmax regression: three linear decision regions")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    fig.tight_layout()
    save(fig, SUB, "softmax-regression")


def linear_regression_ols() -> None:
    """OLS as projection: the fit minimizes the sum of squared residuals — the
    vertical gaps from each point to the line."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 40
    x = np.sort(rng.uniform(-3, 3, n))
    y = 1.0 + 0.8 * x + rng.normal(0, 1.0, n)
    Xd = np.column_stack([np.ones(n), x])
    beta = np.linalg.lstsq(Xd, y, rcond=None)[0]
    yhat = Xd @ beta

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    for xi, yi, yh in zip(x, y, yhat):
        ax.plot([xi, xi], [yi, yh], color=HOT, lw=1.0, alpha=0.7)
    ax.scatter(x, y, s=22, color=C, edgecolor="none", zorder=3, label="data")
    xs = np.array([x.min(), x.max()])
    ax.plot(xs, beta[0] + beta[1] * xs, color=ACCENT, lw=2.2, label="OLS fit")
    ax.plot([], [], color=HOT, lw=1.0, label="residuals")
    ax.set_title("OLS minimizes the squared residuals")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(loc="upper left", frameon=True, facecolor=LEGEND_BG,
              edgecolor=GRID, framealpha=0.92)
    fig.tight_layout()
    save(fig, SUB, "linear-regression-ols")


def linear_regression_mle() -> None:
    """OLS = Gaussian MLE: the log-likelihood surface over (slope, noise σ) peaks
    exactly at the least-squares slope and the residual standard deviation."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(1)
    n = 80
    x = rng.normal(size=n)
    beta_true, sigma_true = 2.5, 0.7
    y = 1.0 + beta_true * x + sigma_true * rng.normal(size=n)
    # profile out the intercept at its OLS value; vary slope b and sigma
    xc, yc = x - x.mean(), y - y.mean()
    b_hat = (xc @ yc) / (xc @ xc)
    resid = yc - b_hat * xc
    s_hat = np.sqrt((resid**2).mean())

    bs = np.linspace(b_hat - 1.2, b_hat + 1.2, 220)
    ss = np.linspace(0.35, 1.4, 220)
    B, S = np.meshgrid(bs, ss)
    sse = np.array([((yc - b * xc) ** 2).sum() for b in bs])  # over b only
    ll = -n * np.log(S) - sse[None, :] / (2 * S**2) - 0.5 * n * np.log(2 * np.pi)

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    cf = ax.contourf(B, S, ll, levels=25, cmap="viridis")
    ax.contour(B, S, ll, levels=12, colors=GRID, linewidths=0.5)
    ax.plot(b_hat, s_hat, "*", color=HOT, ms=16)
    ax.annotate(f"MLE  $\\hat\\beta={b_hat:.2f},\\ \\hat\\sigma={s_hat:.2f}$",
                xy=(b_hat, s_hat), xytext=(b_hat - 1.05, 1.18), color="#ffffff",
                fontsize=10, arrowprops=dict(arrowstyle="->", color=HOT, lw=1.4))
    ax.set_title("Gaussian log-likelihood surface")
    ax.set_xlabel("slope $\\beta$")
    ax.set_ylabel("noise $\\sigma$")
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.ax.tick_params(colors=FG_MUTE)
    cb.outline.set_edgecolor(GRID)
    cb.set_label("log-likelihood", color=FG_MUTE)
    fig.tight_layout()
    save(fig, SUB, "linear-regression-mle")


def main() -> None:
    apply_style()
    bias_variance()
    ridge_regression()
    lasso()
    elastic_net()
    logistic_regression()
    softmax_regression()
    linear_regression_ols()
    linear_regression_mle()


if __name__ == "__main__":
    main()
