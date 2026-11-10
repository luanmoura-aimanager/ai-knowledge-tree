"""Figures for pillar N8 (frontier recsys). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, HOT, apply_style, color, save

SUB = "N8"
C = color(SUB)  # pillar-N accent (cyan)


def hstu_pointwise() -> None:
    """Attention output magnitude for a query that matches n of 64 history items:
    softmax normalizes the output to a convex combination, so it barely changes with n;
    HSTU's pointwise SiLU aggregation grows with n, so the model can see how many
    relevant actions there were. Same setup as the lesson's code."""
    import matplotlib.pyplot as plt

    ns, soft, point = _count_sensitivity()
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(ns, soft / soft[0], color=HOT, lw=2, label="softmax attention")
    ax.plot(ns, point / point[0], color=GOOD, lw=2, label="pointwise SiLU (HSTU)")
    ax.axhline(1, color=FG_MUTE, ls=":", lw=1)
    ax.set_xlabel("relevant actions in a 64-item history")
    ax.set_ylabel("output size (relative to n = 1)")
    ax.set_title("Softmax forgets how many; pointwise attention counts")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "hstu-count")


def _count_sensitivity():
    rng = np.random.default_rng(0)
    d, H = 16, 64
    q = rng.normal(size=d); q /= np.linalg.norm(q)
    v_rel = rng.normal(size=d)
    ns = np.arange(1, 33)
    soft, point = [], []
    for n in ns:
        K = rng.normal(scale=0.3, size=(H, d)); K[:n] += 6 * q
        V = rng.normal(scale=0.3, size=(H, d)); V[:n] += v_rel
        s = K @ q
        a = np.exp(s - s.max()); a /= a.sum()
        silu = s / (1 + np.exp(-s))
        soft.append(np.linalg.norm(a @ V)); point.append(np.linalg.norm((silu / H) @ V))
    return ns, np.array(soft), np.array(point)


def main() -> None:
    apply_style()
    hstu_pointwise()


if __name__ == "__main__":
    main()
