"""Figures for pillar D1 (deep-learning fundamentals). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import CYCLE, FG_MUTE, GRID, HOT, apply_style, color, save

SUB = "D1"
C = color(SUB)  # pillar-D accent (blue)


def activations() -> None:
    """The common activations (left) and their derivatives (right). ReLU's
    derivative is a step (dead below 0); the smooth ones (GELU, Swish, tanh,
    sigmoid) have continuous, bounded gradients."""
    import matplotlib.pyplot as plt

    z = np.linspace(-4, 4, 400)
    relu = np.maximum(0, z)
    gelu = 0.5 * z * (1 + np.tanh(np.sqrt(2 / np.pi) * (z + 0.044715 * z**3)))
    swish = z / (1 + np.exp(-z))
    tanh = np.tanh(z)
    sig = 1 / (1 + np.exp(-z))
    fns = [("ReLU", relu), ("GELU", gelu), ("Swish", swish),
           ("tanh", tanh), ("sigmoid", sig)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    for (name, f), col in zip(fns, CYCLE):
        ax1.plot(z, f, color=col, lw=2.0, label=name)
        ax2.plot(z, np.gradient(f, z), color=col, lw=2.0, label=name)
    for ax in (ax1, ax2):
        ax.axhline(0, color=GRID, lw=0.8)
        ax.axvline(0, color=GRID, lw=0.8)
        ax.set_xlabel("$z$")
    ax1.set_title("Activation functions")
    ax1.set_ylabel("$f(z)$")
    ax1.legend(loc="upper left", fontsize=9)
    ax2.set_title("Their derivatives")
    ax2.set_ylabel("$f'(z)$")
    fig.tight_layout()
    save(fig, SUB, "activations")


def initialization() -> None:
    """Activation variance through a 20-layer ReLU net: naive (too small) collapses
    it toward zero, Xavier decays slowly, and He init keeps it ~constant — the
    condition for trainable depth. Lesson's setup, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    depth, width, n = 20, 256, 1024

    def run(scale_fn):
        h = rng.normal(size=(n, width))
        var = [h.var()]
        for _ in range(depth):
            W = rng.normal(scale=scale_fn(width), size=(width, width))
            h = np.maximum(0, h @ W)
            var.append(h.var())
        return var

    inits = [("naive (0.05)", lambda w: 0.05, FG_MUTE),
             ("Xavier", lambda w: np.sqrt(2 / (w + w)), HOT),
             ("He", lambda w: np.sqrt(2 / w), C)]
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for name, fn, col in inits:
        ax.semilogy(run(fn), "-o", color=col, ms=3.5, label=name)
    ax.set_title("Activation variance through depth (ReLU)")
    ax.set_xlabel("layer")
    ax.set_ylabel("activation variance")
    ax.legend(loc="lower left")
    fig.tight_layout()
    save(fig, SUB, "initialization")


def dl_optimizers() -> None:
    """Left: the warmup+cosine learning-rate schedule. Right: on a badly-scaled
    quadratic (κ = 1000), SGD's step is capped by the steepest direction so the
    flat ones crawl, while AdamW's per-coordinate scaling reaches the optimum far
    faster."""
    import matplotlib.pyplot as plt

    total, warmup, base = 1000, 100, 1.0
    t = np.arange(total)
    lr = np.where(t < warmup, base * t / warmup,
                  base * 0.5 * (1 + np.cos(np.pi * (t - warmup) / (total - warmup))))

    H = np.array([1.0, 1000.0, 100.0, 10.0])  # condition number 1000
    loss = lambda th: 0.5 * np.sum(H * th**2)
    grad = lambda th: H * th
    th0 = np.ones(4)
    eps = 1e-8
    steps = 400

    th, v, sgd = th0.copy(), np.zeros(4), []
    for _ in range(steps):
        v = 0.9 * v + grad(th)
        th = th - 0.0015 * v  # near the stability limit for the κ=1000 direction
        sgd.append(loss(th))

    th, m, v2, adam = th0.copy(), np.zeros(4), np.zeros(4), []
    for i in range(1, steps + 1):
        g = grad(th)
        m = 0.9 * m + 0.1 * g
        v2 = 0.999 * v2 + 0.001 * g * g
        th = th - 0.05 * (m / (1 - 0.9**i)) / (np.sqrt(v2 / (1 - 0.999**i)) + eps)
        adam.append(loss(th))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax1.plot(t, lr, color=C, lw=2.2)
    ax1.axvline(warmup, color=FG_MUTE, ls=":", lw=1.2, label="end of warmup")
    ax1.set_title("Warmup + cosine schedule")
    ax1.set_xlabel("step")
    ax1.set_ylabel("learning rate")
    ax1.legend(loc="upper right")

    ax2.semilogy(sgd, color=FG_MUTE, lw=2.0, label="SGD + momentum")
    ax2.semilogy(adam, color=C, lw=2.2, label="AdamW")
    ax2.set_title("Convergence on an ill-scaled quadratic")
    ax2.set_xlabel("step")
    ax2.set_ylabel("loss")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "dl-optimizers")


