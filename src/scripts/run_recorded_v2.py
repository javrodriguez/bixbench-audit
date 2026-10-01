#!/usr/bin/env python3
"""Recorded run for the ten A′ questions (CHANGES-4, CHANGES-4b, CHANGES-5), one stage and one repetition per call.

Usage: run_recorded_v2.py <run_dir> <data_dir> <env_prefix> <stage> <rep> [manifest]   (manifest: CHANGES-7)
  stage: chip (bix-2-q1, bix-2-q2, bix-7-q1) | bix36 (bix-36-q1 v2, bix-36-q3) | bix13 (fit, q1, q2)
         | bix3 (prep, fit, q1-q3)
  rep: 1 or 2 (each repetition recomputes everything from the capsule data, fits included)
Refuses to start unless: every file in prereg/SCRIPTS-5.sha256 matches; the question file and the lockfile match
their pins; every capsule zip matches its pin; every extracted data tree matches the pilot's record; and this
stage's outputs for this repetition do not already exist.
Every job runs isolated from user libraries (R --vanilla with R_LIBS_USER pointed at a missing folder; Python -s).
Every command, exit status and output hash is appended to <run_dir>/log.txt; environments go to <run_dir>/r<rep>/.
"""
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

LANE = Path(__file__).resolve().parent.parent
Q = LANE / "scripts" / "q"
RUN, DATA, ENV, STAGE, REP = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]
assert STAGE in ("chip", "bix36", "bix13", "bix3") and REP in ("1", "2")
PINS = {
    LANE / "inputs" / "BixBench.jsonl": "0d1204dcdae7193a9132ced5a3502008f6b3b163debc1b65b2aa2d86cb132dc9",
    LANE / "envlock" / "conda-lock.txt": "ef64e570a912d533554dff4f6db8cbbae21bf31245268bf93fd294afa270e46f",
}
PY = [str(ENV / "bin" / "python"), "-s", "-P"]
RS = [str(ENV / "bin" / "Rscript"), "--vanilla"]
OUT = RUN / f"r{REP}"
PILOT = DATA.parent


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def refuse(msg: str) -> None:
    sys.exit(f"REFUSED: {msg}")


def log(line: str) -> None:
    with (RUN / "log.txt").open("a") as f:
        f.write(line + "\n")
    print(line, flush=True)


MANIFEST = sys.argv[6] if len(sys.argv) > 6 else "SCRIPTS-5.sha256"  # CHANGES-7: bix-3 reruns use SCRIPTS-7
for line in (LANE / "prereg" / MANIFEST).read_text().splitlines():
    digest, rel = line.split()
    if sha((LANE / rel).read_bytes()) != digest:
        refuse(f"{rel} differs from {MANIFEST}")
for path, digest in PINS.items():
    if sha(path.read_bytes()) != digest:
        refuse(f"{path.name} differs from its pin")
for line in (PILOT / "inputs.sha256").read_text().splitlines():
    digest, rel, short = line.split()
    if sha((PILOT / rel).read_bytes()) != digest:
        refuse(f"{rel} does not match its pinned hash")
for line in (PILOT / "data-trees.sha256").read_text().splitlines():
    digest, short, _ = line.split()
    root = DATA / short
    files = sorted(p for p in root.rglob("*") if p.is_file())
    listing = "".join(f"{sha(p.read_bytes())}  {p.relative_to(root)}\n" for p in files)
    if sha(listing.encode()) != digest:
        refuse(f"data tree {short} differs from the pilot's record")

fits = OUT / f"fits-{STAGE}"
norm = OUT / "bix-3_normcount.csv"
JOBS = {
    "chip": [("bix-2-q1", PY + [str(Q / "bix-2-q1.py"), str(DATA)]),
             ("bix-2-q2", PY + [str(Q / "bix-2-q2.py"), str(DATA)]),
             ("bix-7-q1", PY + [str(Q / "bix-7-q1.py"), str(DATA)])],
    "bix36": [("bix-36-q1", PY + [str(Q / "bix-36-q1-v2.py"), str(DATA)]),
              ("bix-36-q3", PY + [str(Q / "bix-36-q3.py"), str(DATA)])],
    "bix13": [("fit-bix-13", RS + [str(Q / "bix-13-fit.R"), str(DATA), str(fits)]),
              ("bix-13-q1", PY + [str(Q / "bix-13-q1.py"), str(fits)]),
              ("bix-13-q2", PY + [str(Q / "bix-13-q2.py"), str(fits)])],
    "bix3": [("prep-bix-3", PY + [str(Q / "bix-3-prep.py"), str(DATA), str(norm)]),
             ("fit-bix-3", RS + [str(Q / ("bix-3-fit.R" if MANIFEST == "SCRIPTS-5.sha256" else "bix-3-fit-v2.R")),
                                 str(norm), str(fits)]),
             ("bix-3-q1", PY + [str(Q / "bix-3-q1.py"), str(fits)]),
             ("bix-3-q2", PY + [str(Q / "bix-3-q2.py"), str(fits)]),
             ("bix-3-q3", PY + [str(Q / "bix-3-q3.py"), str(fits)])],
}[STAGE]
if fits.exists() or any((OUT / f"{n}.json").exists() for n, _ in JOBS):
    refuse(f"stage {STAGE} rep {REP} already has outputs in {OUT}; use a fresh run folder")
OUT.mkdir(parents=True, exist_ok=True)

ENVVARS = {k: v for k, v in os.environ.items() if not k.startswith(("R_", "PYTHON"))}
ENVVARS.update({"R_LIBS_USER": str(ENV / "no-user-lib"), "R_LIBS": "", "R_PROFILE_USER": "/dev/null",
                "R_ENVIRON_USER": "/dev/null", "PYTHONNOUSERSITE": "1", "LC_ALL": "C", "TZ": "America/New_York"})
if not (OUT / "env-r.txt").exists():
    r = subprocess.run(RS + ["-e", "suppressPackageStartupMessages({library(DESeq2); library(apeglm)}); "
                         "print(.libPaths()); print(sessionInfo())"], capture_output=True, text=True, env=ENVVARS)
    (OUT / "env-r.txt").write_text(r.stdout + r.stderr)
    p = subprocess.run(PY + ["-c", "import importlib.metadata as m, platform, sys; print(sys.version); "
                             "print(platform.platform()); print(sys.path); "
                             "print('\\n'.join(sorted(f\"{d.metadata['Name']}=={d.version}\" for d in m.distributions())))"],
                       capture_output=True, text=True, env=ENVVARS)
    (OUT / "env-python.txt").write_text(p.stdout + p.stderr)
log(f"{time.strftime('%Y-%m-%d %H:%M:%S %Z')} stage={STAGE} rep={REP} all inputs, scripts and pins verified env={ENV}")

for name, cmd in JOBS:
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, env=ENVVARS)
    (OUT / f"{name}.json").write_text(p.stdout)
    (OUT / f"{name}.stderr").write_text(p.stderr)
    log(f"{name} rep={REP} exit={p.returncode} secs={time.time() - t0:.0f} sha256={sha(p.stdout.encode())} "
        f"cmd={' '.join(cmd)}")
    if p.returncode != 0:
        refuse(f"{name} failed; see {OUT / (name + '.stderr')}")
if fits.exists():
    listing = "".join(f"{sha(f.read_bytes())}  {f.name}\n" for f in sorted(fits.iterdir()))
    (OUT / f"fits-{STAGE}.sha256").write_text(listing)
    log(f"fits-{STAGE} rep={REP} tables={len(list(fits.iterdir()))} sha256={sha(listing.encode())}")
