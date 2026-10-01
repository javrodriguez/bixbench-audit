"""Shared loader for bix-36 (CHANGES-5): miRNA rows for chosen samples, under three normalisations.

  Z1 batch-corrected counts as given; Z2 counts per million of each sample's total over all genes;
  Z3 counts divided by DESeq2-style median-of-ratios size factors, computed over all genes positive in every
     chosen sample.
Z1 is the table exactly as given. Negative values, if any, are set to 0 for Z2 and Z3 only; the counts (all genes,
miRNA rows) are reported.
"""
import glob
from pathlib import Path

import numpy as np
import pandas as pd


def load(data_root: Path, samples_of) -> tuple[dict, pd.DataFrame, dict]:
    hits = glob.glob(str(Path(data_root) / "bix-36" / "CapsuleData-*"))
    assert len(hits) == 1, hits
    d = Path(hits[0])
    gm = pd.read_csv(d / "GeneMetaInfo_Zenodo.csv")
    mir = set(gm.loc[gm["gene_biotype"] == "miRNA", "Geneid"].astype(str))
    ann = pd.read_csv(d / "Sample_annotated_Zenodo.csv")
    ann = samples_of(ann)
    cols = ann["sample"].tolist()
    wanted = set(cols)
    full = pd.read_csv(d / "BatchCorrectedReadCounts_Zenodo.csv", index_col=0,
                       usecols=lambda c: c in wanted or c in ("", "Unnamed: 0"), float_precision="round_trip")
    assert full.index.dtype == object and set(cols) <= set(full.columns), "gene index or samples missing"
    full = full[cols]
    assert len(full) > 0 and np.isfinite(full.to_numpy()).all()
    is_mir = full.index.astype(str).isin(mir)
    assert is_mir.sum() > 0
    n_neg_all = int((full.to_numpy() < 0).sum())
    n_neg_mir = int((full[is_mir].to_numpy() < 0).sum())
    clipped = full.clip(lower=0)  # only for Z2 and Z3; Z1 is the table exactly as given (as in the pilot)
    totals = clipped.sum(axis=0)
    assert (totals > 0).all()
    pos = clipped[(clipped > 0).all(axis=1)]
    assert len(pos) > 100
    logs = np.log(pos)
    sf = np.exp((logs.sub(logs.mean(axis=1), axis=0)).median(axis=0))
    x, xc = full[is_mir], clipped[is_mir]
    norm = {"Z1": x, "Z2": xc.div(totals, axis=1) * 1e6, "Z3": xc.div(sf, axis=1)}
    meta = {"negative_values_all_genes": n_neg_all, "negative_values_mirna": n_neg_mir,
            "negatives_set_to_0_for_Z2_Z3_only": True, "mirna_rows": int(is_mir.sum()),
            "genes_for_size_factors": int(len(pos)), "samples": len(cols)}
    return norm, ann, meta
