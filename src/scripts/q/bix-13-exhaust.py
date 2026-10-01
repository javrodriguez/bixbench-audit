#!/usr/bin/env python3
"""bix-13-q1 exhaustive JBX97-denominator search (CHANGES-12): adversarial review 3's probe rerun under the lane's
hashing. EVERY READING HERE WAS ADDED AFTER THE KEY WAS KNOWN; none enters the rubric.
Exhaustive search over the recorded bix-13 fit tables for any reading that keeps the words' denominator
(JBX97's DE set) and lands near 10.6%: D1-D3 x M1/M2 x MLE/apeglm x F1-F3 x threshold
{log2(1.5), 1.5, 1.5/ln2} x the cut-off applied to every subset of {97, 98, 99}, plus no cut-off,
plus a same-direction numerator. Usage: bix-13-exhaust.py <fit_dir>
"""
import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix13_common import DESIGNS, FILTERS, MODELS, de, table  # noqa: E402

fit = Path(sys.argv[1])
TH = {"lin": math.log2(1.5), "l2": 1.5, "ln": 1.5 / math.log(2)}
vals = {}
for d, m in itertools.product(DESIGNS, MODELS):
    t = {s: table(fit, d, m, s) for s in ("97", "98", "99")}
    for col, f in itertools.product(("lfc_mle", "lfc_apeglm"), FILTERS):
        for thk, th in TH.items():
            for r in range(0, 4):
                for sub in itertools.combinations(("97", "98", "99"), r):
                    s = {k: de(v, f, col if k in sub else None, th if k in sub else None) for k, v in t.items()}
                    if not s["97"]:
                        continue
                    for dirk in ("any", "same"):
                        num = (s["97"] & s["99"]) - s["98"]
                        if dirk == "same":
                            num = {g for g in num if (t["97"].at[g, col] > 0) == (t["99"].at[g, col] > 0)}
                        key = f"{d}-{m}-{col}-{f}-{thk}-cut{''.join(sub) or 'none'}-{dirk}"
                        vals[key] = 100 * len(num) / len(s["97"])
v = sorted(vals.values())
near = {k: x for k, x in vals.items() if 9.5 <= x < 11.7}
print(json.dumps({"n": len(vals), "min": v[0], "max": v[-1], "rounds_to_10_6": sum(round(x, 1) == 10.6 for x in v),
                  "near_9.5_11.7": near,
                  "min_with_cut_on_97": min(x for k, x in vals.items() if "cut97" in k or "cut9799" in k or "cut9798" in k or "cut979899" in k)},
                 sort_keys=True, indent=1))
