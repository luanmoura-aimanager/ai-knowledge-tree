"""Figures for pillar G1 (classical time series). See figures/gen/_style.py."""

from __future__ import annotations

import numpy as np

from _style import FG_MUTE, GOOD, GRID, HOT, apply_style, color, save

SUB = "G1"
C = color(SUB)  # pillar-G accent (teal)


def _acf(x, nlags=30):
    x = x - x.mean()
    n = len(x)
    denom = (x**2).sum()
    return np.array([1.0 if k == 0 else (x[:n - k] * x[k:]).sum() / denom
                     for k in range(nlags + 1)])


def stationarity_acf() -> None:
    """A stationary series has a constant mean and an ACF that decays quickly; a
    random walk drifts with no fixed mean and an ACF that stays near 1 for many lags.
    The ACF is the quickest visual test for stationarity. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 300
    e = rng.normal(size=n)
    ar = np.zeros(n)
    for t in range(1, n):
        ar[t] = 0.6 * ar[t - 1] + e[t]
    rw = np.cumsum(rng.normal(size=n))

    fig, axes = plt.subplots(2, 2, figsize=(8.8, 4.6))
    axes[0, 0].plot(ar, color=C, lw=1.0); axes[0, 0].set_title("stationary AR(1)")
    axes[0, 1].plot(rw, color=HOT, lw=1.0); axes[0, 1].set_title("random walk")
    for ax, x, col in [(axes[1, 0], ar, C), (axes[1, 1], rw, HOT)]:
        ac = _acf(x, 30)
        ax.bar(range(31), ac, color=col, width=0.7)
        ax.axhline(0, color=GRID, lw=0.8)
        ax.set_xlabel("lag"); ax.set_ylabel("ACF")
    fig.tight_layout()
    save(fig, SUB, "stationarity-acf")


def ar_ma_processes() -> None:
    """AR and MA processes leave different ACF fingerprints: an AR(1)'s autocorrelation
    decays geometrically, while an MA(1)'s cuts off sharply after lag 1 — which is how
    you read the order off the data. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 4000
    e = rng.normal(size=n)
    ar = np.zeros(n)
    for t in range(1, n):
        ar[t] = 0.7 * ar[t - 1] + e[t]
    ma = e[1:] + 0.8 * e[:-1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.9))
    ax1.bar(range(16), _acf(ar, 15), color=C, width=0.7)
    ax1.set_title("AR(1): ACF decays geometrically")
    ax2.bar(range(16), _acf(ma, 15), color=HOT, width=0.7)
    ax2.set_title("MA(1): ACF cuts off after lag 1")
    for ax in (ax1, ax2):
        ax.axhline(0, color=GRID, lw=0.8); ax.set_xlabel("lag"); ax.set_ylabel("ACF")
    fig.tight_layout()
    save(fig, SUB, "ar-ma-processes")


def arima_sarima() -> None:
    """ARIMA forecasts by differencing a series to stationarity, fitting the AR/MA
    structure, then integrating back. The forecast reverts toward the mean with a
    widening interval as the horizon grows. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 120
    e = rng.normal(size=n)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = 0.75 * x[t - 1] + e[t]
    x = x + 0.05 * np.arange(n)            # mild trend
    phi = 0.75
    h = 30
    fc = np.zeros(h); last = x[-1] - 0.05 * (n - 1)
    for i in range(h):
        last = phi * last
        fc[i] = last + 0.05 * (n + i)
    se = np.sqrt(np.cumsum(phi ** (2 * np.arange(h))))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(range(n), x, color=C, lw=1.4, label="observed")
    fx = np.arange(n, n + h)
    ax.plot(fx, fc, color=HOT, lw=2.0, label="forecast")
    ax.fill_between(fx, fc - 2 * se, fc + 2 * se, color=HOT, alpha=0.18, label="±2σ")
    ax.axvline(n - 1, color=FG_MUTE, ls=":", lw=1.2)
    ax.set_title("ARIMA forecast with widening interval")
    ax.set_xlabel("time"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "arima-sarima")


def exponential_smoothing() -> None:
    """Exponential smoothing forecasts with a weighted average that decays into the
    past: simple smoothing tracks the level, while Holt's method adds a trend term so
    the forecast can keep climbing. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 80
    trend = 0.3 * np.arange(n)
    y = trend + 3 * np.sin(np.arange(n) / 6) + rng.normal(0, 1.2, n)
    a = 0.3
    ses = np.zeros(n); ses[0] = y[0]
    for t in range(1, n):
        ses[t] = a * y[t] + (1 - a) * ses[t - 1]
    # Holt linear trend
    lv = np.zeros(n); tr = np.zeros(n); lv[0], tr[0] = y[0], 0.3
    b = 0.2
    for t in range(1, n):
        lv[t] = a * y[t] + (1 - a) * (lv[t - 1] + tr[t - 1])
        tr[t] = b * (lv[t] - lv[t - 1]) + (1 - b) * tr[t - 1]
    holt = lv + tr

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(y, color=FG_MUTE, lw=1.0, alpha=0.7, label="data")
    ax.plot(ses, color=C, lw=2.2, label="simple smoothing")
    ax.plot(holt, color=HOT, lw=2.2, label="Holt (level + trend)")
    ax.set_title("Exponential smoothing")
    ax.set_xlabel("time"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "exponential-smoothing")


