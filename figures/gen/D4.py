"""Figures for pillar D4 (generative models). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import CYCLE, FG_DIM, GOOD, GRID, HOT, apply_style, color, save

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


def main() -> None:
    apply_style()
    vae()
    gan()
    diffusion()


if __name__ == "__main__":
    main()
