#!/usr/bin/env python3
"""bix-27-q2 (E5b). Readings named from the question's words before any run and before the key was read; unit: count.

Needs scikit-learn: runs in the E5b Python environment (envlock/e5b-py-lock.txt). Threads are pinned to 1.
Data: ROSMAP_genexp_ad.csv (genes in rows, samples in columns); the samples are clustered.
Fixed by the words: hierarchical clustering into 3 clusters; 50 iterations; 70/30 train-test splits; logistic
regression predicts the test samples' labels from the training clusters.
The words fix no seed, linkage, scaling or label-matching, so each is a reading:
  L, linkage: L1 Ward (Euclidean); L2 average (Euclidean); L3 complete (Euclidean).
  Q, scaling: Q1 the values as given; Q2 each gene z-scored over all samples.
  R, the seed of the 50 splits: R1 0; R2 42; R3 2024 (numpy default_rng; split i is a permutation of the samples,
     the first 70% (rounded down) training).
Procedure, the same for every reading (one standard construction; the words do not specify the rest):
  cluster labels from each iteration are matched to the clustering of all samples by the same linkage
  (Hungarian matching on the training samples), so labels mean the same thing across iterations;
  logistic regression (scikit-learn defaults: L2, C = 1, lbfgs, max_iter raised to 5000) is fitted on the training
  samples' matched labels and predicts the test samples;
  a sample's training consensus is its most frequent matched label over the iterations where it was in training,
  its test consensus the most frequent predicted label over the iterations where it was in test (ties: lowest label);
  value (K1-S1): the number of samples with both consensuses that agree.
Added before any run by E5B-CHANGES-1 (pre-run review MINOR 10):
  K1-S2 "consistently" read strictly: samples whose matched training label is the same in every iteration where
     they were in training, whose predicted test label is the same in every iteration where they were in test,
     and the two agree.
  K2 co-association consensus (the usual meaning of "consensus clustering"): for training, the share of iterations
     in which two samples, both in training, got the same cluster; for test, the same over predicted labels when
     both were in test (pairs never together get share 0); each matrix is cut into 3 clusters by average linkage on
     1 - share; the test consensus is matched to the training consensus (Hungarian) and the agreeing samples among
     those seen in both are counted.
  The answer rests on seeds the words do not fix; readings R1-R3 disagreeing is evidence for "remove".
Usage: bix-27-q2.py <data_root>
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
from scipy.cluster.hierarchy import fcluster, linkage  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402
from scipy.spatial.distance import squareform  # noqa: E402
from sklearn.cluster import AgglomerativeClustering  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402

f = glob.glob(str(Path(sys.argv[1]) / "bix-27" / "CapsuleData-*" / "ROSMAP_genexp_ad.csv"))
assert len(f) == 1, f
g = pd.read_csv(f[0], index_col=0)
X0 = g.T.to_numpy(dtype=float)
assert np.isfinite(X0).all(), "non-finite expression values"
n = X0.shape[0]
sd = X0.std(axis=0)
Xz = (X0 - X0.mean(axis=0)) / np.where(sd > 0, sd, 1.0)
K, ITER, NTRAIN = 3, 50, int(n * 0.7)


def hc(X: np.ndarray, link: str) -> np.ndarray:
    return AgglomerativeClustering(n_clusters=K, linkage=link).fit_predict(X)


def match(lab: np.ndarray, ref: np.ndarray) -> np.ndarray:
    m = np.zeros((K, K))
    for a, b in zip(lab, ref):
        m[a, b] += 1
    r, c = linear_sum_assignment(-m)
    mp = dict(zip(r, c))
    return np.array([mp[a] for a in lab])


def mode(v: list) -> int:
    return int(np.bincount(np.array(v), minlength=K).argmax())


def coassoc_labels(same: np.ndarray, together: np.ndarray) -> np.ndarray:
    share = np.divide(same, together, out=np.zeros_like(same), where=together > 0)
    dist = 1.0 - share
    np.fill_diagonal(dist, 0.0)
    return fcluster(linkage(squareform(dist, checks=False), method="average"), t=K, criterion="maxclust") - 1


out = {}
for lk, link in (("L1", "ward"), ("L2", "average"), ("L3", "complete")):
    for qk, X in (("Q1", X0), ("Q2", Xz)):
        ref = hc(X, link)
        for rk, seed in (("R1", 0), ("R2", 42), ("R3", 2024)):
            rng = np.random.default_rng(seed)
            tr_lab = [[] for _ in range(n)]
            te_lab = [[] for _ in range(n)]
            tr_same, tr_tog = np.zeros((n, n)), np.zeros((n, n))
            te_same, te_tog = np.zeros((n, n)), np.zeros((n, n))
            skipped = 0
            for _ in range(ITER):
                perm = rng.permutation(n)
                tr, te = perm[:NTRAIN], perm[NTRAIN:]
                lab = match(hc(X[tr], link), ref[tr])
                for i, l in zip(tr, lab):
                    tr_lab[i].append(int(l))
                tr_tog[np.ix_(tr, tr)] += 1
                tr_same[np.ix_(tr, tr)] += lab[:, None] == lab[None, :]
                if len(set(lab)) < 2:
                    skipped += 1
                    continue
                clf = LogisticRegression(max_iter=5000).fit(X[tr], lab)
                pred = clf.predict(X[te])
                for i, l in zip(te, pred):
                    te_lab[i].append(int(l))
                te_tog[np.ix_(te, te)] += 1
                te_same[np.ix_(te, te)] += pred[:, None] == pred[None, :]
            both = [i for i in range(n) if tr_lab[i] and te_lab[i]]
            agree = sum(mode(tr_lab[i]) == mode(te_lab[i]) for i in both)
            strict = sum(len(set(tr_lab[i])) == 1 and len(set(te_lab[i])) == 1 and tr_lab[i][0] == te_lab[i][0]
                         for i in both)
            ctr, cte = coassoc_labels(tr_same, tr_tog), coassoc_labels(te_same, te_tog)
            cte_m = match(cte[both], ctr[both]) if both else np.array([], dtype=int)
            k2 = int(np.sum(cte_m == ctr[both])) if both else 0
            common = {"samples_with_both": len(both), "iterations_without_two_clusters": skipped,
                      "reference_cluster_sizes": np.bincount(ref, minlength=K).tolist()}
            out[f"{lk}-{qk}-{rk}-K1-S1"] = {"value": int(agree), "unit": "count", **common, "defensible": True}
            out[f"{lk}-{qk}-{rk}-K1-S2"] = {"value": int(strict), "unit": "count", **common, "defensible": True}
            out[f"{lk}-{qk}-{rk}-K2"] = {"value": k2, "unit": "count", **common,
                                         "consensus_sizes_train_test": [np.bincount(ctr, minlength=K).tolist(),
                                                                        np.bincount(cte, minlength=K).tolist()],
                                         "defensible": True}
print(json.dumps({"question_id": "bix-27-q2", "readings": out, "meta": {"samples": n, "genes": int(X0.shape[1])}},
                 sort_keys=True))
