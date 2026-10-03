#!/usr/bin/env python3
"""E5b recorded run, one stage and one repetition per call (E5B-PREREG-2026-10-01.md, Method).

Usage: run_e5b.py <run_dir> <data_dir> <fit_root> <conda_env> <py_env> <stage> <rep> [manifest]
  manifest: the prereg hash list to check (default E5B-SCRIPTS-1.sha256; E5B-CHANGES-2 uses E5B-SCRIPTS-2.sha256)
  data_dir: holds data/<short_id>/, inputs.sha256 (zips), data-trees.sha256 and annot/ with annot.sha256
  fit_root: where intermediate fit tables go (outside git); their hashes are logged into run_dir
  stage: light (bix-7-q3, bix-14-q2, bix-13-q3, bix-37-q2, bix-52-q3, bix-36-q5, bix-53 fit and q3, bix-30-q5)
         | bix3 (prep with E5a's frozen bix-3-prep.py, the fit, q4) | bix27 (bix-27-q2)
         | origin (E5B-CHANGES-3: origin checks and probes after the keys and notebooks were read; reads the
           recorded bix-3 fit tables of the same repetition)
  rep: 1 or 2 (each recomputes everything from the capsule data)
Refuses to start unless every file in prereg/E5B-SCRIPTS-1.sha256 matches; the question file, the conda lockfile and
the E5b Python lockfile match their pins; every capsule zip matches inputs.sha256 (and ADDENDUM-2's pin where E5a
pinned it); every data tree matches data-trees.sha256; every annotation file matches annot.sha256; and this stage's
outputs for this repetition do not exist yet.
R runs --vanilla with user libraries isolated; Python runs -s -P; LC_ALL=C.
"""
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
Q = SRC / "scripts" / "q"
E = Q / "e5b"
RUN, DATA, FITROOT, ENV, PYENV, STAGE, REP = (Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]),
                                              Path(sys.argv[4]), Path(sys.argv[5]), sys.argv[6], sys.argv[7])
assert STAGE in ("light", "bix3", "bix27", "origin") and REP in ("1", "2")
MANIFEST = sys.argv[8] if len(sys.argv) > 8 else "E5B-SCRIPTS-1.sha256"
PINS = {
    SRC / "inputs" / "BixBench.jsonl": "0d1204dcdae7193a9132ced5a3502008f6b3b163debc1b65b2aa2d86cb132dc9",
    SRC / "envlock" / "conda-lock.txt": "ef64e570a912d533554dff4f6db8cbbae21bf31245268bf93fd294afa270e46f",
}
E5A_ZIPS = {  # ADDENDUM-2 section 7
    "bix-13": "6b29bb5d03693e4098452042ae0169a98926d45ce6ca26b0a45682c8feb7039f",
    "bix-3": "41706da9f999eb4d02544c02e960f3fe8da0d0e3e0c18cfc95047e59924607d6",
    "bix-36": "2f254fd09c1e05bc0eb876dd7395e39f2af07b9cd92f643ce0c80288e8c24f6c",
    "bix-7": "9852ea865a9b394cf0c14469074493f49f8ae79e610fd89ed55b39e4d185e7b4",
}
PY = [str(ENV / "bin" / "python"), "-s", "-P"]
PY2 = [str(PYENV / "bin" / "python"), "-s", "-P"]
RS = [str(ENV / "bin" / "Rscript"), "--vanilla"]
OUT = RUN / f"r{REP}"
FITS = FITROOT / f"r{REP}"
D = DATA / "data"
ANN = DATA / "annot"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def refuse(msg: str) -> None:
    sys.exit(f"REFUSED: {msg}")


def log(line: str) -> None:
    with (RUN / "log.txt").open("a") as f:
        f.write(line + "\n")
    print(line, flush=True)


for line in (SRC / "prereg" / MANIFEST).read_text().splitlines():
    digest, rel = line.split()
    if sha((SRC.parent / rel).read_bytes()) != digest:
        refuse(f"{rel} differs from {MANIFEST}")
for path, digest in PINS.items():
    if sha(path.read_bytes()) != digest:
        refuse(f"{path.name} differs from its pin")
manifest = {line.split()[1] for line in (SRC / "prereg" / MANIFEST).read_text().splitlines()}
NEED = {"src/envlock/e5b-py-lock.txt", "src/scripts/run_e5b.py", "src/scripts/verify_runs_e5b.py",
        "src/scripts/q/chip_common.py", "src/scripts/q/bix-3-prep.py", "src/scripts/compare_e5b.py"}
