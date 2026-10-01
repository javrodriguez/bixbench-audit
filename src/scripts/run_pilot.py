#!/usr/bin/env python3
"""Run the pilot sealed (addendum 2, section 2; review round 3 fixes in prereg/CHANGES-3.md).

1. Refuses to start unless every capsule zip matches its pinned sha256 (addendum 2, section 7).
2. Writes a sha256 over each extracted CapsuleData tree, and the Python and R environments, into the run folder.
3. Runs each frozen question script twice; writes each output to <run>/sealed/<qid>.run<N>.json, made read-only;
   prints only the exit status, the sha256 of each run and whether the two runs match.
4. The positive control bix-8-q6 is reported as pass or fail with its two public numbers only.
Values stay unread until Javier's pick is frozen as addendum 3.
Usage: run_pilot.py <run_dir>
"""
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent
RUN = Path(sys.argv[1])
DATA = RUN / "data"
PINNED = {
    "bix-13": "6b29bb5d03693e4098452042ae0169a98926d45ce6ca26b0a45682c8feb7039f",
    "bix-2": "7f9234d46d92985574164c53b3c62d39fa53dd06f8c10b1dbfb13652dc353be1",
    "bix-3": "41706da9f999eb4d02544c02e960f3fe8da0d0e3e0c18cfc95047e59924607d6",
    "bix-36": "2f254fd09c1e05bc0eb876dd7395e39f2af07b9cd92f643ce0c80288e8c24f6c",
    "bix-39": "be410226ac353bf8afada3e1226f163d374a5d3ffb5ce33560ee312363ba16a2",
    "bix-7": "9852ea865a9b394cf0c14469074493f49f8ae79e610fd89ed55b39e4d185e7b4",
    "bix-8": "6d0bcc4502eb25118564315573a132931d2b8a662e71b21d9b374bd59a884cf8",
    "bix-9": "afcdc39731ec0895aea70e77c06f8750f1629e263b0211be595a7e2d485f8747",
}
PY = ["uv", "run", "--no-project", "--python", "3.12", "--with", "pandas==2.2.3", "--with", "openpyxl==3.1.5",
      "--with", "numpy==2.1.3", "--with", "scipy==1.14.1", "python", "-P"]
Q = LANE / "scripts" / "q"
NORM = RUN / "derived" / "bix-3_normcount.csv"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# 1. pinned zips
for line in (RUN / "inputs.sha256").read_text().splitlines():
    digest, rel, short = line.split()
    got = sha((RUN / rel).read_bytes())
    if got != digest or PINNED[short] != digest:
        sys.exit(f"REFUSED: {rel} sha256 {got} does not match its pin")
print("zips: all pinned hashes match", flush=True)

# 2. data trees and environments
trees = []
for short in sorted(PINNED):
    root = DATA / short
    files = sorted(p for p in root.rglob("*") if p.is_file())
    listing = "".join(f"{sha(p.read_bytes())}  {p.relative_to(root)}\n" for p in files)
    trees.append(f"{sha(listing.encode())}  {short}  files={len(files)}")
(RUN / "data-trees.sha256").write_text("\n".join(trees) + "\n")
py_env = subprocess.run(PY + ["-c", "import importlib.metadata as m, platform, sys; "
                              "print(sys.version); print(platform.platform()); "
                              "print('\\n'.join(sorted(f\"{d.metadata['Name']}=={d.version}\" for d in m.distributions())))"],
                        capture_output=True, text=True, check=True)
(RUN / "env-python.txt").write_text(py_env.stdout)
r_env = subprocess.run(["Rscript", "-e", "suppressPackageStartupMessages({library(DESeq2); library(apeglm); library(jsonlite)}); "
                        "print(sessionInfo())"], capture_output=True, text=True, check=True)
(RUN / "env-r.txt").write_text(r_env.stdout)
print("trees and environments recorded", flush=True)

# 3. sealed runs
JOBS = [
    ("bix-8-q6", PY + [str(Q / "bix-8-q6.py"), str(DATA)]),
    ("bix-3-prep", PY + [str(Q / "bix-3-prep.py"), str(DATA), str(NORM)]),
    ("bix-2-q1", PY + [str(Q / "bix-2-q1.py"), str(DATA)]),
    ("bix-7-q1", PY + [str(Q / "bix-7-q1.py"), str(DATA)]),
    ("bix-36-q1", PY + [str(Q / "bix-36-q1.py"), str(DATA)]),
    ("bix-13-q1", ["Rscript", str(Q / "bix-13-q1.R"), str(DATA)]),
    ("bix-3-q1", ["Rscript", str(Q / "bix-3-q1.R"), str(NORM)]),
]
sealed = RUN / "sealed"
sealed.mkdir(parents=True, exist_ok=True)
log = []
for qid, cmd in JOBS:
    digests = []
    for n in (1, 2):
        p = subprocess.run(cmd, capture_output=True, text=True)
        out = sealed / f"{qid}.run{n}.json"
        err = sealed / f"{qid}.run{n}.stderr"
        out.write_text(p.stdout)
        err.write_text(p.stderr)
        for f in (out, err):
            os.chmod(f, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        digests.append(sha(p.stdout.encode()))
        log.append(f"{qid} run{n} exit={p.returncode} sha256={digests[-1]} cmd={' '.join(cmd)}")
        print(f"{qid} run{n} exit={p.returncode} sha256={digests[-1]}", flush=True)
        if qid == "bix-8-q6" and n == 1:
            ok = p.returncode == 0
            r = json.loads(p.stdout)["readings"] if p.stdout.strip() else {}
            rows = r.get("R-rows", {}).get("value")
            genes = r.get("R-genes", {}).get("value")
            print(f"POSITIVE CONTROL {'PASS' if ok else 'FAIL'}: records={rows} distinct_gene_id={genes}", flush=True)
    print(f"{qid} identical_runs={digests[0] == digests[1]}", flush=True)
(RUN / "sealed.log").write_text("\n".join(log) + "\n")
