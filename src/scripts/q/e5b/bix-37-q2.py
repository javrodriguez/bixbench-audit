#!/usr/bin/env python3
"""bix-37-q2 (E5b). Readings named from the question's words before any run and before the key was read.

Data: the capsule's proteomic table (sheet "Tumor vs Normal"), one row per protein, a group-level "Normal" column.
The ENO1 row is found by its gene column (exactly one row must match, case-insensitive).
  R, "base protein level in normal samples": R1 the "Normal" value as given [intensity];
     R2 its log2 [log2 intensity] (proteomic intensities are often reported on a log2 scale).
  The words fix the rounding (3 significant figures); the accept rule compares at the key's shown precision.
Usage: bix-37-q2.py <data_root>
"""
import glob
import json
import math
import sys
from pathlib import Path

import pandas as pd

f = glob.glob(str(Path(sys.argv[1]) / "bix-37" / "CapsuleData-*" / "Proteomic_data*.xlsx"))
assert len(f) == 1, f
t = pd.read_excel(f[0], sheet_name="Tumor vs Normal")
hit = t[t["gene"].astype(str).str.strip().str.upper() == "ENO1"]
assert len(hit) == 1, len(hit)
v = float(hit["Normal"].iloc[0])
out = {"R1": {"value": v, "unit": "intensity", "defensible": True},
       "R2": {"value": math.log2(v), "unit": "log2 intensity", "defensible": True}}
print(json.dumps({"question_id": "bix-37-q2", "readings": out,
                  "meta": {"protein": str(hit["protein"].iloc[0]), "rows": int(len(t))}}, sort_keys=True))
