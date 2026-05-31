import type { Lesson } from "@/lib/types";

/**
 * Pillar G: Time Series & Forecasting. Ordered lesson curriculum per
 * subsection. Lesson order is the array order; prerequisites are bare ids
 * within the same subsection or "subId/lessonId" across subsections.
 */
export const G_CURRICULUM: Record<string, Lesson[]> = {
  G1: [
    {
      id: "stationarity-acf",
      title: "Stationarity, autocovariance, and the ACF/PACF",
      goal: "Define weak stationarity, derive the autocovariance and autocorrelation functions, and read AR/MA order off the ACF and partial ACF.",
      prerequisites: ["A2/expectation", "A2/variance-moments"],
    },
    {
      id: "unit-root-tests",
      title: "Unit roots: the ADF and KPSS tests",
      goal: "Explain why a unit root breaks stationarity, set up the augmented Dickey-Fuller regression, and combine ADF with KPSS to classify a series.",
      prerequisites: ["stationarity-acf", "B1/hypothesis-testing"],
    },
    {
      id: "ar-ma-processes",
      title: "AR and MA processes",
      goal: "Write the AR(p) and MA(q) recursions, derive their autocovariance structure, and state the stationarity and invertibility conditions in terms of the characteristic roots.",
      prerequisites: ["stationarity-acf"],
    },
    {
      id: "arima-sarima",
      title: "ARIMA and seasonal SARIMA",
      goal: "Combine differencing with ARMA to model integrated series, extend to seasonal SARIMA, and choose orders by information criteria.",
      prerequisites: ["ar-ma-processes", "unit-root-tests"],
    },
    {
      id: "exponential-smoothing",
      title: "Exponential smoothing and the ETS family",
      goal: "Derive simple, Holt, and Holt-Winters smoothing as recursive weighted averages, and place them in the state-space ETS taxonomy.",
      prerequisites: ["stationarity-acf"],
    },
    {
      id: "state-space-kalman",
      title: "State-space form and Kalman filtering for time series",
      goal: "Cast ARIMA and ETS models in state-space form and run the Kalman filter to obtain the exact Gaussian likelihood for parameter estimation.",
      prerequisites: ["arima-sarima", "F3/kalman-filter"],
    },
    {
      id: "var-cointegration",
      title: "VAR, cointegration, and the VECM",
      goal: "Extend AR to a vector autoregression, define cointegration between integrated series, and write the error-correction (VECM) representation.",
      prerequisites: ["ar-ma-processes", "A1/eigenvalues"],
    },
    {
      id: "garch-volatility",
      title: "GARCH models for volatility",
      goal: "Model time-varying conditional variance with ARCH and GARCH, derive the unconditional variance, and explain volatility clustering.",
      prerequisites: ["ar-ma-processes"],
    },
    {
      id: "spectral-analysis",
      title: "Spectral analysis: the periodogram and wavelets",
      goal: "Define the spectral density as the Fourier transform of the autocovariance, estimate it with the periodogram, and contrast Fourier with wavelet resolution.",
      prerequisites: ["stationarity-acf", "A1/inner-products"],
    },
  ],
  G2: [
    {
      id: "ts-feature-engineering",
      title: "Feature engineering: lags, rolling stats, and Fourier terms",
      goal: "Turn a forecasting problem into a supervised table with lag, rolling-window, and Fourier-seasonality features without leaking future information.",
      prerequisites: ["G1/stationarity-acf"],
    },
    {
      id: "gbdt-forecasting",
      title: "Gradient-boosted trees for forecasting",
      goal: "Forecast with gradient-boosted trees on engineered features, and contrast the recursive and direct multi-step strategies.",
      prerequisites: ["ts-feature-engineering", "C3/xgboost-lightgbm"],
    },
    {
      id: "hierarchical-forecasting",
      title: "Hierarchical and grouped forecasting",
      goal: "Define a hierarchy of series, state the coherence constraint, and reconcile base forecasts with bottom-up and the optimal MinT projection.",
      prerequisites: ["gbdt-forecasting", "A1/least-squares"],
    },
    {
      id: "prophet",
      title: "Prophet: a decomposable additive model",
      goal: "Decompose a series into piecewise-linear trend, Fourier seasonality, and holiday effects, and fit it as a regression with changepoint regularization.",
      prerequisites: ["ts-feature-engineering", "C1/linear-regression-mle"],
    },
  ],
  G3: [
    {
      id: "deepar",
      title: "DeepAR: autoregressive probabilistic RNN forecasting",
      goal: "Define DeepAR as an RNN that emits the parameters of a likelihood, derive its training loss, and sample multi-step probabilistic forecasts.",
      prerequisites: ["G2/ts-feature-engineering", "D3/lstm-gru", "A2/mle"],
    },
    {
      id: "nbeats-nhits",
      title: "N-BEATS and N-HiTS: basis expansion forecasting",
      goal: "Build the doubly-residual block stack of N-BEATS, express trend and seasonality as basis projections, and explain the multi-rate pooling of N-HiTS.",
      prerequisites: ["G1/spectral-analysis", "D1/mlp-forward"],
    },
    {
      id: "temporal-fusion-transformer",
      title: "The Temporal Fusion Transformer",
      goal: "Assemble the TFT from variable selection, gated residual networks, and interpretable attention, and train it with the quantile (pinball) loss.",
      prerequisites: ["deepar", "E3/transformer-block"],
    },
    {
      id: "decomposition-transformers",
      title: "Informer, Autoformer, and FEDformer",
      goal: "Trace the long-horizon line of transformers: ProbSparse attention in Informer, series decomposition and auto-correlation in Autoformer, frequency mixing in FEDformer.",
      prerequisites: ["temporal-fusion-transformer", "G1/spectral-analysis"],
    },
    {
      id: "patchtst-itransformer",
      title: "PatchTST and iTransformer",
      goal: "Patch a series into subseries tokens with channel independence (PatchTST), then invert the attention axis to treat each variate as a token (iTransformer).",
      prerequisites: ["decomposition-transformers"],
    },
    {
      id: "ts-foundation-models",
      title: "Time-series foundation models",
      goal: "Explain zero-shot forecasting with pretrained models: Chronos value tokenization, TimeGPT, and Lag-Llama, and the scaling that makes them transfer.",
      prerequisites: ["patchtst-itransformer", "E3/decoder-only"],
    },
  ],
  G4: [
    {
      id: "statistical-anomaly-detection",
      title: "Statistical anomaly detection: IQR, z-score, and ESD",
      goal: "Flag point anomalies with the IQR rule and the robust z-score, and apply the generalized ESD test for multiple outliers under normality.",
      prerequisites: ["G1/stationarity-acf", "B1/hypothesis-testing"],
    },
    {
      id: "cusum-changepoint",
      title: "CUSUM and change-point detection",
      goal: "Derive the CUSUM statistic as a sequential likelihood-ratio accumulator and use it to detect a shift in mean online.",
      prerequisites: ["statistical-anomaly-detection"],
    },
    {
      id: "deep-anomaly-detection",
      title: "Deep anomaly detection with autoencoders",
      goal: "Score anomalies by reconstruction error from a sequence autoencoder, set a threshold from the residual distribution, and explain the LSTM-AE and transformer-AE variants.",
      prerequisites: ["cusum-changepoint", "D4/autoencoders"],
    },
  ],
  G5: [
    {
      id: "granger-causality",
      title: "Granger causality",
      goal: "Define Granger causality as predictive improvement, test it with a restricted-versus-full VAR F-test, and state what it does and does not claim.",
      prerequisites: ["G1/var-cointegration", "B5/potential-outcomes"],
    },
    {
      id: "causalimpact-bsts",
      title: "CausalImpact and Bayesian structural time series",
      goal: "Estimate an intervention effect by forecasting the counterfactual with a Bayesian structural time-series model fit on a control series.",
      prerequisites: [
        "granger-causality",
        "G1/state-space-kalman",
        "B5/diff-in-diff",
      ],
    },
    {
      id: "synthetic-control",
      title: "Synthetic control for time series",
      goal: "Construct a synthetic control as a convex combination of donor units matched on pre-treatment outcomes, and read the treatment effect as the post-period gap.",
      prerequisites: ["causalimpact-bsts", "A1/least-squares"],
    },
  ],
};
