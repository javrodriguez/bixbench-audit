#!/usr/bin/env python3
"""Checks after the recorded run, across run folders (CHANGES-7; replaces verify_runs.py).

Usage: verify_runs_v2.py <pilot_sealed_dir> <run_dir> [<run_dir> ...]
Each output is taken from the LAST run folder listed that holds it in r1; its r1 and r2 must both be in that folder.
1. Completeness: every expected output and both fit folders, in r1 and r2 of the folder chosen for them.
2. Determinism: r1 and r2 byte-identical (outputs and every fit table, both ways).
3. Cross-environment equality with the pilot for bix-2-q1, bix-7-q1, bix-36-q1 (as-given readings) and bix-13-q1
   (pilot key D-M-L-F = recorded key D-M-L-C1-F-N1), floats to 1e-9 relative. Same package versions in both,
   so this checks the pipeline and the install, not version sensitivity.
"""
import json
import math
import sys
from pathlib import Path

pilot, runs = Path(sys.argv[1]), [Path(p) for p in sys.argv[2:]]
EXPECTED = ["bix-2-q1", "bix-2-q2", "bix-7-q1", "bix-36-q1", "bix-36-q3", "bix-13-q1", "bix-13-q2",
            "bix-3-q1", "bix-3-q2", "bix-3-q3", "fit-bix-13", "prep-bix-3", "fit-bix-3"]
FITS = ["fits-bix13", "fits-bix3"]
bad = 0


def home(name: str, is_dir: bool = False) -> Path | None:
    for r in reversed(runs):
        p = r / "r1" / (name if is_dir else f"{name}.json")
        if (p.is_dir() if is_dir else p.exists()):
            return r
    return None


for n in EXPECTED:
    h = home(n)
    ok = h is not None and (h / "r2" / f"{n}.json").exists()
    same = ok and (h / "r1" / f"{n}.json").read_bytes() == (h / "r2" / f"{n}.json").read_bytes()
    bad += not same
    print(f"{n}: folder {h.name if h else '-'}: {'identical r1 = r2' if same else 'MISSING OR DIFFERENT'}")
for fdir in FITS:
    h = home(fdir, is_dir=True)
    if h is None or not (h / "r2" / fdir).is_dir():
        bad += 1
        print(f"{fdir}: MISSING")
        continue
    fa, fb = h / "r1" / fdir, h / "r2" / fdir
    diff = [f.name for f in sorted(fa.iterdir()) if not (fb / f.name).exists() or f.read_bytes() != (fb / f.name).read_bytes()]
    diff += [f.name for f in sorted(fb.iterdir()) if not (fa / f.name).exists()]
    bad += bool(diff)
    print(f"{fdir}: folder {h.name}: {len(list(fa.iterdir()))} tables, "
          f"{'identical r1 = r2' if not diff else 'DIFFERENT ' + ', '.join(diff[:5])}")


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
    h = home(qid)
    pf = pilot / f"{qid}.run1.json"
    if h is None or not pf.exists():
        bad += 1
        print(f"cross-env {qid}: NOT AVAILABLE")
        continue
    p = json.loads(pf.read_text())["readings"]
    r = json.loads((h / "r1" / f"{qid}.json").read_text())["readings"]
    mism = [k for k, v in p.items() if isinstance(v, dict) and "value" in v
            and (fmap(k) not in r or not close(v["value"], r[fmap(k)]["value"]))]
    bad += bool(mism)
    print(f"cross-env {qid}: {len(p) - len(mism)} of {len(p)} pilot readings equal"
          + (f"; differ: {mism[:6]}" if mism else ""))
print("ALL CHECKS PASS" if not bad else f"{bad} CHECK(S) FAILED")
sys.exit(1 if bad else 0)
