#!/usr/bin/env python3
"""bix-3-q4 (E5b). Readings named from the question's words before any run and before the key was read; unit: count.

Reads the fit tables written by bix-3-q4-fit.R (cohort A, fit M, integer input P, filtering F; see that file).
  E, "differentially expressed" in one comparison: E1 padj < 0.05; E2 padj < 0.05 and |MLE log2 fold change| > 1;
     E3 padj < 0.1 (DESeq2's default alpha).
  C, "across all comparisons": C1 genes differentially expressed in every one of the three comparisons
     (intersection); C2 genes differentially expressed in at least one (union); C3 the sum of the three
     per-comparison counts (E5B-CHANGES-1, pre-run review MINOR 8).
  Cohorts A1-A4 and fits as in bix-3-q4-fit.R (A3 and A4 have M1 only).
Usage: bix-3-q4.py <fit_dir>
"""
import json
import sys
from pathlib import Path

import pandas as pd

fit = Path(sys.argv[1])
CONTRASTS = ("FB_BB", "DG_BB", "DG_FB")


def table(tag: str, c: str) -> pd.DataFrame:
    t = pd.read_csv(fit / f"bix-3q4_{tag}_{c}.csv", na_values=["NA"], keep_default_na=False,
                    float_precision="round_trip")
    assert t["gene"].is_unique and len(t) > 20000, (tag, c, len(t))
    return t.set_index("gene")


out = {}
for a in ("A1", "A2", "A3", "A4"):
    for m in (("M1", "M2") if a in ("A1", "A2") else ("M1",)):
        for p in ("P1", "P2"):
            tabs = {c: table(f"{a}_{m}_{p}", c) for c in CONTRASTS}
            for f in ("F1", "F2", "F3"):
                for ek in ("E1", "E2", "E3"):
                    sets = []
                    for c in CONTRASTS:
                        t = tabs[c]
                        ok = t[f"padj_{f}"].notna() & (t[f"padj_{f}"] < (0.1 if ek == "E3" else 0.05))
                        if ek == "E2":
                            ok &= t["lfc_mle"].abs() > 1
                        sets.append(set(t.index[ok]))
                    per = [len(s) for s in sets]
                    out[f"{a}-{m}-{p}-{f}-{ek}-C1"] = {"value": len(set.intersection(*sets)), "unit": "count",
                                                       "per_comparison": per, "defensible": True}
                    out[f"{a}-{m}-{p}-{f}-{ek}-C2"] = {"value": len(set.union(*sets)), "unit": "count",
                                                       "per_comparison": per, "defensible": True}
                    out[f"{a}-{m}-{p}-{f}-{ek}-C3"] = {"value": sum(per), "unit": "count",
                                                       "per_comparison": per, "defensible": True}
print(json.dumps({"question_id": "bix-3-q4", "readings": out}, sort_keys=True))
