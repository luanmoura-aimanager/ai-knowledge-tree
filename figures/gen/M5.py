"""Figures for pillar M5 (policy learning & off-policy evaluation).

See figures/gen/_style.py. Numpy-only, deterministic (rng(0)). Run with
`npm run figures`; do not hand-edit the SVGs.
"""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, GOOD, HOT, apply_style, color, save

SUB = "M5"
C = color(SUB)  # pillar-M accent (#ee7de0)


def policy_value_vs_threshold() -> None:
    """Value V(pi_t) of a threshold policy 'treat if tau_hat(x) > t' as t sweeps.

    A unit has CATE tau(x); the optimal rule treats exactly when tau(x) > 0, so
    the population value V(t) = E[Y(0)] + E[(tau(X)) 1{tau_hat(X) > t}] peaks at
    t = 0 when tau_hat = tau. With a noisy estimate tau_hat the peak both shifts
    and flattens. Lesson: n=20000, tau ~ N(0.3, 1), rng(0).
    """
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 20000
    tau = rng.normal(0.3, 1.0, n)            # true CATE
    base = 1.0                                # E[Y(0)]
    thresholds = np.linspace(-2.0, 2.0, 161)

    def value(score):
        treat = score[None, :] > thresholds[:, None]   # (T, n)
        return base + (treat * tau[None, :]).mean(axis=1)

    v_oracle = value(tau)                              # perfect CATE
    tau_noisy = tau + rng.normal(0, 0.8, n)            # noisy estimate
    v_noisy = value(tau_noisy)

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(thresholds, v_oracle, color=GOOD, lw=2.4, label="oracle $\\tau(x)$")
    ax.plot(thresholds, v_noisy, color=C, lw=2.4, label="noisy $\\hat\\tau(x)$")
    ax.axvline(0.0, color=FG_DIM, lw=1.0, ls="--")
    i_o = int(np.argmax(v_oracle))
    i_n = int(np.argmax(v_noisy))
    ax.scatter([thresholds[i_o]], [v_oracle[i_o]], color=GOOD, s=40, zorder=5)
    ax.scatter([thresholds[i_n]], [v_noisy[i_n]], color=C, s=40, zorder=5)
    ax.set_title("Policy value vs. CATE threshold (peak at $t = 0$)")
    ax.set_xlabel("threshold $t$ in 'treat if $\\hat\\tau(x) > t$'")
    ax.set_ylabel("policy value $V(\\pi_t)$")
    ax.legend(loc="lower center", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "policy-value-threshold")


def ope_variance_vs_overlap() -> None:
    """Variance of IPS, DM, and DR off-policy estimators as overlap worsens.

    A logging policy mu and a target policy pi share a binary action. As the
    logging policy concentrates (worse overlap), importance weights pi/mu blow up
    and IPS variance explodes; DM has low variance but is biased; DR tracks DM's
    low variance while staying (near-)unbiased. We plot the empirical standard
    deviation of each estimator across repeated logged datasets. rng(0).
    """
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 800
    reps = 400
    # overlap controlled by how sharply mu favors action 1 for x>0.
    sharpness = np.linspace(0.5, 6.0, 12)
    # target policy: deterministic, treat (a=1) when x>0.
    # outcome model: Y(a) = a*(0.5 + x) + noise; true target value computed below.

    def logging_prob(x, s):
        z = s * x
        return 1.0 / (1.0 + np.exp(-z))      # P(a=1 | x) under mu

    sd_ips, sd_dm, sd_dr = [], [], []
    # An imperfect (biased) outcome model used by DM and DR.
    for s in sharpness:
        est_ips, est_dm, est_dr = [], [], []
        for _ in range(reps):
            x = rng.normal(0, 1, n)
            p1 = logging_prob(x, s)
            a = (rng.uniform(size=n) < p1).astype(float)
            mean = a * (0.5 + x)
            y = mean + rng.normal(0, 0.5, n)
            mu = np.where(a == 1, p1, 1 - p1)        # prob of taken action
            pi = (x > 0).astype(float)               # target action
            match = (a == pi).astype(float)
            w = match / mu                           # IPS weight (target is deterministic)
            # biased outcome model qhat(x,a): shrunk slope (0.5+x)->(0.3+0.7x)
            q1 = 0.3 + 0.7 * x
            q0 = np.zeros(n)
            qhat_taken = np.where(a == 1, q1, q0)
            qhat_target = np.where(pi == 1, q1, q0)
            est_ips.append((w * y).mean())
            est_dm.append(qhat_target.mean())
            est_dr.append((qhat_target + w * (y - qhat_taken)).mean())
        sd_ips.append(np.std(est_ips))
        sd_dm.append(np.std(est_dm))
        sd_dr.append(np.std(est_dr))

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(sharpness, sd_ips, color=HOT, lw=2.4, marker="o", ms=4, label="IPS")
    ax.plot(sharpness, sd_dm, color=ACCENT, lw=2.4, marker="s", ms=4, label="DM (direct)")
    ax.plot(sharpness, sd_dr, color=GOOD, lw=2.4, marker="^", ms=4, label="DR")
    ax.set_title("Estimator standard deviation as overlap worsens")
    ax.set_xlabel("logging sharpness (worse overlap $\\rightarrow$)")
    ax.set_ylabel("std. dev. of value estimate")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "ope-variance-overlap")


