#!/usr/bin/env python3
"""bix-27-q2 origin check (E5B-CHANGES-3; written after the key and the reference notebook were read).

Rebuilds the notebook's procedure (cells 22-30, 44, 55-56, 64, 71) as closely as the capsule allows:
  samples: drop every projid duplicated in the metadata and every expression column not in the metadata
    (the ".1" copies), leaving 178; values log10(x + 1); samples as rows;
  50 iterations: train_test_split(test_size=0.3, random_state=np.random.randint(1000)); Ward clustering (3) of the
    training set; LogisticRegression() fitted on it; predictions for the training and the test samples;
  consensus matrices (share of iterations two samples, both present, got the same predicted label) for the
    training predictions and the test predictions; each matrix clustered by Ward (3) using its rows as features;
  value: samples whose training and test consensus labels are equal as raw labels (the notebook's count, 173);
    also given after Hungarian matching of the labels.
The notebook seeds nothing, and earlier cells draw from numpy's global generator, so its exact splits cannot be
recovered; this script runs the procedure under ten global seeds (np.random.seed 0-9) to show the spread.
Usage: bix-27-q2-origin.py <data_root>
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"

import glob  # noqa: E402
import json  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402
from sklearn.cluster import AgglomerativeClustering  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402

d = Path(glob.glob(str(Path(sys.argv[1]) / "bix-27" / "CapsuleData-*"))[0])
meta = pd.read_csv(d / "ROSMAP_meta_ad.csv")
expr = pd.read_csv(d / "ROSMAP_genexp_ad.csv", index_col=0)
dup = meta[meta.duplicated(subset=["projid"])]["projid"]
not_meta = [c for c in expr.columns if c not in set(meta["projid"])]
expr = expr.drop(columns=[c for c in expr.columns if c in set(dup)] + not_meta)
X = np.log10(expr + 1).T
assert X.shape[0] == 178, X.shape
K = 3


def consensus(labels: pd.DataFrame) -> pd.DataFrame:
    v = labels.to_numpy(dtype=float)
    ok = ~np.isnan(v)
    same = np.zeros((len(v), len(v)))
    tog = np.zeros((len(v), len(v)))
    for j in range(v.shape[1]):
        m = ok[:, j]
        tog[np.ix_(m, m)] += 1
        col = v[:, j]
        same[np.ix_(m, m)] += col[m][:, None] == col[m][None, :]
    share = np.divide(same, tog, out=np.zeros_like(same), where=tog > 0)
    return pd.DataFrame(share, index=labels.index, columns=labels.index)


out = {}
for seed in range(10):
    np.random.seed(seed)
    trp, tep = [], []
    for b in range(50):
        tr, te = train_test_split(X.index, test_size=0.3, random_state=np.random.randint(1000))
        lab = AgglomerativeClustering(n_clusters=K).fit_predict(X.loc[tr])
        clf = LogisticRegression().fit(X.loc[tr], lab)
        trp.append(pd.Series(clf.predict(X.loc[tr]), index=tr, name=b))
        tep.append(pd.Series(clf.predict(X.loc[te]), index=te, name=b))
    trp, tep = pd.concat(trp, axis=1), pd.concat(tep, axis=1)
    ct, ce = consensus(trp), consensus(tep)
    lt = pd.Series(AgglomerativeClustering(n_clusters=K).fit_predict(ct), index=ct.index)
    le = pd.Series(AgglomerativeClustering(n_clusters=K).fit_predict(ce), index=ce.index)
    both = lt.index.intersection(le.index)
    raw = int((lt[both] == le[both]).sum())
    m = np.zeros((K, K))
    for a, b in zip(le[both], lt[both]):
        m[a, b] += 1
    r, c = linear_sum_assignment(-m)
    matched = int(m[r, c].sum())
    out[f"origin-seed{seed}"] = {"value": raw, "unit": "count", "matched_labels": matched, "samples_in_both": int(len(both)),
                                 "train_consensus_sizes": np.bincount(lt, minlength=K).tolist(), "added": "after key",
                                 "defensible": "origin evidence"}
print(json.dumps({"question_id": "bix-27-q2", "origin": True, "readings": out, "meta": {"samples": int(X.shape[0])}},
                 sort_keys=True))
