#!/usr/bin/env python3
"""bix-36-q5 (E5b). Readings named from the question's words before any run and before the key was read; unit: text
label (with the numbers it rests on).

The key is text, so each reading ends in a label from a named convention; the accept rule compares text exactly
(trimmed, lower-cased), and the note discusses near-synonyms only as readings added after the key.
Samples: cell types CD4, CD8, CD14 and CD19 (PBMC samples excluded, as the words say).
  G, the genes: G1 gene_biotype "miRNA" (the capsule's study); G2 every gene in the table (the words name none).
  Z, normalisation, as E5a's bix36_common.py: Z1 as given; Z2 counts per million; Z3 median-of-ratios size factors
     (computed over genes positive in every chosen sample); negatives set to 0 for Z2 and Z3 only.
  X, a gene's log2 fold change in one comparison, as E5a's bix-36-q3: X1 log2((mean a + 1) / (mean b + 1));
     X2 mean log2(value + 1) in a minus the same in b; X3 log2(mean a / mean b), genes with a zero mean left out.
  O, the comparisons pooled (the words fix no direction): O1 the six pairs, each later cell type against the
     earlier one in the order CD4, CD8, CD14, CD19; O3 the same six pairs reversed; O2 the six pairs in both
     directions (twelve, symmetric by construction, so O2-L1 cannot depend on the data and is reported with
     "defensible": false).
  L, the label: L1 symmetry (Bulmer's rule on sample skewness: |g1| < 0.5 "approximately symmetric",
     0.5-1 "moderately right-skewed" or "moderately left-skewed", > 1 "highly right-skewed" or "highly left-skewed");
     L2 normality (D'Agostino-Pearson K2 test, alpha 0.05: "normal" or "not normal");
     L3 tails (kurtosis test, alpha 0.05, on excess kurtosis: "leptokurtic", "platykurtic", else "mesokurtic");
     L4 modality (local maxima of a binned Gaussian kernel density: 2048 bins between the 0.5th and 99.5th
     percentiles, Scott's bandwidth, maxima above 10% of the highest counted: "unimodal", "bimodal", "multimodal").
  Synonyms (E5B-CHANGES-1, written before any run and before the key was read): each label carries the fixed list
     SYNONYMS below; the E5b comparator accepts a text key equal (trimmed, lower-cased) to the label or a synonym.
Usage: bix-36-q5.py <data_root>
"""
import glob
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

d = glob.glob(str(Path(sys.argv[1]) / "bix-36" / "CapsuleData-*"))
assert len(d) == 1, d
d = Path(d[0])
TYPES = ["CD4", "CD8", "CD14", "CD19"]
gm = pd.read_csv(d / "GeneMetaInfo_Zenodo.csv")
mir = set(gm.loc[gm["gene_biotype"] == "miRNA", "Geneid"].astype(str))
ann = pd.read_csv(d / "Sample_annotated_Zenodo.csv")
ann = ann[ann["celltype"].isin(TYPES)]
cols = ann["sample"].tolist()
full = pd.read_csv(d / "BatchCorrectedReadCounts_Zenodo.csv", index_col=0, float_precision="round_trip")
assert set(cols) <= set(full.columns)
full = full[cols]
assert np.isfinite(full.to_numpy()).all()
clipped = full.clip(lower=0)
totals = clipped.sum(axis=0)
pos = clipped[(clipped > 0).all(axis=1)]
logs = np.log(pos)
sf = np.exp(logs.sub(logs.mean(axis=1), axis=0).median(axis=0))
norm_all = {"Z1": full, "Z2": clipped.div(totals, axis=1) * 1e6, "Z3": clipped.div(sf, axis=1)}
by_type = {t: ann.loc[ann["celltype"] == t, "sample"].tolist() for t in TYPES}
assert all(len(v) > 1 for v in by_type.values())


def lfc(x: pd.DataFrame, a: str, b: str, xk: str) -> np.ndarray:
    xa, xb = x[by_type[a]], x[by_type[b]]
    ma, mb = xa.mean(axis=1), xb.mean(axis=1)
    if xk == "X1":
        v = np.log2((ma + 1) / (mb + 1))
    elif xk == "X2":
        v = np.log2(xa.clip(lower=0) + 1).mean(axis=1) - np.log2(xb.clip(lower=0) + 1).mean(axis=1)
    else:
        both = (ma > 0) & (mb > 0)
        v = np.log2(ma[both] / mb[both])
    v = np.asarray(v, dtype=float)
    return v[np.isfinite(v)]


