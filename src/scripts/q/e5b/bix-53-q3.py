#!/usr/bin/env python3
"""bix-53-q3 (E5b). Readings named from the question's words before any run and before the key was read; unit: count.

Reads the table written by bix-53-q3-fit.R, the Enrichr library KEGG_2019_Mouse (gmt, pinned by hash in the run's
inputs) and Ensembl gene annotations (GTF, pinned by hash) to turn the capsule's Ensembl IDs into the symbols
the library uses (the capsule carries no annotation, so the release is a reading).
Fixed by the words: significant = p < 0.05, |shrunk log2 fold change| > 1 and baseMean > 10 (strict).
  P, "p<0.05": P1 the Wald p-value; P2 the BH-adjusted p-value (padj).
  S, the shrinkage (none is named): S1 apeglm (DESeq2's recommended estimator); S2 DESeq2's "normal" prior.
  D, the genes given to the enrichment "in the KD condition (KL)": D1 every significant gene (KL against WL);
     D2 only genes up in KL; D3 only genes down in KL.
  A, Ensembl ID to symbol: A1 Ensembl release 102 (the last GRCm38 release); A2 Ensembl release 116 (current).
  value: the number of distinct gene symbols in the list that belong to the library's "Glutathione metabolism" set,
     compared case-insensitively (gseapy's Enrichr overlap for that term).
Usage: bix-53-q3.py <fit_csv> <KEGG_2019_Mouse.gmt> <gtf_102.gz> <gtf_116.gz>
"""
import gzip
import json
import re
import sys
from pathlib import Path

import pandas as pd

fit, gmt, g102, g116 = (Path(a) for a in sys.argv[1:5])
t = pd.read_csv(fit, na_values=["NA"], keep_default_na=False, float_precision="round_trip").set_index("gene")
assert t.index.is_unique and len(t) > 20000
sets = {}
for line in gmt.read_text().splitlines():
    parts = line.split("\t")
    sets[parts[0].strip()] = {g.strip().upper() for g in parts[2:] if g.strip()}
term = [k for k in sets if k.lower() == "glutathione metabolism"]
assert len(term) == 1, term
gsh = sets[term[0]]


def symbols(gtf: Path) -> dict:
    m = {}
    with gzip.open(gtf, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            c = line.split("\t", 9)
            if c[2] != "gene":
                continue
            gid = re.search(r'gene_id "([^"]+)"', c[8]).group(1)
            nm = re.search(r'gene_name "([^"]+)"', c[8])
            if nm:
                m[gid] = nm.group(1).upper()
    return m


ann = {"A1": symbols(g102), "A2": symbols(g116)}
out = {}
for pk, pcol in (("P1", "pvalue"), ("P2", "padj")):
    for sk, lcol in (("S1", "lfc_apeglm"), ("S2", "lfc_normal")):
        sig = t[t[pcol].notna() & (t[pcol] < 0.05) & (t[lcol].abs() > 1) & (t["baseMean"] > 10)]
        for dk, sub in (("D1", sig), ("D2", sig[sig[lcol] > 0]), ("D3", sig[sig[lcol] < 0])):
            for ak, mp in ann.items():
                syms = {mp[g] for g in sub.index if g in mp}
                hits = sorted(syms & gsh)
                out[f"{pk}-{sk}-{dk}-{ak}"] = {"value": len(hits), "unit": "count", "genes_in_list": int(len(sub)),
                                               "symbols_in_list": len(syms),
                                               "unmapped": int(sum(g not in mp for g in sub.index)),
                                               "overlap": hits, "defensible": True}
meta = {"term": term[0], "term_size": len(gsh), "mapped_ids": {k: len(v) for k, v in ann.items()}}
print(json.dumps({"question_id": "bix-53-q3", "readings": out, "meta": meta}, sort_keys=True))
