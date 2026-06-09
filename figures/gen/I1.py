"""Figures for pillar I1 (data & drift). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

SUB = "I1"
C = color(SUB)  # pillar-I accent (green)


def drift_detection() -> None:
    """Data drift is a shift between the distribution a model was trained on and the
    one it now sees. A drift metric (here population stability index) stays low while
    the live data matches training, then climbs past an alert threshold once the
    feature distribution moves. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    weeks = np.arange(30)
    # reference histogram bins
    ref = rng.normal(0, 1, 5000)
    edges = np.percentile(ref, np.linspace(0, 100, 11))
    ref_p = np.histogram(ref, edges)[0] / len(ref) + 1e-6
    psi = []
    for w in weeks:
        shift = 0.0 if w < 15 else 0.12 * (w - 15)
        cur = rng.normal(shift, 1 + 0.03 * max(0, w - 15), 1500)
        cur_p = np.histogram(cur, edges)[0] / len(cur) + 1e-6
        psi.append(np.sum((cur_p - ref_p) * np.log(cur_p / ref_p)))

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(weeks, psi, "-o", color=C, ms=4, label="population stability index")
    ax.axhline(0.2, color=HOT, ls="--", lw=1.6, label="alert threshold (0.2)")
    ax.axvline(15, color=FG_MUTE, ls=":", lw=1.4, label="distribution starts shifting")
    ax.set_title("Drift detection: PSI rises as data shifts")
    ax.set_xlabel("weeks since deployment"); ax.set_ylabel("PSI")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "drift-detection")


def main() -> None:
    apply_style()
    drift_detection()


if __name__ == "__main__":
    main()
