"""Figures for pillar F6 (MCMC). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "F6"
C = color(SUB)  # pillar-F accent (cyan)


def _corr_gauss_grid(rho=0.85):
    g = np.linspace(-3.5, 3.5, 200)
    gx, gy = np.meshgrid(g, g)
    z = (gx**2 - 2 * rho * gx * gy + gy**2) / (2 * (1 - rho**2))
    return gx, gy, np.exp(-z)


def metropolis_hastings() -> None:
    """Metropolis–Hastings explores a target by proposing a random step and
    accepting it with probability min(1, p_new/p_old): the chain spends time in each
    region in proportion to its probability, so the sample histogram converges to the
    target density. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)

    def target(x):
        return 0.6 * np.exp(-0.5 * (x + 2) ** 2) + 0.4 * np.exp(-0.5 * (x - 2) ** 2 / 0.6)

    x = 0.0
    samples = []
    for _ in range(40000):
        xp = x + rng.normal(0, 1.2)
        if rng.random() < target(xp) / target(x):
            x = xp
        samples.append(x)
    samples = np.array(samples[2000:])

    xs = np.linspace(-6, 6, 400)
    dens = target(xs)
    dens /= np.trapezoid(dens, xs)
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.hist(samples, bins=60, density=True, color=C, alpha=0.55, label="MH samples")
    ax.plot(xs, dens, color=HOT, lw=2.4, label="target density")
    ax.set_title("Metropolis–Hastings samples match the target")
    ax.set_xlabel("x"); ax.set_ylabel("density")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "metropolis-hastings")


def gibbs_sampling() -> None:
    """Gibbs sampling updates one coordinate at a time from its exact conditional, so
    the chain moves in axis-aligned steps. On a correlated Gaussian this gives the
    characteristic zigzag — and slow mixing along the correlation direction. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    rho = 0.85
    sd = np.sqrt(1 - rho**2)
    x, y = -2.5, 2.5
    path = [(x, y)]
    for _ in range(40):
        x = rng.normal(rho * y, sd); path.append((x, y))
        y = rng.normal(rho * x, sd); path.append((x, y))
    path = np.array(path)

    gx, gy, dens = _corr_gauss_grid(rho)
    fig, ax = plt.subplots(figsize=(6.0, 5.2))
    ax.contour(gx, gy, dens, levels=8, colors=GRID, linewidths=0.8)
    ax.plot(path[:, 0], path[:, 1], color=C, lw=1.2, alpha=0.9)
    ax.scatter(path[:, 0], path[:, 1], s=10, color=HOT, zorder=3)
    ax.set_aspect("equal")
    ax.set_title("Gibbs sampling: axis-aligned zigzag")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    fig.tight_layout()
    save(fig, SUB, "gibbs-sampling")


def hamiltonian_mc() -> None:
    """Hamiltonian Monte Carlo augments the state with momentum and follows the
    distribution's gradient (leapfrog integration), so it proposes distant points
    that are still accepted — exploring far more efficiently than random-walk steps.
    rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    rho = 0.85
    cov = np.array([[1, rho], [rho, 1]])
    prec = np.linalg.inv(cov)
    grad = lambda q: -prec @ q

    def leapfrog(q, p, eps=0.18, L=25):
        traj = [q.copy()]
        p = p + 0.5 * eps * grad(q)
        for _ in range(L):
            q = q + eps * p
            p = p + eps * grad(q)
            traj.append(q.copy())
        return np.array(traj)

    q = np.array([-2.0, 2.0])
    samples = [q.copy()]
    one_traj = None
    for it in range(60):
        p0 = rng.normal(size=2)
        traj = leapfrog(q.copy(), p0.copy())
        q = traj[-1]
        samples.append(q.copy())
        if it == 0:
            one_traj = traj
    samples = np.array(samples)

    gx, gy, dens = _corr_gauss_grid(rho)
    fig, ax = plt.subplots(figsize=(6.0, 5.2))
    ax.contour(gx, gy, dens, levels=8, colors=GRID, linewidths=0.8)
    ax.plot(one_traj[:, 0], one_traj[:, 1], color=GOOD, lw=1.6, label="one leapfrog trajectory")
    ax.scatter(samples[:, 0], samples[:, 1], s=16, color=C, zorder=3, label="HMC samples")
    ax.set_aspect("equal")
    ax.set_title("HMC follows the gradient to distant points")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "hamiltonian-mc")


def langevin_sgld() -> None:
    """Langevin dynamics turns sampling into noisy gradient ascent: each step climbs
    the log-density and adds calibrated Gaussian noise, so the trajectory settles into
    and then wanders through the high-probability region. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    rho = 0.85
    cov = np.array([[1, rho], [rho, 1]])
    prec = np.linalg.inv(cov)
    eps = 0.08
    q = np.array([-3.0, 3.0])
    path = [q.copy()]
    for _ in range(300):
        q = q - 0.5 * eps * (prec @ q) + np.sqrt(eps) * rng.normal(size=2)
        path.append(q.copy())
    path = np.array(path)

    gx, gy, dens = _corr_gauss_grid(rho)
    fig, ax = plt.subplots(figsize=(6.0, 5.2))
    ax.contour(gx, gy, dens, levels=8, colors=GRID, linewidths=0.8)
    ax.plot(path[:, 0], path[:, 1], color=C, lw=0.8, alpha=0.8)
    ax.scatter(path[0, 0], path[0, 1], s=40, color=HOT, zorder=3, label="start")
    ax.set_aspect("equal")
    ax.set_title("Langevin dynamics: gradient + noise")
    ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "langevin-sgld")


def rejection_importance_sampling() -> None:
    """Rejection sampling draws from a simple proposal scaled to envelope the target,
    then keeps each point with probability p(x)/(M·q(x)): accepted points (under the
    target curve) are exact target samples; the rest are thrown away. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)

    def target(x):
        return 0.6 * np.exp(-0.5 * (x + 1.5) ** 2) + 0.4 * np.exp(-0.5 * (x - 1.8) ** 2 / 0.5)

    sig = 2.5
    q = lambda x: np.exp(-0.5 * (x / sig) ** 2) / (sig * np.sqrt(2 * np.pi))
    M = np.max(target(np.linspace(-6, 6, 1000)) / q(np.linspace(-6, 6, 1000))) * 1.02

    xp = rng.normal(0, sig, 800)
    u = rng.random(800) * M * q(xp)
    acc = u < target(xp)

    xs = np.linspace(-6, 6, 400)
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ax.plot(xs, target(xs), color=HOT, lw=2.4, label="target p(x)")
    ax.plot(xs, M * q(xs), color=FG_MUTE, ls="--", lw=1.8, label="envelope M·q(x)")
    ax.scatter(xp[acc], u[acc], s=8, color=C, alpha=0.7, label="accepted")
    ax.scatter(xp[~acc], u[~acc], s=8, color=FG_MUTE, alpha=0.4, label="rejected")
    ax.set_title("Rejection sampling")
    ax.set_xlabel("x"); ax.set_ylabel("height under envelope")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "rejection-importance-sampling")


def main() -> None:
    apply_style()
    metropolis_hastings()
    gibbs_sampling()
    hamiltonian_mc()
    langevin_sgld()
    rejection_importance_sampling()


if __name__ == "__main__":
    main()