NEED |= {f"src/scripts/q/e5b/{p.name}" for p in E.iterdir() if p.suffix in (".py", ".R")}
if (E / "origin").is_dir():
    NEED |= {f"src/scripts/q/e5b/origin/{p.name}" for p in (E / "origin").iterdir() if p.suffix in (".py", ".R")}
if not NEED <= manifest:
    refuse(f"not in E5B-SCRIPTS-1.sha256: {sorted(NEED - manifest)}")
# The data-side hash lists live outside git; their own hashes are frozen in prereg/E5B-DATA.sha256 (E5B-CHANGES-1).
for line in (SRC / "prereg" / "E5B-DATA.sha256").read_text().splitlines():
    digest, name = line.split()
    f = DATA / name
    if not f.exists() or sha(f.read_bytes()) != digest:
        refuse(f"{name} is missing or differs from E5B-DATA.sha256")
# The conda environment must hold exactly the lockfile's packages (one conda-meta record per lockfile URL).
urls = [ln for ln in (SRC / "envlock" / "conda-lock.txt").read_text().splitlines() if ln.startswith("http")]
stems = {u.rsplit("/", 1)[1].split("#")[0].removesuffix(".conda").removesuffix(".tar.bz2") for u in urls}
have = {p.stem for p in (ENV / "conda-meta").glob("*.json")}
if stems != have:
    refuse(f"the conda environment differs from conda-lock.txt: {sorted(stems ^ have)[:6]}")
want = {}
for line in (SRC / "envlock" / "e5b-py-lock.txt").read_text().splitlines():
    if line and not line[0].isspace() and "==" in line:
        name, ver = line.split()[0].split("==")
        want[name.lower().replace("_", "-")] = ver
got = subprocess.run(PY2 + ["-c", "import importlib.metadata as m; print('\\n'.join(f\"{d.metadata['Name']}=={d.version}\" "
                            "for d in m.distributions()))"], capture_output=True, text=True).stdout.split()
got = {g.split("==")[0].lower().replace("_", "-"): g.split("==")[1] for g in got}
if got != want:
    refuse(f"the E5b Python environment differs from e5b-py-lock.txt: {sorted(set(got.items()) ^ set(want.items()))}")
for line in (DATA / "inputs.sha256").read_text().splitlines():
    digest, rel, short = line.split()
    if sha((DATA / rel).read_bytes()) != digest or (short in E5A_ZIPS and digest != E5A_ZIPS[short]):
        refuse(f"{rel} does not match its pinned hash")
for line in (DATA / "data-trees.sha256").read_text().splitlines():
    digest, short, _ = line.split()
    root = D / short
    files = sorted(p for p in root.rglob("*") if p.is_file())
    listing = "".join(f"{sha(p.read_bytes())}  {p.relative_to(root)}\n" for p in files)
    if sha(listing.encode()) != digest:
        refuse(f"data tree {short} differs from its record")
for line in (ANN / "annot.sha256").read_text().splitlines():
    digest, name = line.split()
    if sha((ANN / name).read_bytes()) != digest:
        refuse(f"annotation {name} differs from its pin")

norm = FITS / "bix-3_normcount.csv"
JOBS = {
    "light": [("bix-7-q3", PY + [str(E / "bix-7-q3.py"), str(D)]),
              ("bix-14-q2", PY + [str(E / "bix-14-q2.py"), str(D)]),
              ("bix-13-q3", RS + [str(E / "bix-13-q3.R"), str(D)]),
              ("bix-37-q2", PY + [str(E / "bix-37-q2.py"), str(D)]),
              ("bix-52-q3", PY + [str(E / "bix-52-q3.py"), str(D)]),
              ("bix-36-q5", PY + [str(E / "bix-36-q5.py"), str(D)]),
              ("fit-bix-53", RS + [str(E / "bix-53-q3-fit.R"), str(D), str(FITS / "bix-53_fit.csv")]),
              ("bix-53-q3", PY + [str(E / "bix-53-q3.py"), str(FITS / "bix-53_fit.csv"), str(ANN / "KEGG_2019_Mouse.gmt"),
                                  str(ANN / "Mus_musculus.GRCm38.102.gtf.gz"), str(ANN / "Mus_musculus.GRCm39.116.gtf.gz")]),
              ("bix-30-q5", PY2 + [str(E / "bix-30-q5.py"), str(D)])],
    "bix3": [("prep-bix-3", PY + [str(Q / "bix-3-prep.py"), str(D), str(norm)]),
             ("fit-bix-3-q4", RS + [str(E / "bix-3-q4-fit.R"), str(norm), str(FITS / "fits-bix3q4")]),
             ("bix-3-q4", PY + [str(E / "bix-3-q4.py"), str(FITS / "fits-bix3q4")])],
    "bix27": [("bix-27-q2", PY2 + [str(E / "bix-27-q2.py"), str(D)])],
    "origin": [("origin-bix-13-q3", RS + [str(E / "origin" / "bix-13-q3-origin.R"), str(D)]),
               ("origin-bix-14-q2", PY + [str(E / "origin" / "bix-14-q2-origin.py"), str(D)]),
               ("origin-bix-52-q3", PY + [str(E / "origin" / "bix-52-q3-origin.py"), str(D)]),
               ("origin-fit-bix-53", RS + [str(E / "origin" / "bix-53-q3-origin-fit.R"), str(D), str(FITS / "origin-bix53")]),
               ("origin-bix-53-q3", PY + [str(E / "origin" / "bix-53-q3-origin.py"), str(FITS / "origin-bix53"),
                                          str(ANN / "KEGG_2019_Mouse.gmt"), str(ANN / "Mus_musculus.GRCm38.102.gtf.gz"),
                                          str(ANN / "Mus_musculus.GRCm39.116.gtf.gz")]),
               ("origin-bix-3-q4", PY + [str(E / "origin" / "bix-3-q4-probe.py"), str(FITS / "fits-bix3q4")]),
               ("origin-bix-27-q2", PY2 + [str(E / "origin" / "bix-27-q2-origin.py"), str(D)])],
}[STAGE]
if any((OUT / f"{n}.json").exists() for n, _ in JOBS):
    refuse(f"stage {STAGE} rep {REP} already has outputs in {OUT}; use a fresh run folder")
