#!/usr/bin/env python3
"""bix-3-q4 probe (E5B-CHANGES-3; written after the key and the reference notebook were read).

The notebook (cells 29, 33-41, 49-50) scales each gene's row of the NormCount sheet to sum to a million (the
per-gene scaling E5a reported as a separate defect, CHANGES-9), fits pydeseq2 on the Control mice (~ Tissue), and
counts genes with padj < 0.05, |log2 fold change| > 1 and baseMean >= 10 in all three comparisons: 429.
This probe adds the notebook's baseMean >= 10 to the pre-registered E2 criterion on the recorded fit tables
(reading E2b, "added after key"), for every cohort, fit, input and filtering choice, intersection only.
Usage: bix-3-q4-probe.py <fit_dir>
"""
import json
import sys
from pathlib import Path

import pandas as pd

fit = Path(sys.argv[1])
out = {}
for a in ("A1", "A2", "A3", "A4"):
    for m in (("M1", "M2") if a in ("A1", "A2") else ("M1",)):
        for p in ("P1", "P2"):
            tabs = [pd.read_csv(fit / f"bix-3q4_{a}_{m}_{p}_{c}.csv", na_values=["NA"], keep_default_na=False,
                                float_precision="round_trip").set_index("gene") for c in ("FB_BB", "DG_BB", "DG_FB")]
            for f in ("F1", "F2", "F3"):
                sets = [set(t.index[t[f"padj_{f}"].notna() & (t[f"padj_{f}"] < 0.05) & (t["lfc_mle"].abs() > 1)
                                    & (t["baseMean"] >= 10)]) for t in tabs]
                out[f"{a}-{m}-{p}-{f}-E2b-C1"] = {"value": len(set.intersection(*sets)), "unit": "count",
                                                  "per_comparison": [len(s) for s in sets], "added": "after key",
                                                  "defensible": "Javier to rule"}
print(json.dumps({"question_id": "bix-3-q4", "origin": True, "readings": out}, sort_keys=True))