def garch_volatility() -> None:
    """GARCH models volatility clustering: large moves beget large moves, so the
    conditional standard deviation σₜ rises in turbulent stretches and falls in calm
    ones — tracking the bursts of variance in the returns. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 500
    omega, alpha, beta = 0.05, 0.12, 0.85
    r = np.zeros(n); s2 = np.zeros(n); s2[0] = omega / (1 - alpha - beta)
    for t in range(1, n):
        s2[t] = omega + alpha * r[t - 1] ** 2 + beta * s2[t - 1]
        r[t] = np.sqrt(s2[t]) * rng.normal()

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(r, color=C, lw=0.7, alpha=0.8, label="returns")
    ax.plot(2 * np.sqrt(s2), color=HOT, lw=1.8, label="±2σₜ (GARCH)")
    ax.plot(-2 * np.sqrt(s2), color=HOT, lw=1.8)
    ax.set_title("GARCH: volatility clustering")
    ax.set_xlabel("time"); ax.set_ylabel("return")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "garch-volatility")


def spectral_analysis() -> None:
    """Spectral analysis decomposes a series into frequencies: the periodogram of a
    signal built from two sine waves shows sharp peaks at exactly those frequencies,
    revealing hidden periodicities buried in noise. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 400
    t = np.arange(n)
    sig = np.sin(2 * np.pi * t / 20) + 0.6 * np.sin(2 * np.pi * t / 7) + rng.normal(0, 0.5, n)
    freqs = np.fft.rfftfreq(n)
    power = np.abs(np.fft.rfft(sig - sig.mean())) ** 2 / n

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.8, 3.9))
    ax1.plot(sig, color=C, lw=0.9); ax1.set_title("signal (two periods + noise)")
    ax1.set_xlabel("time")
    ax2.plot(freqs, power, color=HOT, lw=1.6)
    for p in (20, 7):
        ax2.axvline(1 / p, color=FG_MUTE, ls=":", lw=1.2)
    ax2.set_title("periodogram"); ax2.set_xlabel("frequency"); ax2.set_ylabel("power")
    fig.tight_layout()
    save(fig, SUB, "spectral-analysis")


def state_space_kalman() -> None:
    """A local-level state-space model treats the series as a slowly drifting level
    plus noise; the Kalman filter recovers that latent level, smoothing the
    observations while adapting to genuine shifts. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 120
    level = np.cumsum(rng.normal(0, 0.3, n)) + 5
    y = level + rng.normal(0, 1.5, n)
    R, Q = 1.5**2, 0.3**2
    xhat = np.zeros(n); P = np.zeros(n); xhat[0], P[0] = y[0], 1
    for t in range(1, n):
        Pp = P[t - 1] + Q
        K = Pp / (Pp + R)
        xhat[t] = xhat[t - 1] + K * (y[t] - xhat[t - 1]); P[t] = (1 - K) * Pp

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.scatter(range(n), y, s=12, color=FG_MUTE, alpha=0.6, label="observations")
    ax.plot(level, color=GOOD, lw=2.0, label="true level")
    ax.plot(xhat, color=C, lw=2.2, label="Kalman level estimate")
    ax.set_title("Local-level model: Kalman-filtered trend")
    ax.set_xlabel("time"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "state-space-kalman")


def unit_root_tests() -> None:
    """A unit root means shocks never fade: a random walk wanders without returning
    to any mean, while a stationary AR series mean-reverts. Unit-root tests (ADF,
    KPSS) formalize this difference — the basis for deciding whether to difference.
    rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 200
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for i in range(4):
        ax.plot(np.cumsum(rng.normal(size=n)), color=HOT, lw=0.9, alpha=0.6)
    for i in range(4):
        e = rng.normal(size=n); s = np.zeros(n)
        for t in range(1, n):
            s[t] = 0.5 * s[t - 1] + e[t]
        ax.plot(s, color=C, lw=0.9, alpha=0.8)
    ax.axhline(0, color=FG_MUTE, ls="--", lw=1.0)
    ax.plot([], [], color=HOT, label="random walk (unit root)")
    ax.plot([], [], color=C, label="stationary AR(0.5)")
    ax.set_title("Unit root: wandering vs mean-reverting")
    ax.set_xlabel("time"); ax.set_ylabel("value")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    save(fig, SUB, "unit-root-tests")


def var_cointegration() -> None:
    """Two cointegrated series share a common stochastic trend, so although each
    wanders on its own, a linear combination (their spread) is stationary and
    mean-reverting — the statistical basis of pairs trading. rng(0)."""
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(0)
    n = 300
    common = np.cumsum(rng.normal(size=n))
    x = common + rng.normal(0, 0.5, n)
    y = 0.8 * common + rng.normal(0, 0.5, n)
    spread = x - (1 / 0.8) * y

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 4.8), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})
    ax1.plot(x, color=C, lw=1.2, label="series X")
    ax1.plot(y, color=HOT, lw=1.2, label="series Y")
    ax1.set_title("Cointegrated series move together")
    ax1.legend(loc="upper left", fontsize=8)
    ax2.plot(spread, color=GOOD, lw=1.0)
    ax2.axhline(spread.mean(), color=FG_MUTE, ls="--", lw=1.0)
    ax2.set_title("spread is stationary")
    ax2.set_xlabel("time")
    fig.tight_layout()
    save(fig, SUB, "var-cointegration")


def main() -> None:
    apply_style()
    stationarity_acf()
    ar_ma_processes()
    arima_sarima()
    exponential_smoothing()
    garch_volatility()
    spectral_analysis()
    state_space_kalman()
    unit_root_tests()
    var_cointegration()


if __name__ == "__main__":
    main()
