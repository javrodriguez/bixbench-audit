#!/usr/bin/env python3
"""bix-30-q5 (E5b). Readings named from the question's words before any run and before the key was read; unit: count.

Data: the capsule's one sheet of qPCR Ct values (175 miRNAs; samples P_1..P_10 patients, C_11..C_20 controls).
Needs xlrd (the .xls format): runs in the E5b Python environment (envlock/e5b-py-lock.txt).
  N, the values tested: N1 raw Ct; N2 delta-Ct against each sample's mean Ct over all miRNAs (global-mean
     normalisation, a standard choice for qPCR miRNA panels without a named reference); N3 2^-Ct and N4 2^-delta-Ct
     (relative quantities on a linear scale; E5B-CHANGES-1, pre-run review MINOR 12).
  T, the test (none is named), two-sided, per miRNA: T1 Student's t; T2 Welch's t; T3 Mann-Whitney U.
  The three corrections, as the words name them, over all 175 tests (m = 175): Benjamini-Hochberg,
  Benjamini-Yekutieli (c(m) = sum 1/i), Bonferroni (min(1, m p)); a miRNA counts when its adjusted p <= 0.05
  under all three.
  A miRNA whose p-value is not finite counts as not significant; the number of such miRNAs is reported.
  H, missing Ct values (22 blank cells; found when run 1 stopped on its finiteness assert before any value was
     computed, E5B-CHANGES-2): H1 left out of that miRNA's test (and of the sample's global mean); H2 set to Ct 40,
     the conventional cycle limit for an undetected target; H3 miRNAs with any missing value left out, so the
     corrections run over the remaining miRNAs.
Usage: bix-30-q5.py <data_root>
"""
import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

f = glob.glob(str(Path(sys.argv[1]) / "bix-30" / "CapsuleData-*" / "*.xls"))
assert len(f) == 1, f
raw = pd.read_excel(f[0], header=None)
hdr = raw.iloc[1].tolist()
x = raw.iloc[2:].copy()
x.columns = ["mirna"] + [str(h) for h in hdr[1:]]
x = x.dropna(subset=["mirna"]).set_index("mirna").astype(float)
P = [c for c in x.columns if c.startswith("P_")]
C = [c for c in x.columns if c.startswith("C_")]
assert len(P) == 10 and len(C) == 10 and len(x) == 175 and x.index.is_unique, (len(P), len(C), len(x))
n_missing = int(x.isna().to_numpy().sum())
assert np.isfinite(x.to_numpy()[~x.isna().to_numpy()]).all()


def bh(p: np.ndarray, c: float = 1.0) -> np.ndarray:
    m = len(p)
    o = np.argsort(p, kind="mergesort")
    q = p[o] * m * c / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(m)
    out[o] = np.minimum(q, 1.0)
    return out


variants = {"H1": x, "H2": x.fillna(40.0), "H3": x.dropna(axis=0, how="any")}
tests = {
    "T1": lambda a, b: stats.ttest_ind(a, b, equal_var=True).pvalue,
    "T2": lambda a, b: stats.ttest_ind(a, b, equal_var=False).pvalue,
    "T3": lambda a, b: stats.mannwhitneyu(a, b, alternative="two-sided").pvalue,
}
out = {}
for hk, xh in variants.items():
  dct = xh.sub(xh.mean(axis=0, skipna=True), axis=1)
  norm = {"N1": xh, "N2": dct, "N3": np.power(2.0, -xh), "N4": np.power(2.0, -dct)}
  for nk, t in norm.items():
    for tk, test in tests.items():
        def vals(g, cols):
            v = t.loc[g, cols].to_numpy(dtype=float)
            return v[np.isfinite(v)]
        p = np.array([float(test(vals(g, P), vals(g, C))) for g in t.index])
        bad = ~np.isfinite(p)
        pp = np.where(bad, 1.0, p)
        m = len(pp)
        adj = {"BH": bh(pp), "BY": bh(pp, float(np.sum(1.0 / np.arange(1, m + 1)))), "BONF": np.minimum(pp * m, 1.0)}
        sig = {k: (v <= 0.05) & ~bad for k, v in adj.items()}
        allthree = sig["BH"] & sig["BY"] & sig["BONF"]
        out[f"{hk}-{nk}-{tk}"] = {"value": int(allthree.sum()), "unit": "count", "tests": int(m),
                             "each": {k: int(v.sum()) for k, v in sig.items()}, "raw_p_le_0.05": int(((pp <= 0.05) & ~bad).sum()),
                             "non_finite_p": int(bad.sum()), "defensible": True}
print(json.dumps({"question_id": "bix-30-q5", "readings": out, "meta": {"missing_ct": n_missing}}, sort_keys=True))
