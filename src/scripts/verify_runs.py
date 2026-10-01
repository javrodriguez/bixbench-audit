#!/usr/bin/env python3
"""Checks after the recorded run (CHANGES-5).

1. Determinism: every job's output (and every fit table) is byte-identical between r1 and r2.
2. Cross-environment equality with the pilot (the Mac's Homebrew R and uv Python), reading by reading, where the
   same reading exists in both: bix-2-q1, bix-7-q1 (same scripts); bix-36-q1 (pilot keys = v2's Z1 keys);
   bix-13-q1 (pilot key D-M-L-F = recorded key D-M-L-C1-F-N1). Floats must agree to 1e-9 relative.
   Same package versions in both, so this checks the pipeline and the install, not version sensitivity.
Usage: verify_runs.py <run_dir> <pilot_sealed_dir>
"""
import json
import math
import sys
from pathlib import Path

run, pilot = Path(sys.argv[1]), Path(sys.argv[2])
bad = 0
EXPECTED = ["bix-2-q1", "bix-2-q2", "bix-7-q1", "bix-36-q1", "bix-36-q3", "bix-13-q1", "bix-13-q2",
            "bix-3-q1", "bix-3-q2", "bix-3-q3", "fit-bix-13", "prep-bix-3", "fit-bix-3"]
for rep in ("r1", "r2"):
    missing = [n for n in EXPECTED if not (run / rep / f"{n}.json").exists()]
    missing += [d for d in ("fits-bix13", "fits-bix3") if not (run / rep / d).is_dir()]
    bad += bool(missing)
    print(f"completeness {rep}: {'all present' if not missing else 'MISSING ' + ', '.join(missing)}")
names = sorted({p.name for p in (run / "r1").glob("*.json")} | {p.name for p in (run / "r2").glob("*.json")})
for n in names:
    a, b = run / "r1" / n, run / "r2" / n
    same = a.exists() and b.exists() and a.read_bytes() == b.read_bytes()
    bad += not same
    print(f"determinism {n}: {'identical' if same else 'DIFFERENT OR MISSING'}")
for fdir in sorted({p.name for p in (run / "r1").glob("fits-*") if p.is_dir()}):
    fa, fb = run / "r1" / fdir, run / "r2" / fdir
    diff = [f.name for f in sorted(fa.iterdir()) if not (fb / f.name).exists() or f.read_bytes() != (fb / f.name).read_bytes()]
    diff += [f.name for f in sorted(fb.iterdir()) if not (fa / f.name).exists()] if fb.is_dir() else ["r2 folder missing"]
    bad += bool(diff)
    print(f"determinism {fdir}: {'identical' if not diff else 'DIFFERENT ' + ', '.join(diff[:5])}")


def close(x, y) -> bool:
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    return x == y


MAPS = {
    "bix-2-q1": lambda k: k,
    "bix-7-q1": lambda k: k,
    "bix-36-q1": lambda k: k,
    "bix-13-q1": lambda k: "-".join(k.split("-")[:3] + ["C1", k.split("-")[3], "N1"]),
}
for qid, fmap in MAPS.items():
    pf, rf = pilot / f"{qid}.run1.json", run / "r1" / f"{qid}.json"
    if not (pf.exists() and rf.exists()):
        print(f"cross-env {qid}: not available")
        continue
    p = json.loads(pf.read_text())["readings"]
    r = json.loads(rf.read_text())["readings"]
    mism = [k for k, v in p.items() if isinstance(v, dict) and "value" in v
            and (fmap(k) not in r or not close(v["value"], r[fmap(k)]["value"]))]
    bad += bool(mism)
    print(f"cross-env {qid}: {len(p) - len(mism)} of {len(p)} pilot readings equal"
          + (f"; differ: {mism[:6]}" if mism else ""))
print("ALL CHECKS PASS" if not bad else f"{bad} CHECK(S) FAILED")
sys.exit(1 if bad else 0)
