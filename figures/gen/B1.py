"""Figures for pillar B1 (classical inference). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "B1"
C = color(SUB)  # pillar-B accent


def sampling_distributions() -> None:
    """The sample mean of a skewed Exponential(λ=2) is itself ~Gaussian (CLT), and
    its spread shrinks as 1/√n. Lesson's setup: rng(0), n=100, 10k experiments."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    lam = 2.0
    mu, sd = 1 / lam, 1 / lam
    n, reps = 100, 10000
    means = rng.exponential(1 / lam, size=(reps, n)).mean(axis=1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax1.hist(means, bins=60, density=True, color=C, alpha=0.75, label="sample means")
    g = np.linspace(means.min(), means.max(), 300)
    se = sd / np.sqrt(n)
    ax1.plot(g, np.exp(-0.5 * ((g - mu) / se) ** 2) / (se * np.sqrt(2 * np.pi)),
             color=ACCENT, lw=2.2, label=f"$\\mathcal{{N}}(\\mu,\\,\\sigma^2/n)$")
    ax1.axvline(mu, color=FG_MUTE, ls=":", lw=1.2)
    ax1.set_title("Sample mean of Exp(2), n=100")
    ax1.set_xlabel("sample mean")
    ax1.set_ylabel("density")
    ax1.legend(loc="upper right", fontsize=9)

    ns = np.arange(5, 500)
    ax2.plot(ns, 2 * 1.96 * sd / np.sqrt(ns), color=C, lw=2.4)
    ax2.set_title("95% CI width shrinks as $1/\\sqrt{n}$")
    ax2.set_xlabel("sample size $n$")
    ax2.set_ylabel("CI width  $2\\cdot1.96\\,\\sigma/\\sqrt{n}$")
    fig.tight_layout()
    save(fig, SUB, "sampling-distributions")


def hypothesis_testing() -> None:
    """The two error rates: under H₀ the test statistic is N(0,1); under H₁ it
    shifts. α (Type I) is the H₀ tail past the critical value; β (Type II) is the
    H₁ mass that falls short of it. Power = 1 − β."""
    import matplotlib.pyplot as plt

    z = np.linspace(-4, 7, 600)
    d = 3.0  # separation under H1
    zc = 1.645  # one-sided α = 0.05 critical value
    pdf = lambda x, m: np.exp(-0.5 * (x - m) ** 2) / np.sqrt(2 * np.pi)
    h0, h1 = pdf(z, 0), pdf(z, d)

    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.plot(z, h0, color=ACCENT, lw=2.0, label="$H_0$")
    ax.plot(z, h1, color=C, lw=2.0, label="$H_1$")
    ax.fill_between(z, h0, where=z >= zc, color=ACCENT, alpha=0.45, label="α (Type I)")
    ax.fill_between(z, h1, where=z < zc, color=C, alpha=0.35, label="β (Type II)")
    ax.axvline(zc, color=FG_MUTE, ls="--", lw=1.4)
    ax.text(zc + 0.1, 0.41, "critical value", color=FG_MUTE, fontsize=9)
    ax.set_title("Type I vs Type II error")
    ax.set_xlabel("test statistic")
    ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "hypothesis-testing")


