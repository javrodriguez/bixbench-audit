#!/usr/bin/env python3
"""bix-2-q2. Readings named before its first run (CHANGES-4); unit: percent.

  Cohort: family-table Status "Child" with BLM status "Unaffected" (the 19 control-trio children).
  V, the variant rows counted: V1 non-reference genotype with a VAF; V2 any row with a VAF.
  B, the VAF band: B1 0.3 <= VAF <= 0.7; B2 0.3 < VAF < 0.7.
  U, what is pooled: U1 all variant rows of the cohort together; U2 the mean of per-child percentages.
Usage: bix-2-q2.py <data_root>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chip_common import load, non_reference  # noqa: E402

long, fam = load(Path(sys.argv[1]) / "bix-2")
kids = long[(long["Status"] == "Child") & (long["BLM Mutation Status"] == "Unaffected")]
assert kids["sample"].nunique() == 19, kids["sample"].nunique()
rowsets = {"V1": non_reference(kids).dropna(subset=["vaf"]), "V2": kids.dropna(subset=["vaf"])}
bands = {"B1": lambda v: (v >= 0.3) & (v <= 0.7), "B2": lambda v: (v > 0.3) & (v < 0.7)}
out = {}
for vk, v in rowsets.items():
    assert len(v) > 0
    for bk, band in bands.items():
        inside = band(v["vaf"])
        per_child = inside.groupby(v["sample"]).mean()
        out[f"{vk}-{bk}-U1"] = {"value": 100 * float(inside.mean()), "unit": "percent", "in_band": int(inside.sum()),
                                "all": int(len(v)), "defensible": True}
        out[f"{vk}-{bk}-U2"] = {"value": 100 * float(per_child.mean()), "unit": "percent",
                                "children": int(len(per_child)), "defensible": True}
print(json.dumps({"question_id": "bix-2-q2", "readings": out}, sort_keys=True))
