"""Figures for pillar I4 (monitoring & evaluation). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, HOT, apply_style, color, save

SUB = "I4"
C = color(SUB)  # pillar-I accent (green)


def cost_monitoring() -> None:
    """Monitoring breaks spend down by source so cost spikes are attributable: a stack
    of daily cost by component (inference, training, storage) shows where the money
    goes and surfaces the day a runaway job drove the bill up. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    days = np.arange(30)
    inference = 200 + 8 * days + rng.normal(0, 15, 30)
    training = 120 + rng.normal(0, 20, 30)
    training[18] += 600                              # a runaway training job
    storage = 60 + 1.5 * days

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.stackplot(days, inference, training, storage,
                 colors=[C, ACCENT, FG_MUTE], alpha=0.85,
                 labels=["inference", "training", "storage"])
    ax.annotate("runaway job", (18, 1000), color=HOT, fontsize=9,
                xytext=(20, 1150), textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))
    ax.set_title("Cost monitoring: daily spend by component")
    ax.set_xlabel("day"); ax.set_ylabel("cost ($)")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "cost-monitoring")


def production_drift() -> None:
    """Model performance decays in production as the world drifts away from the
    training distribution; accuracy falls until a retrain resets it. Monitoring this
    curve is what tells you when to retrain. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 120
    acc = np.zeros(n)
    a = 0.92
    retrains = [40, 80]
    for t in range(n):
        a -= 0.0016 + 0.0006 * rng.random()
        if t in retrains:
            a = 0.92
        acc[t] = a + 0.004 * rng.normal()

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(acc * 100, color=C, lw=1.8, label="live accuracy")
    ax.axhline(85, color=HOT, ls="--", lw=1.6, label="SLA floor (85%)")
    for r in retrains:
        ax.axvline(r, color=ACCENT, ls=":", lw=1.6)
    ax.plot([], [], color=ACCENT, ls=":", label="retrain")
    ax.set_title("Production drift: accuracy decays, retrain resets")
    ax.set_xlabel("days since launch"); ax.set_ylabel("accuracy (%)")
    ax.legend(loc="lower left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "production-drift")


def slos_and_error_budgets() -> None:
    """An error budget is the failure a target allows: a 99.9% SLO permits 0.1% errors,
    and the budget burns down as errors occur. A steep burn (an incident) eats the
    month's budget early, signaling that reliability work must take priority. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    days = np.arange(30)
    rate = 0.018 + 0.006 * rng.random(30)            # daily burn rate
    rate[12:16] += np.linspace(0.06, 0.13, 4)        # an incident: faster burn
    budget_left = np.clip(1 - np.cumsum(rate), 0, 1)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(days, budget_left * 100, color=C, lw=2.2, label="error budget remaining")
    ax.fill_between(days, budget_left * 100, color=C, alpha=0.12)
    ax.plot(days, (1 - days / 29) * 100, color=FG_MUTE, ls="--", lw=1.4,
            label="ideal even burn")
    ax.axvspan(12, 16, color=HOT, alpha=0.15, label="incident")
    ax.set_title("Error-budget burn-down")
    ax.set_xlabel("day of month"); ax.set_ylabel("budget remaining (%)")
    ax.legend(loc="lower left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "slos-and-error-budgets")


def automated_retraining() -> None:
    """Average daily cost as a function of the retrain interval. Retraining too often
    pays the fixed retrain cost K repeatedly (K/T falls); retraining too rarely lets
    staleness cost pile up (rises). Their sum is U-shaped with a minimum at the optimal
    cadence ~sqrt(2K/cr)."""
    import matplotlib.pyplot as plt

    K, c, r = 500.0, 1.0, 0.10
    T = np.arange(1, 121)
    amortized = K / T
    staleness = c * r * (T + 1) / 2.0
    total = amortized + staleness
    t_opt = T[np.argmin(total)]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(T, amortized, color=FG_MUTE, ls="--", lw=1.6, label="amortized retrain cost (K/T)")
    ax.plot(T, staleness, color=ACCENT, ls=":", lw=1.8, label="average staleness cost")
    ax.plot(T, total, color=C, lw=2.4, label="total daily cost")
    ax.axvline(t_opt, color=HOT, lw=1.6)
    ax.annotate(f"optimal cadence\n≈ {t_opt} days", (t_opt, total.min()),
                color=HOT, fontsize=9, xytext=(t_opt + 14, total.min() + 6),
                textcoords="data",
                arrowprops=dict(arrowstyle="-|>", color=HOT, lw=1.6))
    ax.set_title("Automated retraining: the optimal cadence")
    ax.set_xlabel("retrain interval T (days)"); ax.set_ylabel("average daily cost ($)")
    # Frame the U near its minimum; the steep K/T tail at small T runs off-top by design.
    ax.set_ylim(0, 5 * total.min())
    ax.legend(loc="upper center", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "automated-retraining")


def main() -> None:
    apply_style()
    automated_retraining()
    cost_monitoring()
    production_drift()
    slos_and_error_budgets()


if __name__ == "__main__":
    main()
