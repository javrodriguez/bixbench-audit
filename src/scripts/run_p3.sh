#!/bin/bash
# Runs the P3 reading twice (CHANGES-8): fit, then the three question readings, per repetition.
# Isolation as run_recorded_v2.py: pinned env, R --vanilla with the user library hidden, Python -s -P.
# Usage: run_p3.sh <lane_root>
set -euo pipefail
L="$1"
RUN="$L/runs/recorded-2026-09-30-p3"
NORM="$L/runs/recorded-2026-09-30-bix3/r1/bix-3_normcount.csv"
test ! -e "$RUN" || { echo "REFUSED: $RUN exists"; exit 2; }
"$L/env/bin/python" -s -P - "$L" <<'PY'
import hashlib, pathlib, sys
L = pathlib.Path(sys.argv[1])
for m in ("SCRIPTS-8.sha256",):
    for line in (L / "prereg" / m).read_text().splitlines():
        h, p = line.split()
        if hashlib.sha256((L / p).read_bytes()).hexdigest() != h:
            sys.exit(f"REFUSED: {p} differs from {m}")
print("pins verified")
PY
export R_LIBS_USER="$L/env/no-user-lib" R_LIBS="" R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null PYTHONNOUSERSITE=1 LC_ALL=C TZ=America/New_York
for rep in 1 2; do
  mkdir -p "$RUN/r$rep"
  t0=$(date +%s)
  "$L/env/bin/Rscript" --vanilla "$L/scripts/q/bix-3-fit-p3.R" "$NORM" "$RUN/r$rep/fits-p3" > "$RUN/r$rep/fit-p3.log" 2> "$RUN/r$rep/fit-p3.stderr"
  "$L/env/bin/python" -s -P "$L/scripts/q/bix-3-p3.py" "$RUN/r$rep/fits-p3" > "$RUN/r$rep/bix-3-p3.jsonl" 2> "$RUN/r$rep/bix-3-p3.stderr"
  (cd "$RUN/r$rep/fits-p3" && shasum -a 256 *.csv) > "$RUN/r$rep/fits-p3.sha256"
  echo "$(date '+%F %T %Z') rep=$rep secs=$(( $(date +%s) - t0 )) out=$(shasum -a 256 "$RUN/r$rep/bix-3-p3.jsonl" | cut -d' ' -f1) fits=$(shasum -a 256 "$RUN/r$rep/fits-p3.sha256" | cut -d' ' -f1)" | tee -a "$RUN/log.txt"
done
cmp "$RUN/r1/bix-3-p3.jsonl" "$RUN/r2/bix-3-p3.jsonl" && cmp "$RUN/r1/fits-p3.sha256" "$RUN/r2/fits-p3.sha256" && echo "P3 r1 = r2 identical" | tee -a "$RUN/log.txt"
