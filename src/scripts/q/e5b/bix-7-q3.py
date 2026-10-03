#!/usr/bin/env python3
"""bix-7-q3 (E5b). Readings named from the question's words before any run and before the key was read;
unit: count.

Data: every per-sample table in CHIP_DP10_GQ20_PASS (86 samples), loaded by E5a's frozen chip_common.py.
  V, what "removing reference calls" leaves:
     V1 rows whose zygosity is a non-reference call (Heterozygous or Homozygous Variant);
     V2 rows whose zygosity is anything but "Reference" (blank or other no-call rows stay in).
  U, what a "variant" is:
     U1 a row (one variant in one sample);
     U2 a distinct variant (Chr:Pos plus Ref/Alt), over all samples.
Usage: bix-7-q3.py <data_root>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from chip_common import load  # noqa: E402

long, fam = load(Path(sys.argv[1]) / "bix-7")
keep = {
    "V1": long[long["zyg"].isin({"Heterozygous", "Homozygous Variant"})],
    "V2": long[long["zyg"] != "Reference"],
}
out = {}
for vk, t in keep.items():
    out[f"{vk}-U1"] = {"value": int(len(t)), "unit": "count", "defensible": True}
    out[f"{vk}-U2"] = {"value": int(t[["chrpos", "refalt"]].drop_duplicates().shape[0]), "unit": "count",
                       "defensible": True}
meta = {"samples": int(long["sample"].nunique()), "rows_all": int(len(long)),
        "zygosity_values": sorted(long["zyg"].unique().tolist())}
print(json.dumps({"question_id": "bix-7-q3", "readings": out, "meta": meta}, sort_keys=True))
