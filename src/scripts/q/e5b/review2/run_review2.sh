#!/bin/bash
# E5B-CHANGES-6: reruns adversarial review 2's three probes (copied unchanged) twice under E5B-SCRIPTS-6.sha256,
# single-threaded (the orchestrator's cap: at most 4 workers, BLAS threads 1), into r1/ and r2/, compared byte for byte.
# Usage: run_review2.sh <repo_root> <run_dir> <conda_env> <env2_venv> <data_root>
set -uo pipefail
REPO=$1; RUN=$2; ENV=$3; PY2=$4; DATA=$5
while read -r h f; do [ "$(shasum -a 256 "$REPO/$f" | cut -d' ' -f1)" = "$h" ] || { echo "REFUSED: $f differs"; exit 2; }; done < "$REPO/src/prereg/E5B-SCRIPTS-6.sha256"
[ ! -e "$RUN/r1" ] || { echo "REFUSED: $RUN has outputs"; exit 2; }
export R_LIBS_USER="$ENV/no-user-lib" R_LIBS="" R_PROFILE_USER=/dev/null R_ENVIRON_USER=/dev/null PYTHONNOUSERSITE=1 LC_ALL=C TZ=America/New_York
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
Q="$REPO/src/scripts/q/e5b/review2"
for rep in 1 2; do
  mkdir -p "$RUN/r$rep"
  "$ENV/bin/Rscript" --vanilla "$Q/p52_r.R" "$DATA" > "$RUN/r$rep/p52_r.txt" 2> "$RUN/r$rep/p52_r.stderr"; echo "$(date '+%H:%M:%S') p52_r rep=$rep exit=$?" >> "$RUN/log.txt"
  "$ENV/bin/Rscript" --vanilla "$Q/p52_witness.R" "$DATA" > "$RUN/r$rep/p52_witness.txt" 2> "$RUN/r$rep/p52_witness.stderr"; echo "$(date '+%H:%M:%S') p52_witness rep=$rep exit=$?" >> "$RUN/log.txt"
  "$PY2/bin/python" -s -P "$Q/q27_l3seeds.py" "$DATA" complete 0,1,2,3,5,6,8,9,11,12,42,2024 > "$RUN/r$rep/q27_l3seeds.txt" 2> "$RUN/r$rep/q27_l3seeds.stderr"; echo "$(date '+%H:%M:%S') q27_l3seeds rep=$rep exit=$?" >> "$RUN/log.txt"
done
for f in p52_r.txt p52_witness.txt q27_l3seeds.txt; do cmp -s "$RUN/r1/$f" "$RUN/r2/$f" && echo "$f identical" || echo "$f DIFFERENT"; done | tee -a "$RUN/log.txt"
