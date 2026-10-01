#!/usr/bin/env python3
"""bix-13-q2. Readings named before its first run (CHANGES-4); unit: count of genes.

  D, M, F as in bix-13-fit.R. The words set no fold-change cut-off, so the reading is padj < 0.05 alone (C0);
  C1 adds |MLE log2 fold change| > 1.5, the cut-off a sibling question uses, as a cross-check (defensible False:
  the words do not state it).
  value: genes DE in JBX98 and DE in neither JBX97 nor JBX99, each against JBX1.
Usage: bix-13-q2.py <fit_dir>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix13_common import DESIGNS, FILTERS, MODELS, de, table  # noqa: E402

fit = Path(sys.argv[1])
out = {}
for d in DESIGNS:
    for m in MODELS:
        t = {s: table(fit, d, m, s) for s in ("97", "98", "99")}
        for ck, col, cut in (("C0", None, None), ("C1", "lfc_mle", 1.5)):
            for f in FILTERS:
                s = {k: de(v, f, col, cut) for k, v in t.items()}
                val = len(s["98"] - s["97"] - s["99"])
                out[f"{d}-{m}-{ck}-{f}"] = {"value": val, "unit": "count", "n_de": {k: len(v) for k, v in s.items()},
                                            "defensible": ck == "C0"}
print(json.dumps({"question_id": "bix-13-q2", "readings": out}, sort_keys=True))
