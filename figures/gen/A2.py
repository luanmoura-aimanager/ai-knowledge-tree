"""Figures for pillar A2 (probability & statistics). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, CYCLE, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "A2"
C = color(SUB)  # pillar-A accent (gold)


def common_distributions() -> None:
    """PMF/PDF of the four workhorse distributions, with the lesson's parameters:
    Bernoulli(0.3), Binomial(20, 0.3), Poisson(4), Gaussian(1, 2)."""
    import matplotlib.pyplot as plt
    from math import comb, exp, factorial, pi, sqrt

    fig, axes = plt.subplots(2, 2, figsize=(8.2, 5.2))

    # Bernoulli(0.3)
    ax = axes[0, 0]
    ax.bar([0, 1], [0.7, 0.3], width=0.4, color=C)
    ax.set_xticks([0, 1])
    ax.set_title("Bernoulli($q=0.3$)")
    ax.set_ylabel("probability")

    # Binomial(20, 0.3)
    ax = axes[0, 1]
    n, q = 20, 0.3
    ks = np.arange(0, n + 1)
    pmf = np.array([comb(n, k) * q**k * (1 - q) ** (n - k) for k in ks])
    ax.bar(ks, pmf, color=ACCENT)
    ax.set_title("Binomial($n=20,\\,q=0.3$)")

    # Poisson(4)
    ax = axes[1, 0]
    lam = 4.0
    ks = np.arange(0, 16)
    pmf = np.array([exp(-lam) * lam**k / factorial(k) for k in ks])
    ax.bar(ks, pmf, color=GOOD)
    ax.set_title("Poisson($\\lambda=4$)")
    ax.set_xlabel("$k$")
    ax.set_ylabel("probability")

    # Gaussian(1, 2)
    ax = axes[1, 1]
    mu, sigma = 1.0, 2.0
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma**2)) / (sigma * sqrt(2 * pi))
    ax.plot(x, pdf, color=HOT, lw=2.2)
    ax.fill_between(x, pdf, color=HOT, alpha=0.18)
    ax.set_title("Gaussian($\\mu=1,\\,\\sigma=2$)")
    ax.set_xlabel("$x$")

    fig.tight_layout()
    save(fig, SUB, "common-distributions")


def entropy() -> None:
    """Binary entropy H(q) = -q log₂q - (1-q)log₂(1-q): zero at the certain
    outcomes, maximal (1 bit) at q = 1/2."""
    import matplotlib.pyplot as plt

    q = np.linspace(1e-6, 1 - 1e-6, 500)
    H = -q * np.log2(q) - (1 - q) * np.log2(1 - q)

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.plot(q, H, color=C, lw=2.4)
    ax.plot(0.5, 1.0, "o", color=HOT, ms=8)
    ax.annotate("max = 1 bit at $q=1/2$", xy=(0.5, 1.0), xytext=(0.55, 0.6),
                color=HOT, fontsize=11,
                arrowprops=dict(arrowstyle="->", color=HOT, lw=1.2))
    ax.set_title("Binary entropy")
    ax.set_xlabel("$q = P(\\mathrm{heads})$")
    ax.set_ylabel("$H(q)$  (bits)")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.08)
    fig.tight_layout()
    save(fig, SUB, "entropy")


def lln_clt() -> None:
    """LLN: the running mean of a fair die converges to 3.5. CLT: standardized
    means of an (asymmetric) exponential look Gaussian. Lesson's setup, rng(10)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(10)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 3.7))

    # LLN — a few sample paths + the limit
    N = 5000
    for i, col in enumerate([C, ACCENT, FG_MUTE]):
        draws = rng.integers(1, 7, size=N).astype(float)
        running = np.cumsum(draws) / np.arange(1, N + 1)
        ax1.plot(running, color=col, lw=1.0, alpha=0.9)
    ax1.axhline(3.5, color=HOT, ls="--", lw=1.6, label="$\\mu = 3.5$")
    ax1.set_xscale("log")
    ax1.set_title("LLN: running mean of a die")
    ax1.set_xlabel("number of rolls $n$")
    ax1.set_ylabel("running average")
    ax1.legend(loc="upper right")

    # CLT — standardized exponential means vs N(0,1)
    n, trials = 1000, 20000
    means = rng.exponential(1.0, size=(trials, n)).mean(axis=1)
    standardized = (means - 1.0) / (1.0 / np.sqrt(n))
    ax2.hist(standardized, bins=60, density=True, color=C, alpha=0.75,
             label="standardized means")
    z = np.linspace(-4, 4, 300)
    ax2.plot(z, np.exp(-z**2 / 2) / np.sqrt(2 * np.pi), color=HOT, lw=2.2,
             label="$\\mathcal{N}(0,1)$")
    ax2.set_title("CLT: means of Exp(1)")
    ax2.set_xlabel("standardized sample mean")
    ax2.set_ylabel("density")
    ax2.legend(loc="upper right")

    fig.tight_layout()
    save(fig, SUB, "lln-clt")


