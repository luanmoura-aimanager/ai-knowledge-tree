"""Figures for pillar J7 (capacity & cost modeling). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, HOT, apply_style, color, save

SUB = "J7"
C = color(SUB)  # pillar-J accent


def capacity_cost_modeling() -> None:
    """Capacity is provisioned in discrete units: if one replica serves ~80 req/s,
    the replicas needed step up as a staircase with demand. You must provision for the
    peak (plus headroom), so cost is set by the highest step — and the gap above the
    smooth demand curve is paid-for idle capacity."""
    import matplotlib.pyplot as plt

    qps = np.linspace(0, 500, 500)
    per_replica = 80
    replicas = np.ceil(np.maximum(qps, 1e-9) / per_replica)
    capacity = replicas * per_replica

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(qps, capacity, color=C, lw=2.4, label="provisioned capacity (staircase)")
    ax.plot(qps, qps, color=FG_MUTE, ls="--", lw=1.6, label="actual demand")
    ax.fill_between(qps, qps, capacity, color=C, alpha=0.12, label="paid-for headroom")
    peak = 360
    ax.axvline(peak, color=HOT, ls=":", lw=1.6, label="peak demand")
    ax.set_title("Capacity planning: provision in discrete replicas")
    ax.set_xlabel("demand (requests / s)")
    ax.set_ylabel("capacity (requests / s)")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "capacity-cost-modeling")


def main() -> None:
    apply_style()
    capacity_cost_modeling()


if __name__ == "__main__":
    main()
