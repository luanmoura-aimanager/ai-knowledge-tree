"""Figures for pillar K1 (data modeling & warehousing). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, GRID, apply_style, color, save

SUB = "K1"
C = color(SUB)  # pillar-K accent (mauve)


def slowly_changing_dimensions() -> None:
    """A Type-2 dimension keeps a versioned timeline per natural key: each version is a
    half-open [effective_from, effective_to) interval carrying the attribute value that
    held then. An 'as-of' lookup is a vertical line: it returns the one version whose
    interval contains the query date. Here one customer's region changes twice."""
    import matplotlib.pyplot as plt

    # One customer's versioned region history (effective_from, effective_to, region).
    versions = [
        (2021.0, 2022.4, "North"),
        (2022.4, 2023.7, "West"),
        (2023.7, 2026.0, "South"),   # current row; effective_to = open (capped for plot)
    ]
    colors = [FG_MUTE, ACCENT, C]
    as_of = 2022.9   # query date lands inside the "West" version

    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    for i, (lo, hi, region) in enumerate(versions):
        y = len(versions) - i
        ax.barh(y, hi - lo, left=lo, height=0.45, color=colors[i],
                alpha=0.9, edgecolor=GRID)
        ax.text((lo + hi) / 2, y, region, ha="center", va="center",
                color="#0a0e1f", fontsize=10, fontweight="bold")
        tag = "current" if i == len(versions) - 1 else f"v{i+1}"
        ax.text(lo + 0.03, y + 0.32, f"{tag}: from {lo:.1f}", ha="left",
                va="bottom", color=colors[i], fontsize=8)

    ax.axvline(as_of, color=HOT, lw=1.8, ls="--")
    ax.annotate(f"as-of {as_of:.1f}\n-> West", (as_of, 2.0), color=HOT, fontsize=9,
                xytext=(as_of + 0.25, 2.6), textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))

    ax.set_yticks(range(1, len(versions) + 1))
    ax.set_yticklabels([f"row {len(versions)-i}" for i in range(len(versions))])
    ax.set_xlabel("effective time (year)")
    ax.set_title("Type-2 dimension: one key, versioned over time")
    ax.set_xlim(2020.7, 2026.3)
    ax.set_ylim(0.3, 3.9)
    fig.tight_layout()
    save(fig, SUB, "slowly-changing-dimensions")


def normalization_tradeoffs() -> None:
    """Total query cost vs the read fraction of the workload, for a normalized (join)
    layout against a denormalized (single-scan) layout. The join layout pays a per-read
    join surcharge but cheap writes; the wide layout pays cheap reads but a per-write
    update surcharge (one fact maintained in many rows). The two cost lines cross: the
    denormalized layout wins once reads dominate."""
    import matplotlib.pyplot as plt

    # Cost model (rows touched, arbitrary units), mirrors the lesson's python block.
    read_frac = np.linspace(0.0, 1.0, 101)
    R_norm, R_denorm = 3.0, 1.0     # per-read cost: join touches 3x, wide scan 1x
    W_norm, W_denorm = 1.0, 4.0     # per-write cost: wide fans the update out 4x

    norm = read_frac * R_norm + (1 - read_frac) * W_norm
    denorm = read_frac * R_denorm + (1 - read_frac) * W_denorm

    # Crossover read fraction where the two are equal.
    cross = (W_norm - W_denorm) / ((R_denorm - R_norm) - (W_denorm - W_norm))

    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.plot(read_frac, norm, color=FG_MUTE, lw=2.2,
            label="normalized (join per read)")
    ax.plot(read_frac, denorm, color=C, lw=2.4,
            label="denormalized (scan; fan-out per write)")
    ax.axvline(cross, color=HOT, lw=1.6, ls="--")
    ax.annotate(f"crossover\nread frac ~ {cross:.2f}", (cross, 2.0), color=HOT,
                fontsize=9, xytext=(cross + 0.06, 2.7), textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))
    ax.fill_between(read_frac, denorm, norm, where=(denorm < norm),
                    color=C, alpha=0.12)
    ax.set_xlabel("read fraction of workload")
    ax.set_ylabel("total cost per op (rows touched)")
    ax.set_title("Normalize vs denormalize: cost vs read/write mix")
    ax.legend(loc="upper center", fontsize=8)
    ax.set_xlim(0, 1)
    fig.tight_layout()
    save(fig, SUB, "normalization-tradeoffs")


def main() -> None:
    apply_style()
    slowly_changing_dimensions()
    normalization_tradeoffs()


if __name__ == "__main__":
    main()
