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


def feature_engineering() -> None:
    """A transform fitted on the wrong data leaks held-out statistics into training,
    so the offline score is inflated above the honest accuracy the model reaches in
    production. The clean pipeline (fit on train only) reports an offline score that
    matches production; the leaky one shows a large optimism gap. rng(0)."""
    import matplotlib.pyplot as plt

    labels = ["leaky pipeline\n(fit on all data)", "clean pipeline\n(fit on train only)"]
    offline = np.array([0.94, 0.86])      # reported offline score
    production = np.array([0.82, 0.85])   # honest accuracy in production
    x = np.arange(len(labels))
    w = 0.36

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(x - w / 2, offline * 100, w, color=C, label="offline score (reported)")
    ax.bar(x + w / 2, production * 100, w, color=FG_MUTE, label="production accuracy (actual)")
    # Mark the optimism gap the leak opens.
    ax.annotate("", (x[0] - w / 2, offline[0] * 100), (x[0] + w / 2, production[0] * 100),
                arrowprops=dict(arrowstyle="<->", color=HOT, lw=1.8))
    ax.text(x[0] + 0.05, (offline[0] + production[0]) / 2 * 100, "leakage\noptimism",
            color=HOT, fontsize=9, va="center")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylim(60, 100)
    ax.set_ylabel("accuracy (%)")
    ax.set_title("Feature leakage inflates the offline score")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "feature-engineering")


def main() -> None:
    apply_style()
    drift_detection()
    feature_engineering()


if __name__ == "__main__":
    main()
