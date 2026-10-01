#!/usr/bin/env python3
"""bix-13-q1 (recorded-run version, replaces bix-13-q1.R; CHANGES-4). Unit: percent.

Readings named before the pilot (pilot run 1 used bix-13-q1.R with the same D, M, L, F readings):
  D, M, F as in bix-13-fit.R; L1 MLE log2 fold change, L2 apeglm-shrunk; C1 |log2 fold change| > 1.5.
  N1 denominator: genes DE in JBX97 (the question's own words).
Added after pilot run 1 (CHANGES-4), marked in each reading's "added" field:
  C2 the cut-off read as a natural-log fold change, |ln fold change| > 1.5 (|log2| > 2.164).
  N2 denominator: every gene DE in JBX97, JBX98 or JBX99 (the union). Not a defensible reading of the words;
     recorded as a candidate origin of the key.
Numerator: DE in JBX97 and in JBX99 and not in JBX98. padj < 0.05 throughout.
Usage: bix-13-q1.py <fit_dir>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix13_common import DESIGNS, FILTERS, LN_CUTOFF, MODELS, de, table  # noqa: E402

fit = Path(sys.argv[1])
out = {}
for d in DESIGNS:
    for m in MODELS:
        t = {s: table(fit, d, m, s) for s in ("97", "98", "99")}
        for lk, col in (("L1", "lfc_mle"), ("L2", "lfc_apeglm")):
            for ck, cut in (("C1", 1.5), ("C2", LN_CUTOFF)):
                for f in FILTERS:
                    s = {k: de(v, f, col, cut) for k, v in t.items()}
                    num = (s["97"] & s["99"]) - s["98"]
                    for nk, den in (("N1", s["97"]), ("N2", s["97"] | s["98"] | s["99"])):
                        assert len(den) > 0
                        out[f"{d}-{m}-{lk}-{ck}-{f}-{nk}"] = {
                            "value": 100 * len(num) / len(den), "unit": "percent", "numerator": len(num),
                            "denominator": len(den), "n_de": {k: len(v) for k, v in s.items()},
                            "defensible": nk == "N1",
                            "added": "after pilot run 1" if (ck == "C2" or nk == "N2") else "before pilot",
                        }
print(json.dumps({"question_id": "bix-13-q1", "readings": out}, sort_keys=True))