def estimator_properties() -> None:
    """Mean squared error decomposes into bias² + variance. For the σ² estimator,
    dividing by n (MLE) is biased but lower-variance; dividing by n−1 is unbiased.
    Both MSEs fall as 1/n. Lesson: μ=2, σ=1.5."""
    import matplotlib.pyplot as plt

    sigma = 1.5
    ns = np.array([5, 10, 20, 50, 100, 200, 500, 1000])
    var_true = sigma**2
    # σ̂²_n (÷n): bias = -σ²/n, var = 2σ⁴(n-1)/n²  ; σ̂²_{n-1} (÷n-1): unbiased, var = 2σ⁴/(n-1)
    bias_n = (-var_true / ns)
    var_n = 2 * var_true**2 * (ns - 1) / ns**2
    mse_n = bias_n**2 + var_n
    var_n1 = 2 * var_true**2 / (ns - 1)
    mse_n1 = var_n1  # unbiased

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(ns, bias_n**2, "-o", color=GOOD, ms=4, label="bias$^2$ (÷n)")
    ax.loglog(ns, var_n, "-o", color=HOT, ms=4, label="variance (÷n)")
    ax.loglog(ns, mse_n, "-o", color=C, ms=4, lw=2.4, label="MSE (÷n)")
    ax.loglog(ns, mse_n1, "-o", color=FG_MUTE, ms=4, label="MSE (÷n−1, unbiased)")
    ax.set_title("MSE = bias² + variance")
    ax.set_xlabel("sample size $n$")
    ax.set_ylabel("error")
    ax.legend(loc="lower left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "estimator-properties")


def anova() -> None:
    """ANOVA splits total variation into between-group (signal) and within-group
    (noise); the F-ratio compares them. Lesson: 3 groups, n=30, σ=1.5,
    means 5.0/6.2/5.5, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    mus = [5.0, 6.2, 5.5]
    groups = [rng.normal(m, 1.5, 30) for m in mus]
    grand = np.mean(np.concatenate(groups))
    means = [g.mean() for g in groups]
    ses = [g.std(ddof=1) / np.sqrt(len(g)) for g in groups]
    ssb = sum(len(g) * (m - grand) ** 2 for g, m in zip(groups, means))
    ssw = sum(((g - m) ** 2).sum() for g, m in zip(groups, means))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.9),
                                   gridspec_kw={"width_ratios": [1.4, 1]})
    xs = np.arange(3)
    for i, g in enumerate(groups):
        ax1.scatter(np.full(len(g), i) + rng.uniform(-0.08, 0.08, len(g)), g,
                    s=10, color=C, alpha=0.4, edgecolor="none")
    ax1.errorbar(xs, means, yerr=ses, fmt="o", color=ACCENT, ms=8, capsize=5,
                 lw=2, label="group mean ± SE")
    ax1.axhline(grand, color=FG_MUTE, ls="--", lw=1.4, label="grand mean")
    ax1.set_xticks(xs)
    ax1.set_xticklabels(["A", "B", "C"])
    ax1.set_title("Group means")
    ax1.set_ylabel("value")
    ax1.legend(loc="upper left", fontsize=8)

    ax2.bar(["between\n(SSB)", "within\n(SSW)"], [ssb, ssw], color=[ACCENT, C])
    ax2.set_title("Variance decomposition")
    ax2.set_ylabel("sum of squares")
    fig.tight_layout()
    save(fig, SUB, "anova")


def cramer_rao_bound() -> None:
    """The Cramér–Rao bound is the floor on any unbiased estimator's variance. For
    the Gaussian mean it is σ²/n, and the sample mean sits exactly on it — it is
    efficient. Lesson: σ=2 → CRLB = 4/n, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    sigma = 2.0
    ns = np.array([10, 20, 50, 100, 200, 500, 1000])
    reps = 20000
    emp = np.array([rng.normal(1.0, sigma, size=(reps, n)).mean(axis=1).var() for n in ns])
    crlb = sigma**2 / ns

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(ns, crlb, color=ACCENT, lw=2.4, label="CRLB = $\\sigma^2/n$")
    ax.loglog(ns, emp, "o", color=C, ms=7, label="variance of sample mean")
    ax.set_title("Sample mean attains the Cramér–Rao bound")
    ax.set_xlabel("sample size $n$")
    ax.set_ylabel("variance")
    ax.legend(loc="lower left")
    fig.tight_layout()
    save(fig, SUB, "cramer-rao-bound")


def main() -> None:
    apply_style()
    sampling_distributions()
    hypothesis_testing()
    estimator_properties()
    anova()
    cramer_rao_bound()


if __name__ == "__main__":
    main()
