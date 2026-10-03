#!/usr/bin/env python3
"""bix-36-q5 origin labels (E5B-CHANGES-4; after the key and the notebook were read).

Reads bix-36-q5-origin-fit.R's table; pools the six comparison columns (MLE or apeglm, natural log), and also each
column alone; applies the pre-registered label conventions of bix-36-q5.py (L1 Bulmer symmetry, L2 D'Agostino-
Pearson K2 at 0.05, L3 kurtosis test, L4 kernel-density modes), restated here verbatim; non-finite values dropped.
Usage: bix-36-q5-origin.py <lfc_csv>
"""
import json
import sys

import numpy as np
import pandas as pd
from scipy import stats

t = pd.read_csv(sys.argv[1], na_values=["NA"], keep_default_na=False, float_precision="round_trip")


def modes(v):
    lo, hi = np.percentile(v, [0.5, 99.5])
    h, edges = np.histogram(v, bins=2048, range=(lo, hi))
    width = edges[1] - edges[0]
    bw = float(np.std(v, ddof=1)) * len(v) ** (-1 / 5)
    half = int(np.ceil(4 * bw / width))
    k = np.exp(-0.5 * ((np.arange(-half, half + 1) * width) / bw) ** 2)
    dens = np.convolve(h, k, mode="same")
    peak = (dens[1:-1] > dens[:-2]) & (dens[1:-1] >= dens[2:]) & (dens[1:-1] > 0.1 * dens.max())
    n = int(peak.sum())
    return "unimodal" if n <= 1 else ("bimodal" if n == 2 else "multimodal")


def labels(v):
    v = v[np.isfinite(v)]
    g1, ex = float(stats.skew(v)), float(stats.kurtosis(v))
    side = "right" if g1 > 0 else "left"
    l1 = "approximately symmetric" if abs(g1) < 0.5 else (f"moderately {side}-skewed" if abs(g1) <= 1 else f"highly {side}-skewed")
    k2p, ktp = float(stats.normaltest(v).pvalue), float(stats.kurtosistest(v).pvalue)
    l3 = "mesokurtic" if ktp >= 0.05 else ("leptokurtic" if ex > 0 else "platykurtic")
    return {"L1": l1, "L2": "normal" if k2p >= 0.05 else "not normal", "L3": l3, "L4": modes(v),
            "n": int(len(v)), "skewness": g1, "excess_kurtosis": ex, "normaltest_p": k2p,
            "shapiro_p_first_5000": float(stats.shapiro(v[:5000]).pvalue)}


out = {}
for est in ("mle", "ape"):
    cols = [c for c in t.columns if c.startswith(est + "_")]
    out[f"origin-{est}-pooled"] = labels(t[cols].to_numpy(dtype=float).ravel())
    for c in cols:
        out[f"origin-{c}"] = labels(t[c].to_numpy(dtype=float))
print(json.dumps({"question_id": "bix-36-q5", "origin": True, "readings": out, "meta": {"genes": int(len(t))}},
                 sort_keys=True))
