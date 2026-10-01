"""bix-13-q1 near-key readings (CHANGES-15): adversarial review 6's script rerun under the lane's hashing. Lists every
JBX97-denominator reading between 9.5% and 11.7% in a set of bix-13 fit tables, with addendum 1's ROUND_HALF_UP rounding.
EVERY READING HERE WAS ADDED AFTER THE KEY WAS KNOWN; none enters the rubric. Usage: bix-13-near.py <fit_dir>"""
import itertools, math, sys, json
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
fit = sys.argv[1]
def T(d,m,s):
    t = pd.read_csv(f"{fit}/bix-13_{d}_{m}_{s}.csv", na_values=["NA"], keep_default_na=False, float_precision="round_trip")
    return t.set_index("gene")
TH = {"lin": math.log2(1.5), "l2": 1.5, "ln": 1.5/math.log(2)}
def de(t,f,col,th):
    ok = t[f"padj_{f}"].notna() & (t[f"padj_{f}"]<0.05)
    if col: ok &= t[col].notna() & (t[col].abs()>th)
    return set(t.index[ok])
out=[]; near=[]
for d,m in itertools.product(("D1","D2","D3"),("M1","M2")):
    t={s:T(d,m,s) for s in ("97","98","99")}
    for col,f in itertools.product(("lfc_mle","lfc_apeglm"),("F1","F2","F3")):
        for thk,th in TH.items():
            for r in range(4):
                for sub in itertools.combinations(("97","98","99"),r):
                    s={k:de(v,f,col if k in sub else None, th if k in sub else None) for k,v in t.items()}
                    for dirk in ("any","same"):
                        num=(s["97"]&s["99"])-s["98"]
                        if dirk=="same": num={g for g in num if (t["97"].at[g,col]>0)==(t["99"].at[g,col]>0)}
                        v=100*len(num)/len(s["97"])
                        hu=Decimal(repr(v)).quantize(Decimal("0.1"),rounding=ROUND_HALF_UP)
                        if 9.5<=v<11.7: near.append(dict(d=d,m=m,col=col,f=f,th=thk,sub="".join(sub) or "none",dir=dirk,n=len(num),den=len(s["97"]),v=round(v,4),halfup=str(hu)))
print(json.dumps(near,indent=0))