STAGE_FILES = {"light": ["bix-53_fit.csv"], "bix3": ["bix-3_normcount.csv", "fits-bix3q4"], "bix27": [],
               "origin": ["origin-bix53"]}[STAGE]
if any((FITS / n).exists() for n in STAGE_FILES):
    refuse(f"stage {STAGE} rep {REP} already has intermediate files in {FITS}; use a fresh fit folder")
OUT.mkdir(parents=True, exist_ok=True)
FITS.mkdir(parents=True, exist_ok=True)

ENVVARS = {k: v for k, v in os.environ.items() if not k.startswith(("R_", "PYTHON"))}
ENVVARS.update({"R_LIBS_USER": str(ENV / "no-user-lib"), "R_LIBS": "", "R_PROFILE_USER": "/dev/null",
                "R_ENVIRON_USER": "/dev/null", "PYTHONNOUSERSITE": "1", "LC_ALL": "C", "TZ": "America/New_York"})
if not (OUT / "env-r.txt").exists():
    r = subprocess.run(RS + ["-e", "suppressPackageStartupMessages({library(DESeq2); library(apeglm); library(BiocParallel)}); "
                         "print(.libPaths()); print(sessionInfo())"], capture_output=True, text=True, env=ENVVARS)
    (OUT / "env-r.txt").write_text(r.stdout + r.stderr)
    for tag, py in (("env-python.txt", PY), ("env-python-e5b.txt", PY2)):
        p = subprocess.run(py + ["-c", "import importlib.metadata as m, platform, sys; print(sys.version); "
                                 "print(platform.platform()); "
                                 "print('\\n'.join(sorted(f\"{d.metadata['Name']}=={d.version}\" for d in m.distributions())))"],
                           capture_output=True, text=True, env=ENVVARS)
        (OUT / tag).write_text(p.stdout + p.stderr)
log(f"{time.strftime('%Y-%m-%d %H:%M:%S %Z')} stage={STAGE} rep={REP} manifest={MANIFEST} all inputs, scripts and pins verified")

for name, cmd in JOBS:
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, env=ENVVARS)
    (OUT / f"{name}.json").write_text(p.stdout)
    (OUT / f"{name}.stderr").write_text(p.stderr)
    shown = " ".join(c.replace(str(SRC.parent), "<repo>").replace(str(DATA), "<data>").replace(str(FITROOT), "<fits>")
                     for c in cmd)
    log(f"{name} rep={REP} exit={p.returncode} secs={time.time() - t0:.0f} sha256={sha(p.stdout.encode())} cmd={shown}")
    if p.returncode != 0:
        refuse(f"{name} failed; see {OUT / (name + '.stderr')}")
for fdir in sorted(list(FITS.glob("fits-*")) + list(FITS.glob("origin-*"))):
    listing = "".join(f"{sha(f.read_bytes())}  {f.name}\n" for f in sorted(fdir.iterdir()))
    (OUT / f"{fdir.name}.sha256").write_text(listing)
    log(f"{fdir.name} rep={REP} tables={len(list(fdir.iterdir()))} sha256={sha(listing.encode())}")
for f in sorted(FITS.glob("*.csv")):
    log(f"{f.name} rep={REP} sha256={sha(f.read_bytes())}")
