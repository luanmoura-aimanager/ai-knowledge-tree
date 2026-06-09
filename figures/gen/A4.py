"""Figures for pillar A4 (numerical linear algebra). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import ACCENT, FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "A4"
C = color(SUB)  # pillar-A accent (gold)


def conditioning_stability() -> None:
    """Solving Ax = b in float64: the relative error grows like the condition
    number κ — it tracks the κ·ε bound, so κ = 10¹² loses ~12 of 16 digits.

    Reuses the lesson's matrix builder: random orthogonal U, V and geometrically
    spaced singular values from 1 down to 1/κ (rng(0), n = 50)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    eps = np.finfo(float).eps
    n = 50

    def make_A(kappa):
        U = np.linalg.qr(rng.normal(size=(n, n)))[0]
        V = np.linalg.qr(rng.normal(size=(n, n)))[0]
        s = np.geomspace(1.0, 1.0 / kappa, n)
        return U @ np.diag(s) @ V.T

    kappas = np.geomspace(1e0, 1e15, 31)
    errors = []
    x_true = np.ones(n)
    # κ up to 1e15 deliberately drives nearly-singular solves; the FP flags that
    # raises are the phenomenon under study, not a code bug — silence them.
    with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
        for kappa in kappas:
            A = make_A(kappa)
            b = A @ x_true
            x_hat = np.linalg.solve(A, b)
            errors.append(np.linalg.norm(x_hat - x_true) / np.linalg.norm(x_true))
    errors = np.array(errors)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(kappas, np.clip(errors, eps, None), "-o", color=C, ms=4,
              label="measured relative error")
    ax.loglog(kappas, kappas * eps, color=HOT, ls="--", lw=1.8,
              label=r"bound  $\kappa \cdot \varepsilon_{\mathrm{mach}}$")
    ax.axhline(1.0, color=FG_MUTE, ls=":", lw=1.2, label="no correct digits")
    ax.set_title("Error amplification by the condition number")
    ax.set_xlabel(r"condition number $\kappa(A)$")
    ax.set_ylabel("relative error of the solution")
    ax.set_ylim(1e-17, 10)
    ax.legend(loc="upper left")
    fig.tight_layout()
    save(fig, SUB, "conditioning-stability")


def catastrophic_cancellation() -> None:
    """Subtracting nearly-equal numbers throws away significant digits. Computing
    1 − cos(x) directly loses accuracy as x → 0, while the algebraically identical
    2 sin²(x/2) stays accurate."""
    import matplotlib.pyplot as plt

    x = np.logspace(-8, -0.5, 200)
    true = 2 * np.sin(x / 2) ** 2
    naive = 1 - np.cos(x)
    rel = np.abs(naive - true) / true

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(x, np.clip(rel, 1e-17, None), color=C, lw=2.2)
    ax.axhline(np.finfo(float).eps, color=FG_MUTE, ls="--", lw=1.2,
               label="machine epsilon")
    ax.set_title("Cancellation in 1 − cos(x)")
    ax.set_xlabel("x")
    ax.set_ylabel("relative error of naive 1 − cos(x)")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "catastrophic-cancellation")


