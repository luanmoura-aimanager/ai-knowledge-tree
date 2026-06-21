"""Figures for pillar M3 (orthogonal & semiparametric estimation).

See figures/gen/_style.py. Deterministic (rng(0)); run via `npm run figures`.
"""

from __future__ import annotations

import numpy as np

from _style import ACCENT, GOOD, HOT, apply_style, color, save

SUB = "M3"
C = color(SUB)  # pillar-M accent


def _make_data(rng, n):
    """Confounded design with a constant true ATE = 1.0 (matches aipw.mdx)."""
    X = rng.normal(0, 1, n)
    e_star = 1 / (1 + np.exp(-0.8 * X))
    W = (rng.uniform(size=n) < e_star).astype(float)
    mu0_star = 0.5 * X
    mu1_star = 0.5 * X + 1.0
    Y = np.where(W == 1, mu1_star, mu0_star) + rng.normal(0, 0.5, n)
    return X, e_star, W, mu0_star, mu1_star, Y


def _aipw(W, Y, mu0, mu1, e):
    e = np.clip(e, 1e-3, 1 - 1e-3)
    return (mu1 - mu0
            + W * (Y - mu1) / e
            - (1 - W) * (Y - mu0) / (1 - e)).mean()


def double_robustness() -> None:
    """AIPW stays centered on the true ATE whenever the outcome model OR the
    propensity model is correct; only when both are wrong is it biased. Sampling
    distribution over repeated datasets in four misspecification regimes.
    Lesson aipw.mdx: true ATE = 1.0, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    true_ate = 1.0
    n, reps = 3000, 800

    regimes = {
        "both correct": (True, True),
        "outcome OK,\nprop. wrong": (True, False),
        "prop. OK,\noutcome wrong": (False, True),
        "both wrong": (False, False),
    }
    cols = [GOOD, ACCENT, C, HOT]
    ests = {k: np.empty(reps) for k in regimes}

    for r in range(reps):
        rg = np.random.default_rng(1000 + r)
        X, e_star, W, mu0_s, mu1_s, Y = _make_data(rg, n)
        wrong_mu0 = np.zeros(n)
        wrong_mu1 = np.zeros(n)
        wrong_e = np.full(n, 0.5)
        for k, (mu_ok, e_ok) in regimes.items():
            mu0 = mu0_s if mu_ok else wrong_mu0
            mu1 = mu1_s if mu_ok else wrong_mu1
            e = e_star if e_ok else wrong_e
            ests[k][r] = _aipw(W, Y, mu0, mu1, e)

    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    bins = np.linspace(0.5, 1.8, 46)
    for (k, vals), col in zip(ests.items(), cols):
        ax.hist(vals, bins=bins, density=True, alpha=0.55, color=col,
                label=f"{k} (mean {vals.mean():.2f})")
    ax.axvline(true_ate, color=GOOD, lw=2.0, ls="--", label="true ATE = 1.0")
    ax.set_title("Double robustness of AIPW")
    ax.set_xlabel(r"$\hat\theta_{\mathrm{AIPW}}$")
    ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=8.5)
    fig.tight_layout()
    save(fig, SUB, "double-robustness")


def sampling_normal() -> None:
    """Cross-fit AIPW point estimates across repeated datasets form a normal-
    looking sampling distribution; overlay the normal density implied by the
    influence-function standard error, justifying the Wald interval.
    Lesson dml-inference.mdx: true ATE = 1.0, good overlap, rng(0)."""
    import matplotlib.pyplot as plt

    true_ate = 1.0
    n, reps = 2000, 1200
    B_cols = 3  # [1, x, x^2]

    thetas = np.empty(reps)
    ses = np.empty(reps)
    for s in range(reps):
        r = np.random.default_rng(s + 1)
        X = r.normal(0, 1, n)
        e = 1 / (1 + np.exp(-0.8 * X))
        W = (r.uniform(size=n) < e).astype(float)
        g1, g0 = 0.5 * X + 1.0, 0.5 * X
        Y = np.where(W == 1, g1, g0) + r.normal(0, 0.5, n)
        Bm = np.column_stack([np.ones(n), X, X**2])
        idx = r.permutation(n)
        folds = [idx[:n // 2], idx[n // 2:]]
        phi = np.zeros(n)
        for k in range(2):
            te, tr = folds[k], folds[1 - k]
            m1 = (W[tr] == 1)
            m0 = (W[tr] == 0)
            mu1 = Bm[te] @ np.linalg.lstsq(Bm[tr][m1], Y[tr][m1], rcond=None)[0]
            mu0 = Bm[te] @ np.linalg.lstsq(Bm[tr][m0], Y[tr][m0], rcond=None)[0]
            eh = np.clip(Bm[te] @ np.linalg.lstsq(Bm[tr], W[tr], rcond=None)[0],
                         0.02, 0.98)
            phi[te] = (mu1 - mu0
                       + W[te] * (Y[te] - mu1) / eh
                       - (1 - W[te]) * (Y[te] - mu0) / (1 - eh))
        thetas[s] = phi.mean()
        ses[s] = phi.std() / np.sqrt(n)

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.hist(thetas, bins=40, density=True, color=C, alpha=0.6,
            label="cross-fit AIPW estimates")
    # Normal density implied by the mean influence-function SE.
    se_bar = ses.mean()
    xs = np.linspace(thetas.min(), thetas.max(), 300)
    pdf = np.exp(-0.5 * ((xs - true_ate) / se_bar) ** 2) / (se_bar * np.sqrt(2 * np.pi))
    ax.plot(xs, pdf, color=GOOD, lw=2.2,
            label=f"N(1.0, se={se_bar:.3f}) from IF")
    ax.axvline(true_ate, color=HOT, lw=1.6, ls="--", label="true ATE = 1.0")
    ax.set_title("Sampling distribution of cross-fit AIPW")
    ax.set_xlabel(r"$\hat\theta$")
    ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "sampling-normal")


def main() -> None:
    apply_style()
    double_robustness()
    sampling_normal()


if __name__ == "__main__":
    main()