def clipping_bias_variance() -> None:
    """Bias-variance of clipped IPS as the clip threshold M varies.

    Clipping importance weights at M caps variance but introduces a downward
    bias (clipped mass is dropped). Small M: low variance, large bias. Large M:
    unbiased but high variance. The MSE has a U-shape with a sweet spot. rng(0).
    """
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 600
    reps = 600
    true_value = None
    Ms = np.array([1.5, 2, 3, 5, 8, 12, 20, 40, 1e6])

    # heavy-tailed weights: w = pi/mu with a sharp logging policy.
    def sample():
        x = rng.normal(0, 1, n)
        p1 = 1.0 / (1.0 + np.exp(-3.0 * x))
        a = (rng.uniform(size=n) < p1).astype(float)
        y = a * (0.5 + x) + rng.normal(0, 0.5, n)
        mu = np.where(a == 1, p1, 1 - p1)
        pi = (x > 0).astype(float)
        w = (a == pi).astype(float) / mu
        return w, y

    # true target value via a large oracle sample under the target policy.
    xo = rng.normal(0, 1, 400000)
    true_value = ((xo > 0) * (0.5 + xo)).mean()

    bias2, var = [], []
    for M in Ms:
        ests = []
        for _ in range(reps):
            w, y = sample()
            wc = np.minimum(w, M)
            ests.append((wc * y).mean())
        ests = np.array(ests)
        bias2.append((ests.mean() - true_value) ** 2)
        var.append(ests.var())
    bias2 = np.array(bias2)
    var = np.array(var)
    mse = bias2 + var

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(Ms, bias2, color=ACCENT, lw=2.2, marker="s", ms=4, label="bias$^2$")
    ax.plot(Ms, var, color=HOT, lw=2.2, marker="o", ms=4, label="variance")
    ax.plot(Ms, mse, color=C, lw=2.6, marker="D", ms=4, label="MSE")
    ax.set_xscale("log")
    ax.set_title("Clipped IPS: bias-variance vs. clip threshold $M$")
    ax.set_xlabel("clip threshold $M$ (log scale)")
    ax.set_ylabel("error")
    ax.legend(loc="upper center", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "clipping-bias-variance")


def regret_vs_n() -> None:
    """Regret of a learned threshold policy decays as the logged sample grows.

    With more logged data the CATE estimate sharpens, the learned 'treat if
    tau_hat>0' rule approaches the oracle, and regret V(pi*) - V(pi_hat) shrinks
    roughly like 1/sqrt(n). We average over many logged datasets per n. rng(0).
    """
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    ns = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400])
    reps = 400
    # tau(x) = x (1-d covariate, X ~ N(0,1)). The oracle policy treats when
    # tau(x) > 0, i.e. x > 0. A threshold policy "treat if x > t" has value gain
    #   V(t) = E[tau(X) 1{X > t}] = E[X 1{X > t}] = phi(t),
    # the standard-normal pdf, since d/dx(-phi) = x phi. The oracle is t* = 0 with
    # V(0) = phi(0). Closed-form regret of a learned threshold t_hat is therefore
    #   regret(t_hat) = phi(0) - phi(t_hat) >= 0,  zero only at t_hat = 0.
    phi = lambda t: np.exp(-0.5 * t * t) / np.sqrt(2 * np.pi)
    grid = np.linspace(-1.5, 1.5, 61)        # candidate thresholds (excludes exact 0)

    regrets = []
    for n in ns:
        rs = []
        for _ in range(reps):
            x = rng.normal(0, 1, n)
            y_signal = x + rng.normal(0, 1.0, n)     # noisy per-unit effect signal
            # Learn the threshold by maximizing the empirical value of "treat if
            # x > t" over the grid: sum of y_signal on the treated units / n.
            vals = [(y_signal[x > t].sum()) / n for t in grid]
            t_hat = grid[int(np.argmax(vals))]
            rs.append(phi(0.0) - phi(t_hat))         # closed-form, always >= 0
        regrets.append(np.mean(rs))
    regrets = np.array(regrets)

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(ns, regrets, color=C, lw=2.4, marker="o", ms=5, label="learned policy regret")
    ref = regrets[0] * np.sqrt(ns[0]) / np.sqrt(ns)
    ax.plot(ns, ref, color=FG_DIM, lw=1.6, ls="--", label="$\\propto 1/\\sqrt{n}$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Policy regret shrinks as the logged sample grows")
    ax.set_xlabel("logged sample size $n$ (log scale)")
    ax.set_ylabel("regret $V(\\pi^*) - V(\\hat\\pi)$ (log scale)")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "regret-vs-n")


def main() -> None:
    apply_style()
    policy_value_vs_threshold()
    ope_variance_vs_overlap()
    clipping_bias_variance()
    regret_vs_n()


if __name__ == "__main__":
    main()
