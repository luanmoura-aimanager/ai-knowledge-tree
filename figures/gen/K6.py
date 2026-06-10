"""Figures for pillar K6 (data quality & governance). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GRID, HOT, apply_style, color, save

SUB = "K6"
C = color(SUB)  # pillar-K accent (mauve)


def data_quality_dimensions() -> None:
    """Each quality dimension becomes a check that produces a pass rate in [0, 1].
    A bar per dimension against a fixed alert threshold (HOT) shows at a glance which
    checks pass and which breach: validity sits below the line and trips an alert."""
    import matplotlib.pyplot as plt

    dims = ["completeness", "validity", "uniqueness", "consistency"]
    rates = [0.97, 0.88, 1.00, 0.95]
    threshold = 0.90
    colors = [HOT if r < threshold else C for r in rates]

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    bars = ax.bar(dims, rates, color=colors, alpha=0.9, width=0.6)
    ax.axhline(threshold, color=HOT, ls="--", lw=1.6, label=f"alert threshold ({threshold:.2f})")
    for b, r in zip(bars, rates):
        ax.text(b.get_x() + b.get_width() / 2, r + 0.01, f"{r:.2f}",
                ha="center", va="bottom", fontsize=9, color="#e6e9f5")
    ax.set_ylim(0.0, 1.08)
    ax.set_ylabel("pass rate")
    ax.set_title("Data quality: pass rate per dimension")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "data-quality-dimensions")


def schema_evolution_contracts() -> None:
    """A compatibility matrix: change type (rows) against the two compatibility
    directions (columns), each cell 1 (safe) or 0 (breaking). Adding an optional field
    is safe both ways; dropping a required field keeps backward compatibility but breaks
    forward; a retype breaks both. The HOT cells are what a data contract must reject."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    changes = ["add optional field", "drop required field", "retype field"]
    cols = ["backward", "forward"]
    # 1 = compatible (safe), 0 = breaking.
    M = np.array([
        [1, 1],   # add optional: safe both directions (full)
        [1, 0],   # drop required: new reader survives (backward), old reader loses a field
        [0, 0],   # retype: breaks both
    ])

    cmap = ListedColormap([HOT, C])  # 0 -> HOT (breaking), 1 -> C (safe)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.imshow(M, cmap=cmap, vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(cols)), cols)
    ax.set_yticks(range(len(changes)), changes)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            label = "safe" if M[i, j] else "breaking"
            ax.text(j, i, label, ha="center", va="center", fontsize=10,
                    color="#0a0e1f", fontweight="bold")
    ax.set_title("Schema-change compatibility matrix")
    ax.grid(False)
    fig.tight_layout()
    save(fig, SUB, "schema-evolution-contracts")


def data_observability() -> None:
    """Daily row volume with a stable baseline and an injected drop. A robust band
    (median +/- threshold * MAD / 0.6745) frames normal variation; the day whose volume
    falls outside the band is flagged (HOT) as an operational anomaly before it reaches
    a dashboard. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 30
    days = np.arange(n)
    volume = 10000 + rng.normal(0, 250, n)
    volume[21] = 4200  # a broken upstream feed: a sharp drop

    median = np.median(volume)
    mad = np.median(np.abs(volume - median))
    rz = 0.6745 * (volume - median) / mad
    thr = 3.5
    band = thr * mad / 0.6745
    flagged = np.abs(rz) > thr

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.axhspan(median - band, median + band, color=C, alpha=0.12, label="robust band (3.5 MAD)")
    ax.axhline(median, color=FG_MUTE, ls="--", lw=1.4, label="median baseline")
    ax.plot(days, volume, color=C, lw=1.8, marker="o", ms=4, label="daily row volume")
    ax.scatter(days[flagged], volume[flagged], color=HOT, s=90, zorder=5, label="anomaly")
    ax.annotate("broken feed", (days[21], volume[21]), color=HOT, fontsize=9,
                xytext=(days[21] - 9, volume[21] + 900), textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))
    ax.set_title("Data observability: volume anomaly via robust z-score")
    ax.set_xlabel("day"); ax.set_ylabel("rows ingested")
    ax.legend(loc="lower left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "data-observability")


def main() -> None:
    apply_style()
    data_quality_dimensions()
    schema_evolution_contracts()
    data_observability()


if __name__ == "__main__":
    main()