def labels(v: np.ndarray) -> dict:
    g1 = float(stats.skew(v))
    ex = float(stats.kurtosis(v))
    side = "right" if g1 > 0 else "left"
    l1 = "approximately symmetric" if abs(g1) < 0.5 else (f"moderately {side}-skewed" if abs(g1) <= 1 else f"highly {side}-skewed")
    k2p = float(stats.normaltest(v).pvalue)
    ktp = float(stats.kurtosistest(v).pvalue)
    l3 = "mesokurtic" if ktp >= 0.05 else ("leptokurtic" if ex > 0 else "platykurtic")
    return {"L1": l1, "L2": "normal" if k2p >= 0.05 else "not normal", "L3": l3, "L4": modes(v),
            "stats": {"n": int(len(v)), "skewness": g1, "excess_kurtosis": ex, "normaltest_p": k2p,
                      "kurtosistest_p": ktp, "mean": float(v.mean()), "median": float(np.median(v))}}


SYN = {
    "approximately symmetric": ["approximately symmetric", "symmetric", "symmetrical", "roughly symmetric"],
    "normal": ["normal", "approximately normal", "normally distributed", "gaussian", "bell-shaped", "bell shaped",
               "normal distribution", "approximately normally distributed"],
    "not normal": ["not normal", "non-normal", "not normally distributed", "non-normally distributed"],
    "leptokurtic": ["leptokurtic", "heavy-tailed", "heavy tailed", "fat-tailed"],
    "platykurtic": ["platykurtic", "light-tailed", "light tailed"],
    "mesokurtic": ["mesokurtic"],
    "unimodal": ["unimodal"], "bimodal": ["bimodal"], "multimodal": ["multimodal"],
}
for _deg in ("moderately", "highly"):
    for _side, _sign in (("right", "positively"), ("left", "negatively")):
        SYN[f"{_deg} {_side}-skewed"] = [f"{_deg} {_side}-skewed", f"{_side}-skewed", f"{_side} skewed",
                                         f"skewed {_side}", f"{_sign} skewed", f"{_side}-skewed distribution"]


def modes(v: np.ndarray) -> str:
    lo, hi = np.percentile(v, [0.5, 99.5])
    h, edges = np.histogram(v, bins=2048, range=(lo, hi))
    width = edges[1] - edges[0]
    bw = float(np.std(v, ddof=1)) * len(v) ** (-1 / 5)
    half = int(np.ceil(4 * bw / width))
    k = np.exp(-0.5 * ((np.arange(-half, half + 1) * width) / bw) ** 2)
    dens = np.convolve(h, k, mode="same")
    peak = (dens[1:-1] > dens[:-2]) & (dens[1:-1] >= dens[2:]) & (dens[1:-1] > 0.1 * dens.max())
    n = int(peak.sum())
    return "unimodal" if n <= 1 else ("bimodal" if n == 2 else "multimodal")


pairs = list(itertools.combinations(TYPES, 2))
out = {}
for gk in ("G1", "G2"):
    for zk, x in norm_all.items():
        xg = x[x.index.astype(str).isin(mir)] if gk == "G1" else x
        for xk in ("X1", "X2", "X3"):
            one = [lfc(xg, b, a, xk) for a, b in pairs]
            rev = [lfc(xg, a, b, xk) for a, b in pairs]
            two = one + rev
            for ok, parts in (("O1", one), ("O3", rev), ("O2", two)):
                lab = labels(np.concatenate(parts))
                for lk in ("L1", "L2", "L3", "L4"):
                    out[f"{gk}-{zk}-{xk}-{ok}-{lk}"] = {"value": lab[lk], "unit": "label", "stats": lab["stats"],
                                                        "synonyms": SYN[lab[lk]],
                                                        "defensible": not (ok == "O2" and lk == "L1")}
meta = {"samples": len(cols), "per_type": {t: len(v) for t, v in by_type.items()}, "mirna_rows": int(full.index.astype(str).isin(mir).sum()),
        "genes": int(len(full)), "genes_for_size_factors": int(len(pos))}
print(json.dumps({"question_id": "bix-36-q5", "readings": out, "meta": meta}, sort_keys=True))
