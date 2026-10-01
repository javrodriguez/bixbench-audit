#!/usr/bin/env python3
"""bix-7-q1. Readings, fixed before the first run (addenda 1 and 2); unit: count of groups.

  groups tested: Carrier and Affected (family-table BLM status).
  C, the control: C1 every "Unaffected" sample (the 57 control-trio samples);
     C2 age-matched: Affected against Unaffected children, Carrier against Unaffected fathers and mothers.
  F, frequency per sample: F1 non-reference variant rows; F2 F1 divided by the sample's rows with a genotype call.
  T, the test (none is named), two-sided: welch, student, mannwhitney.
  K, multiple testing (none is named): K0 p < 0.05; K1 Bonferroni over the two groups, p < 0.025.
  A reading whose p-values are not all finite reports value None.
Usage: bix-7-q1.py <data_root>
"""
import json
import math
import sys
from pathlib import Path

from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chip_common import CALLED, load, non_reference  # noqa: E402

long, fam = load(Path(sys.argv[1]) / "bix-7")
nr = non_reference(long)
called = long[long["zyg"].isin(CALLED)]
per = (
    long.groupby("sample")
    .agg(status=("BLM Mutation Status", "first"), role=("Status", "first"))
    .join(nr.groupby("sample").size().rename("n_nonref"))
    .join(called.groupby("sample").size().rename("n_called"))
    .fillna({"n_nonref": 0})
)
assert (per["n_called"] > 0).all()
per["F1"] = per["n_nonref"]
per["F2"] = per["n_nonref"] / per["n_called"]
unaff = per[per["status"] == "Unaffected"]
controls = {
    "C1": {"Carrier": unaff, "Affected": unaff},
    "C2": {"Carrier": unaff[unaff["role"].isin(["Father", "Mother"])], "Affected": unaff[unaff["role"] == "Child"]},
}
tests = {
    "welch": lambda a, b: stats.ttest_ind(a, b, equal_var=False).pvalue,
    "student": lambda a, b: stats.ttest_ind(a, b, equal_var=True).pvalue,
    "mannwhitney": lambda a, b: stats.mannwhitneyu(a, b, alternative="two-sided").pvalue,
}
out = {}
for ck, cmap in controls.items():
    for fk in ("F1", "F2"):
        for tk, t in tests.items():
            ps, ns = {}, {}
            for g in ("Carrier", "Affected"):
                x, c = per[per["status"] == g][fk], cmap[g][fk]
                assert len(x) > 1 and len(c) > 1, (ck, g)
                ps[g] = float(t(x, c))
                ns[g] = [int(len(x)), int(len(c))]
            finite = all(math.isfinite(p) for p in ps.values())
            for kk, alpha in (("K0", 0.05), ("K1", 0.025)):
                out[f"{ck}-{fk}-{tk}-{kk}"] = {
                    "value": sum(p < alpha for p in ps.values()) if finite else None,
                    "unit": "count", "p": ps, "n_group_control": ns, "defensible": True,
                }
print(json.dumps({"question_id": "bix-7-q1", "readings": out, "meta": {"samples": int(len(per))}}, sort_keys=True))
