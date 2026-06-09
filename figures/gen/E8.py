"""Figures for pillar E8 (interpretability & frontier). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "E8"
C = color(SUB)  # pillar-E accent (purple)


def emergent_abilities() -> None:
    """Some abilities stay at chance until the model crosses a scale threshold, then
    jump sharply — 'emergence'. On a smooth log-scale of model size the metric looks
    like a phase transition rather than a gradual climb."""
    import matplotlib.pyplot as plt

    params = np.logspace(7, 12, 200)
    lp = np.log10(params)
    acc = 0.02 + 0.9 / (1 + np.exp(-(lp - 10.3) * 4.5))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.semilogx(params, acc, color=C, lw=2.6)
    ax.axhline(0.02, color=FG_MUTE, ls="--", lw=1.2, label="chance")
    ax.set_title("Emergent ability vs model scale")
    ax.set_xlabel("model parameters")
    ax.set_ylabel("task accuracy")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "emergent-abilities")


def induction_heads() -> None:
    """An induction head implements in-context copying: at a token that repeats an
    earlier one, it attends to the token that *followed* the previous occurrence and
    predicts it next. The attention map shows that shifted-diagonal stripe."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    rng = np.random.default_rng(0)
    period = 4
    seq = np.tile(rng.integers(0, period, period), 3)   # repeating pattern
    n = len(seq)
    attn = np.zeros((n, n)) + 0.02
    for t in range(1, n):
        for j in range(t):
            if seq[j] == seq[t - 1] and j + 1 < t:
                attn[t, j + 1] += 1.0                    # attend to token AFTER the match
    attn = attn / attn.sum(axis=1, keepdims=True)
    cmap = LinearSegmentedColormap.from_list("e8", ["#141a35", C])

    fig, ax = plt.subplots(figsize=(5.6, 5.0))
    ax.imshow(attn, cmap=cmap, vmin=0, vmax=1)
    ax.set_title("Induction-head attention pattern")
    ax.set_xlabel("key position (attended to)")
    ax.set_ylabel("query position")
    ax.grid(False)
    fig.tight_layout()
    save(fig, SUB, "induction-heads")


def probing() -> None:
    """A linear probe reveals where information lives in the residual stream: simple
    syntactic features are most decodable in early-to-middle layers, while abstract
    semantic features peak later. Probe accuracy by layer."""
    import matplotlib.pyplot as plt

    layers = np.arange(0, 24)
    syntax = 0.5 + 0.46 * np.exp(-((layers - 6) ** 2) / 36)
    semantics = 0.5 + 0.42 * np.exp(-((layers - 17) ** 2) / 60)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(layers, syntax, "-o", color=C, ms=3.5, label="syntactic feature")
    ax.plot(layers, semantics, "-o", color=HOT, ms=3.5, label="semantic feature")
    ax.axhline(0.5, color=FG_MUTE, ls="--", lw=1.2, label="chance")
    ax.set_title("Probe accuracy by layer")
    ax.set_xlabel("layer")
    ax.set_ylabel("probe accuracy")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "probing")


def sparse_autoencoders() -> None:
    """A sparse autoencoder trades reconstruction fidelity against sparsity: allowing
    more active features per token lowers reconstruction error along a Pareto
    frontier. SAEs pick a sparse point that yields interpretable, monosemantic
    features."""
    import matplotlib.pyplot as plt

    l0 = np.linspace(4, 200, 80)
    recon = 0.04 + 3.0 / l0          # more active features -> lower error

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(l0, recon, color=C, lw=2.6)
    ax.scatter([20], [0.04 + 3.0 / 20], s=90, color=HOT, zorder=5,
               label="chosen sparse point")
    ax.set_title("Sparse autoencoder: reconstruction vs sparsity")
    ax.set_xlabel("active features per token (L0)")
    ax.set_ylabel("reconstruction error")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "sparse-autoencoders")


def superposition() -> None:
    """Superposition: a model can represent more features than it has dimensions by
    storing them as nearly-orthogonal directions. Five features packed into a 2D
    space spread out as a pentagon, tolerating slight interference between them."""
    import matplotlib.pyplot as plt

    n_feat = 5
    ang = np.linspace(0, 2 * np.pi, n_feat, endpoint=False) + np.pi / 2
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    for k, a in enumerate(ang):
        v = np.array([np.cos(a), np.sin(a)])
        ax.annotate("", xy=v, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=C, lw=2.4))
        ax.text(v[0] * 1.12, v[1] * 1.12, f"f{k+1}", color=FG_DIM, fontsize=11,
                ha="center", va="center")
    ax.add_artist(plt.Circle((0, 0), 1.0, fill=False, color=GRID, lw=0.8))
    ax.axhline(0, color=GRID, lw=0.8); ax.axvline(0, color=GRID, lw=0.8)
    ax.set_aspect("equal"); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Superposition: 5 features in 2 dimensions")
    fig.tight_layout()
    save(fig, SUB, "superposition")


def main() -> None:
    apply_style()
    emergent_abilities()
    induction_heads()
    probing()
    sparse_autoencoders()
    superposition()


if __name__ == "__main__":
    main()
