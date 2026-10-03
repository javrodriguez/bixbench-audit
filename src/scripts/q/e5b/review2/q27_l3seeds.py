# r2 probe: pre-registered bix-27-q2 reading L3-Q1-K1-S1 (complete linkage, values as given, mode-of-matched-labels)
# run over more default_rng seeds; code copied from src/scripts/q/e5b/bix-27-q2.py
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS"): os.environ[_v]="1"
import glob, json, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import AgglomerativeClustering
from sklearn.linear_model import LogisticRegression
f = glob.glob(str(Path(sys.argv[1]) / "bix-27" / "CapsuleData-*" / "ROSMAP_genexp_ad.csv"))[0]
X = pd.read_csv(f, index_col=0).T.to_numpy(dtype=float)
n=X.shape[0]; K,ITER,NTRAIN=3,50,int(n*0.7)
hc=lambda X,l: AgglomerativeClustering(n_clusters=K, linkage=l).fit_predict(X)
def match(lab, ref):
    m=np.zeros((K,K))
    for a,b in zip(lab,ref): m[a,b]+=1
    r,c=linear_sum_assignment(-m); mp=dict(zip(r,c)); return np.array([mp[a] for a in lab])
mode=lambda v: int(np.bincount(np.array(v),minlength=K).argmax())
link=sys.argv[2]; ref=hc(X,link); res={}
for seed in [int(s) for s in sys.argv[3].split(",")]:
    rng=np.random.default_rng(seed); tr_lab=[[] for _ in range(n)]; te_lab=[[] for _ in range(n)]
    for _ in range(ITER):
        perm=rng.permutation(n); tr,te=perm[:NTRAIN],perm[NTRAIN:]
        lab=match(hc(X[tr],link),ref[tr])
        for i,l in zip(tr,lab): tr_lab[i].append(int(l))
        if len(set(lab))<2: continue
        pred=LogisticRegression(max_iter=5000).fit(X[tr],lab).predict(X[te])
        for i,l in zip(te,pred): te_lab[i].append(int(l))
    both=[i for i in range(n) if tr_lab[i] and te_lab[i]]
    res[seed]=sum(mode(tr_lab[i])==mode(te_lab[i]) for i in both)
    print(seed,res[seed],flush=True)
v=list(res.values()); print(json.dumps({"link":link,"values":res,"in_key":sum(160<=x<=180 for x in v),"n":len(v)}))
