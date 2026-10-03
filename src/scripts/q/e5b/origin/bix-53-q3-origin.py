#!/usr/bin/env python3
"""bix-53-q3 origin count (E5B-CHANGES-3; written after the key and the reference notebook were read).

Reads bix-53-q3-origin-fit.R's tables; keeps padj < 0.05, |apeglm LFC| > 1 and baseMean >= 10 (the notebook's
cell 53); maps Ensembl IDs to symbols (A1 Ensembl 102, A2 Ensembl 116; the notebook used the live Ensembl REST
lookup, cell 61); counts distinct symbols in KEGG_2019_Mouse "Glutathione metabolism", and prints the Enrichr
overlap string k/term_size, the key's format.
Usage: bix-53-q3-origin.py <fit_dir> <KEGG_2019_Mouse.gmt> <gtf_102.gz> <gtf_116.gz>
"""
import gzip
import json
import re
import sys
from pathlib import Path

import pandas as pd

fit, gmt, g102, g116 = (Path(a) for a in sys.argv[1:5])
gsh = None
for line in gmt.read_text().splitlines():
    p = line.split("\t")
    if p[0].strip().lower() == "glutathione metabolism":
        gsh = {g.strip().upper() for g in p[2:] if g.strip()}
assert gsh


def symbols(gtf: Path) -> dict:
    m = {}
    with gzip.open(gtf, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            c = line.split("\t", 9)
            if c[2] == "gene":
                nm = re.search(r'gene_name "([^"]+)"', c[8])
                if nm:
                    m[re.search(r'gene_id "([^"]+)"', c[8]).group(1)] = nm.group(1).upper()
    return m


ann = {"A1": symbols(g102), "A2": symbols(g116)}
out = {}
for xk in ("X4", "X6"):
    t = pd.read_csv(fit / f"bix-53-origin-{xk}.csv", na_values=["NA"], keep_default_na=False,
                    float_precision="round_trip").set_index("gene")
    sig = t[t["padj"].notna() & (t["padj"] < 0.05) & (t["lfc_apeglm"].abs() > 1) & (t["baseMean"] >= 10)]
    for ak, mp in ann.items():
        hits = sorted({mp[g] for g in sig.index if g in mp} & gsh)
        out[f"origin-{xk}-{ak}"] = {"value": len(hits), "unit": "count", "overlap_string": f"{len(hits)}/{len(gsh)}",
                                    "significant_genes": int(len(sig)), "overlap": hits, "added": "after key",
                                    "defensible": "Javier to rule"}
print(json.dumps({"question_id": "bix-53-q3", "origin": True, "readings": out}, sort_keys=True))
