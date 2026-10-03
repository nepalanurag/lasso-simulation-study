# Lasso Simulation Study

I ran a simulation study of lasso variable selection across sample sizes (n = 50, 100, 200), dimensions (p = 200, 400, 600), signal strengths, and predictor correlations (rho = 0, 0.5, 0.8), with 100 replications per setting run in parallel.

I compared the minimum-lambda and 1se-lambda tuning rules on sensitivity, false positive rate, precision, exact recovery, and estimation error. Lasso recovers the true variables reliably when signals are strong and predictors are independent, but exact recovery breaks down under high correlation. One practical takeaway: in high dimensions, raw false positive rates can look artificially low because the denominator keeps growing, so the choice of metric matters.

## Files

- `lasso-simulation-study.Rmd` - the simulation code and writeup
- `lasso-simulation-study.pdf` / `lasso-simulation-study.docx` - rendered versions
- `lasso_simulation_results.csv` - results across all settings
- `avg_plot_*.png` - averaged performance plots
