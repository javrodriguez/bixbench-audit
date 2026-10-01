#!/usr/bin/env python3
"""bix-36-q1, version 2 (CHANGES-5). Unit: F statistic.

Pre-registered readings (identical to the pilot's bix-36-q1.py, which ran in pilot run 1): S1-S3, T1-T2, E1-E2 on
counts as given (Z1).
Added after pilot run 1 (review of the recorded-run code, CHANGES-5): Z2 counts per million, Z3 median-of-ratios
size factors (bix36_common.py), each crossed with S, T and E; marked "added after pilot run 1".
  S, one observation: S1 a sample's mean over miRNA genes; S2 each gene x sample value; S3 a gene's mean within
     one cell type. T: T1 as given; T2 log2(value + 1). E: E1 all miRNA genes; E2 non-zero total over kept samples.
  statistic: one-way ANOVA F across CD4, CD8, CD14, CD19 (PBMC excluded).
Usage: bix-36-q1-v2.py <data_root>
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix36_common import load  # noqa: E402

TYPES = ["CD4", "CD8", "CD14", "CD19"]
norm, ann, meta = load(Path(sys.argv[1]), lambda a: a[a["celltype"].isin(TYPES)])
out = {}
for zk, x in norm.items():
    for ek in ("E1", "E2"):
        xe = x if ek == "E1" else x[x.sum(axis=1) > 0]
        for tk in ("T1", "T2"):
            xt = xe if tk == "T1" else np.log2(xe + 1)
            by = {t: xt[ann.loc[ann["celltype"] == t, "sample"]] for t in TYPES}
            obs = {
                "S1": [by[t].mean(axis=0).to_numpy() for t in TYPES],
                "S2": [by[t].to_numpy().ravel() for t in TYPES],
                "S3": [by[t].mean(axis=1).to_numpy() for t in TYPES],
            }
            for sk, groups in obs.items():
                r = stats.f_oneway(*groups)
                f = float(r.statistic)
                key = f"{sk}-{tk}-{ek}" if zk == "Z1" else f"{zk}-{sk}-{tk}-{ek}"
                out[key] = {"value": f if math.isfinite(f) else None, "unit": "F", "p": float(r.pvalue),
                            "n": [int(len(g)) for g in groups], "defensible": True,
                            "added": "before pilot" if zk == "Z1" else "after pilot run 1"}
print(json.dumps({"question_id": "bix-36-q1", "readings": out, "meta": meta}, sort_keys=True))
