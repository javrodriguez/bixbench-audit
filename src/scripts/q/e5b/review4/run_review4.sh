#!/bin/bash
# E5B-CHANGES-8: reruns adversarial review 4's two probes (copied unchanged) twice under E5B-SCRIPTS-8.sha256,
# single-threaded, isolated R; exit status captured before any substitution (review 4, NIT 1).
# Usage: run_review4.sh <repo_root> <run_dir> <conda_env>
set -uo pipefail
REPO=$1; RUN=$2; ENV=$3
while read -r h f; do [ "$(shasum -a 256 "$REPO/$f" | cut -d' ' -f1)" = "$h" ] || { echo "REFUSED: $f differs"; exit 2; }; done < "$REPO/src/prereg/E5B-SCRIPTS-8.sha256"
[ ! -e "$RUN/r1" ] || { echo "REFUSED: $RUN has outputs"; exit 2; }
export R_LIBS_USER="$ENV/no-user-lib" R_LIBS="" R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null LC_ALL=C TZ=America/New_York
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
Q="$REPO/src/scripts/q/e5b/review4"
for rep in 1 2; do
  mkdir -p "$RUN/r$rep"
  for p in p52_zf_r p3_apeglm; do
    "$ENV/bin/Rscript" --vanilla "$Q/$p.R" > "$RUN/r$rep/$p.txt" 2> "$RUN/r$rep/$p.stderr"; rc=$?
    echo "$(date '+%H:%M:%S') $p rep=$rep exit=$rc" >> "$RUN/log.txt"
  done
done
# p3_apeglm prints elapsed times, which differ between runs; compare its lines without the timing lines.
cmp -s "$RUN/r1/p52_zf_r.txt" "$RUN/r2/p52_zf_r.txt" && echo "p52_zf_r identical" | tee -a "$RUN/log.txt" || echo "p52_zf_r DIFFERENT" | tee -a "$RUN/log.txt"
cmp -s <(grep -v "mins\|secs" "$RUN/r1/p3_apeglm.txt") <(grep -v "mins\|secs" "$RUN/r2/p3_apeglm.txt") && echo "p3_apeglm identical (timing lines excluded)" | tee -a "$RUN/log.txt" || echo "p3_apeglm DIFFERENT" | tee -a "$RUN/log.txt"
