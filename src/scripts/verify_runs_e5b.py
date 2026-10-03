#!/usr/bin/env python3
"""Checks after the E5b recorded run (E5B-PREREG-2026-10-01.md, Method: Determinism).

Usage: verify_runs_e5b.py <run_dir> <fit_root> [comma-separated job names]   (the origin run passes its own list)
1. Completeness: every expected output exists in r1 and r2, each with exit 0 in log.txt and valid JSON with readings.
2. Determinism: r1 and r2 byte-identical for every output and for every fit-table listing; the intermediate fit
   files under <fit_root>/r1 and r2 byte-identical, file by file.
"""
import json
import sys
from pathlib import Path

run, fits = Path(sys.argv[1]), Path(sys.argv[2])
EXPECTED = ["bix-7-q3", "bix-14-q2", "bix-13-q3", "bix-37-q2", "bix-52-q3", "bix-36-q5", "fit-bix-53", "bix-53-q3",
            "bix-30-q5", "prep-bix-3", "fit-bix-3-q4", "bix-3-q4", "bix-27-q2"]
if len(sys.argv) > 3:
    EXPECTED = sys.argv[3].split(",")
QUESTIONS = [n for n in EXPECTED if n.startswith("bix-") or (n.startswith("origin-bix") and "fit" not in n)]
bad = 0
log = (run / "log.txt").read_text() if (run / "log.txt").exists() else ""
for n in EXPECTED:
    a, b = run / "r1" / f"{n}.json", run / "r2" / f"{n}.json"
    ok = a.exists() and b.exists() and a.read_bytes() == b.read_bytes()
    exits = [ln for ln in log.splitlines() if ln.startswith(f"{n} rep=")]
    ok = ok and len(exits) == 2 and all(" exit=0 " in ln for ln in exits)
    if ok and n in QUESTIONS:
        try:
            ok = bool(json.loads(a.read_text())["readings"])
        except (ValueError, KeyError):
            ok = False
    bad += not ok
    print(f"{n}: {'identical r1 = r2, exit 0 twice' if ok else 'MISSING, FAILED OR DIFFERENT'}")
for lst in sorted((run / "r1").glob("fits-*.sha256")):
    other = run / "r2" / lst.name
    same = other.exists() and other.read_bytes() == lst.read_bytes()
    bad += not same
    print(f"{lst.name}: {'identical' if same else 'DIFFERENT OR MISSING'}")
fa, fb = fits / "r1", fits / "r2"
files = sorted(p.relative_to(fa) for p in fa.rglob("*") if p.is_file())
other = sorted(p.relative_to(fb) for p in fb.rglob("*") if p.is_file())
diff = [str(p) for p in files if not (fb / p).exists() or (fa / p).read_bytes() != (fb / p).read_bytes()]
diff += [str(p) for p in other if not (fa / p).exists()]
bad += bool(diff) or not files
print(f"intermediate files: {len(files)} in r1, {len(other)} in r2, "
      f"{'all identical' if not diff and files else 'DIFFERENT ' + ', '.join(diff[:5])}")
print("ALL CHECKS PASS" if not bad else f"{bad} CHECK(S) FAILED")
sys.exit(1 if bad else 0)
