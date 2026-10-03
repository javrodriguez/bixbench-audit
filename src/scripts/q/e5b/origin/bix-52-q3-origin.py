#!/usr/bin/env python3
"""bix-52-q3 origin check (E5B-CHANGES-3; written after the key and the reference notebook were read).

Rebuilds the notebook's function (cell 11) in Python: distinct Pos per chromosome, joined to the length table
(chromosomes without a length dropped), expected counts proportional to length, Pearson chi-square; for the
Zebra Finch (ZF) and the Jackdaw (JD) files, before and after the > 90 / < 10 row filter (cells 16 and 19).
The notebook reports, in order, 14722 (ZF all), 458.27 (ZF filtered), 4397.4 (JD all), 49.638 (JD filtered).
A mutation witness plants 20 new filtered sites (methylation 99%) on ZF chromosome 1 and recomputes the ZF
filtered value, which must move. It also records whether the capsule's two length tables are byte-identical (the notebook fetched its ZF length
file from the JD URL, cell 14).
Usage: bix-52-q3-origin.py <data_root>
"""
import glob
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
from scipy import stats

d = Path(glob.glob(str(Path(sys.argv[1]) / "bix-52" / "CapsuleData-*"))[0])


def lengths(name: str) -> pd.Series:
    t = pd.read_csv(d / name, encoding="utf-8-sig", dtype={"Chromosome": str})
    return t.dropna(subset=["Length"]).set_index(t["Chromosome"].str.strip())["Length"].astype(float)


def chi(cpg: pd.DataFrame, ln: pd.Series) -> dict:
    n = cpg.groupby(cpg["Chromosome"].astype(str).str.strip())["Pos"].nunique()
    n = n[n.index.isin(ln.index)]
    exp = ln.reindex(n.index)
    exp = exp / exp.sum() * n.sum()
    r = stats.chisquare(n.to_numpy(dtype=float), exp.to_numpy())
    return {"value": float(r.statistic), "df": int(len(n) - 1), "p": float(r.pvalue), "unit": "chi-square",
            "added": "after key", "defensible": "origin evidence"}


out = {}
for sp in ("ZF", "JD"):
    cpg = pd.read_csv(d / f"{sp}_AgeRelated_CpG_noMT_Final.csv", dtype={"Chromosome": str})
    ln = lengths(f"{sp}_Chromosome_Length.csv")
    filt = cpg[(cpg["MethylationPercentage"] > 90) | (cpg["MethylationPercentage"] < 10)]
    out[f"origin-{sp}-all"] = chi(cpg, ln)
    out[f"origin-{sp}-filtered"] = chi(filt, ln)
zf = pd.read_csv(d / "ZF_AgeRelated_CpG_noMT_Final.csv", dtype={"Chromosome": str})
plant = pd.DataFrame({"Pos": [f"1_planted{i}" for i in range(20)], "Chromosome": "1", "MethylationPercentage": 99.0})
zf_m = pd.concat([zf[["Pos", "Chromosome", "MethylationPercentage"]], plant], ignore_index=True)
zf_m = zf_m[(zf_m["MethylationPercentage"] > 90) | (zf_m["MethylationPercentage"] < 10)]
out["witness-ZF-filtered-plus-20-on-chr1"] = chi(zf_m, lengths("ZF_Chromosome_Length.csv"))
same = hashlib.sha256((d / "ZF_Chromosome_Length.csv").read_bytes()).hexdigest() == \
    hashlib.sha256((d / "JD_Chromosome_Length.csv").read_bytes()).hexdigest()
print(json.dumps({"question_id": "bix-52-q3", "origin": True, "readings": out,
                  "meta": {"zf_and_jd_length_files_identical": same}}, sort_keys=True))
