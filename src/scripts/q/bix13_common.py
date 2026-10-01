"""Reads the shared bix-13 fit tables written by bix-13-fit.R (CHANGES-4)."""
import math
from pathlib import Path

import pandas as pd

DESIGNS, MODELS, FILTERS = ("D1", "D2", "D3"), ("M1", "M2"), ("F1", "F2", "F3")


def table(fit_dir: Path, d: str, m: str, strain: str) -> pd.DataFrame:
    t = pd.read_csv(fit_dir / f"bix-13_{d}_{m}_{strain}.csv", na_values=["NA"], keep_default_na=False,
                    float_precision="round_trip")
    assert len(t) == 5828 and t["gene"].is_unique, (d, m, strain, len(t))
    return t.set_index("gene")


def de(t: pd.DataFrame, f: str, lfc_col: str | None, cutoff: float | None) -> set:
    ok = t[f"padj_{f}"].notna() & (t[f"padj_{f}"] < 0.05)
    if lfc_col is not None:
        ok &= t[lfc_col].notna() & (t[lfc_col].abs() > cutoff)
    return set(t.index[ok])


LN_CUTOFF = 1.5 / math.log(2)  # |ln fold change| > 1.5, expressed on DESeq2's log2 scale
