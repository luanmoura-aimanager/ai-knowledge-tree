"""Figures for pillar F3 (sequential latent models). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "F3"
C = color(SUB)  # pillar-F accent (cyan)


def hidden_markov_models() -> None:
    """The forward algorithm filters a hidden state from noisy observations: it keeps
    a running posterior P(state | observations so far). Here a two-state chain's
    filtered belief tracks the true (shaded) state, lagging slightly at switches.
    rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    A = np.array([[0.95, 0.05], [0.05, 0.95]])
    mu = np.array([0.0, 3.0])
    T = 80
    s = np.zeros(T, int)
    obs = np.zeros(T)
    for t in range(T):
        s[t] = rng.integers(2) if t == 0 else rng.choice(2, p=A[s[t - 1]])
        obs[t] = rng.normal(mu[s[t]], 1.0)

    # forward filtering
    def emit(o):
        return np.exp(-0.5 * (o - mu) ** 2)
    alpha = np.zeros((T, 2))
    a = np.array([0.5, 0.5]) * emit(obs[0]); alpha[0] = a / a.sum()
    for t in range(1, T):
        a = (alpha[t - 1] @ A) * emit(obs[t]); alpha[t] = a / a.sum()

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.fill_between(range(T), 0, s, step="mid", color=FG_MUTE, alpha=0.25, label="true state")
    ax.plot(alpha[:, 1], color=C, lw=2.2, label="filtered P(state = 1)")
    ax.set_title("HMM forward filtering")
    ax.set_xlabel("time step"); ax.set_ylabel("P(state = 1)")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "hidden-markov-models")


def kalman_filter() -> None:
    """The Kalman filter fuses a motion model with noisy measurements: it predicts,
    then corrects, producing an estimate smoother than the raw measurements with a
    shrinking uncertainty band. rng(0), 1D tracking."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    T = 60
    true = np.cumsum(rng.normal(0, 0.4, T)) + 2.0
    R, Q = 1.2, 0.2                       # measurement / process variance
    z = true + rng.normal(0, np.sqrt(R), T)
    xhat = np.zeros(T); P = np.zeros(T)
    xhat[0], P[0] = z[0], 1.0
    for t in range(1, T):
        xp, Pp = xhat[t - 1], P[t - 1] + Q
        K = Pp / (Pp + R)
        xhat[t] = xp + K * (z[t] - xp); P[t] = (1 - K) * Pp

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.scatter(range(T), z, s=14, color=FG_MUTE, alpha=0.6, label="measurements")
    ax.plot(true, color=GOOD, lw=2.0, label="true position")
    ax.plot(xhat, color=C, lw=2.4, label="Kalman estimate")
    ax.fill_between(range(T), xhat - 2 * np.sqrt(P), xhat + 2 * np.sqrt(P),
                    color=C, alpha=0.18, label="±2σ")
    ax.set_title("Kalman filter: predict then correct")
    ax.set_xlabel("time step"); ax.set_ylabel("position")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "kalman-filter")


def particle_filters() -> None:
    """A particle filter represents the state posterior with a weighted cloud of
    samples: each step propagates particles through the motion model, reweights them
    by the measurement, and resamples. The cloud tracks the true state and widens when
    uncertain. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    T, N = 40, 300
    true = np.cumsum(rng.normal(0, 0.5, T))
    z = true + rng.normal(0, 0.8, T)
    P = rng.normal(0, 1, N)
    est = np.zeros(T)
    xs_t, xs_v = [], []
    for t in range(T):
        P = P + rng.normal(0, 0.5, N)                     # propagate
        w = np.exp(-0.5 * ((z[t] - P) / 0.8) ** 2); w /= w.sum()
        est[t] = (w * P).sum()
        idx = rng.choice(N, N, p=w); P = P[idx]           # resample
        xs_t.append(np.full(N, t)); xs_v.append(P.copy())

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.scatter(np.concatenate(xs_t), np.concatenate(xs_v), s=2, color=C, alpha=0.12)
    ax.plot(true, color=GOOD, lw=2.0, label="true state")
    ax.plot(est, color=HOT, lw=2.0, label="particle estimate")
    ax.set_title("Particle filter: a weighted sample cloud")
    ax.set_xlabel("time step"); ax.set_ylabel("state")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "particle-filters")


def main() -> None:
    apply_style()
    hidden_markov_models()
    kalman_filter()
    particle_filters()


if __name__ == "__main__":
    main()