def normalization() -> None:
    """Stacking 30 naive-init ReLU layers lets activation variance decay toward
    zero; inserting LayerNorm at each layer holds it steady — why normalization
    keeps deep nets trainable. Lesson's setup, rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    depth, width = 30, 64

    def layer_norm(z):
        mu = z.mean(axis=1, keepdims=True)
        var = z.var(axis=1, keepdims=True)
        return (z - mu) / np.sqrt(var + 1e-5)

    def run(use_norm):
        h = rng.normal(size=(64, width))
        var = [h.var()]
        for _ in range(depth):
            W = rng.normal(scale=0.1, size=(width, width))
            z = h @ W
            if use_norm:
                z = layer_norm(z)
            h = np.maximum(0, z)
            var.append(h.var())
        return var

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.semilogy(run(False), "-o", color=FG_MUTE, ms=3.5, label="no normalization")
    ax.semilogy(run(True), "-o", color=C, ms=3.5, label="LayerNorm each layer")
    ax.set_title("Normalization keeps activation variance steady")
    ax.set_xlabel("layer")
    ax.set_ylabel("activation variance")
    ax.legend(loc="center right")
    fig.tight_layout()
    save(fig, SUB, "normalization")


def regularization() -> None:
    """Two regularizers. Left: a dropout mask randomly zeros ~p of the activations
    each step (the survivors are rescaled). Right: weight decay shrinks the weight
    norm geometrically toward zero between gradient updates."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)

    mask = (rng.random((16, 24)) > 0.3).astype(float)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.8))
    ax1.imshow(mask, cmap="Blues", vmin=0, vmax=1.4, aspect="auto")
    ax1.set_title("Dropout mask (p = 0.3)")
    ax1.set_xlabel("units")
    ax1.set_ylabel("examples")
    ax1.grid(False)

    steps = np.arange(60)
    for wd, col, lab in [(0.0, FG_MUTE, "no decay"), (0.05, HOT, "wd = 0.05"),
                         (0.15, C, "wd = 0.15")]:
        ax2.plot(steps, (1 - wd) ** steps, color=col, lw=2.2, label=lab)
    ax2.set_title("Weight-decay shrinkage factor")
    ax2.set_xlabel("update step")
    ax2.set_ylabel("$\\|w\\|$ relative to start")
    ax2.legend(loc="upper right")
    fig.tight_layout()
    save(fig, SUB, "regularization")


def universal_approximation() -> None:
    """A single hidden layer of ReLU "bumps" approximates any continuous function:
    more units → lower error. Random features fit to sin(2πx), lesson's rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    x = np.linspace(0, 1, 200)
    y = np.sin(2 * np.pi * x)

    def fit(M):
        w = rng.normal(scale=5.0, size=M)
        b = rng.uniform(-2, 2, size=M)
        Phi = np.maximum(0.0, np.outer(x, w) + b)
        c = np.linalg.lstsq(Phi, y, rcond=None)[0]
        yhat = Phi @ c
        return yhat, np.sqrt(np.mean((yhat - y) ** 2))

    Ms = [5, 20, 100, 500]
    fits = {M: fit(M) for M in Ms}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.9))
    ax1.plot(x, y, color="#ffffff", lw=2.6, label="target sin(2πx)", zorder=5)
    for M, col in zip(Ms, CYCLE):
        ax1.plot(x, fits[M][0], color=col, lw=1.6, alpha=0.9, label=f"M = {M}")
    ax1.set_title("ReLU units approximating a curve")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$f(x)$")
    ax1.legend(loc="upper right", fontsize=8)

    ax2.loglog(Ms, [fits[M][1] for M in Ms], "-o", color=C, ms=5)
    ax2.set_title("Error falls with width")
    ax2.set_xlabel("hidden units $M$")
    ax2.set_ylabel("RMSE")
    fig.tight_layout()
    save(fig, SUB, "universal-approximation")


def main() -> None:
    apply_style()
    activations()
    initialization()
    dl_optimizers()
    normalization()
    regularization()
    universal_approximation()


if __name__ == "__main__":
    main()
