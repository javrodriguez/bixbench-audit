#!/usr/bin/env python3
"""bix-3-q1 (recorded-run version, replaces bix-3-q1.R, which never produced a value; CHANGES-4). Unit: count.

Readings: cohort A1 (Control mice, design ~ Tissue, as the words say); M1/M2, P1/P2, F1-F3 and FT as in bix-3-fit.R
(FT, the thresholded test, added by CHANGES-5 before any bix-3 value existed).
The M reading (whether dentate-gyrus samples share the fit) is added before any bix-3 value was produced.
value: genes with padj < 0.05, |MLE log2 fold change| > 1 and baseMean >= 10, final vs baseline blood.
Usage: bix-3-q1.py <fit_dir>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix3_common import FILTERS_T, MODELS, PSEUDO, de, table  # noqa: E402

fit = Path(sys.argv[1])
out = {}
for m in MODELS:
    for p in PSEUDO:
        t = table(fit, "A1", m, p, "FB_BB")
        for f in FILTERS_T:
            out[f"{m}-{p}-{f}"] = {"value": len(de(t, f, lfc=1, base_min=10)), "unit": "count", "defensible": True}
print(json.dumps({"question_id": "bix-3-q1", "readings": out}, sort_keys=True))
