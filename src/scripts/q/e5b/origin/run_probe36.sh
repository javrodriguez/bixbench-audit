#!/bin/bash
# E5B-CHANGES-4: runs the bix-36-q5 origin probe twice (r1, r2) in the pinned conda environment, isolated as
# run_e5b.py does, logging command, exit status and output hash. Refuses if E5B-SCRIPTS-4.sha256 does not match.
# Usage: run_probe36.sh <repo_root> <data_root> <run_dir> <fit_dir> <conda_env>
set -euo pipefail
REPO=$1; DATA=$2; RUN=$3; FITS=$4; ENV=$5
while read -r h f; do [ "$(shasum -a 256 "$REPO/$f" | cut -d' ' -f1)" = "$h" ] || { echo "REFUSED: $f differs"; exit 2; }; done < "$REPO/src/prereg/E5B-SCRIPTS-4.sha256"
[ ! -e "$RUN/r1" ] || { echo "REFUSED: $RUN has outputs"; exit 2; }
export R_LIBS_USER="$ENV/no-user-lib" R_LIBS="" R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null PYTHONNOUSERSITE=1 LC_ALL=C TZ=America/New_York
for rep in 1 2; do
  mkdir -p "$RUN/r$rep" "$FITS/r$rep"
  echo "$(date '+%Y-%m-%d %H:%M:%S %Z') probe36 rep=$rep start" >> "$RUN/log.txt"
  "$ENV/bin/Rscript" --vanilla "$REPO/src/scripts/q/e5b/origin/bix-36-q5-origin-fit.R" "$DATA" "$FITS/r$rep/bix-36-q5-lfc.csv" > "$RUN/r$rep/origin-fit-bix-36-q5.json" 2> "$RUN/r$rep/origin-fit-bix-36-q5.stderr"
  echo "origin-fit-bix-36-q5 rep=$rep exit=$? lfc_sha256=$(shasum -a 256 "$FITS/r$rep/bix-36-q5-lfc.csv" | cut -d' ' -f1)" >> "$RUN/log.txt"
  "$ENV/bin/python" -s -P "$REPO/src/scripts/q/e5b/origin/bix-36-q5-origin.py" "$FITS/r$rep/bix-36-q5-lfc.csv" > "$RUN/r$rep/origin-bix-36-q5.json" 2> "$RUN/r$rep/origin-bix-36-q5.stderr"
  echo "origin-bix-36-q5 rep=$rep exit=$? sha256=$(shasum -a 256 "$RUN/r$rep/origin-bix-36-q5.json" | cut -d' ' -f1)" >> "$RUN/log.txt"
done
cmp "$RUN/r1/origin-bix-36-q5.json" "$RUN/r2/origin-bix-36-q5.json" && cmp "$FITS/r1/bix-36-q5-lfc.csv" "$FITS/r2/bix-36-q5-lfc.csv" && echo "probe36: r1 = r2 byte-identical" | tee -a "$RUN/log.txt"
