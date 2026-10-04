"""Real-data companion to the lasso simulation study.

The simulation asked: min-lambda vs 1se-lambda tuning, which selects better?
Here the same question goes to real data: the sklearn diabetes set
(442 patients, 10 baseline predictors, disease progression target).

For each tuning rule I bootstrap the data 200 times and record which
predictors get selected, measuring selection stability directly.

Outputs land in the repo: figures in ../docs/figs/, metrics in metrics.json.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoCV, lasso_path

HERE = Path(__file__).resolve().parent          # analysis/
REPO = HERE.parent                              # repo root
FIGS = REPO / "docs" / "figs"
FIGS.mkdir(parents=True, exist_ok=True)

SEED = 42
rng = np.random.default_rng(SEED)
X, y = load_diabetes(return_X_y=True)
names = load_diabetes().feature_names
X = StandardScaler().fit_transform(X)
n, p = X.shape

cv = LassoCV(cv=10, random_state=SEED, max_iter=10000).fit(X, y)
a_min = cv.alpha_
# 1se rule: largest alpha whose mean CV MSE is within one SE of the minimum
mse_mean = cv.mse_path_.mean(axis=1)
mse_se = cv.mse_path_.std(axis=1) / np.sqrt(cv.mse_path_.shape[1])
cutoff = mse_mean.min() + mse_se[mse_mean.argmin()]
a_1se = cv.alphas_[mse_mean <= cutoff].max()
sel_min = (np.abs(cv.coef_) > 1e-10)

from sklearn.linear_model import Lasso
sel_1se = (np.abs(Lasso(alpha=a_1se, max_iter=10000).fit(X, y).coef_) > 1e-10)

# Bootstrap selection stability
B = 200
freq_min = np.zeros(p)
freq_1se = np.zeros(p)
for b in range(B):
    idx = rng.integers(0, n, n)
    Xb, yb = X[idx], y[idx]
    freq_min += (np.abs(Lasso(alpha=a_min, max_iter=10000).fit(Xb, yb).coef_) > 1e-10)
    freq_1se += (np.abs(Lasso(alpha=a_1se, max_iter=10000).fit(Xb, yb).coef_) > 1e-10)
freq_min /= B
freq_1se /= B

out = {"n": n, "p": p, "seed": SEED, "bootstraps": B,
       "alpha_min": float(a_min), "alpha_1se": float(a_1se),
       "selected_min": [names[i] for i in np.where(sel_min)[0]],
       "selected_1se": [names[i] for i in np.where(sel_1se)[0]],
       "selection_freq_min": {names[i]: float(freq_min[i]) for i in range(p)},
       "selection_freq_1se": {names[i]: float(freq_1se[i]) for i in range(p)},
       "mean_freq_min": float(freq_min.mean()), "mean_freq_1se": float(freq_1se.mean())}

# Figure 1: coefficient paths with the two chosen lambdas marked
alphas, coefs, _ = lasso_path(X, y, n_alphas=100)
fig, ax = plt.subplots(figsize=(8, 5))
for j in range(p):
    ax.plot(alphas, coefs[j], label=names[j], linewidth=1.5)
ax.axvline(a_min, color="k", linestyle="--", label=f"lambda.min = {a_min:.3f}")
ax.axvline(a_1se, color="k", linestyle=":", label=f"lambda.1se = {a_1se:.3f}")
ax.set_xscale("log")
ax.set_xlabel("lambda")
ax.set_ylabel("coefficient")
ax.set_title("Lasso coefficient paths (diabetes data, standardized)")
ax.legend(fontsize=8, ncol=2)
fig.tight_layout()
fig.savefig(FIGS / "lasso_paths.png", dpi=110)
plt.close(fig)

# Figure 2: bootstrap selection frequency per rule
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(p)
w = 0.35
ax.bar(x - w / 2, freq_min, w, label="lambda.min")
ax.bar(x + w / 2, freq_1se, w, label="lambda.1se")
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=30, ha="right", fontsize=9)
ax.set_ylabel("fraction of 200 bootstraps selected")
ax.set_title("Selection stability across 200 bootstraps: min vs 1se rule")
ax.legend()
fig.tight_layout()
fig.savefig(FIGS / "lasso_stability.png", dpi=110)
plt.close(fig)

with open(HERE / "metrics.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps({k: v for k, v in out.items() if k not in ("selection_freq_min", "selection_freq_1se")}, indent=2))
