#!/usr/bin/env python3
"""bix-3-q1, q2, q3 under pseudo-count reading P3 (CHANGES-8). Every reading here is marked
"added after recorded run 1 and the notebook"; none enters the rubric. Defensibility of P3 is Javier's ruling.

Same readings as bix-3-q1.py, bix-3-q2.py and bix-3-q3.py, with P3 in place of P1/P2. bix-3-q3 also gets a
non-defensible reading B10 (baseMean >= 10 added, which its words do not state; the notebook's cell 41 applies it),
recorded as evidence of the key's origin only.
Prints three JSON lines, one per question. Usage: bix-3-p3.py <fit_dir>
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix3_common import FILTERS, FILTERS_T, MODELS, de, table  # noqa: E402

Z = 1.959963984540054
ADDED = "after recorded run 1 and the notebook"
fit = Path(sys.argv[1])


def wilson(k: int, n: int) -> tuple[float, float, float]:
    p = k / n
    den = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / den
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return p, centre - half, centre + half


q1 = {}
for m in MODELS:
    t = table(fit, "A1", m, "P3", "FB_BB")
    for f in FILTERS_T:
        q1[f"{m}-P3-{f}"] = {"value": len(de(t, f, lfc=1, base_min=10)), "unit": "count", "defensible": True,
                             "added": ADDED}
print(json.dumps({"question_id": "bix-3-q1", "readings": q1}, sort_keys=True))

q2 = {}
for a, m in (("A1", "M1"), ("A1", "M2"), ("A2", "M1")):
    t = table(fit, a, m, "P3", "FB_BB")
    for f in FILTERS:
        dens = {"N1": int(t[f"padj_{f}"].notna().sum()), "N2": int(len(t)), "N3": int((t["baseMean"] > 0).sum()),
                "N4": int((t["baseMean"] >= 10).sum())}
        for ek, kw in (("E1", {}), ("E2", {"lfc": 1}), ("E3", {"lfc": 1, "base_min": 10})):
            k = len(de(t, f, **kw))
            for nk, n in dens.items():
                if nk == "N4" and ek != "E3":
                    continue
                pt, lo, hi = wilson(k, n)
                for sk, v in (("lo", lo), ("hi", hi), ("pt", pt)):
                    q2[f"{a}-{m}-P3-{f}-{ek}-{nk}-{sk}"] = {"value": v, "unit": "fraction", "k": k, "n": n,
                                                            "defensible": True, "added": ADDED}
print(json.dumps({"question_id": "bix-3-q2", "readings": q2}, sort_keys=True))

q3 = {}
for m in MODELS:
    t = {c: table(fit, "A1", m, "P3", c) for c in ("DG_BB", "DG_FB", "FB_BB")}
    for f in FILTERS_T:
        for bk, base in (("B0", None), ("B10", 10)):
            s = {c: de(v, f, lfc=1, base_min=base) for c, v in t.items()}
            q3[f"{m}-P3-{f}-{bk}"] = {"value": len(s["DG_BB"] - s["DG_FB"] - s["FB_BB"]), "unit": "count",
                                      "n_de": {c: len(v) for c, v in s.items()}, "defensible": bk == "B0",
                                      "added": ADDED}
print(json.dumps({"question_id": "bix-3-q3", "readings": q3}, sort_keys=True))
