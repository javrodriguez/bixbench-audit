"""Shared loader for the CHIP exome capsules (bix-2, bix-7, bix-39).

Reads only CapsuleData files: the per-sample CHIP_DP10_GQ20_PASS/*.xlsx tables and 230215_Trio_Status.xlsx.
Deliberately unread: "CHIP VAF mean proportions.xlsx" (a derived table) and the CHIP gene list.
Every per-sample file must join exactly one family-table row by its ID (a numeric family ID, or an SRA run
accession for the 57 control-trio samples); IDs are compared after stripping whitespace (addendum 2, section 1).
"""
import glob
import re
from pathlib import Path

import pandas as pd

KEEP = {
    ("Variant Info", "Chr:Pos"): "chrpos",
    ("Variant Info", "Ref/Alt"): "refalt",
    ("RefSeq Genes 110, NCBI", "Gene Names"): "gene",
    ("RefSeq Genes 110, NCBI", "Sequence Ontology (Combined)"): "so",
}
PER_SAMPLE = {"Zygosity": "zyg", "Variant Allele Freq": "vaf", "Read Depths (DP)": "dp"}
CALLED = {"Reference", "Heterozygous", "Homozygous Variant"}


def capsule_data(capsule_dir: Path) -> Path:
    hits = glob.glob(str(Path(capsule_dir) / "CapsuleData-*"))
    assert len(hits) == 1, hits
    return Path(hits[0])


def load(capsule_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    d = capsule_data(capsule_dir)
    fam = pd.read_excel(d / "230215_Trio_Status.xlsx")
    fam["sample"] = fam["Sample ID"].astype(str).str.strip()
    fam["Status"] = fam["Status"].astype(str).str.strip()
    fam["BLM Mutation Status"] = fam["BLM Mutation Status"].astype(str).str.strip()
    assert not fam["sample"].duplicated().any()
    frames = []
    for f in sorted((d / "CHIP_DP10_GQ20_PASS").glob("*.xlsx")):
        m = re.search(r"_CHIP_(\d+)-[A-Za-z0-9]+\.xlsx$", f.name) or re.search(r"_CHIP_(SRR\d+)\.xlsx$", f.name)
        assert m, f.name
        s = pd.read_excel(f, header=[0, 1])
        cols = {}
        for top, sub in s.columns:
            if (top, sub) in KEEP:
                cols[(top, sub)] = KEEP[(top, sub)]
            elif sub in PER_SAMPLE:
                cols[(top, sub)] = PER_SAMPLE[sub]
        assert sorted(cols.values()) == sorted(list(KEEP.values()) + list(PER_SAMPLE.values())), (f.name, cols)
        t = s[list(cols)].copy()
        t.columns = list(cols.values())
        assert len(t) > 0, f.name
        t["sample"] = m.group(1)
        t["file"] = f.name
        frames.append(t)
    long = pd.concat(frames, ignore_index=True)
    joined = set(long["sample"]) & set(fam["sample"])
    assert joined == set(long["sample"]), sorted(set(long["sample"]) - joined)
    long = long.merge(fam[["sample", "Status", "BLM Mutation Status"]], on="sample", how="left", validate="many_to_one")
    long["zyg"] = long["zyg"].astype(str).str.strip()
    return long, fam


def non_reference(long: pd.DataFrame) -> pd.DataFrame:
    return long[long["zyg"].isin({"Heterozygous", "Homozygous Variant"})]
