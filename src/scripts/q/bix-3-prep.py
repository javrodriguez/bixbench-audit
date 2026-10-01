#!/usr/bin/env python3
"""Convert the bix-3 capsule's NormCount sheet to CSV for R (the Mac's R has no readxl).

The sheet's header is on its fourth row (Index, GeneID, then one column per sample).
Usage: bix-3-prep.py <data_root> <out_csv>; prints the CSV's sha256.
"""
import glob
import hashlib
import re
import sys
from pathlib import Path

import pandas as pd

f = glob.glob(str(Path(sys.argv[1]) / "bix-3" / "CapsuleData-*" / "Data_deposition_RNAseq_Paroxetine_2017.xlsx"))
assert len(f) == 1, f
x = pd.read_excel(f[0], sheet_name="NormCount", header=3)
assert list(x.columns[:2]) == ["Index", "GeneID"], list(x.columns[:3])
x = x.drop(columns=["Index"]).dropna(subset=["GeneID"])
# Keep only GeneID and per-sample count columns (<group>_<tissue><n>); the sheet's own DE result columns
# (baseMean, log2FoldChange, padj, DEG and the like) are notebook-like outputs and are dropped unread.
samples = [c for c in x.columns if re.fullmatch(r"[A-Za-z_]+_(baseline_blood|final_blood|dentate_gyrus)\d+", str(c))]
dropped = [str(c) for c in x.columns if c != "GeneID" and c not in samples]
x = x[["GeneID"] + samples]
print("dropped columns:", len(dropped), file=sys.stderr)
out = Path(sys.argv[2])
out.parent.mkdir(parents=True, exist_ok=True)
x.to_csv(out, index=False)
print(hashlib.sha256(out.read_bytes()).hexdigest(), x.shape[0], x.shape[1] - 1)
