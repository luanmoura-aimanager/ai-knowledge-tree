"""Figures for pillar H2 (deep RL). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "H2"
C = color(SUB)  # pillar-H accent (pink)


def function_approximation() -> None:
    """With too many states to tabulate, RL approximates the value function with a
    parametric model that generalizes across states — so a few sampled states (dots)
    fix the value everywhere, including states never visited. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    s = np.linspace(0, 10, 200)
    true = np.sin(s) + 0.1 * s
    xt = np.sort(rng.uniform(0, 10, 12))
    yt = np.sin(xt) + 0.1 * xt + 0.1 * rng.normal(size=xt.size)
    coef = np.polyfit(xt, yt, 6)
    approx = np.polyval(coef, s)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(s, true, color=FG_MUTE, ls="--", lw=1.6, label="true value function")
    ax.plot(s, approx, color=C, lw=2.4, label="function approximation")
    ax.scatter(xt, yt, s=30, color=ACCENT, zorder=5, label="sampled states")
    ax.set_title("Value-function approximation generalizes")
    ax.set_xlabel("state"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "function-approximation")


def dqn_improvements() -> None:
    """Each DQN trick attacks a specific failure: a target network and replay
    stabilize the moving target, Double DQN removes overestimation, and prioritized
    replay speeds learning — stacking them lifts the learning curve. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    ep = np.arange(300)
    def curve(rate, ceil, noise):
        return ceil * (1 - np.exp(-ep / rate)) + rng.normal(0, noise, ep.size)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(ep, curve(120, 0.55, 0.05), color=FG_MUTE, lw=1.6, label="vanilla DQN")
    ax.plot(ep, curve(80, 0.78, 0.04), color=ACCENT, lw=1.8, label="+ Double + target net")
    ax.plot(ep, curve(55, 0.92, 0.035), color=C, lw=2.0, label="+ prioritized + dueling (Rainbow)")
    ax.set_title("DQN improvements lift the learning curve")
    ax.set_xlabel("training episodes"); ax.set_ylabel("normalized return")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "dqn-improvements")


def policy_gradient() -> None:
    """Policy gradient pushes the policy's parameters in the direction that increases
    expected return, estimated from sampled trajectories. The return climbs in noisy
    steps because each gradient is a high-variance Monte-Carlo estimate. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    it = np.arange(200)
    base = 1 - np.exp(-it / 45)
    runs = [base * 200 + rng.normal(0, 14, it.size) for _ in range(4)]
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for r in runs:
        ax.plot(it, r, color=C, lw=0.8, alpha=0.4)
    ax.plot(it, np.mean(runs, axis=0), color=ACCENT, lw=2.4, label="mean return")
    ax.set_title("Policy gradient: noisy but steady improvement")
    ax.set_xlabel("policy update"); ax.set_ylabel("episode return")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "policy-gradient")


def ppo() -> None:
    """PPO's clipped objective caps how much the policy can change per update: when
    the probability ratio strays outside [1−ε, 1+ε], the objective flattens, removing
    the incentive to take a large, destabilizing step. The clip is what keeps PPO
    stable."""
    import matplotlib.pyplot as plt

    r = np.linspace(0, 2, 400)
    eps = 0.2
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for A, col, lab in [(1.0, C, "advantage A > 0"), (-1.0, ACCENT, "advantage A < 0")]:
        # PPO clipped surrogate: min(r·A, clip(r,1-ε,1+ε)·A) for either sign of A
        obj = np.minimum(A * r, A * np.clip(r, 1 - eps, 1 + eps))
        ax.plot(r, obj, color=col, lw=2.4, label=lab)
    ax.axvspan(1 - eps, 1 + eps, color=GOOD, alpha=0.12, label="trust region [1−ε, 1+ε]")
    ax.axvline(1.0, color=GRID, lw=0.8)
    ax.set_title("PPO clipped surrogate objective")
    ax.set_xlabel("probability ratio  $r = \\pi / \\pi_{old}$")
    ax.set_ylabel("clipped objective")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "ppo")


def main() -> None:
    apply_style()
    function_approximation()
    dqn_improvements()
    policy_gradient()
    ppo()


if __name__ == "__main__":
    main()
