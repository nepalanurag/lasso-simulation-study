# Dashboard data: Lasso Simulation Study

Results from `lasso-simulation-study.Rmd`. The global comparison values are
transcribed from the rendered PDF, the archived output of the completed
analysis.

## Files

- `simulation_settings.json` - the full simulation grid: sample sizes `n`,
  dimensions `p`, signal strengths `A`, correlations `rho`, 100 replications per
  setting, 500-row test sets, AR(1) Toeplitz predictors, 5 true signals.
- `global_comparison.csv` - global averages across all settings for the two
  tuning rules. Columns: `metric`, `lambda_min`, `lambda_1se`. Metrics:
  Sensitivity, False Positive Rate (FPR), Precision, Exact Recovery Rate,
  Test MSE.
- `lasso_simulation_results.csv` - per-setting averaged results (81 settings x
  metrics for both tuning rules). Same file as the repo root copy, included here
  so the dashboard needs no other source. Columns: `n`, `p`, `A`, `rho`,
  `min_sensitivity`, `min_fpr`, `min_precision`, `min_exact_recovery`,
  `min_est_error`, `min_mse`, `lse_sensitivity`, `lse_fpr`, `lse_precision`,
  `lse_exact_recovery`, `lse_est_error`, `lse_mse` (`min_` = lambda.min,
  `lse_` = lambda.1se).

Headline: lambda.min has higher sensitivity (0.701 vs 0.582) but inflated FPR
(0.068 vs 0.020) and low precision; lambda.1se is conservative with near-zero
FPR. Exact recovery collapses as predictor correlation rises.
