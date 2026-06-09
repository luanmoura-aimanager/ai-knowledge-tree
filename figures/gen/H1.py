"""Figures for pillar H1 (RL foundations). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_DIM, FG_MUTE, GOOD, GRID, apply_style, color, save

SUB = "H1"
C = color(SUB)  # pillar-H accent (pink)


def dynamic_programming() -> None:
    """Value iteration sweeps the Bellman optimality backup until the value function
    converges; the greedy policy it induces (arrows) then points along the shortest
    path to the goal. A 4×5 gridworld with a −1 step cost."""
    import matplotlib.pyplot as plt

    R, Cc = 4, 5
    goal = (0, 4)
    gamma = 0.95
    V = np.zeros((R, Cc))
    acts = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for _ in range(200):
        Vn = V.copy()
        for i in range(R):
            for j in range(Cc):
                if (i, j) == goal:
                    Vn[i, j] = 0; continue
                best = -1e9
                for di, dj in acts:
                    ni, nj = min(max(i + di, 0), R - 1), min(max(j + dj, 0), Cc - 1)
                    best = max(best, -1 + gamma * V[ni, nj])
                Vn[i, j] = best
        V = Vn

    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    im = ax.imshow(V, cmap="magma")
    for i in range(R):
        for j in range(Cc):
            if (i, j) == goal:
                ax.text(j, i, "★", ha="center", va="center", color=GOOD, fontsize=18)
                continue
            best, ba = -1e9, (0, 0)
            for di, dj in acts:
                ni, nj = min(max(i + di, 0), R - 1), min(max(j + dj, 0), Cc - 1)
                if -1 + gamma * V[ni, nj] > best:
                    best, ba = -1 + gamma * V[ni, nj], (di, dj)
            ax.annotate("", xy=(j + 0.32 * ba[1], i + 0.32 * ba[0]), xytext=(j, i),
                        arrowprops=dict(arrowstyle="-|>", color="#e6e9f5", lw=1.6))
    ax.set_title("Value iteration: V(s) and greedy policy")
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("state value V(s)", color=FG_DIM); cb.ax.tick_params(colors=FG_DIM)
    cb.outline.set_edgecolor(GRID)
    fig.tight_layout()
    save(fig, SUB, "dynamic-programming")


def monte_carlo() -> None:
    """Monte-Carlo prediction estimates a state's value by averaging the returns
    actually observed from it; with no model, the running average converges to the
    true expected return as more episodes accumulate. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    true = 4.0
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    for col, a in [(C, 0.5), (ACCENT, 0.4), (GOOD, 0.35)]:
        returns = true + rng.normal(0, 3, 600)
        run = np.cumsum(returns) / np.arange(1, 601)
        ax.plot(run, color=col, lw=1.4, alpha=a)
    ax.axhline(true, color=FG_MUTE, ls="--", lw=2.0, label="true value")
    ax.set_title("Monte-Carlo estimate converges to the true value")
    ax.set_xlabel("episodes"); ax.set_ylabel("running average return")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "monte-carlo")


def q_learning_sarsa() -> None:
    """On the cliff-walking task, Q-learning learns the optimal but risky path along
    the edge, so its returns swing low whenever ε-exploration steps off the cliff;
    SARSA, learning on-policy, prefers a safer path and earns higher returns during
    training. rng(0)."""
    import matplotlib.pyplot as plt

    rows, cols = 4, 12
    start, goal = (3, 0), (3, 11)
    cliff = {(3, c) for c in range(1, 11)}
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def step(s, a):
        i = min(max(s[0] + moves[a][0], 0), rows - 1)
        j = min(max(s[1] + moves[a][1], 0), cols - 1)
        ns = (i, j)
        if ns in cliff:
            return start, -100
        return ns, (0 if ns == goal else -1)

    def run(sarsa, episodes=500, alpha=0.5, eps=0.1, gamma=1.0, seed=0):
        rng = np.random.default_rng(seed)
        Q = np.zeros((rows, cols, 4))
        rets = []
        egreedy = lambda s: rng.integers(4) if rng.random() < eps else int(np.argmax(Q[s]))
        for _ in range(episodes):
            s = start; a = egreedy(s); total = 0
            for _ in range(200):
                ns, r = step(s, a); total += r
                na = egreedy(ns)
                target = r + gamma * (Q[ns][na] if sarsa else Q[ns].max())
                Q[s][a] += alpha * (target - Q[s][a])
                s, a = ns, na
                if s == goal:
                    break
            rets.append(total)
        return np.array(rets)

    def smooth(x, w=20):
        return np.convolve(x, np.ones(w) / w, mode="valid")

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(smooth(run(False)), color=C, lw=1.8, label="Q-learning (off-policy)")
    ax.plot(smooth(run(True)), color=ACCENT, lw=1.8, label="SARSA (on-policy)")
    ax.set_ylim(-100, 0)
    ax.set_title("Cliff walking: Q-learning vs SARSA")
    ax.set_xlabel("episode"); ax.set_ylabel("return (smoothed)")
    ax.legend(loc="lower right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "q-learning-sarsa")


def main() -> None:
    apply_style()
    dynamic_programming()
    monte_carlo()
    q_learning_sarsa()


if __name__ == "__main__":
    main()
