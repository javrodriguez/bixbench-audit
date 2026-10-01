#!/usr/bin/env python3
"""bix-3-q2. Readings named before its first run (CHANGES-4, extended by CHANGES-5); unit: fraction.

The question asks for a 95% Wilson interval (two numbers) and the key is one range, so the target itself is a
reading: -lo the interval's lower bound, -hi its upper bound, -pt the point proportion.
  A, cohort and M, fit: A1-M1 Control mice, all three tissues fitted (~ Tissue); A1-M2 Control mice, the two blood
     tissues only; A2-M1 all mice (~ Response + Tissue).
  P1/P2 pseudo-counts and F1-F3 filtering as in bix-3-fit.R.
  E, "differentially expressed": E1 padj < 0.05; E2 padj < 0.05 and |MLE log2 fold change| > 1;
     E3 bix-3-q1's criterion: padj < 0.05, |MLE log2 fold change| > 1 and baseMean >= 10.
  N, the denominator: N1 genes with a padj (tested); N2 every gene in the table; N3 genes with baseMean > 0;
     N4 genes with baseMean >= 10.
Wilson interval with z = 1.959963984540054 (two-sided 95%).
Usage: bix-3-q2.py <fit_dir>
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix3_common import FILTERS, PSEUDO, de, table  # noqa: E402

Z = 1.959963984540054


def wilson(k: int, n: int) -> tuple[float, float, float]:
    p = k / n
    den = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / den
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return p, centre - half, centre + half


fit = Path(sys.argv[1])
out = {}
for a, m in (("A1", "M1"), ("A1", "M2"), ("A2", "M1")):
    for p in PSEUDO:
        t = table(fit, a, m, p, "FB_BB")
        for f in FILTERS:
            dens = {"N1": int(t[f"padj_{f}"].notna().sum()), "N2": int(len(t)), "N3": int((t["baseMean"] > 0).sum()),
                    "N4": int((t["baseMean"] >= 10).sum())}
            for ek, kw in (("E1", {}), ("E2", {"lfc": 1}), ("E3", {"lfc": 1, "base_min": 10})):
                k = len(de(t, f, **kw))
                for nk, n in dens.items():
                    if nk == "N4" and ek != "E3":
                        continue  # E1/E2 counts can include genes with baseMean < 10, so N4 is not their base
                    assert 0 < n and k <= n
                    pt, lo, hi = wilson(k, n)
                    for sk, v in (("lo", lo), ("hi", hi), ("pt", pt)):
                        out[f"{a}-{m}-{p}-{f}-{ek}-{nk}-{sk}"] = {"value": v, "unit": "fraction", "k": k, "n": n,
                                                                  "defensible": True}
print(json.dumps({"question_id": "bix-3-q2", "readings": out}, sort_keys=True))
