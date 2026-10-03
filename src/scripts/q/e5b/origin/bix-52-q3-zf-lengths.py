#!/usr/bin/env python3
"""bix-52-q3 with real Zebra Finch chromosome lengths (E5B-CHANGES-7; after the key, answering review 3's M1).

Lengths: NCBI assembly report for bTaeGut1.4.pri (GCF_003957565.2), sha256 pinned in E5B-CHANGES-7; the
assembled-molecule rows SUPER_<n> are chromosome <n> (SUPER_Z = Z), mat_W = W; MT is left out (the data file
excludes it). This is the assembly whose naming and lengths fit the data: every data chromosome is present and every
CpG position lies within its chromosome (checked below; the run fails otherwise).
Readings: the pre-registered E1 (expected counts proportional to chromosome length) for U1-U4 (as bix-52-q3.py) over
  K1 every assembly chromosome, K2 chromosomes holding at least one counted site, K3 every chromosome in the data;
  the pre-registered E2 and E3 over the assembly's chromosome set (K1) for completeness.
value: Pearson chi-square, expected scaled to the observed total.
Usage: bix-52-q3-zf-lengths.py <data_root> <assembly_report.txt>
"""
import glob
import json
import sys
from pathlib import Path

import pandas as pd
from scipy import stats

d = Path(glob.glob(str(Path(sys.argv[1]) / "bix-52" / "CapsuleData-*"))[0])
ln = {}
for line in Path(sys.argv[2]).read_text().splitlines():
    if line.startswith("#"):
        continue
    f = line.split("\t")
    if len(f) > 8 and f[1] == "assembled-molecule" and f[0] not in ("MT", "bTaeGut1_MT"):
        name = f[0].replace("SUPER_", "").replace("mat_", "")
        ln[name] = float(f[8])
ln = pd.Series(ln)
cpg = pd.read_csv(d / "ZF_AgeRelated_CpG_noMT_Final.csv", dtype={"Chromosome": str})
cpg["Chromosome"] = cpg["Chromosome"].astype(str).str.strip()
mx = cpg.groupby("Chromosome")["EndPosition"].max()
assert set(mx.index) <= set(ln.index), sorted(set(mx.index) - set(ln.index))
assert all(mx[c] <= ln[c] for c in mx.index), {c: (int(mx[c]), ln[c]) for c in mx.index if mx[c] > ln[c]}
cpg["site"] = cpg["Chromosome"] + ":" + cpg["StartPosition"].astype(str)
cpg["x"] = (cpg["MethylationPercentage"] > 90) | (cpg["MethylationPercentage"] < 10)
site = cpg.groupby("site").agg(chrom=("Chromosome", "first"), m=("MethylationPercentage", "mean"),
                               anyx=("x", "any"), allx=("x", "all"))
ext = (site["m"] > 90) | (site["m"] < 10)
counted = {"U1": (site.loc[ext, "chrom"], site["chrom"]), "U2": (site.loc[site["anyx"], "chrom"], site["chrom"]),
           "U3": (cpg.loc[cpg["x"], "Chromosome"], cpg["Chromosome"]), "U4": (site.loc[site["allx"], "chrom"], site["chrom"])}
out = {}
for uk, (chroms, bg) in counted.items():
    obs_all, bg_all = chroms.value_counts(), bg.value_counts()
    if obs_all.sum() == 0:
        out[f"{uk}-none"] = {"value": None, "unit": "chi-square", "note": "no site counted"}
        continue
    sets = {"K1": list(ln.index), "K2": [c for c in ln.index if c in obs_all.index], "K3": sorted(set(cpg["Chromosome"]))}
    for kk, keys in sets.items():
        obs = obs_all.reindex(keys, fill_value=0).astype(float)
        for ek in (("E1",) if kk != "K1" else ("E1", "E2", "E3")):
            w = {"E1": ln.reindex(keys), "E2": pd.Series(1.0, index=keys),
                 "E3": bg_all.reindex(keys, fill_value=0).astype(float)}[ek]
            keep = w > 0
            o, e = obs[keep], w[keep] / w[keep].sum() * obs[keep].sum()
            r = stats.chisquare(o.to_numpy(), e.to_numpy())
            out[f"{uk}-{ek}-{kk}-ZFlen"] = {"value": float(r.statistic), "df": int(len(o) - 1), "unit": "chi-square",
                                           "observed_total": int(o.sum()), "added": "after key",
                                           "defensible": "pre-registered reading, corrected lengths"}
print(json.dumps({"question_id": "bix-52-q3", "origin": True, "readings": out,
                  "meta": {"genome_bp": float(ln.sum()), "chromosomes": int(len(ln))}}, sort_keys=True))
