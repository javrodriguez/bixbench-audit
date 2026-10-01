#!/usr/bin/env python3
"""bix-36-q3. Readings named before its first run (CHANGES-4, extended by CHANGES-5); unit: log2 fold change.

  genes: gene_biotype "miRNA"; samples: celltype CD14 and CD19.
  Z, normalisation: Z1 as given; Z2 counts per million; Z3 median-of-ratios size factors (bix36_common.py).
  X, a gene's log2 fold change: X1 log2((mean CD14 + 1) / (mean CD19 + 1)); X2 mean log2(value + 1) in CD14 minus
     the same in CD19; X3 log2(mean CD14 / mean CD19), genes with a zero mean in either type left out.
  E, genes kept: E1 all miRNA genes; E2 miRNA genes with a non-zero total over CD14 and CD19 samples.
  value: the median over genes (the key's range is symmetric about 0, so direction does not matter).
Usage: bix-36-q3.py <data_root>
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix36_common import load  # noqa: E402

norm, ann, meta = load(Path(sys.argv[1]), lambda a: a[a["celltype"].isin(["CD14", "CD19"])])
s14 = ann.loc[ann["celltype"] == "CD14", "sample"].tolist()
s19 = ann.loc[ann["celltype"] == "CD19", "sample"].tolist()
assert len(s14) > 1 and len(s19) > 1
out = {}
for zk, x in norm.items():
    for ek in ("E1", "E2"):
        xe = x if ek == "E1" else x[x.sum(axis=1) > 0]
        m14, m19 = xe[s14].mean(axis=1), xe[s19].mean(axis=1)
        both = (m14 > 0) & (m19 > 0)
        lfc = {
            "X1": np.log2((m14 + 1) / (m19 + 1)),
            "X2": np.log2(xe[s14] + 1).mean(axis=1) - np.log2(xe[s19] + 1).mean(axis=1),
            "X3": np.log2(m14[both] / m19[both]),
        }
        for xk, v in lfc.items():
            assert len(v) > 0 and np.isfinite(v.to_numpy()).all(), (zk, ek, xk)
            med = float(np.median(v))
            out[f"{zk}-{xk}-{ek}"] = {"value": med if math.isfinite(med) else None, "unit": "log2FC",
                                      "genes": int(len(v)), "zero_lfc_genes": int((v == 0).sum()), "defensible": True}
print(json.dumps({"question_id": "bix-36-q3", "readings": out, "meta": meta}, sort_keys=True))
