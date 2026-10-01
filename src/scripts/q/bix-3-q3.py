#!/usr/bin/env python3
"""bix-3-q3. Readings named before its first run (CHANGES-4); unit: count.

  Cohort A1 (Control samples only, as the words say); M1/M2, P1/P2, F1-F3 and FT as in bix-3-fit.R
  (FT, the thresholded test, added by CHANGES-5 before any bix-3 value existed).
  DE in a comparison: padj < 0.05 and |MLE log2 fold change| > 1 (the words' cut-offs).
  value: genes DE for dentate gyrus vs baseline blood, and DE in neither dentate gyrus vs final blood
  nor final blood vs baseline blood.
Usage: bix-3-q3.py <fit_dir>
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
        t = {c: table(fit, "A1", m, p, c) for c in ("DG_BB", "DG_FB", "FB_BB")}
        for f in FILTERS_T:
            s = {c: de(v, f, lfc=1) for c, v in t.items()}
            out[f"{m}-{p}-{f}"] = {"value": len(s["DG_BB"] - s["DG_FB"] - s["FB_BB"]), "unit": "count",
                                   "n_de": {c: len(v) for c, v in s.items()}, "defensible": True}
print(json.dumps({"question_id": "bix-3-q3", "readings": out}, sort_keys=True))
