"""Figures for pillar C6 (anomaly detection). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, LEGEND_BG, apply_style, color, save

SUB = "C6"
C = color(SUB)  # pillar-C accent


def statistical_ad() -> None:
    """Threshold-based outlier detection: the IQR fences (1.5·IQR) and the ±3σ
    z-score band flag the three planted outliers. The robust IQR fences sit
    tighter than the σ band, which the outliers themselves inflate. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    normal = rng.normal(0, 1, 200)
    outliers = np.array([6.0, -7.0, 8.0])
    data = np.concatenate([normal, outliers])
    idx = np.arange(len(data))

    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    mu, sd = data.mean(), data.std()
    zlo, zhi = mu - 3 * sd, mu + 3 * sd

    is_out = (data < lo) | (data > hi)

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.scatter(idx[~is_out], data[~is_out], s=14, color=ACCENT, edgecolor="none",
               label="inliers")
    ax.scatter(idx[is_out], data[is_out], s=70, color=HOT, marker="X",
               edgecolor="none", zorder=4, label="flagged (IQR)")
    ax.axhline(hi, color=C, ls="-", lw=1.4, label="IQR fence (1.5·IQR)")
    ax.axhline(lo, color=C, ls="-", lw=1.4)
    ax.axhline(zhi, color=FG_MUTE, ls="--", lw=1.4, label="z-score ±3σ")
    ax.axhline(zlo, color=FG_MUTE, ls="--", lw=1.4)
    ax.set_title("Statistical outlier thresholds")
    ax.set_xlabel("sample index")
    ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=9, frameon=True, facecolor=LEGEND_BG,
              edgecolor=FG_MUTE, framealpha=0.92)
    fig.tight_layout()
    save(fig, SUB, "statistical-ad")


def main() -> None:
    apply_style()
    statistical_ad()


if __name__ == "__main__":
    main()
