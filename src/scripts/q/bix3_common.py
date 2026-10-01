"""Reads the shared bix-3 fit tables written by bix-3-fit.R (CHANGES-4)."""
from pathlib import Path

import pandas as pd

MODELS, PSEUDO, FILTERS = ("M1", "M2"), ("P1", "P2"), ("F1", "F2", "F3")
FILTERS_T = FILTERS + ("FT",)  # FT: DESeq2's test against |log2 fold change| > 1, for cut-off questions
N_GENES = 25402


def table(fit_dir: Path, cohort: str, m: str, p: str, contrast: str) -> pd.DataFrame:
    t = pd.read_csv(fit_dir / f"bix-3_{cohort}_{m}_{p}_{contrast}.csv", na_values=["NA"], keep_default_na=False,
                    float_precision="round_trip")
    assert len(t) == N_GENES and t["gene"].is_unique, (cohort, m, p, contrast, len(t))
    return t.set_index("gene")


def de(t: pd.DataFrame, f: str, lfc: float | None = None, base_min: float | None = None) -> set:
    ok = t[f"padj_{f}"].notna() & (t[f"padj_{f}"] < 0.05)
    if lfc is not None:
        ok &= t["lfc_mle"].abs() > lfc
    if base_min is not None:
        ok &= t["baseMean"] >= base_min
    return set(t.index[ok])
