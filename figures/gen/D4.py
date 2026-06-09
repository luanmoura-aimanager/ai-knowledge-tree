"""Figures for pillar D4 (generative models). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import CYCLE, FG_DIM, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "D4"
C = color(SUB)  # pillar-D accent (blue)


def _gauss(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


def vae() -> None:
    """The VAE's KL term regularizes the encoder toward the unit-Gaussian prior:
    KL(N(μ,σ²)‖N(0,1)) = ½(μ²+σ²−1−2lnσ) is zero only at μ=0, σ=1 and grows as the
    code drifts — the pressure that keeps the latent space well-formed."""
    import matplotlib.pyplot as plt

    mu = np.linspace(-3, 3, 300)
    sd = np.linspace(0.25, 3.0, 300)
    M, S = np.meshgrid(mu, sd)
    KL = 0.5 * (M**2 + S**2 - 1 - 2 * np.log(S))

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    # Rasterize the filled contour (everything below zorder 0) so the SVG embeds
    # a compact raster instead of thousands of vector polygons (~10x smaller).
    ax.set_rasterization_zorder(0)
    cf = ax.contourf(M, S, KL, levels=np.linspace(0, 6, 25), cmap="viridis",
                     extend="max", zorder=-10)
    ax.contour(M, S, KL, levels=[0.25, 1, 2, 4], colors=GRID, linewidths=0.6)
    ax.plot(0, 1, "*", color="#ffffff", ms=16, zorder=5)
    ax.annotate("KL = 0\n(μ=0, σ=1)", xy=(0, 1), xytext=(0.7, 1.9), color="#ffffff",
                fontsize=10, arrowprops=dict(arrowstyle="->", color="#ffffff", lw=1.4))
    ax.set_title("VAE KL term: pull toward the prior")
    ax.set_xlabel("code mean $\\mu$")
    ax.set_ylabel("code std $\\sigma$")
    cb = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cb.ax.tick_params(colors=FG_DIM)
    cb.outline.set_edgecolor(GRID)
    cb.set_label("KL divergence (nats)", color=FG_DIM)
    fig.tight_layout()
    save(fig, SUB, "vae")


def gan() -> None:
    """Mode collapse: the data has two modes but the generator has learned only
    one. The optimal discriminator D*(x) = p_data/(p_data+p_gen) stays near 1 on
    the abandoned mode — the signal that should push the generator to cover it."""
    import matplotlib.pyplot as plt

    x = np.linspace(-4, 4, 500)
    p_data = 0.5 * _gauss(x, -2, 0.4) + 0.5 * _gauss(x, 2, 0.4)
    p_gen = _gauss(x, 2, 0.4)  # collapsed onto the right mode only
    d_star = p_data / (p_data + p_gen + 1e-12)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.fill_between(x, p_data, color=C, alpha=0.45, label="data $p_{data}$")
    ax.fill_between(x, p_gen, color=HOT, alpha=0.45, label="generator $p_g$ (collapsed)")
    ax.set_xlabel("$x$")
    ax.set_ylabel("density")
    ax.set_title("Mode collapse and the optimal discriminator")
    ax.legend(loc="upper left", fontsize=9, frameon=False)

    ax2 = ax.twinx()
    ax2.plot(x, d_star, color=GOOD, lw=2.4)
    ax2.set_ylabel("$D^*(x)$", color=GOOD)
    ax2.tick_params(axis="y", colors=GOOD)
    ax2.set_ylim(0, 1.05)
    ax2.annotate("D≈1 on the\nmissed mode", xy=(-2, 1.0), xytext=(-3.7, 0.55),
                 color=GOOD, fontsize=9, arrowprops=dict(arrowstyle="->", color=GOOD, lw=1.2))
    fig.tight_layout()
    save(fig, SUB, "gan")


def diffusion() -> None:
    """Forward diffusion. Left: the schedule — the signal-retention factor ᾱ_t
    decays from 1 to ≈0 as the per-step noise β_t ramps up. Right: the data
    distribution melts from two sharp modes into a standard Gaussian. Lesson's
    linear schedule, T=100, rng(0)."""
    import matplotlib.pyplot as plt

    T = 100
    beta = np.linspace(1e-4, 0.02, T)
    alpha_bar = np.cumprod(1.0 - beta)
    ts = np.arange(1, T + 1)

    rng = np.random.default_rng(0)
    x0 = np.concatenate([rng.normal(-2, 0.3, 4000), rng.normal(2, 0.3, 4000)])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.9))
    ax1.plot(ts, alpha_bar, color=C, lw=2.4, label=r"$\bar\alpha_t$ (signal kept)")
    ax1.plot(ts, beta / beta.max(), color=HOT, lw=2.0, label=r"$\beta_t$ (scaled)")
    ax1.set_title("Noise schedule")
    ax1.set_xlabel("timestep $t$")
    ax1.set_ylabel("value")
    ax1.legend(loc="center right", fontsize=9)

    cols = [C, GOOD, CYCLE[4], HOT]
    for t, col in zip([1, 25, 60, 100], cols):
        xt = np.sqrt(alpha_bar[t - 1]) * x0 + np.sqrt(1 - alpha_bar[t - 1]) * rng.normal(size=x0.size)
        ax2.hist(xt, bins=80, density=True, histtype="step", color=col, lw=2.0,
                 label=f"t = {t}")
    ax2.set_title("Data melts into noise")
    ax2.set_xlabel("$x_t$")
    ax2.set_ylabel("density")
    ax2.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "diffusion")


def autoencoders() -> None:
    """An autoencoder squeezes data through a bottleneck: reconstruction error falls
    sharply until the bottleneck matches the data's intrinsic dimension, then
    plateaus at the noise floor. Shown with the optimal linear (PCA) reconstruction
    on data whose signal lives in ~4 dimensions. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 500
    t = rng.uniform(0, 2 * np.pi, n)
    X = np.column_stack([np.cos(t), np.sin(t), 0.5 * np.cos(2 * t), 0.5 * np.sin(2 * t),
                         rng.normal(scale=0.05, size=(n, 6))])
    Xc = X - X.mean(0)
    s = np.linalg.svd(Xc, compute_uv=False)
    total = (s**2).sum()
    ks = np.arange(1, X.shape[1] + 1)
    mse = [(total - (s[:k] ** 2).sum()) / n for k in ks]

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(ks, mse, "-o", color=C, ms=5)
    ax.axvline(4, color=HOT, ls=":", lw=1.4, label="intrinsic dimension ≈ 4")
    ax.set_title("Reconstruction error vs bottleneck size")
    ax.set_xlabel("bottleneck dimension $k$")
    ax.set_ylabel("reconstruction MSE")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "autoencoders")


