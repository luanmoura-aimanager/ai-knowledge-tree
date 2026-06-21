"""Figures for pillar M4 (deep causal inference).

See figures/gen/_style.py. Deterministic (rng(0)); run via `npm run figures`.
All plots are numpy/matplotlib only: they illustrate the concepts behind the
neural models (covariate imbalance, IPM shrinkage, PEHE vs balancing weight),
not trained networks, so they reproduce byte-identically without torch.
"""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, GOOD, HOT, LEGEND_BG, apply_style, color, save

SUB = "M4"
C = color(SUB)  # pillar-M accent (#ee7de0)


def _mmd_rbf(a, b, gamma):
    """Squared maximum mean discrepancy with an RBF kernel between samples a, b
    (both shape (n, d)). Unbiased-ish estimate using all pairs."""
    def k(x, y):
        d2 = ((x[:, None, :] - y[None, :, :]) ** 2).sum(-1)
        return np.exp(-gamma * d2)
    return k(a, a).mean() + k(b, b).mean() - 2 * k(a, b).mean()


def imbalance_balance() -> None:
    """Treatment selection puts treated and control covariates on different
    distributions (left); a learned representation Phi that the balancing penalty
    pulls together makes the two pushforward distributions overlap (right). The
    counterfactual error bound shrinks with this overlap. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 600
    # Confounded covariate: treated units drawn from a higher-mean Gaussian.
    x_ctrl = rng.normal(-1.0, 0.8, n)
    x_trt = rng.normal(1.3, 0.8, n)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    bins = np.linspace(-4, 4, 36)
    ax1.hist(x_ctrl, bins=bins, density=True, color=ACCENT, alpha=0.6,
             label="control")
    ax1.hist(x_trt, bins=bins, density=True, color=HOT, alpha=0.6,
             label="treated")
    ax1.set_title("Covariate $X$: treated vs control\n(selection imbalance)")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("density")
    ax1.legend(loc="upper left", fontsize=9, facecolor=LEGEND_BG, framealpha=0.9)

    # A balancing representation contracts the treated branch toward the control
    # one: model Phi(x) = x for control, Phi(x) = 0.25*x - 0.9 for treated, so the
    # two pushforwards land on top of each other while keeping within-group spread.
    phi_ctrl = x_ctrl
    phi_trt = 0.25 * x_trt - 0.9
    ax2.hist(phi_ctrl, bins=bins, density=True, color=ACCENT, alpha=0.6,
             label="control")
    ax2.hist(phi_trt, bins=bins, density=True, color=HOT, alpha=0.6,
             label="treated")
    ax2.set_title("Representation $\\Phi(X)$\n(after balancing penalty)")
    ax2.set_xlabel("$\\Phi(x)$")
    ax2.set_ylabel("density")
    ax2.legend(loc="upper left", fontsize=9, facecolor=LEGEND_BG, framealpha=0.9)
    fig.tight_layout()
    save(fig, SUB, "imbalance-balance")


def ipm_shrinks() -> None:
    """As a balancing knob interpolates the treated branch from raw covariate
    (imbalanced) toward the control distribution (balanced), the MMD between the
    two representation samples falls toward zero. This is the IPM term the CFR
    objective penalizes. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 300
    x_ctrl = rng.normal(-1.0, 0.8, n).reshape(-1, 1)
    x_trt = rng.normal(1.3, 0.8, n).reshape(-1, 1)
    gamma = 0.5

    # t = 0: no balancing (raw imbalanced covariate). t = 1: treated branch
    # mapped to match the control mean and spread exactly.
    ts = np.linspace(0.0, 1.0, 21)
    mmds = []
    target_mean, target_std = x_ctrl.mean(), x_ctrl.std()
    trt_std = x_trt.std()
    for t in ts:
        # affine map of the treated branch toward the control distribution:
        # at t=1 the scaled branch matches the control std, then its mean is
        # pulled onto the control mean.
        scale = (1 - t) + t * (target_std / trt_std)
        phi_trt = x_trt * scale
        phi_trt = phi_trt + (target_mean - phi_trt.mean()) * t
        mmds.append(_mmd_rbf(x_ctrl, phi_trt, gamma))

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(ts, mmds, color=C, lw=2.4, marker="o", ms=4)
    ax.set_title("IPM (RBF-MMD) between representation branches\nshrinks as"
                 " balancing increases")
    ax.set_xlabel("balancing strength $t$ (0 = raw covariate, 1 = matched)")
    ax.set_ylabel(r"$\mathrm{MMD}^2(\{\Phi(x):w=1\},\{\Phi(x):w=0\})$")
    ax.axhline(0, color=FG_DIM, lw=1.0, ls=":")
    fig.tight_layout()
    save(fig, SUB, "ipm-shrinks")


def pehe_vs_alpha() -> None:
    """Synthetic PEHE-vs-balancing-weight curve: too little balancing leaves
    counterfactual extrapolation error; too much erases predictive signal in the
    representation. The error is U-shaped with an interior optimum. Illustrative
    (a smooth convex-plus-linear model), not a trained net. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    alphas = np.logspace(-3, 1.2, 40)
    # variance-style term that falls with balancing + bias-style term that rises
    # as the penalty crushes outcome-relevant structure.
    extrapolation = 0.9 / (1.0 + 6.0 * alphas)        # falls with balancing
    signal_loss = 0.18 * alphas                         # rises with over-balancing
    noise = rng.normal(0, 0.012, alphas.size)
    pehe = extrapolation + signal_loss + 0.18 + noise
    j = int(np.argmin(pehe))

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(alphas, pehe, color=C, lw=2.4, label=r"$\sqrt{\mathrm{PEHE}}$")
    ax.plot(alphas, extrapolation + 0.18, color=ACCENT, lw=1.6, ls="--",
            label="counterfactual extrapolation")
    ax.plot(alphas, signal_loss + 0.18, color=HOT, lw=1.6, ls="--",
            label="lost outcome signal")
    ax.axvline(alphas[j], color=GOOD, lw=1.8, ls=":",
               label=f"best $\\alpha \\approx$ {alphas[j]:.2f}")
    ax.set_xscale("log")
    ax.set_title("Counterfactual error vs balancing weight $\\alpha$")
    ax.set_xlabel(r"balancing weight $\alpha$ (log scale)")
    ax.set_ylabel(r"$\sqrt{\mathrm{PEHE}}$ (lower is better)")
    ax.legend(loc="upper center", fontsize=9, facecolor=LEGEND_BG, framealpha=0.9)
    fig.tight_layout()
    save(fig, SUB, "pehe-vs-alpha")


def main() -> None:
    apply_style()
    imbalance_balance()
    ipm_shrinks()
    pehe_vs_alpha()


if __name__ == "__main__":
    main()
