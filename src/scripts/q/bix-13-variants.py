#!/usr/bin/env python3
"""bix-13-q1 variant grid (CHANGES-10), rerunning adversarial review 1's attempts to reach the key from the words.
EVERY READING HERE WAS ADDED AFTER THE KEY WAS KNOWN; none enters the rubric. Reads the recorded fit tables.

  D1-D3, M1/M2 as in bix-13-fit.R; L1 MLE, L2 apeglm; F1 and F3 filtering.
  V, where the fold-change cut-off applies and how large it is:
    V1 |log2FC| > log2(1.5) = 0.585 (the cut-off read as a linear fold change) on all three strains;
    V2 |log2FC| > 1.5 on JBX97 only, padj alone for JBX99 and JBX98;
    V3 |log2FC| > 1.5 on JBX97 and JBX99, padj alone for excluding JBX98;
    V4 no cut-off on any strain.
  N: N1 denominator = JBX97's DE set; N2 = the union of the three DE sets.
  value: 100 x |DE97 and DE99, not DE98| / N.
Usage: bix-13-variants.py <fit_dir>
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix13_common import DESIGNS, MODELS, de, table  # noqa: E402

fit = Path(sys.argv[1])
LIN = math.log2(1.5)
out = {}
for d in DESIGNS:
    for m in MODELS:
        t = {s: table(fit, d, m, s) for s in ("97", "98", "99")}
        for lk, col in (("L1", "lfc_mle"), ("L2", "lfc_apeglm")):
            for f in ("F1", "F3"):
                cut = {
                    "V1": {"97": LIN, "98": LIN, "99": LIN},
                    "V2": {"97": 1.5, "98": None, "99": None},
                    "V3": {"97": 1.5, "98": None, "99": 1.5},
                    "V4": {"97": None, "98": None, "99": None},
                }
                for vk, c in cut.items():
                    s = {k: de(v, f, col if c[k] is not None else None, c[k]) for k, v in t.items()}
                    num = (s["97"] & s["99"]) - s["98"]
                    for nk, den in (("N1", s["97"]), ("N2", s["97"] | s["98"] | s["99"])):
                        out[f"{d}-{m}-{lk}-{f}-{vk}-{nk}"] = {
                            "value": 100 * len(num) / len(den), "unit": "percent", "numerator": len(num),
                            "denominator": len(den), "defensible": nk == "N1",
                            "added": "after the key was known (review 1 probes)"}
vals = [v["value"] for v in out.values()]
print(json.dumps({"question_id": "bix-13-q1", "readings": out,
                  "meta": {"variants": len(out), "min": min(vals), "max": max(vals),
                           "rounds_to_10_6": sum(round(v, 1) == 10.6 for v in vals)}}, sort_keys=True))
