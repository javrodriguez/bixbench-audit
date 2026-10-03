#!/usr/bin/env python3
"""bix-14-q2 origin check (E5B-CHANGES-3; written after the key and the reference notebook were read).

Rebuilds the notebook's route (cells 20-23) from the capsule data:
  non-reference calls (blank zygosity rows dropped, as R's NA rows are), then rows whose Sequence Ontology is
  intron_variant, intergenic_variant, 3_prime_UTR_variant or 5_prime_UTR_variant removed ("exome" filter),
  then VAF < 0.3; Effect (Combined) relabelled "Synonymous" where the ontology term contains "synonymous";
  per group (Control Parents = Unaffected Father/Mother; BSyn Probands = Affected), the share of rows whose effect
  is "Missense". value: Control Parents minus BSyn Probands.
Also reports the same route without the exome filter, to show which step moves the value.
Readings here are "added after key".
Usage: bix-14-q2-origin.py <data_root>
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
import chip_common  # noqa: E402

chip_common.KEEP[("RefSeq Genes 110, NCBI", "Effect (Combined)")] = "effect"
long, fam = chip_common.load(Path(sys.argv[1]) / "bix-14")
long["vaf_num"] = pd.to_numeric(long["vaf"], errors="coerce")
so = long["so"].astype(str).str.strip()
eff = long["effect"].astype(str).str.strip()
eff = eff.where(~so.str.contains("synonymous", regex=False), "Synonymous")
long = long.assign(so_s=so, eff_s=eff)
nonref = long[long["zyg"].isin({"Heterozygous", "Homozygous Variant"})]
EXCL = {"intron_variant", "intergenic_variant", "3_prime_UTR_variant", "5_prime_UTR_variant"}
parents = fam["Status"].isin(["Father", "Mother"])
grp = {"control_parents": set(fam[(fam["BLM Mutation Status"] == "Unaffected") & parents]["sample"]),
       "probands": set(fam[fam["BLM Mutation Status"] == "Affected"]["sample"]),
       "carriers": set(fam[fam["BLM Mutation Status"] == "Carrier"]["sample"]),
       "control_children": set(fam[(fam["BLM Mutation Status"] == "Unaffected") & ~parents]["sample"])}
out = {}
for rk, t in (("exome", nonref[~nonref["so_s"].isin(EXCL)]), ("no-exome-filter", nonref)):
    v = t[t["vaf_num"] < 0.3]
    share = {}
    for g, s in grp.items():
        x = v[v["sample"].isin(s)]
        share[g] = {"missense_share": float((x["eff_s"] == "Missense").sum() / len(x)), "rows": int(len(x))}
    out[f"origin-{rk}"] = {"value": share["control_parents"]["missense_share"] - share["probands"]["missense_share"],
                           "unit": "fraction", "groups": share, "rows_nonref_after_filter": int(len(t)),
                           "added": "after key", "defensible": "Javier to rule"}
print(json.dumps({"question_id": "bix-14-q2", "origin": True, "readings": out}, sort_keys=True))
