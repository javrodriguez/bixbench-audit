#!/usr/bin/env python3
"""bix-52-q3 (E5b). Readings named from the question's words before any run and before the key was read;
unit: chi-square statistic. Extended before any run by E5B-CHANGES-1 (pre-run review MAJOR 2, MINOR 11).

Data: ZF_AgeRelated_CpG_noMT_Final.csv (one row per CpG site per sample) and ZF_Chromosome_Length.csv.
The filter is fixed by the words: methylation > 90% or < 10% (strict).
  U, what is filtered and counted:
     U1 distinct sites whose mean methylation over the samples is > 90 or < 10;
     U2 distinct sites with at least one sample row > 90 or < 10;
     U3 sample rows (site x sample) > 90 or < 10;
     U4 distinct sites with every sample row > 90 or < 10.
  E, "uniform across the genome" (the expected counts):
     E1 proportional to chromosome length (uniform per base pair);
     E2 equal for every chromosome;
     E3 proportional to all age-related sites (the same unit, unfiltered) on each chromosome.
  K, the chromosomes in the test:
     K1 every chromosome in the length table except MT (the data file excludes MT);
     K2 only length-table chromosomes holding at least one counted site;
     K3 every chromosome present in the data file (this includes 1A and 4A, which the length table lacks);
        with E1, K3 is impossible (no lengths for 1A and 4A) and is not computed.
  value: Pearson's chi-square statistic, sum (O - E)^2 / E, expected counts scaled to the observed total;
  chromosomes with an expected count of 0 (E3 only) are left out and counted.
  Sites on chromosomes absent from the test's chromosome set are dropped and reported per chromosome.
Usage: bix-52-q3.py <data_root>
"""
import glob
import json
import sys
from pathlib import Path

import pandas as pd
from scipy import stats

d = glob.glob(str(Path(sys.argv[1]) / "bix-52" / "CapsuleData-*"))
assert len(d) == 1, d
d = Path(d[0])
cpg = pd.read_csv(d / "ZF_AgeRelated_CpG_noMT_Final.csv", dtype={"Chromosome": str})
ln = pd.read_csv(d / "ZF_Chromosome_Length.csv", encoding="utf-8-sig", dtype={"Chromosome": str})
ln["Chromosome"] = ln["Chromosome"].str.strip()
ln = ln.dropna(subset=["Length"]).set_index("Chromosome")["Length"].astype(float)
assert ln.index.is_unique
cpg["Chromosome"] = cpg["Chromosome"].astype(str).str.strip()
cpg["site"] = cpg["Chromosome"] + ":" + cpg["StartPosition"].astype(str)
cpg["x"] = (cpg["MethylationPercentage"] > 90) | (cpg["MethylationPercentage"] < 10)
site = cpg.groupby("site").agg(chrom=("Chromosome", "first"), m=("MethylationPercentage", "mean"),
                               anyx=("x", "any"), allx=("x", "all"))
site_ext_mean = (site["m"] > 90) | (site["m"] < 10)
counted = {
    "U1": (site.loc[site_ext_mean, "chrom"], site["chrom"]),
    "U2": (site.loc[site["anyx"], "chrom"], site["chrom"]),
    "U3": (cpg.loc[cpg["x"], "Chromosome"], cpg["Chromosome"]),
    "U4": (site.loc[site["allx"], "chrom"], site["chrom"]),
}
length_universe = [c for c in ln.index if c.upper() != "MT"]
data_chroms = sorted(set(cpg["Chromosome"]))
out = {}
for uk, (chroms, background) in counted.items():
    obs_all = chroms.value_counts()
    bg_all = background.value_counts()
    sets = {"K1": length_universe, "K2": [c for c in length_universe if c in obs_all.index], "K3": data_chroms}
    for kk, keys in sets.items():
        obs = obs_all.reindex(keys, fill_value=0).astype(float)
        dropped = {str(c): int(v) for c, v in obs_all.items() if c not in keys}
        for ek in ("E1", "E2", "E3"):
            if ek == "E1" and kk == "K3":
                continue
            w = {"E1": lambda: ln.reindex(keys), "E2": lambda: pd.Series(1.0, index=keys),
                 "E3": lambda: bg_all.reindex(keys, fill_value=0).astype(float)}[ek]()
            zero = w[w <= 0].index.tolist()
            o, w = obs.drop(index=zero), w.drop(index=zero)
            exp = w / w.sum() * o.sum()
            chi = float(stats.chisquare(o.to_numpy(), exp.to_numpy()).statistic)
            out[f"{uk}-{ek}-{kk}"] = {"value": chi, "unit": "chi-square", "observed_total": int(o.sum()),
                                      "chromosomes": int(len(o)), "dropped_by_chromosome": dropped,
                                      "left_out_zero_expected": [str(z) for z in zero], "defensible": True}
meta = {"rows": int(len(cpg)), "sites": int(cpg["site"].nunique()), "samples": int(cpg["Sample"].nunique()),
        "data_chromosomes": data_chroms}
print(json.dumps({"question_id": "bix-52-q3", "readings": out, "meta": meta}, sort_keys=True))
