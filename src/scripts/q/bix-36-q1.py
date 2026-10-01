#!/usr/bin/env python3
"""bix-36-q1. Readings, fixed before the first run (addenda 1 and 2); unit: F statistic.

  genes: gene_biotype "miRNA" in GeneMetaInfo_Zenodo.csv; samples: celltype CD4, CD8, CD14, CD19 (PBMC excluded).
  S, one observation: S1 a sample's mean over miRNA genes; S2 each gene x sample value;
     S3 a gene's mean within one cell type.
  T, scale: T1 batch-corrected counts as given; T2 log2(count + 1).
  E, genes kept: E1 all miRNA genes; E2 miRNA genes with a non-zero total over the kept samples.
  statistic: one-way ANOVA F across the four cell types (scipy f_oneway).
Usage: bix-36-q1.py <data_root>
"""
import glob
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

hits = glob.glob(str(Path(sys.argv[1]) / "bix-36" / "CapsuleData-*"))
assert len(hits) == 1, hits
d = Path(hits[0])
gm = pd.read_csv(d / "GeneMetaInfo_Zenodo.csv")
mir = set(gm.loc[gm["gene_biotype"] == "miRNA", "Geneid"].astype(str))
ann = pd.read_csv(d / "Sample_annotated_Zenodo.csv")
ann = ann[ann["celltype"] != "PBMC"]
parts = []
for chunk in pd.read_csv(d / "BatchCorrectedReadCounts_Zenodo.csv", chunksize=5000, index_col=0):
    parts.append(chunk[chunk.index.astype(str).isin(mir)])
x = pd.concat(parts)
assert set(ann["sample"]) <= set(x.columns)
x = x[ann["sample"].tolist()]
assert len(x) > 0 and np.isfinite(x.to_numpy()).all()
types = ["CD4", "CD8", "CD14", "CD19"]
out = {}
for ek in ("E1", "E2"):
    xe = x if ek == "E1" else x[x.sum(axis=1) > 0]
    for tk in ("T1", "T2"):
        xt = xe if tk == "T1" else np.log2(xe + 1)
        by = {t: xt[ann.loc[ann["celltype"] == t, "sample"]] for t in types}
        obs = {
            "S1": [by[t].mean(axis=0).to_numpy() for t in types],
            "S2": [by[t].to_numpy().ravel() for t in types],
            "S3": [by[t].mean(axis=1).to_numpy() for t in types],
        }
        for sk, groups in obs.items():
            r = stats.f_oneway(*groups)
            f = float(r.statistic)
            out[f"{sk}-{tk}-{ek}"] = {"value": f if math.isfinite(f) else None, "unit": "F", "p": float(r.pvalue),
                                      "n": [int(len(g)) for g in groups], "defensible": True}
meta = {"mirna_genes_in_meta": len(mir), "mirna_rows_in_counts": int(len(x)), "samples": int(x.shape[1])}
print(json.dumps({"question_id": "bix-36-q1", "readings": out, "meta": meta}, sort_keys=True))
