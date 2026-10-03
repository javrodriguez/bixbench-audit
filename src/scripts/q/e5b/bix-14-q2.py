#!/usr/bin/env python3
"""bix-14-q2 (E5b). Readings named from the question's words before any run and before the key was read.
Extended before any run by E5B-CHANGES-1 (pre-run review MAJOR 5, MINOR 6 and 7).

Data: every per-sample table in CHIP_DP10_GQ20_PASS plus the family table, loaded by E5a's frozen chip_common.py;
this script adds one column to the loader's column map at run time ("Effect (Combined)", for M3), leaving the
frozen file unchanged.
  W, the rows examined ("variants with a VAF < 0.3"; a blank VAF is never < 0.3):
     W1 non-reference calls (Heterozygous or Homozygous Variant) with VAF < 0.3;
     W2 every row with VAF < 0.3, whatever its genotype call (the words state only the VAF filter).
  G, "the parental control group" (the words do not say whose parents):
     G1 the parents (Father or Mother) of the control trios, BLM status "Unaffected";
     G2 the parents of the probands, BLM status "Carrier", read as the probands' own parental controls;
     G3 every parent (Father or Mother), Carrier and Unaffected together.
  The probands: every sample with BLM status "Affected".
  M, a missense variant: M1 its Sequence Ontology term contains "missense_variant"; M2 its term is exactly
     "missense_variant" (in this data every term is single, so M2 is expected to equal M1); M3 its RefSeq
     "Effect (Combined)" is "Missense".
  F, "missense variant frequency" of a group (unit in brackets):
     F1 pooled share: missense rows over all examined rows of the group [fraction]; F1p the same [percent];
     F2 mean over the group's samples of each sample's missense share [fraction]; F2p the same [percent];
     F3 mean over the group's samples of each sample's missense row count [count per sample].
  D, "the difference between" the two groups: D1 control minus probands (the words' order); D2 probands minus
     control; D3 the absolute difference.
Usage: bix-14-q2.py <data_root>
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import chip_common  # noqa: E402

chip_common.KEEP[("RefSeq Genes 110, NCBI", "Effect (Combined)")] = "effect"
long, fam = chip_common.load(Path(sys.argv[1]) / "bix-14")
long["vaf_num"] = pd.to_numeric(long["vaf"], errors="coerce")
long["so_s"] = long["so"].astype(str).str.strip()
long["eff_s"] = long["effect"].astype(str).str.strip()
rows = {
    "W1": long[long["zyg"].isin({"Heterozygous", "Homozygous Variant"}) & (long["vaf_num"] < 0.3)],
    "W2": long[long["vaf_num"] < 0.3],
}
is_mis = {
    "M1": lambda t: t["so_s"].str.contains("missense_variant", regex=False),
    "M2": lambda t: t["so_s"] == "missense_variant",
    "M3": lambda t: t["eff_s"].str.lower() == "missense",
}
parents = fam["Status"].isin(["Father", "Mother"])
groups = {
    "G1": fam[(fam["BLM Mutation Status"] == "Unaffected") & parents]["sample"],
    "G2": fam[(fam["BLM Mutation Status"] == "Carrier") & parents]["sample"],
    "G3": fam[fam["BLM Mutation Status"].isin(["Unaffected", "Carrier"]) & parents]["sample"],
    "P": fam[fam["BLM Mutation Status"] == "Affected"]["sample"],
}
have = set(long["sample"])
groups = {k: sorted(set(v) & have) for k, v in groups.items()}
assert all(len(v) > 1 for v in groups.values()), {k: len(v) for k, v in groups.items()}


def freq(t: pd.DataFrame, samples: list, mk: str) -> dict:
    g = t[t["sample"].isin(samples)].copy()
    g["mis"] = is_mis[mk](g)
    per = pd.DataFrame(index=samples)
    per["n"] = g.groupby("sample").size()
    per["k"] = g.groupby("sample")["mis"].sum()
    per = per.fillna(0)
    with_rows = per[per["n"] > 0]
    f1 = float(g["mis"].sum() / len(g))
    f2 = float((with_rows["k"] / with_rows["n"]).mean())
    return {"F1": f1, "F1p": 100 * f1, "F2": f2, "F2p": 100 * f2, "F3": float(per["k"].mean()), "rows": int(len(g)),
            "samples_with_rows": int(len(with_rows))}


UNITS = {"F1": "fraction", "F1p": "percent", "F2": "fraction", "F2p": "percent", "F3": "count"}
out = {}
for wk, t in rows.items():
    for mk in is_mis:
        fp = freq(t, groups["P"], mk)
        for gk in ("G1", "G2", "G3"):
            fc = freq(t, groups[gk], mk)
            for fk, unit in UNITS.items():
                diff = fc[fk] - fp[fk]
                for dk, v in (("D1", diff), ("D2", -diff), ("D3", abs(diff))):
                    out[f"{wk}-{gk}-{mk}-{fk}-{dk}"] = {
                        "value": v, "unit": unit, "control": fc[fk], "probands": fp[fk],
                        "rows_control_probands": [fc["rows"], fp["rows"]],
                        "samples_with_rows_control_probands": [fc["samples_with_rows"], fp["samples_with_rows"]],
                        "defensible": True}
meta = {"group_sizes": {k: len(v) for k, v in groups.items()},
        "vaf_blank_rows": int(long["vaf_num"].isna().sum()), "vaf_max": float(long["vaf_num"].max()),
        "effect_values": sorted(long["eff_s"].unique().tolist())}
print(json.dumps({"question_id": "bix-14-q2", "readings": out, "meta": meta}, sort_keys=True))
