#!/usr/bin/env python3
"""bix-2-q1. Readings, fixed before the first run (addenda 1 and 2); unit: fraction.

  G, the individuals counted (family-table BLM status): G1 Carrier or Affected; G2 Affected; G3 Carrier.
  V, the variant rows counted: V1 non-reference genotype with a VAF; V2 any row with a VAF.
  somatic: VAF < 0.3.
Usage: bix-2-q1.py <data_root>
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chip_common import load, non_reference  # noqa: E402

long, fam = load(Path(sys.argv[1]) / "bix-2")
groups = {"G1": {"Carrier", "Affected"}, "G2": {"Affected"}, "G3": {"Carrier"}}
rowsets = {"V1": non_reference(long).dropna(subset=["vaf"]), "V2": long.dropna(subset=["vaf"])}
out = {}
for gk, g in groups.items():
    for vk, v in rowsets.items():
        w = v[v["BLM Mutation Status"].isin(g)]
        assert len(w) > 0, (gk, vk)
        som = int((w["vaf"] < 0.3).sum())
        val = som / len(w)
        assert math.isfinite(val)
        out[f"{gk}-{vk}"] = {"value": val, "unit": "fraction", "somatic": som, "all": int(len(w)),
                             "samples": int(w["sample"].nunique()), "defensible": True}
meta = {"files": int(long["file"].nunique()), "family_rows": int(len(fam))}
print(json.dumps({"question_id": "bix-2-q1", "readings": out, "meta": meta}, sort_keys=True))