def information_geometry() -> None:
    """Fisher information = curvature of the expected log-likelihood. For
    N(θ, 1) the log-likelihood is a downward parabola whose sharpness grows with
    the sample size N — more data ⇒ more curvature ⇒ a more certain estimate."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(17)
    theta_true = 2.0
    theta = np.linspace(0.5, 3.5, 400)

    fig, ax = plt.subplots(figsize=(6.6, 4.1))
    for n, col in zip([5, 20, 80], CYCLE):
        x = rng.normal(theta_true, 1.0, n)
        # per-sample log-likelihood, shifted to peak at 0 for comparison
        ll = -0.5 * np.sum((x[:, None] - theta[None, :]) ** 2, axis=0)
        ll = ll - ll.max()
        ax.plot(theta, ll, color=col, lw=2.0, label=f"$N={n}$")
    ax.axvline(theta_true, color=FG_MUTE, ls=":", lw=1.2, label="$\\theta_{\\mathrm{true}}=2$")
    ax.set_title("Log-likelihood curvature = Fisher information")
    ax.set_xlabel("$\\theta$")
    ax.set_ylabel("log-likelihood (peak-aligned)")
    ax.set_ylim(-30, 2)
    ax.legend(loc="lower center", ncol=2)
    fig.tight_layout()
    save(fig, SUB, "information-geometry")


def markov_chains() -> None:
    """A distribution pushed through the weather transition matrix converges to
    the stationary distribution regardless of the (certain) start. Lesson's P."""
    import matplotlib.pyplot as plt

    P = np.array([
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.45, 0.35],
    ])
    steps = 12
    pi = np.array([1.0, 0.0, 0.0])
    history = [pi.copy()]
    for _ in range(steps):
        pi = pi @ P
        history.append(pi.copy())
    history = np.array(history)

    vals, vecs = np.linalg.eig(P.T)
    stat = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
    stat = stat / stat.sum()

    names = ["sunny", "cloudy", "rainy"]
    cols = [C, ACCENT, HOT]
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for j in range(3):
        ax.plot(history[:, j], "-o", color=cols[j], ms=3.5, label=names[j])
        ax.axhline(stat[j], color=cols[j], ls=":", lw=1.2, alpha=0.8)
    ax.set_title("Convergence to the stationary distribution")
    ax.set_xlabel("step $n$")
    ax.set_ylabel("$P(\\mathrm{state})$")
    ax.legend(loc="center right", title="started: sunny")
    fig.tight_layout()
    save(fig, SUB, "markov-chains")


def kl_cross_entropy() -> None:
    """KL is asymmetric. For two Bernoullis with p fixed, KL(p‖q) and KL(q‖p)
    differ sharply as q varies — the reason forward vs reverse KL behave differently."""
    import matplotlib.pyplot as plt

    p = 0.7
    q = np.linspace(0.02, 0.98, 400)

    def kl_bern(a, b):
        return a * np.log(a / b) + (1 - a) * np.log((1 - a) / (1 - b))

    fwd = kl_bern(p, q)          # KL(p || q)
    rev = kl_bern(q, p)          # KL(q || p)

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ax.plot(q, fwd, color=C, lw=2.2, label="$D_{KL}(p\\,\\|\\,q)$  (forward)")
    ax.plot(q, rev, color=HOT, lw=2.2, label="$D_{KL}(q\\,\\|\\,p)$  (reverse)")
    ax.axvline(p, color=FG_MUTE, ls=":", lw=1.2, label=f"$q=p={p}$")
    ax.set_title("KL divergence is asymmetric")
    ax.set_xlabel("$q$  (with $p=0.7$ fixed)")
    ax.set_ylabel("KL (nats)")
    ax.set_ylim(0, 3)
    ax.legend(loc="upper center")
    fig.tight_layout()
    save(fig, SUB, "kl-cross-entropy")


def mle() -> None:
    """The Poisson log-likelihood ℓ(λ) = (Σk)logλ - Nλ peaks at λ̂ = mean(counts).
    Lesson's setup: counts ~ Poisson(4), grid 3.5–4.5, rng(11)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(11)
    N = 100_000
    counts = rng.poisson(4.0, N)
    lam_hat = counts.mean()
    grid = np.linspace(3.5, 4.5, 500)
    ll = counts.sum() * np.log(grid) - N * grid
    ll = ll - ll.max()  # peak-align for readability

    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    ax.plot(grid, ll, color=C, lw=2.4)
    ax.axvline(lam_hat, color=HOT, ls="--", lw=1.6,
               label=f"$\\hat\\lambda = \\bar k = {lam_hat:.3f}$")
    ax.plot(lam_hat, 0, "o", color=HOT, ms=8)
    ax.set_title("Poisson log-likelihood and its MLE")
    ax.set_xlabel("$\\lambda$")
    ax.set_ylabel("log-likelihood (peak-aligned)")
    ax.legend(loc="lower center")
    fig.tight_layout()
    save(fig, SUB, "mle")


def main() -> None:
    apply_style()
    common_distributions()
    entropy()
    lln_clt()
    information_geometry()
    markov_chains()
    kl_cross_entropy()
    mle()


if __name__ == "__main__":
    main()