def conjugate_gradient() -> None:
    """Conjugate gradient converges far faster than steepest descent on a symmetric
    positive-definite system: it builds A-orthogonal search directions and reaches
    the solution in at most n steps. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 100
    B = rng.normal(size=(n, n))
    A = B @ B.T / n + 0.5 * np.eye(n)
    b = rng.normal(size=n)

    def cg(maxit):
        x = np.zeros(n); r = b - A @ x; p = r.copy(); res = [np.linalg.norm(r)]
        for _ in range(maxit):
            Ap = A @ p; al = (r @ r) / (p @ Ap)
            x = x + al * p; rn = r - al * Ap
            be = (rn @ rn) / (r @ r); p = rn + be * p; r = rn
            res.append(np.linalg.norm(r))
        return res

    def sd(maxit):
        x = np.zeros(n); r = b - A @ x; res = [np.linalg.norm(r)]
        for _ in range(maxit):
            Ar = A @ r; al = (r @ r) / (r @ Ar)
            x = x + al * r; r = b - A @ x; res.append(np.linalg.norm(r))
        return res

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.semilogy(sd(120), color=FG_MUTE, lw=2.0, label="steepest descent")
    ax.semilogy(cg(120), color=C, lw=2.4, label="conjugate gradient")
    ax.set_title("CG vs steepest descent (SPD system)")
    ax.set_xlabel("iteration")
    ax.set_ylabel("residual norm")
    ax.legend(loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "conjugate-gradient")


def floating_point() -> None:
    """Floating-point numbers are spaced logarithmically: the gap to the next
    representable value (one ULP) grows in proportion to the magnitude, so absolute
    precision degrades for large numbers."""
    import matplotlib.pyplot as plt

    exps = np.arange(-10, 11)
    mags = 2.0**exps
    ulp = np.array([np.nextafter(m, np.inf) - m for m in mags])

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.loglog(mags, ulp, "-o", color=C, ms=4)
    ax.set_title("Spacing between consecutive float64 values")
    ax.set_xlabel("magnitude")
    ax.set_ylabel("gap to next float (ULP)")
    fig.tight_layout()
    save(fig, SUB, "floating-point")


def gmres() -> None:
    """GMRES minimizes the residual over a growing Krylov subspace, so its residual
    norm decreases monotonically each iteration until the nonsymmetric system is
    solved. rng(0)."""
    import matplotlib.pyplot as plt
    from scipy.sparse.linalg import gmres as sp_gmres

    rng = np.random.default_rng(0)
    n = 80
    A = rng.normal(size=(n, n)) / np.sqrt(n) + 2 * np.eye(n)
    b = rng.normal(size=n)
    res = []
    sp_gmres(A, b, rtol=1e-10, maxiter=60, restart=60,
             callback=lambda rk: res.append(float(rk)), callback_type="pr_norm")

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.semilogy(range(1, len(res) + 1), res, "-o", color=C, ms=3)
    ax.set_title("GMRES residual decreases monotonically")
    ax.set_xlabel("iteration")
    ax.set_ylabel("relative residual norm")
    fig.tight_layout()
    save(fig, SUB, "gmres")


def iterative_methods() -> None:
    """Stationary iterations like Jacobi converge geometrically when the iteration
    matrix is a contraction: the error shrinks by a roughly constant factor each
    sweep. rng(0), diagonally-dominant system."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 30
    A = rng.normal(size=(n, n))
    A = A + A.T + n * np.eye(n)          # diagonally dominant
    xstar = rng.normal(size=n)
    b = A @ xstar
    D = np.diag(np.diag(A))
    R = A - D
    Dinv = np.diag(1 / np.diag(A))

    x = np.zeros(n); err = [np.linalg.norm(x - xstar)]
    for _ in range(40):
        x = Dinv @ (b - R @ x)
        err.append(np.linalg.norm(x - xstar))

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.semilogy(err, "-o", color=C, ms=3.5)
    ax.set_title("Jacobi iteration: geometric convergence")
    ax.set_xlabel("sweep")
    ax.set_ylabel("error norm")
    fig.tight_layout()
    save(fig, SUB, "iterative-methods")


def log_sum_exp() -> None:
    """The log-sum-exp trick: computing log Σ exp(xᵢ) directly overflows once the
    xᵢ are large, but subtracting the max first makes it stable for any magnitude —
    with an identical result."""
    import matplotlib.pyplot as plt

    shifts = np.linspace(0, 800, 200)
    naive, stable = [], []
    base = np.array([0.0, 1.0, 2.0])
    with np.errstate(over="ignore"):
        for c in shifts:
            x = base + c
            naive.append(np.log(np.sum(np.exp(x))))
            m = x.max()
            stable.append(m + np.log(np.sum(np.exp(x - m))))
    naive = np.array(naive)

    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(shifts, stable, color=C, lw=2.6, label="stable (shift by max)")
    finite = np.isfinite(naive)
    ax.plot(shifts[finite], naive[finite], color=HOT, lw=2.0, ls="--",
            label="naive log Σ exp")
    fail = shifts[~finite]
    if len(fail):
        ax.axvline(fail.min(), color=FG_MUTE, ls=":", lw=1.4,
                   label=f"naive overflows (x≳{fail.min():.0f})")
    ax.set_title("Log-sum-exp: the stabilizing shift")
    ax.set_xlabel("magnitude of inputs")
    ax.set_ylabel("log Σ exp(x)")
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    save(fig, SUB, "log-sum-exp")


def main() -> None:
    apply_style()
    conditioning_stability()
    catastrophic_cancellation()
    conjugate_gradient()
    floating_point()
    gmres()
    iterative_methods()
    log_sum_exp()


if __name__ == "__main__":
    main()
