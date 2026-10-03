#!/bin/bash
# E5B-CHANGES-7: runs bix-52-q3-zf-lengths.py twice, single-threaded, under E5B-SCRIPTS-7.sha256.
# Usage: run_zf.sh <repo_root> <run_dir> <conda_env> <data_root> <assembly_report>
set -uo pipefail
REPO=$1; RUN=$2; ENV=$3; DATA=$4; REP_FILE=$5
while read -r h f; do [ "$(shasum -a 256 "$REPO/$f" | cut -d' ' -f1)" = "$h" ] || { echo "REFUSED: $f differs"; exit 2; }; done < "$REPO/src/prereg/E5B-SCRIPTS-7.sha256"
[ "$(shasum -a 256 "$REP_FILE" | cut -d' ' -f1)" = "0e604246c7202f62bfb49dcec3b1d4351d5f197c605b1c414cfe20a5f0961655" ] || { echo "REFUSED: assembly report differs from its pin"; exit 2; }
[ ! -e "$RUN/r1" ] || { echo "REFUSED: $RUN has outputs"; exit 2; }
export PYTHONNOUSERSITE=1 LC_ALL=C OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
for rep in 1 2; do
  mkdir -p "$RUN/r$rep"
  "$ENV/bin/python" -s -P "$REPO/src/scripts/q/e5b/origin/bix-52-q3-zf-lengths.py" "$DATA" "$REP_FILE" > "$RUN/r$rep/zf-lengths.json" 2> "$RUN/r$rep/zf-lengths.stderr"
  echo "$(date '+%H:%M:%S') zf-lengths rep=$rep exit=$? sha256=$(shasum -a 256 "$RUN/r$rep/zf-lengths.json" | cut -d' ' -f1)" >> "$RUN/log.txt"
done
cmp -s "$RUN/r1/zf-lengths.json" "$RUN/r2/zf-lengths.json" && echo "zf-lengths identical" | tee -a "$RUN/log.txt" || echo "zf-lengths DIFFERENT" | tee -a "$RUN/log.txt"
