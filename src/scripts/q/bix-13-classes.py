"""bix-13-q1 grid split by class (CHANGES-13): adversarial review 4's probe rerun under the lane's hashing. EVERY READING
HERE WAS ADDED AFTER THE KEY WAS KNOWN; none enters the rubric. Split of the CHANGES-12 1,728-reading grid
by whether JBX97's DE set carries the cut-off. Same loop as scripts/q/bix-13-exhaust.py."""
import itertools, json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bix13_common import DESIGNS, FILTERS, MODELS, de, table
fit = Path(sys.argv[1])
TH = {"lin": math.log2(1.5), "l2": 1.5, "ln": 1.5 / math.log(2)}
rows = []
for d, m in itertools.product(DESIGNS, MODELS):
    t = {s: table(fit, d, m, s) for s in ("97", "98", "99")}
    for col, f in itertools.product(("lfc_mle", "lfc_apeglm"), FILTERS):
        for thk, th in TH.items():
            for r in range(0, 4):
                for sub in itertools.combinations(("97", "98", "99"), r):
                    s = {k: de(v, f, col if k in sub else None, th if k in sub else None) for k, v in t.items()}
                    for dirk in ("any", "same"):
                        num = (s["97"] & s["99"]) - s["98"]
                        if dirk == "same":
                            num = {g for g in num if (t["97"].at[g, col] > 0) == (t["99"].at[g, col] > 0)}
                        rows.append(dict(d=d, m=m, col=col, f=f, th=thk, sub="".join(sub) or "none", dir=dirk,
                                         n=len(num), den=len(s["97"]), v=100 * len(num) / len(s["97"])))
out = {"n": len(rows)}
for name, pred in [("cut_on_97", lambda r: "97" in r["sub"]), ("no_cut_on_97", lambda r: "97" not in r["sub"]),
                   ("all_three_cut", lambda r: r["sub"] == "979899"), ("no_cut_anywhere", lambda r: r["sub"] == "none")]:
    sel = [r for r in rows if pred(r)]
    lo = min(sel, key=lambda r: r["v"]); hi = max(sel, key=lambda r: r["v"])
    out[name] = {"count": len(sel), "min": lo, "max": hi,
                 "below_16_9": sum(r["v"] < 16.9 for r in sel), "above_37_5": sum(r["v"] > 37.5 for r in sel),
                 "round_10_6": sum(round(r["v"], 1) == 10.6 for r in sel)}
print(json.dumps(out, indent=1))