def flow_matching() -> None:
    """Flow matching learns a velocity field that transports a base Gaussian to the
    data along straight conditional paths: each sample rides a line from noise (t=0)
    to a target point (t=1), so the cloud morphs into the target ring. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    m = 600
    x0 = rng.normal(scale=0.6, size=(m, 2))
    ang = rng.uniform(0, 2 * np.pi, m)
    x1 = np.column_stack([3 * np.cos(ang), 3 * np.sin(ang)]) + 0.15 * rng.normal(size=(m, 2))

    fig, ax = plt.subplots(figsize=(6.0, 5.4))
    idx = rng.choice(m, 40, replace=False)
    for i in idx:
        ax.plot([x0[i, 0], x1[i, 0]], [x0[i, 1], x1[i, 1]], color=FG_MUTE, lw=0.5, alpha=0.5)
    ax.scatter(x0[:, 0], x0[:, 1], s=8, color=HOT, alpha=0.5, edgecolor="none",
               label="base $t=0$")
    mid = 0.5 * x0 + 0.5 * x1
    ax.scatter(mid[:, 0], mid[:, 1], s=8, color=GOOD, alpha=0.4, edgecolor="none",
               label="midpoint $t=0.5$")
    ax.scatter(x1[:, 0], x1[:, 1], s=8, color=C, alpha=0.6, edgecolor="none",
               label="target $t=1$")
    ax.set_aspect("equal")
    ax.set_title("Flow matching: straight-line transport")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "flow-matching")


def normalizing_flows() -> None:
    """A normalizing flow is an invertible map: stacked coupling layers warp a simple
    Gaussian into a complex shape, and because each step is invertible with a known
    Jacobian, the exact density transfers with it. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    base = rng.normal(size=(2000, 2))

    def coupling(x, Ws, Wt, flip=False):
        a, b = (x[:, 1], x[:, 0]) if flip else (x[:, 0], x[:, 1])
        s = np.tanh(a[:, None] @ Ws).ravel()
        t = np.tanh(a[:, None] @ Wt).ravel()
        b2 = b * np.exp(0.6 * s) + t
        return np.column_stack([b2, a] if flip else [a, b2])

    z = base.copy()
    for layer in range(4):
        r = np.random.default_rng(layer)
        z = coupling(z, r.normal(scale=0.8, size=(1, 1)), r.normal(scale=1.0, size=(1, 1)),
                     flip=bool(layer % 2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.4, 4.2))
    ax1.scatter(base[:, 0], base[:, 1], s=5, color=FG_MUTE, alpha=0.4, edgecolor="none")
    ax1.set_title("base density (Gaussian)")
    ax2.scatter(z[:, 0], z[:, 1], s=5, color=C, alpha=0.4, edgecolor="none")
    ax2.set_title("after invertible coupling layers")
    for ax in (ax1, ax2):
        ax.set_aspect("equal"); ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    fig.tight_layout()
    save(fig, SUB, "normalizing-flows")


def main() -> None:
    apply_style()
    vae()
    gan()
    diffusion()
    autoencoders()
    flow_matching()
    normalizing_flows()


if __name__ == "__main__":
    main()
