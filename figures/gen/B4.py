"""Figures for pillar B4 (experimentation & bandits). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "B4"
C = color(SUB)  # pillar-B accent


def ab_testing() -> None:
    """An A/B test's estimated lift converges to the truth as data accrues while
    its confidence interval tightens like 1/√n. Lesson: p_A=0.10, p_B=0.12,
    2000/arm, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    pA, pB, n = 0.10, 0.12, 2000
    a = rng.binomial(1, pA, n)
    b = rng.binomial(1, pB, n)
    t = np.arange(1, n + 1)
    diff = np.cumsum(b) / t - np.cumsum(a) / t
    pa, pb = np.cumsum(a) / t, np.cumsum(b) / t
    se = np.sqrt(pa * (1 - pa) / t + pb * (1 - pb) / t)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.fill_between(t, diff - 1.96 * se, diff + 1.96 * se, color=C, alpha=0.25,
                    label="95% CI")
    ax.plot(t, diff, color=C, lw=1.8, label="estimated lift")
    ax.axhline(pB - pA, color=HOT, ls="--", lw=1.6, label="true lift = 0.02")
    ax.axhline(0, color=FG_MUTE, lw=0.8)
    ax.set_ylim(-0.05, 0.09)
    ax.set_title("A/B test: lift estimate and tightening CI")
    ax.set_xlabel("observations per arm")
    ax.set_ylabel("$\\hat p_B - \\hat p_A$")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "ab-testing")


def multi_armed_bandits() -> None:
    """Cumulative regret: ε-greedy, UCB1, and Thompson sampling all learn the best
    arm, but the smart explorers grow regret only logarithmically while random
    selection grows it linearly. Lesson: K=5, μ=[.1,.3,.5,.4,.2], T=2000, rng(0)."""
    import matplotlib.pyplot as plt

    mu = np.array([0.1, 0.3, 0.5, 0.4, 0.2])
    K, T, best = len(mu), 2000, mu.max()

    def play(policy):
        rng = np.random.default_rng(0)
        n = np.zeros(K); s = np.zeros(K); a_, b_ = np.ones(K), np.ones(K)
        reg = np.zeros(T)
        cum = 0.0
        for t in range(T):
            if policy == "random":
                k = rng.integers(K)
            elif policy == "egreedy":
                k = rng.integers(K) if rng.random() < 0.1 else int(np.argmax(np.where(n > 0, s / np.maximum(n, 1), 1.0)))
            elif policy == "ucb":
                if t < K:
                    k = t
                else:
                    k = int(np.argmax(s / n + np.sqrt(2 * np.log(t + 1) / n)))
            else:  # thompson
                k = int(np.argmax(rng.beta(a_, b_)))
            r = rng.random() < mu[k]
            n[k] += 1; s[k] += r
            if policy == "thompson":
                a_[k] += r; b_[k] += 1 - r
            cum += best - mu[k]
            reg[t] = cum
        return reg

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for pol, col, lab in [("random", FG_MUTE, "random"), ("egreedy", GOOD, "ε-greedy"),
                          ("ucb", ACCENT, "UCB1"), ("thompson", C, "Thompson")]:
        ax.plot(play(pol), color=col, lw=2.0, label=lab)
    ax.set_title("Cumulative regret of bandit policies")
    ax.set_xlabel("round $t$")
    ax.set_ylabel("cumulative regret")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "multi-armed-bandits")


def power_analysis() -> None:
    """Statistical power (1−β) rises with sample size, faster for larger effect
    sizes. Two-sample z-test, α=0.05; the dashed line marks the conventional 80%
    target. (Lesson uses σ=1, Cohen's d.)"""
    import matplotlib.pyplot as plt
    from scipy.stats import norm

    n = np.arange(5, 400)
    zc = norm.ppf(1 - 0.025)  # two-sided α=0.05

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for d, col in zip([0.2, 0.5, 0.8, 1.0], [FG_MUTE, ACCENT, GOOD, HOT]):
        power = 1 - norm.cdf(zc - d * np.sqrt(n / 2))
        ax.plot(n, power, color=col, lw=2.2, label=f"d = {d}")
    ax.axhline(0.8, color=GOOD, ls="--", lw=1.4, label="80% power")
    ax.set_title("Power vs sample size by effect size")
    ax.set_xlabel("sample size per group $n$")
    ax.set_ylabel("power (1 − β)")
    ax.set_ylim(0, 1.02)
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "power-analysis")


def main() -> None:
    apply_style()
    ab_testing()
    multi_armed_bandits()
    power_analysis()


if __name__ == "__main__":
    main()
